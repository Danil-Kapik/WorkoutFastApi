import { useState } from 'react'
import { useAuth } from '../auth/AuthContext'
import './Auth.css'

interface RegisterProps {
    onSwitchToLogin: () => void
}

export function Register({ onSwitchToLogin }: RegisterProps) {
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [passwordConfirm, setPasswordConfirm] = useState('')
    const [error, setError] = useState('')
    const { register, loading } = useAuth()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')

        if (!username || !email || !password || !passwordConfirm) {
            setError('Заполните все поля')
            return
        }

        if (password !== passwordConfirm) {
            setError('Пароли не совпадают')
            return
        }

        if (password.length < 6) {
            setError('Пароль должен содержать минимум 6 символов')
            return
        }

        try {
            await register(username, email, password)
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Ошибка регистрации')
        }
    }

    return (
        <div className="auth-container">
            <div className="auth-form">
                <h1>Регистрация</h1>

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
                            placeholder="Выберите имя пользователя"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            id="email"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            disabled={loading}
                            placeholder="Введите email"
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
                            placeholder="Минимум 6 символов"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="passwordConfirm">Подтвердите пароль</label>
                        <input
                            id="passwordConfirm"
                            type="password"
                            value={passwordConfirm}
                            onChange={(e) => setPasswordConfirm(e.target.value)}
                            disabled={loading}
                            placeholder="Повторите пароль"
                        />
                    </div>

                    <button type="submit" className="submit-button" disabled={loading}>
                        {loading ? 'Загрузка...' : 'Зарегистрироваться'}
                    </button>
                </form>

                <p className="auth-switch">
                    Уже есть аккаунт?{' '}
                    <button type="button" onClick={onSwitchToLogin} className="switch-button">
                        Войдите
                    </button>
                </p>
            </div>
        </div>
    )
}
