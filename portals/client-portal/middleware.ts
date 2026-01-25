import { auth } from "@/lib/auth"
import { NextResponse } from "next/server"

export default auth((req) => {
    const isLoggedIn = !!req.auth
    const isOnOnboarding = req.nextUrl.pathname.startsWith('/onboarding')
    const isOnDashboard = req.nextUrl.pathname.startsWith('/dashboard')

    if (isLoggedIn) {
        const onboarded = (req.auth?.user as any)?.onboarded

        if (!onboarded && !isOnOnboarding && isOnDashboard) {
            return NextResponse.redirect(new URL('/onboarding', req.nextUrl))
        }

        if (onboarded && isOnOnboarding) {
            return NextResponse.redirect(new URL('/dashboard', req.nextUrl))
        }

        if (req.nextUrl.pathname === '/login') {
            return NextResponse.redirect(new URL(onboarded ? '/dashboard' : '/onboarding', req.nextUrl))
        }
    } else if (isOnDashboard || isOnOnboarding) {
        return NextResponse.redirect(new URL('/login', req.nextUrl))
    }
})

export const config = {
    matcher: [
        '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
        '/(api|trpc)(.*)',
    ],
};
