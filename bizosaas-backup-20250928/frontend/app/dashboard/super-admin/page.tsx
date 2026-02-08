'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { LoggingDashboard } from "@/components/dashboard/logging-dashboard"
import { 
  Crown,
  Building,
  Users,
  TrendingUp,
  TrendingDown,
  DollarSign,
  Activity,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Clock,
  Zap,
  Bot,
  ShoppingCart,
  Package,
  BarChart3,
  Globe,
  Server,
  Database,
  Cpu,
  HardDrive,
  Wifi,
  Shield,
  Eye,
  Settings,
  ArrowUpRight,
  ArrowDownRight,
  RefreshCw,
  Search,
  Filter,
  Download,
  AlertCircle,
  Gauge,
  GitBranch,
  Play,
  Pause,
  Square,
  RotateCcw,
  ExternalLink,
  Network,
  Timer,
  Monitor,
  FileText
} from 'lucide-react'

interface Company {
  id: string
  name: string
  platform: 'bizoholic' | 'coreldove' | 'thrillring' | 'quanttrade' | 'ai-assistant'
  status: 'active' | 'inactive' | 'suspended' | 'trial'
  users: number
  revenue: number
  lastActive: string
  subscription: {
    plan: 'starter' | 'professional' | 'enterprise' | 'custom'
    status: 'active' | 'cancelled' | 'expired' | 'trial'
    mrr: number
    billing_cycle: 'monthly' | 'yearly'
  }
  metrics: {
    campaigns: number
    leads: number
    conversion_rate: number
    churn_risk: 'low' | 'medium' | 'high'
  }
}

interface SystemMetric {
  id: string
  name: string
  value: string | number
  status: 'healthy' | 'warning' | 'critical'
  change?: number
  unit?: string
  icon: React.ComponentType<{ className?: string }>
}

interface AIAgent {
  id: string
  name: string
  type: 'marketing' | 'ecommerce' | 'analytics' | 'support'
  company: string
  status: 'active' | 'idle' | 'error' | 'maintenance'
  performance: number
  tasks_today: number
  success_rate: number
  last_execution: string
}

interface WorkflowExecution {
  id: string
  workflowId: string
  runId: string
  workflowType: string
  status: 'running' | 'completed' | 'failed' | 'cancelled' | 'timeout'
  startTime: string
  endTime?: string
  duration?: number
  taskQueue: string
  namespace: string
  input?: any
  result?: any
  error?: string
}

interface WorkflowStats {
  totalExecutions: number
  runningExecutions: number
  completedExecutions: number
  failedExecutions: number
  successRate: number
  averageDuration: number
  throughputPerMinute: number
}

const companies: Company[] = [
  {
    id: '1',
    name: 'TechStart Inc',
    platform: 'bizoholic',
    status: 'active',
    users: 12,
    revenue: 15420,
    lastActive: '2024-08-26T10:30:00Z',
    subscription: {
      plan: 'professional',
      status: 'active',
      mrr: 149,
      billing_cycle: 'monthly'
    },
    metrics: {
      campaigns: 25,
      leads: 1240,
      conversion_rate: 12.5,
      churn_risk: 'low'
    }
  },
  {
    id: '2',
    name: 'Fashion Forward',
    platform: 'coreldove',
    status: 'active',
    users: 5,
    revenue: 8950,
    lastActive: '2024-08-26T09:15:00Z',
    subscription: {
      plan: 'enterprise',
      status: 'active',
      mrr: 449,
      billing_cycle: 'yearly'
    },
    metrics: {
      campaigns: 18,
      leads: 890,
      conversion_rate: 15.2,
      churn_risk: 'low'
    }
  },
  {
    id: '3',
    name: 'Local Restaurant',
    platform: 'bizoholic',
    status: 'trial',
    users: 3,
    revenue: 0,
    lastActive: '2024-08-25T16:45:00Z',
    subscription: {
      plan: 'starter',
      status: 'trial',
      mrr: 0,
      billing_cycle: 'monthly'
    },
    metrics: {
      campaigns: 5,
      leads: 120,
      conversion_rate: 8.3,
      churn_risk: 'high'
    }
  },
  {
    id: '4',
    name: 'Investment Firm',
    platform: 'quanttrade',
    status: 'active',
    users: 25,
    revenue: 45200,
    lastActive: '2024-08-26T11:00:00Z',
    subscription: {
      plan: 'custom',
      status: 'active',
      mrr: 2500,
      billing_cycle: 'monthly'
    },
    metrics: {
      campaigns: 50,
      leads: 2340,
      conversion_rate: 22.1,
      churn_risk: 'low'
    }
  }
]

