from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ رابط الاتصال الكامل (تم تضمينه مباشرة)
DATABASE_URL = "postgresql+psycopg2://postgres:fLQsnIlPxaSPGeLlShqaVWnZVRVZCcUu@tramway.proxy.rlwy.net:55093/railway"

# ✅ إنشاء محرك الاتصال
engine = create_engine(DATABASE_URL)

# ✅ إعداد الجلسة
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ الأساس لبناء الجداول
Base = declarative_base()
