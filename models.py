from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class AdminUser(Base):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class APIToken(Base):
    __tablename__ = "api_tokens"
    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    client_email = Column(String, nullable=False)
    permission_type = Column(String, nullable=False)  # e.g., facebook, registration
    gmail_account = Column(String, nullable=False)  # Gmail associated
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    disable_after = Column(DateTime, nullable=True)
