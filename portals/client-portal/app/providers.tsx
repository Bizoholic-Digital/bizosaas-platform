'use client';

import { ClerkProvider } from '@clerk/nextjs';
import { ThemeProvider } from '@/components/theme-provider';
import { Toaster } from 'sonner';

import { GraphQLProvider } from '@/components/providers/GraphQLProvider';
import { MobileSidebarProvider } from '@/components/MobileSidebarContext';
import AuthProvider from '@/components/auth/AuthProvider';

export function Providers({ children }: { children: React.ReactNode }) {
    const clerkKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

    const content = (
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
    );

    if (!clerkKey) {
        console.warn("⚠️ NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY is missing. Clerk authentication will be disabled.");
        return content;
    }

    return (
        <ClerkProvider publishableKey={clerkKey}>
            {content}
        </ClerkProvider>
    );
}
