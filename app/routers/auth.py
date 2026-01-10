from fastapi import APIRouter, status, Depends
from app.core.security import get_current_user
from app.schemas.users import UserCreateSchema, UserLoginSchema
from app.services.user_service import UserService


router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateSchema):
    await UserService.register_user(user_data)
    return {"message": "Вы успешно зарегистрированы!"}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(data: UserLoginSchema):
    access_token = await UserService.authenticate_user(
        login=data.login,
        password=data.password,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me")
async def read_users_me(current_user=Depends(get_current_user)):
    return await UserService.get_current_user(user=current_user)
