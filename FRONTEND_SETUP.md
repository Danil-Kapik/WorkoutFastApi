# Workspace Setup Instructions

## Структура проекта

```
FastAPIProject/
├── app/                    # FastAPI backend
│   ├── main.py
│   ├── core/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── dao/
│   └── alembic/           # Database migrations
└── frontend/              # React + Vite + TypeScript
    ├── src/
    ├── public/
    └── package.json
```

## Запуск проекта (локально)

### Шаг 1: Backend

```bash
# Из корня проекта (FastAPIProject/)
cd app

# Убедитесь, что файл .env содержит правильные данные БД
cat .env

# Запустите Alembic миграции (если нужно)
alembic -c alembic.ini upgrade head

# Запустите FastAPI сервер
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend будет доступен на `http://localhost:8000`
API документация: `http://localhost:8000/docs`

### Шаг 2: Frontend

```bash
# В другом терминале, из корня проекта (FastAPIProject/)
cd frontend

# Установите зависимости (если ещё не установлены)
npm install

# Запустите dev сервер
npm run dev
```

Frontend будет доступен на `http://localhost:5173`

## Переменные окружения

### Backend (.env)

```
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=password
DB_NAME=workout_db
```

### Frontend (.env)

```
VITE_API_URL=http://localhost:8000
```

## Build для production

### Backend

Backend не требует сборки, используется как-есть через uvicorn.

### Frontend

```bash
cd frontend
npm run build
# Результат в папке dist/
```

## Основные функции

### Авторизация
- ✅ Вход (OAuth2 с username/password)
- ✅ Регистрация (username, email, password)
- ✅ JWT token в localStorage
- ✅ Автоматическая загрузка user при открытии приложения

### Управление прогрессом
- ✅ Просмотр всех записей о прогрессе
- ✅ Группировка по типам упражнений
- ✅ Статистика (последний результат, среднее, количество записей)
- ✅ Таблица со всеми записями

### Тренировки (Sessions)
- ✅ Начало новой тренировки
- ✅ Завершение тренировки с вводом количества повторений
- ✅ История тренировок с пагинацией
- ✅ Фильтр по типам упражнений
- ✅ Статусы (в процессе / завершена)

## Архитектура Frontend

### API Layer (`src/api/`)
- `client.ts` — fetch wrapper с автоматическим Authorization header
- `auth.ts` — endpoints авторизации
- `progress.ts` — endpoints прогресса
- `sessions.ts` — endpoints тренировок

### Auth Layer (`src/auth/`)
- `AuthContext.tsx` — React Context для управления user/token
- `RequireAuth.tsx` — компонент защиты роутов

### Pages (`src/pages/`)
- `Login.tsx` — страница входа
- `Register.tsx` — страница регистрации
- `Dashboard.tsx` — страница с прогрессом
- `Sessions.tsx` — страница с тренировками

### Components (`src/components/`)
- `Navigation.tsx` — навигация между страницами

## Особенности реализации

✅ **Минимум зависимостей**: React, React-DOM и Vite
✅ **TypeScript**: полная типизация API ответов
✅ **Context API**: state management без Redux/MobX
✅ **Fetch API**: собственная обёртка вместо React Query
✅ **CSS Modules / Plain CSS**: никаких UI frameworks
✅ **Clean Architecture**: удобно расширяется при изменении backend API

## Типичный workflow разработки

1. Backend что-то изменил → обнови `src/types/api.ts`
2. Новый endpoint → добавь в соответствующий файл `src/api/`
3. Новая страница → создай в `src/pages/`
4. Новый компонент → создай в `src/components/`

## Troubleshooting

### CORS ошибка при запросе к backend

Убедитесь, что backend запущен на `http://localhost:8000` и есть CORS поддержка.
Если frontend на другом адресе, обновите `VITE_API_URL` в `.env`

### 404 при получении /auth/me

Убедитесь, что:
- Backend запущен
- Token валидный (сохранён в localStorage)
- Authorization header правильно отправляется

### Blank page при загрузке

Проверьте консоль браузера (F12) на ошибки JavaScript/TypeScript.

## Развертывание

### На сервер

1. **Backend** — используйте gunicorn/uvicorn с nginx
2. **Frontend** — разместите содержимое папки `dist/` на web сервер или используйте статик хостинг

### Environment Variables на сервере

```bash
# Backend .env
DB_HOST=<production_db_host>
DB_PORT=5432
DB_USER=<db_user>
DB_PASS=<db_password>
DB_NAME=<db_name>

# Frontend .env
VITE_API_URL=https://api.yourdomain.com
```

## Контакты / Поддержка

Все файлы хорошо структурированы и комментированы. При изменении backend API просто обнови соответствующие файлы в `src/api/` и `src/types/`.
