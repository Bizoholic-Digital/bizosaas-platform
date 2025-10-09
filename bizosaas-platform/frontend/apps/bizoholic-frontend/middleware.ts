import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// Domain-based routing strategy:
// - bizoholic.com -> Marketing website (homepage)
// - app.bizoholic.com -> BizOSaaS platform (dashboard)
// - admin.bizoholic.com -> Wagtail CMS admin
// - coreldove.com -> Ecommerce storefront
// - app.coreldove.com -> CoreLDove dashboard
const DOMAIN_ROUTING = {
  // Marketing websites (public content)
  'bizoholic.com': '/',
  'www.bizoholic.com': '/',
  'coreldove.com': '/products',
  'www.coreldove.com': '/products',
  'thrillring.com': '/',
  'www.thrillring.com': '/',
  'quanttrade.com': '/',
  'www.quanttrade.com': '/',
  
  // SaaS platform dashboards (authenticated)
  'app.bizoholic.com': '/dashboard',
  'app.coreldove.com': '/dashboard/coreldove',
  'app.thrillring.com': '/dashboard/thrillring', 
  'app.quanttrade.com': '/dashboard/quanttrade',
  
  // CMS admin interfaces
  'admin.bizoholic.com': '/wagtail-admin',
  'cms.bizoholic.com': '/wagtail-admin',
  
  // Development routing
  'localhost:3000': '/', // Marketing website in dev
  'localhost:3001': '/', // Marketing website in dev (containerized)
  'localhost:8006': '/wagtail-admin' // CMS admin direct access
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const hostname = request.headers.get('host') || request.nextUrl.hostname
  
  // Skip API routes, static files, and Next.js internals
  if (
    pathname.startsWith('/api/') ||
    pathname.startsWith('/_next/') ||
    pathname.startsWith('/favicon.ico') ||
    pathname.includes('.')
  ) {
    return NextResponse.next()
  }
  
  // Handle Wagtail CMS admin routing
  if (pathname.startsWith('/admin')) {
    if (hostname === 'localhost:3000' || hostname === 'localhost:3001' || hostname === 'bizoholic.com' || hostname === 'www.bizoholic.com') {
      // Redirect /admin to Wagtail CMS (port 8006)
      return NextResponse.redirect(new URL('http://localhost:8006/admin/'))
    }
  }
  
  // Handle SaaS platform routing
  if (pathname.startsWith('/auth/login')) {
    const redirectParam = request.nextUrl.searchParams.get('redirect')
    const isAppDomain = hostname.startsWith('app.')
    
    if (!redirectParam && isAppDomain) {
      // Add platform redirect parameter for app domains
      const url = new URL(request.url)
      url.searchParams.set('redirect', 'bizosaas')
      return NextResponse.redirect(url)
    }
  }
  
  // Handle storefront - let it pass through to the actual storefront page

  // Domain-based routing for root paths
  const domainRoute = DOMAIN_ROUTING[hostname as keyof typeof DOMAIN_ROUTING]
  
  if (domainRoute && pathname === '/' && domainRoute !== '/') {
    // Rewrite root to appropriate section based on domain
    const response = NextResponse.rewrite(new URL(domainRoute, request.url))
    response.headers.set('x-tenant-domain', hostname)
    response.headers.set('x-platform-type', getDomainType(hostname))
    return response
  }
  
  // Add headers for API calls and tenant resolution
  const response = NextResponse.next()
  response.headers.set('x-tenant-domain', hostname)
  response.headers.set('x-platform-type', getDomainType(hostname))
  
  return response
}

// Helper function to determine platform type based on domain
function getDomainType(hostname: string): string {
  if (hostname.startsWith('app.')) {
    return 'saas-platform'
  }
  if (hostname.startsWith('admin.') || hostname.startsWith('cms.') || hostname === 'localhost:8006') {
    return 'cms-admin'
  }
  return 'marketing-website'
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}