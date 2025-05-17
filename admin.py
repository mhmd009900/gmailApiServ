from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import AdminUser, APIToken
from utils.auth import hash_password, verify_password
from utils.token_utils import generate_token
import os
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/create-admin")
def create_admin(email: str, password: str, db: Session = Depends(get_db)):
    if db.query(AdminUser).filter_by(email=email).first():
        raise HTTPException(status_code=400, detail="Admin already exists")
    db.add(AdminUser(email=email, hashed_password=hash_password(password)))
    db.commit()
    return {"message": "Admin created"}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    admin = db.query(AdminUser).filter_by(email=email).first()
    if not admin or not verify_password(password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

@router.post("/generate-tokens")
def generate_tokens(admin_email: str, admin_password: str, client_email: str, count: int, permission_type: str, db: Session = Depends(get_db)):
    admin = db.query(AdminUser).filter_by(email=admin_email).first()
    if not admin or not verify_password(admin_password, admin.hashed_password):
        raise HTTPException(status_code=403, detail="Invalid admin credentials")
    gmail_accounts = os.getenv("GMAIL_ACCOUNTS", "").split(",")
    if len(gmail_accounts) < count:
        raise HTTPException(status_code=400, detail="Not enough Gmail accounts")
    tokens = []
    for i in range(count):
        token = APIToken(
            token=generate_token(),
            client_email=client_email,
            permission_type=permission_type,
            gmail_account=gmail_accounts[i].strip(),
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        db.add(token)
        tokens.append(token.token)
    db.commit()
    return {"tokens": tokens}

@router.get("/list-admins")
def list_admins(db: Session = Depends(get_db)):
    admins = db.query(AdminUser).all()
    return [{"email": a.email, "id": a.id} for a in admins]
