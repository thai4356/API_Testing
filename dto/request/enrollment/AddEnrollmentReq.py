from pydantic import BaseModel, field_validator

class AddEnrollmentReq(BaseModel):
    studentEmail: str
    courseId: int

    @field_validator("studentEmail")
    @classmethod
    def validate_gmail(cls, v: str):
        if not v or not v.strip():
            raise ValueError("studentEmail must not be empty")
        v = v.strip()
        if not v.endswith("@gmail.com"):
            raise ValueError("studentEmail must be a Gmail address")
        return v

    @field_validator("courseId")
    @classmethod
    def validate_course_id(cls, v: int):
        if not isinstance(v, int) or v <= 0:
            raise ValueError("courseId must be a positive integer")
        return v
