from app.models.models import UserProgress
from app.dao.base import BaseDAO


class UserProgressDAO(BaseDAO[UserProgress]):
    model = UserProgress
