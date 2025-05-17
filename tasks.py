from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from database import SessionLocal
from models import Account

scheduler = BackgroundScheduler()
scheduler.start()

def deactivate_account(account_id: int):
    db = SessionLocal()
    acc = db.query(Account).filter_by(id=account_id).first()
    if acc:
        acc.is_active = False
        db.commit()
    db.close()

def schedule_deactivation(account_id: int):
    run_at = datetime.utcnow() + timedelta(minutes=10)
    scheduler.add_job(deactivate_account, 'date', run_date=run_at, args=[account_id])
