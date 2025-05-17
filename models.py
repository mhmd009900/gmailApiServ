from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

class GmailAccount(Base):
    __tablename__ = "gmail_accounts"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    credentials_json = Column(String)  # سيتم تخزين محتوى JSON كنص
    token_json = Column(String)        # سيتم تخزين محتوى JSON كنص

class ApiToken(Base):
    __tablename__ = "api_tokens"
    id = Column(Integer, primary_key=True, index=True)
    client_email = Column(String, index=True)  # إيميل العميل الذي يملك التوكن
    token = Column(String, unique=True, index=True)
    permissions = Column(JSON)  # {"facebook": True, "registration": True}
    gmail_account_ids = Column(JSON)  # قائمة أرقام GmailAccount IDs المستخدمة
    status = Column(String, default="active")  # active, disabled
    created_at = Column(DateTime, default=datetime.utcnow)
    disabled_at = Column(DateTime, nullable=True)
