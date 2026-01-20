from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.models import User
from app.schemas.workout_session import (
    WorkoutSessionStartSchema,
    WorkoutSessionReadSchema,
)
from app.schemas.user_progress import UserProgressReadSchema
from app.services.workout_session_service import WorkoutSessionService
from app.schemas.workout_session import ProgressAndSessionResponse


router = APIRouter(prefix="/sessions", tags=["Воркаут сессии"])


async def get_workout_session_service(
    session: AsyncSession = Depends(get_session),
) -> WorkoutSessionService:
    return WorkoutSessionService(session)


@router.post(
    "/create",
    response_model=ProgressAndSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_progress_and_session(
    data: WorkoutSessionStartSchema,
    current_user: User = Depends(get_current_user),
    service: WorkoutSessionService = Depends(get_workout_session_service),
) -> ProgressAndSessionResponse:
    """
    Создаёт прогресс пользователя и его первую тренировочную сессию.

    Эндпоинт автоматически определяет уровень сложности на основе
    количества повторений и создаёт соответствующие записи в базе данных.

    Параметры:
    - exercise_type: Тип упражнения (подтягивания, отжимания, тяга, присед)
    - reps: Количество повторений (автоматически определяет сложность)

    Возвращает:
    - progress: Созданный или существующий прогресс пользователя
    - session: Созданная тренировочная сессия
    """
    try:
        progress, session = await service.create_progress_and_session(
            user_id=current_user.id,
            exercise_type=data.exercise_type,
            reps=data.reps,
        )

        return ProgressAndSessionResponse(
            progress=UserProgressReadSchema.model_validate(progress),
            session=WorkoutSessionReadSchema.model_validate(session),
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Прогресс для данного упражнения уже существует.",
        ) from exc
