# Meeting Activity tab — one-time setup

The Meeting Activity page reads `calendar-data.json`, which a GitHub Action
refreshes from your Google Calendar every 6 hours. To turn it on you do three
things once: make a Google OAuth app, get a refresh token, and add three
secrets to GitHub. ~10 minutes.

Only **per-day counts** are ever written to the website — no meeting titles,
attendees, or details. And only meetings with **at least one other person
invited** are counted, so solo focus blocks don't pad the numbers.

## 1. Create a Google OAuth app
1. Go to https://console.cloud.google.com and create (or pick) a project.
2. **APIs & Services → Library** → search **Google Calendar API** → **Enable**.
3. **APIs & Services → OAuth consent screen**:
   - User type: **External**, then create.
   - Fill in the app name and your email where required.
   - On **Test users**, add your own Google account. (Test mode is fine — you're
     the only user. Refresh tokens for unverified apps in test mode last until
     revoked, so re-run step 2 below if it ever stops syncing.)
4. **APIs & Services → Credentials → Create credentials → OAuth client ID**:
   - Application type: **Desktop app**. Name it anything.
   - Create, then copy the **Client ID** and **Client Secret**.

## 2. Get your refresh token (run once on your Mac)
In Terminal, from the repo folder:
```
export GOOGLE_CLIENT_ID=paste_client_id
export GOOGLE_CLIENT_SECRET=paste_client_secret
python3 tools/get_google_refresh_token.py
```
Your browser opens → pick your account → click **Allow** (you may see an
"unverified app" warning since it's only you — click **Advanced → Continue**).
The terminal prints a long **refresh token**. Copy it.

## 3. Add the three secrets to GitHub
Either in the browser — repo → **Settings → Secrets and variables → Actions → New
repository secret** — add these three:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REFRESH_TOKEN`

…or in Terminal with the GitHub CLI (replace the values):
```
gh secret set GOOGLE_CLIENT_ID --body "your_client_id"
gh secret set GOOGLE_CLIENT_SECRET --body "your_client_secret"
gh secret set GOOGLE_REFRESH_TOKEN --body "your_refresh_token"
```

## 4. Run it
Repo → **Actions → "Update calendar data" → Run workflow**. After ~30 seconds it
commits a fresh `calendar-data.json` and the Meeting Activity page fills in.
After that it runs on its own every 6 hours.

Notes:
- The secrets live only in GitHub Actions — they are never in the website or exposed.
- The published JSON is just `{ date: count }` plus a few totals. No event
  titles or attendees are ever written, so nothing private leaves your machine.
- "A meeting" = a timed event with at least one other invitee that you haven't
  declined. Tweak the rule in `scripts/fetch_calendar.py` (`is_meeting`).
- It pulls the last 5 calendar years so the page can show a year picker.
  Change `HISTORY_YEARS` in the same file.
