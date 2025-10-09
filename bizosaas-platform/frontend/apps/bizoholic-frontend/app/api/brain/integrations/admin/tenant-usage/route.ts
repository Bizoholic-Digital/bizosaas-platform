import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://host.docker.internal:8001'

export async function GET(request: NextRequest) {
  try {
    const response = await fetch(`${BRAIN_API_URL}/api/integrations/admin/tenant-usage`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store'
    })

    if (!response.ok) {
      throw new Error(`Brain API responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    console.error('Error fetching tenant usage from Brain API:', error)
    
    // Return mock data for development
    return NextResponse.json({
      tenant_integrations: [
        {
          tenant_id: 'bizoholic',
          tenant_name: 'Bizoholic Digital',
          integration_id: 'google-analytics-4',
          integration_name: 'Google Analytics 4',
          enabled: true,
          configured: true,
          last_used: '2025-09-13T15:45:00Z',
          usage_count: 1250,
          error_count: 2,
          status: 'active'
        },
        {
          tenant_id: 'bizoholic',
          tenant_name: 'Bizoholic Digital',
          integration_id: 'meta-ads-advanced',
          integration_name: 'Meta Ads (Advanced)',
          enabled: true,
          configured: true,
          last_used: '2025-09-13T16:20:00Z',
          usage_count: 845,
          error_count: 0,
          status: 'active'
        },
        {
          tenant_id: 'coreldove',
          tenant_name: 'Coreldove E-commerce',
          integration_id: 'stripe-payments',
          integration_name: 'Stripe Payments',
          enabled: true,
          configured: true,
          last_used: '2025-09-13T16:15:00Z',
          usage_count: 2340,
          error_count: 1,
          status: 'active'
        },
        {
          tenant_id: 'coreldove',
          tenant_name: 'Coreldove E-commerce',
          integration_id: 'hubspot-enterprise',
          integration_name: 'HubSpot Enterprise',
          enabled: false,
          configured: false,
          last_used: '2025-09-10T10:30:00Z',
          usage_count: 156,
          error_count: 3,
          status: 'inactive'
        },
        {
          tenant_id: 'demo-client-001',
          tenant_name: 'Demo Client 001',
          integration_id: 'google-analytics-4',
          integration_name: 'Google Analytics 4',
          enabled: true,
          configured: true,
          last_used: '2025-09-13T14:20:00Z',
          usage_count: 567,
          error_count: 0,
          status: 'active'
        },
        {
          tenant_id: 'demo-client-002',
          tenant_name: 'Demo Client 002',
          integration_id: 'meta-ads-advanced',
          integration_name: 'Meta Ads (Advanced)',
          enabled: true,
          configured: false,
          last_used: '2025-09-12T18:45:00Z',
          usage_count: 234,
          error_count: 5,
          status: 'error'
        }
      ]
    })
  }
}