import { useEffect, useState } from 'react'
import { progressApi } from '../api/progress'
import { ProgressResponse } from '../types/api'
import './Dashboard.css'

export function Dashboard() {
    const [progress, setProgress] = useState<ProgressResponse[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

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
                                    <span className="stat-label">Последняя попытка</span>
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
                <h2>История</h2>
                <div>Всего записей: {progress.length}</div>
            </div>
        </div>
    )
}
