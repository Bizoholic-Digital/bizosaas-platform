"use client"

import { useEffect, useState } from 'react'

interface HydrationSafeProps {
  children: React.ReactNode
  fallback?: React.ReactNode
  className?: string
}

/**
 * HydrationSafe component prevents hydration mismatches by 
 * only rendering children after client-side hydration is complete
 */
export function HydrationSafe({ children, fallback = null, className }: HydrationSafeProps) {
  const [isHydrated, setIsHydrated] = useState(false)

  useEffect(() => {
    setIsHydrated(true)
  }, [])

  if (!isHydrated) {
    return fallback ? <div className={className}>{fallback}</div> : null
  }

  return <div className={className}>{children}</div>
}

/**
 * Hook to safely check if component is hydrated
 * Use this to conditionally render content that might cause hydration issues
 */
export function useIsHydrated() {
  const [isHydrated, setIsHydrated] = useState(false)

  useEffect(() => {
    setIsHydrated(true)
  }, [])

  return isHydrated
}

/**
 * SafeDate component that prevents date hydration mismatches
 * Always shows consistent date format between server and client
 */
interface SafeDateProps {
  date: string | Date
  format?: 'short' | 'medium' | 'long' | 'relative'
  className?: string
}

export function SafeDate({ date, format = 'medium', className }: SafeDateProps) {
  const isHydrated = useIsHydrated()
  
  // Always use the same format on server and initial client render
  const fallbackText = typeof date === 'string' ? date.split('T')[0] : date.toDateString().split(' ').slice(1, 3).join(' ')
  
  if (!isHydrated) {
    return <span className={className}>{fallbackText}</span>
  }

  // After hydration, show the properly formatted date
  const dateObj = typeof date === 'string' ? new Date(date) : date
  
  let formatted = fallbackText
  try {
    switch (format) {
      case 'short':
        formatted = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
        break
      case 'medium':
        formatted = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
        break
      case 'long':
        formatted = dateObj.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
        break
      case 'relative':
        const now = new Date()
        const diff = now.getTime() - dateObj.getTime()
        const minutes = Math.floor(diff / (1000 * 60))
        const hours = Math.floor(diff / (1000 * 60 * 60))
        const days = Math.floor(diff / (1000 * 60 * 60 * 24))
        
        if (minutes < 60) {
          formatted = `${minutes}m ago`
        } else if (hours < 24) {
          formatted = `${hours}h ago`
        } else {
          formatted = `${days}d ago`
        }
        break
      default:
        formatted = dateObj.toLocaleDateString()
    }
  } catch (error) {
    console.warn('Date formatting error:', error)
    formatted = fallbackText
  }
  
  return <span className={className}>{formatted}</span>
}