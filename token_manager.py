from datetime import datetime
from database import SessionLocal
from models import APIToken
import threading
import time

def cleanup_expired_tokens():
  while True:
    db = SessionLocal()
    expired = db.query(APIToken).filter(APIToken.expires_at <= datetime.utcnow(), APIToken.used == False).all()
    for token in expired:
      db.delete(token)
      db.commit()
      db.close()
      time.sleep(3600) # every hour

def schedule_token_cleanup():
  thread = threading.Thread(target=cleanup_expired_tokens, daemon=True)
  thread.start()
