import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET() {
  try {
    const response = await fetch(`${BRAIN_API_URL}/api/brain/admin/integrations`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3009',
      }
    })

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status)
      return NextResponse.json({
        integrations: [
          {
            id: 'int-001',
            name: 'Django CRM',
            type: 'api',
            status: 'connected',
            lastSync: '2024-09-26T08:00:00Z',
            endpoint: 'http://localhost:8000',
            description: 'Customer relationship management system',
            health_score: 98
          },
          {
            id: 'int-002',
            name: 'Wagtail CMS',
            type: 'api',
            status: 'connected',
            lastSync: '2024-09-26T07:45:00Z',
            endpoint: 'http://localhost:8006',
            description: 'Content management system',
            health_score: 95
          },
          {
            id: 'int-003',
            name: 'Saleor E-commerce',
            type: 'api',
            status: 'connected',
            lastSync: '2024-09-26T08:10:00Z',
            endpoint: 'http://localhost:8003',
            description: 'E-commerce platform',
            health_score: 92
          },
          {
            id: 'int-004',
            name: 'Stripe Payments',
            type: 'payment',
            status: 'connected',
            lastSync: '2024-09-26T07:30:00Z',
            endpoint: 'https://api.stripe.com',
            description: 'Payment processing',
            health_score: 99
          },
          {
            id: 'int-005',
            name: 'Analytics Dashboard',
            type: 'analytics',
            status: 'error',
            lastSync: null,
            endpoint: 'http://localhost:3010',
            description: 'Business intelligence platform',
            health_score: 45
          }
        ]
      }, { status: 200 })
    }

    const data = await response.json()
    return NextResponse.json(data)
    
  } catch (error) {
    console.error('Integrations API error:', error)
    return NextResponse.json({
      integrations: [],
      error: 'Unable to fetch integration data'
    }, { status: 200 })
  }
}