from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import APIToken
from gmail_reader import read_gmail_for_registration

router = APIRouter()

@router.post("/use-token")
def use_token(token: str, db: Session = Depends(get_db)):
    t = db.query(APIToken).filter_by(token=token).first()
    if not t:
        raise HTTPException(status_code=404, detail="Token not found")
    if t.used:
        raise HTTPException(status_code=400, detail="Token already used")
    if read_gmail_for_registration(t.gmail_account):
        t.used = True
        db.commit()
        return {"message": "Token verified via Gmail"}
    return {"message": "No registration email found yet"}
