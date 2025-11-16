'use client'

/**
 * AuthProvider for BizOSaaS Admin Dashboard
 * Wraps the centralized auth system with admin-specific configuration
 */

import { AuthProvider as CentralizedAuthProvider } from '@/lib/auth'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'

interface AuthProviderProps {
  children: React.ReactNode
  platform: string
}

export default function AuthProvider({ children, platform }: AuthProviderProps) {
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
    <QueryClientProvider client={queryClient}>
      <CentralizedAuthProvider>
        {children}
      </CentralizedAuthProvider>
    </QueryClientProvider>
  )
}

// Re-export useAuth from centralized auth
export { useAuth } from '@/lib/auth'
