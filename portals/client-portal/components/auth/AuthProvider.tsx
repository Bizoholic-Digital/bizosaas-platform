"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useSession, signIn, signOut } from "next-auth/react";

interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  tenant?: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  checkAuth: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    // Return dummy context during build/SSR if provider is missing to prevent build failures
    if (typeof window === 'undefined') {
      return {
        user: null,
        isLoading: true,
        login: async () => false,
        logout: () => { },
        checkAuth: async () => false
      };
    }
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

export default function AuthProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const { data: session, status } = useSession();
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  // Sync NextAuth session with our user state
  useEffect(() => {
    if (status === "loading") {
      setIsLoading(true);
      return;
    }

    if (session?.user) {
      const userData: User = {
        id: session.user.id,
        email: session.user.email,
        name: session.user.name,
        role: session.user.role,
        tenant: session.user.tenant_id
      };
      setUser(userData);

      // Store tokens in localStorage for API calls
      if (typeof window !== "undefined") {
        localStorage.setItem("access_token", session.access_token);
        localStorage.setItem("refresh_token", session.refresh_token);
        localStorage.setItem("user_data", JSON.stringify(userData));
      }
    } else {
      setUser(null);
      if (typeof window !== "undefined") {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user_data");
      }
    }

    setIsLoading(false);
  }, [session, status]);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      console.log('[AUTH] Attempting NextAuth login...');

      const result = await signIn('credentials', {
        email,
        password,
        redirect: false,
      });

      if (result?.error) {
        console.error('[AUTH] Login failed:', result.error);
        return false;
      }

      if (result?.ok) {
        console.log('[AUTH] Login successful');
        return true;
      }

      return false;
    } catch (error) {
      console.error("[AUTH] Login error:", error);
      return false;
    }
  };

  const logout = () => {
    console.log('[AUTH] Logging out...');
    signOut({ callbackUrl: '/login' });

    if (typeof window !== "undefined") {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user_data");
    }
  };

  const checkAuth = async (): Promise<boolean> => {
    // NextAuth handles this automatically via session
    return !!session?.user;
  };

  // Redirect logic
  useEffect(() => {
    if (status === "loading") return;

    if (!session && !pathname?.includes("/login")) {
      console.log("[AUTH] No session found, redirecting to login from:", pathname);
      router.push('/login');
    }
  }, [session, status, pathname, router]);

  const value = {
    user,
    isLoading,
    login,
    logout,
    checkAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
