import os
import tempfile
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def load_credentials_from_json_strings(credentials_json: str, token_json: str):
    # كتابة ملفات مؤقتة
    creds_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    token_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")

    creds_file.write(credentials_json.encode())
    creds_file.flush()

    token_file.write(token_json.encode())
    token_file.flush()

    return creds_file.name, token_file.name

def get_gmail_service(credentials_json: str, token_json: str):
    creds_path, token_path = load_credentials_from_json_strings(credentials_json, token_json)
    creds = Credentials.from_authorized_user_file(token_path, scopes=["https://www.googleapis.com/auth/gmail.readonly"])
    service = build('gmail', 'v1', credentials=creds)
    return service
