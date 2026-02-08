'use client'

import { useState, useEffect, useCallback } from 'react'
import { agentsApi, AIAgent, AgentConfig, AgentExecution, AgentStats } from '@/lib/api/agents-api'

// Hook for managing AI agents
export function useAgents(options: {
  autoRefresh?: boolean
  refreshInterval?: number
} = {}) {
  const [agents, setAgents] = useState<AIAgent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchAgents = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await agentsApi.getAgents()
      setAgents(data)
    } catch (err) {
      console.error('Failed to fetch agents:', err)
      setError(err instanceof Error ? err.message : 'Failed to fetch agents')
      
      // Fallback to mock data
      const mockAgents: AIAgent[] = [
        {
          id: '1',
          name: 'Digital Presence Auditor',
          type: 'analytics',
          status: 'active',
          description: 'Analyzes company digital presence across all platforms and provides optimization recommendations',
          lastRun: new Date(Date.now() - 3600000).toISOString(),
          nextRun: new Date(Date.now() + 3600000).toISOString(),
          tasksCompleted: 45,
          tasksTotal: 50,
          performance: 92,
          capabilities: ['Website Analysis', 'Social Media Audit', 'SEO Assessment', 'Competitor Analysis'],
          config: {
            enabled: true,
            schedule: { type: 'interval', value: '60' },
            parameters: { depth: 'comprehensive', includeCompetitors: true },
            notifications: { onSuccess: true, onError: true, onWarning: false },
            limits: { maxExecutionTime: 1800, maxRetries: 3 },
            integrations: { 'google-analytics': { enabled: true, config: {} } }
          },
          metrics: {
            successRate: 94.2,
            avgExecutionTime: 180,
            tasksThisWeek: 12,
            totalExecutions: 156,
            errorRate: 0.058
          }
        },
        {
          id: '2',
          name: 'Campaign Strategist',
          type: 'marketing',
          status: 'working',
          description: 'Creates and optimizes marketing campaigns using AI-driven insights and market analysis',
          lastRun: new Date(Date.now() - 1800000).toISOString(),
          tasksCompleted: 23,
          tasksTotal: 30,
          performance: 88,
          capabilities: ['Campaign Creation', 'Audience Targeting', 'Budget Optimization', 'A/B Testing'],
          config: {
            enabled: true,
            schedule: { type: 'cron', value: '0 */4 * * *' },
            parameters: { budgetRange: { min: 100, max: 10000 }, targetAudience: 'broad' },
            notifications: { onSuccess: true, onError: true, onWarning: true },
            limits: { maxExecutionTime: 3600, maxRetries: 2 },
            integrations: { 'google-ads': { enabled: true, config: {} }, 'facebook-ads': { enabled: true, config: {} } }
          },
          metrics: {
            successRate: 91.7,
            avgExecutionTime: 240,
            tasksThisWeek: 8,
            totalExecutions: 89,
            errorRate: 0.083
          }
        },
        {
          id: '3',
          name: 'Content Generator',
          type: 'content',
          status: 'idle',
          description: 'Generates high-quality marketing content including copy, images, and video scripts',
          lastRun: new Date(Date.now() - 7200000).toISOString(),
          nextRun: new Date(Date.now() + 43200000).toISOString(),
          tasksCompleted: 67,
          tasksTotal: 75,
          performance: 96,
          capabilities: ['Content Writing', 'Image Generation', 'Video Scripts', 'Social Posts'],
          config: {
            enabled: true,
            schedule: { type: 'manual' },
            parameters: { contentTypes: ['blog', 'social', 'email'], tone: 'professional' },
            notifications: { onSuccess: false, onError: true, onWarning: false },
            limits: { maxExecutionTime: 900, maxRetries: 1 },
            integrations: { 'openai': { enabled: true, config: {} }, 'midjourney': { enabled: false, config: {} } }
          },
          metrics: {
            successRate: 97.3,
            avgExecutionTime: 90,
            tasksThisWeek: 15,
            totalExecutions: 234,
            errorRate: 0.027
          }
        }
      ]
      setAgents(mockAgents)
    } finally {
      setLoading(false)
    }
  }, [])

  const updateAgentConfig = useCallback(async (agentId: string, config: Partial<AgentConfig>) => {
    try {
      const updatedAgent = await agentsApi.updateAgentConfig(agentId, config)
      setAgents(prev => prev.map(agent => 
        agent.id === agentId ? updatedAgent : agent
      ))
      return updatedAgent
    } catch (err) {
      console.error('Failed to update agent config:', err)
      throw err
    }
  }, [])

  const startAgent = useCallback(async (agentId: string) => {
    try {
      const execution = await agentsApi.startAgent(agentId)
      // Update agent status optimistically
      setAgents(prev => prev.map(agent => 
        agent.id === agentId ? { ...agent, status: 'working' as const } : agent
      ))
      return execution
    } catch (err) {
      console.error('Failed to start agent:', err)
      throw err
    }
  }, [])

  const stopAgent = useCallback(async (agentId: string) => {
    try {
      await agentsApi.stopAgent(agentId)
      setAgents(prev => prev.map(agent => 
        agent.id === agentId ? { ...agent, status: 'idle' as const } : agent
      ))
    } catch (err) {
      console.error('Failed to stop agent:', err)
      throw err
    }
  }, [])

  const pauseAgent = useCallback(async (agentId: string) => {
    try {
      await agentsApi.pauseAgent(agentId)
      setAgents(prev => prev.map(agent => 
        agent.id === agentId ? { ...agent, status: 'paused' as const } : agent
      ))
    } catch (err) {
      console.error('Failed to pause agent:', err)
      throw err
    }
  }, [])

  const restartAgent = useCallback(async (agentId: string) => {
    try {
      const execution = await agentsApi.restartAgent(agentId)
      setAgents(prev => prev.map(agent => 
        agent.id === agentId ? { ...agent, status: 'working' as const } : agent
      ))
      return execution
    } catch (err) {
      console.error('Failed to restart agent:', err)
      throw err
    }
  }, [])

  useEffect(() => {
    fetchAgents()
  }, [fetchAgents])

  // Auto-refresh functionality
  useEffect(() => {
    if (options.autoRefresh && options.refreshInterval) {
      const interval = setInterval(fetchAgents, options.refreshInterval)
      return () => clearInterval(interval)
    }
  }, [options.autoRefresh, options.refreshInterval, fetchAgents])

  return {
    agents,
    loading,
    error,
    refetch: fetchAgents,
    updateAgentConfig,
    startAgent,
    stopAgent,
    pauseAgent,
    restartAgent,
  }
}

