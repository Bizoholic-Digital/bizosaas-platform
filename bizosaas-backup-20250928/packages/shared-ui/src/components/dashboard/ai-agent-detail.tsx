'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { ScrollArea } from '@/components/ui/scroll-area'
import { 
  Bot, 
  Target, 
  Settings,
  Activity,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle,
  TrendingUp,
  Database,
  Cpu,
  Memory,
  Network,
  Play,
  Pause,
  RotateCcw,
  Terminal,
  FileText,
  BarChart3,
  Wrench,
  Brain,
  ArrowLeft
} from 'lucide-react'
import { cn } from '@/lib/utils'

interface AgentTask {
  id: string
  name: string
  status: 'completed' | 'running' | 'failed' | 'pending'
  startTime: string
  endTime?: string
  duration?: string
  result?: string
  error?: string
  workflow_id?: string
}

interface AgentTool {
  id: string
  name: string
  type: 'api' | 'database' | 'ai_model' | 'external_service'
  status: 'active' | 'inactive' | 'error'
  description: string
  lastUsed: string
  usageCount: number
  config: Record<string, any>
}

interface AgentPerformanceMetrics {
  efficiency: number
  accuracy: number
  responseTime: number
  taskSuccessRate: number
  resourceUsage: {
    cpu: number
    memory: number
    apiCalls: number
  }
  trends: {
    tasksPerHour: number[]
    errorRate: number[]
    responseTime: number[]
  }
}

interface AgentConfiguration {
  model: string
  temperature: number
  maxTokens: number
  prompt: string
  systemInstructions: string
  tools: string[]
  webhooks: string[]
  schedule: string
  retryPolicy: {
    maxRetries: number
    backoffMultiplier: number
  }
  resources: {
    memoryLimit: string
    cpuLimit: string
    timeout: number
  }
}

interface DetailedAIAgent {
  id: string
  name: string
  type: string
  status: 'active' | 'idle' | 'error' | 'processing'
  description: string
  category: 'strategy' | 'content' | 'analytics' | 'automation'
  version: string
  createdAt: string
  lastActive: string
  tasksCompleted: number
  currentTask?: string
  recentTasks: AgentTask[]
  tools: AgentTool[]
  performance: AgentPerformanceMetrics
  configuration: AgentConfiguration
  logs: Array<{
    timestamp: string
    level: 'info' | 'warning' | 'error'
    message: string
    context?: Record<string, any>
  }>
}

