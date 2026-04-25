from datetime import date

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from jose import jwt, JWTError

from .db import get_session
from .models.user import User
from .models.usage import DailyUsage
from .config import get_settings

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: Session = Depends(get_session),
) -> User:
    settings = get_settings()
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def enforce_usage_limit(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> User:
    """Check daily message count and increment it. Returns the user if allowed."""
    settings = get_settings()
    limit = settings.daily_message_limit
    if limit <= 0:
        return user

    today = date.today()
    record = session.exec(
        select(DailyUsage)
        .where(DailyUsage.user_id == user.id, DailyUsage.date == today)
    ).first()

    if record and record.message_count >= limit:
        raise HTTPException(
            status_code=429,
            detail=f"Daily message limit ({limit}) reached. Resets at midnight UTC.",
        )

    if record:
        record.message_count += 1
    else:
        record = DailyUsage(user_id=user.id, date=today, message_count=1)
        session.add(record)
    session.commit()

    return user
