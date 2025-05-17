import os, json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_credentials_for(gmail_account: str):
    creds_json = os.getenv(f"CREDENTIALS_{gmail_account}")
    token_json = os.getenv(f"TOKEN_{gmail_account}")
    if not creds_json or not token_json:
        raise ValueError("Missing credentials or token for " + gmail_account)
    creds = Credentials.from_authorized_user_info(json.loads(token_json))
    return creds

def read_gmail_for_registration(gmail_account: str) -> bool:
    creds = get_credentials_for(gmail_account)
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", q="subject:registration", maxResults=1).execute()
    return bool(results.get("messages", []))
