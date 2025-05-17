from fastapi import FastAPI
from .database import Base, engine
from .accounts import router as accounts_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(accounts_router, prefix="/api")
