import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Forward the request to the Brain API
    const brainApiResponse = await fetch(`http://host.docker.internal:8001/api/integrations/google-search-console/search-analytics`, {
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
    console.error('Error fetching Google Search Console search analytics:', error)
    return NextResponse.json(
      { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error' 
      },
      { status: 500 }
    )
  }
}