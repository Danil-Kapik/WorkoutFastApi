from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.progress_dao import UserProgressDAO
from app.models.models import ExerciseType, UserProgress


class UserProgressService:
    def __init__(self, session: AsyncSession):
        self.dao = UserProgressDAO(session)

    async def get_user_progress(self, user_id: int) -> list[UserProgress]:
        return await self.dao.list_by_user_id(user_id=user_id)

    async def get_progress_for_exercise(
        self,
        user_id: int,
        exercise_type: ExerciseType,
    ) -> UserProgress | None:
        """Получить прогресс пользователя по конкретному упражнению"""
        return await self.dao.get_by_user_and_exercise(
            user_id=user_id,
            exercise_type=exercise_type,
        )
