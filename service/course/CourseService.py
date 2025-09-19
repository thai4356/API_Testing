# service/course/CourseService.py
from abc import ABC, abstractmethod
from typing import List
from entity.Course import Course

class CourseService(ABC):
    @abstractmethod
    def list_courses(self) -> List[Course]: ...
    @abstractmethod
    def list_courses_page(self, limit: int, offset: int) -> List[Course]: ...
    @abstractmethod
    def create_course(self, title: str, description: str | None, difficulty: str) -> Course: ...
