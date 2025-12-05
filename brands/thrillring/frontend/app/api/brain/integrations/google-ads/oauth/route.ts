import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_BASE = process.env.BRAIN_API_URL || 'http://host.docker.internal:8001'

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const action = searchParams.get('action')
    const tenant_id = searchParams.get('tenant_id') || 'demo'
    
    let endpoint = ''
    
    if (action === 'callback') {
      const code = searchParams.get('code')
      const state = searchParams.get('state')
      const error = searchParams.get('error')
      
      const url = new URL(`${BRAIN_API_BASE}/api/integrations/google-ads/oauth/callback`)
      if (code) url.searchParams.set('code', code)
      if (state) url.searchParams.set('state', state)
      if (error) url.searchParams.set('error', error)
      
      endpoint = url.toString()
    } else {
      // Default to status check
      endpoint = `${BRAIN_API_BASE}/api/integrations/google-ads/oauth/status?tenant_id=${tenant_id}`
    }
    
    const response = await fetch(endpoint)
    const data = await response.json()
    
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error with Google Ads OAuth:', error)
    return NextResponse.json(
      { success: false, error: 'OAuth operation failed' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_BASE}/api/integrations/google-ads/oauth/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    })
    
    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error starting Google Ads OAuth:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to start OAuth flow' },
      { status: 500 }
    )
  }
}