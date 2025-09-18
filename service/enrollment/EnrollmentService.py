from abc import ABC, abstractmethod
from typing import List, Tuple
from entity.Enrollment import Enrollment
from entity.Course import Course

class EnrollmentService(ABC):
    @abstractmethod
    def enroll(self, student_email: str, course_id: int) -> Enrollment: ...

    @abstractmethod
    def list_student_courses(self, email: str) -> List[Tuple[Course, Enrollment]]: ...
