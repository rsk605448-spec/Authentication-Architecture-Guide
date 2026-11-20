# Authentication Architecture Guide

A small, documented FastAPI example showing how an API authenticates users with password hashing and signed JWT access tokens.

> **Scope:** This is a teaching/demo repository, not an audit of an existing application. Production systems need HTTPS, a persistent user store, key rotation, rate limiting, monitoring, and a reviewed deployment configuration.

## What is included

- `app/main.py` — registration, login, and protected profile endpoints.
- `app/security.py` — password hashing and JWT creation/verification.
- `app/store.py` — deliberately simple in-memory user store for the demo.
- `docs/` — architecture, request flow, and credential/token handling.
- `tests/` — basic tests for the core token and password behavior.
- `.env.example` — configuration names; never put real secrets here.

## Request flow

1. A client sends an email and password to `POST /register` or `POST /login` over HTTPS.
2. The server hashes new passwords before storing them. It never stores the original password.
3. On login, the server verifies the submitted password against the stored password hash.
4. If valid, the server signs a short-lived JWT access token.
5. The client sends that token in `Authorization: Bearer <token>`.
6. The API verifies the signature and expiry before returning protected data.

See [the component map](docs/COMPONENTS.md), [the request flow](docs/REQUEST_FLOW.md), and [credential handling](docs/CREDENTIALS_AND_TOKENS.md).

## Run locally

Requires Python 3.11+.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

Set `JWT_SECRET` to a long random value before running outside a local demo. The fallback secret exists only to make the sample easy to start and must not be used in production.

## Example

Register:

```bash
curl -X POST http://127.0.0.1:8000/register \\
  -H "Content-Type: application/json" \\
  -d '{"email":"learner@example.com","password":"a-long-demo-password"}'
```

Login:

```bash
curl -X POST http://127.0.0.1:8000/login \\
  -H "Content-Type: application/json" \\
  -d '{"email":"learner@example.com","password":"a-long-demo-password"}'
```

Use the returned access token:

```bash
curl http://127.0.0.1:8000/me \\
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Important limitations

- The user store is in memory: accounts disappear when the process restarts.
- There is no refresh-token endpoint, logout/revocation store, email verification, password reset, or role/permission system.
- The example uses a shared HMAC signing secret. Production key management and rotation need a deliberate design.
- JWT payloads are encoded, not encrypted. Do not put passwords or secrets in claims.
- Do not commit `.env` files, API keys, private keys, or real user data.

## Tests

```bash
pytest -q
```

## License

MIT — see [LICENSE](LICENSE).
