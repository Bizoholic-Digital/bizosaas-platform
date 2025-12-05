import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const tenantId = searchParams.get('tenant_id') || 'demo'
    
    // Forward the request to the Brain API
    const brainApiResponse = await fetch(`http://host.docker.internal:8001/api/integrations/google-search-console/oauth/status?tenant_id=${tenantId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    if (!brainApiResponse.ok) {
      throw new Error(`Brain API responded with status: ${brainApiResponse.status}`)
    }
    
    const data = await brainApiResponse.json()
    return NextResponse.json(data)
    
  } catch (error) {
    console.error('Error checking Google Search Console OAuth status:', error)
    return NextResponse.json(
      { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      },
      { status: 500 }
    )
  }
}