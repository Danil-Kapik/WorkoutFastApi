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


async def get_test():
    pass
    # async with async_engine.connect() as conn:
    #     res = await conn.execute(text("SELECT VERSION()"))
    #     print(f"{res.first()=}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(get_test())
