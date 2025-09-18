from typing import List, Optional, Tuple
from sqlmodel import Session, select
from repository.BaseRepository import BaseRepository
from entity.Enrollment import Enrollment
from entity.Course import Course

class EnrollmentRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def find_existing(self, student_email: str, course_id: int) -> Optional[Enrollment]:
        stmt = select(Enrollment).where(
            Enrollment.studentEmail == student_email,
            Enrollment.courseId == course_id,
        )
        return self.session.exec(stmt).first()

    def create(self, student_email: str, course_id: int) -> Enrollment:
        enroll = Enrollment(studentEmail=student_email, courseId=course_id)
        self.session.add(enroll)
        self.session.commit()
        self.session.refresh(enroll)
        return enroll

    def courses_of_student(self, email: str) -> List[Tuple[Course, Enrollment]]:
        stmt = (
            select(Course, Enrollment)
            .join(Enrollment, Enrollment.courseId == Course.id)
            .where(Enrollment.studentEmail == email)
            .order_by(Enrollment.enrolledAt.desc())
        )
        return list(self.session.exec(stmt).all())
