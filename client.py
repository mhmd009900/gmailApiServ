from fastapi import APIRouter, Query, Depends, HTTPException
from database import get_db
from models import APIToken
from gmail_reader import gmail_login_and_fetch
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/fetch")
def fetch_emails(token: str, db: Session = Depends(get_db)):
    record = db.query(APIToken).filter_by(token=token, is_active=True).first()
    if not record:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    query = "subject:registration" if record.permission_type == "registration" else "subject:facebook"
    emails = gmail_login_and_fetch(record.gmail_account, query)

    for email in emails:
        headers = {h['name']: h['value'] for h in email['headers']}
        subject = headers.get("Subject", "").lower()
        if record.permission_type in subject:
            record.disable_after = datetime.utcnow() + timedelta(minutes=10)
            db.commit()
            break

    return [{
        "from": h.get("From"),
        "subject": h.get("Subject"),
        "date": h.get("Date"),
        "snippet": m["snippet"]
    } for m in emails for h in [dict((x['name'], x['value']) for x in m['headers'])]]
