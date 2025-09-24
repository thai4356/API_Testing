from pydantic import BaseModel, EmailStr, Field

class UserCreateReq(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str | None = None
