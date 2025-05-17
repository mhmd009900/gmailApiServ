from fastapi import FastAPI, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from auth import authenticate_admin, create_api_tokens, get_token, disable_token
from database import SessionLocal, engine, Base
from models import GmailAccount
from gmail_client import get_gmail_service
from schemas import TokenCreateRequest, TokenResponse
from datetime import datetime, timedelta
import json
from init_db import init_db
Base.metadata.create_all(bind=engine)
init_db()
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/admin/create-tokens", status_code=201)
def admin_create_tokens(request: TokenCreateRequest, db: Session = Depends(get_db), 
                        admin_email: str = Header(...), admin_password: str = Header(...)):
    admin = authenticate_admin(db, admin_email, admin_password)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")

    # جلب جميع حسابات Gmail IDs (يمكنك تخصيص اختيار الحسابات حسب طلبك)
    gmail_accounts = db.query(GmailAccount).all()
    gmail_ids = [acc.id for acc in gmail_accounts]

    tokens = create_api_tokens(db, request.client_email, request.number_of_tokens, request.permissions, gmail_ids)

    return [ {"token": t.token, "status": t.status, "created_at": t.created_at} for t in tokens]

@app.get("/emails")
def read_emails(token: str = Header(...), db: Session = Depends(get_db)):
    api_token = get_token(db, token)
    if not api_token:
        raise HTTPException(status_code=403, detail="Invalid or disabled token")

    # جلب بيانات الاعتماد الخاصة بحسابات Gmail المرتبطة بالتوكن
    emails = []
    for gmail_acc_id in api_token.gmail_account_ids:
        gmail_acc = db.query(GmailAccount).filter(GmailAccount.id == gmail_acc_id).first()
        if not gmail_acc:
            continue

        service = get_gmail_service(gmail_acc.credentials_json, gmail_acc.token_json)
        # استدعاء API لاسترجاع رسائل (مثال فقط، قم بتطوير حسب حاجتك)
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])

        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            snippet = msg_data.get('snippet')
            # تحقق من وجود رسالة "registration" أو "facebook" حسب الصلاحيات
            # إذا وجدتها: اعطل التوكن بعد 10 دقائق (يمكن تنفيذ لوجيك مع الـ background task)
            emails.append({
                "gmail_account": gmail_acc.email,
                "snippet": snippet
            })

    return emails
