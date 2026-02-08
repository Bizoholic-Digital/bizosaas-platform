// Middleware for route protection and authentication
// SECURITY UPDATE: Now checks for refresh_token cookie (HttpOnly)
// Access token stored in memory on client side

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Get basePath from environment (e.g., '/portal')
const basePath = process.env.BASE_PATH || ''

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // SECURITY: Check for refresh_token (HttpOnly cookie) instead of access_token
  // Access tokens are now stored in memory (client-side)
  // Refresh token presence indicates user has valid session
  const refreshToken = request.cookies.get('refresh_token')
  const hasAuth = !!refreshToken

  // Remove basePath from pathname for route matching
  const pathWithoutBase = basePath ? pathname.replace(basePath, '') : pathname

  // Define protected routes (without basePath)
  const isProtectedRoute = pathWithoutBase.startsWith('/dashboard') ||
                          pathWithoutBase.startsWith('/settings') ||
                          pathWithoutBase.startsWith('/billing') ||
                          pathWithoutBase.startsWith('/services') ||
                          pathWithoutBase.startsWith('/support') ||
                          pathWithoutBase.startsWith('/campaigns') ||
                          pathWithoutBase.startsWith('/analytics')

  // Define auth routes (login, signup, etc.) - without basePath
  const isAuthRoute = pathWithoutBase === '/login' ||
                     pathWithoutBase === '/signup' ||
                     pathWithoutBase === '/forgot-password' ||
                     pathWithoutBase === '/reset-password'

  // Redirect unauthenticated users trying to access protected routes
  if (isProtectedRoute && !hasAuth) {
    const loginUrl = new URL(`${basePath}/login`, request.url)
    loginUrl.searchParams.set('from', pathWithoutBase)
    return NextResponse.redirect(loginUrl)
  }

  // Redirect authenticated users away from auth pages
  if (isAuthRoute && hasAuth) {
    return NextResponse.redirect(new URL(`${basePath}/dashboard`, request.url))
  }

  // Add security headers to response
  const response = NextResponse.next()

  // CSRF Protection: Validate Origin and Referer for mutations
  const mutationMethods = ['POST', 'PUT', 'DELETE', 'PATCH']
  if (mutationMethods.includes(request.method)) {
    const origin = request.headers.get('origin')
    const referer = request.headers.get('referer')
    const host = request.headers.get('host')

    // Verify request comes from same origin (basic CSRF protection)
    if (origin && !origin.includes(host || '')) {
      console.warn(`CSRF attempt detected: origin=${origin}, host=${host}`)
      return new NextResponse('CSRF validation failed', { status: 403 })
    }

    if (referer && !referer.includes(host || '')) {
      console.warn(`CSRF attempt detected: referer=${referer}, host=${host}`)
      return new NextResponse('CSRF validation failed', { status: 403 })
    }
  }

  return response
}

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/settings/:path*',
    '/billing/:path*',
    '/services/:path*',
    '/support/:path*',
    '/campaigns/:path*',
    '/analytics/:path*',
    '/login',
    '/signup',
    '/forgot-password',
    '/reset-password'
  ]
}
