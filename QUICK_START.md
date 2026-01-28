# 🚀 Quick Start Guide

## Что создано

Полностью рабочий **React + Vite + TypeScript** frontend для вашего FastAPI backend.

## 📦 Что включено

✅ **5 страниц**: Login, Register, Dashboard, Sessions, Navigation
✅ **4 API модуля**: auth, progress, sessions + fetch wrapper
✅ **AuthContext**: управление user/token через React Context API
✅ **Protected routes**: защита страниц
✅ **TypeScript**: полная типизация
✅ **CSS Modules**: чистые стили без UI frameworks
✅ **5 зависимостей**: React, React-DOM (остальное dev-only)

## ⚡ За 2 минуты до запуска

### Терминал 1: Backend

```bash
cd app
uvicorn app.main:app --reload --port 8000
```

Проверьте: `http://localhost:8000/docs`

### Терминал 2: Frontend

```bash
cd frontend
npm install          # первый раз
npm run dev
```

Откроется: `http://localhost:5173`

## 🎯 Сразу работает

1. **Вход** — через username/password
2. **Регистрация** — через username/email/password
3. **Dashboard** — показывает весь прогресс пользователя
4. **Sessions** — запуск/завершение тренировок, история с пагинацией

## 📁 Файлы проекта

```
frontend/src/
├── api/client.ts           ← Fetch wrapper с Authorization
├── api/{auth,progress,sessions}.ts  ← API endpoints
├── auth/AuthContext.tsx    ← State management (user, token)
├── auth/RequireAuth.tsx    ← Protected routes
├── pages/{Login,Register,Dashboard,Sessions}.tsx  ← Страницы
├── components/Navigation.tsx        ← Меню
├── types/api.ts            ← TypeScript types
└── App.tsx                 ← Главный компонент
```

## 🔧 Если нужно изменить backend API URL

Отредактируй `frontend/.env`:

```
VITE_API_URL=http://localhost:8000
```

## 📝 Особенности кода

✅ **Чистый и понятный** — легко ориентироваться
✅ **Хорошо структурирован** — API, pages, components разделены
✅ **Типизирован** — TypeScript everywhere
✅ **Без лишнего** — Redux, MobX, React Query не нужны
✅ **Готов к продакшену** — `npm run build` создаёт `dist/`

## 🚨 Важные моменты

1. **Backend должен быть запущен** перед frontend
2. **JWT token** хранится в localStorage (автоматически)
3. **Authorization header** добавляется автоматически (в fetch wrapper)
4. **Protected pages** требуют авторизации (RequireAuth компонент)

## 🎓 Как добавить новую функцию

### Новый API endpoint

```typescript
// 1. Добавь тип в src/types/api.ts
export interface NewResponse { ... }

// 2. Создай функцию в src/api/ файле
export const api = {
  getNew: () => apiCall<NewResponse>('/endpoint')
}

// 3. Используй в компоненте
const data = await api.getNew()
```

### Новую страницу

```typescript
// 1. Создай src/pages/NewPage.tsx
export function NewPage() { ... }

// 2. Добавь в App.tsx тип Page и renderPage()
type Page = ... | 'newpage'
{currentPage === 'newpage' && <NewPage />}

// 3. Добавь кнопку в Navigation
<button onClick={() => onNavigate('newpage')}>...</button>
```

## 📊 Статус

| Функция | Статус |
|---------|--------|
| Login | ✅ |
| Register | ✅ |
| Dashboard | ✅ |
| Sessions | ✅ |
| Protected Routes | ✅ |
| Error Handling | ✅ |
| Pagination | ✅ |
| Filtering | ✅ |
| TypeScript | ✅ |
| Build | ✅ |

## 💾 Build для production

```bash
npm run build
# Создаст dist/ папку с готовым приложением
```

Затем раздавай содержимое `dist/` через nginx/apache/CDN.

## 🎯 Всё готово!

Откройте браузер и начните использовать 🎉

```
Frontend: http://localhost:5173
Backend:  http://localhost:8000
```

Вопросы? Смотри `FRONTEND_COMPLETE.md` или `README.md` в папке `frontend/`.
