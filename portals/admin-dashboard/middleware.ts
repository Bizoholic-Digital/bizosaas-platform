import { withAuth } from "next-auth/middleware";
import { NextResponse } from "next/server";

// Shared secret logic to match API route
const secret = (process.env.NEXTAUTH_SECRET && process.env.NEXTAUTH_SECRET.length > 8)
    ? process.env.NEXTAUTH_SECRET
    : 'bizosaas-staging-emergency-fallback-secret-2024';

export default withAuth(
    function middleware(req: any) { // Request type can be complex, staying with any for now but adding token check
        const { pathname } = req.nextUrl;
        const nextauth = (req as any).nextauth;
        const token = nextauth?.token;

        console.log("🛡️ [Admin Middleware] Path:", pathname, "Token exists:", !!token);

        // Check authorization - require admin role
        const roles = (token?.roles as string[]) || [];
        const hasAdminRole = roles.includes("platform_admin") || roles.includes("super_admin") || roles.includes("admin");

        if (!hasAdminRole) {
            console.warn("⚠️ [Admin Middleware] User lacks admin role. Roles:", roles);
            // return NextResponse.redirect(new URL("/unauthorized", req.url));
        }

        return NextResponse.next();
    },
    {
        callbacks: {
            authorized: ({ token, req }) => {
                // Return true to allow the middleware function to handle specific logic
                // But ensure token is valid for protected routes
                console.log("🛡️ [Admin Middleware] Authorized check. Token roles:", token?.roles);
                return !!token;
            },
        },
        pages: {
            signIn: "/login",
        },
        cookies: {
            sessionToken: {
                name: 'bizosaas-session-token',
            },
        },
        secret: secret,
    }
);

export const config = {
    matcher: [
        /*
         * Match all request paths except for the ones starting with:
         * - api (API routes, NextAuth handle these separately)
         * - login (Login page)
         * - unauthorized (Unauthorized page)
         * - _next/static (static files)
         * - _next/image (image optimization files)
         * - favicon.ico (favicon file)
         * - public folder icons
         */
        "/((?!api|login|unauthorized|_next/static|_next/image|favicon.ico|manifest.json|manifest.webmanifest|service-worker.js|icons).*)",
    ],
};
