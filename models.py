from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
from datetime import datetime, timedelta

class AdminUser(Base):
   __tablename__ = "admin_users"
   id = Column(Integer, primary_key=True, index=True)
   email = Column(String, unique=True, index=True)
   hashed_password = Column(String)

class APIToken(Base):
   __tablename__ = "api_tokens"
   id = Column(Integer, primary_key=True, index=True)
   token = Column(String, unique=True, index=True)
   client_email = Column(String, index=True)
   permission_type = Column(String)
   gmail_account = Column(String)
   created_at = Column(DateTime, default=datetime.utcnow)
   expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))
   used = Column(Boolean, default=False)
