from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EnrollmentListRes(BaseModel):
    courseId: int
    title: str
    description: Optional[str] = None
    difficulty: str
    enrolled_at: datetime
