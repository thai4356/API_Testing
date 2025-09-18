from typing import List, Tuple
from sqlmodel import select
from entity.Enrollment import Enrollment
from entity.Course import Course
from entity.User import User
from repository.enrollment.EnrollmentRepository import EnrollmentRepository
from repository.course.CourseRepository import CourseRepository

class EnrollmentServiceImpl:
    def __init__(self, enroll_repo: EnrollmentRepository, course_repo: CourseRepository):
        self.enroll_repo = enroll_repo
        self.course_repo = course_repo

    def enroll(self, student_email: str, course_id: int) -> Enrollment:
        # 1) user (gmail) phải tồn tại
        student = self.enroll_repo.session.exec(
            select(User).where(User.email == student_email)
        ).first()
        if not student:
            raise ValueError("Student email does not exist")

        # 2) course phải tồn tại
        course = self.course_repo.get_by_id(course_id)
        if not course:
            raise ValueError("Course not found")

        # 3) không được đăng ký trùng
        existed = self.enroll_repo.find_existing(student_email, course_id)
        if existed:
            raise ValueError("Already enrolled in this course")

        # 4) tạo mới
        return self.enroll_repo.create(student_email, course_id)

    def list_student_courses(self, email: str) -> List[Tuple[Course, Enrollment]]:
        return self.enroll_repo.courses_of_student(email)
