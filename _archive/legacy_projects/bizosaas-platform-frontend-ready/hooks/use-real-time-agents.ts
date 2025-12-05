import { useState, useEffect } from 'react'
import { useAgentStatusUpdates } from '@/lib/websocket'

interface AIAgent {
  id: string
  name: string
  type: 'marketing' | 'analytics' | 'content' | 'social' | 'seo' | 'reputation' | 'support'
  status: 'active' | 'idle' | 'working' | 'error' | 'paused' | 'maintenance'
  performance: number
  capabilities: string[]
  metrics: {
    successRate: number
    avgExecutionTime: number
    tasksThisWeek: number
    tasksToday: number
    errorCount: number
    uptime: number
  }
  lastExecution: string
  currentTask?: string
  progress?: number
  created_at: string
  updated_at: string
}

export function useRealTimeAgents(initialAgents: AIAgent[] = []) {
  const [agents, setAgents] = useState<AIAgent[]>(initialAgents)
  const [recentActivity, setRecentActivity] = useState<Array<{
    agentId: string
    action: string
    details: string
    timestamp: string
  }>>([])

  // Subscribe to agent status updates
  useEffect(() => {
    const unsubscribe = useAgentStatusUpdates((data) => {
      const { agent_id, action, agent_data, details } = data
      
      // Add to recent activity
      setRecentActivity(prev => [
        {
          agentId: agent_id,
          action,
          details: details || `Agent ${action}`,
          timestamp: new Date().toISOString()
        },
        ...prev.slice(0, 19) // Keep only 20 recent activities
      ])

      // Update agents list
      switch (action) {
        case 'created':
          setAgents(prev => [agent_data, ...prev])
          break
          
        case 'updated':
          setAgents(prev => prev.map(agent => 
            agent.id === agent_id 
              ? { ...agent, ...agent_data, updated_at: new Date().toISOString() }
              : agent
          ))
          break
          
        case 'deleted':
          setAgents(prev => prev.filter(agent => agent.id !== agent_id))
          break
          
        case 'status_changed':
          setAgents(prev => prev.map(agent => 
            agent.id === agent_id 
              ? { 
                  ...agent, 
                  status: agent_data.status,
                  lastExecution: new Date().toISOString(),
                  updated_at: new Date().toISOString() 
                }
              : agent
          ))
          break
          
        case 'task_started':
          setAgents(prev => prev.map(agent => 
            agent.id === agent_id 
              ? { 
                  ...agent, 
                  status: 'working',
                  currentTask: agent_data.task_name,
                  progress: 0,
                  updated_at: new Date().toISOString() 
                }
              : agent
          ))
          break
          
        case 'task_progress':
          setAgents(prev => prev.map(agent => 
            agent.id === agent_id 
              ? { 
                  ...agent, 
                  progress: agent_data.progress,
                  updated_at: new Date().toISOString() 
                }
              : agent
          ))
          break
          
        case 'task_completed':
          setAgents(prev => prev.map(agent => 
            agent.id === agent_id 
              ? { 
                  ...agent, 
                  status: 'active',
                  currentTask: undefined,
                  progress: undefined,
                  lastExecution: new Date().toISOString(),
                  metrics: {
                    ...agent.metrics,
                    tasksToday: agent.metrics.tasksToday + 1,
                    tasksThisWeek: agent.metrics.tasksThisWeek + 1,
                    successRate: agent_data.success ? 
                      Math.min(100, agent.metrics.successRate + 1) : 
                      Math.max(0, agent.metrics.successRate - 1)
                  },
                  updated_at: new Date().toISOString() 
                }
              : agent
          ))
          break
          
        case 'task_failed':
          setAgents(prev => prev.map(agent => 
            agent.id === agent_id 
              ? { 
                  ...agent, 
                  status: 'error',
                  currentTask: undefined,
                  progress: undefined,
                  lastExecution: new Date().toISOString(),
                  metrics: {
                    ...agent.metrics,
                    errorCount: agent.metrics.errorCount + 1,
                    successRate: Math.max(0, agent.metrics.successRate - 2)
                  },
                  updated_at: new Date().toISOString() 
                }
              : agent
          ))
          break
          
        case 'performance_updated':
          setAgents(prev => prev.map(agent => 
            agent.id === agent_id 
              ? { 
                  ...agent, 
                  performance: agent_data.performance,
                  metrics: { ...agent.metrics, ...agent_data.metrics },
                  updated_at: new Date().toISOString() 
                }
              : agent
          ))
          break
      }
    })

    return unsubscribe
  }, [])

  // Utility functions
  const getAgentById = (id: string) => agents.find(agent => agent.id === id)
  
  const getAgentsByStatus = (status: AIAgent['status']) => 
    agents.filter(agent => agent.status === status)
  
  const getAgentsByType = (type: AIAgent['type']) => 
    agents.filter(agent => agent.type === type)
  
  const getActiveAgents = () => getAgentsByStatus('active').concat(getAgentsByStatus('working'))
  
  const getIdleAgents = () => getAgentsByStatus('idle')
  
  const getErroredAgents = () => getAgentsByStatus('error')
  
  const getWorkingAgents = () => getAgentsByStatus('working')

  const getAveragePerformance = () => {
    if (agents.length === 0) return 0
    return agents.reduce((sum, agent) => sum + agent.performance, 0) / agents.length
  }
  
  const getTotalTasksToday = () => 
    agents.reduce((sum, agent) => sum + agent.metrics.tasksToday, 0)
  
  const getTotalTasksThisWeek = () => 
    agents.reduce((sum, agent) => sum + agent.metrics.tasksThisWeek, 0)
  
  const getTotalErrors = () => 
    agents.reduce((sum, agent) => sum + agent.metrics.errorCount, 0)
  
  const getOverallSuccessRate = () => {
    if (agents.length === 0) return 0
    return agents.reduce((sum, agent) => sum + agent.metrics.successRate, 0) / agents.length
  }

  const getRecentlyActive = (minutes: number = 30) => {
    const cutoff = new Date(Date.now() - minutes * 60 * 1000)
    return agents.filter(agent => new Date(agent.lastExecution) > cutoff)
  }

  const getAgentHealth = () => {
    const total = agents.length
    const healthy = agents.filter(agent => 
      agent.status !== 'error' && agent.performance > 80
    ).length
    const warning = agents.filter(agent => 
      agent.status !== 'error' && agent.performance > 60 && agent.performance <= 80
    ).length
    const critical = agents.filter(agent => 
      agent.status === 'error' || agent.performance <= 60
    ).length
    
    return { total, healthy, warning, critical }
  }

  return {
    agents,
    recentActivity,
    setAgents,
    
    // Utility functions
    getAgentById,
    getAgentsByStatus,
    getAgentsByType,
    getActiveAgents,
    getIdleAgents,
    getErroredAgents,
    getWorkingAgents,
    
    // Metrics
    getAveragePerformance,
    getTotalTasksToday,
    getTotalTasksThisWeek,
    getTotalErrors,
    getOverallSuccessRate,
    getRecentlyActive,
    getAgentHealth,
    
    // Counts
    totalAgents: agents.length,
    activeAgentsCount: getActiveAgents().length,
    workingAgentsCount: getWorkingAgents().length,
    erroredAgentsCount: getErroredAgents().length,
    recentlyActiveCount: getRecentlyActive().length
  }
}