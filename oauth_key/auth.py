# oauth_key/auth.py
import os, datetime, jwt
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ALG = "RS256"
EXPIRE_MIN = int(os.getenv("JWT_EXPIRE_MIN", "60"))

# thư mục chứa file này (oauth_key/)
BASE_DIR = Path(__file__).resolve().parent

# Mặc định: key nằm trong cùng thư mục oauth_key/
DEFAULT_PRIVATE = BASE_DIR / "oauth-private.key"
DEFAULT_PUBLIC  = BASE_DIR / "oauth-public.key"

# Cho phép override qua .env, nếu không sẽ dùng mặc định tuyệt đối
PRIVATE_KEY_PATH = Path(os.getenv("JWT_PRIVATE_KEY_PATH", str(DEFAULT_PRIVATE))).resolve()
PUBLIC_KEY_PATH  = Path(os.getenv("JWT_PUBLIC_KEY_PATH",  str(DEFAULT_PUBLIC))).resolve()

with open(PRIVATE_KEY_PATH, "rb") as f:
    PRIVATE_KEY = f.read()
with open(PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = f.read()

def create_access_token(sub: str) -> str:
    now = datetime.datetime.utcnow()
    payload = {"sub": sub, "iat": now, "exp": now + datetime.timedelta(minutes=EXPIRE_MIN)}
    return jwt.encode(payload, PRIVATE_KEY, algorithm=ALG)

def decode_token(token: str) -> dict:
    return jwt.decode(token, PUBLIC_KEY, algorithms=[ALG])
