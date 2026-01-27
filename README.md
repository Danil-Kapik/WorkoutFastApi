# Fitness Tracker API

Асинхронный REST API для отслеживания прогресса в упражнениях с прогрессивным увеличением сложности.

## Описание проекта

Приложение позволяет пользователям:
- **Регистрироваться и входить** в систему с JWT аутентификацией
- **Отслеживать прогресс** по различным упражнениям (подтягивания, отжимания, тяга, присед)
- **Записывать тренировочные сессии** с фиксацией выполненного объёма
- **Автоматически повышать сложность** при достижении целевого количества повторений
- **Просматривать историю тренировок** с разбиением на страницы по упражнениям

## Стек технологий

- **FastAPI** - веб-фреймворк для создания REST API
- **SQLAlchemy 2.0+** - асинхронный ORM для работы с БД
- **PostgreSQL** - база данных (async через asyncpg)
- **Alembic** - управление миграциями
- **Pydantic** - валидация данных и сериализация
- **JWT** - аутентификация и авторизация
- **bcrypt** - хеширование паролей

## Структура проекта

```
app/
├── main.py                      # Точка входа приложения
├── core/
│   ├── config.py               # Конфигурация и переменные окружения
│   ├── database.py             # Инициализация БД и сессий
│   └── security.py             # JWT и хеширование паролей
├── models/
│   └── models.py               # SQLAlchemy модели (User, UserProgress, WorkoutSession)
├── schemas/
│   ├── users.py                # Pydantic схемы пользователя
│   ├── user_progress.py        # Схемы прогресса
│   └── workout_session.py      # Схемы тренировочной сессии
├── routers/
│   ├── auth.py                 # Маршруты аутентификации
│   ├── user_progress.py        # API прогресса
│   └── workout_session.py      # API тренировочных сессий
├── services/
│   ├── user_service.py         # Бизнес-логика пользователей
│   ├── user_progress_service.py # Логика управления прогрессом
│   └── workout_session_service.py # Логика тренировочных сессий
├── dao/
│   ├── base.py                 # Базовый класс DAO с CRUD операциями
│   ├── users_dao.py            # DAO для пользователей
│   ├── progress_dao.py         # DAO для прогресса
│   └── workout_session_dao.py  # DAO для сеансов
├── scripts/
│   ├── initial_data.py         # Скрипт заполнения тестовых данных
│   └── curl_test.py            # Примеры curl запросов
└── alembic/
    ├── env.py                  # Конфигурация Alembic
    └── versions/               # Файлы миграций
```

## Архитектура приложения

```
HTTP Request → Router → Service → DAO → Database
     ↓           ↓         ↓       ↓
  FastAPI    Validation  Business  SQL
             & Routing   Logic
```

- **Router** - обработка HTTP запросов, валидация input/output через Pydantic
- **Service** - бизнес-логика (регистрация, аутентификация, управление прогрессом)
- **DAO** - абстракция для работы с БД (CRUD операции)
- **Models** - SQLAlchemy модели с валидацией на уровне БД

## Установка и запуск

### Предварительные требования

- Python 3.10+
- PostgreSQL 12+
- pip

### 1. Клонирование репозитория

```bash
git clone https://github.com/ваш-username/FastAPIProject.git
cd FastAPIProject
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Конфигурация переменных окружения

Создайте файл `.env` в корне проекта:

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=your_password
DB_NAME=fitness_tracker

# Security
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Применение миграций

```bash
alembic -c alembic.ini upgrade head
```

### 6. Заполнение тестовых данных (опционально)

```bash
PYTHONPATH=. python -m app.scripts.initial_data
```

### 7. Запуск приложения

```bash
python -m uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: `http://localhost:8000`

Документация по API доступна по адресам:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication `/auth`

| Метод | Endpoint | Описание | Параметры |
|-------|----------|---------|-----------|
| POST | `/auth/register` | Регистрация пользователя | `username`, `email`, `password` |
| POST | `/auth/login` | Вход и получение JWT токена | `username`, `password` |
| GET | `/auth/me` | Получить информацию о текущем пользователе | Authorization header |

### User Progress `/progress`

| Метод | Endpoint | Описание |
|-------|----------|---------|
| GET | `/progress/` | Получить весь прогресс пользователя |
| GET | `/progress/by-exercise` | Получить прогресс по упражнению |
| POST | `/progress/` | Создать новый прогресс |

**Уровни сложности (Difficulty):**
- `дохляк` (BEGINNER) - 1-5 повторений
- `живчик` (INTERMEDIATE) - 6-12 повторений  
- `спортик` (ADVANCED) - 13-30 повторений

