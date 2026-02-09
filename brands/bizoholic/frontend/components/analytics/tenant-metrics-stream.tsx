"use client"

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts'
import {
  Activity, Users, Bot, TrendingUp, DollarSign,
  Target, Zap, Clock, CheckCircle, AlertTriangle,
  Eye, MousePointer, ShoppingCart, UserPlus
} from 'lucide-react'
import { useWebSocket } from '@/lib/websocket-client'
import { useAuth } from '@/hooks/use-auth'

interface TenantMetric {
  id: string
  name: string
  value: number | string
  change: number
  trend: 'up' | 'down' | 'neutral'
  formatted_value: string
  timestamp: string
  category: 'revenue' | 'traffic' | 'conversions' | 'agents' | 'campaigns'
}

interface UserActivity {
  user_id: string
  user_name: string
  action: string
  resource: string
  timestamp: string
  ip_address?: string
  user_agent?: string
}

interface CampaignMetric {
  campaign_id: string
  campaign_name: string
  impressions: number
  clicks: number
  conversions: number
  cost: number
  ctr: number
  conversion_rate: number
  roas: number
  status: 'active' | 'paused' | 'completed'
}

interface TenantLiveData {
  tenant_id: string
  tenant_name: string
  metrics: TenantMetric[]
  user_activities: UserActivity[]
  campaigns: CampaignMetric[]
  chart_data: {
    revenue: Array<{ time: string, value: number }>
    traffic: Array<{ time: string, sessions: number, users: number }>
    conversions: Array<{ time: string, leads: number, sales: number }>
  }
  agent_performance: Array<{
    agent_id: string
    agent_name: string
    success_rate: number
    tasks_completed: number
    avg_response_time: number
  }>
}

interface TenantMetricsStreamProps {
  role?: string
  allowedTenants?: string[]
  defaultView?: 'overview' | 'detailed' | 'comparison'
}

