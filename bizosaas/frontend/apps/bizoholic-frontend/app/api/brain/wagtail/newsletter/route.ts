import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_URL}/wagtail/newsletter-signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.BRAIN_API_KEY || 'dev-token'}`,
      },
      body: JSON.stringify({
        form_type: 'bizoholic_newsletter',
        data: {
          email: body.email,
          source: body.source || 'website',
          interests: body.interests || ['marketing_insights'],
          timestamp: new Date().toISOString(),
          ip_address: request.headers.get('x-forwarded-for') || 'unknown',
          user_agent: request.headers.get('user-agent') || 'unknown'
        }
      }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(`Brain API responded with status: ${response.status}, ${JSON.stringify(errorData)}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error submitting newsletter signup to Brain API:', error)
    
    // Fallback response for development
    const fallbackData = {
      success: true,
      message: 'Thank you for subscribing! (Development mode)',
      subscriber_id: 'dev-' + Date.now(),
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData, { status: 200 })
  }
}