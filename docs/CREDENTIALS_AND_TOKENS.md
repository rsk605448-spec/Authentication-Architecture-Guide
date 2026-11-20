# Credentials and Tokens

## Password handling

- The client submits a password only during registration or login.
- Registration hashes the password with bcrypt, which generates a salt.
- The stored record contains the bcrypt hash, not the original password.
- Login uses bcrypt verification; it does not decrypt or recover the original password.
- Passwords should never be logged, returned in API responses, or committed to source control.

## JWT access token

The login endpoint issues a signed JWT containing:

| Claim | Meaning |
|---|---|
| `sub` | User identity (email in this teaching example) |
| `iat` | Issued-at time |
| `exp` | Expiration time (15 minutes after issue) |

The example uses HS256, an HMAC-based signing algorithm, with the `JWT_SECRET` environment variable.

### What signing does and does not do

- Signing lets the API detect whether the token was changed and whether it was signed with the configured secret.
- Signing does **not** encrypt the payload. Anyone who obtains the token can decode its claims.
- The token is a bearer credential: anyone possessing a valid token can use it until it expires or the server rejects it.
- Never place passwords, API keys, or confidential personal data in claims.

## Secret management

1. Copy `.env.example` to `.env` for local development.
2. Generate a long, random secret and set `JWT_SECRET`.
3. Keep `.env` out of Git (the repository's `.gitignore` excludes it).
4. In production, use a managed secret store, planned key rotation, and separate secrets per environment.
5. Do not use the development fallback secret outside local learning.

## Deliberate omissions

This project has no refresh tokens, token revocation list, logout endpoint, MFA, session/device management, or key rotation mechanism. A production design must decide how to revoke access early, rotate signing keys, store credentials safely, and respond to compromise.
