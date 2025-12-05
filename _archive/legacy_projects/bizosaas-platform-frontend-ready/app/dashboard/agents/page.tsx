"use client"

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Progress } from '@/components/ui/progress'
import { 
  Bot, 
  Activity,
  Zap,
  Settings,
  Play,
  Pause,
  RotateCcw,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertTriangle,
  Users,
  Target,
  PieChart,
  Megaphone,
  Search,
  BarChart3
} from 'lucide-react'
import { useAgents, useAgentStats } from '@/hooks/use-agents'
import { AgentConfigPanel } from '@/components/agent-config-panel'
import { RealTimeAgentMonitor } from '@/components/agents/real-time-agent-monitor'
import { AIAgent } from '@/lib/api/agents-api'


export default function AIAgentsPage() {
  const [activeTab, setActiveTab] = useState('overview')
  
  // Live agent data hooks
  const { 
    agents, 
    loading, 
    error,
    startAgent,
    stopAgent,
    pauseAgent,
    restartAgent
  } = useAgents({
    autoRefresh: true,
    refreshInterval: 30000 // Refresh every 30 seconds
  })
  
  const { stats, loading: statsLoading } = useAgentStats()

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500'
      case 'working': return 'bg-blue-500 animate-pulse'
      case 'idle': return 'bg-gray-500'
      case 'paused': return 'bg-yellow-500'
      case 'error': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <CheckCircle className="h-4 w-4" />
      case 'working': return <Activity className="h-4 w-4 animate-pulse" />
      case 'idle': return <Clock className="h-4 w-4" />
      case 'paused': return <Pause className="h-4 w-4" />
      case 'error': return <AlertTriangle className="h-4 w-4" />
      default: return <Bot className="h-4 w-4" />
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'marketing': return <Target className="h-5 w-5" />
      case 'analytics': return <BarChart3 className="h-5 w-5" />
      case 'content': return <PieChart className="h-5 w-5" />
      case 'social': return <Users className="h-5 w-5" />
      case 'seo': return <Search className="h-5 w-5" />
      case 'reputation': return <Megaphone className="h-5 w-5" />
      default: return <Bot className="h-5 w-5" />
    }
  }

  const formatLastRun = (timestamp: string) => {
    const date = new Date(timestamp)
    return date.toLocaleString()
  }

  // Use live stats when available, fallback to calculated values
  const totalTasks = stats?.totalExecutions || agents.reduce((sum, agent) => sum + agent.tasksCompleted, 0)
  const activeAgents = stats?.activeAgents || agents.filter(agent => agent.status === 'active').length
  const avgPerformance = stats?.avgPerformance || (agents.length > 0 ? Math.round(agents.reduce((sum, agent) => sum + agent.performance, 0) / agents.length) : 0)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">AI Agents</h1>
          <p className="text-muted-foreground">
            Monitor and manage your autonomous AI marketing agents
          </p>
        </div>
        <Button>
          <Settings className="mr-2 h-4 w-4" />
          Agent Settings
        </Button>
      </div>

      {/* Stats Overview */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Agents</CardTitle>
            <Bot className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {statsLoading ? '...' : activeAgents}
            </div>
            <p className="text-xs text-muted-foreground">
              of {stats?.totalAgents || agents.length} total agents
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tasks Completed</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {statsLoading ? '...' : totalTasks}
            </div>
            <p className="text-xs text-muted-foreground">
              +23 from yesterday
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Performance</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {statsLoading ? '...' : avgPerformance}%
            </div>
            <p className="text-xs text-muted-foreground">
              +2.1% from last week
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">System Status</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {statsLoading ? '...' : (stats?.systemHealth === 'optimal' ? 'Optimal' : stats?.systemHealth || 'Optimal')}
            </div>
            <p className="text-xs text-muted-foreground">
              {stats?.uptime ? `${stats.uptime}% uptime` : 'All systems running'}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Agents Grid */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="realtime">Live Monitor</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="logs">Activity Logs</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-600 text-sm">Error loading agents: {error}</p>
            </div>
          )}
          
          {loading ? (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="animate-pulse">
                  <div className="h-64 bg-gray-200 rounded-md"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {agents.map((agent) => (
              <Card key={agent.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {getTypeIcon(agent.type)}
                      <CardTitle className="text-lg">{agent.name}</CardTitle>
                    </div>
                    <div className="flex items-center gap-2">
                      {getStatusIcon(agent.status)}
                      <Badge className={`${getStatusColor(agent.status)} text-white text-xs`}>
                        {agent.status}
                      </Badge>
                    </div>
                  </div>
                  <CardDescription className="text-sm">
                    {agent.description}
                  </CardDescription>
                </CardHeader>

                <CardContent className="space-y-4">
                  {/* Progress */}
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Progress</span>
                      <span>{agent.tasksCompleted}/{agent.tasksTotal}</span>
                    </div>
                    <Progress 
                      value={(agent.tasksCompleted / agent.tasksTotal) * 100} 
                      className="h-2"
                    />
                  </div>

                  {/* Performance */}
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Performance</span>
                      <span>{agent.performance}%</span>
                    </div>
                    <Progress 
                      value={agent.performance} 
                      className="h-2"
                    />
                  </div>

                  {/* Metrics */}
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div>
                      <p className="font-medium">{agent.metrics.successRate}%</p>
                      <p className="text-muted-foreground text-xs">Success Rate</p>
                    </div>
                    <div>
                      <p className="font-medium">{agent.metrics.tasksThisWeek}</p>
                      <p className="text-muted-foreground text-xs">This Week</p>
                    </div>
                  </div>

                  {/* Capabilities */}
                  <div>
                    <p className="text-sm font-medium mb-2">Capabilities</p>
                    <div className="flex flex-wrap gap-1">
                      {agent.capabilities.slice(0, 3).map((capability) => (
                        <Badge key={capability} variant="secondary" className="text-xs">
                          {capability}
                        </Badge>
                      ))}
                      {agent.capabilities.length > 3 && (
                        <Badge variant="secondary" className="text-xs">
                          +{agent.capabilities.length - 3} more
                        </Badge>
                      )}
                    </div>
                  </div>

                  {/* Last Run */}
                  <div className="text-xs text-muted-foreground">
                    <p>Last run: {agent.lastRun ? formatLastRun(agent.lastRun) : 'Never'}</p>
                    {agent.nextRun && (
                      <p>Next run: {formatLastRun(agent.nextRun)}</p>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2">
                    {agent.status === 'active' || agent.status === 'working' ? (
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="flex-1"
                        onClick={() => pauseAgent(agent.id)}
                      >
                        <Pause className="mr-1 h-3 w-3" />
                        Pause
                      </Button>
                    ) : (
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="flex-1"
                        onClick={() => startAgent(agent.id)}
                      >
                        <Play className="mr-1 h-3 w-3" />
                        Start
                      </Button>
                    )}
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => restartAgent(agent.id)}
                    >
                      <RotateCcw className="h-3 w-3" />
                    </Button>
                    <AgentConfigPanel agent={agent} />
                  </div>
                </CardContent>
                </Card>
              ))}
              
              {agents.length === 0 && !loading && (
                <div className="col-span-full text-center py-12 text-muted-foreground">
                  <Bot className="h-16 w-16 mx-auto mb-4" />
                  <p>No AI agents configured</p>
                  <p className="text-sm mt-2">Configure your first agent to get started</p>
                </div>
              )}
            </div>
          )}
        </TabsContent>

        <TabsContent value="realtime" className="space-y-4">
          <RealTimeAgentMonitor />
        </TabsContent>

        <TabsContent value="performance">
          <Card>
            <CardHeader>
              <CardTitle>Agent Performance Analytics</CardTitle>
              <CardDescription>
                Detailed performance metrics and trends for all AI agents
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8 text-muted-foreground">
                <BarChart3 className="h-12 w-12 mx-auto mb-4" />
                <p>Performance analytics dashboard coming soon</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="logs">
          <Card>
            <CardHeader>
              <CardTitle>Activity Logs</CardTitle>
              <CardDescription>
                Real-time activity logs from all AI agents
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8 text-muted-foreground">
                <Activity className="h-12 w-12 mx-auto mb-4" />
                <p>Activity logs dashboard coming soon</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}