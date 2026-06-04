#!/usr/bin/env python3
"""One-time helper: get a Spotify REFRESH TOKEN for the website's GitHub Action.

You only run this once, on your own Mac. It opens Spotify in your browser,
you click "Agree", and it prints a refresh token to paste into GitHub secrets.

Setup before running:
  1. Create an app at https://developer.spotify.com/dashboard
  2. In the app settings, add this Redirect URI exactly:
        http://127.0.0.1:8888/callback
  3. Copy the app's Client ID and Client Secret.

Run:
  export SPOTIFY_CLIENT_ID=your_client_id
  export SPOTIFY_CLIENT_SECRET=your_client_secret
  python3 tools/get_spotify_refresh_token.py
"""
import base64, http.server, json, os, secrets, sys, urllib.parse, urllib.request, webbrowser

CID = os.environ.get("SPOTIFY_CLIENT_ID")
CSECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
if not CID or not CSECRET:
    sys.exit("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables first.")

REDIRECT = "http://127.0.0.1:8888/callback"
SCOPES = "user-top-read user-read-recently-played"
state = secrets.token_urlsafe(8)

auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
    "client_id": CID,
    "response_type": "code",
    "redirect_uri": REDIRECT,
    "scope": SCOPES,
    "state": state,
})

holder = {}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        if params.get("state", [None])[0] != state:
            self.wfile.write(b"State mismatch. Close and re-run.")
            return
        holder["code"] = params.get("code", [None])[0]
        self.wfile.write(b"<h2>Done.</h2><p>Close this tab and return to your terminal.</p>")

    def log_message(self, *a):
        pass


print("Opening browser to authorize. If it doesn't open, paste this URL:\n\n" + auth_url + "\n")
webbrowser.open(auth_url)
http.server.HTTPServer(("127.0.0.1", 8888), Handler).handle_request()

code = holder.get("code")
if not code:
    sys.exit("No authorization code received.")

body = urllib.parse.urlencode({
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": REDIRECT,
}).encode()
auth = base64.b64encode(f"{CID}:{CSECRET}".encode()).decode()
req = urllib.request.Request(
    "https://accounts.spotify.com/api/token", data=body,
    headers={"Authorization": "Basic " + auth,
             "Content-Type": "application/x-www-form-urlencoded"})
tok = json.load(urllib.request.urlopen(req, timeout=30))

print("\n" + "=" * 60)
print("YOUR REFRESH TOKEN (save as the SPOTIFY_REFRESH_TOKEN secret):\n")
print(tok["refresh_token"])
print("=" * 60)
