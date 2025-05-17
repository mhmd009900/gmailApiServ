from database import Base, engine, SessionLocal
from models import Admin, GmailAccount
from auth import hash_password

def init_db():
    # 1. إنشاء الجداول إن لم تكن موجودة
    Base.metadata.create_all(bind=engine)

    # 2. إنشاء أدمن افتراضي (مرة واحدة فقط)
    db = SessionLocal()
    existing_admin = db.query(Admin).filter_by(email="admin@example.com").first()
    if not existing_admin:
        admin = Admin(
            email="admin@example.com",
            password=hash_password("supersecurepassword")
        )
        db.add(admin)
        db.commit()
        print("✅ أدمن مبدئي تم إنشاؤه: admin@example.com / supersecurepassword")
    else:
        print("✅ الأدمن موجود مسبقًا.")

    db.close()

if __name__ == "__main__":
    init_db()
