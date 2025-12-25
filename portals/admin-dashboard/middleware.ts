import { withAuth } from "next-auth/middleware";
import { NextResponse } from "next/server";

export default withAuth(
    function middleware(req: any) { // Request type can be complex, staying with any for now but adding token check
        const { pathname } = req.nextUrl;
        const nextauth = (req as any).nextauth;
        const token = nextauth?.token;

        // Check authorization - require admin role
        const roles = (token?.roles as string[]) || [];
        const hasAdminRole = roles.includes("platform_admin") || roles.includes("super_admin") || roles.includes("admin");

        if (!hasAdminRole) {
            return NextResponse.redirect(new URL("/unauthorized", req.url));
        }

        return NextResponse.next();
    },
    {
        callbacks: {
            authorized: () => true,
        },
        pages: {
            signIn: "/login",
        },
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
