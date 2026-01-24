'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useSession, signIn as nextAuthSignIn, signOut as nextAuthSignOut, SessionProvider } from "next-auth/react";

interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  tenant?: string;
}

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<boolean>
  logout: () => void
  checkAuth: () => Promise<boolean>
  getToken: () => Promise<string | null>
  platform: string
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: React.ReactNode
  platform: string
}

function NextAuthProvider({ children, platform }: AuthProviderProps) {
  const { data: session, status } = useSession()
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    if (session?.user) {
      setUser({
        id: (session.user as any).id as string,
        email: session.user.email as string,
        name: session.user.name as string,
        role: (session as any).user.role || "user",
        tenant: (session as any).user.tenant_id || "default"
      })
    } else {
      setUser(null)
    }
  }, [session])

  const login = async (): Promise<boolean> => {
    await nextAuthSignIn("authentik")
    return true
  }

  const logout = () => {
    nextAuthSignOut({ callbackUrl: '/login' })
  }

  const checkAuth = async (): Promise<boolean> => !!session

  const getToken = async () => {
    return (session as any)?.access_token as string || null;
  }

  const value: AuthContextType = {
    user,
    loading: status === "loading",
    login,
    logout,
    checkAuth,
    getToken,
    platform
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export default function AuthProvider(props: AuthProviderProps) {
  return (
    <SessionProvider>
      <NextAuthProvider {...props} />
    </SessionProvider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}