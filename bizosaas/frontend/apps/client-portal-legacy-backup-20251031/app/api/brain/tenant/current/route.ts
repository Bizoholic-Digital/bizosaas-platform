import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET(request: NextRequest) {
  try {
    // Get tenant ID from header
    const tenantId = request.headers.get('X-Tenant') || 'coreldove'

    // Forward request to BizOSaaS Brain
    const response = await fetch(`${BRAIN_API_URL}/api/brain/tenant/current`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-Tenant': tenantId,
        'Host': 'localhost:3006',
      },
    })

    if (!response.ok) {
      // Fallback tenant data
      return NextResponse.json({
        id: tenantId,
        name: tenantId.charAt(0).toUpperCase() + tenantId.slice(1),
        slug: tenantId,
        status: 'active',
        subscription_plan: 'professional',
        created_at: new Date().toISOString(),
        settings: {
          theme: 'default',
          currency: 'USD',
          timezone: 'UTC',
          features: []
        }
      })
    }

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    console.error('Error fetching current tenant:', error)

    // Fallback data
    return NextResponse.json({
      id: 'coreldove',
      name: 'CorelDove',
      slug: 'coreldove',
      status: 'active',
      subscription_plan: 'enterprise',
      created_at: new Date().toISOString(),
      settings: {
        theme: 'ecommerce',
        currency: 'INR',
        timezone: 'Asia/Kolkata',
        features: ['ecommerce', 'ai_content', 'amazon_integration']
      }
    })
  }
}
