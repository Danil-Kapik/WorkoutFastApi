from typing import Type, TypeVar, Generic, Any, Sequence
from sqlalchemy import select, exists, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Load
from typing import List

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
        """Получить коллекцию элементов с фильтрацией, сортировкой и пагинацией."""
        stmt = select(self.model).filter(*expressions).filter_by(**filters)

        if options:
            stmt = stmt.options(*options)

        if order_by is not None:
            stmt = stmt.order_by(
                *(order_by if isinstance(order_by, list) else [order_by])
            )
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def find_one(
        self,
        *expressions,
        options: Sequence[Load] | None = None,
        order_by=None,
        **filters
    ) -> T | None:
        """Получить один элемент по фильтрам."""
        stmt = select(self.model).filter(*expressions).filter_by(**filters)

        if options is not None:
            stmt = stmt.options(*options)

        if order_by is not None:
            stmt = stmt.order_by(
                *(order_by if isinstance(order_by, list) else [order_by])
            )
        stmt = stmt.limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id_with_options(
        self, id_: int, *options: Load
    ) -> T | None:
        """Получить элемент по ID с опциями загрузки."""
        stmt = select(self.model).where(self.model.id == id_)

        if options:
            stmt = stmt.options(*options)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, id_: int) -> T | None:
        """Получить элемент по ID."""
        return await self.session.get(self.model, id_)

    async def exists(self, *expressions, **filters) -> bool:
        """Проверить наличие элемента в базе."""
        stmt = select(
            exists(
                select(self.model).filter(*expressions).filter_by(**filters)
            )
        )
        result = await self.session.execute(stmt)
        return bool(result.scalar())

    async def create(self, **data: Any) -> T:
        """Создать новый элемент и сохранить в базе."""
        obj = self.model(**data)
        return await self.save(obj)

    async def save(self, obj: T) -> T:
        """Сохранить элемент в базе в рамках трансакции."""
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def update(
        self, *expressions, data: dict[str, Any], **filters
    ) -> List[T]:
        """Обновить элементы по фильтрам и вернуть их обновленные версии."""
        stmt = (
            update(self.model)
            .filter(*expressions)
            .filter_by(**filters)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete(self, *expressions, **filters) -> int:
        """Удалить элементы по фильтрам."""
        stmt = delete(self.model).filter(*expressions).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.rowcount

    async def count(self, *expressions, **filters) -> int:
        """Получить количество элементов по фильтрам."""
        stmt = select(func.count(self.model.id))
        if expressions:
            stmt = stmt.filter(*expressions)
        if filters:
            stmt = stmt.filter_by(**filters)

        result = await self.session.execute(stmt)
        return result.scalar_one()
