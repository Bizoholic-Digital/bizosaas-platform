import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET(request: NextRequest) {
  try {
    // Forward request to BizOSaaS Brain
    const response = await fetch(`${BRAIN_API_URL}/api/brain/tenant/list/all`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3006',
      },
    })

    if (!response.ok) {
      // Fallback tenant list
      return NextResponse.json({
        success: true,
        tenants: [
          {
            id: 'coreldove',
            name: 'CorelDove',
            slug: 'coreldove',
            domain: 'coreldove.com',
            logo_url: '/logos/coreldove.png',
            status: 'active',
            subscription_plan: 'enterprise'
          },
          {
            id: 'bizoholic',
            name: 'Bizoholic',
            slug: 'bizoholic',
            domain: 'bizoholic.com',
            logo_url: '/logos/bizoholic.png',
            status: 'active',
            subscription_plan: 'professional'
          },
          {
            id: 'thrillring',
            name: 'ThrillRing Gaming',
            slug: 'thrillring',
            domain: 'thrillring.com',
            logo_url: '/logos/thrillring.png',
            status: 'active',
            subscription_plan: 'professional'
          }
        ],
        total: 3
      })
    }

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    console.error('Error fetching tenant list:', error)

    // Fallback data
    return NextResponse.json({
      success: true,
      tenants: [
        {
          id: 'coreldove',
          name: 'CorelDove',
          slug: 'coreldove',
          status: 'active',
          subscription_plan: 'enterprise'
        }
      ],
      total: 1
    })
  }
}
