from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Client
from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_client(api_key: str = Header(...), db: Session = Depends(get_db)):
    client = db.query(Client).filter_by(api_key=api_key, active=True).first()
    if not client:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return client
