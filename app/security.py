"""Password hashing and JWT utilities for the demo."""
import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()

ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 15


def _secret() -> str:
    # A development-only fallback keeps the sample easy to run.
    # Always set JWT_SECRET to a high-entropy value outside local learning.
    return os.getenv("JWT_SECRET", "DEVELOPMENT_ONLY_CHANGE_THIS_SECRET")


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def create_access_token(subject: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_MINUTES),
    }
    return jwt.encode(payload, _secret(), algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, _secret(), algorithms=[ALGORITHM])