const mockDetailedAgent: DetailedAIAgent = {
  id: 'agent-001',
  name: 'Campaign Strategy Agent',
  type: 'marketing_strategist',
  status: 'active',
  description: 'Advanced AI agent specializing in campaign strategy optimization and audience targeting',
  category: 'strategy',
  version: '2.1.3',
  createdAt: '2024-01-15T10:00:00Z',
  lastActive: '2 minutes ago',
  tasksCompleted: 247,
  currentTask: 'Analyzing Q4 campaign performance data',
  recentTasks: [
    {
      id: 'task-001',
      name: 'Q4 Campaign Analysis',
      status: 'running',
      startTime: '2024-09-11T06:30:00Z',
      workflow_id: 'wf-campaign-analysis-001'
    },
    {
      id: 'task-002', 
      name: 'Audience Segmentation',
      status: 'completed',
      startTime: '2024-09-11T05:15:00Z',
      endTime: '2024-09-11T05:45:00Z',
      duration: '30 minutes',
      result: 'Identified 5 high-value audience segments'
    },
    {
      id: 'task-003',
      name: 'Budget Optimization',
      status: 'completed', 
      startTime: '2024-09-11T04:00:00Z',
      endTime: '2024-09-11T04:25:00Z',
      duration: '25 minutes',
      result: 'Optimized budget allocation across 12 campaigns'
    }
  ],
  tools: [
    {
      id: 'google-ads-api',
      name: 'Google Ads API',
      type: 'api',
      status: 'active',
      description: 'Access to Google Ads campaign data and management',
      lastUsed: '5 minutes ago',
      usageCount: 1247,
      config: { version: 'v15', scope: 'campaigns,keywords' }
    },
    {
      id: 'analytics-db',
      name: 'Analytics Database',
      type: 'database',
      status: 'active',
      description: 'Historical campaign performance data',
      lastUsed: '2 minutes ago',
      usageCount: 892,
      config: { connection: 'postgresql://analytics:5432', timeout: 30 }
    },
    {
      id: 'openai-gpt4',
      name: 'OpenAI GPT-4',
      type: 'ai_model',
      status: 'active',
      description: 'Strategic analysis and recommendations',
      lastUsed: '1 minute ago',
      usageCount: 156,
      config: { model: 'gpt-4-turbo-preview', temperature: 0.3 }
    }
  ],
  performance: {
    efficiency: 94,
    accuracy: 97,
    responseTime: 2.3,
    taskSuccessRate: 96.5,
    resourceUsage: {
      cpu: 45,
      memory: 67,
      apiCalls: 1247
    },
    trends: {
      tasksPerHour: [12, 15, 18, 14, 16, 20, 17],
      errorRate: [1.2, 0.8, 1.5, 0.9, 1.1, 0.7, 1.0],
      responseTime: [2.1, 2.3, 1.9, 2.2, 2.0, 2.3, 2.1]
    }
  },
  configuration: {
    model: 'gpt-4-turbo-preview',
    temperature: 0.3,
    maxTokens: 4096,
    prompt: 'You are an expert marketing strategist...',
    systemInstructions: 'Analyze campaign data and provide strategic recommendations...',
    tools: ['google-ads-api', 'analytics-db', 'openai-gpt4'],
    webhooks: ['campaign-update', 'performance-alert'],
    schedule: '*/15 * * * *',
    retryPolicy: {
      maxRetries: 3,
      backoffMultiplier: 2
    },
    resources: {
      memoryLimit: '2Gi',
      cpuLimit: '1000m',
      timeout: 300
    }
  },
  logs: [
    {
      timestamp: '2024-09-11T07:30:15Z',
      level: 'info',
      message: 'Started Q4 campaign analysis task',
      context: { task_id: 'task-001', workflow_id: 'wf-campaign-analysis-001' }
    },
    {
      timestamp: '2024-09-11T07:28:45Z',
      level: 'info',
      message: 'Successfully retrieved campaign data from Google Ads API',
      context: { campaigns_count: 47, date_range: '2024-10-01 to 2024-12-31' }
    },
    {
      timestamp: '2024-09-11T07:25:12Z',
      level: 'warning',
      message: 'Rate limit approaching for Google Ads API',
      context: { remaining_quota: 150, reset_time: '2024-09-11T08:00:00Z' }
    }
  ]
}

interface AIAgentDetailProps {
  agentId: string
  onBack: () => void
}

