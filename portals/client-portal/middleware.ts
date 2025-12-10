import { withAuth } from "next-auth/middleware";
import { NextResponse } from "next/server";

export default withAuth(
    async function middleware(req) {
        const token = req.nextauth.token;
        const path = req.nextUrl.pathname;

        // Skip onboarding check for these paths
        if (
            path.startsWith('/onboarding') ||
            path.startsWith('/api') ||
            path.startsWith('/login') ||
            path.startsWith('/_next') ||
            path === '/favicon.ico'
        ) {
            return NextResponse.next();
        }

        // Check if user has completed onboarding
        if (token?.email) {
            try {
                // Call Brain Gateway API to check onboarding status
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/brain/users/profile`, {
                    headers: {
                        'Authorization': `Bearer ${token.accessToken}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (response.ok) {
                    const profile = await response.json();

                    // If user hasn't completed onboarding, redirect to onboarding
                    if (!profile.onboarding_completed && path !== '/onboarding') {
                        return NextResponse.redirect(new URL('/onboarding', req.url));
                    }

                    // If user has completed onboarding but is on onboarding page, redirect to dashboard
                    if (profile.onboarding_completed && path === '/onboarding') {
                        return NextResponse.redirect(new URL('/dashboard', req.url));
                    }
                }
            } catch (error) {
                console.error('Error checking onboarding status:', error);
                // On error, allow access (fail open for better UX)
            }
        }

        return NextResponse.next();
    },
    {
        pages: {
            signIn: "/login",
        },
        callbacks: {
            authorized: ({ token }) => !!token,
        },
    }
);

export const config = {
    matcher: [
        /*
         * Match all request paths except for the ones starting with:
         * - api (API routes)
         * - login (Login page)
         * - _next/static (static files)
         * - _next/image (image optimization files)
         * - favicon.ico (favicon file)
         * - public folder
         */
        "/((?!api|login|_next/static|_next/image|favicon.ico|.*\\.png$).*)",
    ],
};
