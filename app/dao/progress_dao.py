from app.models.models import UserProgress
from app.dao.base import BaseDAO


class UserProgressDAO(BaseDAO[UserProgress]):
    model = UserProgress

    @classmethod
    async def get_by_user_id(cls, user_id: int) -> list[UserProgress]:
        """Возвращает список объектов `UserProgress`
        для пользователя с указанным  `user_id`.
        """
        return await cls.get_all(user_id=user_id)
