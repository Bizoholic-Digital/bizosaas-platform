import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const tenantId = searchParams.get('tenant_id') || 'demo'
    
    // Forward the request to the Brain API
    const brainApiResponse = await fetch(`http://host.docker.internal:8001/api/integrations/google-search-console?tenant_id=${tenantId}`, {
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
    console.error('Error getting Google Search Console integration details:', error)
    return NextResponse.json(
      { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const tenantId = searchParams.get('tenant_id') || 'demo'
    const body = await request.json()
    
    // Forward the request to the Brain API
    const brainApiResponse = await fetch(`http://host.docker.internal:8001/api/integrations/google-search-console`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        tenant_id: tenantId,
        ...body
      })
    })
    
    if (!brainApiResponse.ok) {
      throw new Error(`Brain API responded with status: ${brainApiResponse.status}`)
    }
    
    const data = await brainApiResponse.json()
    return NextResponse.json(data)
    
  } catch (error) {
    console.error('Error with Google Search Console integration:', error)
    return NextResponse.json(
      { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      },
      { status: 500 }
    )
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const tenantId = searchParams.get('tenant_id') || 'demo'
    
    // Forward the request to the Brain API
    const brainApiResponse = await fetch(`http://host.docker.internal:8001/api/integrations/google-search-console/disconnect`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        tenant_id: tenantId
      })
    })
    
    if (!brainApiResponse.ok) {
      throw new Error(`Brain API responded with status: ${brainApiResponse.status}`)
    }
    
    const data = await brainApiResponse.json()
    return NextResponse.json(data)
    
  } catch (error) {
    console.error('Error disconnecting Google Search Console integration:', error)
    return NextResponse.json(
      { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      },
      { status: 500 }
    )
  }
}