'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { useUser, useClerk } from "@clerk/nextjs";

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
  platform: string
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: React.ReactNode
  platform: string
}

export default function AuthProvider({ children, platform }: AuthProviderProps) {
  const { user: clerkUser, isLoaded } = useUser();
  const { signOut, openSignIn } = useClerk();
  const [user, setUser] = useState<User | null>(null)

  const router = useRouter()
  const pathname = usePathname()

  useEffect(() => {
    if (isLoaded && clerkUser) {
      const primaryEmail = clerkUser.primaryEmailAddress?.emailAddress || "";
      const role = (clerkUser.publicMetadata?.role as string) || "user";
      const tenant = (clerkUser.publicMetadata?.tenant_id as string) || "default";

      setUser({
        id: clerkUser.id,
        email: primaryEmail,
        name: clerkUser.fullName || primaryEmail.split('@')[0],
        role: role,
        tenant: tenant
      });
    } else if (isLoaded && !clerkUser) {
      setUser(null);
    }
  }, [isLoaded, clerkUser]);

  const login = async (email: string, password: string): Promise<boolean> => {
    openSignIn();
    return true;
  };

  const logout = () => {
    signOut(() => router.push('/login'));
  };

  const checkAuth = async (): Promise<boolean> => {
    return !!clerkUser;
  };

  const value: AuthContextType = {
    user,
    loading: !isLoaded,
    login,
    logout,
    checkAuth,
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