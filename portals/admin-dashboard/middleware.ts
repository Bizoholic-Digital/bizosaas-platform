import { auth } from "@/lib/auth"
import { NextResponse } from "next/server"

export default auth((req) => {
    const isLoggedIn = !!req.auth
    const { pathname } = req.nextUrl

    // Add paths that require authentication
    const protectedPaths = ['/dashboard', '/tenants', '/settings', '/users', '/admin']
    const isProtected = protectedPaths.some(path => pathname.startsWith(path))

    if (isProtected) {
        if (!isLoggedIn) {
            return NextResponse.redirect(new URL('/login', req.nextUrl))
        }

        // Feature-gate protection
        const user = req.auth?.user as any;
        const planFeatures = user?.plan_features || [];

        const featureRoutes: Record<string, string> = {
            '/dashboard/tenants': 'api_access', // Example: only if they have API/Infrastructure access
            '/dashboard/users': 'api_access',
            '/dashboard/tools': 'api_access',
            '/dashboard/system-status': 'api_access'
        };

        const matchingRoute = Object.keys(featureRoutes).find(route => pathname.startsWith(route));
        if (matchingRoute) {
            const requiredFeature = featureRoutes[matchingRoute];
            if (!planFeatures.includes(requiredFeature)) {
                // For admin, we might want a different redirect or just a simple error
                return NextResponse.redirect(new URL('/dashboard?error=feature_restricted', req.url));
            }
        }
    }

    // Redirect authenticated users away from login page
    if (pathname === '/login') {
        if (isLoggedIn) {
            return NextResponse.redirect(new URL('/dashboard', req.nextUrl))
        }
    }

    return NextResponse.next();
})

export const config = {
    matcher: [
        '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
        '/(api|trpc)(.*)',
    ],
};
