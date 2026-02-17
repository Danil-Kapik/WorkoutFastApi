import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.routers.user_progress import get_progress_service
from app.core.security import get_current_user
from app.models.models import ExerciseType, Difficulty, User
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime


@pytest.fixture
def mock_user():
    """Мок для текущего пользователя."""
    user = MagicMock(spec=User)
    user.id = 1
    user.username = "testuser"
    user.email = "test@example.com"
    return user


@pytest.fixture
def mock_progress_service():
    """Мок для UserProgressService."""
    service = AsyncMock()
    return service


@pytest.fixture
def mock_progress_data():
    """Мок-данные для прогресса пользователя."""
    return {
        "id": 1,
        "user_id": 1,
        "exercise_type": ExerciseType.PULL_UPS,
        "difficulty": Difficulty.BEGINNER,
        "current_reps_per_set": 5,
        "last_success_at": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }


def override_get_current_user(mock_user):
    """Функция для переопределения зависимости get_current_user."""

    async def _get_current_user():
        return mock_user

    return _get_current_user


@pytest.mark.asyncio
async def test_get_user_progress_success(
    mock_user, mock_progress_service, mock_progress_data
):
    """Тест получения всего прогресса пользователя."""
    # Мок возвращает список с одним прогрессом
    progress_obj = MagicMock()
    for key, value in mock_progress_data.items():
        setattr(progress_obj, key, value)

    mock_progress_service.get_user_progress.return_value = [progress_obj]

    app.dependency_overrides[get_current_user] = override_get_current_user(
        mock_user
    )
    app.dependency_overrides[get_progress_service] = (
        lambda: mock_progress_service
    )

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as ac:
            response = await ac.get("/progress/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]["user_id"] == 1
        assert data[0]["exercise_type"] == "подтягивания"

        # Проверяем, что сервис был вызван с правильными параметрами
        mock_progress_service.get_user_progress.assert_called_once_with(
            user_id=1
        )
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_progress_for_exercise_success(
    mock_user, mock_progress_service, mock_progress_data
):
    """Тест получения прогресса для конкретного упражнения."""
    progress_obj = MagicMock()
    for key, value in mock_progress_data.items():
        setattr(progress_obj, key, value)

    mock_progress_service.get_progress_for_exercise.return_value = progress_obj

    app.dependency_overrides[get_current_user] = override_get_current_user(
        mock_user
    )
    app.dependency_overrides[get_progress_service] = (
        lambda: mock_progress_service
    )

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as ac:
            response = await ac.get(
                "/progress/by-exercise?exercise_type=подтягивания"
            )

        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == 1
        assert data["exercise_type"] == "подтягивания"
        assert data["difficulty"] == "дохляк"
        assert data["current_reps_per_set"] == 5

        # Проверяем, что сервис был вызван с правильными параметрами
        mock_progress_service.get_progress_for_exercise.assert_called_once_with(
            user_id=1,
            exercise_type=ExerciseType.PULL_UPS,
        )
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_progress_for_exercise_not_found(
    mock_user, mock_progress_service
):
    """Тест получения прогресса когда упражнение не найдено."""
    mock_progress_service.get_progress_for_exercise.return_value = None

    app.dependency_overrides[get_current_user] = override_get_current_user(
        mock_user
    )
    app.dependency_overrides[get_progress_service] = (
        lambda: mock_progress_service
    )

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as ac:
            response = await ac.get(
                "/progress/by-exercise?exercise_type=подтягивания"
            )

        assert response.status_code == 200
        assert response.json() is None
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_progress_success(
    mock_user, mock_progress_service, mock_progress_data
):
    """Тест создания нового прогресса для упражнения."""
    progress_obj = MagicMock()
    for key, value in mock_progress_data.items():
        setattr(progress_obj, key, value)

    mock_progress_service.create_progress.return_value = progress_obj

    app.dependency_overrides[get_current_user] = override_get_current_user(
        mock_user
    )
    app.dependency_overrides[get_progress_service] = (
        lambda: mock_progress_service
    )

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as ac:
            response = await ac.post(
                "/progress/",
                json={
                    "exercise_type": "подтягивания",
                    "current_reps_per_set": 5,
                },
            )

        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == 1
        assert data["exercise_type"] == "подтягивания"
        assert data["current_reps_per_set"] == 5

        # Проверяем, что сервис был вызван с правильными параметрами
        mock_progress_service.create_progress.assert_called_once_with(
            user_id=1,
            exercise_type=ExerciseType.PULL_UPS,
            reps=5,
        )
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_progress_invalid_reps(mock_user, mock_progress_service):
    """Тест создания прогресса с невалидным количеством повторений."""
    app.dependency_overrides[get_current_user] = override_get_current_user(
        mock_user
    )
    app.dependency_overrides[get_progress_service] = (
        lambda: mock_progress_service
    )

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as ac:
            response = await ac.post(
                "/progress/",
                json={
                    "exercise_type": "подтягивания",
                    "current_reps_per_set": 0,  # Невалидное значение
                },
            )

        assert response.status_code == 422  # Validation error
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_progress_invalid_exercise_type(
    mock_user, mock_progress_service
):
    """Тест получения прогресса с невалидным типом упражнения."""
    app.dependency_overrides[get_current_user] = override_get_current_user(
        mock_user
    )
    app.dependency_overrides[get_progress_service] = (
        lambda: mock_progress_service
    )

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as ac:
            response = await ac.get(
                "/progress/by-exercise?exercise_type=невалидное"
            )

        assert response.status_code == 422  # Validation error
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_progress_missing_exercise_type(
    mock_user, mock_progress_service
):
    """Тест получения прогресса без параметра exercise_type."""
    app.dependency_overrides[get_current_user] = override_get_current_user(
        mock_user
    )
    app.dependency_overrides[get_progress_service] = (
        lambda: mock_progress_service
    )

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as ac:
            response = await ac.get("/progress/by-exercise")

        assert response.status_code == 422  # Missing required parameter
    finally:
        app.dependency_overrides.clear()
