# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from passlib.hash import bcrypt
from sqlmodel import Session, select
from database import init_db, engine
from controller.UserController import router as user_router
from controller.CourseController import router as course_router
from controller.EnrollmentController import router as enrollment_router
from sqlmodel import select
from fastapi.security import OAuth2PasswordBearer
from entity.Course import Course
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # đường dẫn login hiện có của bạn

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

with Session(engine) as session:
    # if no courses, seed 4 demo courses
    has_course = session.exec(select(Course)).first()
    if not has_course:
        demo = [
            Course(title="FastAPI for Beginners", description="Intro to FastAPI", difficulty="Beginner"),
            Course(title="Data Structures", description="Core DS in Python", difficulty="Intermediate"),
            Course(title="Distributed Systems", description="Consensus & fault tolerance", difficulty="Advanced"),
            Course(title="Databases 101", description="Relational modeling & SQL", difficulty="Beginner"),
        ]
        session.add_all(demo)
        session.commit()
        print("✅ Seeded 4 demo courses")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI Project",
        version="1.0.0",
        description="API docs with JWT auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema



app = FastAPI(title="FastAPIProject", lifespan=lifespan)

app.openapi = custom_openapi
# include routers
app.include_router(user_router)
app.include_router(course_router)
app.include_router(enrollment_router)

@app.get("/ping")
def ping():
    return {"msg": "pong"}

# DEBUG: in route list để chắc chắn router đã đăng ký
for r in app.routes:
    try:
        print("ROUTE:", r.path, getattr(r, "methods", None))
    except Exception:
        pass
