import { NextRequest, NextResponse } from 'next/server'

// Agent management API routes
class AIAgentService {
  private baseUrl = 'http://localhost:8000' // AI Agents service

  async getAllAgents(tenantId?: string) {
    try {
      const params = new URLSearchParams({
        ...(tenantId && { tenant_id: tenantId })
      })

      const response = await fetch(`${this.baseUrl}/api/agents?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(10000)
      })

      if (!response.ok) {
        throw new Error(`Failed to fetch agents: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to fetch agents:', error)
      throw error
    }
  }

  async getAgentDetails(agentId: string) {
    try {
      const response = await fetch(`${this.baseUrl}/api/agents/${agentId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(10000)
      })

      if (!response.ok) {
        throw new Error(`Failed to fetch agent details: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to fetch agent details:', error)
      throw error
    }
  }

  async controlAgent(agentId: string, action: 'start' | 'stop' | 'pause' | 'restart') {
    try {
      const response = await fetch(`${this.baseUrl}/api/agents/${agentId}/control`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action }),
        signal: AbortSignal.timeout(30000)
      })

      if (!response.ok) {
        throw new Error(`Failed to control agent: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to control agent:', error)
      throw error
    }
  }

  async getAgentTasks(agentId: string, limit: number = 50) {
    try {
      const params = new URLSearchParams({
        limit: limit.toString()
      })

      const response = await fetch(`${this.baseUrl}/api/agents/${agentId}/tasks?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(10000)
      })

      if (!response.ok) {
        throw new Error(`Failed to fetch agent tasks: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to fetch agent tasks:', error)
      throw error
    }
  }

  async getAgentLogs(agentId: string, limit: number = 100) {
    try {
      const params = new URLSearchParams({
        limit: limit.toString()
      })

      const response = await fetch(`${this.baseUrl}/api/agents/${agentId}/logs?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(10000)
      })

      if (!response.ok) {
        throw new Error(`Failed to fetch agent logs: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to fetch agent logs:', error)
      throw error
    }
  }

  async updateAgentConfig(agentId: string, config: Record<string, any>) {
    try {
      const response = await fetch(`${this.baseUrl}/api/agents/${agentId}/config`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(config),
        signal: AbortSignal.timeout(30000)
      })

      if (!response.ok) {
        throw new Error(`Failed to update agent config: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to update agent config:', error)
      throw error
    }
  }
}

const agentService = new AIAgentService()

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url)
  const tenantId = searchParams.get('tenant_id')

  try {
    const agents = await agentService.getAllAgents(tenantId || undefined)
    
    return NextResponse.json({
      success: true,
      agents: agents
    })

  } catch (error) {
    console.error('Agents API error:', error)
    return NextResponse.json(
      { error: 'Failed to fetch agents' },
      { status: 500 }
    )
  }
}

export async function POST(req: NextRequest) {
  try {
    const data = await req.json()
    const { action, agent_id, config } = data

    if (!agent_id) {
      return NextResponse.json(
        { error: 'agent_id is required' },
        { status: 400 }
      )
    }

    let result

    switch (action) {
      case 'control':
        if (!data.control_action) {
          return NextResponse.json(
            { error: 'control_action is required for control operations' },
            { status: 400 }
          )
        }
        result = await agentService.controlAgent(agent_id, data.control_action)
        break

      case 'update_config':
        if (!config) {
          return NextResponse.json(
            { error: 'config is required for update operations' },
            { status: 400 }
          )
        }
        result = await agentService.updateAgentConfig(agent_id, config)
        break

      default:
        return NextResponse.json(
          { error: 'Invalid action. Supported actions: control, update_config' },
          { status: 400 }
        )
    }

    return NextResponse.json({
      success: true,
      result: result
    })

  } catch (error) {
    console.error('Agent control API error:', error)
    return NextResponse.json(
      { error: 'Failed to perform agent operation' },
      { status: 500 }
    )
  }
}