# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from passlib.hash import bcrypt
from sqlmodel import Session, select
from database import init_db, engine
from controller.UserController import router as user_router
from controller.CourseController import router as course_router
from controller.EnrollmentController import router as enrollment_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    from entity.User import User  # import trong lifespan

    with Session(engine) as session:
        admin = session.exec(select(User).where(User.email == "admin@gmail.com")).first()
        if not admin:
            admin = User(
                email="admin@gmail.com",
                password=bcrypt.hash("admin123"),
                user_token="admin_token",
                name="Administrator",
                is_active=True,
                is_superuser=True,
            )
            session.add(admin)
            session.commit()
    yield

app = FastAPI(title="FastAPIProject", lifespan=lifespan)

# include routers
app.include_router(user_router)
app.include_router(course_router)
app.include_router(enrollment_router)

# DEBUG: in route list để chắc chắn router đã đăng ký
for r in app.routes:
    try:
        print("ROUTE:", r.path, getattr(r, "methods", None))
    except Exception:
        pass
