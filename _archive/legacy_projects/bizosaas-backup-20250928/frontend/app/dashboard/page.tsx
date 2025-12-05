'use client'

import { Metadata } from 'next'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { 
  BarChart3, 
  Users, 
  TrendingUp, 
  Bot,
  ArrowUpRight,
  ArrowDownRight,
  Play,
  Pause,
  Settings,
  Activity,
  DollarSign,
  Target,
  CalendarDays,
  MessageCircle
} from 'lucide-react'
import WorkflowVisualization from '@/components/workflow-visualization'
import { useDashboardMetrics, useRealtimeMetrics } from '@/hooks/use-analytics'
import { useAgents } from '@/hooks/use-agents'
import { formatMetricValue, getMetricTrend } from '@/lib/api/analytics-api'
import { CalendarHub } from '@/components/calendar'
import { RealTimeAnalytics } from '@/components/analytics/real-time-analytics'
import { RealTimeAgentMonitor } from '@/components/agents/real-time-agent-monitor'
import { TenantMetricsStream } from '@/components/analytics/tenant-metrics-stream'
import { PrimaryAIInterface } from '@/components/chat/primary-ai-interface'
import { SimpleThemeSettings } from '@/components/theme/simple-theme-settings'
import WorkflowDesigner from '@/components/workflow/workflow-designer'
import AgentOrchestrationDashboard from '@/components/agents/agent-orchestration-dashboard'
import EnhancedSupersetDashboard from '@/components/analytics/enhanced-superset-dashboard'
import APIIntegrationManager from '@/components/integrations/api-integration-manager'
import MultiTenantNamespaceManager from '@/components/namespace/multi-tenant-namespace-manager'
import React, { useState } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { useAuth } from '@/lib/auth'

