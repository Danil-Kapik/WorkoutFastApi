import { apiCall } from './client'
import type { AuthResponse, User } from '../types'

export const authApi = {
    login: async (username: string, password: string): Promise<AuthResponse> => {
        const formData = new FormData()
        formData.append('username', username)
        formData.append('password', password)

        const apiUrl = (import.meta.env.VITE_API_URL as string) || 'http://localhost:8000'
        const response = await fetch(`${apiUrl}/auth/login`, {
            method: 'POST',
            body: formData,
        })

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}))
            throw new Error(errorData.detail || 'Login failed')
        }

        return response.json()
    },

    register: async (username: string, email: string, password: string): Promise<AuthResponse> => {
        return apiCall('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, email, password }),
        })
    },

    me: async (): Promise<User> => {
        return apiCall('/auth/me')
    },
}
