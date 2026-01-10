from app.core.database import async_session
from sqlalchemy import select
from typing import Type, Generic, TypeVar
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T", bound=DeclarativeBase)


class BaseDAO(Generic[T]):
    model: Type[T] | None = None

    @classmethod
    async def get_all(cls, **filters) -> list[T]:
        async with async_session() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filters) -> T | None:
        async with async_session() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def create(cls, **kwargs) -> T:
        obj = cls.model(**kwargs)
        async with async_session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj
