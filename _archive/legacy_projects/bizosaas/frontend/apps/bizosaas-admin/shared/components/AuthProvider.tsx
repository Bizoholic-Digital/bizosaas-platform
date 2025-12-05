'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'

interface AuthContextType {
  user: any | null
  loading: boolean
  login: (credentials: any) => Promise<void>
  logout: () => void
  platform: string
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: React.ReactNode
  platform: string
}

export default function AuthProvider({ children, platform }: AuthProviderProps) {
  const [user, setUser] = useState<any | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Initialize auth state
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    try {
      // Check for existing auth token
      const token = localStorage.getItem('auth_token')
      if (token) {
        // Validate token and get user info
        // For now, mock user
        setUser({ id: 1, name: 'Admin User', email: 'admin@bizosaas.com' })
      }
    } catch (error) {
      console.error('Auth check failed:', error)
    } finally {
      setLoading(false)
    }
  }

  const login = async (credentials: any) => {
    try {
      setLoading(true)
      // Implement actual login logic here
      const mockUser = { id: 1, name: 'Admin User', email: 'admin@bizosaas.com' }
      setUser(mockUser)
      localStorage.setItem('auth_token', 'mock_token')
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('auth_token')
  }

  const value: AuthContextType = {
    user,
    loading,
    login,
    logout,
    platform
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}