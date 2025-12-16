'use client';

import { SessionProvider, Session } from 'next-auth/react';
import { ThemeProvider } from '@/components/theme-provider';
import { Toaster } from 'sonner';

import { GraphQLProvider } from '@/components/providers/GraphQLProvider';
import { MobileSidebarProvider } from '@/components/MobileSidebarContext';
import AuthProvider from '@/components/auth/AuthProvider';

export function Providers({ children, session }: { children: React.ReactNode; session?: Session | null }) {
    return (
        <SessionProvider session={session}>
            <AuthProvider>
                <GraphQLProvider>
                    <ThemeProvider
                        attribute="class"
                        defaultTheme="system"
                        enableSystem
                        disableTransitionOnChange
                    >
                        <MobileSidebarProvider>
                            {children}
                            <Toaster />
                        </MobileSidebarProvider>
                    </ThemeProvider>
                </GraphQLProvider>
            </AuthProvider>
        </SessionProvider>
    );
}
