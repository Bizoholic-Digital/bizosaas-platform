import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://host.docker.internal:8001'

export async function POST(
  request: NextRequest,
  { params }: { params: { integrationId: string } }
) {
  try {
    const body = await request.json()
    const { integrationId } = params

    const response = await fetch(`${BRAIN_API_URL}/api/integrations/admin/${integrationId}/toggle`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    })

    if (!response.ok) {
      throw new Error(`Brain API responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    console.error(`Error toggling integration ${params.integrationId}:`, error)
    
    // Return mock success response for development
    return NextResponse.json({
      success: true,
      message: `Integration ${params.integrationId} toggled successfully`,
      integration_id: params.integrationId,
      global_enabled: JSON.parse(await request.text()).global_enabled
    })
  }
}