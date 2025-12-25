import { auth } from "@/lib/auth";
import { NextResponse } from "next/server";

export default auth(async (req) => {
    // TEMPORARILY DISABLED FOR DEBUGGING
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
