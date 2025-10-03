import os, pickle
from urllib.parse import parse_qs, urlparse
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

TOKEN_FILE = "token.pickle"
SCOPES = ["https://www.googleapis.com/auth/drive"]
REDIRECT_URI = "http://localhost:53682/"

creds = None
if os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE, "rb") as f:
        creds = pickle.load(f)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES, redirect_uri=REDIRECT_URI)
        auth_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
        )
        print("\nOpen this URL in your browser, approve, then copy the FINAL redirected URL (with ?code=...):\n")
        print(auth_url, "\n")
        redirected = input("Paste the FULL redirected URL here:\n> ").strip()
        code = parse_qs(urlparse(redirected).query).get("code", [None])[0]
        if not code:
            raise SystemExit("No 'code' in pasted URL.")
        flow.fetch_token(code=code)
        creds = flow.credentials

    with open(TOKEN_FILE, "wb") as f:
        pickle.dump(creds, f)

print("✅ token.pickle created/refreshed successfully.")