export function TenantMetricsStream({
  role = 'tenant_admin',
  allowedTenants = [],
  defaultView = 'overview'
}: TenantMetricsStreamProps) {
  const { user } = useAuth()
  const [tenantData, setTenantData] = useState<Record<string, TenantLiveData>>({})
  const [selectedTenant, setSelectedTenant] = useState<string>('')
  const [activeView, setActiveView] = useState(defaultView)
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting')

  const { client, isConnected, connectDashboard } = useWebSocket({
    tenantId: user?.tenant_id || 'demo',
    userRole: user?.role || role,
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

    // Handle tenant metrics updates
    const unsubscribeMetrics = client.onMessage('tenant_metrics_update', (message) => {
      const { tenant_id, data } = message.data
      setTenantData(prev => ({
        ...prev,
        [tenant_id]: {
          ...prev[tenant_id],
          ...data
        }
      }))
    })

    // Handle real-time user activities
    const unsubscribeActivity = client.onMessage('user_activity_stream', (message) => {
      const { tenant_id, activity } = message.data
      setTenantData(prev => ({
        ...prev,
        [tenant_id]: {
          ...prev[tenant_id],
          user_activities: [activity, ...(prev[tenant_id]?.user_activities || []).slice(0, 49)]
        }
      }))
    })

    // Handle campaign metrics updates
    const unsubscribeCampaigns = client.onMessage('campaign_metrics_stream', (message) => {
      const { tenant_id, campaigns } = message.data
      setTenantData(prev => ({
        ...prev,
        [tenant_id]: {
          ...prev[tenant_id],
          campaigns: campaigns
        }
      }))
    })

    // Handle multi-tenant overview (for super admins)
    const unsubscribeOverview = client.onMessage('multi_tenant_overview', (message) => {
      setTenantData(message.data || {})
    })

    return () => {
      unsubscribeConnection()
      unsubscribeMetrics()
      unsubscribeActivity()
      unsubscribeCampaigns()
      unsubscribeOverview()
    }
  }, [client, connectDashboard])

  // Auto-select first available tenant
  useEffect(() => {
    const availableTenants = Object.keys(tenantData)
    if (availableTenants.length > 0 && !selectedTenant) {
      setSelectedTenant(availableTenants[0])
    }
  }, [tenantData, selectedTenant])

  // Request tenant-specific data when connected
  useEffect(() => {
    if (isConnected && client) {
      if (role === 'super_admin') {
        client.send({
          type: 'subscribe_multi_tenant_metrics',
          allowed_tenants: allowedTenants
        })
      } else {
        client.requestUpdate('tenant_metrics')
      }
    }
  }, [isConnected, client, role, allowedTenants])

  const getMetricIcon = (category: string) => {
    switch (category) {
      case 'revenue': return DollarSign
      case 'traffic': return Eye
      case 'conversions': return Target
      case 'agents': return Bot
      case 'campaigns': return Zap
      default: return Activity
    }
  }

  const getMetricColor = (trend: string) => {
    switch (trend) {
      case 'up': return 'text-green-600'
      case 'down': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  const formatChange = (change: number) => {
    const sign = change >= 0 ? '+' : ''
    return `${sign}${change}%`
  }

  const currentTenantData = selectedTenant ? tenantData[selectedTenant] : null

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Live Tenant Metrics</h2>
          <p className="text-muted-foreground">
            Real-time performance metrics and user activity across tenants
          </p>
        </div>
        <div className="flex items-center space-x-2">
          {/* Tenant Selector for Super Admins */}
          {role === 'super_admin' && Object.keys(tenantData).length > 1 && (
            <select
              value={selectedTenant}
              onChange={(e) => setSelectedTenant(e.target.value)}
              className="px-3 py-2 border rounded-md text-sm"
            >
              {Object.entries(tenantData).map(([tenantId, data]) => (
                <option key={tenantId} value={tenantId}>
                  {data.tenant_name || tenantId}
                </option>
              ))}
            </select>
          )}
          <div className={`w-3 h-3 rounded-full ${connectionStatus === 'connected' ? 'bg-green-500' :
            connectionStatus === 'connecting' ? 'bg-yellow-500' : 'bg-red-500'
            }`} />
          <span className="text-sm text-muted-foreground capitalize">
            {connectionStatus}
          </span>
        </div>
      </div>

      {!currentTenantData ? (
        <Card>
          <CardContent className="flex items-center justify-center h-64">
            <div className="text-center">
              <Activity className="h-8 w-8 mx-auto mb-4 text-muted-foreground" />
              <p className="text-muted-foreground">
                {connectionStatus === 'connected' ? 'Waiting for tenant data...' : 'Connecting to live data stream...'}
              </p>
            </div>
          </CardContent>
        </Card>
      ) : (
        <Tabs value={activeView} onValueChange={(value) => setActiveView(value as any)}>
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="detailed">Detailed Metrics</TabsTrigger>
            <TabsTrigger value="activity">User Activity</TabsTrigger>
            <TabsTrigger value="campaigns">Campaigns</TabsTrigger>
            {role === 'super_admin' && <TabsTrigger value="comparison">Compare Tenants</TabsTrigger>}
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            {/* Key Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {currentTenantData.metrics?.map((metric, index) => {
                const Icon = getMetricIcon(metric.category)
                return (
                  <Card key={metric.id}>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium">{metric.name}</CardTitle>
                      <Icon className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">{metric.formatted_value}</div>
                      <p className={`text-xs ${getMetricColor(metric.trend)}`}>
                        {formatChange(metric.change)} from last hour
                      </p>
                    </CardContent>
                  </Card>
                )
              })}
            </div>

            {/* Charts Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Revenue Chart */}
              <Card>
                <CardHeader>
                  <CardTitle>Revenue Trend</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={currentTenantData.chart_data?.revenue || []}>
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
                      <Line type="monotone" dataKey="value" stroke="#10b981" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Traffic Chart */}
              <Card>
                <CardHeader>
                  <CardTitle>Traffic Overview</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={currentTenantData.chart_data?.traffic || []}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis
                        dataKey="time"
                        tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                      />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="sessions" fill="#3b82f6" name="Sessions" />
                      <Bar dataKey="users" fill="#8b5cf6" name="Users" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>

            {/* Agent Performance */}
            <Card>
              <CardHeader>
                <CardTitle>AI Agent Performance</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {currentTenantData.agent_performance?.map((agent) => (
                    <div key={agent.agent_id} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center space-x-3">
                        <Bot className="h-4 w-4 text-blue-500" />
                        <div>
                          <p className="font-medium">{agent.agent_name}</p>
                          <p className="text-sm text-muted-foreground">
                            {agent.tasks_completed} tasks completed
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="font-medium">{agent.success_rate}% success rate</p>
                        <p className="text-sm text-muted-foreground">
                          {agent.avg_response_time}ms avg response
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Detailed Metrics Tab */}
          <TabsContent value="detailed" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <Card className="lg:col-span-2">
                <CardHeader>
                  <CardTitle>Conversion Funnel</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={400}>
                    <LineChart data={currentTenantData.chart_data?.conversions || []}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Line type="monotone" dataKey="leads" stroke="#f59e0b" name="Leads" />
                      <Line type="monotone" dataKey="sales" stroke="#10b981" name="Sales" />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Metric Categories</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {['revenue', 'traffic', 'conversions', 'agents'].map((category) => {
                      const categoryMetrics = currentTenantData.metrics?.filter(m => m.category === category) || []
                      return (
                        <div key={category} className="p-3 border rounded-lg">
                          <h4 className="font-medium capitalize mb-2">{category}</h4>
                          <div className="space-y-1">
                            {categoryMetrics.map((metric) => (
                              <div key={metric.id} className="flex justify-between text-sm">
                                <span>{metric.name}</span>
                                <span className="font-medium">{metric.formatted_value}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* User Activity Tab */}
          <TabsContent value="activity" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Live User Activity Stream</CardTitle>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-96">
                  <div className="space-y-4">
                    {currentTenantData.user_activities?.map((activity, index) => (
                      <div key={index} className="flex items-start space-x-3 p-3 border rounded-lg">
                        <UserPlus className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium">
                            {activity.user_name} {activity.action} {activity.resource}
                          </p>
                          <div className="flex items-center justify-between mt-1">
                            <p className="text-xs text-muted-foreground">
                              {activity.ip_address && `from ${activity.ip_address}`}
                            </p>
                            <p className="text-xs text-muted-foreground">
                              {new Date(activity.timestamp).toLocaleTimeString()}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                    {!currentTenantData.user_activities?.length && (
                      <p className="text-center text-muted-foreground py-8">
                        No recent user activities
                      </p>
                    )}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Campaigns Tab */}
          <TabsContent value="campaigns" className="space-y-6">
            <div className="grid gap-6">
              {currentTenantData.campaigns?.map((campaign) => (
                <Card key={campaign.campaign_id}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle>{campaign.campaign_name}</CardTitle>
                      <Badge variant={campaign.status === 'active' ? 'default' : 'secondary'}>
                        {campaign.status}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 lg:grid-cols-6 gap-4">
                      <div>
                        <p className="text-sm text-muted-foreground">Impressions</p>
                        <p className="font-medium">{campaign.impressions.toLocaleString()}</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">Clicks</p>
                        <p className="font-medium">{campaign.clicks.toLocaleString()}</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">CTR</p>
                        <p className="font-medium">{campaign.ctr.toFixed(2)}%</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">Conversions</p>
                        <p className="font-medium">{campaign.conversions}</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">Conv. Rate</p>
                        <p className="font-medium">{campaign.conversion_rate.toFixed(2)}%</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">ROAS</p>
                        <p className="font-medium">{campaign.roas.toFixed(2)}x</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Tenant Comparison Tab (Super Admin Only) */}
          {role === 'super_admin' && (
            <TabsContent value="comparison" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Tenant Performance Comparison</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    {Object.entries(tenantData).map(([tenantId, data]) => (
                      <div key={tenantId} className="p-4 border rounded-lg">
                        <h4 className="font-medium mb-4">{data.tenant_name || tenantId}</h4>
                        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                          {data.metrics?.slice(0, 4).map((metric) => (
                            <div key={metric.id}>
                              <p className="text-sm text-muted-foreground">{metric.name}</p>
                              <p className="font-medium">{metric.formatted_value}</p>
                              <p className={`text-xs ${getMetricColor(metric.trend)}`}>
                                {formatChange(metric.change)}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          )}
        </Tabs>
      )}
    </div>
  )
}