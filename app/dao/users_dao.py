from sqlalchemy import or_, select
from app.core.database import async_session
from app.dao.base import BaseDAO
from app.models.models import User


class UsersDAO(BaseDAO[User]):
    model = User

    @classmethod
    async def find_user_by_email_or_username(
        cls, email: str, username: str
    ) -> User | None:
        async with async_session() as session:
            query = select(cls.model).where(
                or_(cls.model.email == email, cls.model.username == username)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by_login(cls, login: str) -> User | None:
        async with async_session() as session:
            query = select(cls.model).where(
                or_(
                    cls.model.email == login,
                    cls.model.username == login,
                )
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
