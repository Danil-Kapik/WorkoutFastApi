# 🚀 Быстрая интеграция компонентов

## В вашем Dashboard.tsx

Текущий код может быть заменён новыми компонентами:

### ДО (текущий код):
```tsx
<div className="progress-list">
    <h2>История тренировок</h2>
    <div className="filter-group">
        {/* ... фильтр ... */}
    </div>
    {sessions.length === 0 ? (
        <div className="empty-state">
            <p>Истории тренировок нет</p>
        </div>
    ) : (
        <>
            <div className="sessions-list">
                {sessions.map((session) => (
                    <div key={session.id} className="session-card">
                        {/* ... карточка ... */}
                    </div>
                ))}
            </div>
            {/* пагинация ... */}
        </>
    )}
</div>
```

### ПОСЛЕ (с новыми компонентами):
```tsx
import { WorkoutSessionList } from '../components'

// ... в JSX:
<div className="progress-list">
    <h2>История тренировок</h2>
    <div className="filter-group">
        <label htmlFor="history-filter">Фильтр:</label>
        <select
            id="history-filter"
            value={filterOption}
            onChange={(e) => {
                setFilterOption(e.target.value as FilterOption)
                setSessionsPage(1)
            }}
        >
            {EXERCISE_TYPES.map((option) => (
                <option key={option.value} value={option.value}>
                    {option.label}
                </option>
            ))}
        </select>
    </div>
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
        isLoading={false}
        onPageChange={setSessionsPage}
    />
</div>
```

## В других компонентах

### Простое использование карточки:
```tsx
import { WorkoutSessionCard } from '../components'

export function MyComponent() {
    const session = {
        id: 1,
        user_id: 1,
        exercise_type: 'подтягивания',
        difficulty: 'спортик',
        reps_per_set_at_start: 15,
        completed: true,
        notes: null,
        created_at: '2026-01-30T14:30:00Z',
        updated_at: '2026-01-30T14:35:00Z',
    }
    
    return <WorkoutSessionCard session={session} />
}
```

### С собственной пагинацией:
```tsx
import { useEffect, useState } from 'react'
import { WorkoutSessionList } from '../components'
import { sessionsApi } from '../api/sessions'
import type { SessionListResponse } from '../types/api'

export function AllSessions() {
    const [data, setData] = useState<SessionListResponse | null>(null)
    const [loading, setLoading] = useState(true)
    const [page, setPage] = useState(1)

    useEffect(() => {
        const load = async () => {
            setLoading(true)
            try {
                const result = await sessionsApi.getList(page, 10)
                setData(result)
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [page])

    return (
        <div>
            <h1>Все тренировки</h1>
            {data ? (
                <WorkoutSessionList
                    data={data}
                    isLoading={loading}
                    onPageChange={setPage}
                />
            ) : (
                <div>Ошибка загрузки</div>
            )}
        </div>
    )
}
```

## Преимущества новых компонентов

✅ **Чистота кода** - вместо 50+ строк JSX просто 10 строк  
✅ **Переиспользуемость** - один компонент для разных мест  
✅ **Тип-безопасность** - TypeScript не пропустит ошибки  
✅ **Легче тестировать** - простая логика  
✅ **Легче поддерживать** - изменения в одном месте  
✅ **Согласованность** - всегда одинаковый внешний вид  

## Стили

Компоненты уже имеют встроенные стили в CSS файлах:
- `WorkoutSessionCard.css`
- `WorkoutSessionList.css`

Если нужно переопределить стили, используйте селекторы:
- `.workout-session-card`
- `.workout-session-list`
- `.status-badge`
- `.pagination-controls`

Пример:
```css
/* ваш CSS */
.workout-session-card {
    border-color: #your-color;
}

.status-completed {
    background-color: #your-green;
}
```

## Типы

Все типы уже есть в `frontend/src/types/api.ts`:
```typescript
export interface SessionResponse { /* ... */ }
export interface SessionListResponse { /* ... */ }
```

Просто импортируйте:
```typescript
import type { SessionResponse, SessionListResponse } from '../types/api'
```

## Mock-данные для тестирования

В `WorkoutSessionExamples.ts` есть готовые mock-данные:
```typescript
import { 
    MOCK_SESSION_COMPLETED,
    MOCK_SESSION_NOT_COMPLETED,
    MOCK_SESSIONS_LIST 
} from '../components/WorkoutSessionExamples'

// используйте в своих тестах
```

## ❓ FAQ

**Q: Компоненты делают запросы?**  
A: Нет! Они только отображают данные. Все запросы вы делаете сами и передаёте результат.

**Q: Можно ли изменить пропсы?**  
A: Нет, пропсы соответствуют backend контракту. Если нужны другие данные - добавьте их в backend.

**Q: Почему нет Redux?**  
A: Для простых компонентов Redux не нужен. State управляется в родительском компоненте.

**Q: Можно ли добавить свои стили?**  
A: Да, компоненты используют классы CSS, которые можно переопределить.

**Q: Работает ли на мобильных?**  
A: Да, полностью адаптивны. CSS использует media queries.
