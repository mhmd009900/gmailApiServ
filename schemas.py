from pydantic import BaseModel
from typing import Optional

class AccountAssignResponse(BaseModel):
    account_id: int
    token_path: str

class RegistrationDetected(BaseModel):
    account_id: int
