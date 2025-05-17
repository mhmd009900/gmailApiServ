from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    api_key = Column(String, unique=True, index=True)
    quota = Column(Integer, default=10)
    used = Column(Integer, default=0)
    active = Column(Boolean, default=True)

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    token_path = Column(String)
    credentials_path = Column(String)
    is_active = Column(Boolean, default=True)
    assigned_to = Column(Integer, ForeignKey("clients.id"), nullable=True)
    registered_at = Column(DateTime, nullable=True)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer)
    account_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    registration_detected_at = Column(DateTime, nullable=True)
