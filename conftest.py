from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base
import pytest
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    """Создает event loop для всей сессии тестов."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def session():
    """Создает чистую базу данных и сессию для каждого теста"""
    # 1. Создаем движок для работы с БД в памяти
    engine = create_engine("sqlite:///:memory:")

    # 2. Создаем все таблицы, описанные в моделях
    Base.metadata.create_all(engine)

    # 3. Настраиваем фабрику сессий
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()

    yield session  # Передаем сессию в тест

    # 4. После завершения теста закрываем сессию и удаляем таблицы
    session.close()
    Base.metadata.drop_all(engine)
