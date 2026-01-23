from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.user_progress import (
    UserProgressReadSchema,
)
from app.services.user_progress_service import UserProgressService
from app.core.security import get_current_user
from app.models.models import User, ExerciseType

router = APIRouter(prefix="/progress", tags=["Прогресс пользователя"])


async def get_progress_service(session: AsyncSession = Depends(get_session)):
    return UserProgressService(session)


@router.get("/", response_model=list[UserProgressReadSchema])
async def get_user_progress(
    current_user: User = Depends(get_current_user),
    service: UserProgressService = Depends(get_progress_service),
):
    return await service.get_user_progress(user_id=current_user.id)


@router.get("/by-exercise", response_model=UserProgressReadSchema | None)
async def get_progress_for_exercise(
    exercise_type: ExerciseType = Query(..., description="Тип упражнения"),
    current_user: User = Depends(get_current_user),
    service: UserProgressService = Depends(get_progress_service),
) -> UserProgressReadSchema | None:
    session = await service.get_progress_for_exercise(
        user_id=current_user.id,
        exercise_type=exercise_type,
    )
    if session:
        return UserProgressReadSchema.model_validate(session)
    return None
