from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


DATABASE_URL = "postgresql://postgres:fLQsnIlPxaSPGeLlShqaVWnZVRVZCcUu@tramway.proxy.rlwy.net:55093/railway"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
