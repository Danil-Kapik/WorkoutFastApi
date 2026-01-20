from typing import Type, TypeVar, Generic, Any, Sequence
from sqlalchemy import select, exists, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Load

T = TypeVar("T", bound=DeclarativeBase)


class BaseDAO(Generic[T]):
    model: Type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(
        self,
        *expressions,
        order_by=None,
        limit: int | None = None,
        offset: int | None = None,
        options: Sequence[Load] | None = None,
        **filters
    ) -> list[T]:
        stmt = select(self.model).filter(*expressions).filter_by(**filters)

        if options:
            stmt = stmt.options(*options)

        if order_by is not None:
            stmt = stmt.order_by(
                *(order_by if isinstance(order_by, list) else [order_by])
            )
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def find_one(
        self, *expressions, options: Sequence[Load] | None = None, **filters
    ) -> T | None:
        stmt = select(self.model).filter(*expressions).filter_by(**filters)

        if options:
            stmt = stmt.options(*options)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id_with_options(
        self, id_: int, *options: Load
    ) -> T | None:
        stmt = select(self.model).where(self.model.id == id_)

        if options:
            stmt = stmt.options(*options)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, id_: int) -> T | None:
        return await self.session.get(self.model, id_)

    async def exists(self, *expressions, **filters) -> bool:
        stmt = select(
            exists(
                select(self.model).filter(*expressions).filter_by(**filters)
            )
        )
        result = await self.session.execute(stmt)
        return bool(result.scalar())

    async def create(self, **data: Any) -> T:
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def update(
        self, *expressions, data: dict[str, Any], **filters
    ) -> T | None:
        stmt = (
            update(self.model)
            .filter(*expressions)
            .filter_by(**filters)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, *expressions, **filters) -> int:
        stmt = delete(self.model).filter(*expressions).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.rowcount
