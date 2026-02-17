import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.routers.auth import get_user_service
from unittest.mock import AsyncMock


@pytest.fixture
def mock_user_service():
    """Мок для UserService с настроенным поведением методов."""
    service = AsyncMock()
    # Настраиваем поведение метода authenticate_user
    service.authenticate_user.return_value = "fake-jwt-token"
    # Метод register_user ничего не возвращает по логике эндпоинта
    service.register_user.return_value = None
    return service


@pytest.mark.asyncio
async def test_register_user_success(mock_user_service):
    """Тест успешной регистрации пользователя."""
    # Переопределяем зависимость в FastAPI
    app.dependency_overrides[get_user_service] = lambda: mock_user_service

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as ac:
            response = await ac.post(
                "/auth/register",
                json={
                    "username": "testuser",
                    "email": "test@example.com",
                    "password": "password123",
                },
            )

        assert response.status_code == 201
        assert response.json() == {"message": "Вы успешно зарегистрированы!"}
        # Проверяем, что роутер передал данные в сервис
        mock_user_service.register_user.assert_called_once()
    finally:
        # Очищаем переопределения после теста
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_login_user_success(mock_user_service):
    """Тест успешной аутентификации пользователя и получения токена."""
    app.dependency_overrides[get_user_service] = lambda: mock_user_service

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as ac:
            # OAuth2PasswordRequestForm ожидает данные в формате form-data, а не JSON
            response = await ac.post(
                "/auth/login",
                data={
                    "username": "test@example.com",
                    "password": "password123",
                },
            )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["access_token"] == "fake-jwt-token"
        assert response_data["token_type"] == "bearer"
        # Проверяем, что сервис был вызван с правильными параметрами
        mock_user_service.authenticate_user.assert_called_once_with(
            "test@example.com", "password123"
        )
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_register_user_invalid_schema(mock_user_service):
    """Тест регистрации с неверной схемой данных."""
    app.dependency_overrides[get_user_service] = lambda: mock_user_service

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as ac:
            # Отправляем неполные данные
            response = await ac.post(
                "/auth/register",
                json={
                    "email": "test@example.com"
                    # password отсутствует
                },
            )

        assert response.status_code == 422  # Unprocessable Entity
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_login_user_invalid_data(mock_user_service):
    """Тест логина с неверными данными."""
    app.dependency_overrides[get_user_service] = lambda: mock_user_service

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as ac:
            # Отправляем неполные данные для логина
            response = await ac.post(
                "/auth/login",
                data={
                    "username": "test@example.com"
                    # password отсутствует
                },
            )

        assert response.status_code == 422  # Unprocessable Entity
    finally:
        app.dependency_overrides.clear()
