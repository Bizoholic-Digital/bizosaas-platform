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
      // Use FastAPI authentication through Brain API Gateway
      const response = await apiService.login({ email, password });

      if (response.success && response.data?.token && response.data?.user) {
        // Transform API response to our User interface
        const userData: User = {
          id: response.data.user.id,
          email: response.data.user.email,
          name: response.data.user.name,
          role: response.data.user.role,
          tenant: response.data.user.tenant_id || 'default'
        };

        setUser(userData);

        // Store token and user data for persistence
        if (typeof window !== "undefined") {
          localStorage.setItem("auth_token", response.data.token);
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
      localStorage.removeItem("auth_token");
      localStorage.removeItem("user_data");
    }
    // Redirect to login page (basePath /portal is handled automatically)
    if (typeof window !== "undefined") {
      window.location.href = "/portal/login";
    }
  };

  const checkAuth = async (): Promise<boolean> => {
    try {
      if (typeof window !== "undefined") {
        // Check for auth token and user data
        const authToken = localStorage.getItem("auth_token");
        const userData = localStorage.getItem("user_data");

        if (authToken && userData) {
          try {
            const user = JSON.parse(userData);
            setUser(user);
            return true;
          } catch (e) {
            console.error("Error parsing user data:", e);
            // Clear invalid data
            localStorage.removeItem("auth_token");
            localStorage.removeItem("user_data");
          }
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
      // Redirect unauthenticated users to login page
      if (!user && pathname !== "/login" && !pathname.startsWith("/login")) {
        router.push("/login");
      }
      // Redirect authenticated users away from login page
      else if (user && pathname === "/login") {
        router.push("/");
      }
    }
  }, [user, isLoading, pathname, router]);

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
