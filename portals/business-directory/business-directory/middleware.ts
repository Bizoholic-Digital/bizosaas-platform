import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
    const url = request.nextUrl;
    const hostname = request.headers.get('host') || '';

    // Define allowed domains (including development)
    const rootDomain = process.env.NEXT_PUBLIC_ROOT_DOMAIN || 'bizoholic.net';
    const isDevelopment = process.env.NODE_ENV === 'development';

    // Extract subdomain
    let subdomain = '';
    if (isDevelopment) {
        // In dev, usually localhost:3004. You can use localTest.me or similar for subdomain testing.
        // For now, let's assume no subdomain in dev unless specified via header
        subdomain = request.headers.get('x-subdomain') || '';
    } else {
        const hostParts = hostname.split('.');
        if (hostParts.length >= 3) {
            subdomain = hostParts[0];
        }
    }

    // Case 1: Subdomain routing (e.g., acme-inc.bizoholic.net)
    if (subdomain && subdomain !== 'www' && subdomain !== 'directory') {
        // If the path is already business-related or internal, let it through
        if (
            url.pathname.startsWith('/_next') ||
            url.pathname.startsWith('/api') ||
            url.pathname.startsWith('/public') ||
            url.pathname.startsWith('/favicon.ico') ||
            url.pathname.startsWith('/business/') // Prevent recursive rewrites
        ) {
            return NextResponse.next();
        }

        console.log(`[DIRECTORY-MIDDLEWARE] Subdomain rewrite: ${subdomain} -> /business/${subdomain}${url.pathname}`);
        return NextResponse.rewrite(new URL(`/business/${subdomain}${url.pathname === '/' ? '' : url.pathname}`, request.url));
    }

    // Case 2: Path-based routing on directory subdomain (e.g., directory.bizoholic.net/acme-inc)
    if (subdomain === 'directory') {
        const pathParts = url.pathname.split('/').filter(Boolean);

        // If it's a direct path under directory (e.g. /acme-inc) and NOT a reserved path
        if (pathParts.length > 0 &&
            !['api', '_next', 'public', 'favicon.ico', 'business', 'search', 'categories'].includes(pathParts[0])) {

            const slug = pathParts[0];
            const remainingPath = '/' + pathParts.slice(1).join('/');

            console.log(`[DIRECTORY-MIDDLEWARE] Path-based rewrite: ${slug} -> /business/${slug}${remainingPath === '/' ? '' : remainingPath}`);
            return NextResponse.rewrite(new URL(`/business/${slug}${remainingPath === '/' ? '' : remainingPath}`, request.url));
        }
    }

    return NextResponse.next();
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
