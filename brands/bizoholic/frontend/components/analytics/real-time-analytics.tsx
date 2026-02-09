"use client"

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Activity, Users, Bot, TrendingUp, AlertCircle } from 'lucide-react'
import { useWebSocket } from '@/lib/websocket-client'
import { useAuth } from '@/hooks/use-auth'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'

interface RealTimeMetric {
  name: string
  value: number | string
  change: number
  timestamp: string
}

interface AgentExecution {
  id: string
  name: string
  status: 'running' | 'completed' | 'failed'
  progress?: number
  tenant_id: string
  started_at: string
  completed_at?: string
}

interface LiveData {
  metrics: RealTimeMetric[]
  agents: AgentExecution[]
  activities: Array<{
    type: string
    message: string
    timestamp: string
    user?: string
  }>
  chart_data: Array<{
    time: string
    active_agents: number
    completed_tasks: number
    revenue: number
  }>
}

export function RealTimeAnalytics() {
  const { user } = useAuth()
  const [liveData, setLiveData] = useState<LiveData>({
    metrics: [],
    agents: [],
    activities: [],
    chart_data: []
  })
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting')

  const { client, isConnected, connectDashboard } = useWebSocket({
    tenantId: user?.tenant_id || 'demo',
    userRole: user?.role || 'user',
    userId: user?.id || 'demo-user'
  })

  useEffect(() => {
    if (!client) return

    // Connect to dashboard WebSocket
    connectDashboard?.()

    // Handle connection status
    const unsubscribeConnection = client.onConnection((connected) => {
      setConnectionStatus(connected ? 'connected' : 'disconnected')
    })

    // Handle initial dashboard data
    const unsubscribeInitial = client.onMessage('initial_dashboard_data', (message) => {
      if (message.data) {
        setLiveData(message.data)
      }
    })

    // Handle real-time metric updates
    const unsubscribeMetrics = client.onMessage('metrics_update', (message) => {
      setLiveData(prev => ({
        ...prev,
        metrics: message.data || prev.metrics
      }))
    })

    // Handle agent status updates
    const unsubscribeAgents = client.onMessage('agent_status_update', (message) => {
      setLiveData(prev => ({
        ...prev,
        agents: prev.agents.map(agent =>
          agent.id === message.agent_id
            ? { ...agent, ...message.data }
            : agent
        )
      }))
    })

    // Handle new activity notifications
    const unsubscribeActivity = client.onMessage('activity_notification', (message) => {
      setLiveData(prev => ({
        ...prev,
        activities: [message.data, ...prev.activities.slice(0, 9)] // Keep last 10 activities
      }))
    })

    // Handle chart data updates
    const unsubscribeChart = client.onMessage('chart_data_update', (message) => {
      setLiveData(prev => ({
        ...prev,
        chart_data: message.data || prev.chart_data
      }))
    })

    return () => {
      unsubscribeConnection()
      unsubscribeInitial()
      unsubscribeMetrics()
      unsubscribeAgents()
      unsubscribeActivity()
      unsubscribeChart()
    }
  }, [client, connectDashboard])

  // Request initial data when connected
  useEffect(() => {
    if (isConnected && client) {
      client.requestUpdate('dashboard_overview')
    }
  }, [isConnected, client])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-blue-500'
      case 'completed': return 'bg-green-500'
      case 'failed': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  const formatChange = (change: number) => {
    const sign = change >= 0 ? '+' : ''
    return `${sign}${change}%`
  }

  return (
    <div className="space-y-6">
      {/* Connection Status */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Real-Time Analytics</h2>
        <div className="flex items-center space-x-2">
          <div className={`w-3 h-3 rounded-full ${connectionStatus === 'connected' ? 'bg-green-500' :
              connectionStatus === 'connecting' ? 'bg-yellow-500' : 'bg-red-500'
            }`} />
          <span className="text-sm text-muted-foreground capitalize">
            {connectionStatus}
          </span>
        </div>
      </div>

      {/* Real-Time Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {liveData.metrics.map((metric, index) => (
          <Card key={metric.name}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{metric.name}</CardTitle>
              {index === 0 && <Activity className="h-4 w-4 text-muted-foreground" />}
              {index === 1 && <Users className="h-4 w-4 text-muted-foreground" />}
              {index === 2 && <Bot className="h-4 w-4 text-muted-foreground" />}
              {index === 3 && <TrendingUp className="h-4 w-4 text-muted-foreground" />}
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{metric.value}</div>
              <p className={`text-xs ${metric.change >= 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                {formatChange(metric.change)} from last hour
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Real-Time Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Live Activity Metrics</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={liveData.chart_data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="time"
                  tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                />
                <YAxis />
                <Tooltip
                  labelFormatter={(value) => new Date(value).toLocaleTimeString()}
                />
                <Line
                  type="monotone"
                  dataKey="active_agents"
                  stroke="#8884d8"
                  strokeWidth={2}
                  name="Active Agents"
                />
                <Line
                  type="monotone"
                  dataKey="completed_tasks"
                  stroke="#82ca9d"
                  strokeWidth={2}
                  name="Completed Tasks"
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Revenue Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Revenue Tracking</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={liveData.chart_data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="time"
                  tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                />
                <YAxis />
                <Tooltip
                  labelFormatter={(value) => new Date(value).toLocaleTimeString()}
                  formatter={(value) => [`$${value}`, 'Revenue']}
                />
                <Bar dataKey="revenue" fill="#f59e0b" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Active AI Agents */}
        <Card>
          <CardHeader>
            <CardTitle>Active AI Agents</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {liveData.agents.length === 0 ? (
                <p className="text-muted-foreground">No active agents</p>
              ) : (
                liveData.agents.map((agent) => (
                  <div key={agent.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className={`w-3 h-3 rounded-full ${getStatusColor(agent.status)}`} />
                      <div>
                        <p className="font-medium">{agent.name}</p>
                        <p className="text-sm text-muted-foreground">
                          Started: {new Date(agent.started_at).toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <Badge variant="outline" className="capitalize">
                        {agent.status}
                      </Badge>
                      {agent.progress && (
                        <p className="text-sm text-muted-foreground mt-1">
                          {agent.progress}% complete
                        </p>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>

        {/* Live Activity Feed */}
        <Card>
          <CardHeader>
            <CardTitle>Live Activity Feed</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {liveData.activities.length === 0 ? (
                <p className="text-muted-foreground">No recent activities</p>
              ) : (
                liveData.activities.map((activity, index) => (
                  <div key={index} className="flex items-start space-x-3 p-3 border rounded-lg">
                    <AlertCircle className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium">{activity.message}</p>
                      <div className="flex items-center justify-between mt-1">
                        <p className="text-xs text-muted-foreground">
                          {activity.user && `by ${activity.user}`}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {new Date(activity.timestamp).toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}