#!/usr/bin/env python3
"""One-time helper: get a Google REFRESH TOKEN for the website's GitHub Action.

You only run this once, on your own Mac. It opens Google in your browser,
you click "Allow", and it prints a refresh token to paste into GitHub secrets.

Setup before running (see tools/SETUP-calendar.md for the full walkthrough):
  1. In Google Cloud Console, enable the Google Calendar API.
  2. Create an OAuth client of type "Desktop app".
  3. In the OAuth consent screen, add yourself as a Test user.
  4. Copy the client's Client ID and Client Secret.

Run:
  export GOOGLE_CLIENT_ID=your_client_id
  export GOOGLE_CLIENT_SECRET=your_client_secret
  python3 tools/get_google_refresh_token.py
"""
import http.server, json, os, secrets, sys, urllib.parse, urllib.request, webbrowser

CID = os.environ.get("GOOGLE_CLIENT_ID")
CSECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
if not CID or not CSECRET:
    sys.exit("Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables first.")

REDIRECT = "http://127.0.0.1:8888/callback"
SCOPES = "https://www.googleapis.com/auth/calendar.readonly"
state = secrets.token_urlsafe(8)

auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
    "client_id": CID,
    "response_type": "code",
    "redirect_uri": REDIRECT,
    "scope": SCOPES,
    "state": state,
    "access_type": "offline",   # required to receive a refresh token
    "prompt": "consent",        # force a refresh token even on re-auth
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
    "client_id": CID,
    "client_secret": CSECRET,
    "code": code,
    "redirect_uri": REDIRECT,
    "grant_type": "authorization_code",
}).encode()
req = urllib.request.Request(
    "https://oauth2.googleapis.com/token", data=body,
    headers={"Content-Type": "application/x-www-form-urlencoded"})
tok = json.load(urllib.request.urlopen(req, timeout=30))

if "refresh_token" not in tok:
    sys.exit("No refresh token returned. Revoke the app's access at "
             "https://myaccount.google.com/permissions and run this again.")

print("\n" + "=" * 60)
print("YOUR REFRESH TOKEN (save as the GOOGLE_REFRESH_TOKEN secret):\n")
print(tok["refresh_token"])
print("=" * 60)
