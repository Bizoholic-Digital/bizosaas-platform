import { auth } from "@/lib/auth";
import { NextResponse } from "next/server";

export default auth(async (req) => {
    const isLoginPage = req.nextUrl.pathname === "/login";
    const isAuthenticated = !!req.auth;

    if (!isAuthenticated && !isLoginPage) {
        const loginUrl = new URL("/login", req.url);
        loginUrl.searchParams.set("callbackUrl", req.nextUrl.pathname);
        return NextResponse.redirect(loginUrl);
    }

    return NextResponse.next();
});

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
