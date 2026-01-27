"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useSession, signIn as nextAuthSignIn, signOut as nextAuthSignOut, SessionProvider } from "next-auth/react";

interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  image?: string;
  tenant?: string;
  onboarded?: boolean;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email?: string, password?: string) => Promise<boolean>;
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
      const u = session.user as any;
      const newUser: User = {
        id: String(u.id || u.sub || ""),
        email: String(u.email || ""),
        name: String(u.name || ""),
        image: typeof u.image === 'string' ? u.image : undefined,
        role: String(u.role || "user"),
        tenant: String(u.tenant_id || "default"),
        onboarded: Boolean(u.onboarded)
      };

      setUser((prev) => {
        if (prev &&
          prev.id === newUser.id &&
          prev.email === newUser.email &&
          prev.onboarded === newUser.onboarded &&
          prev.role === newUser.role) {
          return prev;
        }
        return newUser;
      });
    } else if (status !== "loading") {
      setUser(prev => prev === null ? prev : null);
    }
  }, [session, status]);

  const login = React.useCallback(async (): Promise<boolean> => {
    await nextAuthSignIn("authentik");
    return true;
  }, []);

  const logout = React.useCallback(() => {
    nextAuthSignOut({ callbackUrl: "/" });
  }, []);

  const checkAuth = React.useCallback(async (): Promise<boolean> => !!session, [session]);

  const getToken = React.useCallback(async () => {
    return (session as any)?.access_token as string || null;
  }, [session]);

  const value = React.useMemo(() => ({
    user,
    isLoading: status === "loading",
    login,
    logout,
    checkAuth,
    getToken,
  }), [user, status, login, logout, checkAuth, getToken]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export default function AuthProvider(props: { children: React.ReactNode }) {
  return (
    <SessionProvider>
      <NextAuthProvider {...props} />
    </SessionProvider>
  );
}
