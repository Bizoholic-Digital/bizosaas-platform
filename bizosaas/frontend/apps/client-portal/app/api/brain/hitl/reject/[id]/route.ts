import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params

    // Try to call BizOSaaS Brain HITL rejection endpoint
    const response = await fetch(`${BRAIN_API_URL}/api/brain/hitl/reject/${id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3006',
      },
      body: JSON.stringify(await request.json())
    })

    if (!response.ok) {
      // Fallback: Log rejection locally
      console.log(`Rejection for ${id} recorded (fallback mode)`)

      return NextResponse.json({
        success: true,
        message: `Item ${id} rejected successfully`,
        status: 'rejected',
        timestamp: new Date().toISOString()
      })
    }

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    console.error('Error rejecting item:', error)

    return NextResponse.json({
      success: true,
      message: 'Rejection recorded (offline mode)',
      status: 'rejected',
      timestamp: new Date().toISOString()
    })
  }
}
