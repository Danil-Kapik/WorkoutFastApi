import { useState } from 'react'
import { useAuth } from './auth/AuthContext'
import { RequireAuth } from './auth/RequireAuth'
import { Navigation } from './components/Navigation'
import { Login } from './pages/Login'
import { Register } from './pages/Register'
import { Dashboard } from './pages/Dashboard'
import { Sessions } from './pages/Sessions'

type Page = 'login' | 'register' | 'dashboard' | 'sessions'

function App() {
    const [currentPage, setCurrentPage] = useState<Page>('login')
    const { user, initialized } = useAuth()

    if (!initialized) {
        return <div className="app-loading">Загрузка приложения...</div>
    }

    const handleNavigate = (page: string) => {
        setCurrentPage(page as Page)
    }

    const renderPage = () => {
        if (!user) {
            // Auth pages
            if (currentPage === 'register') {
                return <Register onSwitchToLogin={() => setCurrentPage('login')} />
            }
            return <Login onSwitchToRegister={() => setCurrentPage('register')} />
        }

        // Protected pages
        return (
            <RequireAuth>
                {currentPage === 'sessions' && <Sessions />}
                {currentPage === 'dashboard' && <Dashboard />}
                {!['sessions', 'dashboard'].includes(currentPage) && <Dashboard />}
            </RequireAuth>
        )
    }

    return (
        <div className="app">
            <Navigation onNavigate={handleNavigate} currentPage={currentPage} />
            <main className="app-main">{renderPage()}</main>
        </div>
    )
}

export default App
