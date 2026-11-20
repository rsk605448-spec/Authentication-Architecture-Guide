"""In-memory user storage for the educational demo.

Replace this module with a persistent database and proper uniqueness constraints
before any production use. This store is process-local and not thread/process safe.
"""
from typing import Any

_USERS: dict[str, dict[str, Any]] = {}


def get_user(email: str) -> dict[str, Any] | None:
    return _USERS.get(email.lower())


def create_user(email: str, password_hash: str) -> dict[str, Any]:
    normalized = email.lower()
    if normalized in _USERS:
        raise ValueError("User already exists")
    user = {"email": normalized, "password_hash": password_hash}
    _USERS[normalized] = user
    return user


def clear_users() -> None:
    """Clear demo data; intended for tests only."""
    _USERS.clear()
