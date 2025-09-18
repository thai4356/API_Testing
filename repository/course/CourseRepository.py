from typing import Optional, List
from sqlmodel import Session, select
from repository.BaseRepository import BaseRepository
from entity.Course import Course

class CourseRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_all(self) -> List[Course]:
        return list(self.session.exec(select(Course)).all())

    def create(self, course: Course) -> Course:
        self.session.add(course)
        self.session.commit()
        self.session.refresh(course)
        return course

    # ✅ thêm
    def get_by_id(self, course_id: int) -> Optional[Course]:
        return self.session.exec(select(Course).where(Course.id == course_id)).first()
