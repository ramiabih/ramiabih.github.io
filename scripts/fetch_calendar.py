#!/usr/bin/env python3
"""Fetch Rami's Google Calendar meetings and write calendar-data.json.

Run by the GitHub Action (.github/workflows/calendar.yml) on a schedule.
Reads three secrets from the environment:
  GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN
No third-party libraries — standard library only.

Privacy: the file it writes contains ONLY per-day counts and a few totals.
No meeting titles, attendees, or descriptions ever leave this script, so the
public website never exposes anything about what the meetings actually are.

"A meeting" here means a timed event that has at least one OTHER person
invited (not just Rami) and that Rami hasn't declined. Solo focus blocks and
self-bookings are skipped on purpose.
"""
import json, os, sys, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

CID = os.environ.get("GOOGLE_CLIENT_ID")
CSECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REFRESH = os.environ.get("GOOGLE_REFRESH_TOKEN")
if not (CID and CSECRET and REFRESH):
    sys.exit("Missing GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET / GOOGLE_REFRESH_TOKEN")

WINDOW_DAYS = 365


def get_token():
    body = urllib.parse.urlencode({
        "client_id": CID,
        "client_secret": CSECRET,
        "refresh_token": REFRESH,
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token", data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    return json.load(urllib.request.urlopen(req, timeout=30))["access_token"]


def api(token, path, params=None):
    url = "https://www.googleapis.com/calendar/v3" + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
    return json.load(urllib.request.urlopen(req, timeout=30))


def is_meeting(event, self_email):
    """True if this is a timed event with >=1 other invitee that Rami didn't decline."""
    if event.get("status") == "cancelled":
        return False
    if "dateTime" not in event.get("start", {}):
        return False  # all-day events (birthdays, OOO, holidays) aren't meetings
    attendees = event.get("attendees", [])
    others = 0
    for a in attendees:
        if a.get("resource"):
            continue  # meeting rooms / equipment, not people
        is_self = a.get("self") or a.get("email", "").lower() == self_email.lower()
        if is_self:
            if a.get("responseStatus") == "declined":
                return False  # Rami declined — doesn't count
            continue
        others += 1
    return others >= 1


def main():
    token = get_token()

    cal = api(token, "/calendars/primary")
    self_email = cal.get("id", "")
    tz = ZoneInfo(cal.get("timeZone", "UTC"))

    now = datetime.now(timezone.utc)
    time_min = (now - timedelta(days=WINDOW_DAYS)).isoformat().replace("+00:00", "Z")
    time_max = now.isoformat().replace("+00:00", "Z")

    counts = {}
    total = 0
    page_token = None
    while True:
        params = {
            "timeMin": time_min,
            "timeMax": time_max,
            "singleEvents": "true",   # expand recurring events into instances
            "showDeleted": "false",
            "maxResults": "2500",
        }
        if page_token:
            params["pageToken"] = page_token
        data = api(token, "/calendars/primary/events", params)
        for ev in data.get("items", []):
            if not is_meeting(ev, self_email):
                continue
            start = datetime.fromisoformat(ev["start"]["dateTime"])
            key = start.astimezone(tz).date().isoformat()
            counts[key] = counts.get(key, 0) + 1
            total += 1
        page_token = data.get("nextPageToken")
        if not page_token:
            break

    busiest = max(counts.items(), key=lambda kv: kv[1], default=None)
    out = {
        "updated": now.isoformat(),
        "timezone": str(tz),
        "window_days": WINDOW_DAYS,
        "window_start": (now - timedelta(days=WINDOW_DAYS)).astimezone(tz).date().isoformat(),
        "window_end": now.astimezone(tz).date().isoformat(),
        "total": total,
        "avg_per_day": round(total / WINDOW_DAYS, 1),
        "busiest": {"date": busiest[0], "count": busiest[1]} if busiest else None,
        "counts": dict(sorted(counts.items())),
    }
    with open("calendar-data.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"wrote calendar-data.json: {total} meetings across {len(counts)} days")


if __name__ == "__main__":
    main()
