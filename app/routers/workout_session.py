from fastapi import APIRouter, Depends, status, Query

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
from app.services.workout_session_service import WorkoutSessionService


router = APIRouter(prefix="/sessions", tags=["Воркаут сессии"])


async def get_workout_session_service(
    session: AsyncSession = Depends(get_session),
) -> WorkoutSessionService:
    return WorkoutSessionService(session)


@router.post(
    "/start",
    response_model=WorkoutSessionReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def start_workout_session(
    data: WorkoutSessionStartSchema,
    current_user: User = Depends(get_current_user),
    service: WorkoutSessionService = Depends(get_workout_session_service),
) -> WorkoutSessionReadSchema:
    session = await service.start_session(
        user_id=current_user.id,
        exercise_type=data.exercise_type,
    )
    return WorkoutSessionReadSchema.model_validate(session)


@router.patch(
    "/{session_id}/finish",
    response_model=WorkoutSessionReadSchema,
)
async def finish_workout_session(
    session_id: int,
    data: WorkoutSessionUpdateSchema,
    current_user: User = Depends(get_current_user),
    service: WorkoutSessionService = Depends(get_workout_session_service),
) -> WorkoutSessionReadSchema:
    session = await service.finish_session(
        session_id=session_id,
        user_id=current_user.id,
        completed=data.completed,
        notes=data.notes,
    )
    return WorkoutSessionReadSchema.model_validate(session)


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
