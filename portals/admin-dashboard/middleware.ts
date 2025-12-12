import { auth } from "@/lib/auth";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import type { Session } from "next-auth";

export default auth((req: NextRequest & { auth: Session | null }) => {
    const { pathname } = req.nextUrl;

    // Public routes - allow access
    if (
        pathname === "/login" ||
        pathname === "/unauthorized" ||
        pathname.startsWith("/api/auth") ||
        pathname.startsWith("/api/health") ||
        pathname.startsWith("/_next") ||
        pathname.startsWith("/favicon")
    ) {
        return NextResponse.next();
    }

    // Check authentication
    if (!req.auth) {
        const url = new URL("/login", req.url);
        url.searchParams.set("callbackUrl", pathname);
        return NextResponse.redirect(url);
    }

    // Check authorization - require admin role
    const roles = (req.auth.user as any)?.roles || [];
    const hasAdminRole = roles.includes("platform_admin") || roles.includes("super_admin");

    if (!hasAdminRole) {
        return NextResponse.redirect(new URL("/unauthorized", req.url));
    }

    return NextResponse.next();
});

export const config = {
    matcher: [
        "/((?!_next/static|_next/image|favicon.ico).*)",
    ],
};
