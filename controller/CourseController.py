from typing import List
from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlmodel import Session
from database import get_session
from repository.course.CourseRepository import CourseRepository
from service.course.CourseServiceImpl import CourseServiceImpl
from dto.request.course.AddCourseReq import AddCourseReq
from dto.response.course.CourseListRes import CourseListRes
from oauth_key.auth import decode_token

router = APIRouter(prefix="/courses", tags=["courses"])

def get_course_service(session: Session = Depends(get_session)) -> CourseServiceImpl:
    repo = CourseRepository(session)
    return CourseServiceImpl(repo)

def require_user(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return sub

@router.get("/", response_model=List[CourseListRes])
def list_courses(
    _user: str = Depends(require_user),
    service: CourseServiceImpl = Depends(get_course_service),
):
    return service.list_courses()

@router.get("/page", response_model=List[CourseListRes])
def list_courses_page(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    _user: str = Depends(require_user),
    service: CourseServiceImpl = Depends(get_course_service),
):
    return service.list_courses_page(limit=limit, offset=offset)

@router.post("/", response_model=CourseListRes, status_code=201)
def add_course(
    payload: AddCourseReq,
    _user: str = Depends(require_user),
    service: CourseServiceImpl = Depends(get_course_service),
):
    return service.create_course(payload.title, payload.description, payload.difficulty)
