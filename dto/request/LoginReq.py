from pydantic import BaseModel, field_validator

class LoginReq(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str):
        if not v or v.strip() == "":
            raise ValueError("Email must not be empty")
        if not v.endswith("@gmail.com"):
            raise ValueError("Only Gmail addresses are allowed")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if not v or v.strip() == "":
            raise ValueError("Password must not be empty")
        return v
