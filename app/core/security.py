from datetime import datetime, timedelta, timezone
import hashlib
import bcrypt
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.dao.users_dao import UsersDAO

from app.core.config import settings


_ROUNDS = 12

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.auth.SECRET_KEY,
            algorithms=[settings.auth.ALGORITHM],
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if user is None:
        raise credentials_exception

    return user


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
