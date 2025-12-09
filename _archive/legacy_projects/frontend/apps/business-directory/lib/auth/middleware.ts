// Middleware for protecting routes and handling authentication
// Works with FastAPI Brain Gateway auth system

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Routes that require authentication
const protectedRoutes = [
  '/dashboard',
  '/dashboard/projects',
  '/dashboard/analytics',
  '/dashboard/reports',
  '/dashboard/billing',
  '/dashboard/support',
  '/dashboard/settings',
  '/dashboard/team',
  '/dashboard/content',
  '/dashboard/campaigns',
]

// Routes that should redirect to dashboard if already authenticated
const authRoutes = ['/login', '/signup']

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Check if accessing a protected route
  const isProtectedRoute = protectedRoutes.some(route =>
    pathname.startsWith(route)
  )

  // Check if accessing an auth page
  const isAuthRoute = authRoutes.some(route =>
    pathname.startsWith(route)
  )

  // Get auth token from cookies (set by Brain Gateway)
  const accessToken = request.cookies.get('access_token')
  const isAuthenticated = !!accessToken

  // Protect dashboard routes
  if (isProtectedRoute && !isAuthenticated) {
    // Not authenticated, redirect to login with return URL
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('from', pathname)
    return NextResponse.redirect(loginUrl)
  }

  // Redirect authenticated users away from auth pages
  if (isAuthRoute && isAuthenticated) {
    // Already logged in, redirect to dashboard
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  // Optional: Verify token with Brain Gateway for extra security
  // Uncomment if you want server-side token validation on every request
  /*
  if (isProtectedRoute && accessToken) {
    try {
      const response = await fetch(`${process.env.BRAIN_API_BASE_URL}/auth/verify`, {
        headers: {
          'Cookie': `access_token=${accessToken.value}`
        }
      })

      if (!response.ok) {
        // Token invalid, redirect to login
        const loginUrl = new URL('/login', request.url)
        loginUrl.searchParams.set('from', pathname)
        const response = NextResponse.redirect(loginUrl)
        // Clear invalid cookie
        response.cookies.delete('access_token')
        return response
      }
    } catch (error) {
      console.error('Token verification failed:', error)
      // On error, let the request through (fail open for now)
      // In production, you might want to redirect to login
    }
  }
  */

  return NextResponse.next()
}

// Configure which routes to run middleware on
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.png$|.*\\.jpg$|.*\\.jpeg$|.*\\.svg$).*)',
  ],
}
