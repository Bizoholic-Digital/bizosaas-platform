'use client'

/**
 * Unified Authentication Hook for BizOSaaS Platform
 * Provides consistent authentication across all frontend applications
 * 
 * Features:
 * - Cross-platform session management
 * - Role-based access control
 * - FastAPI Brain Gateway integration
 * - Unified Auth Service v2 communication
 */

import { useState, useEffect, useCallback } from 'react'
import { API_CONFIG, AUTH_STORAGE, getApiHeaders } from '../lib/api-config'

export interface User {
  id: string
  email: string
  name: string
  role: 'super_admin' | 'tenant_admin' | 'manager' | 'client'
  tenant_id?: string
  permissions: string[]
  platforms: string[]
}

export interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  token: string | null
}

export const useUnifiedAuth = (platform: string) => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
    token: null
  })

  // Verify session with Unified Auth Service v2
  const verifySession = useCallback(async () => {
    try {
      setAuthState(prev => ({ ...prev, isLoading: true, error: null }))

      const token = localStorage.getItem(AUTH_STORAGE.TOKEN_KEY)
      if (!token) {
        setAuthState(prev => ({
          ...prev,
          isAuthenticated: false,
          isLoading: false,
          user: null,
          token: null
        }))
        return false
      }

      const response = await fetch(`${API_CONFIG.AUTH_API_URL}${API_CONFIG.ENDPOINTS.VERIFY_SESSION}`, {
        method: 'GET',
        headers: {
          ...getApiHeaders(platform),
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const userData = await response.json()

        // Check if user has access to this platform
        const hasAccess = checkPlatformAccess(userData.role, platform)

        if (hasAccess) {
          setAuthState({
            user: userData,
            isAuthenticated: true,
            isLoading: false,
            error: null,
            token
          })

          // Store user data
          localStorage.setItem(AUTH_STORAGE.USER_KEY, JSON.stringify(userData))
          return true
        } else {
          throw new Error('Insufficient permissions for this platform')
        }
      } else {
        throw new Error('Session verification failed')
      }
    } catch (error) {
      // Silently handle auth service unavailability - don't break existing flows
      console.warn('Auth service unavailable, continuing without unified auth:', error)

      setAuthState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null, // Don't show error if auth service is just unavailable
        token: null
      })
      return false
    }
  }, [platform])

  // Login function
  const login = useCallback(async (email: string, password: string) => {
    try {
      setAuthState(prev => ({ ...prev, isLoading: true, error: null }))

      const response = await fetch(`${API_CONFIG.AUTH_API_URL}${API_CONFIG.ENDPOINTS.LOGIN}`, {
        method: 'POST',
        headers: getApiHeaders(platform),
        body: JSON.stringify({
          email,
          password,
          platform,
          grant_type: 'password'
        }),
        redirect: 'manual'
      })

      if (response.ok) {
        const authData = await response.json()

        // Store tokens
        localStorage.setItem(AUTH_STORAGE.TOKEN_KEY, authData.access_token)
        if (authData.refresh_token) {
          localStorage.setItem(AUTH_STORAGE.REFRESH_KEY, authData.refresh_token)
        }

        // Verify and load user data
        await verifySession()
        return true
      } else {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Login failed')
      }
    } catch (error) {
      // Handle auth service unavailability gracefully
      console.warn('Unified auth login failed, falling back to platform auth:', error)
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: null // Don't show error to allow platform-specific auth to work
      }))
      return false
    }
  }, [platform, verifySession])

  // Logout function
  const logout = useCallback(async () => {
    try {
      const token = localStorage.getItem(AUTH_STORAGE.TOKEN_KEY)

      if (token) {
        // Notify server about logout
        await fetch(`${API_CONFIG.AUTH_API_URL}${API_CONFIG.ENDPOINTS.LOGOUT}`, {
          method: 'POST',
          headers: {
            ...getApiHeaders(platform),
            'Authorization': `Bearer ${token}`
          }
        })
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear local data regardless of server response
      clearAuthData()
      setAuthState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
        token: null
      })
    }
  }, [platform])

  // Token refresh
  const refreshToken = useCallback(async () => {
    try {
      const refreshToken = localStorage.getItem(AUTH_STORAGE.REFRESH_KEY)
      if (!refreshToken) {
        throw new Error('No refresh token available')
      }

      const response = await fetch(`${API_CONFIG.AUTH_API_URL}${API_CONFIG.ENDPOINTS.REFRESH_TOKEN}`, {
        method: 'POST',
        headers: getApiHeaders(platform),
        body: JSON.stringify({
          refresh_token: refreshToken,
          grant_type: 'refresh_token'
        })
      })

      if (response.ok) {
        const tokenData = await response.json()
        localStorage.setItem(AUTH_STORAGE.TOKEN_KEY, tokenData.access_token)

        // Update auth state with new token
        setAuthState(prev => ({
          ...prev,
          token: tokenData.access_token
        }))

        return true
      } else {
        throw new Error('Token refresh failed')
      }
    } catch (error) {
      console.error('Token refresh error:', error)
      logout()
      return false
    }
  }, [platform, logout])

  // Platform access control
  const checkPlatformAccess = (role: string, platform: string): boolean => {
    const platformPermissions = {
      'super_admin': ['bizosaas-admin', 'bizoholic-marketing', 'coreldove-ecommerce'],
      'tenant_admin': ['bizosaas-admin', 'bizoholic-marketing', 'coreldove-ecommerce'],
      'manager': ['bizoholic-marketing', 'coreldove-ecommerce'],
      'client': []
    }

    return platformPermissions[role as keyof typeof platformPermissions]?.includes(platform) || false
  }

  // Clear authentication data
  const clearAuthData = () => {
    localStorage.removeItem(AUTH_STORAGE.TOKEN_KEY)
    localStorage.removeItem(AUTH_STORAGE.REFRESH_KEY)
    localStorage.removeItem(AUTH_STORAGE.USER_KEY)
  }

  // Initialize authentication on mount
  useEffect(() => {
    verifySession()
  }, [verifySession])

  // Auto-refresh token before expiration
  useEffect(() => {
    if (authState.isAuthenticated && authState.token) {
      // Set up token refresh interval (e.g., every 45 minutes for 1-hour tokens)
      const refreshInterval = setInterval(() => {
        refreshToken()
      }, 45 * 60 * 1000) // 45 minutes

      return () => clearInterval(refreshInterval)
    }
  }, [authState.isAuthenticated, authState.token, refreshToken])

  return {
    ...authState,
    login,
    logout,
    refreshToken,
    verifySession,
    clearAuthData
  }
}