import { ReactNode } from 'react'
import { useAuth } from './AuthContext'

interface RequireAuthProps {
    children: ReactNode
}

export function RequireAuth({ children }: RequireAuthProps) {
    const { token, initialized } = useAuth()

    if (!initialized) {
        return <div className="loading">Загрузка...</div>
    }

    if (!token) {
        return (
            <div className="unauthorized">
                <p>Требуется авторизация</p>
            </div>
        )
    }

    return <>{children}</>
}
