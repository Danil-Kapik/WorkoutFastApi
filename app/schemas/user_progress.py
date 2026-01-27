from pydantic import BaseModel, Field
from datetime import datetime
from app.schemas.base import BaseSchema, TimestampSchema
from app.models.models import ExerciseType as ExerciseTypeEnum
from app.models.models import Difficulty as DifficultyEnum


class UserProgressCreateSchema(BaseModel):
    exercise_type: ExerciseTypeEnum
    current_reps_per_set: int = Field(
        ..., ge=1
    )  # "..." означает обязательное поле


class UserProgressReadSchema(BaseSchema, TimestampSchema):
    id: int
    user_id: int
    exercise_type: ExerciseTypeEnum
    difficulty: DifficultyEnum
    current_reps_per_set: int
    last_success_at: datetime | None
