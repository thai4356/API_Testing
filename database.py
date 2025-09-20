# database.py
import os
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import NullPool

# Chỉ đọc .env khi chạy LOCAL (Vercel đã có ENV sẵn)
if not os.getenv("VERCEL"):
    from dotenv import load_dotenv
    load_dotenv()

def env(key: str) -> str:
    v = os.getenv(key)
    if not v:
        # Fail-fast để không bao giờ fallback về localhost
        raise RuntimeError(f"Missing ENV: {key}. Set it in Vercel → Settings → Environment Variables.")
    return v

DB_HOST = env("DB_HOST")
DB_PORT = env("DB_PORT")
DB_USER = env("DB_USER")
DB_PASSWORD = env("DB_PASSWORD")
DB_NAME = env("DB_NAME")  # Railway thường là 'railway'

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)

# Dùng NullPool cho serverless (mỗi request 1 kết nối ngắn hạn)
engine = create_engine(
    DATABASE_URL,
    echo=False,
    poolclass=NullPool,
    connect_args={"connect_timeout": 10},
)

def get_session():
    with Session(engine) as session:
        yield session

def init_db() -> None:
    from entity.User import User         # noqa
    from entity.Course import Course     # noqa
    from entity.Enrollment import Enrollment  # noqa
    SQLModel.metadata.create_all(engine)
