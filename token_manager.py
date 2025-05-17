from threading import Timer
from datetime import datetime
from database import SessionLocal
from models import APIToken

def disable_expired_tokens():
    db = SessionLocal()
    now = datetime.utcnow()
    tokens = db.query(APIToken).filter(APIToken.is_active == True, APIToken.disable_after != None).all()
    for token in tokens:
        if now > token.disable_after:
            token.is_active = False
            db.add(token)
    db.commit()
    db.close()

def schedule_token_cleanup(interval_seconds: int = 60):
    def run():
        disable_expired_tokens()
        schedule_token_cleanup(interval_seconds)
    Timer(interval_seconds, run).start()
