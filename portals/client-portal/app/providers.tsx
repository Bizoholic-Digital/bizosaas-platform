'use client';

import { SessionProvider } from 'next-auth/react';
import { ThemeProvider } from '@/components/theme-provider';

import { GraphQLProvider } from '@/components/providers/GraphQLProvider';
import { MobileSidebarProvider } from '@/components/MobileSidebarContext';

export function Providers({ children }: { children: React.ReactNode }) {
    return (
        <SessionProvider>
            <GraphQLProvider>
                <ThemeProvider
                    attribute="class"
                    defaultTheme="system"
                    enableSystem
                    disableTransitionOnChange
                >
                    <MobileSidebarProvider>
                        {children}
                    </MobileSidebarProvider>
                </ThemeProvider>
            </GraphQLProvider>
        </SessionProvider>
    );
}
