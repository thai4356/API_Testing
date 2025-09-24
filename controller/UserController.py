from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from database import get_session
from dto.request.LoginReq import LoginReq
from dto.response.LoginRes import LoginRes
from repository.user.UserRepository import UserRepository
from service.user.UserServiceImpl import UserServiceImpl
from oauth_key.auth import create_access_token
from dto.request.User.UserCreateReq import UserCreateReq
from dto.response.User.UserCreateRes import UserCreateRes

router = APIRouter(prefix="", tags=["auth"])

def get_user_service(session: Session = Depends(get_session)) -> UserServiceImpl:
    repo = UserRepository(session)
    return UserServiceImpl(repo)

@router.post("/login", response_model=LoginRes)
def login(payload: LoginReq, user_service: UserServiceImpl = Depends(get_user_service)):
    user = user_service.authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(sub=user.email)

    return LoginRes(
        access_token=token,
        id=user.id,
        email=user.email,
        name=user.name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at.isoformat() if user.created_at else None,
        updated_at=user.updated_at.isoformat() if user.updated_at else None,
    )

@router.post("/signup", response_model=UserCreateRes, status_code=status.HTTP_201_CREATED)
def signup(payload: UserCreateReq, user_service: UserServiceImpl = Depends(get_user_service)):
    try:
        user = user_service.create_user(payload.email, payload.password, payload.name)
    except ValueError as e:
        # Email duplicate
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return UserCreateRes(
        id=user.id,
        email=user.email,
        name=user.name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at.isoformat() if getattr(user, "created_at", None) else None,
        updated_at=user.updated_at.isoformat() if getattr(user, "updated_at", None) else None,
    )