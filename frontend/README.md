# Frontend для Workout Tracker

React + Vite + TypeScript приложение для управления тренировками.

## Требования

- Node.js 18+
- npm или yarn

## Установка

```bash
cd frontend
npm install
```

## Запуск

### Development сервер

```bash
npm run dev
```

Приложение откроется на `http://localhost:5173`

### Production build

```bash
npm run build
```

Собранные файлы находятся в папке `dist/`.

## Структура проекта

```
src/
├── api/               # API клиент и endpoints
│   ├── client.ts      # fetch wrapper с Authorization
│   ├── auth.ts        # auth endpoints
│   ├── progress.ts    # progress endpoints
│   └── sessions.ts    # sessions endpoints
├── auth/              # Авторизация
│   ├── AuthContext.tsx    # Context для управления user/token
│   └── RequireAuth.tsx    # компонент защиты роутов
├── pages/             # Страницы приложения
│   ├── Login.tsx          # Страница входа
│   ├── Register.tsx       # Страница регистрации
│   ├── Dashboard.tsx      # Страница прогресса
│   └── Sessions.tsx       # Страница тренировок
├── components/        # Переиспользуемые компоненты
│   └── Navigation.tsx      # Навигация
├── types/             # TypeScript типы
│   └── api.ts         # типы API ответов
├── App.tsx            # Главный компонент
├── main.tsx           # Entry point
└── index.css          # Глобальные стили
```

## Особенности

✅ React 18 + TypeScript
✅ Vite для быстрой разработки
✅ Context API для state management
✅ Fetch API с автоматическим Authorization header
✅ JWT token в localStorage
✅ Protected routes
✅ Чистый CSS (без UI frameworks)
✅ Минимум зависимостей

## API интеграция

Frontend автоматически подключается к backend на `http://localhost:8000`.

Если backend находится на другом адресе, измените `VITE_API_URL` в файле `.env`:

```
VITE_API_URL=http://your-backend-url:8000
```

## Особенности реализации

### Fetch API обёртка

Fetch обёртка в `src/api/client.ts` автоматически:
- Добавляет `Authorization: Bearer {token}` header
- Парсит JSON ответы
- Выбрасывает ошибку при `!res.ok`

### AuthContext

`AuthContext` хранит:
- `user` — текущий пользователь
- `token` — JWT access token
- `loading` — статус загрузки
- `initialized` — готовность приложения

Методы:
- `login(username, password)` — вход в систему
- `register(username, email, password)` — регистрация
- `logout()` — выход

### Protected Routes

Компонент `RequireAuth` защищает страницы от неавторизованного доступа.

## Развертывание

1. Собрать production версию:
   ```bash
   npm run build
   ```

2. Скопировать содержимое папки `dist/` на сервер

3. Настроить CORS на backend-е или использовать proxy

## Миграция при изменении backend API

Все типы и endpoints находятся в папке `src/api/` и `src/types/`, что облегчает обновление при изменениях backend.
