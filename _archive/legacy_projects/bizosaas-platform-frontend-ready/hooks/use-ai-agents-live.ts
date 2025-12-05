/**
 * AI Agents Integration Hook  
 * Connects dashboards to Universal AI Chat Interface (Port 8001)
 */

import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'

const AI_AGENTS_BASE = 'http://localhost:8001'

// Types for AI Agents data
export interface AIAgentStatus {
  id: string
  name: string
  type: 'marketing' | 'ecommerce' | 'analytics' | 'support' | 'content' | 'seo'
  status: 'active' | 'idle' | 'working' | 'error' | 'maintenance'
  performance: number
  tasks_today: number
  success_rate: number
  last_execution: string
  current_task?: string
  tenant_id?: string
}

export interface AIAgentsHealth {
  status: string
  service: string
  timestamp: string
  active_sessions: number
  total_agents: number
  available_agents: number
}

export interface ChatSession {
  id: string
  user_id: string
  tenant_id: string
  agent_id: string
  agent_name: string
  status: 'active' | 'completed' | 'waiting'
  started_at: string
  last_message_at: string
  message_count: number
}

export interface AgentMetrics {
  agent_id: string
  agent_name: string
  total_conversations: number
  avg_response_time: number
  satisfaction_score: number
  success_rate: number
  active_conversations: number
}

// Custom hooks for AI Agents data
export const useAIAgentsHealth = () => {
  return useQuery({
    queryKey: ['ai-agents', 'health'],
    queryFn: async (): Promise<AIAgentsHealth> => {
      const response = await fetch(`${AI_AGENTS_BASE}/health`)
      if (!response.ok) throw new Error('AI Agents health check failed')
      return response.json()
    },
    refetchInterval: 10000, // Refetch every 10 seconds
  })
}

export const useAIAgentsList = () => {
  return useQuery({
    queryKey: ['ai-agents', 'list'],
    queryFn: async (): Promise<string[]> => {
      const response = await fetch(`${AI_AGENTS_BASE}/agents`)
      if (!response.ok) throw new Error('Failed to fetch agents list')
      const data = await response.json()
      return data.agents || []
    },
    staleTime: 2 * 60 * 1000, // 2 minutes
  })
}

export const useActiveChatSessions = () => {
  return useQuery({
    queryKey: ['ai-agents', 'sessions'],
    queryFn: async (): Promise<ChatSession[]> => {
      const response = await fetch(`${AI_AGENTS_BASE}/chat/sessions`)
      if (!response.ok) {
        // Return empty array if endpoint doesn't exist yet
        return []
      }
      const data = await response.json()
      return data.sessions || []
    },
    refetchInterval: 15000, // Refetch every 15 seconds
  })
}

export const useAgentMetrics = () => {
  return useQuery({
    queryKey: ['ai-agents', 'metrics'],
    queryFn: async (): Promise<AgentMetrics[]> => {
      const response = await fetch(`${AI_AGENTS_BASE}/metrics/agents`)
      if (!response.ok) {
        // Return empty array if endpoint doesn't exist yet
        return []
      }
      const data = await response.json()
      return data.agent_metrics || []
    },
    refetchInterval: 60000, // Refetch every minute
  })
}

// Mock data generator for development (until real endpoints are available)
const generateMockAgents = (agentNames: string[]): AIAgentStatus[] => {
  const types = ['marketing', 'ecommerce', 'analytics', 'support', 'content', 'seo'] as const
  const statuses = ['active', 'idle', 'working', 'error'] as const
  
  return agentNames.map((name, index) => ({
    id: `agent_${index + 1}`,
    name,
    type: types[index % types.length],
    status: statuses[Math.floor(Math.random() * statuses.length)],
    performance: Math.floor(Math.random() * 40) + 60, // 60-100%
    tasks_today: Math.floor(Math.random() * 100),
    success_rate: Math.floor(Math.random() * 30) + 70, // 70-100%
    last_execution: new Date(Date.now() - Math.random() * 3600000).toISOString(),
    current_task: Math.random() > 0.7 ? 'Processing campaign optimization...' : undefined,
    tenant_id: `tenant_${Math.floor(Math.random() * 5) + 1}`
  }))
}

// Enhanced agents data with real-time status
export const useAIAgentsData = () => {
  const { data: health, isLoading: healthLoading } = useAIAgentsHealth()
  const { data: agentNames, isLoading: agentsLoading } = useAIAgentsList()
  const { data: sessions, isLoading: sessionsLoading } = useActiveChatSessions()
  const { data: metrics, isLoading: metricsLoading } = useAgentMetrics()

  const isLoading = healthLoading || agentsLoading

  // Transform data for dashboard consumption
  const dashboardData = {
    health: {
      status: health?.status || 'unknown',
      service: health?.service || 'AI Agents',
      active_sessions: health?.active_sessions || 0,
      total_agents: health?.total_agents || 0,
      available_agents: health?.available_agents || 0
    },
    agents: agentNames ? generateMockAgents(agentNames) : [],
    activeSessions: sessions || [],
    metrics: metrics || [],
    summary: {
      totalAgents: health?.total_agents || 0,
      activeAgents: agentNames ? generateMockAgents(agentNames).filter(a => a.status === 'active').length : 0,
      workingAgents: agentNames ? generateMockAgents(agentNames).filter(a => a.status === 'working').length : 0,
      averagePerformance: agentNames ? 
        Math.round(generateMockAgents(agentNames).reduce((sum, a) => sum + a.performance, 0) / agentNames.length) : 0
    }
  }

  return {
    data: dashboardData,
    isLoading,
    error: null
  }
}

// WebSocket connection for real-time AI agent updates
export const useAIAgentsRealtime = () => {
  const [realtimeData, setRealtimeData] = useState<{
    activeConversations: number
    agentActivity: Record<string, string>
    systemLoad: number
  } | null>(null)
  const [connected, setConnected] = useState(false)

  useEffect(() => {
    let ws: WebSocket | null = null

    const connectWebSocket = () => {
      try {
        // Connect to AI Agents WebSocket endpoint
        ws = new WebSocket(`ws://localhost:8001/ws/agents-status`)
        
        ws.onopen = () => {
          setConnected(true)
          console.log('AI Agents WebSocket connected')
        }

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            setRealtimeData(data)
          } catch (err) {
            console.error('Failed to parse WebSocket message:', err)
          }
        }

        ws.onclose = () => {
          setConnected(false)
          console.log('AI Agents WebSocket disconnected')
          // Attempt to reconnect after 5 seconds
          setTimeout(connectWebSocket, 5000)
        }

        ws.onerror = (error) => {
          console.error('AI Agents WebSocket error:', error)
          setConnected(false)
        }
      } catch (error) {
        console.error('Failed to connect to AI Agents WebSocket:', error)
        setConnected(false)
      }
    }

    connectWebSocket()

    return () => {
      if (ws) {
        ws.close()
      }
    }
  }, [])

  return {
    data: realtimeData,
    connected
  }
}

// Chat interface integration
export const useChatInterface = (agentId: string, tenantId?: string) => {
  const [messages, setMessages] = useState<any[]>([])
  const [connected, setConnected] = useState(false)
  
  const sendMessage = async (message: string) => {
    try {
      const response = await fetch(`${AI_AGENTS_BASE}/chat/${agentId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          tenant_id: tenantId,
          session_id: `session_${Date.now()}`
        })
      })
      
      if (!response.ok) throw new Error('Failed to send message')
      
      const data = await response.json()
      return data.response
    } catch (error) {
      console.error('Failed to send message to agent:', error)
      throw error
    }
  }

  return {
    messages,
    connected,
    sendMessage
  }
}