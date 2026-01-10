from app.dao.users_dao import UsersDAO
from app.schemas.users import UserCreateSchema
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)
from app.models.models import User
from fastapi import HTTPException, status


class UserService:

    @staticmethod
    async def register_user(user_data: UserCreateSchema) -> None:
        existing_user = await UsersDAO.find_user_by_email_or_username(
            email=user_data.email,
            username=user_data.username,
        )

        if existing_user:
            if existing_user.email == user_data.email:
                detail = "Пользователь с таким email уже существует"
            else:
                detail = "Имя пользователя уже занято"

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail,
            )

        user_dict = user_data.model_dump()
        user_dict["password"] = get_password_hash(user_data.password)

        await UsersDAO.create(**user_dict)

    @staticmethod
    async def authenticate_user(login: str, password: str) -> str:
        user = await UsersDAO.find_by_login(login)

        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль",
            )

        return create_access_token(subject=str(user.id))

    @staticmethod
    async def get_current_user(user: User) -> User:
        return user
