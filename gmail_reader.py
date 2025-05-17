from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import List
import os
import base64
from email import message_from_bytes

def gmail_login_and_fetch(gmail_account: str, query: str, max_results: int = 10):
    creds_env = os.getenv(f"GMAIL_CREDS_{gmail_account}")
    token_env = os.getenv(f"GMAIL_TOKEN_{gmail_account}")
    
    if not creds_env or not token_env:
        raise Exception("Missing credentials or token for Gmail")

    creds = Credentials.from_authorized_user_info(eval(token_env), scopes=["https://www.googleapis.com/auth/gmail.readonly"])
    service = build("gmail", "v1", credentials=creds)

    result = service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
    messages = result.get("messages", [])
    output = []

    for msg in messages:
        msg_detail = service.users().messages().get(userId="me", id=msg["id"], format="full").execute()
        snippet = msg_detail.get("snippet", "")
        headers = msg_detail["payload"].get("headers", [])
        output.append({"headers": headers, "snippet": snippet})

    return output
