'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { useRouter, usePathname } from 'next/navigation'

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
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(() => {
    return typeof window !== "undefined"
  })
  const router = useRouter()
  const pathname = usePathname()

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      // Call unified auth service directly
      const response = await fetch('http://localhost:8008/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ email, password })
      });

      if (response.ok) {
        const data = await response.json();

        // Transform API response to our User interface
        const userData: User = {
          id: data.user.id,
          email: data.user.email,
          name: `${data.user.first_name} ${data.user.last_name}`,
          role: data.user.role,
          tenant: data.user.tenant_id || 'default'
        };

        setUser(userData);

        // Store tokens for persistence
        if (typeof window !== "undefined") {
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("refresh_token", data.refresh_token);
          localStorage.setItem("user_data", JSON.stringify(userData));
        }
        return true;
      }
      return false;
    } catch (error) {
      console.error("Login error:", error);
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    if (typeof window !== "undefined") {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user_data");
      // Legacy cleanup
      localStorage.removeItem("auth_token");
    }
    // Federated Logout: Redirect to Authentik
    const authentikUrl = process.env.NEXT_PUBLIC_SSO_URL || 'https://sso.bizoholic.net';
    const returnUrl = encodeURIComponent(window.location.origin + '/login');
    window.location.href = `${authentikUrl}/if/session/end/?return_to=${returnUrl}`;
  };

  const checkAuth = async (): Promise<boolean> => {
    try {
      if (typeof window !== "undefined") {
        // Check for unified auth tokens
        const accessToken = localStorage.getItem("access_token");
        const userData = localStorage.getItem("user_data");

        if (accessToken && userData) {
          try {
            const user = JSON.parse(userData);
            setUser(user);
            return true;
          } catch (e) {
            console.error("Error parsing user data:", e);
          }
        }

        // Fallback to legacy token system for backward compatibility
        const legacyToken = localStorage.getItem("auth_token");
        if (legacyToken === "mock_token") {
          setUser({
            id: "admin",
            email: "admin@bizosaas.com",
            name: "Admin User",
            role: "tenant_admin",
            tenant: "default"
          });
          return true;
        }
      }
      return false;
    } catch (error) {
      console.error("Auth check error:", error);
      return false;
    }
  };

  // Check authentication on initial mount
  useEffect(() => {
    if (typeof window === "undefined") return;

    const initializeAuth = async () => {
      setLoading(true);

      // Handle authentication token from URL (from unified auth redirect)
      const urlParams = new URLSearchParams(window.location.search);
      const token = urlParams.get('token');
      const userData = urlParams.get('user');

      if (token && userData) {
        try {
          // Store the authentication data
          const decodedUser = JSON.parse(decodeURIComponent(userData));
          localStorage.setItem('access_token', token);
          localStorage.setItem('user_data', JSON.stringify(decodedUser));

          // Refresh auth state
          await checkAuth();

          // Clean up URL
          const url = new URL(window.location.href);
          url.searchParams.delete('token');
          url.searchParams.delete('user');
          router.replace(url.pathname + url.search);
        } catch (error) {
          console.error('Error handling auth token:', error);
        }
      } else {
        await checkAuth();
      }

      setLoading(false);
    };

    initializeAuth();
  }, []);

  // Handle authentication redirects
  useEffect(() => {
    if (typeof window === "undefined") return;

    if (!loading) {
      // Only allow admin and super_admin roles
      if (!user && pathname !== "/login") {
        const returnUrl = encodeURIComponent(window.location.pathname + window.location.search);
        window.location.href = `http://localhost:3010?return_url=${returnUrl}`;
      } else if (user && user.role !== 'super_admin' && user.role !== 'tenant_admin') {
        // Redirect non-admin users to client portal
        window.location.href = 'http://localhost:3001';
      }
    }
  }, [user, loading, pathname]);

  const value: AuthContextType = {
    user,
    loading,
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