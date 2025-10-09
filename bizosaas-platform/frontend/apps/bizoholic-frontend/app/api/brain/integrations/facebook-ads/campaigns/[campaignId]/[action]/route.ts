import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_BASE = process.env.BRAIN_API_URL || 'http://host.docker.internal:8001'

export async function POST(
  request: NextRequest,
  { params }: { params: { campaignId: string; action: string } }
) {
  try {
    const { campaignId, action } = params
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_BASE}/api/integrations/facebook-ads/campaigns/${campaignId}/${action}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    })
    
    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error with Facebook Ads campaign action:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to perform campaign action' },
      { status: 500 }
    )
  }
}