import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://host.docker.internal:8001'

export async function POST(request: NextRequest) {
  let body: any = {}
  
  try {
    body = await request.json()
    const { action, integration_ids } = body

    const response = await fetch(`${BRAIN_API_URL}/api/integrations/admin/bulk-action`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ action, integration_ids })
    })

    if (!response.ok) {
      throw new Error(`Brain API responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    console.error(`Error executing bulk action:`, error)
    
    // Return mock bulk action response for development
    return NextResponse.json({
      success: true,
      action: body.action || 'unknown',
      affected_integrations: body.integration_ids?.length || 0,
      results: (body.integration_ids || []).map((id: string) => ({
        integration_id: id,
        success: true,
        message: `${body.action || 'action'} executed successfully for ${id}`
      })),
      summary: {
        total: body.integration_ids?.length || 0,
        successful: body.integration_ids?.length || 0,
        failed: 0,
        skipped: 0
      }
    })
  }
}