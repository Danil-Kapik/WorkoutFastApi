import { apiCall } from './client'
import type { UserProgress, ProgressResponse } from '../types'

export const progressApi = {
    getAll: async (): Promise<ProgressResponse[]> => {
        return apiCall('/progress')
    },

    getByExercise: async (exerciseType: string): Promise<ProgressResponse[]> => {
        return apiCall(`/progress/by-exercise?exercise_type=${encodeURIComponent(exerciseType)}`)
    },

    create: async (data: Omit<UserProgress, 'id' | 'createdAt' | 'updatedAt'>): Promise<ProgressResponse> => {
        return apiCall('/progress', {
            method: 'POST',
            body: JSON.stringify(data),
        })
    },
}
