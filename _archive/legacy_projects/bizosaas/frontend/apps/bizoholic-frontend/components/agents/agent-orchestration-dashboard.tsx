'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import { Progress } from '@/components/ui/progress'
import { 
  Bot, 
  Users, 
  Activity, 
  Zap, 
  Play, 
  Pause, 
  Square, 
  Settings,
  BarChart3,
  TrendingUp,
  TrendingDown,
  Cpu,
  Database,
  Globe,
  MessageSquare,
  FileText,
  Mail,
  Phone,
  Calendar,
  DollarSign,
  ShoppingCart,
  Target,
  Brain,
  Network,
  AlertTriangle,
  CheckCircle,
  Clock,
  Filter,
  Search,
  RefreshCw,
  Download,
  Upload,
  Eye,
  EyeOff,
  ChevronRight,
  ChevronDown
} from 'lucide-react'

// Agent patterns and categories
const AGENT_PATTERNS = {
  '4-agent': {
    name: '4-Agent Team',
    description: 'Complex multi-role coordination',
    icon: Users,
    color: 'bg-purple-500',
    agents: 22
  },
  '3-agent': {
    name: '3-Agent Squad',
    description: 'Specialized task groups',
    icon: Users,
    color: 'bg-blue-500',
    agents: 24
  },
  '2-agent': {
    name: '2-Agent Pair',
    description: 'Dual-role collaboration',
    icon: Users,
    color: 'bg-green-500',
    agents: 18
  },
  'single-agent': {
    name: 'Single Agent',
    description: 'Independent task execution',
    icon: Bot,
    color: 'bg-orange-500',
    agents: 24
  }
}

const BUSINESS_CATEGORIES = {
  'social-media': { name: 'Social Media', count: 12, color: 'bg-pink-500' },
  'e-commerce': { name: 'E-commerce', count: 10, color: 'bg-green-500' },
  'llm-providers': { name: 'LLM Providers', count: 8, color: 'bg-purple-500' },
  'productivity': { name: 'Productivity', count: 9, color: 'bg-blue-500' },
  'email-marketing': { name: 'Email Marketing', count: 7, color: 'bg-red-500' },
  'analytics': { name: 'Analytics', count: 8, color: 'bg-yellow-500' },
  'crm-sales': { name: 'CRM & Sales', count: 11, color: 'bg-indigo-500' },
  'content-creation': { name: 'Content Creation', count: 6, color: 'bg-teal-500' },
  'seo-tools': { name: 'SEO Tools', count: 5, color: 'bg-gray-500' },
  'advertising': { name: 'Advertising', count: 7, color: 'bg-orange-500' },
  'communication': { name: 'Communication', count: 4, color: 'bg-cyan-500' },
  'automation': { name: 'Automation', count: 8, color: 'bg-lime-500' },
  'project-management': { name: 'Project Management', count: 3, color: 'bg-rose-500' }
}

// Mock agent data
const generateMockAgents = () => {
  const agents = []
  let agentId = 1

  Object.entries(BUSINESS_CATEGORIES).forEach(([categoryKey, category]) => {
    Object.entries(AGENT_PATTERNS).forEach(([patternKey, pattern]) => {
      const agentsInCategory = Math.floor(category.count / Object.keys(AGENT_PATTERNS).length)
      
      for (let i = 0; i < agentsInCategory; i++) {
        const statuses = ['active', 'idle', 'working', 'error', 'maintenance']
        const status = statuses[Math.floor(Math.random() * statuses.length)]
        
        agents.push({
          id: `agent-${agentId++}`,
          name: `${category.name} ${pattern.name} ${i + 1}`,
          category: categoryKey,
          pattern: patternKey,
          status,
          performance: Math.floor(Math.random() * 30) + 70,
          tasksCompleted: Math.floor(Math.random() * 100),
          tasksActive: status === 'working' ? Math.floor(Math.random() * 5) + 1 : 0,
          lastActive: new Date(Date.now() - Math.random() * 3600000 * 24),
          cpu: Math.floor(Math.random() * 40) + 20,
          memory: Math.floor(Math.random() * 60) + 30,
          uptime: Math.floor(Math.random() * 168) + 1, // hours
          errors: Math.floor(Math.random() * 10),
          successRate: Math.floor(Math.random() * 20) + 80,
          avgResponseTime: Math.floor(Math.random() * 500) + 100, // ms
          currentTask: status === 'working' ? `Processing ${category.name.toLowerCase()} task` : null
        })
      }
    })
  })

  return agents
}

