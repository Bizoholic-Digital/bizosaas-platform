'use client'

import React, { useState, useEffect, useContext, createContext, useCallback } from 'react'
import authClient, { AuthUser, LoginCredentials } from '@/lib/auth-client'

interface AuthContextValue {
  user: AuthUser | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (credentials: LoginCredentials) => Promise<void>
  logout: () => Promise<void>
  refresh: () => Promise<void>
  hasRole: (role: string) => boolean
  hasServiceAccess: (serviceName: string) => boolean
  checkServiceAccess: (serviceName: string) => Promise<boolean>
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const refresh = useCallback(async () => {
    try {
      const currentUser = await authClient.getCurrentUser()
      setUser(currentUser)
    } catch (error) {
      console.error('Failed to refresh user:', error)
      setUser(null)
    }
  }, [])

  const login = useCallback(async (credentials: LoginCredentials) => {
    setIsLoading(true)
    try {
      const user = await authClient.login(credentials)
      setUser(user)
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }, [])

  const logout = useCallback(async () => {
    setIsLoading(true)
    try {
      await authClient.logout()
      setUser(null)
    } catch (error) {
      console.error('Logout failed:', error)
    } finally {
      setIsLoading(false)
    }
  }, [])

  const hasRole = useCallback((role: string) => {
    return authClient.hasRole(role)
  }, [])

  const hasServiceAccess = useCallback((serviceName: string) => {
    return authClient.hasServiceAccess(serviceName)
  }, [])

  const checkServiceAccess = useCallback(async (serviceName: string) => {
    return authClient.checkServiceAccess(serviceName)
  }, [])

  useEffect(() => {
    const initAuth = async () => {
      setIsLoading(true)
      try {
        if (authClient.isAuthenticated()) {
          const currentUser = await authClient.getCurrentUser()
          setUser(currentUser)
        }
      } catch (error) {
        console.error('Auth initialization failed:', error)
      } finally {
        setIsLoading(false)
      }
    }

    initAuth()
  }, [])

  const value: AuthContextValue = {
    user,
    isLoading,
    isAuthenticated: !!user && authClient.isAuthenticated(),
    login,
    logout,
    refresh,
    hasRole,
    hasServiceAccess,
    checkServiceAccess,
  }

  return React.createElement(AuthContext.Provider, { value }, children)
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export function useRequireAuth(redirectTo: string = '/auth/login') {
  const { isAuthenticated, isLoading } = useAuth()
  
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      window.location.href = redirectTo
    }
  }, [isAuthenticated, isLoading, redirectTo])

  return { isAuthenticated, isLoading }
}

export function useRequireRole(requiredRole: string, redirectTo: string = '/unauthorized') {
  const { user, hasRole, isLoading } = useAuth()
  
  useEffect(() => {
    if (!isLoading && user && !hasRole(requiredRole)) {
      window.location.href = redirectTo
    }
  }, [user, hasRole, requiredRole, isLoading, redirectTo])

  return { hasAccess: hasRole(requiredRole), isLoading }
}

export function useServiceAccess(serviceName: string) {
  const { hasServiceAccess, checkServiceAccess } = useAuth()
  const [isLoading, setIsLoading] = useState(false)
  const [hasAccess, setHasAccess] = useState(hasServiceAccess(serviceName))

  useEffect(() => {
    const verifyAccess = async () => {
      setIsLoading(true)
      try {
        const access = await checkServiceAccess(serviceName)
        setHasAccess(access)
      } catch (error) {
        console.error(`Failed to check access for ${serviceName}:`, error)
        setHasAccess(false)
      } finally {
        setIsLoading(false)
      }
    }

    verifyAccess()
  }, [serviceName, checkServiceAccess])

  return { hasAccess, isLoading }
}