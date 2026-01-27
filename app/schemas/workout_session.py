from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field
from app.schemas.base import BaseSchema, TimestampSchema
from app.models.models import ExerciseType as ExerciseTypeEnum
from app.models.models import Difficulty as DifficultyEnum


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
    exercise_type: ExerciseTypeEnum


class WorkoutSessionUpdateSchema(BaseModel):
    completed: bool | None = None
    notes: str | None = Field(None, max_length=500)
