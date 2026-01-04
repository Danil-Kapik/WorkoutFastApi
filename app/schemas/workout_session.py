from pydantic import BaseModel
from app.schemas.base import ORMBaseSchema, TimestampSchema
from app.models.models import ExerciseType as ExerciseTypeEnum
from app.models.models import Difficulty as DifficultyEnum


class WorkoutSessionCreateSchema(BaseModel):
    exercise_type: ExerciseTypeEnum
    difficulty: DifficultyEnum
    reps_per_set_at_start: int
    notes: str | None = None


class WorkoutSessionUpdateSchema(BaseModel):
    completed: bool | None = None
    notes: str | None = None


class WorkoutSessionReadSchema(ORMBaseSchema, TimestampSchema):
    id: int
    user_id: int
    exercise_type: ExerciseTypeEnum
    difficulty: DifficultyEnum
    reps_per_set_at_start: int
    completed: bool
    notes: str | None
