import { apiCall } from './client'
import type { UserProgress, ProgressResponse } from '../types'

export const progressApi = {
    getAll: async (): Promise<ProgressResponse[]> => {
        return apiCall('/progress')
    },

    // Backend returns a single progress record or null when not found
    getByExercise: async (exerciseType: string): Promise<ProgressResponse | null> => {
        try {
            return await apiCall(
                `/progress/by-exercise?exercise_type=${encodeURIComponent(exerciseType)}`
            )
        } catch (err) {
            // If not found or any error, return null to indicate absence
            return null
        }
    },

    // Accept payload in backend shape
    create: async (data: { exercise_type: string; current_reps_per_set: number }): Promise<ProgressResponse> => {
        return apiCall('/progress', {
            method: 'POST',
            body: JSON.stringify(data),
        })
    },
}
