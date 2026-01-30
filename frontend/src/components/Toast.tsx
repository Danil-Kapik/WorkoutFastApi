import React, { useEffect } from 'react'
import './Toast.css'

export type ToastType = 'info' | 'error'

interface ToastProps {
    message: string
    type?: ToastType
    duration?: number
    onClose?: () => void
}

export const Toast: React.FC<ToastProps> = ({ message, type = 'info', duration = 3000, onClose }) => {
    useEffect(() => {
        const t = setTimeout(() => {
            onClose && onClose()
        }, duration)
        return () => clearTimeout(t)
    }, [duration, onClose])

    return (
        <div className={`toast ${type}`} role="status" aria-live="polite">
            {message}
        </div>
    )
}

export default Toast
