import React, { createContext, useState, useCallback, useEffect, ReactNode } from 'react'
import { User } from '../types/api'
import { authApi } from '../api/auth'

interface AuthContextType {
    user: User | null
    token: string | null
    loading: boolean
    login: (username: string, password: string) => Promise<void>
    register: (username: string, email: string, password: string) => Promise<void>
    logout: () => void
    initialized: boolean
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null)
    const [token, setToken] = useState<string | null>(null)
    const [loading, setLoading] = useState(false)
    const [initialized, setInitialized] = useState(false)

    // Load user on mount
    useEffect(() => {
        const loadUser = async () => {
            const savedToken = localStorage.getItem('access_token')
            if (savedToken) {
                setToken(savedToken)
                try {
                    const userData = await authApi.me()
                    setUser(userData)
                } catch (error) {
                    localStorage.removeItem('access_token')
                    setToken(null)
                }
            }
            setInitialized(true)
        }

        loadUser()
    }, [])

    const login = useCallback(async (username: string, password: string) => {
        setLoading(true)
        try {
            const response = await authApi.login(username, password)
            localStorage.setItem('access_token', response.access_token)
            setToken(response.access_token)

            const userData = await authApi.me()
            setUser(userData)
        } finally {
            setLoading(false)
        }
    }, [])

    const register = useCallback(async (username: string, email: string, password: string) => {
        setLoading(true)
        try {
            const response = await authApi.register(username, email, password)
            localStorage.setItem('access_token', response.access_token)
            setToken(response.access_token)

            const userData = await authApi.me()
            setUser(userData)
        } finally {
            setLoading(false)
        }
    }, [])

    const logout = useCallback(() => {
        localStorage.removeItem('access_token')
        setToken(null)
        setUser(null)
    }, [])

    return (
        <AuthContext.Provider value={{ user, token, loading, login, register, logout, initialized }}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const context = React.useContext(AuthContext)
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider')
    }
    return context
}
