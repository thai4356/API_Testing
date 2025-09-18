from typing import List
from entity.Course import Course
from repository.course.CourseRepository import CourseRepository
from service.course.CourseService import CourseService

class CourseServiceImpl(CourseService):
    def __init__(self, repo: CourseRepository):
        self.repo = repo

    def list_courses(self) -> List[Course]:
        return self.repo.get_all()

    def create_course(self, title: str, description: str | None, difficulty: str) -> Course:
        return self.repo.create(Course(title=title, description=description, difficulty=difficulty))
