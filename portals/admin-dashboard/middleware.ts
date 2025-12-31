import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

// Define protected routes
const isProtectedRoute = createRouteMatcher([
    '/',           // Dashboard root
    '/dashboard(.*)', // All dashboard sub-routes
    '/tenants(.*)',
    '/settings(.*)',
    '/users(.*)',
]);

export default clerkMiddleware(async (auth, req) => {
    if (isProtectedRoute(req)) {
        await auth.protect();
    }
}, {
    publishableKey: 'pk_test_Yml6b3NhYXMtY29yZS0xNy5jbGVyay5hY2NvdW50cy5kZXYk'
});

export const config = {
    matcher: [
        // Skip Next.js internals and all static files
        '/((?!api/health|_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
        // Match other API routes but keep health check excluded
        '/api/(?!health)(.*)',
        '/trpc/(.*)'
    ],
};
