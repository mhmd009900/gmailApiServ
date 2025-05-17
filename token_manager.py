import threading, time
from sqlalchemy.orm import Session
from database import SessionLocal
from models import APIToken
from datetime import datetime

def mark_expired_tokens():
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        expired = db.query(APIToken).filter(APIToken.expires_at <= now, APIToken.used == False).all()
        for token in expired:
            token.used = True
        db.commit()
    finally:
        db.close()

def schedule_token_cleanup():
    def run():
        while True:
            mark_expired_tokens()
            time.sleep(60)
    threading.Thread(target=run, daemon=True).start()
