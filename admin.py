from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import AdminUser, APIToken
from auth import hash_password, verify_password
from token_utils import generate_token
from datetime import datetime
import os

router = APIRouter()

@router.post("/create_admin")
def create_admin(email: str, password: str, db: Session = Depends(get_db)):
    if db.query(AdminUser).filter_by(email=email).first():
        raise HTTPException(status_code=400, detail="Admin already exists")
    hashed = hash_password(password)
    admin = AdminUser(email=email, hashed_password=hashed)
    db.add(admin)
    db.commit()
    return {"message": "Admin created"}
@router.get("/list-admins")
def list_admins(db: Session = Depends(get_db)):
    admins = db.query(AdminUser).all()
    return [{"email": admin.email, "id": admin.id} for admin in admins]

@router.post("/generate_tokens")
def generate_tokens(admin_email: str, admin_password: str, client_email: str, count: int, permission_type: str, db: Session = Depends(get_db)):
    admin = db.query(AdminUser).filter_by(email=admin_email).first()
    if not admin or not verify_password(admin_password, admin.hashed_password):
        raise HTTPException(status_code=403, detail="Invalid admin credentials")

    gmail_accounts = os.getenv("GMAIL_ACCOUNTS").split(",")
    if len(gmail_accounts) < count:
        raise HTTPException(status_code=400, detail="Not enough Gmail accounts")

    tokens = []
    for i in range(count):
        token_str = generate_token()
        token = APIToken(
            token=token_str,
            client_email=client_email,
            permission_type=permission_type,
            gmail_account=gmail_accounts[i].strip()
        )
        db.add(token)
        tokens.append(token_str)
    db.commit()
    return {"tokens": tokens}
