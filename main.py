from fastapi import FastAPI
import admin, client
from token_manager import schedule_token_cleanup
from database import init_db

app = FastAPI()

app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(client.router, prefix="/api", tags=["Client"])

@app.on_event("startup")
def startup_event():
print("Server is running...")
init_db()
schedule_token_cleanup()

if name == "main":
import uvicorn, os
port = int(os.environ.get("PORT", 8000))
uvicorn.run("main:app", host="0.0.0.0", port=port)

