import { useEffect, useState } from 'react'
import { progressApi } from '../api/progress'
import { sessionsApi } from '../api/sessions'
import { ProgressResponse, SessionListResponse } from '../types/api'
import { WorkoutSessionList } from '../components'
import './Dashboard.css'

type FilterOption = 'all' | 'подтягивания' | 'отжимания' | 'тяга' | 'присед'

const EXERCISE_TYPES: { label: string; value: FilterOption }[] = [
    { label: 'Все', value: 'all' },
    { label: 'Подтягивания', value: 'подтягивания' },
    { label: 'Отжимания', value: 'отжимания' },
    { label: 'Становая', value: 'тяга' },
    { label: 'Присед', value: 'присед' },
]

export function Dashboard() {
    const [progress, setProgress] = useState<ProgressResponse[]>([])
    const [sessionsData, setSessionsData] = useState<SessionListResponse | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [sessionsPage, setSessionsPage] = useState(1)
    const [filterOption, setFilterOption] = useState<FilterOption>('all')

    const SESSIONS_PAGE_SIZE = 10

    useEffect(() => {
        const loadProgress = async () => {
            try {
                const data = await progressApi.getAll()
                setProgress(data)
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Ошибка загрузки прогресса')
            } finally {
                setLoading(false)
            }
        }

        loadProgress()
    }, [])

    useEffect(() => {
        const loadSessions = async () => {
            try {
                let data
                if (filterOption === 'all') {
                    data = await sessionsApi.getList(sessionsPage, SESSIONS_PAGE_SIZE)
                } else {
                    // by-exercise filter
                    data = await sessionsApi.getByExercise(filterOption, sessionsPage, SESSIONS_PAGE_SIZE)
                }
                setSessionsData(data)
            } catch (err) {
                console.error('Ошибка загрузки истории тренировок:', err)
            }
        }

        loadSessions()
    }, [sessionsPage, filterOption])

    if (loading) {
        return <div className="page-loading">Загрузка прогресса...</div>
    }

    if (error) {
        return <div className="page-error">Ошибка: {error}</div>
    }

    if (progress.length === 0) {
        return (
            <div className="page-container">
                <h1>Ваш прогресс</h1>
                <div className="empty-state">
                    <p>У вас нет записей о прогрессе</p>
                    <p>Начните тренировку, чтобы добавить первую запись</p>
                </div>
            </div>
        )
    }

    return (
        <div className="page-container">
            <h1>Ваш прогресс</h1>

            <div className="progress-grid">
                {progress.map((item) => (
                    <div key={item.id} className="progress-card">
                        <h3>{item.exercise_type}</h3>
                        <div className="progress-stats">
                            <div className="stat">
                                <span className="stat-label">Повторения</span>
                                <span className="stat-value">{item.current_reps_per_set}</span>
                            </div>
                            <div className="stat">
                                <span className="stat-label">Сложность</span>
                                <span className="stat-value">{item.difficulty}</span>
                            </div>
                            {item.last_success_at && (
                                <div className="stat">
                                    <span className="stat-label">Последняя успешная попытка</span>
                                    <span className="stat-value">
                                        {new Date(item.last_success_at).toLocaleDateString('ru-RU')}
                                    </span>
                                </div>
                            )}
                            <div className="stat">
                                <span className="stat-label">Дата создания</span>
                                <span className="stat-value">{new Date(item.created_at).toLocaleDateString('ru-RU')}</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

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
                {sessionsData && (
                    <WorkoutSessionList
                        data={sessionsData}
                        isLoading={false}
                        onPageChange={setSessionsPage}
                    />
                )}
            </div>
        </div>
    )
}
