from fastapi import APIRouter, Depends
from app.models.models import User
from app.core.security import get_current_user
from app.services.user_progress_service import UserProgressService


router = APIRouter(
    prefix="/user_progress",
    tags=["Прогресс пользователя"],
)


@router.get("/")
async def get_user_progress(
    current_user: User = Depends(get_current_user),
):
    return await UserProgressService.get_user_progress(user_id=current_user.id)
