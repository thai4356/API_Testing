import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "railway")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session

def init_db() -> None:
    from entity.User import User         # noqa: F401
    from entity.Course import Course     # noqa: F401
    from entity.Enrollment import Enrollment  # noqa: F401
    SQLModel.metadata.create_all(engine)
