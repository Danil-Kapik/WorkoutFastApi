const API_BASE_URL = (import.meta.env.VITE_API_URL as string) || 'http://localhost:8000'

export async function apiCall<T>(
    endpoint: string,
    options: RequestInit = {}
): Promise<T> {
    const token = localStorage.getItem('access_token')

    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
    }

    if (options.headers instanceof Headers) {
        options.headers.forEach((value, key) => {
            headers[key] = value
        })
    } else if (options.headers && typeof options.headers === 'object') {
        Object.assign(headers, options.headers)
    }

    if (token) {
        headers['Authorization'] = `Bearer ${token}`
    }

    const url = `${API_BASE_URL}${endpoint}`
    const response = await fetch(url, {
        ...options,
        headers,
    })

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `API Error: ${response.status}`)
    }

    return response.json()
}
