'use client';

import { ThemeProvider } from '@/components/theme-provider';
import { Toaster } from 'sonner';

import { GraphQLProvider } from '@/components/providers/GraphQLProvider';
import { MobileSidebarProvider } from '@/components/MobileSidebarContext';
import AuthProvider from '@/components/auth/AuthProvider';
import { BrandingProvider } from '@/components/providers/BrandingProvider';

export function Providers({ children }: { children: React.ReactNode }) {
    return (
        <BrandingProvider>
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
        </BrandingProvider>
    );
}
