import time

import pytest
from jwt import ExpiredSignatureError

from app.security import create_access_token, decode_access_token, hash_password, verify_password


def test_password_hash_is_not_plaintext_and_verifies():
    password = "correct-horse-battery"
    password_hash = hash_password(password)
    assert password_hash != password
    assert verify_password(password, password_hash)
    assert not verify_password("wrong-password", password_hash)


def test_token_contains_subject():
    token = create_access_token("learner@example.com")
    payload = decode_access_token(token)
    assert payload["sub"] == "learner@example.com"
    assert "exp" in payload


def test_expired_token_is_rejected(monkeypatch):
    import app.security as security

    monkeypatch.setattr(security, "ACCESS_TOKEN_MINUTES", -1)
    token = security.create_access_token("learner@example.com")
    with pytest.raises(ExpiredSignatureError):
        security.decode_access_token(token)
