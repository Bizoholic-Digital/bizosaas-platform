// Middleware stub - auth checking disabled for now
// Will be implemented when backend auth API is ready

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // For now, allow all requests through
  // TODO: Add auth token validation when backend is ready
  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/settings/:path*']
}
