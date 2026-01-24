"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useSession, signIn as nextAuthSignIn, signOut as nextAuthSignOut, SessionProvider } from "next-auth/react";

interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  tenant?: string;
  onboarded?: boolean;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  checkAuth: () => Promise<boolean>;
  getToken: () => Promise<string | null>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    if (typeof window === 'undefined') {
      return {
        user: null,
        isLoading: true,
        login: async () => false,
        logout: () => { },
        checkAuth: async () => false,
        getToken: async () => null
      };
    }
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

function NextAuthProvider({ children }: { children: React.ReactNode }) {
  const { data: session, status } = useSession();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    if (session?.user) {
      setUser({
        id: (session.user as any).id as string,
        email: session.user.email as string,
        name: session.user.name as string,
        role: (session as any).user.role || "user",
        tenant: (session as any).user.tenant_id || "default",
        onboarded: (session as any).user.onboarded || false
      });
    } else {
      setUser(null);
    }
  }, [session]);

  const login = async (): Promise<boolean> => {
    await nextAuthSignIn("authentik");
    return true;
  };

  const logout = () => {
    nextAuthSignOut({ callbackUrl: "/" });
  };

  const checkAuth = async (): Promise<boolean> => !!session;

  const getToken = async () => {
    return (session as any)?.access_token as string || null;
  }

  const value = {
    user,
    isLoading: status === "loading",
    login,
    logout,
    checkAuth,
    getToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export default function AuthProvider(props: { children: React.ReactNode }) {
  return (
    <SessionProvider>
      <NextAuthProvider {...props} />
    </SessionProvider>
  );
}
