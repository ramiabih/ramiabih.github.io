#!/usr/bin/env python3
"""Fetch Rami's Spotify listening data and write music-data.json.

Run by the GitHub Action (.github/workflows/spotify.yml) on a schedule.
Reads three secrets from the environment:
  SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REFRESH_TOKEN
No third-party libraries — standard library only.
"""
import base64, json, os, sys, urllib.parse, urllib.request
from datetime import datetime, timezone

CID = os.environ.get("SPOTIFY_CLIENT_ID")
CSECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
REFRESH = os.environ.get("SPOTIFY_REFRESH_TOKEN")
if not (CID and CSECRET and REFRESH):
    sys.exit("Missing SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET / SPOTIFY_REFRESH_TOKEN")


def get_token():
    body = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": REFRESH,
    }).encode()
    auth = base64.b64encode(f"{CID}:{CSECRET}".encode()).decode()
    req = urllib.request.Request(
        "https://accounts.spotify.com/api/token", data=body,
        headers={"Authorization": "Basic " + auth,
                 "Content-Type": "application/x-www-form-urlencoded"})
    return json.load(urllib.request.urlopen(req, timeout=30))["access_token"]


def api(token, path):
    req = urllib.request.Request("https://api.spotify.com/v1" + path,
                                 headers={"Authorization": "Bearer " + token})
    return json.load(urllib.request.urlopen(req, timeout=30))


def img(images):
    return images[0]["url"] if images else ""


def track_obj(t):
    return {
        "name": t["name"],
        "artists": ", ".join(a["name"] for a in t["artists"]),
        "album": t["album"]["name"],
        "image": img(t["album"]["images"]),
        "url": t["external_urls"].get("spotify", ""),
    }


def artist_obj(a):
    return {
        "name": a["name"],
        "image": img(a["images"]),
        "url": a["external_urls"].get("spotify", ""),
        "genres": a.get("genres", []),
    }


def main():
    token = get_token()
    ranges = {}
    for r in ("short_term", "medium_term", "long_term"):
        tracks = api(token, f"/me/top/tracks?time_range={r}&limit=20").get("items", [])
        artists = api(token, f"/me/top/artists?time_range={r}&limit=20").get("items", [])
        ranges[r] = {
            "tracks": [track_obj(t) for t in tracks],
            "artists": [artist_obj(a) for a in artists],
        }

    recent_items = api(token, "/me/player/recently-played?limit=50").get("items", [])
    recent = [{
        "name": i["track"]["name"],
        "artists": ", ".join(a["name"] for a in i["track"]["artists"]),
        "image": img(i["track"]["album"]["images"]),
        "url": i["track"]["external_urls"].get("spotify", ""),
        "played_at": i["played_at"],
    } for i in recent_items]

    out = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "ranges": ranges,
        "recent": recent,
    }
    with open("music-data.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print("wrote music-data.json:",
          {k: len(v["tracks"]) for k, v in ranges.items()}, "| recent:", len(recent))


if __name__ == "__main__":
    main()
