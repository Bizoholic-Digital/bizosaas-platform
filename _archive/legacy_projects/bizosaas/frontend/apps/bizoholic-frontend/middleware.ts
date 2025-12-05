import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Routes that don't require authentication
const publicRoutes = [
  '/',
  '/about',
  '/services',
  '/pricing',
  '/contact',
  '/blog',
  '/portfolio',
  '/login',
  '/register',
  '/portal/login',
  '/portal/register',
]

// Check if a path matches any public route
function isPublicRoute(pathname: string): boolean {
  return publicRoutes.some(route => {
    if (route === pathname) return true
    // Allow dynamic routes like /blog/[slug]
    if (pathname.startsWith(route + '/')) return true
    return false
  })
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Allow public routes
  if (isPublicRoute(pathname)) {
    return NextResponse.next()
  }

  // Allow API routes
  if (pathname.startsWith('/api/')) {
    return NextResponse.next()
  }

  // Allow static files
  if (
    pathname.startsWith('/_next/') ||
    pathname.startsWith('/static/') ||
    pathname.includes('.') // files with extensions
  ) {
    return NextResponse.next()
  }

  // Check for authentication token
  const token = request.cookies.get('access_token')

  // Protect portal routes
  if (pathname.startsWith('/portal') && !pathname.startsWith('/portal/login')) {
    if (!token) {
      // Redirect to login with return URL
      const url = request.nextUrl.clone()
      url.pathname = '/portal/login'
      url.searchParams.set('redirect', pathname)
      return NextResponse.redirect(url)
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files (images, etc.)
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico)$).*)',
  ],
}
