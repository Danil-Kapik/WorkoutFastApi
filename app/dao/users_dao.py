from sqlalchemy import or_

from app.dao.base import BaseDAO
from app.models.models import User


class UsersDAO(BaseDAO[User]):
    model = User

    async def find_by_login(self, login: str) -> User | None:
        return await self.find_one(
            or_(User.email == login, User.username == login)
        )
