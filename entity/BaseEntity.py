# entity/BaseEntity.py
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel

class BaseEntity(SQLModel, table=False):  # base/mixin, KHÔNG tạo bảng
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
