from app.dao.base import BaseDAO
from app.models.models import UserProgress, ExerciseType


class UserProgressDAO(BaseDAO[UserProgress]):
    model = UserProgress

    async def list_by_user_id(self, user_id: int) -> list[UserProgress]:
        """Получить весь прогресс данного пользователя."""
        return await self.list(
            user_id=user_id,
            order_by=self.model.updated_at.desc(),
            # options=[
            #     selectinload(UserProgress.user).selectinload(User.progress),
            # ],
        )

    async def get_by_user_and_exercise(
        self,
        user_id: int,
        exercise_type: ExerciseType,
    ) -> UserProgress | None:
        """Получить прогресс для определенного упражнения."""
        return await self.find_one(
            user_id=user_id, exercise_type=exercise_type
        )
