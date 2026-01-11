from app.models.models import UserProgress
from app.dao.base import BaseDAO
from typing import Sequence


class UserProgressDAO(BaseDAO[UserProgress]):
    model = UserProgress

    async def get_by_user_id(self, user_id: int) -> Sequence[UserProgress]:
        """
        Возвращает список прогресса для конкретного пользователя.
        """
        return await self.get_all(user_id=user_id)
