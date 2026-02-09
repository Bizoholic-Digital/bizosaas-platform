'use client';

import { ThemeProvider } from 'next-themes';
import { Toaster } from 'sonner';
import { useEffect } from 'react';
import { HeaderProvider } from '@/lib/contexts/HeaderContext';

import AuthProvider from '@/components/auth/AuthProvider';

function LegacyCleaner() {
    useEffect(() => {
        // Only clear Clerk specific things to avoid conflict with Authentik
        const clerkCookies = [
            '__clerk_db_jwt',
            'clerk-db-jwt',
            'clerk-interstitial-token'
        ];
        clerkCookies.forEach(name => {
            document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
        });

        const staleKeys = ['clerk-cache', '__clerk_client_jwt'];
        staleKeys.forEach(key => {
            localStorage.removeItem(key);
            sessionStorage.removeItem(key);
        });
    }, []);

    return null;
}

export function Providers({ children }: { children: React.ReactNode }) {
    return (
        <AuthProvider>
            <LegacyCleaner />
            <ThemeProvider
                attribute="class"
                defaultTheme="system"
                enableSystem
                disableTransitionOnChange
            >
                <HeaderProvider>
                    {children}
                </HeaderProvider>
                <Toaster />
            </ThemeProvider>
        </AuthProvider>
    );
}
