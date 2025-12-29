"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useUser, useClerk } from "@clerk/nextjs";

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
  const { user: clerkUser, isLoaded, isSignedIn } = useUser();
  const { signOut, openSignIn } = useClerk();
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  useEffect(() => {
    if (isLoaded && clerkUser) {
      // Map Clerk user to internal User interface
      const primaryEmail = clerkUser.primaryEmailAddress?.emailAddress || "";
      const role = (clerkUser.publicMetadata?.role as string) || "user";
      const tenant = (clerkUser.publicMetadata?.tenant_id as string) || "default";

      const userData: User = {
        id: clerkUser.id,
        email: primaryEmail,
        name: clerkUser.fullName || primaryEmail.split('@')[0],
        role: role,
        tenant: tenant
      };

      setUser(userData);

      // Store token for legacy API calls if needed
      // Clerk handles tokens automatically via middleware, but for client-side fetches:
      // useAuth().getToken() is better, but here we just set user state.
    } else if (isLoaded && !clerkUser) {
      setUser(null);
    }
  }, [isLoaded, clerkUser]);

  const login = async (email: string, password: string): Promise<boolean> => {
    // Redirect to Clerk login
    openSignIn();
    return true;
  };

  const logout = () => {
    signOut(() => router.push("/"));
  };

  const checkAuth = async (): Promise<boolean> => {
    return !!isSignedIn;
  };

  const value = {
    user,
    isLoading: !isLoaded,
    login,
    logout,
    checkAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
