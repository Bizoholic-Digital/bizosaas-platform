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
      const response = await apiService.login({ email, password });
      
      if (response.success && response.data?.user) {
        setUser(response.data.user);
        // Store token for persistence
        if (typeof window !== "undefined") {
          localStorage.setItem("auth_token", response.data.token || "demo_token");
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
      sessionStorage.removeItem("auth_token");
    }
    router.push("/login");
  };

  const checkAuth = async (): Promise<boolean> => {
    try {
      // Check for stored token
      if (typeof window !== "undefined") {
        const token = localStorage.getItem("auth_token");
        if (token) {
          try {
            // Try to decode token first
            const tokenData = JSON.parse(Buffer.from(token, "base64").toString());
            if (tokenData.exp > Date.now()) {
              // Token is valid, set user from token data
              setUser({
                id: tokenData.user_id || "demo",
                email: tokenData.email || "demo@bizosaas.com",
                name: "Demo User", // Default for demo
                role: "admin",
                tenant: tokenData.tenant_id || "demo"
              });
              return true;
            }
          } catch (e) {
            // Fallback for simple demo token
            if (token === "demo_token") {
              setUser({
                id: "demo",
                email: "demo@bizosaas.com",
                name: "Demo User",
                role: "admin",
                tenant: "demo"
              });
              return true;
            }
          }
        }
      }
      return false;
    } catch (error) {
      console.error("Auth check error:", error);
      return false;
    }
  };

  // Only check auth on initial mount
  // Simple redirect logic - no loops
  useEffect(() => {
    // Only run on client side to prevent hydration issues
    if (typeof window === "undefined") return;
    
    if (!isLoading) {
      // Only redirect if we have auth state and its not login page
      if (!user && pathname !== "/login" && pathname !== "/") {
        router.push("/login");
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
