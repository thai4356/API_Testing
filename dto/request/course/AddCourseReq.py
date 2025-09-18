from pydantic import BaseModel, field_validator

class AddCourseReq(BaseModel):
    title: str
    description: str | None = None
    difficulty: str

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str):
        if not v or v.strip() == "":
            raise ValueError("Title must not be empty")
        return v

    @field_validator("difficulty")
    @classmethod
    def difficulty_valid(cls, v: str):
        allowed = {"Beginner", "Intermediate", "Advanced"}
        if v not in allowed:
            raise ValueError(f"Difficulty must be one of {allowed}")
        return v
