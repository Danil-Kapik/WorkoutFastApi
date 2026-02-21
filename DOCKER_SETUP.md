# Docker Setup Guide

## 📋 Структура Docker-конфигурации

Проект полностью докеризирован для production-ready развёртывания.

### Созданные файлы

```
├── docker-compose.yml          # Оркестрация 3 сервисов
├── .dockerignore               # Root-level ignore для контекста
├── .env.example                # Пример переменных окружения
├── app/
│   ├── Dockerfile              # FastAPI backend
│   └── .dockerignore           # Backend-specific ignore
└── frontend/
    ├── Dockerfile              # React + Nginx (multi-stage)
    ├── .dockerignore           # Frontend-specific ignore
    └── nginx.conf              # Nginx конфиг с reverse proxy
```

## 🚀 Быстрый старт

### 1️⃣ Подготовка окружения

Создайте `.env` файл из примера:

```bash
cp .env.example .env
```

Обновите переменные окружения (необязательно для локальной разработки):

```env
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=fitness_db
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2️⃣ Запуск проекта

```bash
# Сборка и запуск всех сервисов
docker compose up --build

# Или в фоновом режиме
docker compose up --build -d
```

**Ожидаемый вывод:** Все 3 сервиса должны запуститься и пройти healthchecks.

### 3️⃣ Доступ к приложению

- **Frontend:** http://localhost (Nginx на порту 80)
- **Backend API:** http://localhost:8000
- **API docs (Swagger):** http://localhost:8000/docs
- **Database:** localhost:5432

### 4️⃣ Выполнение команд в контейнере

```bash
# Запуск миграций вручную (они автоматически выполняются при старте)
docker compose exec backend alembic upgrade head

# Сидирование базы данных
docker compose exec backend python -m app.scripts.initial_data

# Запуск тестов
docker compose exec backend pytest

# Bash в backend контейнере
docker compose exec backend bash
```

## 📦 Архитектура Docker-образов

### Backend (FastAPI)

**Image:** `python:3.11-slim`

✅ **Оптимизации:**

- Slim образ для уменьшения размера
- Системные зависимости для `asyncpg`, `psycopg3`, `cryptography`, `cffi`
- `--no-cache-dir` при установке pip
- `PYTHONDONTWRITEBYTECODE=1` + `PYTHONUNBUFFERED=1`
- Healthcheck каждые 30 секунд
- Автоматические миграции перед стартом

✅ **Переменные окружения:**

```python
PYTHONDONTWRITEBYTECODE=1      # Не создавать .pyc
PYTHONUNBUFFERED=1              # Вывод в реальном времени
PIP_NO_CACHE_DIR=1              # Не кешировать pip
```

✅ **Стартовая команда:**

```bash
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --loop uvloop
```

### Frontend (React + Nginx)

**Image:** Multi-stage build
- Build stage: `node:18-alpine`
- Production: `nginx:stable-alpine`

✅ **Особенности:**

- Multi-stage для минимизации размера финального образа
- SPA routing (`try_files $uri $uri/ /index.html`)
- Reverse proxy на backend (`/api/` → `http://backend:8000/`)
- Gzip compression
- Кеширование статических ассетов
- Non-root nginx пользователь для безопасности

✅ **Nginx routing:**

```
/              → SPA (index.html)
/api/*         → Backend (http://backend:8000/*)
/health        → Health check
static assets  → Кешируются на 1 год
```

### PostgreSQL

**Image:** `postgres:15-alpine`

✅ **Особенности:**

- Healthcheck (pg_isready) каждые 5 секунд, 5 попыток
- Персистентность через `postgres_data` volume
- Автоматическое создание БД и пользователя

## 🔧 Детали конфигурации

### docker-compose.yml - Ключевые параметры

```yaml
services:
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ..."]  # Проверка готовности
      interval: 5s
      timeout: 5s
      retries: 5
  
  backend:
    depends_on:
      db:
        condition: service_healthy                # Ждёт, пока БД готова
    environment:
      DB_HOST: db                                 # DNS имя сервиса
      # ... остальные переменные из .env
  
  frontend:
    depends_on:
      - backend                                   # Просто ждёт старта
```

