from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# تأكد من أن هذا المتغير موجود في البيئة
DATABASE_URL = os.getenv("DATABASE_URL")

# التحقق من وجود المتغير فعليًا لتفادي الخطأ
if not DATABASE_URL:
    raise Exception("DATABASE_URL not set in environment variables")

# إعداد الاتصال
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
