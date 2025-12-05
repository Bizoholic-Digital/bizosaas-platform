'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
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
  MessageCircle,
  Zap,
  Clock,
  CheckCircle
} from 'lucide-react'

// Import components
import { CalendarHub } from '@/components/calendar'
import WorkflowVisualization from '@/components/workflow-visualization'
import { useDashboardMetrics, useRealtimeMetrics } from '@/hooks/use-analytics'
import { useAgents } from '@/hooks/use-agents'
import { useApiGatewayDashboard } from '@/hooks/use-api-gateway'
import { useAIAgentsData } from '@/hooks/use-ai-agents-live'
import { formatMetricValue, getMetricTrend } from '@/lib/api/analytics-api'

// AI Chat Interface Component
function AIAssistantChat() {
  const [messages, setMessages] = useState([
    {
      id: '1',
      type: 'assistant',
      content: 'Hi! I\'m your AI assistant. You can ask me about your traffic, performance, leads, and more. Try asking: "What\'s my traffic today?" or "How many leads this month?"',
      timestamp: new Date()
    }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return

    const newMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    }

    setMessages([...messages, newMessage])
    setInputMessage('')
    setIsTyping(true)

    // Simulate AI response based on query patterns
    setTimeout(() => {
      let response = 'I understand your question. Let me check that for you...'
      
      if (inputMessage.toLowerCase().includes('traffic')) {
        response = '📈 Your traffic today: 1,247 visitors (↑15% vs yesterday). Top sources: Google Organic (45%), Direct (25%), Social Media (18%).'
      } else if (inputMessage.toLowerCase().includes('leads')) {
        response = '🎯 This month you\'ve generated 89 leads (↑22% vs last month). Top performing campaigns: "Summer Sale" (34 leads), "SEO Content" (28 leads).'
      } else if (inputMessage.toLowerCase().includes('performance')) {
        response = '⚡ Platform performance: All systems operational. AI Agents: 12 active, API Response time: 245ms, Uptime: 99.8%.'
      } else if (inputMessage.toLowerCase().includes('revenue') || inputMessage.toLowerCase().includes('sales')) {
        response = '💰 Revenue this month: $12,450 (↑18% vs last month). MRR: $8,200. Top tier: Tier 3 clients contributing 65% of revenue.'
      } else if (inputMessage.toLowerCase().includes('agents')) {
        response = '🤖 AI Agents status: 12 active, 3 working on campaigns, 4 on standby. Top performer: SEO Optimizer (94% success rate).'
      }

      const aiMessage = {
        id: Date.now().toString(),
        type: 'assistant',
        content: response,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, aiMessage])
      setIsTyping(false)
    }, 2000)
  }

  return (
    <Card className="h-[600px] flex flex-col">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MessageCircle className="h-5 w-5" />
          AI Assistant
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto space-y-4 mb-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-3 rounded-lg ${
                  message.type === 'user'
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted'
                }`}
              >
                <p className="text-sm">{message.content}</p>
                <span className="text-xs opacity-70">
                  {message.timestamp.toLocaleTimeString()}
                </span>
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-muted p-3 rounded-lg">
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="flex gap-2">
          <Input
            placeholder="Ask me about traffic, performance, leads, revenue..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          />
          <Button onClick={handleSendMessage} disabled={isTyping}>
            Send
          </Button>
        </div>

        {/* Quick Actions */}
        <div className="flex flex-wrap gap-2 mt-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setInputMessage("What's my traffic today?")}
          >
            Traffic Today
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setInputMessage("How many leads this month?")}
          >
            Leads This Month
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setInputMessage("Show platform performance")}
          >
            Performance Status
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

export default function EnhancedDashboardPage() {
  // Live data hooks
  const { metrics, loading: metricsLoading, error: metricsError } = useDashboardMetrics('7d')
  const { metrics: realtimeMetrics, connected } = useRealtimeMetrics()
  const { agents, loading: agentsLoading } = useAgents({ autoRefresh: true })
  const { data: gatewayData } = useApiGatewayDashboard()
  const { data: aiData } = useAIAgentsData()
  
  // Tab state
  const [activeTab, setActiveTab] = useState('overview')

  // Enhanced stats with live data
  const stats = [
    {
      title: 'Monthly Revenue',
      value: metrics ? formatMetricValue(metrics.overview.monthlyRevenue, 'currency') : '$12,450',
      change: metrics ? `${metrics.overview.revenueGrowth > 0 ? '+' : ''}${metrics.overview.revenueGrowth.toFixed(1)}% from last month` : '+18% from last month',
      trend: metrics ? (metrics.overview.revenueGrowth > 0 ? 'up' : 'down') : 'up',
      icon: DollarSign,
      color: 'text-green-600',
    },
    {
      title: 'Total Leads',
      value: metrics ? metrics.leads.totalLeads.toLocaleString() : '1,247',
      change: metrics ? `+${metrics.leads.newLeadsToday} today` : '+89 today',
      trend: 'up',
      icon: Target,
      color: 'text-blue-600',
    },
    {
      title: 'AI Agents Active',
      value: aiData?.summary.activeAgents?.toString() || '12',
      change: `${aiData?.summary.workingAgents || 3} working now`,
      trend: 'up',
      icon: Bot,
      color: 'text-purple-600',
    },
    {
      title: 'Platform Uptime',
      value: '99.8%',
      change: gatewayData?.gateway.status === 'healthy' ? 'All systems operational' : 'Some services degraded',
      trend: gatewayData?.gateway.status === 'healthy' ? 'up' : 'down',
      icon: Activity,
      color: 'text-green-600',
    },
  ]

  // Mock agents data for the overview
  const activeAgents = agents || [
    { id: '1', name: 'SEO Optimizer', status: 'working', performance: 94, currentTask: 'Optimizing keywords for client sites' },
    { id: '2', name: 'Content Creator', status: 'active', performance: 88, currentTask: 'Ready for content generation' },
    { id: '3', name: 'Social Media Manager', status: 'working', performance: 92, currentTask: 'Scheduling posts for 5 clients' },
    { id: '4', name: 'Email Marketer', status: 'idle', performance: 85, currentTask: 'Waiting for campaign data' },
  ]

  // Mock campaigns for overview
  const topCampaigns = metrics?.campaigns?.topPerformingCampaigns || [
    { id: '1', name: 'Summer Sale Campaign', ctr: 3.2, impressions: 15420, conversions: 89, cost: 1250 },
    { id: '2', name: 'SEO Content Drive', ctr: 2.8, impressions: 12300, conversions: 67, cost: 890 },
    { id: '3', name: 'Social Media Blitz', ctr: 4.1, impressions: 8900, conversions: 45, cost: 650 },
  ]

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Enhanced Dashboard</h1>
          <p className="text-muted-foreground">
            Comprehensive view of your autonomous AI marketing platform with real-time data and AI assistance.
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge variant={connected ? "default" : "secondary"}>
            {connected ? 'Live Data Connected' : 'Offline Mode'}
          </Badge>
        </div>
      </div>

      {/* Tabs Navigation */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview" className="flex items-center gap-2">
            <BarChart3 className="h-4 w-4" />
            Overview
          </TabsTrigger>
          <TabsTrigger value="calendar" className="flex items-center gap-2">
            <CalendarDays className="h-4 w-4" />
            Calendar
          </TabsTrigger>
          <TabsTrigger value="ai-chat" className="flex items-center gap-2">
            <MessageCircle className="h-4 w-4" />
            AI Assistant
          </TabsTrigger>
          <TabsTrigger value="agents" className="flex items-center gap-2">
            <Bot className="h-4 w-4" />
            AI Agents
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Key Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {stats.map((stat) => (
              <Card key={stat.title}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                  <stat.icon className={`h-4 w-4 ${stat.color}`} />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <p className="text-xs text-muted-foreground flex items-center">
                    {stat.trend === 'up' ? (
                      <ArrowUpRight className="h-3 w-3 text-green-600 mr-1" />
                    ) : (
                      <ArrowDownRight className="h-3 w-3 text-red-600 mr-1" />
                    )}
                    {stat.change}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <Button className="h-16 flex flex-col items-center gap-2" onClick={() => setActiveTab('calendar')}>
                  <CalendarDays className="h-6 w-6" />
                  Schedule Campaign
                </Button>
                <Button variant="outline" className="h-16 flex flex-col items-center gap-2" onClick={() => setActiveTab('ai-chat')}>
                  <MessageCircle className="h-6 w-6" />
                  Ask AI Assistant
                </Button>
                <Button variant="outline" className="h-16 flex flex-col items-center gap-2">
                  <TrendingUp className="h-6 w-6" />
                  View Analytics
                </Button>
                <Button variant="outline" className="h-16 flex flex-col items-center gap-2">
                  <Settings className="h-6 w-6" />
                  Platform Settings
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Campaign Performance & AI Agents Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Campaign Performance */}
            <Card>
              <CardHeader>
                <CardTitle>Top Performing Campaigns</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {topCampaigns.map((campaign, index) => (
                    <div key={campaign.id} className="flex items-center justify-between p-4 border rounded-lg">
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
                  ))}
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
                  {activeAgents.slice(0, 4).map((agent) => (
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
                            {(agent as any).currentTask || agent.description}
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <Badge variant="outline" className="text-xs">
                          {agent.performance}% performance
                        </Badge>
                      </div>
                    </div>
                  ))}
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
              height="400px"
              showControls={true}
            />
          </div>
        </TabsContent>

        {/* Calendar Tab */}
        <TabsContent value="calendar" className="space-y-6">
          <CalendarHub userRole="admin" className="mt-0" />
        </TabsContent>

        {/* AI Chat Tab */}
        <TabsContent value="ai-chat" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <AIAssistantChat />
            </div>
            <div className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Sample Questions</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <p className="text-sm">Try asking:</p>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      <li>• "What's my traffic for today?"</li>
                      <li>• "How many leads this month?"</li>
                      <li>• "Show platform performance"</li>
                      <li>• "Which campaigns are performing best?"</li>
                      <li>• "What's my revenue this month?"</li>
                      <li>• "Status of AI agents"</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Live Data Sources</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm">API Gateway</span>
                      <Badge variant={gatewayData?.gateway.status === 'healthy' ? 'default' : 'destructive'}>
                        {gatewayData?.gateway.status || 'Connected'}
                      </Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">AI Agents</span>
                      <Badge variant={aiData?.health.status === 'healthy' ? 'default' : 'destructive'}>
                        {aiData?.health.status || 'Connected'}
                      </Badge>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">Analytics</span>
                      <Badge variant={connected ? 'default' : 'secondary'}>
                        {connected ? 'Live' : 'Cached'}
                      </Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        {/* AI Agents Tab */}
        <TabsContent value="agents" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {activeAgents.map((agent) => (
              <Card key={agent.id}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>{agent.name}</span>
                    <Badge variant={
                      agent.status === 'working' ? 'default' :
                      agent.status === 'active' ? 'secondary' :
                      'outline'
                    }>
                      {agent.status}
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-sm">
                        <span>Performance</span>
                        <span>{agent.performance}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${
                            agent.performance > 90 ? 'bg-green-500' :
                            agent.performance > 75 ? 'bg-blue-500' :
                            'bg-yellow-500'
                          }`}
                          style={{ width: `${agent.performance}%` }}
                        ></div>
                      </div>
                    </div>
                    <div>
                      <p className="text-sm font-medium">Current Task:</p>
                      <p className="text-sm text-muted-foreground">{(agent as any).currentTask || agent.description}</p>
                    </div>
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline">
                        <Settings className="h-4 w-4 mr-2" />
                        Configure
                      </Button>
                      <Button size="sm" variant="outline">
                        <Play className="h-4 w-4 mr-2" />
                        {agent.status === 'working' ? 'Pause' : 'Start'}
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}