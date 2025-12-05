import { NextRequest, NextResponse } from 'next/server';

// Client site configurations mapping
const CLIENT_SITES = {
  'bizoholic': {
    id: 'bizoholic',
    name: 'Bizoholic Digital',
    template: 'bizoholic_pro',
    primaryColor: '#0ea5e9',
    logo: '/logos/bizoholic-logo.png',
    features: ['ai_agents', 'analytics', 'campaigns', 'crm', 'directory'],
  },
  'coreldove': {
    id: 'coreldove',
    name: 'CoreLDove Commerce',
    template: 'agency_essentials',
    primaryColor: '#10b981',
    logo: '/logos/coreldove-logo.png',
    features: ['ecommerce', 'ai_agents', 'analytics', 'campaigns'],
  },
  'thrillring': {
    id: 'thrillring',
    name: 'Thrillring Events',
    template: 'startup_focus',
    primaryColor: '#f59e0b',
    logo: '/logos/thrillring-logo.png',
    features: ['events', 'ai_agents', 'analytics', 'social_media'],
  },
  // Demo/Default configuration for new clients
  'demo': {
    id: 'demo',
    name: 'Demo Client Site',
    template: 'startup_focus',
    primaryColor: '#6366f1',
    logo: '/logos/demo-logo.png',
    features: ['ai_agents', 'analytics'],
  },
};

// Multi-tenant domain routing
export function middleware(request: NextRequest) {
  const { pathname, search } = request.nextUrl;
  const hostname = request.headers.get('host') || '';
  
  // Skip middleware for API routes, static files, and Next.js internals
  if (
    pathname.startsWith('/api/') ||
    pathname.startsWith('/_next/') ||
    pathname.startsWith('/static/') ||
    pathname.includes('.') ||
    pathname === '/favicon.ico'
  ) {
    return NextResponse.next();
  }

  let clientId: string | null = null;
  let routingType: 'subdomain' | 'custom_domain' | 'path_based' = 'subdomain';

  // 1. Custom Domain Detection (highest priority)
  if (hostname === 'bizoholic.com' || hostname === 'www.bizoholic.com') {
    clientId = 'bizoholic';
    routingType = 'custom_domain';
  } else if (hostname === 'coreldove.com' || hostname === 'www.coreldove.com') {
    clientId = 'coreldove';
    routingType = 'custom_domain';
  } else if (hostname === 'thrillring.com' || hostname === 'www.thrillring.com') {
    clientId = 'thrillring';
    routingType = 'custom_domain';
  }
  
  // 2. Subdomain Detection (localhost or development)
  else if (hostname.includes('localhost') || hostname.includes('127.0.0.1')) {
    const subdomain = hostname.split('.')[0];
    if (subdomain && CLIENT_SITES[subdomain as keyof typeof CLIENT_SITES]) {
      clientId = subdomain;
      routingType = 'subdomain';
    }
  }
  
  // 3. Path-based Detection (fallback)
  else if (pathname.startsWith('/client/')) {
    const pathParts = pathname.split('/');
    const potentialClientId = pathParts[2];
    if (potentialClientId && CLIENT_SITES[potentialClientId as keyof typeof CLIENT_SITES]) {
      clientId = potentialClientId;
      routingType = 'path_based';
    }
  }

  // Default to demo if no client detected
  if (!clientId) {
    clientId = 'demo';
  }

  const clientConfig = CLIENT_SITES[clientId as keyof typeof CLIENT_SITES];
  
  if (!clientConfig) {
    // Redirect to main platform or error page
    return NextResponse.redirect(new URL('/error/not-found', request.url));
  }

  // Create response with client context
  const response = NextResponse.next();
  
  // Set client context headers for the application
  response.headers.set('x-client-id', clientConfig.id);
  response.headers.set('x-client-name', clientConfig.name);
  response.headers.set('x-client-template', clientConfig.template);
  response.headers.set('x-client-primary-color', clientConfig.primaryColor);
  response.headers.set('x-client-logo', clientConfig.logo);
  response.headers.set('x-client-features', JSON.stringify(clientConfig.features));
  response.headers.set('x-routing-type', routingType);
  
  // For path-based routing, rewrite the URL to remove the client prefix
  if (routingType === 'path_based') {
    const newPathname = pathname.replace(`/client/${clientId}`, '') || '/';
    const url = request.nextUrl.clone();
    url.pathname = newPathname;
    return NextResponse.rewrite(url);
  }
  
  return response;
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
};