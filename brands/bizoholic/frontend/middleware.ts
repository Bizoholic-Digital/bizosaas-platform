export { default } from "next-auth/middleware"

export const config = {
  matcher: [
    "/dashboard/:path*",
    "/portal/:path*",
    "/admin/:path*",
    // Add other protected routes here
  ],
}
