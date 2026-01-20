from pydantic import BaseModel
from app.schemas.base import ORMBaseSchema, TimestampSchema
from app.models.models import ExerciseType as ExerciseTypeEnum
from app.models.models import Difficulty as DifficultyEnum
from app.schemas.user_progress import UserProgressReadSchema


class WorkoutSessionStartSchema(BaseModel):
    """Схема для создания первой тренировочной сессии с прогрессом.
    Сложность вычисляется автоматически на основе количества повторений."""

    exercise_type: ExerciseTypeEnum
    reps: int


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


class ProgressAndSessionResponse(BaseModel):
    """Ответ с созданным прогрессом и сессией"""

    progress: UserProgressReadSchema
    session: WorkoutSessionReadSchema
