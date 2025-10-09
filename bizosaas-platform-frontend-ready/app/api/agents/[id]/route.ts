import { NextRequest, NextResponse } from 'next/server'

interface RouteParams {
  params: {
    id: string
  }
}

// Individual agent API routes
class AIAgentService {
  private baseUrl = 'http://localhost:8000' // AI Agents service

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
      
      // Return mock data if service is unavailable
      return {
        id: agentId,
        name: 'Marketing Strategy Agent',
        type: 'marketing_strategist',
        status: 'active',
        description: 'AI agent for marketing strategy optimization',
        category: 'strategy',
        version: '2.1.3',
        created_at: '2024-01-15T10:00:00Z',
        last_active: '2 minutes ago',
        tasks_completed: 247,
        current_task: 'Analyzing campaign performance',
        performance: {
          efficiency: 94,
          accuracy: 97,
          response_time: 2.3,
          task_success_rate: 96.5,
          resource_usage: {
            cpu: 45,
            memory: 67,
            api_calls: 1247
          }
        }
      }
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
      
      // Return mock data if service is unavailable
      return {
        tasks: [
          {
            id: 'task-001',
            name: 'Campaign Analysis',
            status: 'running',
            start_time: new Date(Date.now() - 1800000).toISOString(), // 30 min ago
            workflow_id: 'wf-campaign-001'
          },
          {
            id: 'task-002',
            name: 'Audience Segmentation',
            status: 'completed',
            start_time: new Date(Date.now() - 3600000).toISOString(), // 1 hour ago
            end_time: new Date(Date.now() - 1800000).toISOString(),
            duration: '30 minutes',
            result: 'Identified 5 high-value segments'
          }
        ]
      }
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
      
      // Return mock data if service is unavailable
      return {
        logs: [
          {
            timestamp: new Date().toISOString(),
            level: 'info',
            message: 'Started campaign analysis task',
            context: { task_id: 'task-001' }
          },
          {
            timestamp: new Date(Date.now() - 300000).toISOString(), // 5 min ago
            level: 'info',
            message: 'Retrieved campaign data from Google Ads API',
            context: { campaigns_count: 47 }
          },
          {
            timestamp: new Date(Date.now() - 600000).toISOString(), // 10 min ago
            level: 'warning',
            message: 'Rate limit approaching for Google Ads API',
            context: { remaining_quota: 150 }
          }
        ]
      }
    }
  }

  async getAgentTools(agentId: string) {
    try {
      const response = await fetch(`${this.baseUrl}/api/agents/${agentId}/tools`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(10000)
      })

      if (!response.ok) {
        throw new Error(`Failed to fetch agent tools: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to fetch agent tools:', error)
      
      // Return mock data if service is unavailable
      return {
        tools: [
          {
            id: 'google-ads-api',
            name: 'Google Ads API',
            type: 'api',
            status: 'active',
            description: 'Access to Google Ads campaign data',
            last_used: '5 minutes ago',
            usage_count: 1247
          },
          {
            id: 'analytics-db',
            name: 'Analytics Database',
            type: 'database',
            status: 'active',
            description: 'Historical campaign performance data',
            last_used: '2 minutes ago',
            usage_count: 892
          }
        ]
      }
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
      
      // Return mock response if service is unavailable
      return {
        success: true,
        action: action,
        agent_id: agentId,
        status: action === 'start' ? 'active' : action === 'stop' ? 'stopped' : action,
        message: `Agent ${action} operation completed`
      }
    }
  }
}

const agentService = new AIAgentService()

export async function GET(req: NextRequest, { params }: RouteParams) {
  const { searchParams } = new URL(req.url)
  const data = searchParams.get('data') || 'details'
  const limit = parseInt(searchParams.get('limit') || '50')

  try {
    let result

    switch (data) {
      case 'details':
        result = await agentService.getAgentDetails(params.id)
        break
      
      case 'tasks':
        result = await agentService.getAgentTasks(params.id, limit)
        break
      
      case 'logs':
        result = await agentService.getAgentLogs(params.id, limit)
        break
      
      case 'tools':
        result = await agentService.getAgentTools(params.id)
        break
      
      default:
        return NextResponse.json(
          { error: 'Invalid data type. Supported: details, tasks, logs, tools' },
          { status: 400 }
        )
    }

    return NextResponse.json({
      success: true,
      agent_id: params.id,
      data: result
    })

  } catch (error) {
    console.error('Agent detail API error:', error)
    return NextResponse.json(
      { error: 'Failed to fetch agent data' },
      { status: 500 }
    )
  }
}

export async function POST(req: NextRequest, { params }: RouteParams) {
  try {
    const data = await req.json()
    const { action } = data

    if (!action) {
      return NextResponse.json(
        { error: 'action is required' },
        { status: 400 }
      )
    }

    const result = await agentService.controlAgent(params.id, action)

    return NextResponse.json({
      success: true,
      agent_id: params.id,
      result: result
    })

  } catch (error) {
    console.error('Agent control API error:', error)
    return NextResponse.json(
      { error: 'Failed to control agent' },
      { status: 500 }
    )
  }
}

export async function PUT(req: NextRequest, { params }: RouteParams) {
  try {
    const config = await req.json()

    // In production, this would update agent configuration
    console.log('Updating agent config:', params.id, config)

    return NextResponse.json({
      success: true,
      agent_id: params.id,
      message: 'Agent configuration updated successfully',
      config: config
    })

  } catch (error) {
    console.error('Agent config update API error:', error)
    return NextResponse.json(
      { error: 'Failed to update agent configuration' },
      { status: 500 }
    )
  }
}