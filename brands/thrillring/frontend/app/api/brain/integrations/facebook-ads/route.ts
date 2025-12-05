import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_BASE = process.env.BRAIN_API_URL || 'http://host.docker.internal:8001'

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const tenant_id = searchParams.get('tenant_id') || 'demo'
    const type = searchParams.get('type') || 'status'
    
    let endpoint = `${BRAIN_API_BASE}/api/integrations/facebook-ads`
    
    const url = new URL(endpoint)
    url.searchParams.set('tenant_id', tenant_id)
    url.searchParams.set('type', type)
    
    const response = await fetch(url.toString())
    const data = await response.json()
    
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching Facebook Ads data:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to fetch Facebook Ads data' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_BASE}/api/integrations/facebook-ads/action`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    })
    
    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error processing Facebook Ads action:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to process action' },
      { status: 500 }
    )
  }
}