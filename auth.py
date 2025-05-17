import secrets
from sqlalchemy.orm import Session
from models import ApiToken, Admin
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def create_admin(db: Session, email: str, password: str):
    hashed = hash_password(password)
    admin = Admin(email=email, password_hash=hashed)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

def authenticate_admin(db: Session, email: str, password: str):
    admin = db.query(Admin).filter(Admin.email == email).first()
    if not admin:
        return False
    if not verify_password(password, admin.password_hash):
        return False
    return admin

def create_api_tokens(db: Session, client_email: str, number: int, permissions: dict, gmail_account_ids: list):
    tokens = []
    for _ in range(number):
        token_value = secrets.token_urlsafe(32)
        api_token = ApiToken(
            client_email=client_email,
            token=token_value,
            permissions=permissions,
            gmail_account_ids=gmail_account_ids,
            status="active",
            created_at=datetime.utcnow()
        )
        db.add(api_token)
        tokens.append(api_token)
    db.commit()
    return tokens

def disable_token(db: Session, token_str: str):
    token = db.query(ApiToken).filter(ApiToken.token == token_str).first()
    if token and token.status == "active":
        token.status = "disabled"
        token.disabled_at = datetime.utcnow()
        db.commit()
    return token

def get_token(db: Session, token_str: str):
    return db.query(ApiToken).filter(ApiToken.token == token_str, ApiToken.status=="active").first()
