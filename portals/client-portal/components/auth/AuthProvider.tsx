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
    console.log('[AUTH] Session sync effect triggered:', { status, hasSession: !!session, sessionUser: session?.user?.email });

    if (status === "loading") {
      console.log('[AUTH] Status is loading, waiting...');
      setIsLoading(true);
      return;
    }

    if (session?.user) {
      console.log('[AUTH] Session found, setting user data:', session.user.email);
      const userData: User = {
        id: session.user.id,
        email: session.user.email,
        name: session.user.name || session.user.email?.split('@')[0] || 'User',
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
      console.log('[AUTH] No session found, clearing user data. Status:', status);
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

    if (typeof window !== "undefined") {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user_data");
    }

    // Federated Logout: Redirect to Authentik to clear the provider session
    const authentikUrl = process.env.NEXT_PUBLIC_SSO_URL || 'https://sso.bizoholic.net';
    const returnUrl = encodeURIComponent(window.location.origin + '/login');
    const authentikLogoutUrl = `${authentikUrl}/if/session/end/?return_to=${returnUrl}`;

    signOut({ redirect: false }).then(() => {
      window.location.href = authentikLogoutUrl;
    });
  };

  const checkAuth = async (): Promise<boolean> => {
    // NextAuth handles this automatically via session
    return !!session?.user;
  };

  // Redirect logic - TEMPORARILY DISABLED FOR DEBUGGING
  useEffect(() => {
    if (status === "loading") return;

    // Only redirect if we're CERTAIN the user is unauthenticated
    // Don't redirect during intermediate states
    console.log('[AUTH] Redirect check:', { status, pathname, shouldRedirect: status === "unauthenticated" && !pathname?.includes("/login") });

    // TEMPORARILY COMMENTED OUT TO DEBUG
    // if (status === "unauthenticated" && !pathname?.includes("/login")) {
    //   console.log("[AUTH] User is unauthenticated, redirecting to login from:", pathname);
    //   router.push('/login?error=session_expired');
    // }
  }, [status, pathname, router]);

  const value = {
    user,
    isLoading,
    login,
    logout,
    checkAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