export function AIAgentDetail({ agentId, onBack }: AIAgentDetailProps) {
  const [agent, setAgent] = useState<DetailedAIAgent>(mockDetailedAgent)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    // In production, fetch agent details by ID
    setLoading(true)
    setTimeout(() => {
      setAgent(mockDetailedAgent)
      setLoading(false)
    }, 1000)
  }, [agentId])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-50'
      case 'processing': return 'text-blue-600 bg-blue-50'
      case 'idle': return 'text-yellow-600 bg-yellow-50'
      case 'error': return 'text-red-600 bg-red-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  const getTaskStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'running': return <Activity className="w-4 h-4 text-blue-500 animate-pulse" />
      case 'failed': return <XCircle className="w-4 h-4 text-red-500" />
      case 'pending': return <Clock className="w-4 h-4 text-yellow-500" />
      default: return <AlertCircle className="w-4 h-4 text-gray-500" />
    }
  }

  const handleAgentAction = async (action: 'start' | 'pause' | 'restart') => {
    setLoading(true)
    try {
      // Call agent control API
      console.log(`${action} agent:`, agentId)
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Bot className="h-12 w-12 mx-auto mb-4 opacity-50 animate-pulse" />
          <p className="text-muted-foreground">Loading agent details...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="icon" onClick={onBack}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold">{agent.name}</h1>
            <p className="text-muted-foreground">{agent.description}</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <Badge className={cn('px-3 py-1', getStatusColor(agent.status))}>
            {agent.status}
          </Badge>
          <Badge variant="outline">v{agent.version}</Badge>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Tasks Completed</p>
                <p className="text-2xl font-bold">{agent.tasksCompleted}</p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Efficiency</p>
                <p className="text-2xl font-bold">{agent.performance.efficiency}%</p>
              </div>
              <TrendingUp className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Success Rate</p>
                <p className="text-2xl font-bold">{agent.performance.taskSuccessRate}%</p>
              </div>
              <Target className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Avg Response</p>
                <p className="text-2xl font-bold">{agent.performance.responseTime}s</p>
              </div>
              <Clock className="h-8 w-8 text-orange-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Action Buttons */}
      <div className="flex items-center space-x-2">
        <Button 
          variant={agent.status === 'active' ? 'secondary' : 'default'}
          onClick={() => handleAgentAction(agent.status === 'active' ? 'pause' : 'start')}
          disabled={loading}
        >
          {agent.status === 'active' ? (
            <>
              <Pause className="w-4 h-4 mr-2" />
              Pause Agent
            </>
          ) : (
            <>
              <Play className="w-4 h-4 mr-2" />
              Start Agent
            </>
          )}
        </Button>
        <Button variant="outline" onClick={() => handleAgentAction('restart')} disabled={loading}>
          <RotateCcw className="w-4 h-4 mr-2" />
          Restart
        </Button>
      </div>

      {/* Detailed Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="tasks">Tasks</TabsTrigger>
          <TabsTrigger value="tools">Tools</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="config">Config</TabsTrigger>
          <TabsTrigger value="logs">Logs</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Current Status</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <p className="text-sm text-muted-foreground">Current Task</p>
                  <p className="font-medium">{agent.currentTask || 'No active task'}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Last Active</p>
                  <p className="font-medium">{agent.lastActive}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Created</p>
                  <p className="font-medium">{new Date(agent.createdAt).toLocaleDateString()}</p>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Resource Usage</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>CPU Usage</span>
                    <span>{agent.performance.resourceUsage.cpu}%</span>
                  </div>
                  <Progress value={agent.performance.resourceUsage.cpu} />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Memory Usage</span>
                    <span>{agent.performance.resourceUsage.memory}%</span>
                  </div>
                  <Progress value={agent.performance.resourceUsage.memory} />
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">API Calls Today</p>
                  <p className="text-2xl font-bold">{agent.performance.resourceUsage.apiCalls}</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="tasks" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Recent Tasks</CardTitle>
              <CardDescription>Latest task execution history</CardDescription>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-[400px]">
                <div className="space-y-4">
                  {agent.recentTasks.map((task) => (
                    <div key={task.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-3">
                        {getTaskStatusIcon(task.status)}
                        <div>
                          <p className="font-medium">{task.name}</p>
                          <p className="text-sm text-muted-foreground">
                            Started: {new Date(task.startTime).toLocaleString()}
                          </p>
                          {task.duration && (
                            <p className="text-sm text-muted-foreground">Duration: {task.duration}</p>
                          )}
                          {task.result && (
                            <p className="text-sm text-green-600">{task.result}</p>
                          )}
                        </div>
                      </div>
                      <Badge variant="outline">{task.status}</Badge>
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="tools" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Agent Tools</CardTitle>
              <CardDescription>Connected tools and their status</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4">
                {agent.tools.map((tool) => (
                  <div key={tool.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className={cn('p-2 rounded-lg', 
                        tool.status === 'active' ? 'bg-green-100 text-green-600' :
                        tool.status === 'error' ? 'bg-red-100 text-red-600' :
                        'bg-gray-100 text-gray-600'
                      )}>
                        {tool.type === 'api' && <Network className="h-4 w-4" />}
                        {tool.type === 'database' && <Database className="h-4 w-4" />}
                        {tool.type === 'ai_model' && <Brain className="h-4 w-4" />}
                        {tool.type === 'external_service' && <Cpu className="h-4 w-4" />}
                      </div>
                      <div>
                        <p className="font-medium">{tool.name}</p>
                        <p className="text-sm text-muted-foreground">{tool.description}</p>
                        <p className="text-xs text-muted-foreground">
                          Used {tool.usageCount} times • Last: {tool.lastUsed}
                        </p>
                      </div>
                    </div>
                    <Badge variant={tool.status === 'active' ? 'default' : 'secondary'}>
                      {tool.status}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="performance" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Performance Metrics</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Efficiency</span>
                    <span>{agent.performance.efficiency}%</span>
                  </div>
                  <Progress value={agent.performance.efficiency} />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Accuracy</span>
                    <span>{agent.performance.accuracy}%</span>
                  </div>
                  <Progress value={agent.performance.accuracy} />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Success Rate</span>
                    <span>{agent.performance.taskSuccessRate}%</span>
                  </div>
                  <Progress value={agent.performance.taskSuccessRate} />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Performance Trends</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <p className="text-sm text-muted-foreground mb-2">Tasks per Hour (Last 7 hours)</p>
                    <div className="flex items-end space-x-1 h-20">
                      {agent.performance.trends.tasksPerHour.map((value, index) => (
                        <div
                          key={index}
                          className="bg-blue-500 rounded-t"
                          style={{ 
                            height: `${(value / Math.max(...agent.performance.trends.tasksPerHour)) * 100}%`,
                            width: '100%' 
                          }}
                        />
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Average Response Time</p>
                    <p className="text-2xl font-bold">{agent.performance.responseTime}s</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="config" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Agent Configuration</CardTitle>
              <CardDescription>Current agent settings and parameters</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <p className="text-sm font-medium mb-2">AI Model Settings</p>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Model:</span>
                        <span>{agent.configuration.model}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Temperature:</span>
                        <span>{agent.configuration.temperature}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Max Tokens:</span>
                        <span>{agent.configuration.maxTokens}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <p className="text-sm font-medium mb-2">Resource Limits</p>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Memory:</span>
                        <span>{agent.configuration.resources.memoryLimit}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">CPU:</span>
                        <span>{agent.configuration.resources.cpuLimit}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Timeout:</span>
                        <span>{agent.configuration.resources.timeout}s</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <div>
                    <p className="text-sm font-medium mb-2">Retry Policy</p>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Max Retries:</span>
                        <span>{agent.configuration.retryPolicy.maxRetries}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Backoff:</span>
                        <span>{agent.configuration.retryPolicy.backoffMultiplier}x</span>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <p className="text-sm font-medium mb-2">Schedule</p>
                    <p className="text-sm text-muted-foreground font-mono bg-gray-50 p-2 rounded">
                      {agent.configuration.schedule}
                    </p>
                  </div>
                </div>
              </div>

              <div>
                <p className="text-sm font-medium mb-2">System Instructions</p>
                <ScrollArea className="h-32 w-full border rounded-md p-3">
                  <p className="text-sm text-muted-foreground">
                    {agent.configuration.systemInstructions}
                  </p>
                </ScrollArea>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="logs" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Agent Logs</CardTitle>
              <CardDescription>Recent activity and debug information</CardDescription>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-[500px] w-full">
                <div className="space-y-2">
                  {agent.logs.map((log, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 border rounded-lg font-mono text-sm">
                      <div className={cn('w-2 h-2 rounded-full mt-2 flex-shrink-0',
                        log.level === 'error' ? 'bg-red-500' :
                        log.level === 'warning' ? 'bg-yellow-500' :
                        'bg-blue-500'
                      )} />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs text-muted-foreground">
                            {new Date(log.timestamp).toLocaleString()}
                          </span>
                          <Badge variant="outline" className="text-xs">
                            {log.level}
                          </Badge>
                        </div>
                        <p className="text-sm">{log.message}</p>
                        {log.context && (
                          <details className="mt-2">
                            <summary className="text-xs text-muted-foreground cursor-pointer">Context</summary>
                            <pre className="text-xs bg-gray-50 p-2 rounded mt-1 overflow-x-auto">
                              {JSON.stringify(log.context, null, 2)}
                            </pre>
                          </details>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}