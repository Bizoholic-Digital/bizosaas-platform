import { NextRequest, NextResponse } from 'next/server'

interface WorkflowRequest {
  workflow_type: string
  tenant_id: string
  user_id: string
  input_data: Record<string, any>
}

// Temporal workflow client proxy
class TemporalWorkflowClient {
  private baseUrl = 'http://localhost:8000'
  
  async startWorkflow(request: WorkflowRequest) {
    try {
      const response = await fetch(`${this.baseUrl}/api/workflows/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
        signal: AbortSignal.timeout(30000) // 30 second timeout
      })

      if (!response.ok) {
        throw new Error(`Workflow start failed: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Temporal workflow start error:', error)
      throw error
    }
  }

  async getWorkflowStatus(workflowId: string) {
    try {
      const response = await fetch(`${this.baseUrl}/api/workflows/status/${workflowId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(10000) // 10 second timeout
      })

      if (!response.ok) {
        throw new Error(`Workflow status failed: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Temporal workflow status error:', error)
      throw error
    }
  }

  async listWorkflows(tenantId?: string, limit: number = 50) {
    try {
      const params = new URLSearchParams({
        limit: limit.toString(),
        ...(tenantId && { tenant_id: tenantId })
      })

      const response = await fetch(`${this.baseUrl}/api/workflows/list?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(10000)
      })

      if (!response.ok) {
        throw new Error(`Workflow list failed: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Temporal workflow list error:', error)
      throw error
    }
  }

  async cancelWorkflow(workflowId: string) {
    try {
      const response = await fetch(`${this.baseUrl}/api/workflows/cancel/${workflowId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(10000)
      })

      if (!response.ok) {
        throw new Error(`Workflow cancel failed: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Temporal workflow cancel error:', error)
      throw error
    }
  }
}

const temporalClient = new TemporalWorkflowClient()

export async function POST(req: NextRequest) {
  try {
    const data: WorkflowRequest = await req.json()
    
    // Validate request
    if (!data.workflow_type || !data.tenant_id || !data.user_id) {
      return NextResponse.json(
        { error: 'workflow_type, tenant_id, and user_id are required' },
        { status: 400 }
      )
    }

    // Start workflow
    const result = await temporalClient.startWorkflow(data)
    
    return NextResponse.json({
      success: true,
      workflow_id: result.workflow_id,
      execution_id: result.execution_id,
      status: result.status,
      started_at: result.started_at
    })

  } catch (error) {
    console.error('Workflow start API error:', error)
    return NextResponse.json(
      { error: 'Failed to start workflow' },
      { status: 500 }
    )
  }
}

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url)
  const action = searchParams.get('action') || 'list'
  const workflowId = searchParams.get('workflow_id')
  const tenantId = searchParams.get('tenant_id')
  const limit = parseInt(searchParams.get('limit') || '50')

  try {
    switch (action) {
      case 'status':
        if (!workflowId) {
          return NextResponse.json(
            { error: 'workflow_id required for status action' },
            { status: 400 }
          )
        }
        const statusResult = await temporalClient.getWorkflowStatus(workflowId)
        return NextResponse.json(statusResult)

      case 'list':
        const listResult = await temporalClient.listWorkflows(tenantId || undefined, limit)
        return NextResponse.json(listResult)

      default:
        return NextResponse.json(
          { error: 'Invalid action. Use: status, list' },
          { status: 400 }
        )
    }

  } catch (error) {
    console.error('Workflow API error:', error)
    return NextResponse.json(
      { error: 'Failed to process workflow request' },
      { status: 500 }
    )
  }
}

export async function DELETE(req: NextRequest) {
  const { searchParams } = new URL(req.url)
  const workflowId = searchParams.get('workflow_id')

  if (!workflowId) {
    return NextResponse.json(
      { error: 'workflow_id required' },
      { status: 400 }
    )
  }

  try {
    const result = await temporalClient.cancelWorkflow(workflowId)
    
    return NextResponse.json({
      success: true,
      workflow_id: workflowId,
      cancelled: true
    })

  } catch (error) {
    console.error('Workflow cancel API error:', error)
    return NextResponse.json(
      { error: 'Failed to cancel workflow' },
      { status: 500 }
    )
  }
}