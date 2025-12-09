'use client'

// Auth Context for managing authentication state across the application
// Integrates with BizOSaaS centralized auth system

import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { useRouter } from 'next/navigation'
import { authClient, type LoginCredentials, type SignupData, type Tenant } from './auth-client'
import type { User } from './types'

interface AuthContextType {
  user: User | null
  loading: boolean
  isAuthenticated: boolean
  hasRole: (role: string) => boolean
  hasServiceAccess: (service: string) => boolean
  login: (credentials: LoginCredentials) => Promise<void>
  signup: (data: SignupData) => Promise<void>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
  tenants: Tenant[]
  currentTenant: Tenant | null
  switchTenant: (tenantId: string) => Promise<void>
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [tenants, setTenants] = useState<Tenant[]>([])
  const router = useRouter()

  // Check authentication status on mount
  useEffect(() => {
    checkAuth()
  }, [])

  // Load tenants when user is authenticated
  useEffect(() => {
    if (user) {
      loadTenants()
    }
  }, [user])

  const checkAuth = async () => {
    try {
      const response = await authClient.getCurrentUser()
      setUser(response?.user || null)
    } catch (error) {
      console.error('Auth check failed:', error)
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  const loadTenants = async () => {
    try {
      const response = await authClient.getTenants()
      const userTenants = Array.isArray(response) ? response : []
      setTenants(userTenants)
    } catch (error) {
      console.error('Failed to load tenants:', error)
    }
  }

  const login = async (credentials: LoginCredentials) => {
    try {
      setLoading(true)
      const response = await authClient.login(credentials)
      setUser(response.user)
      // Redirect to dashboard after successful login
      router.push('/dashboard')
    } catch (error) {
      setUser(null)
      throw error // Re-throw so login form can show error
    } finally {
      setLoading(false)
    }
  }

  const signup = async (data: SignupData) => {
    try {
      setLoading(true)
      const response = await authClient.signup(data)
      setUser(response.user)
      // Redirect to dashboard after successful signup
      router.push('/dashboard')
    } catch (error) {
      setUser(null)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const logout = async () => {
    try {
      await authClient.logout()
      setUser(null)
      setTenants([])
      // Redirect to home page after logout
      router.push('/')
    } catch (error) {
      console.error('Logout error:', error)
      // Clear state even if logout request fails
      setUser(null)
      setTenants([])
      router.push('/')
    }
  }

  const refreshUser = async () => {
    try {
      const response = await authClient.getCurrentUser()
      setUser(response?.user || null)
    } catch (error) {
      console.error('Failed to refresh user:', error)
      setUser(null)
    }
  }

  const switchTenant = async (tenantId: string) => {
    try {
      const response = await authClient.switchTenant(tenantId)
      setUser(response.user)
      await loadTenants()
      // Reload page to refresh tenant-specific data
      window.location.reload()
    } catch (error) {
      console.error('Failed to switch tenant:', error)
      throw error
    }
  }

  // Role-based access control helpers
  const hasRole = (requiredRole: string): boolean => {
    if (!user) return false

    const roleHierarchy = {
      'super_admin': 5,
      'tenant_admin': 4,
      'user': 3,
      'readonly': 2,
      'agent': 1,
    }

    const userRoleLevel = roleHierarchy[user.role as keyof typeof roleHierarchy] || 0
    const requiredRoleLevel = roleHierarchy[requiredRole as keyof typeof roleHierarchy] || 0

    return userRoleLevel >= requiredRoleLevel
  }

  const hasServiceAccess = (service: string): boolean => {
    if (!user) return false
    if (user.role === 'super_admin') return true
    if (!user.allowed_services || user.allowed_services.length === 0) return true
    return user.allowed_services.includes(service)
  }

  const currentTenant = (Array.isArray(tenants) ? tenants.find(t => t.id === user?.tenant_id) : null) || null

  const value: AuthContextType = {
    user,
    loading,
    isAuthenticated: !!user,
    hasRole,
    hasServiceAccess,
    login,
    signup,
    logout,
    refreshUser,
    tenants,
    currentTenant,
    switchTenant,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// Custom hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
