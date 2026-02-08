'use client'

<<<<<<< HEAD:brands/bizoholic/frontend/app/providers.tsx
import { ThemeProvider } from '@/components/theme-provider'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from '@/lib/auth'
import { TenantThemeProvider } from '@/components/tenant-theme-provider'
import { useState } from 'react'
import { SessionProvider } from 'next-auth/react'

import { Client, Provider as UrqlProvider, cacheExchange, fetchExchange } from 'urql'

interface ProvidersProps {
  children: React.ReactNode
}

export function Providers({ children }: ProvidersProps) {
=======
/**
 * Providers for Analytics Dashboard
 * Wraps the app with authentication and React Query providers
 */

import { AuthProvider } from '@/lib/auth'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'

export function Providers({ children }: { children: React.ReactNode }) {
>>>>>>> 689624bdacbb85634f44c01400300bc3ce37e57e:bizosaas/frontend/apps/analytics-dashboard/app/providers.tsx
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

<<<<<<< HEAD:brands/bizoholic/frontend/app/providers.tsx
  const [urqlClient] = useState(
    () =>
      new Client({
        url: process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT || 'https://cms.bizoholic.net/graphql',
        exchanges: [cacheExchange, fetchExchange],
      })
  )

  return (
    <SessionProvider>
      <QueryClientProvider client={queryClient}>
        <UrqlProvider value={urqlClient}>
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
        </UrqlProvider>
      </QueryClientProvider>
    </SessionProvider>
  )
}
=======
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>{children}</AuthProvider>
    </QueryClientProvider>
  )
}
>>>>>>> 689624bdacbb85634f44c01400300bc3ce37e57e:bizosaas/frontend/apps/analytics-dashboard/app/providers.tsx
