'use client'

/**
 * Simple Authentication Provider for BizOSaaS Platform
 * Provides authentication context without forcing redirects
 * Allows existing auth flows to work while adding unified features
 */

import React, { createContext, useContext } from 'react'
import { useUnifiedAuth, User, AuthState } from '../hooks/useUnifiedAuth'

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<boolean>
  logout: () => Promise<void>
  refreshToken: () => Promise<boolean>
  verifySession: () => Promise<boolean>
}

const AuthContext = createContext<AuthContextType | null>(null)

interface AuthProviderProps {
  children: React.ReactNode
  platform: string
}

export const AuthProvider: React.FC<AuthProviderProps> = ({
  children,
  platform
}) => {
  const auth = useUnifiedAuth(platform)

  // Provide auth context to children without any redirect logic
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
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export default AuthProvider