При достижении целевого количества повторений уровень автоматически повышается.

### Workout Sessions `/sessions`

| Метод | Endpoint | Описание |
|-------|----------|---------|
| POST | `/sessions/start` | Начать новую тренировочную сессию |
| PATCH | `/sessions/{session_id}/finish` | Завершить сессию |
| GET | `/sessions/` | Получить все сессии с пагинацией |
| GET | `/sessions/by-exercise` | Получить сессии по упражнению |
| GET | `/sessions/last` | Получить последнюю тренировочную сессию |

## Модели данных

### User (Пользователь)

```python
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  # password - хранится в хешированном виде
}
```

### UserProgress (Прогресс упражнения)

```python
{
  "id": 1,
  "user_id": 1,
  "exercise_type": "подтягивания",  # PULL_UPS | PUSH_UPS | DEADLIFT | SQUAT
  "difficulty": "дохляк",            # BEGINNER | INTERMEDIATE | ADVANCED
  "current_reps_per_set": 5,
  "last_success_at": "2024-01-27T12:30:00Z",
  "created_at": "2024-01-20T10:00:00Z",
  "updated_at": "2024-01-27T12:30:00Z"
}
```

### WorkoutSession (Тренировочная сессия)

```python
{
  "id": 1,
  "user_id": 1,
  "exercise_type": "подтягивания",
  "difficulty": "дохляк",
  "reps_per_set_at_start": 5,
  "completed": true,
  "notes": "Отличная тренировка!",
  "created_at": "2024-01-27T12:00:00Z",
  "updated_at": "2024-01-27T12:30:00Z"
}
```

## Поток работы приложения

1. **Регистрация/Вход**
   - Пользователь регистрируется с username и password
   - При входе получает JWT токен на 30 минут
   - Token передаётся в заголовке `Authorization: Bearer <token>` для всех защищённых запросов

2. **Создание прогресса**
   - Пользователь создаёт новый прогресс для упражнения (например, подтягивания)
   - На основе количества повторений определяется уровень сложности
   - Система сохраняет стартовое количество повторений

3. **Тренировочная сессия**
   - Пользователь начинает сессию для упражнения
   - Система берёт текущий прогресс и сложность из записи
   - После завершения сессии:
     - Если `completed: true` → увеличиваются повторения на 1
     - Система проверяет, достиг ли пользователь целевых повторений
     - При достижении целевых повторений → сложность повышается

4. **Просмотр статистики**
   - Пользователь может просмотреть весь свой прогресс
   - Может посмотреть историю сессий по упражнениям
   - Видит текущий уровень и количество повторений для каждого упражнения

## Разработка и тестирование

### Запуск тестов

```bash
pytest tests/
```

### Создание новой миграции

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Просмотр логов миграций

```bash
alembic current
alembic history
```

## Ошибки и коды ответов

- **200 OK** - Успешное выполнение запроса
- **201 Created** - Ресурс успешно создан
- **400 Bad Request** - Ошибка валидации данных
- **401 Unauthorized** - Требуется аутентификация
- **409 Conflict** - Username или упражнение уже существуют
- **422 Unprocessable Entity** - Ошибка в параметрах запроса
- **500 Internal Server Error** - Ошибка сервера

## Переменные окружения

| Переменная | Описание | Пример |
|-----------|---------|--------|
| `DB_HOST` | Хост PostgreSQL | localhost |
| `DB_PORT` | Порт PostgreSQL | 5432 |
| `DB_USER` | Пользователь БД | postgres |
| `DB_PASS` | Пароль БД | password |
| `DB_NAME` | Имя БД | fitness_tracker |
| `SECRET_KEY` | Секретный ключ для JWT | very-long-random-string |
| `ALGORITHM` | Алгоритм JWT | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни токена в минутах | 30 |

## Полезные команды

```bash
# Запуск сервера с автоперезагрузкой
python -m uvicorn app.main:app --reload

# Запуск в production режиме
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app

# Интерактивное тестирование API
python app/scripts/curl_test.py

# Проверка синтаксиса кода
python -m pylance app/

# Форматирование кода
black app/

# Проверка типов
mypy app/
```

## Документация кода

- Все основные методы содержат docstring с описанием функциональности
- Имена переменных и функций следуют стилю snake_case
- Типизация кода выполняется через Pydantic и SQLAlchemy Type Hints

## Лицензия

MIT

## Контакты

Для вопросов и предложений создавайте Issues в репозитории.
