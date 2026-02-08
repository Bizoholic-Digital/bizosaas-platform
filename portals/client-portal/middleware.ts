import { auth } from "@/lib/auth"
import { NextResponse } from "next/server"

export default auth((req) => {
    // req.auth is populated by the auth wrapper
    const isLoggedIn = !!req.auth;
    const { pathname } = req.nextUrl;
    const hostname = req.headers.get('host') || req.nextUrl.hostname;

    // Handle CMS domain redirect
    if (hostname === 'cms.bizoholic.com' && pathname === '/') {
        return NextResponse.redirect(new URL('/dashboard/cms', req.url));
    }

    const isProtected = pathname.startsWith('/dashboard') || pathname.startsWith('/onboarding');
    const isAuthPage = pathname.startsWith('/login') || pathname.startsWith('/register');

    if (isAuthPage) {
        if (isLoggedIn) {
            const onboarded = (req.auth?.user as any)?.onboarded;
            return NextResponse.redirect(new URL(onboarded ? '/dashboard' : '/onboarding', req.url));
        }
        return NextResponse.next();
    }

    if (isProtected) {
        if (!isLoggedIn) {
            const from = pathname + req.nextUrl.search;
            return NextResponse.redirect(new URL(`/login?from=${encodeURIComponent(from)}`, req.url));
        }

        const user = req.auth?.user as any;
        const onboarded = user?.onboarded;

        // Redirect to onboarding if not done
        if (pathname.startsWith('/dashboard') && !onboarded) {
            return NextResponse.redirect(new URL('/onboarding', req.url));
        }

        // Feature-gate protection
        const planFeatures = user?.plan_features || [];

        // Simple mapping for routes to feature slugs
        const featureRoutes: Record<string, string> = {
            '/dashboard/crm': 'crm',
            '/dashboard/cms': 'cms',
            '/dashboard/ecommerce': 'ecommerce',
            '/dashboard/marketing': 'marketing',
            '/dashboard/bi': 'analytics'
        };

        const matchingRoute = Object.keys(featureRoutes).find(route => pathname.startsWith(route));
        if (matchingRoute) {
            const requiredFeature = featureRoutes[matchingRoute];
            if (!planFeatures.includes(requiredFeature)) {
                return NextResponse.redirect(new URL('/dashboard/billing?error=feature_restricted', req.url));
            }
        }

        return NextResponse.next();
    }

    return NextResponse.next();
});

export const config = {
    // Match only the paths we care about to avoid overhead on static assets
    matcher: ['/dashboard/:path*', '/onboarding/:path*', '/login', '/register'],
};
