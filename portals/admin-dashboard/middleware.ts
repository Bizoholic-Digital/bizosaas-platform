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
});

matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    '/((?!api/health|_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes (except health check)
    '/(api|trpc)(.*)',
],
