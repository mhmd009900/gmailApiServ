from fastapi import FastAPI
from routes import admin, client
from token_manager import schedule_token_cleanup
from database import init_db

app = FastAPI()

app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(client.router, prefix="/api", tags=["Client"])

@app.on_event("startup")
def startup_event():
    init_db()
    schedule_token_cleanup()
    print("Server is running...")
