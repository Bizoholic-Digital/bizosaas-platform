"use client"

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Bot, 
  Play, 
  Pause, 
  Square, 
  Clock, 
  CheckCircle, 
  XCircle, 
  AlertCircle,
  Zap,
  Activity,
  TrendingUp,
  Users
} from 'lucide-react'
import { useWebSocket } from '@/lib/websocket-client'
import { useAuth } from '@/hooks/use-auth'

interface AgentExecution {
  id: string
  name: string
  category: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'paused'
  progress: number
  tenant_id: string
  started_at: string
  completed_at?: string
  error_message?: string
  result?: any
  logs: Array<{
    timestamp: string
    level: 'info' | 'warning' | 'error'
    message: string
  }>
  metrics?: {
    cpu_usage: number
    memory_usage: number
    execution_time: number
    tokens_used?: number
    cost_usd?: number
  }
}

interface AgentStats {
  total_executions: number
  success_rate: number
  avg_execution_time: number
  total_cost: number
  active_agents: number
}

export function RealTimeAgentMonitor() {
  const { user } = useAuth()
  const [agents, setAgents] = useState<AgentExecution[]>([])
  const [stats, setStats] = useState<AgentStats>({
    total_executions: 0,
    success_rate: 0,
    avg_execution_time: 0,
    total_cost: 0,
    active_agents: 0
  })
  const [selectedAgent, setSelectedAgent] = useState<AgentExecution | null>(null)
  const [filter, setFilter] = useState<'all' | 'running' | 'completed' | 'failed'>('all')

  const { client, isConnected, connectAgents } = useWebSocket({
    tenantId: user?.user.tenant_id || 'demo',
    userRole: user?.user.role || 'user',
    userId: user?.user.id || 'demo-user'
  })

  useEffect(() => {
    if (!client) return

    // Connect to agents WebSocket
    connectAgents?.()

    // Handle initial agent data
    const unsubscribeInitial = client.onMessage('initial_agent_data', (message) => {
      if (message.data) {
        setAgents(message.data.agents || [])
        setStats(message.data.stats || stats)
      }
    })

    // Handle agent execution updates
    const unsubscribeExecution = client.onMessage('agent_execution_update', (message) => {
      const agentData = message.data
      setAgents(prev => {
        const existingIndex = prev.findIndex(a => a.id === agentData.id)
        if (existingIndex >= 0) {
          const updated = [...prev]
          updated[existingIndex] = agentData
          return updated
        } else {
          return [agentData, ...prev]
        }
      })

      // Update selected agent if it matches
      if (selectedAgent?.id === agentData.id) {
        setSelectedAgent(agentData)
      }
    })

    // Handle agent stats updates
    const unsubscribeStats = client.onMessage('agent_stats_update', (message) => {
      setStats(message.data || stats)
    })

    // Handle new agent log entries
    const unsubscribeLog = client.onMessage('agent_log_update', (message) => {
      const { agent_id, log_entry } = message.data
      setAgents(prev => prev.map(agent => 
        agent.id === agent_id 
          ? { ...agent, logs: [log_entry, ...agent.logs.slice(0, 99)] } // Keep last 100 logs
          : agent
      ))

      if (selectedAgent?.id === agent_id) {
        setSelectedAgent(prev => prev ? {
          ...prev,
          logs: [log_entry, ...prev.logs.slice(0, 99)]
        } : null)
      }
    })

    return () => {
      unsubscribeInitial()
      unsubscribeExecution()
      unsubscribeStats()
      unsubscribeLog()
    }
  }, [client, connectAgents, selectedAgent?.id, stats])

  // Request initial data when connected
  useEffect(() => {
    if (isConnected && client) {
      client.requestUpdate('agent_status')
    }
  }, [isConnected, client])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return <Play className="h-4 w-4 text-blue-500" />
      case 'completed': return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'failed': return <XCircle className="h-4 w-4 text-red-500" />
      case 'paused': return <Pause className="h-4 w-4 text-yellow-500" />
      default: return <Clock className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-blue-500'
      case 'completed': return 'bg-green-500'
      case 'failed': return 'bg-red-500'
      case 'paused': return 'bg-yellow-500'
      default: return 'bg-gray-500'
    }
  }

  const filteredAgents = agents.filter(agent => 
    filter === 'all' || agent.status === filter
  )

  const handleAgentAction = (agentId: string, action: 'pause' | 'resume' | 'stop') => {
    if (client) {
      client.send({
        type: 'agent_control',
        agent_id: agentId,
        action: action
      })
    }
  }

  const formatDuration = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const remainingSeconds = seconds % 60
    
    if (hours > 0) {
      return `${hours}h ${minutes}m ${remainingSeconds}s`
    } else if (minutes > 0) {
      return `${minutes}m ${remainingSeconds}s`
    } else {
      return `${remainingSeconds}s`
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">AI Agent Monitor</h2>
        <div className="flex items-center space-x-2">
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
          <span className="text-sm text-muted-foreground">
            {isConnected ? 'Live' : 'Disconnected'}
          </span>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Agents</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.active_agents}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Executions</CardTitle>
            <Bot className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_executions}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.success_rate.toFixed(1)}%</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Execution</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatDuration(stats.avg_execution_time)}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Cost</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${stats.total_cost.toFixed(2)}</div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Agent List */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Agent Executions</CardTitle>
                <Tabs value={filter} onValueChange={(value: any) => setFilter(value)}>
                  <TabsList>
                    <TabsTrigger value="all">All</TabsTrigger>
                    <TabsTrigger value="running">Running</TabsTrigger>
                    <TabsTrigger value="completed">Completed</TabsTrigger>
                    <TabsTrigger value="failed">Failed</TabsTrigger>
                  </TabsList>
                </Tabs>
              </div>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-[600px]">
                <div className="space-y-4">
                  {filteredAgents.map((agent) => (
                    <div
                      key={agent.id}
                      className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                        selectedAgent?.id === agent.id ? 'bg-accent' : 'hover:bg-muted'
                      }`}
                      onClick={() => setSelectedAgent(agent)}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          {getStatusIcon(agent.status)}
                          <h3 className="font-medium">{agent.name}</h3>
                          <Badge variant="outline">{agent.category}</Badge>
                        </div>
                        <Badge variant="secondary" className="capitalize">
                          {agent.status}
                        </Badge>
                      </div>

                      {agent.status === 'running' && (
                        <div className="mb-2">
                          <div className="flex items-center justify-between text-sm mb-1">
                            <span>Progress</span>
                            <span>{agent.progress}%</span>
                          </div>
                          <Progress value={agent.progress} className="w-full" />
                        </div>
                      )}

                      <div className="flex items-center justify-between text-sm text-muted-foreground">
                        <span>Started: {new Date(agent.started_at).toLocaleTimeString()}</span>
                        {agent.metrics && (
                          <span>Cost: ${agent.metrics.cost_usd?.toFixed(4) || '0.0000'}</span>
                        )}
                      </div>

                      {agent.status === 'running' && user?.user.role === 'super_admin' && (
                        <div className="flex items-center space-x-2 mt-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={(e) => {
                              e.stopPropagation()
                              handleAgentAction(agent.id, 'pause')
                            }}
                          >
                            <Pause className="h-3 w-3" />
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={(e) => {
                              e.stopPropagation()
                              handleAgentAction(agent.id, 'stop')
                            }}
                          >
                            <Square className="h-3 w-3" />
                          </Button>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </div>

        {/* Agent Details */}
        <div>
          <Card>
            <CardHeader>
              <CardTitle>Agent Details</CardTitle>
            </CardHeader>
            <CardContent>
              {selectedAgent ? (
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium mb-2">{selectedAgent.name}</h4>
                    <div className="text-sm text-muted-foreground space-y-1">
                      <p>Category: {selectedAgent.category}</p>
                      <p>Status: {selectedAgent.status}</p>
                      <p>Started: {new Date(selectedAgent.started_at).toLocaleString()}</p>
                      {selectedAgent.completed_at && (
                        <p>Completed: {new Date(selectedAgent.completed_at).toLocaleString()}</p>
                      )}
                    </div>
                  </div>

                  {selectedAgent.metrics && (
                    <div>
                      <h5 className="font-medium mb-2">Performance Metrics</h5>
                      <div className="text-sm space-y-1">
                        <p>CPU Usage: {selectedAgent.metrics.cpu_usage.toFixed(1)}%</p>
                        <p>Memory: {selectedAgent.metrics.memory_usage.toFixed(1)} MB</p>
                        <p>Execution Time: {formatDuration(selectedAgent.metrics.execution_time)}</p>
                        {selectedAgent.metrics.tokens_used && (
                          <p>Tokens Used: {selectedAgent.metrics.tokens_used.toLocaleString()}</p>
                        )}
                        {selectedAgent.metrics.cost_usd && (
                          <p>Cost: ${selectedAgent.metrics.cost_usd.toFixed(4)}</p>
                        )}
                      </div>
                    </div>
                  )}

                  {selectedAgent.error_message && (
                    <div>
                      <h5 className="font-medium mb-2 text-red-600">Error Message</h5>
                      <p className="text-sm text-red-600 bg-red-50 p-2 rounded">
                        {selectedAgent.error_message}
                      </p>
                    </div>
                  )}

                  <div>
                    <h5 className="font-medium mb-2">Live Logs</h5>
                    <ScrollArea className="h-64 bg-muted p-2 rounded">
                      <div className="space-y-1">
                        {selectedAgent.logs.map((log, index) => (
                          <div key={index} className="text-xs">
                            <span className="text-muted-foreground">
                              {new Date(log.timestamp).toLocaleTimeString()}
                            </span>
                            <span className={`ml-2 ${
                              log.level === 'error' ? 'text-red-600' :
                              log.level === 'warning' ? 'text-yellow-600' :
                              'text-foreground'
                            }`}>
                              [{log.level.toUpperCase()}] {log.message}
                            </span>
                          </div>
                        ))}
                      </div>
                    </ScrollArea>
                  </div>
                </div>
              ) : (
                <p className="text-muted-foreground">Select an agent to view details</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}