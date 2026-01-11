from sqlalchemy import or_, select
from app.dao.base import BaseDAO
from app.models.models import User


class UsersDAO(BaseDAO[User]):
    model = User

    async def find_user_by_email_or_username(
        self, email: str, username: str
    ) -> User | None:
        query = select(self.model).where(
            or_(self.model.email == email, self.model.username == username)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def find_by_login(self, login: str) -> User | None:
        query = select(self.model).where(
            or_(
                self.model.email == login,
                self.model.username == login,
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
