'use client';

import { ClerkProvider } from '@clerk/nextjs';
import { ThemeProvider } from '@/components/theme-provider';
import { Toaster } from 'sonner';

import { GraphQLProvider } from '@/components/providers/GraphQLProvider';
import { MobileSidebarProvider } from '@/components/MobileSidebarContext';
import AuthProvider from '@/components/auth/AuthProvider';

export function Providers({ children }: { children: React.ReactNode }) {
    return (
        <ClerkProvider>
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
        </ClerkProvider>
    );
}
