from sqlmodel import Field
from entity.BaseEntity import BaseEntity

class Course(BaseEntity, table=True):
    __tablename__ = "courses"
    title: str = Field(nullable=False, max_length=255)
    description: str | None = Field(default=None)
    # 'Beginner' | 'Intermediate' | 'Advanced'
    difficulty: str = Field(nullable=False)
