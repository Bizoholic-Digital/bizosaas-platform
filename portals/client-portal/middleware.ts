import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

/**
 * PASS-THROUGH MIDDLEWARE
 * Temporarily disabling all logic to stop potential redirect loops 
 * between /onboarding and /login.
 */
export default function middleware(req: NextRequest) {
    return NextResponse.next();
}

export const config = {
    matcher: [
        '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    ],
};