const systemMetrics: SystemMetric[] = [
  {
    id: 'cpu',
    name: 'CPU Usage',
    value: 45,
    status: 'healthy',
    change: -5,
    unit: '%',
    icon: Cpu
  },
  {
    id: 'memory',
    name: 'Memory Usage',
    value: 62,
    status: 'warning',
    change: 8,
    unit: '%',
    icon: HardDrive
  },
  {
    id: 'database',
    name: 'DB Connections',
    value: 145,
    status: 'healthy',
    change: 12,
    unit: 'active',
    icon: Database
  },
  {
    id: 'api_calls',
    name: 'API Calls/min',
    value: '2.4k',
    status: 'healthy',
    change: 15,
    unit: '/min',
    icon: Activity
  },
  {
    id: 'uptime',
    name: 'System Uptime',
    value: '99.9%',
    status: 'healthy',
    unit: '',
    icon: Server
  },
  {
    id: 'response_time',
    name: 'Avg Response',
    value: 120,
    status: 'healthy',
    change: -8,
    unit: 'ms',
    icon: Gauge
  }
]

// Mock workflow data - in real implementation, this would come from Temporal API
const workflowStats: WorkflowStats = {
  totalExecutions: 1547,
  runningExecutions: 23,
  completedExecutions: 1456,
  failedExecutions: 68,
  successRate: 95.6,
  averageDuration: 142.5, // seconds
  throughputPerMinute: 8.3
}

const recentWorkflows: WorkflowExecution[] = [
  {
    id: 'wf_001',
    workflowId: 'campaign-optimization',
    runId: 'run_12345',
    workflowType: 'MarketingCampaignOptimization',
    status: 'running',
    startTime: '2024-08-26T10:45:00Z',
    taskQueue: 'marketing-agents',
    namespace: 'bizosaas-prod',
    input: { campaignId: 'camp_123', platform: 'google-ads' }
  },
  {
    id: 'wf_002',
    workflowId: 'product-research',
    runId: 'run_12346',
    workflowType: 'ProductResearchWorkflow',
    status: 'completed',
    startTime: '2024-08-26T10:30:00Z',
    endTime: '2024-08-26T10:42:00Z',
    duration: 720,
    taskQueue: 'ecommerce-agents',
    namespace: 'bizosaas-prod',
    input: { category: 'electronics', budget: 1000 },
    result: { productsFound: 45, bestOpportunity: 'smartphones' }
  },
  {
    id: 'wf_003',
    workflowId: 'analytics-report',
    runId: 'run_12347',
    workflowType: 'AnalyticsReportGeneration',
    status: 'failed',
    startTime: '2024-08-26T10:15:00Z',
    endTime: '2024-08-26T10:25:00Z',
    duration: 600,
    taskQueue: 'analytics-agents',
    namespace: 'bizosaas-prod',
    input: { reportType: 'performance', dateRange: '7d' },
    error: 'Failed to connect to analytics API'
  },
  {
    id: 'wf_004',
    workflowId: 'customer-support',
    runId: 'run_12348',
    workflowType: 'CustomerSupportWorkflow',
    status: 'completed',
    startTime: '2024-08-26T09:45:00Z',
    endTime: '2024-08-26T09:58:00Z',
    duration: 780,
    taskQueue: 'support-agents',
    namespace: 'bizosaas-prod',
    input: { ticketId: 'tick_567', priority: 'high' },
    result: { resolution: 'completed', satisfactionScore: 4.8 }
  }
]

const aiAgents: AIAgent[] = [
  {
    id: '1',
    name: 'Marketing Campaign Agent',
    type: 'marketing',
    company: 'TechStart Inc',
    status: 'active',
    performance: 94,
    tasks_today: 42,
    success_rate: 89.5,
    last_execution: '2024-08-26T10:45:00Z'
  },
  {
    id: '2',
    name: 'Product Research Agent',
    type: 'ecommerce',
    company: 'Fashion Forward',
    status: 'active',
    performance: 87,
    tasks_today: 28,
    success_rate: 92.1,
    last_execution: '2024-08-26T10:30:00Z'
  },
  {
    id: '3',
    name: 'Analytics Agent',
    type: 'analytics',
    company: 'Investment Firm',
    status: 'idle',
    performance: 98,
    tasks_today: 156,
    success_rate: 96.7,
    last_execution: '2024-08-26T09:15:00Z'
  },
  {
    id: '4',
    name: 'Support Agent',
    type: 'support',
    company: 'Local Restaurant',
    status: 'error',
    performance: 45,
    tasks_today: 3,
    success_rate: 67.2,
    last_execution: '2024-08-25T18:30:00Z'
  }
]

