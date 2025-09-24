from pydantic import BaseModel, EmailStr

class UserCreateRes(BaseModel):
    id: int
    email: EmailStr
    name: str | None = None
    is_active: bool
    is_superuser: bool
    created_at: str | None = None
    updated_at: str | None = None
