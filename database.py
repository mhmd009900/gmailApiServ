from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "postgresql://postgres:fLQsnIlPxaSPGeLlShqaVWnZVRVZCcUu@tramway.proxy.rlwy.net:55093/railway"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
from models import AdminUser, APIToken
Base.metadata.create_all(bind=engine)

def get_db():
db = SessionLocal()
try:
yield db
finally:
db.close()
