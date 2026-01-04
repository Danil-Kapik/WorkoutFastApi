from pydantic import BaseModel
from datetime import datetime
from app.schemas.base import ORMBaseSchema, TimestampSchema
from app.models.models import ExerciseType as ExerciseTypeEnum
from app.models.models import Difficulty as DifficultyEnum


class UserProgressCreateSchema(BaseModel):
    exercise_type: ExerciseTypeEnum
    difficulty: DifficultyEnum
    current_reps_per_set: int = 1


class UserProgressUpdateSchema(BaseModel):
    current_reps_per_set: int | None = None
    difficulty: DifficultyEnum | None = None


class UserProgressReadSchema(ORMBaseSchema, TimestampSchema):
    id: int
    user_id: int
    exercise_type: ExerciseTypeEnum
    difficulty: DifficultyEnum
    current_reps_per_set: int
    last_success_at: datetime | None
