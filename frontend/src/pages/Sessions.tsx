import { useEffect, useState } from 'react'
import { sessionsApi } from '../api/sessions'
import { SessionResponse } from '../types/api'
import './Sessions.css'

const EXERCISE_TYPES = ['подтягивания', 'отжимания', 'тяга', 'присед']

export function Sessions() {
    const [sessions, setSessions] = useState<SessionResponse[]>([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const [activeSessionId, setActiveSessionId] = useState<number | null>(null)
    const [repsInput, setRepsInput] = useState('')

    useEffect(() => {
        const loadLatestSession = async () => {
            // Fetch latest sessions to show current status if needed
            try {
                const data = await sessionsApi.getList(1, 1)
                if (data.items.length > 0) {
                    const latestSession = data.items[0]
                    if (!latestSession.completed) {
                        setActiveSessionId(latestSession.id)
                    }
                }
            } catch (err) {
                console.error('Ошибка загрузки последней тренировки:', err)
            }
        }

        loadLatestSession()
    }, [])

    const handleStartSession = async (exerciseType: string) => {
        try {
            setError('')
            setLoading(true)
            const session = await sessionsApi.start(exerciseType)
            setActiveSessionId(session.id)
            setSessions([session, ...sessions])
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Ошибка начала тренировки')
        } finally {
            setLoading(false)
        }
    }

    const handleFinishSession = async (sessionId: number) => {
        if (!repsInput || isNaN(Number(repsInput))) {
            setError('Введите корректное количество повторений')
            return
        }

        try {
            setLoading(true)
            const updatedSession = await sessionsApi.finish(sessionId, Number(repsInput))
            setSessions(sessions.map((s) => (s.id === sessionId ? updatedSession : s)))
            setActiveSessionId(null)
            setRepsInput('')
            setError('')
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Ошибка завершения тренировки')
        } finally {
            setLoading(false)
        }
    }

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

            {activeSessionId !== null && (
                <section className="active-session">
                    <h2>Текущая тренировка</h2>
                    {sessions.map((session) => {
                        if (session.id === activeSessionId && !session.completed) {
                            return (
                                <div key={session.id} className="session-card">
                                    <div className="session-header">
                                        <h3>{session.exercise_type}</h3>
                                        <span className="session-status">В процессе</span>
                                    </div>

                                    <div className="session-details">
                                        <div className="detail">
                                            <span className="label">Начало:</span>
                                            <span className="value">
                                                {new Date(session.created_at).toLocaleString('ru-RU')}
                                            </span>
                                        </div>
                                        <div className="detail">
                                            <span className="label">Сложность:</span>
                                            <span className="value">{session.difficulty}</span>
                                        </div>
                                    </div>

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
                                            {loading ? 'Сохранение...' : 'Завершить тренировку'}
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
                                </div>
                            )
                        }
                        return null
                    })}
                </section>
            )}

            <section className="sessions-info">
                <p>История ваших тренировок доступна на вкладке "Прогресс"</p>
            </section>
        </div>
    )
}
