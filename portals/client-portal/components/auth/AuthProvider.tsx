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
  onboarded?: boolean;
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

function ClerkAuthProvider({ children }: { children: React.ReactNode }) {
  const userHook = useUser();
  const clerkHook = useClerk();

  const clerkUser = userHook?.user;
  const isLoaded = userHook?.isLoaded ?? false;
  const isSignedIn = userHook?.isSignedIn ?? false;
  const signOut = clerkHook?.signOut;
  const openSignIn = clerkHook?.openSignIn;

  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  useEffect(() => {
    if (isLoaded && clerkUser) {
      const primaryEmail = clerkUser.primaryEmailAddress?.emailAddress || "";
      const role = (clerkUser.publicMetadata?.role as string) || "user";
      const tenant = (clerkUser.publicMetadata?.tenant_id as string) || "default";
      const onboarded = (clerkUser.publicMetadata?.onboarded as boolean) || false;

      const userData: User = {
        id: clerkUser.id,
        email: primaryEmail,
        name: clerkUser.fullName || primaryEmail.split('@')[0],
        role: role,
        tenant: tenant,
        onboarded: onboarded
      };

      setUser(userData);
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
      signOut(() => router.push("/"));
    } else {
      router.push("/");
    }
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

function DefaultAuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  const login = async (email: string, password: string): Promise<boolean> => {
    console.warn("Login called but Clerk is not configured.");
    return false;
  };

  const logout = () => {
    router.push("/");
  };

  const checkAuth = async (): Promise<boolean> => false;

  const value = {
    user,
    isLoading: false,
    login,
    logout,
    checkAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export default function AuthProvider(props: { children: React.ReactNode }) {
  const clerkKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

  if (clerkKey) {
    return <ClerkAuthProvider {...props} />;
  }

  return <DefaultAuthProvider {...props} />;
}
