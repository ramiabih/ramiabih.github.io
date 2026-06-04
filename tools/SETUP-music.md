# Music tab — one-time setup

The Music page reads `music-data.json`, which a GitHub Action refreshes from Spotify
every 6 hours. To turn it on you do three things once: make a Spotify app, get a
refresh token, and add three secrets to GitHub. ~10 minutes.

> **Heads-up (Feb 2026):** Spotify now requires a **Premium** account to use
> Developer Mode. Build the app on your Premium account. The endpoints this uses
> (top tracks/artists, recently played) and the `127.0.0.1` redirect URI below are
> all still current.

## 1. Create a Spotify app
1. Go to https://developer.spotify.com/dashboard and log in (Premium account).
2. Click **Create app**. Name it anything (e.g. "ramiabih.com").
3. In settings, add this exact **Redirect URI**:
   ```
   http://127.0.0.1:8888/callback
   ```
4. Save. Copy the **Client ID** and **Client Secret**.

## 2. Get your refresh token (run once on your Mac)
In Terminal, from the repo folder:
```
export SPOTIFY_CLIENT_ID=paste_client_id
export SPOTIFY_CLIENT_SECRET=paste_client_secret
python3 tools/get_spotify_refresh_token.py
```
Your browser opens → click **Agree**. The terminal prints a long **refresh token**.
Copy it.

## 3. Add the three secrets to GitHub
Either in the browser — repo → **Settings → Secrets and variables → Actions → New
repository secret** — add these three:
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_REFRESH_TOKEN`

…or in Terminal with the GitHub CLI (replace the values):
```
gh secret set SPOTIFY_CLIENT_ID --body "your_client_id"
gh secret set SPOTIFY_CLIENT_SECRET --body "your_client_secret"
gh secret set SPOTIFY_REFRESH_TOKEN --body "your_refresh_token"
```

## 4. Run it
Repo → **Actions → "Update Spotify data" → Run workflow**. After ~30 seconds it
commits a fresh `music-data.json` and the Music page fills in. After that it runs
on its own every 6 hours.

Notes:
- The secrets live only in GitHub Actions — they are never in the website or exposed.
- Spotify gives top tracks/artists for ~last month / 6 months / all-time, plus your
  last 50 plays. It has no deeper per-song history, so that's the ceiling here.
