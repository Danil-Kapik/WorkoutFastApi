from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.users import UserCreateSchema
from app.services.user_service import UserService
from app.core.security import get_current_user
from app.core.database import get_session
from app.schemas.users import TokenResponse


async def get_user_service(session: AsyncSession = Depends(get_session)):
    return UserService(session)


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreateSchema,
    service: UserService = Depends(get_user_service),
):
    await service.register_user(user_data)
    return {"message": "Вы успешно зарегистрированы!"}


@router.post("/login", response_model=TokenResponse)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    access_token = await service.authenticate_user(
        form_data.username,
        form_data.password,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me")
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user