interface Agent {
  id: string
  name: string
  category: string
  pattern: string
  status: 'active' | 'idle' | 'working' | 'error' | 'maintenance'
  performance: number
  tasksCompleted: number
  tasksActive: number
  lastActive: Date
  cpu: number
  memory: number
  uptime: number
  errors: number
  successRate: number
  avgResponseTime: number
  currentTask?: string | null
}

export default function AgentOrchestrationDashboard() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [filteredAgents, setFilteredAgents] = useState<Agent[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [selectedPattern, setSelectedPattern] = useState<string>('all')
  const [selectedStatus, setSelectedStatus] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null)
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set())

  // Initialize agents
  useEffect(() => {
    const mockAgents = generateMockAgents()
    setAgents(mockAgents)
    setFilteredAgents(mockAgents)
  }, [])

  // Auto refresh simulation
  useEffect(() => {
    if (!autoRefresh) return

    const interval = setInterval(() => {
      setAgents(prev => prev.map(agent => ({
        ...agent,
        cpu: Math.max(0, Math.min(100, agent.cpu + (Math.random() - 0.5) * 10)),
        memory: Math.max(0, Math.min(100, agent.memory + (Math.random() - 0.5) * 10)),
        performance: Math.max(0, Math.min(100, agent.performance + (Math.random() - 0.5) * 5)),
        avgResponseTime: Math.max(50, agent.avgResponseTime + (Math.random() - 0.5) * 50)
      })))
    }, 5000)

    return () => clearInterval(interval)
  }, [autoRefresh])

  // Filter agents
  useEffect(() => {
    let filtered = agents

    if (selectedCategory !== 'all') {
      filtered = filtered.filter(agent => agent.category === selectedCategory)
    }

    if (selectedPattern !== 'all') {
      filtered = filtered.filter(agent => agent.pattern === selectedPattern)
    }

    if (selectedStatus !== 'all') {
      filtered = filtered.filter(agent => agent.status === selectedStatus)
    }

    if (searchQuery) {
      filtered = filtered.filter(agent => 
        agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        agent.id.toLowerCase().includes(searchQuery.toLowerCase())
      )
    }

    setFilteredAgents(filtered)
  }, [agents, selectedCategory, selectedPattern, selectedStatus, searchQuery])

  // Calculate summary stats
  const summaryStats = {
    total: agents.length,
    active: agents.filter(a => a.status === 'active').length,
    working: agents.filter(a => a.status === 'working').length,
    idle: agents.filter(a => a.status === 'idle').length,
    error: agents.filter(a => a.status === 'error').length,
    avgPerformance: Math.round(agents.reduce((sum, a) => sum + a.performance, 0) / agents.length),
    totalTasks: agents.reduce((sum, a) => sum + a.tasksCompleted, 0),
    activeTasks: agents.reduce((sum, a) => sum + a.tasksActive, 0)
  }

  // Handle agent actions
  const handleAgentAction = (agentId: string, action: 'start' | 'stop' | 'restart' | 'configure') => {
    setAgents(prev => prev.map(agent => {
      if (agent.id === agentId) {
        switch (action) {
          case 'start':
            return { ...agent, status: 'active' as const }
          case 'stop':
            return { ...agent, status: 'idle' as const }
          case 'restart':
            return { ...agent, status: 'working' as const, errors: 0 }
          default:
            return agent
        }
      }
      return agent
    }))
  }

  // Status badge component
  const StatusBadge = ({ status }: { status: string }) => {
    const colors = {
      active: 'bg-green-500',
      working: 'bg-blue-500',
      idle: 'bg-gray-500',
      error: 'bg-red-500',
      maintenance: 'bg-yellow-500'
    }
    
    return (
      <Badge variant="outline" className={`${colors[status as keyof typeof colors]} text-white border-0`}>
        {status}
      </Badge>
    )
  }

  // Performance indicator
  const PerformanceIndicator = ({ value, label }: { value: number; label: string }) => (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span>{label}</span>
        <span>{value}%</span>
      </div>
      <Progress value={value} className="h-1" />
    </div>
  )

  // Agent card component
  const AgentCard = ({ agent }: { agent: Agent }) => {
    const PatternIcon = AGENT_PATTERNS[agent.pattern as keyof typeof AGENT_PATTERNS].icon
    
    return (
      <Card className="hover:shadow-lg transition-shadow cursor-pointer"
            onClick={() => setSelectedAgent(agent)}>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className={`p-1 rounded ${AGENT_PATTERNS[agent.pattern as keyof typeof AGENT_PATTERNS].color}`}>
                <PatternIcon className="w-4 h-4 text-white" />
              </div>
              <div className="text-sm font-medium truncate">{agent.name}</div>
            </div>
            <StatusBadge status={agent.status} />
          </div>
          <div className="flex items-center space-x-2 text-xs text-muted-foreground">
            <Badge variant="outline" className="text-xs">
              {BUSINESS_CATEGORIES[agent.category as keyof typeof BUSINESS_CATEGORIES].name}
            </Badge>
            <Badge variant="outline" className="text-xs">
              {agent.pattern}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-3">
          <PerformanceIndicator value={agent.performance} label="Performance" />
          <PerformanceIndicator value={agent.cpu} label="CPU" />
          <PerformanceIndicator value={agent.memory} label="Memory" />
          
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="text-center p-2 bg-muted rounded">
              <div className="font-medium">{agent.tasksCompleted}</div>
              <div className="text-muted-foreground">Completed</div>
            </div>
            <div className="text-center p-2 bg-muted rounded">
              <div className="font-medium">{agent.tasksActive}</div>
              <div className="text-muted-foreground">Active</div>
            </div>
          </div>

          {agent.currentTask && (
            <div className="text-xs p-2 bg-blue-50 rounded">
              <div className="font-medium text-blue-700">Current Task:</div>
              <div className="text-blue-600">{agent.currentTask}</div>
            </div>
          )}

          <div className="flex space-x-1">
            <Button size="sm" variant="outline" className="flex-1 text-xs"
                    onClick={(e) => {
                      e.stopPropagation()
                      handleAgentAction(agent.id, agent.status === 'active' ? 'stop' : 'start')
                    }}>
              {agent.status === 'active' ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
            </Button>
            <Button size="sm" variant="outline" className="flex-1 text-xs"
                    onClick={(e) => {
                      e.stopPropagation()
                      handleAgentAction(agent.id, 'restart')
                    }}>
              <RefreshCw className="w-3 h-3" />
            </Button>
            <Button size="sm" variant="outline" className="flex-1 text-xs"
                    onClick={(e) => {
                      e.stopPropagation()
                      handleAgentAction(agent.id, 'configure')
                    }}>
              <Settings className="w-3 h-3" />
            </Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  // Category group component
  const CategoryGroup = ({ category, agents }: { category: string, agents: Agent[] }) => {
    const categoryData = BUSINESS_CATEGORIES[category as keyof typeof BUSINESS_CATEGORIES]
    const isExpanded = expandedCategories.has(category)
    
    return (
      <div className="space-y-2">
        <div 
          className="flex items-center justify-between p-3 bg-muted rounded-lg cursor-pointer"
          onClick={() => {
            const newExpanded = new Set(expandedCategories)
            if (isExpanded) {
              newExpanded.delete(category)
            } else {
              newExpanded.add(category)
            }
            setExpandedCategories(newExpanded)
          }}
        >
          <div className="flex items-center space-x-3">
            <div className={`w-3 h-3 rounded ${categoryData.color}`} />
            <div className="font-medium">{categoryData.name}</div>
            <Badge variant="outline">{agents.length} agents</Badge>
          </div>
          {isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
        </div>
        
        {isExpanded && (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {agents.map(agent => (
              <AgentCard key={agent.id} agent={agent} />
            ))}
          </div>
        )}
      </div>
    )
  }

  // Group agents by category
  const agentsByCategory = filteredAgents.reduce((acc, agent) => {
    if (!acc[agent.category]) {
      acc[agent.category] = []
    }
    acc[agent.category].push(agent)
    return acc
  }, {} as Record<string, Agent[]>)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">AI Agent Orchestration Dashboard</h2>
          <p className="text-muted-foreground">
            Monitor and manage 88 AI agents across 13 business categories with real-time performance insights
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Switch checked={autoRefresh} onCheckedChange={setAutoRefresh} />
            <span className="text-sm">Auto Refresh</span>
          </div>
          <Button variant="outline" onClick={() => window.location.reload()}>
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-8">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Bot className="w-4 h-4 text-blue-600" />
              <div className="text-2xl font-bold">{summaryStats.total}</div>
            </div>
            <div className="text-xs text-muted-foreground">Total Agents</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-4 h-4 text-green-600" />
              <div className="text-2xl font-bold">{summaryStats.active}</div>
            </div>
            <div className="text-xs text-muted-foreground">Active</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Activity className="w-4 h-4 text-blue-600" />
              <div className="text-2xl font-bold">{summaryStats.working}</div>
            </div>
            <div className="text-xs text-muted-foreground">Working</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-gray-600" />
              <div className="text-2xl font-bold">{summaryStats.idle}</div>
            </div>
            <div className="text-xs text-muted-foreground">Idle</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4 text-red-600" />
              <div className="text-2xl font-bold">{summaryStats.error}</div>
            </div>
            <div className="text-xs text-muted-foreground">Errors</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-4 h-4 text-green-600" />
              <div className="text-2xl font-bold">{summaryStats.avgPerformance}%</div>
            </div>
            <div className="text-xs text-muted-foreground">Avg Performance</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Target className="w-4 h-4 text-purple-600" />
              <div className="text-2xl font-bold">{summaryStats.totalTasks}</div>
            </div>
            <div className="text-xs text-muted-foreground">Tasks Completed</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Zap className="w-4 h-4 text-orange-600" />
              <div className="text-2xl font-bold">{summaryStats.activeTasks}</div>
            </div>
            <div className="text-xs text-muted-foreground">Active Tasks</div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="patterns">Agent Patterns</TabsTrigger>
          <TabsTrigger value="categories">Business Categories</TabsTrigger>
          <TabsTrigger value="performance">Performance Analytics</TabsTrigger>
          <TabsTrigger value="configuration">Configuration</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Filters */}
          <div className="flex flex-wrap items-center gap-4 p-4 bg-muted rounded-lg">
            <div className="flex items-center space-x-2">
              <Search className="w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search agents..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-64"
              />
            </div>
            
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="All Categories" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                {Object.entries(BUSINESS_CATEGORIES).map(([key, category]) => (
                  <SelectItem key={key} value={key}>{category.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={selectedPattern} onValueChange={setSelectedPattern}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="All Patterns" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Patterns</SelectItem>
                {Object.entries(AGENT_PATTERNS).map(([key, pattern]) => (
                  <SelectItem key={key} value={key}>{pattern.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={selectedStatus} onValueChange={setSelectedStatus}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="All Statuses" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Statuses</SelectItem>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="working">Working</SelectItem>
                <SelectItem value="idle">Idle</SelectItem>
                <SelectItem value="error">Error</SelectItem>
                <SelectItem value="maintenance">Maintenance</SelectItem>
              </SelectContent>
            </Select>

            <div className="flex items-center space-x-2 ml-auto">
              <span className="text-sm text-muted-foreground">
                {filteredAgents.length} of {agents.length} agents
              </span>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setViewMode(viewMode === 'grid' ? 'list' : 'grid')}
              >
                {viewMode === 'grid' ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
              </Button>
            </div>
          </div>

          {/* Agents Display */}
          {viewMode === 'grid' ? (
            <div className="space-y-6">
              {Object.entries(agentsByCategory).map(([category, agents]) => (
                <CategoryGroup key={category} category={category} agents={agents} />
              ))}
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {filteredAgents.map(agent => (
                <AgentCard key={agent.id} agent={agent} />
              ))}
            </div>
          )}
        </TabsContent>

        {/* Agent Patterns Tab */}
        <TabsContent value="patterns" className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {Object.entries(AGENT_PATTERNS).map(([key, pattern]) => {
              const patternAgents = agents.filter(a => a.pattern === key)
              const activeCount = patternAgents.filter(a => a.status === 'active').length
              const workingCount = patternAgents.filter(a => a.status === 'working').length
              
              return (
                <Card key={key}>
                  <CardHeader>
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 rounded ${pattern.color}`}>
                        <pattern.icon className="w-6 h-6 text-white" />
                      </div>
                      <div>
                        <CardTitle className="text-lg">{pattern.name}</CardTitle>
                        <div className="text-sm text-muted-foreground">{pattern.description}</div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="grid grid-cols-3 gap-2 text-center">
                        <div className="p-2 bg-muted rounded">
                          <div className="text-lg font-bold">{pattern.agents}</div>
                          <div className="text-xs text-muted-foreground">Total</div>
                        </div>
                        <div className="p-2 bg-green-50 rounded">
                          <div className="text-lg font-bold text-green-600">{activeCount}</div>
                          <div className="text-xs text-muted-foreground">Active</div>
                        </div>
                        <div className="p-2 bg-blue-50 rounded">
                          <div className="text-lg font-bold text-blue-600">{workingCount}</div>
                          <div className="text-xs text-muted-foreground">Working</div>
                        </div>
                      </div>
                      
                      <Progress 
                        value={(activeCount + workingCount) / pattern.agents * 100} 
                        className="h-2"
                      />
                      
                      <div className="text-center">
                        <div className="text-sm font-medium">
                          {Math.round((activeCount + workingCount) / pattern.agents * 100)}% Utilization
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </TabsContent>

        {/* Business Categories Tab */}
        <TabsContent value="categories" className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {Object.entries(BUSINESS_CATEGORIES).map(([key, category]) => {
              const categoryAgents = agents.filter(a => a.category === key)
              const activeCount = categoryAgents.filter(a => a.status === 'active').length
              const workingCount = categoryAgents.filter(a => a.status === 'working').length
              const avgPerformance = categoryAgents.length > 0 
                ? Math.round(categoryAgents.reduce((sum, a) => sum + a.performance, 0) / categoryAgents.length)
                : 0
              
              return (
                <Card key={key}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className={`w-4 h-4 rounded ${category.color}`} />
                        <CardTitle className="text-lg">{category.name}</CardTitle>
                      </div>
                      <Badge variant="outline">{categoryAgents.length} agents</Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="text-center p-3 bg-green-50 rounded">
                          <div className="text-lg font-bold text-green-600">{activeCount}</div>
                          <div className="text-xs text-muted-foreground">Active</div>
                        </div>
                        <div className="text-center p-3 bg-blue-50 rounded">
                          <div className="text-lg font-bold text-blue-600">{workingCount}</div>
                          <div className="text-xs text-muted-foreground">Working</div>
                        </div>
                      </div>
                      
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span>Avg Performance</span>
                          <span>{avgPerformance}%</span>
                        </div>
                        <Progress value={avgPerformance} className="h-2" />
                      </div>
                      
                      <Button variant="outline" size="sm" className="w-full">
                        <Eye className="w-4 h-4 mr-2" />
                        View Agents
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </TabsContent>

        {/* Performance Analytics Tab */}
        <TabsContent value="performance" className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Performance Distribution</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {['90-100%', '80-89%', '70-79%', '60-69%', '<60%'].map((range, index) => {
                    const [min, max] = range === '<60%' ? [0, 59] : range.split('-').map(r => parseInt(r.replace('%', '')))
                    const count = agents.filter(a => {
                      if (range === '<60%') return a.performance < 60
                      return a.performance >= min && a.performance <= max
                    }).length
                    const percentage = (count / agents.length) * 100
                    
                    return (
                      <div key={range} className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>{range} Performance</span>
                          <span>{count} agents ({percentage.toFixed(1)}%)</span>
                        </div>
                        <Progress value={percentage} className="h-2" />
                      </div>
                    )
                  })}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Resource Utilization</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span>Average CPU Usage</span>
                      <span>{Math.round(agents.reduce((sum, a) => sum + a.cpu, 0) / agents.length)}%</span>
                    </div>
                    <Progress value={agents.reduce((sum, a) => sum + a.cpu, 0) / agents.length} className="h-2" />
                  </div>
                  
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span>Average Memory Usage</span>
                      <span>{Math.round(agents.reduce((sum, a) => sum + a.memory, 0) / agents.length)}%</span>
                    </div>
                    <Progress value={agents.reduce((sum, a) => sum + a.memory, 0) / agents.length} className="h-2" />
                  </div>
                  
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span>Average Response Time</span>
                      <span>{Math.round(agents.reduce((sum, a) => sum + a.avgResponseTime, 0) / agents.length)}ms</span>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span>Overall Success Rate</span>
                      <span>{Math.round(agents.reduce((sum, a) => sum + a.successRate, 0) / agents.length)}%</span>
                    </div>
                    <Progress value={agents.reduce((sum, a) => sum + a.successRate, 0) / agents.length} className="h-2" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Configuration Tab */}
        <TabsContent value="configuration" className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Global Settings</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium">Auto-scaling</div>
                    <div className="text-sm text-muted-foreground">Automatically scale agents based on load</div>
                  </div>
                  <Switch />
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium">Health Monitoring</div>
                    <div className="text-sm text-muted-foreground">Monitor agent health and auto-restart</div>
                  </div>
                  <Switch defaultChecked />
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium">Performance Alerts</div>
                    <div className="text-sm text-muted-foreground">Alert when performance drops below threshold</div>
                  </div>
                  <Switch defaultChecked />
                </div>
                
                <div className="space-y-2">
                  <div className="font-medium">Performance Threshold</div>
                  <Select defaultValue="70">
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="90">90%</SelectItem>
                      <SelectItem value="80">80%</SelectItem>
                      <SelectItem value="70">70%</SelectItem>
                      <SelectItem value="60">60%</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Deployment Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Button className="w-full" onClick={() => alert('Deploy new agents configuration')}>
                  <Upload className="w-4 h-4 mr-2" />
                  Deploy New Agents
                </Button>
                
                <Button variant="outline" className="w-full">
                  <Download className="w-4 h-4 mr-2" />
                  Export Configuration
                </Button>
                
                <Button variant="outline" className="w-full">
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Restart All Agents
                </Button>
                
                <Button variant="destructive" className="w-full">
                  <Square className="w-4 h-4 mr-2" />
                  Emergency Stop All
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      {/* Agent Detail Modal would go here */}
      {selectedAgent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
             onClick={() => setSelectedAgent(null)}>
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full m-4" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">{selectedAgent.name}</h3>
              <Button variant="ghost" size="sm" onClick={() => setSelectedAgent(null)}>×</Button>
            </div>
            
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <div className="text-sm font-medium">Status</div>
                <StatusBadge status={selectedAgent.status} />
              </div>
              <div className="space-y-2">
                <div className="text-sm font-medium">Performance</div>
                <div className="text-2xl font-bold">{selectedAgent.performance}%</div>
              </div>
              <div className="space-y-2">
                <div className="text-sm font-medium">Uptime</div>
                <div>{selectedAgent.uptime}h</div>
              </div>
              <div className="space-y-2">
                <div className="text-sm font-medium">Success Rate</div>
                <div>{selectedAgent.successRate}%</div>
              </div>
            </div>
            
            <div className="mt-6 flex space-x-2">
              <Button size="sm">Configure</Button>
              <Button size="sm" variant="outline">View Logs</Button>
              <Button size="sm" variant="outline">Restart</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}