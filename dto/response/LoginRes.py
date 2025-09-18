from pydantic import BaseModel, Field
from typing import Optional

class LoginRes(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
    id: int
    email: str
    name: Optional[str] = None
    is_active: bool
    is_superuser: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