// Hook for agent statistics
export function useAgentStats() {
  const [stats, setStats] = useState<AgentStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchStats = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await agentsApi.getAgentStats()
      setStats(data)
    } catch (err) {
      console.error('Failed to fetch agent stats:', err)
      setError(err instanceof Error ? err.message : 'Failed to fetch stats')
      
      // Fallback stats
      setStats({
        totalAgents: 6,
        activeAgents: 4,
        totalExecutions: 1247,
        avgPerformance: 89,
        systemHealth: 'optimal',
        uptime: 99.7
      })
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchStats()
  }, [fetchStats])

  return {
    stats,
    loading,
    error,
    refetch: fetchStats,
  }
}

// Hook for agent executions
export function useAgentExecutions(agentId: string) {
  const [executions, setExecutions] = useState<AgentExecution[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchExecutions = useCallback(async () => {
    if (!agentId) return
    
    try {
      setLoading(true)
      setError(null)
      const data = await agentsApi.getAgentExecutions(agentId)
      setExecutions(data)
    } catch (err) {
      console.error('Failed to fetch executions:', err)
      setError(err instanceof Error ? err.message : 'Failed to fetch executions')
      
      // Mock executions
      const mockExecutions: AgentExecution[] = [
        {
          id: '1',
          agentId,
          status: 'completed',
          startTime: new Date(Date.now() - 3600000).toISOString(),
          endTime: new Date(Date.now() - 3300000).toISOString(),
          duration: 300,
          result: { tasksCompleted: 5, insights: 12 },
          logs: ['Started execution', 'Processing data...', 'Generated insights', 'Execution completed'],
          metrics: { tasksProcessed: 5, dataGenerated: 1024, apiCallsMade: 23 }
        },
        {
          id: '2',
          agentId,
          status: 'running',
          startTime: new Date(Date.now() - 600000).toISOString(),
          logs: ['Started execution', 'Processing data...'],
          metrics: { tasksProcessed: 2, dataGenerated: 512, apiCallsMade: 8 }
        }
      ]
      setExecutions(mockExecutions)
    } finally {
      setLoading(false)
    }
  }, [agentId])

  const cancelExecution = useCallback(async (executionId: string) => {
    try {
      await agentsApi.cancelExecution(executionId)
      setExecutions(prev => prev.map(exec => 
        exec.id === executionId ? { ...exec, status: 'cancelled' as const } : exec
      ))
    } catch (err) {
      console.error('Failed to cancel execution:', err)
      throw err
    }
  }, [])

  useEffect(() => {
    fetchExecutions()
  }, [fetchExecutions])

  return {
    executions,
    loading,
    error,
    refetch: fetchExecutions,
    cancelExecution,
  }
}

// Hook for system status
export function useSystemStatus() {
  const [status, setStatus] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchStatus = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await agentsApi.getSystemStatus()
      setStatus(data)
    } catch (err) {
      console.error('Failed to fetch system status:', err)
      setError(err instanceof Error ? err.message : 'Failed to fetch status')
      
      // Mock status
      setStatus({
        status: 'healthy',
        agents: { total: 6, active: 4, errors: 1 },
        resources: { cpu: 35, memory: 62, disk: 18 },
        uptime: 99.7
      })
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchStatus()
    
    // Refresh every 30 seconds
    const interval = setInterval(fetchStatus, 30000)
    return () => clearInterval(interval)
  }, [fetchStatus])

  return {
    status,
    loading,
    error,
    refetch: fetchStatus,
  }
}