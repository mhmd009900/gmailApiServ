from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TokenCreateRequest(BaseModel):
    client_email: str
    number_of_tokens: int
    permissions: dict  # مثال {"facebook": True, "registration": True}

class TokenResponse(BaseModel):
    token: str
    status: str
    created_at: datetime
    disabled_at: Optional[datetime]

class ApiTokenOut(BaseModel):
    client_email: str
    token: str
    permissions: dict
    status: str
