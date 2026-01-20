from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from app.core.config import settings

async_engine = create_async_engine(url=settings.db.DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        async with session.begin():
            yield session


"""Схема работы сессий и транзакций:

HTTP request
   ↓
get_session()
   ↓
session.begin()
   ↓
router
   ↓
service (без commit)
   ↓
dao
   ↓
возврат
   ↓
commit() или rollback() автоматически

------------------------------------------

database.py
  └── get_session (только session + transaction)

router
  └── try / except IntegrityError → HTTP

service
  └── бизнес-логика

dao
  └── ORM
"""
