import { NextRequest, NextResponse } from 'next/server'
import { cookies } from 'next/headers'

const AUTH_API_URL = process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://bizosaas-auth-v2:8007'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { email, password } = body

    if (!email || !password) {
      return NextResponse.json(
        { error: 'Email and password are required' },
        { status: 400 }
      )
    }

    // Call FastAPI auth service
    const response = await fetch(`${AUTH_API_URL}/auth/sso/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    })

    if (!response.ok) {
      const errorText = await response.text()
      let errorDetail = 'Authentication failed'

      try {
        const errorJson = JSON.parse(errorText)
        errorDetail = errorJson.detail || errorJson.error || errorText
      } catch (e) {
        console.error('Failed to parse error response:', errorText)
        errorDetail = errorText || `Error ${response.status}: ${response.statusText}`
      }

      return NextResponse.json(
        { error: errorDetail },
        { status: response.status }
      )
    }

    const data = await response.json()

    // Set secure HTTP-only cookie with the access token
    const cookieStore = await cookies()
    cookieStore.set('access_token', data.access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 60 * 60 * 24, // 24 hours
      path: '/',
    })

    // Return user data (without token for security)
    // AuthResponse structure: { access_token, user: {...}, tenant: {...}, permissions: [...] }
    return NextResponse.json({
      user_id: data.user?.id || data.user_id,
      email: data.user?.email || data.email,
      first_name: data.user?.first_name,
      last_name: data.user?.last_name,
      full_name: data.user?.first_name && data.user?.last_name
        ? `${data.user.first_name} ${data.user.last_name}`
        : data.user?.email?.split('@')[0],
      role: data.user?.role,
      tenant_id: data.user?.tenant_id || data.tenant?.id,
    })
  } catch (error) {
    console.error('Login error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
