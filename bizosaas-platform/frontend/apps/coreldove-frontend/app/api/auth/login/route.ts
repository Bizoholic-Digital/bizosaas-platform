import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { email, password, platform } = await request.json()

    // For demo purposes, accept the CoreLDove admin credentials
    // In production, this would validate against BizOSaaS auth service
    if (email === 'admin@coreldove.local' && password === 'admin') {
      const user = {
        id: '1',
        email: 'admin@coreldove.local',
        name: 'CoreLDove Admin',
        role: 'admin',
        platform: platform || 'coreldove',
        authenticated: true,
        permissions: [
          'product_sourcing',
          'saleor_admin',
          'analytics_view',
          'content_generation'
        ]
      }

      // Set session cookie
      const response = NextResponse.json(user)
      response.cookies.set('coreldove_session', 'authenticated', {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        maxAge: 86400 // 24 hours
      })

      return response
    }

    return NextResponse.json(
      { message: 'Invalid credentials' }, 
      { status: 401 }
    )
  } catch (error) {
    console.error('Login error:', error)
    return NextResponse.json(
      { message: 'Login failed' }, 
      { status: 500 }
    )
  }
}