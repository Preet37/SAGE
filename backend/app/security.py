"""Auth: bcrypt password hashing + HS256 JWT.

We use the `bcrypt` library directly (not passlib) for compatibility with
bcrypt 4.x. Passwords are pre-hashed with SHA-256 so we are not subject to
bcrypt's 72-byte input limit and so user-supplied long passwords do not
silently truncate (a real CVE pattern when passlib is layered on top).
"""

from __future__ import annotations

import base64
import hashlib
from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session as OrmSession

from app.config import settings
from app.db import get_db
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
JWT_ISSUER = "sage"


def _prepare(p: str) -> bytes:
    """SHA-256 then base64 → fixed 44-byte input. Avoids bcrypt's 72-byte cap."""
    digest = hashlib.sha256(p.encode("utf-8")).digest()
    return base64.b64encode(digest)


def hash_password(p: str) -> str:
    if not isinstance(p, str) or not 8 <= len(p) <= 1024:
        raise ValueError("password must be 8–1024 characters")
    return bcrypt.hashpw(_prepare(p), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(p: str, hashed: str) -> bool:
    if not isinstance(p, str) or not isinstance(hashed, str):
        return False
    try:
        return bcrypt.checkpw(_prepare(p), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def create_access_token(sub: str) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {
            "sub": sub,
            "iat": int(now.timestamp()),
            "iss": JWT_ISSUER,
            "exp": now + timedelta(minutes=settings.jwt_expire_minutes),
        },
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )


def get_current_user(
    token: str = Depends(oauth2_scheme), db: OrmSession = Depends(get_db)
) -> User:
    creds_err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg],
            issuer=JWT_ISSUER,
            options={"require": ["exp", "iat", "sub", "iss"]},
        )
    except JWTError:
        raise creds_err

    email = payload.get("sub")
    if not isinstance(email, str) or "@" not in email:
        raise creds_err

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise creds_err
    return user
