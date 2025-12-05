import { NextRequest, NextResponse } from 'next/server'

const UNIFIED_AUTH_URL = process.env.UNIFIED_AUTH_URL || 'http://host.docker.internal:8007'

export async function GET(request: NextRequest) {
  try {
    // Forward cookies to unified auth service for session validation
    const cookies = request.headers.get('cookie')
    
    const response = await fetch(`${UNIFIED_AUTH_URL}/api/auth/verify-session`, {
      method: 'GET',
      headers: {
        'Cookie': cookies || '',
        'Content-Type': 'application/json',
        'User-Agent': 'CoreLDove-Frontend/1.0'
      }
    })
    
    if (response.ok) {
      const userData = await response.json()
      return NextResponse.json({ 
        authenticated: true, 
        user: userData,
        platform: 'coreldove',
        role: userData.role || 'tenant_admin',
        permissions: userData.permissions || []
      })
    } else {
      return NextResponse.json({ 
        authenticated: false,
        error: 'Session validation failed' 
      }, { status: 401 })
    }
  } catch (error) {
    console.error('Session validation error:', error)
    // Fallback to demo session for development
    return NextResponse.json({
      authenticated: true,
      user: {
        id: '1',
        email: 'admin@coreldove.local',
        name: 'CoreLDove Admin'
      },
      role: 'tenant_admin',
      platform: 'coreldove',
      permissions: [
        'product_sourcing',
        'saleor_admin',
        'analytics_view',
        'content_generation'
      ]
    })
  }
}

export async function DELETE() {
  // Logout endpoint
  const response = NextResponse.json({ message: 'Logged out successfully' })
  response.cookies.set('coreldove_session', '', {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 0
  })
  return response
}