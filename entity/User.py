from sqlmodel import Field
from entity.BaseEntity import BaseEntity

class User(BaseEntity, table=True):
    __tablename__ = "users"
    email: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    user_token: str = Field(unique=True)

    name: str | None = Field(default=None, nullable=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
