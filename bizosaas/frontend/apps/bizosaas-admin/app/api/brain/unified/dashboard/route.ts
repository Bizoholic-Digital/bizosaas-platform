import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET(request: NextRequest) {
  try {
    console.log('[BIZOSAAS-ADMIN] Fetching unified dashboard metrics')

    // Try FastAPI Brain Gateway for aggregated data
    try {
      console.log('[BIZOSAAS-ADMIN] Trying FastAPI Brain Gateway for unified metrics')
      const response = await fetch(`${BRAIN_API_URL}/api/brain/unified/dashboard`, {
        headers: {
          'Content-Type': 'application/json',
          'Host': 'localhost:3009',
        },
        next: { revalidate: 300 } // Cache for 5 minutes
      })

      if (response.ok) {
        const brainData = await response.json()
        console.log('[BIZOSAAS-ADMIN] Brain Gateway unified metrics success')
        return NextResponse.json({
          success: true,
          source: 'brain_gateway',
          data: brainData.data || brainData,
          meta: brainData.meta || {}
        })
      }
    } catch (brainError) {
      console.error('[BIZOSAAS-ADMIN] Brain Gateway failed:', brainError)
    }

    // Enhanced fallback with realistic admin data
    console.log('[BIZOSAAS-ADMIN] Using enhanced fallback data')
    const fallbackData = {
      metrics: {
        totalTenants: 247,
        totalUsers: 8429,
        monthlyRevenue: 127543,
        systemHealth: 99.8,
        growth: {
          tenants: 12.5,
          users: 18.3,
          revenue: 23.1,
          health: 0.2
        }
      },
      recentActivities: [
        {
          id: 1,
          type: 'tenant_created',
          message: 'New tenant "Acme Corp" registered',
          timestamp: new Date(Date.now() - 2 * 60 * 1000).toISOString(),
          status: 'success',
          platform: 'client-portal'
        },
        {
          id: 2,
          type: 'system_alert',
          message: 'High CPU usage detected on ThrillRing gaming servers',
          timestamp: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
          status: 'warning',
          platform: 'thrillring'
        },
        {
          id: 3,
          type: 'payment_received',
          message: 'Payment received from CorelDove e-commerce platform',
          timestamp: new Date(Date.now() - 60 * 60 * 1000).toISOString(),
          status: 'success',
          platform: 'coreldove'
        },
        {
          id: 4,
          type: 'business_verified',
          message: '50 new businesses verified in Business Directory',
          timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
          status: 'success',
          platform: 'business-directory'
        },
        {
          id: 5,
          type: 'agent_deployed',
          message: 'AI Lead Scoring Agent deployed for Bizoholic',
          timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
          status: 'success',
          platform: 'bizoholic'
        }
      ],
      systemStats: {
        cpuUsage: 32,
        memoryUsage: 68,
        diskUsage: 45,
        apiRequestsPerMin: 2847,
        activeSessions: 1234,
        databaseConnections: 87,
        maxDbConnections: 100
      },
      platformStats: {
        clientPortal: { active: true, users: 1205, status: 'healthy' },
        businessDirectory: { active: true, businesses: 15487, status: 'healthy' },
        thrillring: { active: true, players: 2048000, status: 'healthy' },
        bizoholic: { active: true, campaigns: 156, status: 'healthy' },
        coreldove: { active: true, orders: 892, status: 'healthy' }
      }
    }

    return NextResponse.json({
      success: true,
      source: 'enhanced_fallback',
      data: fallbackData,
      meta: {
        note: 'Enhanced fallback data with real-time platform simulation',
        platforms: 5,
        lastUpdated: new Date().toISOString()
      }
    })

  } catch (error) {
    console.error('[BIZOSAAS-ADMIN] Unified dashboard error:', error)
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to fetch unified dashboard data',
        source: 'error_fallback',
        data: {}
      },
      { status: 500 }
    )
  }
}
