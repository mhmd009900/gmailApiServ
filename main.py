from fastapi import FastAPI
import admin, client
from token_manager import schedule_token_cleanup
from database import init_db
import os
import uvicorn

app = FastAPI()

app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(client.router, prefix="/api", tags=["Client"])

@app.on_event("startup")
def startup_event():
    init_db()
    schedule_token_cleanup()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # تستخدم بورت متغير البيئة الذي يوفره Railway
    uvicorn.run("main:app", host="0.0.0.0", port=port)
