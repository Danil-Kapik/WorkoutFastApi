from typing import Generic, TypeVar, List
from pydantic import BaseModel
from app.schemas.base import BaseSchema, TimestampSchema
from app.models.models import ExerciseType as ExerciseTypeEnum
from app.models.models import Difficulty as DifficultyEnum
from app.schemas.user_progress import UserProgressReadSchema


T = TypeVar("T")


class PaginatedResponse(BaseSchema, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool


class WorkoutSessionReadSchema(BaseSchema, TimestampSchema):
    id: int
    user_id: int
    exercise_type: ExerciseTypeEnum
    difficulty: DifficultyEnum
    reps_per_set_at_start: int
    completed: bool
    notes: str | None


class WorkoutSessionStartSchema(BaseModel):
    """Схема для создания первой тренировочной сессии с прогрессом.
    Сложность вычисляется автоматически на основе количества повторений."""

    exercise_type: ExerciseTypeEnum
    reps: int


class WorkoutSessionUpdateSchema(BaseModel):
    completed: bool | None = None
    notes: str | None = None


class ProgressAndSessionResponse(BaseModel):
    """Ответ с созданным прогрессом и сессией"""

    progress: UserProgressReadSchema | None
    session: WorkoutSessionReadSchema
