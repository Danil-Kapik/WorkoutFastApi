import { useAuth } from '../auth/AuthContext'
import './Navigation.css'

interface NavigationProps {
    onNavigate: (page: string) => void
    currentPage: string
}

export function Navigation({ onNavigate, currentPage }: NavigationProps) {
    const { user, logout } = useAuth()

    if (!user) {
        return (
            <nav className="navigation">
                <div className="nav-brand">Workout Tracker</div>
                <div className="nav-links">
                    <button
                        className={`nav-button ${currentPage === 'login' ? 'active' : ''}`}
                        onClick={() => onNavigate('login')}
                    >
                        Вход
                    </button>
                    <button
                        className={`nav-button ${currentPage === 'register' ? 'active' : ''}`}
                        onClick={() => onNavigate('register')}
                    >
                        Регистрация
                    </button>
                </div>
            </nav>
        )
    }

    return (
        <nav className="navigation">
            <div className="nav-brand">Workout Tracker</div>
            <div className="nav-user">
                <span className="user-name">Привет, {user.username}!</span>
            </div>
            <div className="nav-links">
                <button
                    className={`nav-button ${currentPage === 'dashboard' ? 'active' : ''}`}
                    onClick={() => onNavigate('dashboard')}
                >
                    Прогресс
                </button>
                <button
                    className={`nav-button ${currentPage === 'sessions' ? 'active' : ''}`}
                    onClick={() => onNavigate('sessions')}
                >
                    Тренировки
                </button>
                <button className="nav-button logout-button" onClick={logout}>
                    Выход
                </button>
            </div>
        </nav>
    )
}
