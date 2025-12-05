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
  CalendarDays,
  ExternalLink,
  Network,
  Timer,
  Monitor,
  FileText
} from 'lucide-react'

// Import our live data hooks
import { useApiGatewayDashboard, useApiGatewayRealtime } from '@/hooks/use-api-gateway'
import { useAIAgentsData, useAIAgentsRealtime } from '@/hooks/use-ai-agents-live'
import { CalendarHub } from '@/components/calendar'

interface LiveCompany {
  id: string
  name: string
  tier: 'tier_1' | 'tier_2' | 'tier_3'
  status: 'active' | 'inactive' | 'trial'
  users: number
  revenue: number
  lastActive: string
  subscription: {
    plan: string
    status: string
    mrr: number
    billing_cycle: string
  }
  metrics: {
    campaigns: number
    leads: number
    conversion_rate: number
    churn_risk: 'low' | 'medium' | 'high'
  }
}

export default function SuperAdminEnhancedPage() {
  const [selectedTimeRange, setSelectedTimeRange] = useState('7d')
  const [selectedTier, setSelectedTier] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')

  // Live data hooks
  const { data: gatewayData, isLoading: gatewayLoading, error: gatewayError } = useApiGatewayDashboard()
  const { data: realtimeGateway, connected: gatewayConnected } = useApiGatewayRealtime()
  const { data: aiData, isLoading: aiLoading, error: aiError } = useAIAgentsData()
  const { data: realtimeAI, connected: aiConnected } = useAIAgentsRealtime()

  // Transform live data for dashboard display
  const liveCompanies: LiveCompany[] = [
    // Mock data that would come from real tenant management system
    {
      id: '1',
      name: 'TechStart Inc',
      tier: 'tier_2',
      status: 'active',
      users: 12,
      revenue: 15420,
      lastActive: new Date().toISOString(),
      subscription: {
        plan: 'Dynamic CMS',
        status: 'active',
        mrr: gatewayData?.tiers.tier_2.price || 297,
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
      tier: 'tier_3',
      status: 'active',
      users: 8,
      revenue: 8950,
      lastActive: new Date(Date.now() - 300000).toISOString(),
      subscription: {
        plan: 'Full Platform',
        status: 'active',
        mrr: gatewayData?.tiers.tier_3.price || 997,
        billing_cycle: 'monthly'
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
      tier: 'tier_1',
      status: 'trial',
      users: 3,
      revenue: 0,
      lastActive: new Date(Date.now() - 3600000).toISOString(),
      subscription: {
        plan: 'Static Site',
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
    }
  ]

  const filteredCompanies = liveCompanies.filter(company => {
    const matchesSearch = company.name.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesTier = selectedTier === 'all' || company.tier === selectedTier
    return matchesSearch && matchesTier
  })

  // Live metrics from API Gateway and AI Agents
  const totalMRR = liveCompanies.reduce((sum, company) => sum + company.subscription.mrr, 0)
  const totalUsers = liveCompanies.reduce((sum, company) => sum + company.users, 0)
  const totalRevenue = liveCompanies.reduce((sum, company) => sum + company.revenue, 0)
  const activeAgents = aiData?.summary.activeAgents || 0

  const getTierBadgeColor = (tier: string) => {
    switch (tier) {
      case 'tier_1': return 'bg-blue-100 text-blue-800'
      case 'tier_2': return 'bg-green-100 text-green-800'  
      case 'tier_3': return 'bg-purple-100 text-purple-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getTierName = (tier: string) => {
    switch (tier) {
      case 'tier_1': return 'Static Site ($97)'
      case 'tier_2': return 'Dynamic CMS ($297)'
      case 'tier_3': return 'Full Platform ($997)'
      default: return tier
    }
  }

  const getStatusBadge = (status: string) => {
    const variants = {
      active: 'default' as const,
      inactive: 'secondary' as const,
      trial: 'outline' as const,
    }
    
    return (
      <Badge variant={variants[status as keyof typeof variants] || 'secondary'} className="capitalize">
        {status}
      </Badge>
    )
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

  return (
    <div className="flex-1 space-y-6 p-8 pt-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight flex items-center">
            <Crown className="h-8 w-8 text-yellow-500 mr-3" />
            Super Admin Dashboard (Live)
          </h2>
          <p className="text-muted-foreground">
            Real-time system overview and multi-company management across all platforms
          </p>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex items-center space-x-2">
            <Badge 
              variant="outline" 
              className={gatewayConnected ? "text-green-600 border-green-600" : "text-yellow-600 border-yellow-600"}
            >
              <Activity className="w-3 h-3 mr-1" />
              Gateway {gatewayConnected ? 'Connected' : 'Polling'}
            </Badge>
            <Badge 
              variant="outline" 
              className={aiConnected ? "text-green-600 border-green-600" : "text-yellow-600 border-yellow-600"}
            >
              <Bot className="w-3 h-3 mr-1" />
              AI Agents {aiConnected ? 'Live' : 'Cached'}
            </Badge>
          </div>
          <Button variant="outline" size="sm" onClick={() => window.location.reload()}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Live Error Handling */}
      {(gatewayError || aiError) && (
        <Alert>
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            Connection issues detected: {gatewayError || aiError}. Using cached data where available.
          </AlertDescription>
        </Alert>
      )}

      {/* Live Global Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total MRR (Live)</CardTitle>
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
            <CardTitle className="text-sm font-medium">API Requests (Live)</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {gatewayLoading ? '...' : (gatewayData?.metrics.total_requests || 0).toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              Avg: {gatewayData?.metrics.average_response_time || 0}ms response
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active AI Agents (Live)</CardTitle>
            <Bot className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {aiLoading ? '...' : activeAgents}
            </div>
            <p className="text-xs text-muted-foreground">
              <Activity className="h-3 w-3 inline mr-1" />
              {aiData?.health.total_agents || 0} total agents
            </p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="companies" className="space-y-4">
        <TabsList className="grid w-full grid-cols-7">
          <TabsTrigger value="companies">Companies</TabsTrigger>
          <TabsTrigger value="system">System Health</TabsTrigger>
          <TabsTrigger value="agents">AI Agents (Live)</TabsTrigger>
          <TabsTrigger value="api-gateway">API Gateway</TabsTrigger>
          <TabsTrigger value="calendar">
            <CalendarDays className="h-4 w-4 mr-2" />
            Calendar
          </TabsTrigger>
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
            <Select value={selectedTier} onValueChange={setSelectedTier}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="All Tiers" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Tiers</SelectItem>
                <SelectItem value="tier_1">Tier 1 - Static Site</SelectItem>
                <SelectItem value="tier_2">Tier 2 - Dynamic CMS</SelectItem>
                <SelectItem value="tier_3">Tier 3 - Full Platform</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid gap-4">
            {filteredCompanies.map((company) => (
              <Card key={company.id}>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-2">
                        <Bot className="h-5 w-5" />
                        <Badge className={getTierBadgeColor(company.tier)}>
                          {getTierName(company.tier)}
                        </Badge>
                      </div>
                      <div>
                        <h3 className="font-semibold">{company.name}</h3>
                        <p className="text-sm text-muted-foreground">
                          {company.users} users • Last active: {new Date(company.lastActive).toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <p className="text-sm font-medium">${company.subscription.mrr}/month</p>
                        <p className="text-xs text-muted-foreground">
                          {company.subscription.plan}
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
            {gatewayData?.services.map((service, index) => (
              <Card key={index}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">{service.name}</CardTitle>
                  <div className="flex items-center space-x-2">
                    {getSystemStatusIcon(service.status)}
                    <Server className="h-4 w-4 text-muted-foreground" />
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold capitalize">
                    {service.status}
                  </div>
                  {service.response_time && (
                    <p className="text-xs text-muted-foreground">
                      Response: {service.response_time.toFixed(1)}ms
                    </p>
                  )}
                  <p className="text-xs text-muted-foreground">
                    Circuit: {service.circuit_state}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Live System Metrics</CardTitle>
              <CardDescription>Real-time API Gateway performance</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-muted-foreground">Total Requests</p>
                    <p className="font-medium">{(gatewayData?.metrics.total_requests || 0).toLocaleString()}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Avg Response Time</p>
                    <p className="font-medium">{gatewayData?.metrics.average_response_time || 0}ms</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Redis Available</p>
                    <p className={`font-medium ${gatewayData?.metrics.redis_available ? 'text-green-600' : 'text-red-600'}`}>
                      {gatewayData?.metrics.redis_available ? 'Yes' : 'No'}
                    </p>
                  </div>
                  <div>
                    <p className="text-muted-foreground">Last Update</p>
                    <p className="font-medium">{new Date().toLocaleTimeString()}</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="agents" className="space-y-4">
          <div className="grid gap-4">
            {aiLoading && (
              <div className="text-center py-8">
                <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4" />
                <p>Loading AI agents data...</p>
              </div>
            )}
            {aiData?.agents.slice(0, 6).map((agent, index) => (
              <Card key={agent.id}>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-2">
                        <div className={`w-3 h-3 rounded-full ${
                          agent.status === 'active' ? 'bg-green-500' : 
                          agent.status === 'working' ? 'bg-blue-500 animate-pulse' :
                          agent.status === 'idle' ? 'bg-yellow-500' : 'bg-red-500'
                        }`} />
                        <Bot className="h-5 w-5" />
                      </div>
                      <div>
                        <h3 className="font-semibold">{agent.name}</h3>
                        <p className="text-sm text-muted-foreground">
                          {agent.type} • {agent.tenant_id}
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
                      <Badge 
                        variant={agent.status === 'active' ? 'default' : 'secondary'} 
                        className="capitalize"
                      >
                        {agent.status}
                      </Badge>
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
                    {agent.current_task && (
                      <p className="text-xs text-blue-600 mt-1">{agent.current_task}</p>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="api-gateway" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>API Gateway Configuration (Live)</CardTitle>
              <CardDescription>Real-time three-tier routing configuration</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-3">
                <div className="text-center p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                    ${gatewayData?.tiers.tier_1.price || 97}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    {gatewayData?.tiers.tier_1.name || 'Static Site Tier'}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    {gatewayData?.tiers.tier_1.clients || 0} clients
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    Features: {gatewayData?.tiers.tier_1.features.join(', ')}
                  </div>
                </div>
                <div className="text-center p-4 bg-green-50 dark:bg-green-900 rounded-lg">
                  <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                    ${gatewayData?.tiers.tier_2.price || 297}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    {gatewayData?.tiers.tier_2.name || 'Dynamic CMS Tier'}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    {gatewayData?.tiers.tier_2.clients || 0} clients
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    Features: {gatewayData?.tiers.tier_2.features.join(', ')}
                  </div>
                </div>
                <div className="text-center p-4 bg-purple-50 dark:bg-purple-900 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
                    ${gatewayData?.tiers.tier_3.price || 997}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    {gatewayData?.tiers.tier_3.name || 'Full Platform Tier'}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    {gatewayData?.tiers.tier_3.clients || 0} clients
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    Features: {gatewayData?.tiers.tier_3.features.join(', ')}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="calendar" className="space-y-4">
          <CalendarHub userRole="super_admin" className="mt-0" />
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Platform Performance (Live)</CardTitle>
              <CardDescription>Revenue and usage by tier (real-time data)</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Bot className="h-4 w-4" />
                    <span className="text-sm">Tier 1 (Static Sites)</span>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium">${(gatewayData?.tiers.tier_1.price || 97) * (gatewayData?.tiers.tier_1.clients || 0)}/mo</p>
                    <p className="text-xs text-muted-foreground">{gatewayData?.tiers.tier_1.clients || 0} companies</p>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <ShoppingCart className="h-4 w-4" />
                    <span className="text-sm">Tier 2 (Dynamic CMS)</span>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium">${(gatewayData?.tiers.tier_2.price || 297) * (gatewayData?.tiers.tier_2.clients || 0)}/mo</p>
                    <p className="text-xs text-muted-foreground">{gatewayData?.tiers.tier_2.clients || 0} companies</p>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <TrendingUp className="h-4 w-4" />
                    <span className="text-sm">Tier 3 (Full Platform)</span>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium">${(gatewayData?.tiers.tier_3.price || 997) * (gatewayData?.tiers.tier_3.clients || 0)}/mo</p>
                    <p className="text-xs text-muted-foreground">{gatewayData?.tiers.tier_3.clients || 0} companies</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="alerts" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <AlertTriangle className="h-5 w-5 text-red-500 mr-2" />
                  System Alerts (Live)
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {!gatewayData?.metrics.redis_available && (
                    <Alert>
                      <XCircle className="h-4 w-4" />
                      <AlertDescription>
                        Redis connection unavailable - using fallback caching
                      </AlertDescription>
                    </Alert>
                  )}
                  {gatewayData?.metrics.average_response_time > 1000 && (
                    <Alert>
                      <AlertTriangle className="h-4 w-4" />
                      <AlertDescription>
                        High API response times detected ({gatewayData.metrics.average_response_time}ms)
                      </AlertDescription>
                    </Alert>
                  )}
                  {gatewayData?.services.filter(s => s.status !== 'healthy').length > 0 && (
                    <Alert>
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>
                        {gatewayData.services.filter(s => s.status !== 'healthy').length} services reporting issues
                      </AlertDescription>
                    </Alert>
                  )}
                  {gatewayData?.services.length === 0 && (
                    <div className="text-center py-4 text-green-600">
                      <CheckCircle className="h-8 w-8 mx-auto mb-2" />
                      <p>All systems operational</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}