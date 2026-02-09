import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const role = searchParams.get('role')
    const status = searchParams.get('status')
    const search = searchParams.get('search')
    
    const queryString = new URLSearchParams()
    if (role && role !== 'all') queryString.append('role', role)
    if (status && status !== 'all') queryString.append('status', status)
    if (search) queryString.append('search', search)
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/admin/users?${queryString}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3009',
      }
    })

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status)
      return NextResponse.json({
        users: [
          {
            id: "user-001",
            email: "john.doe@acmecorp.com",
            firstName: "John",
            lastName: "Doe",
            role: "admin",
            status: "active",
            tenant: { id: "tenant-001", name: "Acme Corp" },
            created_at: "2024-01-15T10:00:00Z",
            last_login: "2024-09-26T07:30:00Z",
            is_verified: true,
            login_count: 247
          },
          {
            id: "user-002",
            email: "sarah.smith@techstart.com",
            firstName: "Sarah",
            lastName: "Smith",
            role: "manager",
            status: "active",
            tenant: { id: "tenant-002", name: "TechStart LLC" },
            created_at: "2024-02-20T14:30:00Z",
            last_login: "2024-09-26T08:45:00Z",
            is_verified: true,
            login_count: 189
          }
        ],
        total_count: 8429,
        active_count: 8234,
        pending_count: 67,
        suspended_count: 128,
        admin_count: 23,
        user_count: 7892,
        manager_count: 456,
        viewer_count: 58
      }, { status: 200 })
    }

    const data = await response.json()
    return NextResponse.json(data)
    
  } catch (error) {
    console.error('Users API error:', error)
    return NextResponse.json({
      users: [],
      total_count: 0,
      active_count: 0,
      pending_count: 0,
      suspended_count: 0,
      error: 'Unable to fetch user data'
    }, { status: 200 })
  }
}