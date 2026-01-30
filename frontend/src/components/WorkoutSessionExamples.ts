/**
 * Workout Components Usage Examples
 * 
 * This file demonstrates how to use WorkoutSessionCard and WorkoutSessionList
 * with real data structures matching the backend contract.
 */

import type { SessionResponse, SessionListResponse } from '../types/api'

// Mock data examples matching backend contract

export const MOCK_SESSION_COMPLETED: SessionResponse = {
    id: 1,
    user_id: 1,
    exercise_type: 'подтягивания',
    difficulty: 'спортик',
    reps_per_set_at_start: 15,
    completed: true,
    notes: 'Хорошо удалось, без проблем',
    created_at: '2026-01-30T14:30:00Z',
    updated_at: '2026-01-30T14:35:00Z',
}

export const MOCK_SESSION_NOT_COMPLETED: SessionResponse = {
    id: 2,
    user_id: 1,
    exercise_type: 'отжимания',
    difficulty: 'живчик',
    reps_per_set_at_start: 12,
    completed: false,
    notes: null,
    created_at: '2026-01-29T10:15:00Z',
    updated_at: '2026-01-29T10:15:00Z',
}

export const MOCK_SESSION_WITH_NOTES: SessionResponse = {
    id: 3,
    user_id: 1,
    exercise_type: 'тяга',
    difficulty: 'дохляк',
    reps_per_set_at_start: 5,
    completed: true,
    notes: 'Устал после работы, но справился',
    created_at: '2026-01-28T18:45:00Z',
    updated_at: '2026-01-28T18:50:00Z',
}

export const MOCK_SESSIONS_LIST: SessionListResponse = {
    items: [
        MOCK_SESSION_COMPLETED,
        MOCK_SESSION_NOT_COMPLETED,
        MOCK_SESSION_WITH_NOTES,
    ],
    total: 25,
    page: 1,
    size: 3,
    pages: 9,
    has_next: true,
    has_prev: false,
}

export const MOCK_SESSIONS_LIST_LAST_PAGE: SessionListResponse = {
    items: [
        {
            id: 24,
            user_id: 1,
            exercise_type: 'присед',
            difficulty: 'спортик',
            reps_per_set_at_start: 20,
            completed: true,
            notes: null,
            created_at: '2026-01-20T08:00:00Z',
            updated_at: '2026-01-20T08:05:00Z',
        },
        {
            id: 25,
            user_id: 1,
            exercise_type: 'подтягивания',
            difficulty: 'живчик',
            reps_per_set_at_start: 10,
            completed: true,
            notes: 'Последняя за месяц!',
            created_at: '2026-01-21T09:30:00Z',
            updated_at: '2026-01-21T09:35:00Z',
        },
    ],
    total: 25,
    page: 9,
    size: 3,
    pages: 9,
    has_next: false,
    has_prev: true,
}

export const MOCK_SESSIONS_LIST_EMPTY: SessionListResponse = {
    items: [],
    total: 0,
    page: 1,
    size: 10,
    pages: 0,
    has_next: false,
    has_prev: false,
}

/**
 * Example: Using WorkoutSessionCard
 * 
 * import { WorkoutSessionCard } from '../components'
 * 
 * export function CardExample() {
 *   return (
 *     <div>
 *       <h2>Завершённая сессия</h2>
 *       <WorkoutSessionCard session={MOCK_SESSION_COMPLETED} />
 *       
 *       <h2>Незавершённая сессия</h2>
 *       <WorkoutSessionCard session={MOCK_SESSION_NOT_COMPLETED} />
 *       
 *       <h2>Сессия с заметками</h2>
 *       <WorkoutSessionCard session={MOCK_SESSION_WITH_NOTES} />
 *     </div>
 *   )
 * }
 */

/**
 * Example: Using WorkoutSessionList
 * 
 * import { WorkoutSessionList } from '../components'
 * import { useState } from 'react'
 * 
 * export function ListExample() {
 *   const [page, setPage] = useState(1)
 *   const [data, setData] = useState(MOCK_SESSIONS_LIST)
 *   
 *   const handlePageChange = (newPage: number) => {
 *     if (newPage === 9) {
 *       setData(MOCK_SESSIONS_LIST_LAST_PAGE)
 *     } else if (newPage === 1) {
 *       setData(MOCK_SESSIONS_LIST)
 *     }
 *     setPage(newPage)
 *   }
 *   
 *   return (
 *     <WorkoutSessionList
 *       data={data}
 *       isLoading={false}
 *       onPageChange={handlePageChange}
 *     />
 *   )
 * }
 */

/**
 * Example: Real integration with API
 * 
 * import { useEffect, useState } from 'react'
 * import { WorkoutSessionList } from '../components'
 * import { sessionsApi } from '../api/sessions'
 * import type { SessionListResponse } from '../types/api'
 * 
 * export function RealIntegration() {
 *   const [data, setData] = useState<SessionListResponse | null>(null)
 *   const [loading, setLoading] = useState(true)
 *   const [error, setError] = useState<string | null>(null)
 *   const [page, setPage] = useState(1)
 *   
 *   useEffect(() => {
 *     const fetchSessions = async () => {
 *       setLoading(true)
 *       setError(null)
 *       try {
 *         const result = await sessionsApi.getList(page, 10)
 *         setData(result)
 *       } catch (err) {
 *         setError(err instanceof Error ? err.message : 'Unknown error')
 *       } finally {
 *         setLoading(false)
 *       }
 *     }
 *     
 *     fetchSessions()
 *   }, [page])
 *   
 *   if (error) return <div>Error: {error}</div>
 *   if (!data) return <div>Loading...</div>
 *   
 *   return (
 *     <div>
 *       <h1>Все тренировки</h1>
 *       <WorkoutSessionList
 *         data={data}
 *         isLoading={loading}
 *         onPageChange={setPage}
 *       />
 *     </div>
 *   )
 * }
 */

/**
 * Example: Filter by exercise type
 * 
 * import { useEffect, useState } from 'react'
 * import { WorkoutSessionList } from '../components'
 * import { sessionsApi } from '../api/sessions'
 * import type { SessionListResponse } from '../types/api'
 * 
 * export function FilteredSessions() {
 *   const [data, setData] = useState<SessionListResponse | null>(null)
 *   const [loading, setLoading] = useState(true)
 *   const [page, setPage] = useState(1)
 *   const [filter, setFilter] = useState<string>('подтягивания')
 *   
 *   useEffect(() => {
 *     const fetchSessions = async () => {
 *       setLoading(true)
 *       try {
 *         const result = await sessionsApi.getByExercise(filter, page, 10)
 *         setData(result)
 *       } finally {
 *         setLoading(false)
 *       }
 *     }
 *     
 *     fetchSessions()
 *   }, [page, filter])
 *   
 *   if (!data) return <div>Loading...</div>
 *   
 *   return (
 *     <div>
 *       <select onChange={(e) => setFilter(e.target.value)}>
 *         <option value="подтягивания">Подтягивания</option>
 *         <option value="отжимания">Отжимания</option>
 *         <option value="тяга">Тяга</option>
 *         <option value="присед">Присед</option>
 *       </select>
 *       
 *       <WorkoutSessionList
 *         data={data}
 *         isLoading={loading}
 *         onPageChange={setPage}
 *       />
 *     </div>
 *   )
 * }
 */
