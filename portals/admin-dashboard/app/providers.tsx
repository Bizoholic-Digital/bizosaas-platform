'use client';

import React, { useState } from 'react';
import { ClerkProvider } from '@clerk/nextjs';
import { ThemeProvider } from '@/components/theme-provider';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import AuthProvider from '../shared/components/AuthProvider';

export function Providers({ children }: { children: React.ReactNode }) {
    // Standard Next.js pattern: Create QueryClient inside useState to ensure persistence across renders
    const [queryClient] = useState(() => new QueryClient());
    return (
        <QueryClientProvider client={queryClient}>
            <ClerkProvider>
                <AuthProvider platform="admin">
                    <ThemeProvider
                        attribute="class"
                        defaultTheme="system"
                        enableSystem
                        disableTransitionOnChange
                    >
                        {children}
                    </ThemeProvider>
                </AuthProvider>
            </ClerkProvider>
        </QueryClientProvider>
    );
}
