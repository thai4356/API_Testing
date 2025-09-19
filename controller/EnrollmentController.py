from typing import List
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlmodel import Session
from database import get_session
from repository.enrollment.EnrollmentRepository import EnrollmentRepository
from repository.course.CourseRepository import CourseRepository
from service.enrollment.EnrollmentServiceImpl import EnrollmentServiceImpl
from dto.request.enrollment.AddEnrollmentReq import AddEnrollmentReq
from dto.response.enrollment.EnrollmentListRes import EnrollmentListRes
from oauth_key.auth import decode_token
from sqlmodel import select

router = APIRouter(prefix="/api", tags=["enrollments"])

def get_service(session: Session = Depends(get_session)) -> EnrollmentServiceImpl:
    enroll_repo = EnrollmentRepository(session)
    course_repo = CourseRepository(session)
    return EnrollmentServiceImpl(enroll_repo, course_repo)

def require_user(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return sub

@router.post("/enrollments", status_code=status.HTTP_201_CREATED)
def enroll(
    req: AddEnrollmentReq,
    _user: str = Depends(require_user),
    service: EnrollmentServiceImpl = Depends(get_service),
):
    try:
        service.enroll(req.studentEmail, req.courseId)
        return {"message": "Enrolled successfully"}
    except ValueError as e:
        msg = str(e)
        if "Already enrolled" in msg:
            raise HTTPException(status_code=409, detail=msg)   # Conflict
        if "not exist" in msg or "not found" in msg:
            raise HTTPException(status_code=404, detail=msg)   # Not found
        raise HTTPException(status_code=400, detail=msg)

@router.get("/students/{email}/enrollments", response_model=List[EnrollmentListRes])
def get_student_enrollments(
    email: str,
    _user: str = Depends(require_user),
    service: EnrollmentServiceImpl = Depends(get_service),
):
    #check user
    from entity.User import User
    user = service.enroll_repo.session.exec(
        select(User).where(User.email == email)
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="Student email not found")

    pairs = service.list_student_courses(email)
    return [
        EnrollmentListRes(
            courseId=c.id,
            title=c.title,
            description=c.description,
            difficulty=c.difficulty,
            enrolled_at=e.enrolledAt,
        )
        for (c, e) in pairs
    ]

