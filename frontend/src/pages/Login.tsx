import { useState } from 'react'
import { useAuth } from '../auth/AuthContext'
import './Auth.css'

interface LoginProps {
    onSwitchToRegister: () => void
}

export function Login({ onSwitchToRegister }: LoginProps) {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const { login, loading } = useAuth()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')

        if (!username || !password) {
            setError('Заполните все поля')
            return
        }

        try {
            await login(username, password)
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Ошибка входа')
        }
    }

    return (
        <div className="auth-container">
            <div className="auth-form">
                <h1>Вход</h1>

                {error && <div className="error-message">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="username">Имя пользователя</label>
                        <input
                            id="username"
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            disabled={loading}
                            placeholder="Введите имя пользователя"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Пароль</label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            disabled={loading}
                            placeholder="Введите пароль"
                        />
                    </div>

                    <button type="submit" className="submit-button" disabled={loading}>
                        {loading ? 'Загрузка...' : 'Войти'}
                    </button>
                </form>

                <p className="auth-switch">
                    Нет аккаунта?{' '}
                    <button type="button" onClick={onSwitchToRegister} className="switch-button">
                        Зарегистрируйтесь
                    </button>
                </p>
            </div>
        </div>
    )
}
