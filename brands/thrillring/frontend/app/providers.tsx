'use client'

import { ThemeProvider } from '@/components/theme-provider'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { createClient, Provider as UrqlProvider, cacheExchange, fetchExchange } from 'urql'
import { AuthProvider } from '@/lib/auth'
import { TenantThemeProvider } from '@/components/tenant-theme-provider'
import { useState } from 'react'

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

  const graphqlUrl =
    process.env.NEXT_PUBLIC_GRAPHQL_URL ||
    (process.env.NEXT_PUBLIC_BRAIN_API_URL ? `${process.env.NEXT_PUBLIC_BRAIN_API_URL}/graphql` : null) ||
    (process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL}/graphql` : null) ||
    'http://localhost:8000/graphql';

  const [urqlClient] = useState(() =>
    createClient({
      url: graphqlUrl,
      exchanges: [cacheExchange, fetchExchange],
      suspense: false
    })
  )

  return (
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
  )
}