# Components

This document maps each part of the example to its responsibility.

## Runtime components

| Component | File | Responsibility |
|---|---|---|
| HTTP/API layer | `app/main.py` | Defines FastAPI routes, validates request bodies, returns HTTP responses, and protects `GET /me`. |
| Password/JWT utilities | `app/security.py` | Hashes and verifies passwords with bcrypt; creates and verifies signed JWT access tokens. |
| User store | `app/store.py` | Keeps demo user records in a process-local dictionary. |
| Configuration template | `.env.example` | Documents the environment variable needed for JWT signing without including a real secret. |
| Tests | `tests/test_security.py` | Checks password hashing and token validity/expiry behavior. |

## Request path

```text
Client
  |
  | HTTP request
  v
FastAPI route (main.py)
  |                         |
  | password operation     | token operation
  v                         v
security.py  <----------> store.py
  |
  v
HTTP response
```

## Important distinction

Authentication answers **who is making the request?** This sample authenticates users by verifying a password at login and a signed bearer token on protected requests.

Authorization answers **what may that user do?** This sample does not implement roles, permissions, or resource-level authorization. A valid token alone does not demonstrate a full authorization system.
