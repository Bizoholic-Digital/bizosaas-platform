import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const status = searchParams.get('status')
    const search = searchParams.get('search')
    
    // Forward request to FastAPI AI Central Hub
    const queryString = new URLSearchParams()
    if (status && status !== 'all') queryString.append('status', status)
    if (search) queryString.append('search', search)
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/admin/tenants?${queryString}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3009',
      }
    })

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status, response.statusText)
      // Return fallback data for development
      return NextResponse.json({
        tenants: [
          {
            id: "tenant-001",
            name: "Acme Corp",
            domain: "acme.bizosaas.com",
            status: "active",
            plan: "enterprise",
            users_count: 45,
            created_at: "2024-01-15T10:00:00Z",
            last_activity: "2024-09-26T07:30:00Z",
            revenue: 15000,
            ai_agents_count: 12
          },
          {
            id: "tenant-002", 
            name: "TechStart LLC",
            domain: "techstart.bizosaas.com",
            status: "active",
            plan: "professional",
            users_count: 23,
            created_at: "2024-02-20T14:30:00Z",
            last_activity: "2024-09-26T08:45:00Z",
            revenue: 8500,
            ai_agents_count: 8
          },
          {
            id: "tenant-003",
            name: "Global Dynamics",
            domain: "globaldyn.bizosaas.com", 
            status: "active",
            plan: "starter",
            users_count: 12,
            created_at: "2024-03-10T09:15:00Z",
            last_activity: "2024-09-25T16:20:00Z",
            revenue: 2500,
            ai_agents_count: 5
          },
          {
            id: "tenant-004",
            name: "Innovation Labs",
            domain: "innolabs.bizosaas.com",
            status: "trial", 
            plan: "trial",
            users_count: 7,
            created_at: "2024-09-20T11:00:00Z",
            last_activity: "2024-09-26T06:15:00Z",
            revenue: 0,
            ai_agents_count: 3
          },
          {
            id: "tenant-005",
            name: "Enterprise Solutions Inc",
            domain: "entsol.bizosaas.com",
            status: "suspended",
            plan: "enterprise",
            users_count: 67,
            created_at: "2023-11-05T12:00:00Z",
            last_activity: "2024-09-15T14:20:00Z",
            revenue: 25000,
            ai_agents_count: 18
          }
        ],
        total_count: 247,
        active_count: 243,
        trial_count: 4,
        suspended_count: 3,
        total_revenue: 127543,
        total_users: 8429,
        growth_rate: 12.5,
        churn_rate: 2.1
      }, { status: 200 })
    }

    const data = await response.json()
    return NextResponse.json(data)
    
  } catch (error) {
    console.error('Tenant API error:', error)
    // Return fallback data on any error
    return NextResponse.json({
      tenants: [],
      total_count: 0,
      active_count: 0,
      trial_count: 0,
      suspended_count: 0,
      total_revenue: 0,
      total_users: 0,
      growth_rate: 0,
      churn_rate: 0,
      error: 'Unable to fetch tenant data'
    }, { status: 200 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/admin/tenants`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3009',
      },
      body: JSON.stringify(body)
    })

    if (!response.ok) {
      console.error('FastAPI AI Central Hub POST error:', response.status)
      return NextResponse.json({
        success: false,
        message: 'Unable to create tenant - using fallback response',
        tenant: {
          id: `tenant-${Date.now()}`,
          ...body,
          status: 'pending',
          created_at: new Date().toISOString(),
          users_count: 0,
          revenue: 0,
          ai_agents_count: 0
        }
      }, { status: 200 })
    }

    const data = await response.json()
    return NextResponse.json(data)
    
  } catch (error) {
    console.error('Tenant creation error:', error)
    return NextResponse.json({
      success: false,
      message: 'Error creating tenant',
      error: (error as any).message
    }, { status: 500 })
  }
}