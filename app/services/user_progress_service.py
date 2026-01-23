from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.progress_dao import UserProgressDAO
from app.models.models import ExerciseType
from app.schemas.user_progress import UserProgressReadSchema


class UserProgressService:
    def __init__(self, session: AsyncSession):
        self.dao = UserProgressDAO(session)

    async def get_user_progress(
        self, user_id: int
    ) -> list[UserProgressReadSchema]:
        progress = await self.dao.list_by_user_id(user_id=user_id)
        return [
            UserProgressReadSchema.model_validate(item) for item in progress
        ]

    async def get_progress_for_exercise(
        self,
        user_id: int,
        exercise_type: ExerciseType,
    ) -> UserProgressReadSchema | None:
        progress = await self.dao.get_by_user_and_exercise(
            user_id=user_id,
            exercise_type=exercise_type,
        )
        if progress:
            return UserProgressReadSchema.model_validate(progress)
        return None
