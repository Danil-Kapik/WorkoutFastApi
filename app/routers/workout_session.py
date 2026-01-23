from fastapi import APIRouter, Depends, HTTPException, status, Query

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.models import ExerciseType, User
from app.schemas.workout_session import (
    WorkoutSessionStartSchema,
    WorkoutSessionReadSchema,
    PaginatedResponse,
    WorkoutSessionUpdateSchema,
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


@router.get(
    "/",
    response_model=PaginatedResponse[WorkoutSessionReadSchema],
)
async def get_sessions(
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(10, ge=1, le=100, description="Размер страницы"),
    service: WorkoutSessionService = Depends(get_workout_session_service),
) -> PaginatedResponse[WorkoutSessionReadSchema]:
    data_dict = await service.get_user_sessions_paginated(
        user_id=current_user.id,
        page=page,
        size=size,
    )
    # Хз нужно или нет вручную валидировать если FastAPI уже это делает
    return PaginatedResponse[WorkoutSessionReadSchema](**data_dict)


@router.get(
    "/by-exercise",
    response_model=PaginatedResponse[WorkoutSessionReadSchema],
)
async def get_sessions_by_exercise(
    exercise_type: ExerciseType = Query(..., description="Тип упражнения"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(10, ge=1, le=100, description="Размер страницы"),
    current_user: User = Depends(get_current_user),
    service: WorkoutSessionService = Depends(get_workout_session_service),
) -> PaginatedResponse[WorkoutSessionReadSchema]:
    dict_data = await service.get_sessions_by_exercise_paginated(
        user_id=current_user.id,
        exercise_type=exercise_type,
        page=page,
        size=size,
    )
    # Хз нужно или нет вручную валидировать если FastAPI уже это делает
    return PaginatedResponse[WorkoutSessionReadSchema](**dict_data)


@router.get(
    "/last",
    response_model=WorkoutSessionReadSchema | None,
)
async def get_last_session(
    exercise_type: ExerciseType | None = Query(
        None, description="Тип упражнения"
    ),
    current_user: User = Depends(get_current_user),
    service: WorkoutSessionService = Depends(get_workout_session_service),
) -> WorkoutSessionReadSchema | None:
    session_model = await service.get_last_session(
        user_id=current_user.id,
        exercise_type=exercise_type,
    )
    if not session_model:
        return None
    # Хз нужно или нет вручную валидировать если FastAPI уже это делает
    return WorkoutSessionReadSchema.model_validate(session_model)


@router.post(
    "/{session_id}/complete",
    response_model=ProgressAndSessionResponse,
)
async def complete_workout_session(
    session_id: int,
    data: WorkoutSessionUpdateSchema,
    current_user: User = Depends(get_current_user),
    service: WorkoutSessionService = Depends(get_workout_session_service),
) -> ProgressAndSessionResponse:
    """
    Завершает тренировочную сессию и,
    при необходимости, обновляет прогресс пользователя.
    """
    try:
        workout_session, progress = (
            await service.complete_workout_session_and_update_progress(
                session_id=session_id,
                completed=data.completed,
                notes=data.notes,
            )
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return ProgressAndSessionResponse(
        session=WorkoutSessionReadSchema.model_validate(workout_session),
        progress=(
            UserProgressReadSchema.model_validate(progress)
            if progress
            else None
        ),
    )


@router.patch(
    "/{session_id}",
    response_model=ProgressAndSessionResponse,
)
async def update_workout_session(
    session_id: int,
    data: WorkoutSessionUpdateSchema,
    current_user: User = Depends(get_current_user),
    service: WorkoutSessionService = Depends(get_workout_session_service),
) -> ProgressAndSessionResponse:
    """
    Частично обновляет тренировочную сессию.
    При завершении автоматически обновляет прогресс.
    """
    try:
        workout_session, progress = await service.update_session(
            session_id=session_id,
            completed=data.completed,
            notes=data.notes,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return ProgressAndSessionResponse(
        session=WorkoutSessionReadSchema.model_validate(workout_session),
        progress=(
            UserProgressReadSchema.model_validate(progress)
            if progress
            else None
        ),
    )
