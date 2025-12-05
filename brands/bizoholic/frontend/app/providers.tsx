'use client'

import { ThemeProvider } from '@/components/theme-provider'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from '@/lib/auth'
import { TenantThemeProvider } from '@/components/tenant-theme-provider'
import { useState } from 'react'
import { SessionProvider } from 'next-auth/react'

interface ProvidersProps {
  children: React.ReactNode
}

export function Providers({ children }: ProvidersProps) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000, // 1 minute
          },
        },
      })
  )

  return (
    <SessionProvider>
      <QueryClientProvider client={queryClient}>
        <TenantThemeProvider defaultTenant="bizosaas">
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem={true}
            disableTransitionOnChange={false}
            storageKey="bizosaas-theme"
          >
            <AuthProvider>
              {children}
            </AuthProvider>
          </ThemeProvider>
        </TenantThemeProvider>
      </QueryClientProvider>
    </SessionProvider>
  )
}