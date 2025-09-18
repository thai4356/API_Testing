from datetime import datetime, timezone
from sqlmodel import Field
from entity.BaseEntity import BaseEntity

class Enrollment(BaseEntity, table=True):
    __tablename__ = "enrollments"

    # student email đăng ký
    studentEmail: str = Field(nullable=False, index=True)

    # khóa học được đăng ký (FK tới courses.id)
    courseId: int = Field(nullable=False, foreign_key="courses.id")

    # thời điểm đăng ký
    enrolledAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
