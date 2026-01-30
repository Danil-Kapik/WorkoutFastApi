import { SessionResponse } from '../types/api'
import './WorkoutSessionCard.css'

interface WorkoutSessionCardProps {
    session: SessionResponse
}

export function WorkoutSessionCard({ session }: WorkoutSessionCardProps) {
    const formatDate = (dateString: string): string => {
        return new Date(dateString).toLocaleString('ru-RU', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
        })
    }

    const getStatusClass = (completed: boolean): string => {
        return completed ? 'status-completed' : 'status-not-completed'
    }

    const getStatusText = (completed: boolean): string => {
        return completed ? 'Завершена' : 'Не завершена'
    }

    return (
        <div className="workout-session-card">
            <div className="card-header">
                <h3 className="exercise-title">{session.exercise_type}</h3>
                <span className={`status-badge ${getStatusClass(session.completed)}`}>
                    {getStatusText(session.completed)}
                </span>
            </div>

            <div className="card-body">
                <div className="info-row">
                    <span className="label">Сложность:</span>
                    <span className="value">{session.difficulty}</span>
                </div>

                <div className="info-row">
                    <span className="label">Повторения:</span>
                    <span className="value">{session.reps_per_set_at_start}</span>
                </div>

                {session.notes && (
                    <div className="info-row notes-row">
                        <span className="label">Заметки:</span>
                        <span className="value">{session.notes}</span>
                    </div>
                )}

                <div className="info-row date-row">
                    <span className="label">Дата создания:</span>
                    <span className="value">{formatDate(session.created_at)}</span>
                </div>
            </div>
        </div>
    )
}
