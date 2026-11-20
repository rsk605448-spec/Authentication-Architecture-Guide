# Authentication Architecture Guide

A beginner-friendly, runnable FastAPI example showing password-based authentication with bcrypt password hashing and signed JWT access tokens.

> **Educational scope:** This is a learning project, not a production-ready identity platform or a security audit. It uses an in-memory user store and has no refresh-token, logout/revocation, email-verification, password-reset, MFA, or role-based authorization flow.

## Architecture at a glance

- **FastAPI routes** receive registration, login, and protected-profile requests.
- **Security helpers** hash passwords with bcrypt and sign/verify JWTs.
- **In-memory store** holds demo user records while the process is running.
- **Bearer-token dependency** protects the `GET /me` endpoint.

## Repository map

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py                 # HTTP routes and request validation
│   ├── security.py             # bcrypt and JWT helpers
│   └── store.py                # in-memory demo user store
├── docs/
│   ├── COMPONENTS.md           # component responsibilities
│   ├── REQUEST_FLOW.md          # registration/login/protected flow
│   └── CREDENTIALS_AND_TOKENS.md
├── tests/
│   └── test_security.py
├── .env.example
├── .gitignore
├── LICENSE
└── requirements.txt
```

## Components

See [docs/COMPONENTS.md](docs/COMPONENTS.md) for the component map and [docs/CODE_WALKTHROUGH.md](docs/CODE_WALKTHROUGH.md) for a code-level walkthrough with endpoint-to-helper references.

## Request flow

1. A client submits an email and password to `POST /register` or `POST /login`.
2. Registration hashes the password before storing the record.
3. Login verifies the submitted password against the stored bcrypt hash.
4. Successful login returns a short-lived signed JWT access token.
5. The client sends `Authorization: Bearer <token>` to `GET /me`.
6. The API verifies the token signature and expiry before returning the user's profile.

See [docs/REQUEST_FLOW.md](docs/REQUEST_FLOW.md).

## Credentials and tokens

Passwords are never stored as plaintext. bcrypt stores a salted password hash. JWTs are signed (not encrypted), so their claims can be decoded by anyone holding the token. Never put passwords, API keys, or other secrets in JWT claims.

See [docs/CREDENTIALS_AND_TOKENS.md](docs/CREDENTIALS_AND_TOKENS.md).

## Run locally

Requires Python 3.11+.

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set a long random `JWT_SECRET` before running. Then:

```bash
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API docs.

## Try the API

Register:

```bash
curl -X POST http://127.0.0.1:8000/register \
  -H "Content-Type: application/json" \
  -d '{"email":"learner@example.com","password":"a-long-demo-password"}'
```

Login:

```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"learner@example.com","password":"a-long-demo-password"}'
```

Copy the returned `access_token`, then:

```bash
curl http://127.0.0.1:8000/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Run tests

```bash
pytest -q
```

## Security boundaries and production gaps

- The user store is in memory; all accounts disappear when the process restarts. It is not safe for multiple workers.
- The demo has no refresh-token endpoint, logout/revocation list, email verification, password reset, MFA, or authorization roles.
- Use HTTPS in deployment. Do not send credentials over plain HTTP outside localhost.
- Replace the demo secret with a high-entropy secret from a secret manager. Rotate keys deliberately.
- Add persistent database storage, rate limiting, audit logging, monitoring, account lockout/abuse controls, and security tests before production.
- JWT payloads are encoded, not encrypted. Keep claims minimal.
- Never commit `.env`, credentials, tokens, private keys, or real user data.

## License

MIT. See [LICENSE](LICENSE).
