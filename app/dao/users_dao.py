from sqlalchemy import or_, select
from sqlalchemy.orm import lazyload

from app.dao.base import BaseDAO
from app.models.models import User


class UsersDAO(BaseDAO[User]):
    model = User

    async def find_by_login(self, login: str) -> User | None:
        return await self.find_one(
            or_(User.email == login, User.username == login)
        )

    async def find_by_email_or_username(
        self, email: str, username: str
    ) -> User | None:
        return await self.find_one(
            or_(User.email == email, User.username == username)
        )

    async def get_for_auth(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id).options(lazyload("*"))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
