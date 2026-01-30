import { apiCall } from './client'
import type { SessionResponse, SessionListResponse } from '../types'

export const sessionsApi = {
    start: async (exerciseType: string): Promise<SessionResponse> => {
        return apiCall('/sessions/start', {
            method: 'POST',
            body: JSON.stringify({ exercise_type: exerciseType }),
        })
    },

    finish: async (sessionId: number, reps: number): Promise<SessionResponse> => {
        return apiCall(`/sessions/${sessionId}/finish`, {
            method: 'PATCH',
            body: JSON.stringify({ reps }),
        })
    },

    getList: async (page: number = 1, size: number = 10): Promise<SessionListResponse> => {
        return apiCall(`/sessions?page=${page}&size=${size}`)
    },

    getByExercise: async (
        exerciseType: string,
        page: number = 1,
        size: number = 10
    ): Promise<SessionListResponse> => {
        return apiCall(
            `/sessions/by-exercise?exercise_type=${encodeURIComponent(exerciseType)}&page=${page}&size=${size}`
        )
    },

    getLast: async (exerciseType?: string): Promise<SessionResponse | null> => {
        try {
            const url = exerciseType
                ? `/sessions/last?exercise_type=${encodeURIComponent(exerciseType)}`
                : `/sessions/last`
            return await apiCall(url)
        } catch {
            return null
        }
    },
}
