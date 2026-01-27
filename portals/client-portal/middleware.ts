import { auth } from "@/lib/auth"
import { NextResponse } from "next/server"

export default auth((req) => {
    // req.auth is populated by the auth wrapper
    const isLoggedIn = !!req.auth;
    const { pathname } = req.nextUrl;

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

        // If logged in but not onboarded and trying to access dashboard, send to onboarding
        const onboarded = (req.auth?.user as any)?.onboarded;
        if (pathname.startsWith('/dashboard') && !onboarded) {
            return NextResponse.redirect(new URL('/onboarding', req.url));
        }

        return NextResponse.next();
    }

    return NextResponse.next();
});

export const config = {
    // Match only the paths we care about to avoid overhead on static assets
    matcher: ['/dashboard/:path*', '/onboarding/:path*', '/login', '/register'],
};