### Сетевые настройки

```yaml
networks:
  app-network:
    driver: bridge
```

Все сервисы в одной сети → могут общаться по DNS имени:
- backend → db (посредством `postgresql://db:5432`)
- frontend → backend (посредством `http://backend:8000`)

### Volumes

```yaml
volumes:
  postgres_data:     # Именованный volume для persistency БД
```

## 🛡️ Security Best Practices

1. **Secret Key:** Измените `SECRET_KEY` в production
   ```env
   SECRET_KEY=your-actual-production-secret-key
   ```

2. **Database credentials:** Используйте secure переменные в production
   ```bash
   docker run --env-file /run/secrets/db_creds ...
   ```

3. **Non-root user:** Nginx запускается от `nginx:nginx` (UID 101)

4. **CORS:** Настроены для Docker (`http://frontend`, `http://localhost`)

5. **Healthchecks:** Все сервисы имеют healthchecks

## 📊 Мониторинг и логирование

### Просмотр логов

```bash
# Все сервисы
docker compose logs -f

# Конкретный сервис
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db

# Последние 100 строк
docker compose logs --tail=100
```

### Статус сервисов

```bash
docker compose ps
```

## 🧹 Очистка и управление

```bash
# Остановить все контейнеры
docker compose down

# Удалить volume (БД)
docker compose down -v

# Пересборка без кеша
docker compose build --no-cache

# Просмотр размеров образов
docker images | grep fastapi

# Очистка неиспользуемых образов
docker image prune -a
```

## 🐛 Troubleshooting

### Backend не коннектится к БД

```bash
# Проверить healthcheck БД
docker compose ps

# Посмотреть логи backend
docker compose logs backend

# Проверить переменные окружения
docker compose exec backend env | grep DB
```

### Frontend показывает 502 Bad Gateway

```bash
# Проверить, запущен ли backend
docker compose ps

# Проверить логи frontend (nginx)
docker compose logs frontend

# Проверить connectivity
docker compose exec frontend ping backend
```

### Миграции не выполнены

```bash
# Запустить миграции вручную
docker compose exec backend alembic upgrade head

# Проверить историю миграций
docker compose exec backend alembic history
```

### Ошибка "Cannot connect to database"

```bash
# Убедиться, что БД инициализирована
docker compose logs db

# Перестартовать БД
docker compose restart db

# Проверить соединение
docker compose exec backend python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
```

## 📈 Production Considerations

### Environment Variables

Используйте `.env` файл для:
- Development: локальные значения
- Production: выставляйте переменные через:
  - `docker run -e VAR=value`
  - `--env-file production.env`
  - Docker Secrets (Docker Swarm)
  - Container orchestration (Kubernetes)

### Database Persistence

```bash
# Посмотреть volumes
docker volume ls

# Создать backup
docker compose exec db pg_dump -U postgres fitness_db > backup.sql

# Restore
docker compose exec -T db psql -U postgres < backup.sql
```

### Resource Limits

Добавьте в docker-compose.yml для production:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### Reverse Proxy (Production)

Поставьте перед Nginx свой reverse proxy:
- Traefik
- HAProxy
- Caddy

Это обеспечит:
- SSL/TLS termination
- Load balancing
- DDoS protection

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push Docker Images

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: docker/build-push-action@v4
        with:
          context: ./app
          push: true
          tags: yourregistry/fastapi-backend:latest
```

## 📚 Дополнительные ресурсы

- [Docker compose documentation](https://docs.docker.com/compose/)
- [FastAPI deployment](https://fastapi.tiangolo.com/deployment/)
- [SQLAlchemy async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic migrations](https://alembic.sqlalchemy.org/)
- [Nginx configuration](https://nginx.org/en/docs/)

---

**Версия:** 1.0  
**Last Updated:** February 21, 2026  
**Project:** FastAPI Fitness Tracker
