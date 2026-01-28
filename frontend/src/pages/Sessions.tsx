import { useEffect, useState } from 'react'
import { sessionsApi } from '../api/sessions'
import { SessionResponse } from '../types/api'
import './Sessions.css'

const EXERCISE_TYPES = ['подтягивания', 'отжимания', 'приседания', 'планка']

export function Sessions() {
    const [sessions, setSessions] = useState<SessionResponse[]>([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const [page, setPage] = useState(1)
    const [total, setTotal] = useState(0)
    const [selectedExercise, setSelectedExercise] = useState<string>('')
    const [activeSessionId, setActiveSessionId] = useState<number | null>(null)
    const [repsInput, setRepsInput] = useState('')

    const PAGE_SIZE = 10

    useEffect(() => {
        const loadSessions = async () => {
            setLoading(true)
            setError('')
            try {
                let data
                if (selectedExercise) {
                    data = await sessionsApi.getByExercise(selectedExercise, page, PAGE_SIZE)
                } else {
                    data = await sessionsApi.getList(page, PAGE_SIZE)
                }
                setSessions(data.items)
                setTotal(data.total)
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Ошибка загрузки тренировок')
            } finally {
                setLoading(false)
            }
        }

        loadSessions()
    }, [page, selectedExercise])

    const handleStartSession = async (exerciseType: string) => {
        try {
            const session = await sessionsApi.start(exerciseType)
            setActiveSessionId(session.id)
            setSessions([session, ...sessions])
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Ошибка начала тренировки')
        }
    }

    const handleFinishSession = async (sessionId: number) => {
        if (!repsInput || isNaN(Number(repsInput))) {
            setError('Введите корректное количество повторений')
            return
        }

        try {
            const updatedSession = await sessionsApi.finish(sessionId, Number(repsInput))
            setSessions(sessions.map((s) => (s.id === sessionId ? updatedSession : s)))
            setActiveSessionId(null)
            setRepsInput('')
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Ошибка завершения тренировки')
        }
    }

    const totalPages = Math.ceil(total / PAGE_SIZE)

    return (
        <div className="page-container">
            <h1>Тренировки</h1>

            {error && <div className="page-error">Ошибка: {error}</div>}

            <section className="sessions-controls">
                <h2>Начать новую тренировку</h2>
                <div className="exercise-buttons">
                    {EXERCISE_TYPES.map((type) => (
                        <button
                            key={type}
                            className="exercise-btn"
                            onClick={() => handleStartSession(type)}
                            disabled={loading}
                        >
                            {type}
                        </button>
                    ))}
                </div>
            </section>

            <section className="sessions-filter">
                <h2>История тренировок</h2>
                <div className="filter-group">
                    <label htmlFor="exercise-select">Фильтр по упражнению:</label>
                    <select
                        id="exercise-select"
                        value={selectedExercise}
                        onChange={(e) => {
                            setSelectedExercise(e.target.value)
                            setPage(1)
                        }}
                    >
                        <option value="">Все упражнения</option>
                        {EXERCISE_TYPES.map((type) => (
                            <option key={type} value={type}>
                                {type}
                            </option>
                        ))}
                    </select>
                </div>
            </section>

            {loading && !sessions.length ? (
                <div className="page-loading">Загрузка тренировок...</div>
            ) : sessions.length === 0 ? (
                <div className="empty-state">
                    <p>Тренировок не найдено</p>
                </div>
            ) : (
                <>
                    <div className="sessions-list">
                        {sessions.map((session) => (
                            <div key={session.id} className="session-card">
                                <div className="session-header">
                                    <h3>{session.exercise_type}</h3>
                                    <span className="session-status">
                                        {session.finished_at ? 'Завершена' : 'В процессе'}
                                    </span>
                                </div>

                                <div className="session-details">
                                    <div className="detail">
                                        <span className="label">Начало:</span>
                                        <span className="value">
                                            {new Date(session.started_at).toLocaleString('ru-RU')}
                                        </span>
                                    </div>
                                    {session.finished_at && (
                                        <div className="detail">
                                            <span className="label">Завершение:</span>
                                            <span className="value">
                                                {new Date(session.finished_at).toLocaleString('ru-RU')}
                                            </span>
                                        </div>
                                    )}
                                    {session.reps && (
                                        <div className="detail">
                                            <span className="label">Повторений:</span>
                                            <span className="value">{session.reps}</span>
                                        </div>
                                    )}
                                    <div className="detail">
                                        <span className="label">Сложность:</span>
                                        <span className="value">{session.difficulty}</span>
                                    </div>
                                </div>

                                {!session.finished_at && activeSessionId !== session.id && (
                                    <button
                                        className="session-action-btn"
                                        onClick={() => setActiveSessionId(session.id)}
                                    >
                                        Завершить
                                    </button>
                                )}

                                {activeSessionId === session.id && !session.finished_at && (
                                    <div className="session-finish-form">
                                        <input
                                            type="number"
                                            value={repsInput}
                                            onChange={(e) => setRepsInput(e.target.value)}
                                            placeholder="Введите количество повторений"
                                            min="0"
                                        />
                                        <button
                                            className="session-action-btn confirm"
                                            onClick={() => handleFinishSession(session.id)}
                                            disabled={loading}
                                        >
                                            {loading ? 'Сохранение...' : 'Сохранить'}
                                        </button>
                                        <button
                                            className="session-action-btn cancel"
                                            onClick={() => {
                                                setActiveSessionId(null)
                                                setRepsInput('')
                                            }}
                                        >
                                            Отмена
                                        </button>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>

                    {totalPages > 1 && (
                        <div className="pagination">
                            <button onClick={() => setPage(1)} disabled={page === 1}>
                                Первая
                            </button>
                            <button onClick={() => setPage(page - 1)} disabled={page === 1}>
                                Предыдущая
                            </button>
                            <span className="page-info">
                                Страница {page} из {totalPages}
                            </span>
                            <button onClick={() => setPage(page + 1)} disabled={page === totalPages}>
                                Следующая
                            </button>
                            <button onClick={() => setPage(totalPages)} disabled={page === totalPages}>
                                Последняя
                            </button>
                        </div>
                    )}
                </>
            )}
        </div>
    )
}
