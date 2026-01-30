import { useEffect, useState } from 'react'
import { sessionsApi } from '../api/sessions'
import { progressApi } from '../api/progress'
import { SessionResponse } from '../types'
import Toast from '../components/Toast'
import './Sessions.css'

const EXERCISE_TYPES = ['подтягивания', 'отжимания', 'тяга', 'присед']

export function Sessions() {
    const [sessions, setSessions] = useState<SessionResponse[]>([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const [toast, setToast] = useState<{ message: string; type?: 'info' | 'error' } | null>(null)
    const [continuingSession, setContinuingSession] = useState<SessionResponse | null>(null)
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
            setToast(null)
            setLoading(true)

            // Check if progress for this exercise exists
            const progress = await progressApi.getByExercise(exerciseType)
            if (progress) {
                setToast({ message: `Прогресс по упражнению "${exerciseType}" уже существует.`, type: 'info' })
                return
            }

            // Create progress with default starting reps and then start a session
            await progressApi.create({ exercise_type: exerciseType, current_reps_per_set: 1 })

            const session = await sessionsApi.start(exerciseType)
            setActiveSessionId(session.id)
            setSessions([session, ...sessions])
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Ошибка начала тренировки')
        } finally {
            setLoading(false)
        }
    }

    const handleContinueSession = async (exerciseType: string) => {
        try {
            setError('')
            setToast(null)
            setLoading(true)
            // Try to start a session; service will error if no progress
            const session = await sessionsApi.start(exerciseType)
            setContinuingSession(session)
            setActiveSessionId(session.id)
            setSessions([session, ...sessions])
        } catch (err) {
            // If start fails (no progress), show specific message
            setError(`Тренировка для упражнения ${exerciseType} не найдена`)
        } finally {
            setLoading(false)
        }
    }

    const handleCompleteContinue = async (completed: boolean) => {
        if (!continuingSession) return
        try {
            setError('')
            setToast(null)
            setLoading(true)
            const updated = await sessionsApi.finish(continuingSession.id, { completed })
            setSessions(sessions.map((s) => (s.id === updated.id ? updated : s)))
            setContinuingSession(null)
            setActiveSessionId(null)

            // show toast depending on result
            if (completed) {
                setToast({ message: 'Прогресс по тренировке сохранен', type: 'info' })
            } else {
                setToast({ message: 'В следующий раз постарайся!!', type: 'error' })
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Ошибка завершения тренировки')
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
            const updatedSession = await sessionsApi.finish(sessionId, {
                completed: true,
                notes: `reps:${Number(repsInput)}`,
            })
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
            {toast && (
                <Toast
                    message={toast.message}
                    type={toast.type as 'info' | 'error'}
                    onClose={() => setToast(null)}
                />
            )}

            <section className="sessions-controls">
                <h2>Продолжить тренировку</h2>
                <div className="exercise-buttons">
                    {EXERCISE_TYPES.map((type) => (
                        <button
                            key={type}
                            className="exercise-btn"
                            onClick={() => handleContinueSession(type)}
                            disabled={loading}
                        >
                            {type}
                        </button>
                    ))}
                </div>
            </section>

            {continuingSession && (
                <section className="sessions-controls">
                    <h2>Текущая попытка продолжения</h2>
                    <div className="session-card">
                        <div className="session-header">
                            <h3>{continuingSession.exercise_type}</h3>
                            <span className="session-status">{continuingSession.completed ? 'Завершена' : 'В процессе'}</span>
                        </div>

                        <div className="session-details">
                            <div className="detail">
                                <span className="label">Начало:</span>
                                <span className="value">{new Date(continuingSession.created_at).toLocaleString('ru-RU')}</span>
                            </div>
                            <div className="detail">
                                <span className="label">Сложность:</span>
                                <span className="value">{continuingSession.difficulty}</span>
                            </div>
                            <div className="detail">
                                <span className="label">Повторов в подходе:</span>
                                <span className="value">{continuingSession.reps_per_set_at_start}</span>
                            </div>
                        </div>

                        <div className="session-finish-form">
                            <button
                                className="session-action-btn confirm"
                                onClick={() => handleCompleteContinue(true)}
                                disabled={loading}
                            >
                                Выполнил
                            </button>
                            <button
                                className="session-action-btn cancel"
                                onClick={() => handleCompleteContinue(false)}
                                disabled={loading}
                            >
                                Сдулся
                            </button>
                        </div>
                    </div>
                </section>
            )}

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

