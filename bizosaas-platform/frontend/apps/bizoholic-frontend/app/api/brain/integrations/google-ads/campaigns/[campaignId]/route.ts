import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_BASE = process.env.BRAIN_API_URL || 'http://host.docker.internal:8001'

export async function GET(
  request: NextRequest,
  { params }: { params: { campaignId: string } }
) {
  try {
    const searchParams = request.nextUrl.searchParams
    const action = searchParams.get('action')
    const tenant_id = searchParams.get('tenant_id') || 'demo'
    const date_range = searchParams.get('date_range') || '30'
    
    const campaignId = params.campaignId
    
    if (action === 'performance') {
      const url = `${BRAIN_API_BASE}/api/integrations/google-ads/campaigns/${campaignId}/performance?tenant_id=${tenant_id}&date_range=${date_range}`
      
      const response = await fetch(url)
      const data = await response.json()
      
      return NextResponse.json(data)
    }
    
    return NextResponse.json(
      { success: false, error: 'Invalid action specified' },
      { status: 400 }
    )
  } catch (error) {
    console.error('Error fetching campaign data:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to fetch campaign data' },
      { status: 500 }
    )
  }
}

export async function POST(
  request: NextRequest,
  { params }: { params: { campaignId: string } }
) {
  try {
    const body = await request.json()
    const { action, ...requestData } = body
    const campaignId = params.campaignId
    
    let endpoint = ''
    let method = 'POST'
    
    switch (action) {
      case 'pause':
        endpoint = `${BRAIN_API_BASE}/api/integrations/google-ads/campaigns/${campaignId}/pause`
        break
      case 'resume':
        endpoint = `${BRAIN_API_BASE}/api/integrations/google-ads/campaigns/${campaignId}/resume`
        break
      case 'sync':
        endpoint = `${BRAIN_API_BASE}/api/integrations/google-ads/campaigns/sync`
        break
      default:
        return NextResponse.json(
          { success: false, error: 'Invalid action' },
          { status: 400 }
        )
    }
    
    const response = await fetch(endpoint, {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData)
    })
    
    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error performing campaign action:', error)
    return NextResponse.json(
      { success: false, error: 'Campaign action failed' },
      { status: 500 }
    )
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { campaignId: string } }
) {
  try {
    const body = await request.json()
    const { action, ...requestData } = body
    const campaignId = params.campaignId
    
    if (action === 'budget') {
      const response = await fetch(`${BRAIN_API_BASE}/api/integrations/google-ads/campaigns/${campaignId}/budget`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      })
      
      const data = await response.json()
      return NextResponse.json(data)
    }
    
    return NextResponse.json(
      { success: false, error: 'Invalid action for PUT request' },
      { status: 400 }
    )
  } catch (error) {
    console.error('Error updating campaign:', error)
    return NextResponse.json(
      { success: false, error: 'Campaign update failed' },
      { status: 500 }
    )
  }
}