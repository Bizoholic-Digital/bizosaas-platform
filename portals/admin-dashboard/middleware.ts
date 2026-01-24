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
    }

    // Redirect authenticated users away from login page
    if (pathname === '/login') {
        if (isLoggedIn) {
            return NextResponse.redirect(new URL('/dashboard', req.nextUrl))
        }
    }
})

export const config = {
    matcher: [
        '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
        '/(api|trpc)(.*)',
    ],
};
