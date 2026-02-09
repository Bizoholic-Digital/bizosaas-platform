import { NextRequest, NextResponse } from 'next/server'
import { cookies } from 'next/headers'

const AUTH_API_URL = process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://bizosaas-auth-v2:8007'

export async function GET(request: NextRequest) {
  try {
    const cookieStore = await cookies()
    const token = cookieStore.get('access_token')

    console.log('[/api/auth/me] Token present:', !!token)
    if (token) {
      console.log('[/api/auth/me] Token length:', token.value?.length)
    }

    if (!token) {
      console.log('[/api/auth/me] No token found in cookies')
      return NextResponse.json(
        { error: 'Not authenticated' },
        { status: 401 }
      )
    }

    // Call FastAPI auth service to get user info
    console.log('[/api/auth/me] Calling backend:', `${AUTH_API_URL}/auth/me`)
    const response = await fetch(`${AUTH_API_URL}/auth/me`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token.value}`,
      },
    })

    console.log('[/api/auth/me] Backend response status:', response.status)

    if (!response.ok) {
      const errorText = await response.text()
      console.log('[/api/auth/me] Backend error:', errorText)
      // Clear invalid token
      cookieStore.set('access_token', '', {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax',
        maxAge: 0,
        expires: new Date(0),
        path: '/',
      })
      return NextResponse.json(
        { error: 'Invalid or expired token' },
        { status: 401 }
      )
    }

    const data = await response.json()
    console.log('[/api/auth/me] Success, user:', data.user?.email)
    return NextResponse.json(data)
  } catch (error) {
    console.error('Get user error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