// AI Chat Component
function AIAssistantChat() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I can help you with platform insights. Try asking me about traffic, leads, or performance metrics.' }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return
    
    const userMessage = { role: 'user', content: inputMessage }
    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    // Simulate AI response based on query patterns
    let response = "I'm processing your request..."
    
    if (inputMessage.toLowerCase().includes('traffic')) {
      response = '📈 Your traffic today: 1,247 visitors (↑15% vs yesterday)\n\n• Direct: 45% (561 visitors)\n• Organic Search: 32% (399 visitors)\n• Social Media: 23% (287 visitors)'
    } else if (inputMessage.toLowerCase().includes('leads')) {
      response = '🎯 This month you\'ve generated 89 leads (↑22% vs last month)\n\n• Tier 1 ($97): 45 leads\n• Tier 2 ($297): 32 leads  \n• Tier 3 ($997): 12 leads'
    } else if (inputMessage.toLowerCase().includes('performance') || inputMessage.toLowerCase().includes('metrics')) {
      response = '⚡ Platform Performance Overview:\n\n• API Response Time: 145ms (Excellent)\n• AI Agents Active: 23/46 agents\n• Success Rate: 94.2%\n• Monthly Revenue: $45,678 (↑18%)'
    } else if (inputMessage.toLowerCase().includes('agents')) {
      response = '🤖 AI Agents Status:\n\n• Active: 23 agents\n• Working: 8 agents\n• Idle: 15 agents\n\nTop Performers:\n• Content Creator Agent (98% success)\n• SEO Optimizer Agent (96% success)\n• Social Media Agent (94% success)'
    }

    setTimeout(() => {
      setMessages(prev => [...prev, { role: 'assistant', content: response }])
      setIsLoading(false)
    }, 1500)
  }

  return (
    <div className="flex flex-col h-96 border rounded-lg">
      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {messages.map((message, index) => (
          <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
              message.role === 'user' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-100 text-gray-900'
            }`}>
              <div className="whitespace-pre-wrap text-sm">{message.content}</div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-900 px-4 py-2 rounded-lg">
              <div className="animate-pulse">Processing...</div>
            </div>
          </div>
        )}
      </div>
      
      <div className="p-4 border-t">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Ask about traffic, leads, performance..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm"
          />
          <Button onClick={handleSendMessage} disabled={isLoading}>
            <MessageCircle className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}

// AI Agents Management Component  
function AIAgentsManagement() {
  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {[
          { name: 'Content Creator', status: 'active', performance: 98, tasks: 12 },
          { name: 'SEO Optimizer', status: 'working', performance: 96, tasks: 8 },
          { name: 'Social Media Manager', status: 'active', performance: 94, tasks: 15 },
          { name: 'Lead Generator', status: 'working', performance: 92, tasks: 6 },
          { name: 'Campaign Analyzer', status: 'idle', performance: 89, tasks: 0 },
          { name: 'Competitor Research', status: 'active', performance: 87, tasks: 4 }
        ].map((agent, index) => (
          <Card key={index}>
            <CardContent className="p-4">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-medium">{agent.name}</h3>
                <div className={`w-2 h-2 rounded-full ${
                  agent.status === 'active' ? 'bg-green-500' : 
                  agent.status === 'working' ? 'bg-blue-500 animate-pulse' :
                  'bg-gray-400'
                }`} />
              </div>
              <div className="text-sm text-muted-foreground mb-2">
                {agent.status === 'working' ? 'Currently working...' : 
                 agent.status === 'active' ? 'Ready for tasks' :
                 'Idle - Waiting for activation'}
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm">Performance: {agent.performance}%</span>
                <Badge variant="outline" className="text-xs">
                  {agent.tasks} tasks
                </Badge>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}





export default function DashboardPage() {
  // Authentication hook
  const { user, isLoading: authLoading } = useAuth()
  const isAuthenticated = !!user
  
  // Live data hooks
  const { metrics, loading: metricsLoading, error: metricsError } = useDashboardMetrics('7d')
  const { metrics: realtimeMetrics, connected } = useRealtimeMetrics()
  const { agents, loading: agentsLoading } = useAgents({ autoRefresh: true })
  
  // Tab state - Default to AI Command Center
  const [activeTab, setActiveTab] = useState('ai-command')

  // Calculate dynamic stats from live data
  const stats = [
    {
      title: 'Monthly Revenue',
      value: metrics ? formatMetricValue(metrics.overview.monthlyRevenue, 'currency') : '...',
      change: metrics ? `${metrics.overview.revenueGrowth > 0 ? '+' : ''}${metrics.overview.revenueGrowth.toFixed(1)}% from last month` : 'Loading...',
      trend: metrics ? (metrics.overview.revenueGrowth > 0 ? 'up' : 'down') : 'neutral',
      icon: DollarSign,
      color: 'text-green-600',
    },
    {
      title: 'Total Leads',
      value: metrics ? metrics.leads.totalLeads.toLocaleString() : '...',
      change: metrics ? `+${metrics.leads.newLeadsToday} today` : 'Loading...',
      trend: 'up',
      icon: Users,
      color: 'text-blue-600',
    },
    {
      title: 'Conversion Rate',
      value: metrics ? `${metrics.overview.conversionRate}%` : '...',
      change: metrics ? `${metrics.leads.convertedLeads} converted this month` : 'Loading...',
      trend: 'up',
      icon: Target,
      color: 'text-purple-600',
    },
    {
      title: 'AI Agents Active',
      value: agents.filter(a => a.status === 'active').length.toString(),
      change: `${agents.filter(a => a.status === 'working').length} currently working`,
      trend: 'neutral',
      icon: Bot,
      color: 'text-orange-600',
    },
  ]

  const activeAgents = agents.filter(a => a.status === 'active' || a.status === 'working')
  const topCampaigns = metrics?.campaigns.topPerformingCampaigns || []

  // Handle loading states
  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-lg text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  // Handle authentication
  if (!isAuthenticated) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-600">Authentication Required</h2>
          <p className="mt-2 text-muted-foreground">Please log in to access the dashboard.</p>
        </div>
      </div>
    )
  }

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-8">
      {/* Tab Navigation */}
      <div className="border-b">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold">Dashboard Overview</h1>
            <p className="text-muted-foreground">
              Traditional dashboard view - Try the <span className="text-blue-600 font-medium">🤖 AI Command Center</span> tab for natural language control!
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="flex items-center space-x-2">
              {realtimeMetrics && (
                <Badge variant="outline" className="text-blue-600 border-blue-600">
                  <Activity className="w-3 h-3 mr-1" />
                  {realtimeMetrics.currentUsers} users online
                </Badge>
              )}
              <Badge 
                variant="outline" 
                className={connected ? "text-green-600 border-green-600" : "text-yellow-600 border-yellow-600"}
              >
                {connected ? 'Live Data Connected' : 'Using Cached Data'}
              </Badge>
            </div>
            <Button size="sm">
              <Settings className="w-4 h-4 mr-2" />
              Configure
            </Button>
          </div>
        </div>
        
        <TabsList className="grid w-full max-w-7xl grid-cols-12 gap-1">
          <TabsTrigger value="ai-command" className="bg-gradient-to-r from-blue-500 to-purple-600 text-white border border-blue-300 col-span-2">
            🤖 AI Command
          </TabsTrigger>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="workflow-designer">📊 Workflows</TabsTrigger>
          <TabsTrigger value="agent-orchestration">🤖 Agents</TabsTrigger>
          <TabsTrigger value="analytics-superset">📈 Analytics</TabsTrigger>
          <TabsTrigger value="api-integrations">🔗 APIs</TabsTrigger>
          <TabsTrigger value="namespace-manager">🏢 Namespaces</TabsTrigger>
          <TabsTrigger value="realtime">Live Data</TabsTrigger>
          <TabsTrigger value="tenant-metrics">Tenants</TabsTrigger>
          <TabsTrigger value="calendar">Calendar</TabsTrigger>
          <TabsTrigger value="ai-chat">AI Chat</TabsTrigger>
          <TabsTrigger value="theme-settings">🎨 Themes</TabsTrigger>
        </TabsList>
      </div>

      {/* Primary AI Command Center Tab */}
      <TabsContent value="ai-command" className="space-y-6">
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg border border-blue-200">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-2xl font-bold text-blue-900">🤖 AI Command Center</h2>
              <p className="text-blue-700">
                Your primary admin interface - manage everything through natural language
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant="default" className="bg-green-500">
                Primary Interface
              </Badge>
              <Badge variant={connected ? "default" : "secondary"}>
                {connected ? 'Live Connected' : 'Offline Mode'}
              </Badge>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-sm h-[600px]">
            <PrimaryAIInterface onTabNavigate={setActiveTab} />
          </div>
        </div>
      </TabsContent>

      {/* Overview Tab */}
      <TabsContent value="overview" className="space-y-8">
        {/* Real-time connection status banner */}
        {!connected && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-yellow-800">
                Real-time connection unavailable. Showing cached data.
              </span>
            </div>
          </div>
        )}

      {/* Stats Grid */}
      <div className="grid gap-4 md:gap-6 md:grid-cols-2 lg:grid-cols-4">
        {metricsError && (
          <div className="col-span-full mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-600 text-sm">Error loading dashboard metrics: {metricsError}</p>
          </div>
        )}
        {stats.map((stat, index) => (
          <Card key={index} className="hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {stat.title}
              </CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {metricsLoading ? (
                  <div className="animate-pulse bg-gray-200 h-6 w-16 rounded"></div>
                ) : (
                  stat.value
                )}
              </div>
              <div className="flex items-center text-sm text-muted-foreground">
                {stat.trend === 'up' && <ArrowUpRight className="h-4 w-4 text-green-600 mr-1" />}
                {stat.trend === 'down' && <ArrowDownRight className="h-4 w-4 text-red-600 mr-1" />}
                <span>{stat.change}</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Top Performing Campaigns */}
        <Card>
          <CardHeader>
            <CardTitle>Top Performing Campaigns</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {metricsLoading ? (
                [...Array(3)].map((_, i) => (
                  <div key={i} className="animate-pulse">
                    <div className="h-16 bg-gray-200 rounded-lg"></div>
                  </div>
                ))
              ) : (
                topCampaigns.slice(0, 3).map((campaign, index) => (
                  <div key={campaign.id || index} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="flex items-center space-x-2">
                        <Play className="h-4 w-4 text-green-600" />
                        <Badge 
                          variant={campaign.ctr > 3 ? 'default' : campaign.ctr > 2 ? 'secondary' : 'outline'}
                          className="text-xs"
                        >
                          {campaign.ctr > 3 ? 'high' : campaign.ctr > 2 ? 'medium' : 'low'} CTR
                        </Badge>
                      </div>
                    </div>
                    <div className="flex-1 ml-4">
                      <div className="font-medium">{campaign.name}</div>
                      <div className="text-sm text-muted-foreground">
                        {campaign.ctr.toFixed(1)}% CTR • {campaign.impressions.toLocaleString()} impressions
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-medium">{campaign.conversions} conversions</div>
                      <div className="text-sm text-muted-foreground">{formatMetricValue(campaign.cost, 'currency')}</div>
                    </div>
                  </div>
                ))
              )}
              {!metricsLoading && topCampaigns.length === 0 && (
                <div className="text-center py-8 text-muted-foreground">
                  <BarChart3 className="h-12 w-12 mx-auto mb-4" />
                  <p>No campaign data available</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* AI Agents Status */}
        <Card>
          <CardHeader>
            <CardTitle>AI Agents Status</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {agentsLoading ? (
                [...Array(4)].map((_, i) => (
                  <div key={i} className="animate-pulse">
                    <div className="h-16 bg-gray-200 rounded-lg"></div>
                  </div>
                ))
              ) : (
                activeAgents.slice(0, 4).map((agent, index) => (
                  <div key={agent.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className={`w-2 h-2 rounded-full ${
                        agent.status === 'active' ? 'bg-green-500' : 
                        agent.status === 'working' ? 'bg-blue-500 animate-pulse' :
                        agent.status === 'idle' ? 'bg-yellow-500' : 'bg-gray-400'
                      }`} />
                      <div>
                        <div className="font-medium">{agent.name}</div>
                        <div className="text-sm text-muted-foreground">
                          {agent.status === 'working' ? 'Currently working...' : 
                           agent.status === 'active' ? 'Ready for tasks' :
                           'Waiting for activation'}
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <Badge variant="outline" className="text-xs">
                        {agent.performance}% performance
                      </Badge>
                    </div>
                  </div>
                ))
              )}
              {!agentsLoading && activeAgents.length === 0 && (
                <div className="text-center py-8 text-muted-foreground">
                  <Bot className="h-12 w-12 mx-auto mb-4" />
                  <p>No active agents</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Real-Time Workflow Visualization */}
      <div className="space-y-6">
        <WorkflowVisualization
          platform="bizoholic"
          workflowType="marketing_campaign"
          autoStart={false}
          height="500px"
          showControls={true}
          showMetrics={true}
          className="lg:col-span-2"
        />
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Button variant="outline" className="h-24 flex flex-col items-center justify-center hover:bg-primary/5">
              <BarChart3 className="h-6 w-6 mb-2" />
              New Campaign
            </Button>
            <Button variant="outline" className="h-24 flex flex-col items-center justify-center hover:bg-primary/5">
              <Users className="h-6 w-6 mb-2" />
              Import Leads
            </Button>
            <Button variant="outline" className="h-24 flex flex-col items-center justify-center hover:bg-primary/5">
              <Bot className="h-6 w-6 mb-2" />
              Train AI Agent
            </Button>
            <Button variant="outline" className="h-24 flex flex-col items-center justify-center hover:bg-primary/5">
              <TrendingUp className="h-6 w-6 mb-2" />
              View Reports
            </Button>
          </div>
        </CardContent>
      </Card>
      </TabsContent>

      {/* Real-Time Analytics Tab */}
      <TabsContent value="realtime" className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">Live Dashboard Analytics</h2>
            <p className="text-muted-foreground">
              Real-time metrics, agent activity, and platform performance monitoring.
            </p>
          </div>
          <Badge variant={connected ? "default" : "secondary"}>
            {connected ? 'Live Data' : 'Cached Data'}
          </Badge>
        </div>
        
        <RealTimeAnalytics />
      </TabsContent>

      {/* Real-Time Agent Monitor Tab */}
      <TabsContent value="agents-monitor" className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">AI Agents Live Monitor</h2>
            <p className="text-muted-foreground">
              Monitor AI agent executions, performance metrics, and real-time logs.
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <Badge variant={connected ? "default" : "secondary"}>
              {connected ? 'Live Monitoring' : 'Offline Mode'}
            </Badge>
            <Button size="sm">
              <Bot className="w-4 h-4 mr-2" />
              Launch Agent
            </Button>
          </div>
        </div>
        
        <RealTimeAgentMonitor />
      </TabsContent>

      {/* Tenant Metrics Stream Tab */}
      <TabsContent value="tenant-metrics" className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">Tenant Metrics Stream</h2>
            <p className="text-muted-foreground">
              Live tenant-specific metrics and cross-tenant performance comparison.
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <Badge variant={connected ? "default" : "secondary"}>
              {connected ? 'Live Streaming' : 'Offline Mode'}
            </Badge>
            <Button size="sm">
              <Activity className="w-4 h-4 mr-2" />
              Configure Metrics
            </Button>
          </div>
        </div>
        
        <TenantMetricsStream 
          role="admin"
          allowedTenants={['demo']}
          defaultView="overview"
        />
      </TabsContent>

      {/* Calendar Tab */}
      <TabsContent value="calendar" className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">Calendar Hub</h2>
            <p className="text-muted-foreground">
              Manage campaigns, AI agent schedules, client meetings, and maintenance windows.
            </p>
          </div>
          <Button size="sm">
            <CalendarDays className="w-4 h-4 mr-2" />
            Sync Calendar
          </Button>
        </div>
        
        <CalendarHub tenantId="demo-tenant" userRole="admin" />
      </TabsContent>

      {/* AI Chat Tab */}
      <TabsContent value="ai-chat" className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">AI Assistant Chat</h2>
            <p className="text-muted-foreground">
              Chat with your AI assistant for real-time insights and platform management.
            </p>
          </div>
          <Button size="sm">
            <MessageCircle className="w-4 h-4 mr-2" />
            New Conversation
          </Button>
        </div>
        
        <AIAssistantChat />
      </TabsContent>

      {/* Workflow Designer Tab */}
      <TabsContent value="workflow-designer" className="space-y-6">
        <WorkflowDesigner />
      </TabsContent>

      {/* Agent Orchestration Tab */}
      <TabsContent value="agent-orchestration" className="space-y-6">
        <AgentOrchestrationDashboard />
      </TabsContent>

      {/* Enhanced Analytics Tab */}
      <TabsContent value="analytics-superset" className="space-y-6">
        <EnhancedSupersetDashboard />
      </TabsContent>

      {/* API Integration Manager Tab */}
      <TabsContent value="api-integrations" className="space-y-6">
        <APIIntegrationManager />
      </TabsContent>

      {/* Namespace Manager Tab */}
      <TabsContent value="namespace-manager" className="space-y-6">
        <MultiTenantNamespaceManager />
      </TabsContent>

      {/* Theme Settings Tab */}
      <TabsContent value="theme-settings" className="space-y-6">
        <SimpleThemeSettings />
      </TabsContent>
    </Tabs>
  )
}