import { SessionListResponse } from '../types/api'
import { WorkoutSessionCard } from './WorkoutSessionCard'
import './WorkoutSessionList.css'

interface WorkoutSessionListProps {
    data: SessionListResponse
    isLoading?: boolean
    onPageChange?: (newPage: number) => void
}

export function WorkoutSessionList({ data, isLoading = false, onPageChange }: WorkoutSessionListProps) {
    const handlePrevPage = () => {
        if (data.has_prev && onPageChange) {
            onPageChange(data.page - 1)
        }
    }

    const handleNextPage = () => {
        if (data.has_next && onPageChange) {
            onPageChange(data.page + 1)
        }
    }

    if (isLoading) {
        return <div className="workout-session-list-loading">Загрузка...</div>
    }

    if (data.items.length === 0) {
        return <div className="workout-session-list-empty">Тренировки не найдены</div>
    }

    return (
        <div className="workout-session-list">
            <div className="sessions-container">
                {data.items.map((session) => (
                    <WorkoutSessionCard key={session.id} session={session} />
                ))}
            </div>

            {data.pages > 1 && (
                <div className="pagination-controls">
                    <button
                        className="pagination-btn prev-btn"
                        onClick={handlePrevPage}
                        disabled={!data.has_prev}
                        aria-label="Предыдущая страница"
                    >
                        ← Предыдущая
                    </button>

                    <div className="pagination-info">
                        <span className="page-number">
                            {data.page} из {data.pages}
                        </span>
                        <span className="total-count">
                            Всего: {data.total}
                        </span>
                    </div>

                    <button
                        className="pagination-btn next-btn"
                        onClick={handleNextPage}
                        disabled={!data.has_next}
                        aria-label="Следующая страница"
                    >
                        Следующая →
                    </button>
                </div>
            )}
        </div>
    )
}
