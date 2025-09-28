import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_BASE = process.env.BRAIN_API_URL || 'http://host.docker.internal:8001'

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const tenant_id = searchParams.get('tenant_id') || 'demo'
    const account_id = searchParams.get('account_id')
    const status = searchParams.get('status')
    
    const url = new URL(`${BRAIN_API_BASE}/api/integrations/facebook-ads/campaigns`)
    url.searchParams.set('tenant_id', tenant_id)
    if (account_id) url.searchParams.set('account_id', account_id)
    if (status) url.searchParams.set('status', status)
    
    const response = await fetch(url.toString())
    const data = await response.json()
    
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching Facebook Ads campaigns:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to fetch campaigns' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_BASE}/api/integrations/facebook-ads/campaigns/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    })
    
    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error creating Facebook Ads campaign:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to create campaign' },
      { status: 500 }
    )
  }
}