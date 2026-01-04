from datetime import datetime, timedelta, timezone
import hashlib
import bcrypt
from jose import jwt

from app.core.config import settings


_ROUNDS = 12


def _prehash(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).digest()


def get_password_hash(password: str) -> str:
    prehashed = _prehash(password)
    salt = bcrypt.gensalt(rounds=_ROUNDS)
    hashed = bcrypt.hashpw(prehashed, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    prehashed = _prehash(plain_password)
    return bcrypt.checkpw(prehashed, hashed_password.encode("utf-8"))


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Создает подписанный JWT access token.
    subject — идентификатор пользователя (user_id / email)
    """
    now = datetime.now(timezone.utc)

    expire = (
        now + expires_delta
        if expires_delta
        else now + timedelta(minutes=settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {
        "sub": subject,
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.auth.SECRET_KEY,
        algorithm=settings.auth.ALGORITHM,
    )
