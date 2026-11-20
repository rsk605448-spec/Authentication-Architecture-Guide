"""FastAPI endpoints for registration, login, and the protected profile."""
import re
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from app.security import create_access_token, decode_access_token, hash_password, verify_password
from app.store import create_user, get_user

app = FastAPI(title="Authentication Architecture Guide", version="1.0.0")
bearer_scheme = HTTPBearer(auto_error=False)


class Credentials(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=8, max_length=128)


def validate_email(email: str) -> bool:
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(credentials: Credentials):
    if not validate_email(credentials.email):
        raise HTTPException(status_code=422, detail="Invalid email address")
    if get_user(credentials.email):
        raise HTTPException(status_code=409, detail="Account already exists")
    try:
        user = create_user(credentials.email, hash_password(credentials.password))
    except ValueError:
        raise HTTPException(status_code=409, detail="Account already exists")
    return {"message": "User registered", "email": user["email"]}


@app.post("/login")
def login(credentials: Credentials):
    user = get_user(credentials.email)
    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(user["email"])
    return {"access_token": token, "token_type": "bearer"}


def current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Bearer token required")
    try:
        payload = decode_access_token(credentials.credentials)
        subject = payload.get("sub")
        if not subject:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = get_user(subject)
    if not user:
        raise HTTPException(status_code=401, detail="User no longer exists")
    return user


@app.get("/me")
def me(user: Annotated[dict, Depends(current_user)]):
    return {"email": user["email"]}
