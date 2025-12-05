import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const tenantId = searchParams.get('tenant_id')
    const siteUrl = searchParams.get('site_url')
    
    // Forward the request to the Brain API
    const brainApiResponse = await fetch(`http://host.docker.internal:8001/api/integrations/google-search-console/sitemaps?tenant_id=${tenantId}&site_url=${encodeURIComponent(siteUrl || '')}`, {
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
    console.error('Error fetching Google Search Console sitemaps:', error)
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
    const body = await request.json()
    
    // Forward the request to the Brain API
    const brainApiResponse = await fetch(`http://host.docker.internal:8001/api/integrations/google-search-console/sitemaps`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    })
    
    if (!brainApiResponse.ok) {
      throw new Error(`Brain API responded with status: ${brainApiResponse.status}`)
    }
    
    const data = await brainApiResponse.json()
    return NextResponse.json(data)
    
  } catch (error) {
    console.error('Error adding Google Search Console sitemap:', error)
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
    const body = await request.json()
    
    // Forward the request to the Brain API
    const brainApiResponse = await fetch(`http://host.docker.internal:8001/api/integrations/google-search-console/sitemaps`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    })
    
    if (!brainApiResponse.ok) {
      throw new Error(`Brain API responded with status: ${brainApiResponse.status}`)
    }
    
    const data = await brainApiResponse.json()
    return NextResponse.json(data)
    
  } catch (error) {
    console.error('Error deleting Google Search Console sitemap:', error)
    return NextResponse.json(
      { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      },
      { status: 500 }
    )
  }
}