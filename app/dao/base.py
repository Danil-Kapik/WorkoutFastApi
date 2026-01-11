from typing import Type, Generic, TypeVar, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


T = TypeVar("T", bound=DeclarativeBase)


class BaseDAO(Generic[T]):
    model: Type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, **filters) -> Sequence[T]:
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def find_one_or_none(self, **filters) -> T | None:
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> T:
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        return obj
