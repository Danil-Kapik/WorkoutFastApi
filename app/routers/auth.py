from fastapi import APIRouter, HTTPException, status
from app.core.security import get_password_hash
from app.schemas.users import UserCreateSchema, UserLoginSchema
from app.core.security import verify_password, create_access_token
from app.dao.users_dao import UsersDAO


router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateSchema):
    existing_user = await UsersDAO.find_user_by_email_or_username(
        email=user_data.email, username=user_data.username
    )
    if existing_user:
        if existing_user.email == user_data.email:
            detail = "Пользователь с таким email уже существует"
        else:
            detail = "Имя пользователя уже занято"

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=detail
        )

    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.model_dump()
    user_dict["password"] = hashed_password

    await UsersDAO.create(**user_dict)
    return {"message": "Вы успешно зарегистрированы!"}


@router.post("/login")
async def login_user(data: UserLoginSchema):
    user = await UsersDAO.find_by_login(data.login)

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )

    access_token = create_access_token(subject=str(user.id))

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
