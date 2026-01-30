export interface User {
    id: number
    username: string
    email: string
    createdAt?: string
    updatedAt?: string
}

export interface AuthResponse {
    access_token: string
    token_type: string
    user?: User
}

export interface UserProgress {
    id: number
    userId: number
    exerciseType: string
    reps: number
    sets: number
    weight?: number
    difficulty: number
    createdAt: string
    updatedAt: string
}

export interface ProgressResponse {
    id: number
    user_id: number
    exercise_type: string
    current_reps_per_set: number
    difficulty: number | string
    last_success_at: string | null
    created_at: string
    updated_at: string
}

export interface Session {
    id: number
    userId: number
    exerciseType: string
    startedAt: string
    finishedAt?: string
    reps?: number
    difficulty: number
    createdAt: string
    updatedAt: string
}

export interface SessionResponse {
    id: number
    user_id: number
    exercise_type: string
    difficulty: string
    reps_per_set_at_start: number
    completed: boolean
    notes: string | null
    created_at: string
    updated_at: string
}

export interface SessionListResponse {
    items: SessionResponse[]
    total: number
    page: number
    size: number
    pages: number
    has_next: boolean
    has_prev: boolean
}
