'use client'

import { useEffect, useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { useAuthStore } from '@/lib/auth-store'
import { Loader2 } from 'lucide-react'

interface RouteGuardProps {
  children: React.ReactNode
  requireAuth?: boolean
  redirectTo?: string
}

const publicRoutes = [
  '/',
  '/auth/login',
  '/auth/register',
  '/auth/forgot-password',
  '/auth/reset-password',
  '/auth/verify-email',
  '/pricing',
  '/about',
  '/contact',
  '/privacy',
  '/terms',
]

export function RouteGuard({ 
  children, 
  requireAuth = true, 
  redirectTo 
}: RouteGuardProps) {
  const router = useRouter()
  const pathname = usePathname()
  const { isAuthenticated, user, token, refreshToken } = useAuthStore()
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const checkAuth = async () => {
      // Check if current route is public
      const isPublicRoute = pathname && (publicRoutes.includes(pathname) || 
                           pathname.startsWith('/auth/'))

      // If explicitly requiring auth
      if (requireAuth) {
        if (!isAuthenticated || !token) {
          router.push(redirectTo || `/auth/login?redirect=${encodeURIComponent(pathname || '/')}`)
          return
        }

        // Try to refresh token to ensure it's still valid (skip for demo tokens)
        if (!token.startsWith('demo-jwt-token-')) {
          try {
            const refreshSuccess = await refreshToken()
            if (!refreshSuccess) {
              router.push(redirectTo || `/auth/login?redirect=${encodeURIComponent(pathname || '/')}`)
              return
            }
          } catch (error) {
            console.error('Auth check failed:', error)
            router.push(redirectTo || `/auth/login?redirect=${encodeURIComponent(pathname || '/')}`)
            return
          }
        }
      } else {
        // If not requiring auth and on public route, just continue
        if (isPublicRoute) {
          setIsLoading(false)
          return
        }

        // If not requiring auth but user is authenticated and should redirect
        if (isAuthenticated && redirectTo) {
          router.push(redirectTo)
          return
        }
      }

      setIsLoading(false)
    }

    checkAuth()
  }, [pathname, isAuthenticated, token, router, refreshToken, requireAuth, redirectTo])

  // Show loading spinner while checking authentication
  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="text-sm text-muted-foreground">Checking authentication...</p>
        </div>
      </div>
    )
  }

  // Render children
  return <>{children}</>
}
