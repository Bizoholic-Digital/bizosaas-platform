'use client'

/**
 * Unified Authentication Wrapper Component
 * Provides authentication context and routing for all BizOSaaS platforms
 * 
 * Features:
 * - Cross-platform session management
 * - Role-based access control  
 * - Automatic redirects based on authentication state
 * - Loading states and error handling
 */

import React, { createContext, useContext, useEffect } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { useUnifiedAuth, User, AuthState } from '../hooks/useUnifiedAuth'

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<boolean>
  logout: () => Promise<void>
  refreshToken: () => Promise<boolean>
  verifySession: () => Promise<boolean>
}

const AuthContext = createContext<AuthContextType | null>(null)

interface AuthWrapperProps {
  children: React.ReactNode
  platform: string
  requireAuth?: boolean
  allowedRoles?: string[]
  redirectTo?: string
}

export const AuthWrapper: React.FC<AuthWrapperProps> = ({
  children,
  platform,
  requireAuth = true,
  allowedRoles,
  redirectTo = '/auth/login'
}) => {
  const auth = useUnifiedAuth(platform)
  const router = useRouter()
  const pathname = usePathname()

  // Check if current route requires authentication
  const isAuthRoute = pathname?.startsWith('/auth/')
  const isPublicRoute = pathname === '/' || pathname?.startsWith('/public/')

  useEffect(() => {
    if (auth.isLoading) return

    // If authentication is required and user is not authenticated
    if (requireAuth && !auth.isAuthenticated && !isAuthRoute && !isPublicRoute) {
      router.push(redirectTo)
      return
    }

    // If user is authenticated but on auth page, redirect to dashboard
    if (auth.isAuthenticated && isAuthRoute) {
      const dashboardUrl = getDashboardUrl(auth.user, platform)
      router.push(dashboardUrl)
      return
    }

    // Check role-based access
    if (auth.isAuthenticated && allowedRoles && auth.user) {
      const hasValidRole = allowedRoles.includes(auth.user.role)
      if (!hasValidRole) {
        console.error(`Access denied: User role '${auth.user.role}' not in allowed roles:`, allowedRoles)
        router.push('/auth/unauthorized')
        return
      }
    }
  }, [
    auth.isAuthenticated,
    auth.isLoading, 
    auth.user,
    requireAuth,
    allowedRoles,
    isAuthRoute,
    isPublicRoute,
    redirectTo,
    platform,
    router,
    pathname
  ])

  // Show loading state
  if (auth.isLoading) {
    return <LoadingScreen platform={platform} />
  }

  // Show error state
  if (auth.error && !isAuthRoute) {
    return <ErrorScreen error={auth.error} onRetry={auth.verifySession} />
  }

  // Provide auth context to children
  const contextValue: AuthContextType = {
    ...auth,
    login: auth.login,
    logout: auth.logout,
    refreshToken: auth.refreshToken,
    verifySession: auth.verifySession
  }

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  )
}

// Hook to use auth context
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthWrapper')
  }
  return context
}

// Get dashboard URL based on user role and platform
const getDashboardUrl = (user: User | null, platform: string): string => {
  if (!user) return '/auth/login'

  switch (platform) {
    case 'bizosaas-admin':
      return user.role === 'super_admin' ? '/super-admin' : '/admin'
    case 'bizoholic-marketing':
      return '/dashboard'
    case 'coreldove-ecommerce':
      return '/dashboard'
    default:
      return '/dashboard'
  }
}

// Loading Screen Component
const LoadingScreen: React.FC<{ platform: string }> = ({ platform }) => {
  const platformColors = {
    'bizosaas-admin': 'bg-blue-600',
    'bizoholic-marketing': 'bg-teal-600', 
    'coreldove-ecommerce': 'bg-coral-600'
  }

  const bgColor = platformColors[platform as keyof typeof platformColors] || 'bg-gray-600'

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <div className={`inline-block w-8 h-8 border-4 border-gray-200 border-t-current rounded-full animate-spin ${bgColor.replace('bg-', 'text-')}`}></div>
        <p className="mt-4 text-gray-600">Loading BizOSaaS Platform...</p>
        <p className="text-sm text-gray-400 capitalize">{platform.replace('-', ' ')}</p>
      </div>
    </div>
  )
}

// Error Screen Component  
const ErrorScreen: React.FC<{ error: string; onRetry: () => void }> = ({ error, onRetry }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center max-w-md mx-auto p-6">
        <div className="text-red-500 mb-4">
          <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        </div>
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Authentication Error</h2>
        <p className="text-gray-600 mb-6">{error}</p>
        <button
          onClick={onRetry}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Retry
        </button>
      </div>
    </div>
  )
}

export default AuthWrapper