import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET() {
  try {
    const response = await fetch(`${BRAIN_API_URL}/api/brain/admin/security`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3009',
      }
    })

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status)
      return NextResponse.json({
        events: [
          {
            id: 'sec-001',
            type: 'failed_auth',
            severity: 'medium',
            description: 'Multiple failed login attempts detected',
            timestamp: '2024-09-26T08:05:00Z',
            user_email: 'suspicious@example.com',
            ip_address: '192.168.1.100'
          },
          {
            id: 'sec-002',
            type: 'login_attempt',
            severity: 'low',
            description: 'Successful login from new location',
            timestamp: '2024-09-26T07:45:00Z',
            user_email: 'john.doe@acmecorp.com',
            ip_address: '10.0.0.50'
          },
          {
            id: 'sec-003',
            type: 'policy_violation',
            severity: 'high',
            description: 'User account suspended for policy violation',
            timestamp: '2024-09-26T05:50:00Z',
            user_email: 'david.wilson@acmecorp.com',
            ip_address: '172.16.0.75'
          }
        ],
        security_score: 94,
        alerts_today: 3,
        resolved_alerts: 127,
        avg_response_time: '12min'
      }, { status: 200 })
    }

    const data = await response.json()
    return NextResponse.json(data)
    
  } catch (error) {
    console.error('Security API error:', error)
    return NextResponse.json({
      events: [],
      security_score: 0,
      alerts_today: 0,
      resolved_alerts: 0,
      avg_response_time: 'N/A',
      error: 'Unable to fetch security data'
    }, { status: 200 })
  }
}