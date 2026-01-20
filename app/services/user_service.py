from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.users_dao import UsersDAO
from app.schemas.users import UserCreateSchema
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)


class UserService:
    def __init__(self, session: AsyncSession):
        self.dao = UsersDAO(session)
        self.session = session

    async def register_user(self, user_data: UserCreateSchema) -> None:
        existing_user = await self.dao.find_by_username(
            username=user_data.username
        )

        if existing_user:
            detail = "Email уже занят"
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=detail
            )

        user_dict = user_data.model_dump()
        user_dict["password"] = get_password_hash(user_dict.pop("password"))

        await self.dao.create(**user_dict)

    async def authenticate_user(self, login: str, password: str) -> str:
        user = await self.dao.find_by_username(login)
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль",
            )
        return create_access_token(subject=str(user.id))
