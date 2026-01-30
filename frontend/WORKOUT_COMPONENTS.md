# WorkoutSession Components

Компоненты React для отображения workout-сессий, основанные на backend контракте.

## Типы (TypeScript)

```typescript
// из frontend/src/types/api.ts

export interface SessionResponse {
    id: number
    user_id: number
    exercise_type: string          // "подтягивания", "отжимания", "тяга", "присед"
    difficulty: string             // "дохляк", "живчик", "спортик"
    reps_per_set_at_start: number  // количество повторений
    completed: boolean              // статус завершения
    notes: string | null            // опциональные заметки
    created_at: string              // ISO 8601 дата
    updated_at: string              // ISO 8601 дата
}

export interface SessionListResponse {
    items: SessionResponse[]
    total: number                   // всего записей
    page: number                    // текущая страница
    size: number                    // размер страницы
    pages: number                   // всего страниц
    has_next: boolean               // есть ли следующая страница
    has_prev: boolean               // есть ли предыдущая страница
}
```

## Компоненты

### WorkoutSessionCard

Компонент для отображения одной workout-сессии.

**Пропсы:**
- `session: SessionResponse` - данные сессии

**Отображает:**
- Название упражнения (exercise_type)
- Статус завершения (completed)
- Сложность (difficulty)
- Количество повторений (reps_per_set_at_start)
- Заметки (notes, если не null)
- Дату создания (created_at, форматированная)

**Пример использования:**

```tsx
import { WorkoutSessionCard } from '../components'
import type { SessionResponse } from '../types/api'

const session: SessionResponse = {
    id: 1,
    user_id: 1,
    exercise_type: "подтягивания",
    difficulty: "спортик",
    reps_per_set_at_start: 15,
    completed: true,
    notes: "Легко удалось",
    created_at: "2026-01-30T10:30:00Z",
    updated_at: "2026-01-30T10:35:00Z"
}

export function MyComponent() {
    return <WorkoutSessionCard session={session} />
}
```

### WorkoutSessionList

Компонент для отображения списка workout-сессий с пагинацией.

**Пропсы:**
- `data: SessionListResponse` - объект с массивом сессий и информацией о пагинации
- `isLoading?: boolean` - флаг загрузки (по умолчанию false)
- `onPageChange?: (newPage: number) => void` - callback для смены страницы

**Отображает:**
- Сетка карточек сессий (WorkoutSessionCard)
- Пустое состояние, если нет сессий
- Состояние загрузки
- Кнопки пагинации (только если страниц > 1)
- Информацию о текущей странице и общем количестве записей

**Пример использования:**

```tsx
import { useEffect, useState } from 'react'
import { WorkoutSessionList } from '../components'
import { sessionsApi } from '../api/sessions'
import type { SessionListResponse } from '../types/api'

export function WorkoutsPage() {
    const [data, setData] = useState<SessionListResponse | null>(null)
    const [loading, setLoading] = useState(false)
    const [page, setPage] = useState(1)

    useEffect(() => {
        const loadSessions = async () => {
            setLoading(true)
            try {
                const result = await sessionsApi.getList(page, 10)
                setData(result)
            } catch (error) {
                console.error('Failed to load sessions:', error)
            } finally {
                setLoading(false)
            }
        }

        loadSessions()
    }, [page])

    if (!data) return <div>Ошибка загрузки</div>

    return (
        <WorkoutSessionList
            data={data}
            isLoading={loading}
            onPageChange={setPage}
        />
    )
}
```

## Особенности

### 1. Строгое соответствие backend контракту
- Типы полностью совпадают с `WorkoutSessionReadSchema` и `PaginatedResponse`
- Компоненты отображают только то, что приходит с API
- Нет придумывания данных на фронте

### 2. Компонент карточки (WorkoutSessionCard)
- Принимает только данные, не делает запросов
- Форматирует дату в читаемый вид (ru-RU)
- Отображает статус с цветной подсказкой
- Условно показывает заметки (если не null)
- Адаптивен под мобильные устройства

### 3. Компонент списка (WorkoutSessionList)
- Управляет пагинацией через коллбэк
- Использует has_next/has_prev из API для кнопок
- Показывает информацию о странице (page / pages)
- Показывает общее количество записей
- Обрабатывает состояния: загрузка, пусто, с данными

### 4. Стиль и UX
- Чистый и минималистичный дизайн
- Хорошая визуальная иерархия
- Полностью адаптивен (мобильный, планшет, ПК)
- Хорошая контрастность и читаемость
- Плавные переходы и анимации

## Интеграция в существующий проект

### В Dashboard.tsx:

```tsx
import { WorkoutSessionList } from '../components'
import { sessionsApi } from '../api/sessions'

// Используйте вместо текущего JSX:
<WorkoutSessionList
    data={{
        items: sessions,
        total: sessionsTotal,
        page: sessionsPage,
        size: SESSIONS_PAGE_SIZE,
        pages: totalSessionPages,
        has_next: sessionsPage < totalSessionPages,
        has_prev: sessionsPage > 1,
    }}
    isLoading={loading}
    onPageChange={setSessionsPage}
/>
```

## Без Redux, React Query и UI-библиотек

Компоненты используют только:
- React и TypeScript
- Встроенные хуки (useState, useEffect)
- Чистый CSS для стилизации
- Никаких зависимостей от сторонних библиотек UI

## Структура файлов

```
frontend/src/
├── components/
│   ├── index.ts                    # экспорты компонентов
│   ├── WorkoutSessionCard.tsx       # карточка одной сессии
│   ├── WorkoutSessionCard.css       # стили карточки
│   ├── WorkoutSessionList.tsx       # список сессий
│   └── WorkoutSessionList.css       # стили списка
├── types/
│   └── api.ts                       # типы SessionResponse, SessionListResponse
└── api/
    └── sessions.ts                  # API методы (getList, getByExercise)
```

## Data Flow

```
API Response (backend)
    ↓
SessionListResponse (типы)
    ↓
WorkoutSessionList (компонент)
    ├─ map → WorkoutSessionCard × N
    └─ Pagination Controls
    
Пользователь кликает "Next"
    ↓
onPageChange callback
    ↓
Родительский компонент обновляет page
    ↓
useEffect загружает новые данные
    ↓
WorkoutSessionList получает новые данные
    ↓
Компоненты перерисовываются
```
