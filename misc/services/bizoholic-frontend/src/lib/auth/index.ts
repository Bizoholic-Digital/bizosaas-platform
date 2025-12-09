'use client'

/**
 * Authentication utilities
 * Stub implementation for @bizoholic-digital/auth module
 */

import { useState, useEffect, type ReactNode, type ReactElement } from 'react'

export interface AuthCredentials {
  email: string
  password: string
}

export interface SignupData extends AuthCredentials {
  name: string
  company?: string
}

export interface User {
  id: string
  email: string
  name: string
  company?: string
}

export interface AuthResponse {
  success: boolean
  user?: User
  token?: string
  error?: string
}

/**
 * Login with email and password
 */
export async function login(credentials: AuthCredentials): Promise<AuthResponse> {
  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
    })

    if (!response.ok) {
      return { success: false, error: 'Invalid credentials' }
    }

    const data = await response.json()
    return { success: true, ...data }
  } catch (error) {
    return { success: false, error: 'Login failed' }
  }
}

/**
 * Sign up new user
 */
export async function signup(data: SignupData): Promise<AuthResponse> {
  try {
    const response = await fetch('/api/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })

    if (!response.ok) {
      return { success: false, error: 'Signup failed' }
    }

    const result = await response.json()
    return { success: true, ...result }
  } catch (error) {
    return { success: false, error: 'Signup failed' }
  }
}

/**
 * Request password reset
 */
export async function requestPasswordReset(email: string): Promise<{ success: boolean, error?: string }> {
  try {
    const response = await fetch('/api/auth/forgot-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    })

    return { success: response.ok }
  } catch (error) {
    return { success: false, error: 'Failed to send reset email' }
  }
}

/**
 * Reset password with token
 */
export async function resetPassword(token: string, newPassword: string): Promise<{ success: boolean, error?: string }> {
  try {
    const response = await fetch('/api/auth/reset-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, password: newPassword }),
    })

    return { success: response.ok }
  } catch (error) {
    return { success: false, error: 'Failed to reset password' }
  }
}

/**
 * Confirm password reset (alias for resetPassword)
 */
export async function confirmPasswordReset(token: string, password: string): Promise<{ success: boolean, error?: string }> {
  return await resetPassword(token, password)
}

/**
 * Verify email with token
 */
export async function verifyEmail(token: string): Promise<{ success: boolean, error?: string }> {
  try {
    const response = await fetch('/api/auth/verify-email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token }),
    })

    return { success: response.ok }
  } catch (error) {
    return { success: false, error: 'Failed to verify email' }
  }
}

/**
 * Logout current user
 */
export async function logout(): Promise<void> {
  try {
    await fetch('/api/auth/logout', { method: 'POST' })
  } catch (error) {
    console.error('Logout failed:', error)
  }
}

/**
 * Get current user
 */
export async function getCurrentUser(): Promise<User | null> {
  try {
    const response = await fetch('/api/auth/me')
    if (!response.ok) return null
    return await response.json()
  } catch (error) {
    return null
  }
}

/**
 * Auth client object (for compatibility)
 */
export const authClient = {
  login,
  signup,
  logout,
  requestPasswordReset,
  resetPassword,
  confirmPasswordReset,
  verifyEmail,
  getCurrentUser,
}

/**
 * useAuth hook for React components
 */
export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    getCurrentUser().then((currentUser) => {
      setUser(currentUser)
      setIsLoading(false)
    })
  }, [])

  return {
    user,
    isLoading,
    loading: isLoading, // Alias for compatibility
    isAuthenticated: !!user,
    login: async (credentials: AuthCredentials) => {
      const result = await login(credentials)
      if (result.success && result.user) {
        setUser(result.user)
      }
      return result
    },
    signup: async (data: SignupData) => {
      const result = await signup(data)
      if (result.success && result.user) {
        setUser(result.user)
      }
      return result
    },
    logout: async () => {
      await logout()
      setUser(null)
    },
  }
}

/**
 * Auth Provider component (stub for compatibility)
 */
export function AuthProvider({ children }: { children: ReactNode }) {
  return children as any
}
