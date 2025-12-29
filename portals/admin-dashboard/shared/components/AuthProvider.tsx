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

function ClerkAuthProvider({ children, platform }: AuthProviderProps) {
  const userHook = useUser();
  const clerkHook = useClerk();

  const clerkUser = userHook?.user;
  const isLoaded = userHook?.isLoaded ?? false;
  const signOut = clerkHook?.signOut;
  const openSignIn = clerkHook?.openSignIn;

  const [user, setUser] = useState<User | null>(null)
  const router = useRouter()

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
    if (openSignIn) {
      openSignIn();
      return true;
    }
    return false;
  };

  const logout = () => {
    if (signOut) {
      signOut(() => router.push('/login'));
    } else {
      router.push('/login');
    }
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

function DefaultAuthProvider({ children, platform }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const router = useRouter()

  const login = async (email: string, password: string): Promise<boolean> => {
    console.warn("Login called but Clerk is not configured.");
    return false;
  };

  const logout = () => {
    router.push('/login');
  };

  const checkAuth = async (): Promise<boolean> => false;

  const value: AuthContextType = {
    user,
    loading: false,
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

export default function AuthProvider(props: AuthProviderProps) {
  const clerkKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

  if (clerkKey) {
    return <ClerkAuthProvider {...props} />;
  }

  return <DefaultAuthProvider {...props} />;
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}