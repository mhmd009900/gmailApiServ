from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth import get_current_client, get_db
from models import Account, Session as UserSession
from schemas import AccountAssignResponse, RegistrationDetected
from tasks import schedule_deactivation
from datetime import datetime

router = APIRouter()

@router.post("/assign", response_model=AccountAssignResponse)
def assign_account(client=Depends(get_current_client), db: Session = Depends(get_db)):
    if client.used >= client.quota:
        raise HTTPException(status_code=403, detail="Quota exceeded")

    account = db.query(Account).filter_by(is_active=True, assigned_to=None).first()
    if not account:
        raise HTTPException(status_code=404, detail="No accounts available")

    account.assigned_to = client.id
    db.add(account)

    session = UserSession(client_id=client.id, account_id=account.id)
    db.add(session)

    client.used += 1
    db.commit()
    return {"account_id": account.id, "token_path": account.token_path}

@router.post("/registration")
def registration_detected(data: RegistrationDetected, db: Session = Depends(get_db)):
    acc = db.query(Account).filter_by(id=data.account_id).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    
    acc.registered_at = datetime.utcnow()
    db.commit()

    # جدولة التعطيل بعد 10 دقائق
    schedule_deactivation(acc.id)
    return {"detail": "Scheduled deactivation"}
