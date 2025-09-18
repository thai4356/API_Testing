from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CourseListRes(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    difficulty: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
