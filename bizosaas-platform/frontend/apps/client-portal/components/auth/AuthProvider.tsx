"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import apiService from "../../lib/api";

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
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

export default function AuthProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(() => {
    // Prevent hydration mismatch by starting with false on server
    return typeof window !== "undefined";
  });
  const router = useRouter();
  const pathname = usePathname();

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
      sessionStorage.removeItem("auth_token");
    }
    // Redirect to unified auth instead of local login
    window.location.href = "http://localhost:3010";
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
        if (legacyToken === "demo_token") {
          setUser({
            id: "demo",
            email: "demo@bizosaas.com",
            name: "Demo User",
            role: "user",
            tenant: "demo"
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
      setIsLoading(true);
      await checkAuth();
      setIsLoading(false);
    };

    initializeAuth();
  }, []);

  // Handle authentication redirects
  useEffect(() => {
    if (typeof window === "undefined") return;

    if (!isLoading) {
      // Redirect unauthenticated users to unified auth portal
      if (!user && pathname !== "/login" && pathname !== "/") {
        window.location.href = "http://localhost:3010";
      }
    }
  }, [user, isLoading, pathname]);

  const value: AuthContextType = {
    user,
    isLoading,
    login,
    logout,
    checkAuth,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
