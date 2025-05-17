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
    print("Server is running...")  # طباعة عند بدء التشغيل

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}...")  # طباعة قبل التشغيل
    uvicorn.run("main:app", host="0.0.0.0", port=port)