export default function SuperAdminPage() {
  const [selectedTimeRange, setSelectedTimeRange] = useState('7d')
  const [selectedPlatform, setSelectedPlatform] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')

  const filteredCompanies = companies.filter(company => {
    const matchesSearch = company.name.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesPlatform = selectedPlatform === 'all' || company.platform === selectedPlatform
    return matchesSearch && matchesPlatform
  })

  const totalMRR = companies.reduce((sum, company) => sum + company.subscription.mrr, 0)
  const totalUsers = companies.reduce((sum, company) => sum + company.users, 0)
  const totalRevenue = companies.reduce((sum, company) => sum + company.revenue, 0)
  const activeAgents = aiAgents.filter(agent => agent.status === 'active').length

  const getStatusBadge = (status: string, type: 'company' | 'subscription' | 'system' | 'agent' = 'company') => {
    const variants = {
      // Company statuses
      active: 'default' as const,
      inactive: 'secondary' as const,
      suspended: 'destructive' as const,
      trial: 'outline' as const,
      // Subscription statuses
      cancelled: 'secondary' as const,
      expired: 'destructive' as const,
      // System statuses
      healthy: 'default' as const,
      warning: 'outline' as const,
      critical: 'destructive' as const,
      // Agent statuses
      idle: 'secondary' as const,
      error: 'destructive' as const,
      maintenance: 'outline' as const
    }
    
    return (
      <Badge variant={variants[status as keyof typeof variants]} className="capitalize">
        {status}
      </Badge>
    )
  }

  const getPlatformIcon = (platform: string) => {
    const icons = {
      bizoholic: Bot,
      coreldove: ShoppingCart,
      thrillring: Activity,
      quanttrade: TrendingUp,
      'ai-assistant': Zap
    }
    const Icon = icons[platform as keyof typeof icons] || Building
    return <Icon className="h-4 w-4" />
  }

  const getChurnRiskColor = (risk: string) => {
    switch (risk) {
      case 'high': return 'text-red-600'
      case 'medium': return 'text-yellow-600'
      case 'low': return 'text-green-600'
      default: return 'text-gray-600'
    }
  }

  const getSystemStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy': return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'warning': return <AlertTriangle className="h-4 w-4 text-yellow-500" />
      case 'critical': return <XCircle className="h-4 w-4 text-red-500" />
      default: return <Clock className="h-4 w-4 text-gray-500" />
    }
  }

  const getAgentStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <Activity className="h-3 w-3 text-green-500" />
      case 'idle': return <Clock className="h-3 w-3 text-gray-500" />
      case 'error': return <XCircle className="h-3 w-3 text-red-500" />
      case 'maintenance': return <Settings className="h-3 w-3 text-yellow-500" />
      default: return <Clock className="h-3 w-3 text-gray-500" />
    }
  }

  const getWorkflowStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return <Play className="h-4 w-4 text-blue-500" />
      case 'completed': return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'failed': return <XCircle className="h-4 w-4 text-red-500" />
      case 'cancelled': return <Square className="h-4 w-4 text-gray-500" />
      case 'timeout': return <Timer className="h-4 w-4 text-yellow-500" />
      default: return <Clock className="h-4 w-4 text-gray-500" />
    }
  }

  const getWorkflowStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'text-blue-600 bg-blue-50'
      case 'completed': return 'text-green-600 bg-green-50'
      case 'failed': return 'text-red-600 bg-red-50'
      case 'cancelled': return 'text-gray-600 bg-gray-50'
      case 'timeout': return 'text-yellow-600 bg-yellow-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  const formatDuration = (seconds: number) => {
    if (seconds < 60) return `${seconds}s`
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${seconds % 60}s`
    return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`
  }

  return (
    <div className="flex-1 space-y-6 p-8 pt-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight flex items-center">
            <Crown className="h-8 w-8 text-yellow-500 mr-3" />
            Super Admin Dashboard
          </h2>
          <p className="text-muted-foreground">
            System overview and multi-company management across all platforms
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Export Report
          </Button>
          <Button variant="outline" size="sm">
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Global Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total MRR</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${totalMRR.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              <ArrowUpRight className="h-3 w-3 inline mr-1 text-green-600" />
              <span className="text-green-600">+12.5%</span> vs last month
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Users</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalUsers.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              <ArrowUpRight className="h-3 w-3 inline mr-1 text-green-600" />
              <span className="text-green-600">+8.2%</span> vs last month
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${(totalRevenue / 1000).toFixed(1)}k</div>
            <p className="text-xs text-muted-foreground">
              <ArrowUpRight className="h-3 w-3 inline mr-1 text-green-600" />
              <span className="text-green-600">+15.7%</span> vs last month
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active AI Agents</CardTitle>
            <Bot className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{activeAgents}</div>
            <p className="text-xs text-muted-foreground">
              <Activity className="h-3 w-3 inline mr-1" />
              {aiAgents.length} total agents
            </p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="companies" className="space-y-4">
        <TabsList className="grid w-full grid-cols-7">
          <TabsTrigger value="companies">Companies</TabsTrigger>
          <TabsTrigger value="system">System Health</TabsTrigger>
          <TabsTrigger value="agents">AI Agents</TabsTrigger>
          <TabsTrigger value="workflows">Workflows</TabsTrigger>
          <TabsTrigger value="monitoring">Monitoring</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="alerts">Alerts</TabsTrigger>
        </TabsList>

        <TabsContent value="companies" className="space-y-4">
          <div className="flex items-center gap-4 mb-4">
            <div className="flex items-center gap-2 flex-1">
              <Search className="h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search companies..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="max-w-sm"
              />
            </div>
            <Select value={selectedPlatform} onValueChange={setSelectedPlatform}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="All Platforms" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Platforms</SelectItem>
                <SelectItem value="bizoholic">Bizoholic</SelectItem>
                <SelectItem value="coreldove">CoreLDove</SelectItem>
                <SelectItem value="thrillring">ThrillRing</SelectItem>
                <SelectItem value="quanttrade">QuantTrade</SelectItem>
                <SelectItem value="ai-assistant">AI Assistant</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="outline" size="sm">
              <Filter className="h-4 w-4 mr-2" />
              Filter
            </Button>
          </div>

          <div className="grid gap-4">
            {filteredCompanies.map((company) => (
              <Card key={company.id}>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      {getPlatformIcon(company.platform)}
                      <div>
                        <h3 className="font-semibold">{company.name}</h3>
                        <p className="text-sm text-muted-foreground capitalize">
                          {company.platform} • {company.users} users
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <p className="text-sm font-medium">${company.subscription.mrr}/month</p>
                        <p className="text-xs text-muted-foreground">
                          {company.subscription.plan} plan
                        </p>
                      </div>
                      {getStatusBadge(company.status)}
                      <Button variant="ghost" size="sm">
                        <Eye className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-4 gap-4 mt-4 pt-4 border-t">
                    <div>
                      <p className="text-xs text-muted-foreground">Campaigns</p>
                      <p className="text-sm font-medium">{company.metrics.campaigns}</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">Leads</p>
                      <p className="text-sm font-medium">{company.metrics.leads.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">Conversion</p>
                      <p className="text-sm font-medium">{company.metrics.conversion_rate}%</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">Churn Risk</p>
                      <p className={`text-sm font-medium capitalize ${getChurnRiskColor(company.metrics.churn_risk)}`}>
                        {company.metrics.churn_risk}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="system" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {systemMetrics.map((metric) => {
              const Icon = metric.icon
              return (
                <Card key={metric.id}>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">{metric.name}</CardTitle>
                    <div className="flex items-center space-x-2">
                      {getSystemStatusIcon(metric.status)}
                      <Icon className="h-4 w-4 text-muted-foreground" />
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {metric.value}{metric.unit}
                    </div>
                    {metric.change && (
                      <p className="text-xs text-muted-foreground">
                        {metric.change > 0 ? (
                          <ArrowUpRight className="h-3 w-3 inline mr-1 text-green-600" />
                        ) : (
                          <ArrowDownRight className="h-3 w-3 inline mr-1 text-red-600" />
                        )}
                        <span className={metric.change > 0 ? 'text-green-600' : 'text-red-600'}>
                          {Math.abs(metric.change)}%
                        </span>
                        vs last hour
                      </p>
                    )}
                  </CardContent>
                </Card>
              )
            })}
          </div>

          <Card>
            <CardHeader>
              <CardTitle>System Alerts</CardTitle>
              <CardDescription>Recent system notifications and warnings</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <Alert>
                  <AlertTriangle className="h-4 w-4" />
                  <AlertDescription>
                    High memory usage detected on server cluster-02 (78% utilization)
                  </AlertDescription>
                </Alert>
                <Alert>
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>
                    Database connection pool approaching limit (145/200 connections)
                  </AlertDescription>
                </Alert>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="agents" className="space-y-4">
          <div className="grid gap-4">
            {aiAgents.map((agent) => (
              <Card key={agent.id}>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-2">
                        {getAgentStatusIcon(agent.status)}
                        <Bot className="h-5 w-5" />
                      </div>
                      <div>
                        <h3 className="font-semibold">{agent.name}</h3>
                        <p className="text-sm text-muted-foreground">
                          {agent.company} • {agent.type}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <p className="text-sm font-medium">{agent.performance}% performance</p>
                        <p className="text-xs text-muted-foreground">
                          {agent.success_rate}% success rate
                        </p>
                      </div>
                      {getStatusBadge(agent.status, 'agent')}
                      <Button variant="ghost" size="sm">
                        <Settings className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                  
                  <div className="mt-4 pt-4 border-t">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs text-muted-foreground">Performance</span>
                      <span className="text-xs font-medium">{agent.performance}%</span>
                    </div>
                    <Progress value={agent.performance} className="h-2" />
                    <div className="flex justify-between mt-2 text-xs text-muted-foreground">
                      <span>Tasks today: {agent.tasks_today}</span>
                      <span>Last: {new Date(agent.last_execution).toLocaleTimeString()}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="workflows" className="space-y-4">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-lg font-semibold">Temporal Workflow Engine</h3>
              <p className="text-sm text-muted-foreground">Monitor and manage all AI agent workflows across the platform</p>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" asChild>
                <a href="http://localhost:8088" target="_blank" rel="noopener noreferrer">
                  <ExternalLink className="h-4 w-4 mr-2" />
                  Open Full Dashboard
                </a>
              </Button>
              <Button variant="outline" size="sm">
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </Button>
            </div>
          </div>

          {/* Workflow Statistics */}
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Executions</CardTitle>
                <GitBranch className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{workflowStats.totalExecutions.toLocaleString()}</div>
                <p className="text-xs text-muted-foreground">
                  <ArrowUpRight className="h-3 w-3 inline mr-1 text-green-600" />
                  <span className="text-green-600">+23</span> in last hour
                </p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Currently Running</CardTitle>
                <Play className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{workflowStats.runningExecutions}</div>
                <p className="text-xs text-muted-foreground">
                  <Activity className="h-3 w-3 inline mr-1" />
                  Active workflows
                </p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
                <CheckCircle className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{workflowStats.successRate}%</div>
                <p className="text-xs text-muted-foreground">
                  <ArrowUpRight className="h-3 w-3 inline mr-1 text-green-600" />
                  <span className="text-green-600">+2.1%</span> vs last week
                </p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Avg Duration</CardTitle>
                <Timer className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{formatDuration(workflowStats.averageDuration)}</div>
                <p className="text-xs text-muted-foreground">
                  <ArrowDownRight className="h-3 w-3 inline mr-1 text-green-600" />
                  <span className="text-green-600">-15s</span> vs yesterday
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Embedded Temporal Dashboard */}
          <div className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Network className="h-5 w-5 mr-2" />
                  Temporal Web UI
                </CardTitle>
                <CardDescription>Live workflow monitoring and management interface</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="aspect-[16/10] border rounded-lg overflow-hidden bg-gray-50">
                  <iframe
                    src="http://localhost:8088"
                    className="w-full h-full"
                    title="Temporal Dashboard"
                    sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-popups-to-escape-sandbox"
                  />
                </div>
                <div className="mt-4 flex items-center justify-between text-sm text-muted-foreground">
                  <span>🔒 Protected by BizOSaas authentication</span>
                  <Button variant="ghost" size="sm" asChild>
                    <a href="http://localhost:8088" target="_blank" rel="noopener noreferrer">
                      <ExternalLink className="h-3 w-3 mr-1" />
                      Full Screen
                    </a>
                  </Button>
                </div>
              </CardContent>
            </Card>

            <div className="space-y-6">
              {/* Recent Workflow Executions */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-base">Recent Executions</CardTitle>
                  <CardDescription>Latest workflow runs across all namespaces</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {recentWorkflows.map((workflow) => (
                      <div key={workflow.id} className="flex items-start space-x-3 p-3 rounded-lg border">
                        <div className="flex-shrink-0 mt-0.5">
                          {getWorkflowStatusIcon(workflow.status)}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between">
                            <h4 className="text-sm font-medium truncate">{workflow.workflowType}</h4>
                            <Badge variant="outline" className={`text-xs ${getWorkflowStatusColor(workflow.status)}`}>
                              {workflow.status}
                            </Badge>
                          </div>
                          <p className="text-xs text-muted-foreground">
                            ID: {workflow.workflowId} • Queue: {workflow.taskQueue}
                          </p>
                          <div className="flex items-center justify-between mt-2 text-xs text-muted-foreground">
                            <span>Started: {new Date(workflow.startTime).toLocaleTimeString()}</span>
                            {workflow.duration && (
                              <span>Duration: {formatDuration(workflow.duration)}</span>
                            )}
                          </div>
                          {workflow.error && (
                            <p className="text-xs text-red-600 mt-1">{workflow.error}</p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Performance Metrics */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-base">Performance Overview</CardTitle>
                  <CardDescription>Workflow execution metrics</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span>Success Rate</span>
                        <span className="font-medium">{workflowStats.successRate}%</span>
                      </div>
                      <Progress value={workflowStats.successRate} className="h-2" />
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Completed</p>
                        <p className="font-medium text-green-600">{workflowStats.completedExecutions}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Failed</p>
                        <p className="font-medium text-red-600">{workflowStats.failedExecutions}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Throughput</p>
                        <p className="font-medium">{workflowStats.throughputPerMinute}/min</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Avg Time</p>
                        <p className="font-medium">{formatDuration(workflowStats.averageDuration)}</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="monitoring" className="space-y-4">
          <LoggingDashboard />
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Platform Performance</CardTitle>
                <CardDescription>Revenue and usage by platform</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Bot className="h-4 w-4" />
                      <span className="text-sm">Bizoholic</span>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium">$298/mo</p>
                      <p className="text-xs text-muted-foreground">2 companies</p>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <ShoppingCart className="h-4 w-4" />
                      <span className="text-sm">CoreLDove</span>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium">$449/mo</p>
                      <p className="text-xs text-muted-foreground">1 company</p>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <TrendingUp className="h-4 w-4" />
                      <span className="text-sm">QuantTrade</span>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium">$2,500/mo</p>
                      <p className="text-xs text-muted-foreground">1 company</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Growth Metrics</CardTitle>
                <CardDescription>Key growth indicators across all platforms</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Monthly Growth Rate</span>
                    <span className="text-sm font-medium text-green-600">+12.5%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Customer Acquisition Cost</span>
                    <span className="text-sm font-medium">$89</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Customer Lifetime Value</span>
                    <span className="text-sm font-medium">$2,140</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Churn Rate</span>
                    <span className="text-sm font-medium text-red-600">2.1%</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="alerts" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <AlertTriangle className="h-5 w-5 text-red-500 mr-2" />
                  Critical Alerts
                </CardTitle>
                <CardDescription>Immediate attention required</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <Alert>
                    <XCircle className="h-4 w-4" />
                    <AlertDescription>
                      Support Agent for Local Restaurant has been offline for 8 hours
                    </AlertDescription>
                  </Alert>
                  <Alert>
                    <AlertTriangle className="h-4 w-4" />
                    <AlertDescription>
                      High churn risk detected for Local Restaurant (trial ending in 2 days)
                    </AlertDescription>
                  </Alert>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <AlertCircle className="h-5 w-5 text-yellow-500 mr-2" />
                  Warnings
                </CardTitle>
                <CardDescription>Items to monitor closely</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <Alert>
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>
                      Memory usage trending upward on production servers
                    </AlertDescription>
                  </Alert>
                  <Alert>
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>
                      API response times increased by 15% in the last hour
                    </AlertDescription>
                  </Alert>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}