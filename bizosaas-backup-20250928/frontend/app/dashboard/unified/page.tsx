'use client'

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
  Settings,
  Activity,
  DollarSign,
  Target,
  CalendarDays,
  MessageCircle,
  Server,
  ShoppingCart,
  FileText,
  Database,
  AlertTriangle,
  CheckCircle,
  ExternalLink,
  RefreshCw,
  Monitor,
  Building2,
  ShoppingBag,
  Zap,
  Globe,
  Package,
  Play,
  Pause,
  Clock,
  Eye,
  Layers
} from 'lucide-react'
import { useState, useEffect } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { apiClient, type ServiceHealth, type PlatformOverview } from '@/lib/api-client'

// Service Health Monitoring Component
function ServiceHealthMonitor() {
  const [services, setServices] = useState<ServiceHealth[]>([])
  const [refreshing, setRefreshing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  const refreshServices = async () => {
    setRefreshing(true)
    setError(null)
    
    try {
      const healthData = await apiClient.getSystemHealth()
      setServices(healthData.services)
    } catch (err) {
      setError('Failed to connect to API Gateway. Please check if the service is running on port 8082.')
      console.error('Failed to refresh services:', err)
      
      // Set fallback services with offline status
      setServices([
        {
          name: 'API Gateway',
          type: 'FastAPI Gateway',
          url: 'http://localhost:8082',
          status: 'outage',
          uptime: 0,
          responseTime: 0,
          lastCheck: new Date(),
          metrics: {},
          description: 'Central API Gateway (Connection Failed)'
        },
        {
          name: 'Wagtail CMS',
          type: 'Content Management',
          url: 'http://localhost:8006',
          admin: 'http://localhost:8006/admin',
          status: 'operational',
          uptime: 99.2,
          responseTime: 198,
          lastCheck: new Date(),
          metrics: { pages: 67, posts: 234, media: 1567 },
          description: 'Multi-tenant content management system'
        },
        {
          name: 'Saleor E-commerce',
          type: 'E-commerce Platform', 
          url: 'http://localhost:9000',
          frontend: 'http://localhost:9000',
          status: 'operational',
          uptime: 98.7,
          responseTime: 267,
          lastCheck: new Date(),
          metrics: { organizations: 12, products: 2341, orders: 156 },
          description: 'Multi-tenant e-commerce with organization isolation'
        }
      ])
    } finally {
      setRefreshing(false)
    }
  }

  // Initial load
  useEffect(() => {
    refreshServices()
  }, [])
  
  useEffect(() => {
    const interval = setInterval(refreshServices, 30000) // Auto-refresh every 30s
    return () => clearInterval(interval)
  }, [])
  
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'operational': return 'text-green-600'
      case 'degraded': return 'text-yellow-600'
      case 'outage': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }
  
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'operational': return CheckCircle
      case 'degraded': return AlertTriangle
      case 'outage': return AlertTriangle
      default: return Monitor
    }
  }

  const getServiceIcon = (name: string) => {
    if (name.includes('Directory')) return Building2
    if (name.includes('E-commerce') || name.includes('CoreLDove')) return ShoppingBag
    if (name.includes('CMS') || name.includes('Wagtail')) return FileText
    if (name.includes('Website') || name.includes('Bizoholic')) return Globe
    if (name.includes('AI') || name.includes('Crew')) return Bot
    if (name.includes('Database') || name.includes('PostgreSQL')) return Database
    return Server
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-foreground">Platform Services Health</h3>
          <p className="text-sm text-muted-foreground">Real-time monitoring of all BizOSaaS services</p>
        </div>
        <Button 
          onClick={refreshServices} 
          disabled={refreshing}
          variant="outline"
          size="sm"
        >
          <RefreshCw className={`w-4 h-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      {error && (
        <Alert className="border-red-200 bg-red-50">
          <AlertTriangle className="h-4 w-4 text-red-600" />
          <AlertDescription className="text-red-800">
            {error}
          </AlertDescription>
        </Alert>
      )}
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {services.map((service, index) => {
          const StatusIcon = getStatusIcon(service.status)
          const ServiceIcon = getServiceIcon(service.name)
          return (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <ServiceIcon className="w-5 h-5 text-muted-foreground" />
                    <CardTitle className="text-sm font-medium">{service.name}</CardTitle>
                  </div>
                  <StatusIcon className={`w-4 h-4 ${getStatusColor(service.status)}`} />
                </div>
                <p className="text-xs text-muted-foreground">{service.type}</p>
                <p className="text-xs text-muted-foreground">{service.description}</p>
              </CardHeader>
              <CardContent className="pt-0">
                <div className="space-y-2">
                  <div className="flex justify-between items-center text-xs">
                    <span>Uptime</span>
                    <span className="font-medium">{service.uptime}%</span>
                  </div>
                  <Progress value={service.uptime} className="h-1" />
                  
                  <div className="flex justify-between items-center text-xs">
                    <span>Response Time</span>
                    <span className="font-medium">{Math.round(service.responseTime)}ms</span>
                  </div>
                  
                  <div className="flex justify-between items-center text-xs">
                    <span>Last Check</span>
                    <span className="font-medium">
                      {service.lastCheck.toLocaleTimeString()}
                    </span>
                  </div>
                  
                  <div className="flex items-center justify-between pt-2">
                    <Badge 
                      variant={service.status === 'operational' ? 'default' : 'destructive'}
                      className="text-xs"
                    >
                      {service.status}
                    </Badge>
                    <div className="flex space-x-1">
                      {service.frontend && (
                        <Button size="sm" variant="ghost" asChild>
                          <a href={service.frontend} target="_blank" rel="noopener noreferrer" title="Open Frontend">
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        </Button>
                      )}
                      {service.admin && (
                        <Button size="sm" variant="ghost" asChild>
                          <a href={service.admin} target="_blank" rel="noopener noreferrer" title="Open Admin">
                            <Settings className="w-3 h-3" />
                          </a>
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}

// Service Management Component
function ServiceManagement() {
  const services = [
    {
      category: 'Directory Services',
      icon: Building2,
      color: 'text-blue-600',
      items: [
        { 
          name: 'Business Directory API', 
          description: 'FastAPI backend for business listings',
          url: 'http://localhost:8000',
          actions: [
            { name: 'Restart', icon: RefreshCw },
            { name: 'View Logs', icon: Eye },
            { name: 'Configuration', icon: Settings }
          ]
        },
        { 
          name: 'Directory Frontend', 
          description: 'NextJS frontend for directory management',
          url: 'http://localhost:3002',
          actions: [
            { name: 'Deploy', icon: Zap },
            { name: 'View Logs', icon: Eye },
            { name: 'Performance', icon: TrendingUp }
          ]
        }
      ]
    },
    {
      category: 'E-commerce Platform',
      icon: ShoppingBag,
      color: 'text-green-600',
      items: [
        { 
          name: 'Saleor GraphQL API', 
          description: 'E-commerce backend and GraphQL API',
          url: 'http://localhost:8024',
          actions: [
            { name: 'Restart', icon: RefreshCw },
            { name: 'Database', icon: Database },
            { name: 'GraphQL Playground', icon: Play }
          ]
        },
        { 
          name: 'CoreLDove Storefront', 
          description: 'E-commerce storefront and admin',
          url: 'http://localhost:3001',
          actions: [
            { name: 'Deploy', icon: Zap },
            { name: 'Cache Clear', icon: RefreshCw },
            { name: 'View Analytics', icon: BarChart3 }
          ]
        }
      ]
    },
    {
      category: 'Content Management',
      icon: FileText,
      color: 'text-purple-600',
      items: [
        { 
          name: 'Wagtail CMS', 
          description: 'Content management system',
          url: 'http://localhost:8006/admin',
          actions: [
            { name: 'Restart', icon: RefreshCw },
            { name: 'Backup', icon: Database },
            { name: 'Media Management', icon: Package }
          ]
        }
      ]
    },
    {
      category: 'AI & Automation',
      icon: Bot,
      color: 'text-orange-600',
      items: [
        { 
          name: 'CrewAI Agents', 
          description: 'AI workflow automation system',
          url: 'http://localhost:8002',
          actions: [
            { name: 'Monitor', icon: Monitor },
            { name: 'Reset Agents', icon: RefreshCw },
            { name: 'View Tasks', icon: Layers }
          ]
        }
      ]
    }
  ]
  
  return (
    <div className="space-y-6">
      {services.map((category, idx) => (
        <div key={idx}>
          <div className="flex items-center space-x-2 mb-4">
            <category.icon className={`w-5 h-5 ${category.color}`} />
            <h3 className="text-lg font-semibold">{category.category}</h3>
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            {category.items.map((service, index) => (
              <Card key={index}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-base">{service.name}</CardTitle>
                    <Button size="sm" variant="ghost" asChild>
                      <a href={service.url} target="_blank" rel="noopener noreferrer">
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    </Button>
                  </div>
                  <p className="text-sm text-muted-foreground">{service.description}</p>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {service.actions.map((action, actionIdx) => (
                      <Button key={actionIdx} size="sm" variant="outline" className="flex items-center space-x-1">
                        <action.icon className="w-3 h-3" />
                        <span>{action.name}</span>
                      </Button>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

// Cross-Service Analytics Component
function CrossServiceAnalytics() {
  const analyticsData = {
    directory: {
      listings: 2341,
      categories: 67,
      views: 12567,
      leads: 89,
      conversion: 3.8,
      growth: '+12%'
    },
    ecommerce: {
      products: 4567,
      orders: 156,
      revenue: 45678,
      customers: 892,
      avgOrder: 293,
      growth: '+18%'
    },
    content: {
      pages: 67,
      posts: 234,
      media: 1567,
      views: 34521,
      engagement: 4.2,
      growth: '+8%'
    },
    ai: {
      agents: 23,
      tasks: 1567,
      success: 94.2,
      automation: 78,
      insights: 145,
      growth: '+15%'
    }
  }
  
  return (
    <div className="space-y-6">
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center">
              <Building2 className="w-4 h-4 mr-2 text-blue-600" />
              Directory Performance
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Total Listings</span>
                <span className="font-medium">{analyticsData.directory.listings.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Monthly Views</span>
                <span className="font-medium">{analyticsData.directory.views.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Conversion Rate</span>
                <span className="font-medium">{analyticsData.directory.conversion}%</span>
              </div>
              <div className="flex justify-between items-center pt-2">
                <span className="text-xs text-muted-foreground">Growth</span>
                <Badge variant="outline" className="text-green-600 border-green-200">
                  {analyticsData.directory.growth}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center">
              <ShoppingBag className="w-4 h-4 mr-2 text-green-600" />
              E-commerce Stats
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Products</span>
                <span className="font-medium">{analyticsData.ecommerce.products.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Monthly Revenue</span>
                <span className="font-medium">${analyticsData.ecommerce.revenue.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Avg Order Value</span>
                <span className="font-medium">${analyticsData.ecommerce.avgOrder}</span>
              </div>
              <div className="flex justify-between items-center pt-2">
                <span className="text-xs text-muted-foreground">Growth</span>
                <Badge variant="outline" className="text-green-600 border-green-200">
                  {analyticsData.ecommerce.growth}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center">
              <FileText className="w-4 h-4 mr-2 text-purple-600" />
              Content Metrics
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Total Pages</span>
                <span className="font-medium">{analyticsData.content.pages}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Monthly Views</span>
                <span className="font-medium">{analyticsData.content.views.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Engagement Score</span>
                <span className="font-medium">{analyticsData.content.engagement}/5</span>
              </div>
              <div className="flex justify-between items-center pt-2">
                <span className="text-xs text-muted-foreground">Growth</span>
                <Badge variant="outline" className="text-green-600 border-green-200">
                  {analyticsData.content.growth}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center">
              <Bot className="w-4 h-4 mr-2 text-orange-600" />
              AI Performance
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Active Agents</span>
                <span className="font-medium">{analyticsData.ai.agents}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Success Rate</span>
                <span className="font-medium">{analyticsData.ai.success}%</span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Automation %</span>
                <span className="font-medium">{analyticsData.ai.automation}%</span>
              </div>
              <div className="flex justify-between items-center pt-2">
                <span className="text-xs text-muted-foreground">Growth</span>
                <Badge variant="outline" className="text-green-600 border-green-200">
                  {analyticsData.ai.growth}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

// Client Management Component
function ClientManagement() {
  const clients = [
    {
      name: 'Tech Solutions Ltd',
      tier: 'Enterprise',
      services: ['Directory', 'E-commerce', 'AI Agents'],
      revenue: 4500,
      status: 'active',
      lastActivity: '2 hours ago'
    },
    {
      name: 'Local Restaurant Chain',
      tier: 'Pro',
      services: ['Directory', 'CMS'],
      revenue: 1200,
      status: 'active',
      lastActivity: '5 hours ago'
    },
    {
      name: 'Fashion Boutique',
      tier: 'Starter',
      services: ['E-commerce'],
      revenue: 800,
      status: 'trial',
      lastActivity: '1 day ago'
    }
  ]

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {clients.map((client, index) => (
          <Card key={index} className="hover:shadow-lg transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm font-medium">{client.name}</CardTitle>
                <Badge 
                  variant={client.status === 'active' ? 'default' : 'outline'}
                  className="text-xs"
                >
                  {client.tier}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Monthly Revenue</span>
                  <span className="font-medium">${client.revenue}</span>
                </div>
                <div className="text-xs text-muted-foreground">
                  Services: {client.services.join(', ')}
                </div>
                <div className="flex justify-between items-center pt-2">
                  <span className="text-xs text-muted-foreground">Last Activity: {client.lastActivity}</span>
                  <div className={`w-2 h-2 rounded-full ${
                    client.status === 'active' ? 'bg-green-500' : 'bg-yellow-500'
                  }`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

export default function UnifiedDashboardPage() {
  const [activeTab, setActiveTab] = useState('overview')
  const [platformOverview, setPlatformOverview] = useState<PlatformOverview>({
    totalServices: 0,
    operationalServices: 0,
    totalUsers: 0,
    monthlyRevenue: 0,
    aiTasks: 0,
    systemLoad: 0
  })
  const [loading, setLoading] = useState(true)

  // Load platform overview on component mount
  useEffect(() => {
    const loadPlatformData = async () => {
      try {
        const overview = await apiClient.getPlatformOverview()
        setPlatformOverview(overview)
      } catch (error) {
        console.error('Failed to load platform overview:', error)
      } finally {
        setLoading(false)
      }
    }

    loadPlatformData()
  }, [])

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="border-b pb-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-foreground">BizOSaaS Unified Dashboard</h1>
            <p className="text-muted-foreground mt-2">
              Central command center for all platform services - Directory, E-commerce, CMS, AI Agents, and Analytics.
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <Badge variant="outline" className="text-green-600 border-green-600">
              <CheckCircle className="w-3 h-3 mr-1" />
              All Systems Operational
            </Badge>
            <Badge variant="outline" className="text-blue-600 border-blue-600">
              <Activity className="w-3 h-3 mr-1" />
              {platformOverview.totalUsers} users online
            </Badge>
            <Button size="sm">
              <Settings className="w-4 h-4 mr-2" />
              Configure
            </Button>
          </div>
        </div>
        
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full max-w-4xl grid-cols-7">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="services">Services</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="clients">Clients</TabsTrigger>
            <TabsTrigger value="ai-agents">AI Agents</TabsTrigger>
            <TabsTrigger value="branding">Branding</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-8 mt-8">
            {/* Platform Health Summary */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium flex items-center">
                    <Server className="w-4 h-4 mr-2 text-green-600" />
                    System Health
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-green-600">
                    {platformOverview.operationalServices}/{platformOverview.totalServices}
                  </div>
                  <p className="text-sm text-muted-foreground">Services Operational</p>
                  <Progress value={(platformOverview.operationalServices / platformOverview.totalServices) * 100} className="h-1 mt-2" />
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium flex items-center">
                    <Users className="w-4 h-4 mr-2 text-blue-600" />
                    Active Users
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{platformOverview.totalUsers.toLocaleString()}</div>
                  <p className="text-sm text-muted-foreground">Across all platforms</p>
                  <div className="flex items-center text-xs text-green-600 mt-2">
                    <ArrowUpRight className="w-3 h-3 mr-1" />
                    +12% from yesterday
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium flex items-center">
                    <DollarSign className="w-4 h-4 mr-2 text-green-600" />
                    Total Revenue
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">${platformOverview.monthlyRevenue.toLocaleString()}</div>
                  <p className="text-sm text-muted-foreground">This month</p>
                  <div className="flex items-center text-xs text-green-600 mt-2">
                    <ArrowUpRight className="w-3 h-3 mr-1" />
                    +18% from last month
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium flex items-center">
                    <Bot className="w-4 h-4 mr-2 text-purple-600" />
                    AI Tasks
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{platformOverview.aiTasks}</div>
                  <p className="text-sm text-muted-foreground">Running workflows</p>
                  <div className="flex items-center text-xs text-blue-600 mt-2">
                    <Clock className="w-3 h-3 mr-1" />
                    94.2% success rate
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Quick Service Overview */}
            <Card>
              <CardHeader>
                <CardTitle>Quick Service Overview</CardTitle>
                <p className="text-sm text-muted-foreground">
                  High-level status of all platform services
                </p>
              </CardHeader>
              <CardContent>
                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                  <div className="flex items-center space-x-3">
                    <Building2 className="w-8 h-8 text-blue-600" />
                    <div>
                      <h3 className="font-medium">Business Directory</h3>
                      <p className="text-sm text-muted-foreground">2,341 listings • 89 leads</p>
                      <Badge variant="outline" className="text-xs mt-1">API + Frontend</Badge>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <ShoppingBag className="w-8 h-8 text-green-600" />
                    <div>
                      <h3 className="font-medium">E-commerce Platform</h3>
                      <p className="text-sm text-muted-foreground">4,567 products • $45k revenue</p>
                      <Badge variant="outline" className="text-xs mt-1">Saleor + Storefront</Badge>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <FileText className="w-8 h-8 text-purple-600" />
                    <div>
                      <h3 className="font-medium">Content Management</h3>
                      <p className="text-sm text-muted-foreground">67 pages • 234 posts</p>
                      <Badge variant="outline" className="text-xs mt-1">Wagtail CMS</Badge>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <Globe className="w-8 h-8 text-orange-600" />
                    <div>
                      <h3 className="font-medium">Marketing Website</h3>
                      <p className="text-sm text-muted-foreground">3,421 visitors • 12 campaigns</p>
                      <Badge variant="outline" className="text-xs mt-1">NextJS</Badge>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <Bot className="w-8 h-8 text-yellow-600" />
                    <div>
                      <h3 className="font-medium">AI Agent System</h3>
                      <p className="text-sm text-muted-foreground">23 agents • 156 tasks</p>
                      <Badge variant="outline" className="text-xs mt-1">CrewAI</Badge>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <Database className="w-8 h-8 text-red-600" />
                    <div>
                      <h3 className="font-medium">Database System</h3>
                      <p className="text-sm text-muted-foreground">45 connections • 2.3GB</p>
                      <Badge variant="outline" className="text-xs mt-1">PostgreSQL</Badge>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Service Integration Flow */}
            <Card>
              <CardHeader>
                <CardTitle>Service Integration Flow</CardTitle>
                <p className="text-sm text-muted-foreground">
                  Data flow and integration between platform services
                </p>
              </CardHeader>
              <CardContent>
                <div className="bg-muted/50 rounded-lg p-6">
                  <div className="flex items-center justify-center space-x-4 text-sm flex-wrap">
                    <div className="flex items-center space-x-2">
                      <Building2 className="w-5 h-5 text-blue-600" />
                      <span>Directory</span>
                    </div>
                    <ArrowUpRight className="w-4 h-4 text-muted-foreground" />
                    <div className="flex items-center space-x-2">
                      <Bot className="w-5 h-5 text-purple-600" />
                      <span>AI Agents</span>
                    </div>
                    <ArrowUpRight className="w-4 h-4 text-muted-foreground" />
                    <div className="flex items-center space-x-2">
                      <ShoppingBag className="w-5 h-5 text-green-600" />
                      <span>E-commerce</span>
                    </div>
                    <ArrowUpRight className="w-4 h-4 text-muted-foreground" />
                    <div className="flex items-center space-x-2">
                      <FileText className="w-5 h-5 text-orange-600" />
                      <span>CMS</span>
                    </div>
                  </div>
                  <p className="text-center text-xs text-muted-foreground mt-4">
                    Real-time data synchronization and automated workflows
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          
          {/* Services Management Tab */}
          <TabsContent value="services" className="space-y-6 mt-8">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-foreground">Service Management</h2>
                <p className="text-muted-foreground">
                  Monitor and manage all BizOSaaS platform services from one central location.
                </p>
              </div>
              <div className="flex space-x-2">
                <Button size="sm" variant="outline">
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Refresh All
                </Button>
                <Button size="sm">
                  <Settings className="w-4 h-4 mr-2" />
                  Global Settings
                </Button>
              </div>
            </div>
            
            <ServiceHealthMonitor />
            
            <div className="mt-8">
              <h3 className="text-lg font-semibold mb-4">Service Actions</h3>
              <ServiceManagement />
            </div>
          </TabsContent>
          
          {/* Cross-Service Analytics Tab */}
          <TabsContent value="analytics" className="space-y-6 mt-8">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-foreground">Cross-Service Analytics</h2>
                <p className="text-muted-foreground">
                  Unified analytics across directory, e-commerce, content, and AI services.
                </p>
              </div>
              <Button size="sm">
                <BarChart3 className="w-4 h-4 mr-2" />
                Export Report
              </Button>
            </div>
            
            <CrossServiceAnalytics />
          </TabsContent>

          {/* Client Management Tab */}
          <TabsContent value="clients" className="space-y-6 mt-8">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-foreground">Client Management</h2>
                <p className="text-muted-foreground">
                  Multi-tenant client dashboard and onboarding workflows.
                </p>
              </div>
              <Button size="sm">
                <Users className="w-4 h-4 mr-2" />
                Add Client
              </Button>
            </div>
            
            <ClientManagement />
          </TabsContent>

          {/* AI Agents Tab */}
          <TabsContent value="ai-agents" className="space-y-6 mt-8">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-foreground">AI Agents Management</h2>
                <p className="text-muted-foreground">
                  Monitor and configure your 6 specialized AI agents.
                </p>
              </div>
              <Button size="sm">
                <Bot className="w-4 h-4 mr-2" />
                Configure Agents
              </Button>
            </div>
            
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {[
                { 
                  name: 'Content Creator Agent', 
                  status: 'active', 
                  performance: 98, 
                  tasks: 12,
                  description: 'Generates marketing content and blog posts',
                  lastTask: 'Created 3 blog posts for client XYZ'
                },
                { 
                  name: 'SEO Optimizer Agent', 
                  status: 'working', 
                  performance: 96, 
                  tasks: 8,
                  description: 'Optimizes content for search engines',
                  lastTask: 'Analyzing keyword performance'
                },
                { 
                  name: 'Social Media Agent', 
                  status: 'active', 
                  performance: 94, 
                  tasks: 15,
                  description: 'Manages social media campaigns',
                  lastTask: 'Scheduled 10 social posts'
                },
                { 
                  name: 'Lead Generator Agent', 
                  status: 'working', 
                  performance: 92, 
                  tasks: 6,
                  description: 'Identifies and qualifies leads',
                  lastTask: 'Qualifying 25 new leads'
                },
                { 
                  name: 'Campaign Analyzer Agent', 
                  status: 'idle', 
                  performance: 89, 
                  tasks: 0,
                  description: 'Analyzes campaign performance',
                  lastTask: 'Generated performance report'
                },
                { 
                  name: 'Competitor Research Agent', 
                  status: 'active', 
                  performance: 87, 
                  tasks: 4,
                  description: 'Monitors competitor activities',
                  lastTask: 'Analyzed 5 competitor websites'
                }
              ].map((agent, index) => (
                <Card key={index} className="hover:shadow-lg transition-shadow">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-medium">{agent.name}</h3>
                      <div className={`w-2 h-2 rounded-full ${
                        agent.status === 'active' ? 'bg-green-500' : 
                        agent.status === 'working' ? 'bg-blue-500 animate-pulse' :
                        'bg-gray-400'
                      }`} />
                    </div>
                    <p className="text-xs text-muted-foreground mb-2">{agent.description}</p>
                    <div className="text-sm text-muted-foreground mb-2">
                      {agent.status === 'working' ? 'Currently working...' : 
                       agent.status === 'active' ? 'Ready for tasks' :
                       'Idle - Waiting for activation'}
                    </div>
                    <div className="text-xs text-muted-foreground mb-2">
                      Last: {agent.lastTask}
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
          </TabsContent>

          {/* Branding Management Tab */}
          <TabsContent value="branding" className="space-y-6 mt-8">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-foreground">Brand Management</h2>
                <p className="text-muted-foreground">
                  Manage logos, branding, and visual assets across all platform services.
                </p>
              </div>
              <Button size="sm">
                <Package className="w-4 h-4 mr-2" />
                Upload Assets
              </Button>
            </div>
            
            <div className="grid gap-6 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle>Platform Branding</CardTitle>
                  <p className="text-sm text-muted-foreground">
                    Manage the main platform logo and branding elements
                  </p>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label>Current Logo</Label>
                    <div className="flex items-center space-x-4 p-4 border rounded-lg">
                      <img 
                        src="/bizoholic-logo-hq.png" 
                        alt="Current Logo" 
                        className="h-12 w-auto"
                      />
                      <div>
                        <p className="font-medium">bizoholic-logo-hq.png</p>
                        <p className="text-sm text-muted-foreground">500x500px, PNG</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <Label>Platform Name</Label>
                    <Input defaultValue="Bizoholic Digital" />
                  </div>
                  
                  <div className="space-y-2">
                    <Label>Primary Color</Label>
                    <div className="flex items-center space-x-2">
                      <div className="w-10 h-10 bg-primary rounded border"></div>
                      <Input defaultValue="#3B82F6" className="flex-1" />
                    </div>
                  </div>
                  
                  <div className="flex space-x-2">
                    <Button variant="outline" className="flex-1">
                      <Eye className="w-4 h-4 mr-2" />
                      Preview
                    </Button>
                    <Button className="flex-1">
                      <RefreshCw className="w-4 h-4 mr-2" />
                      Update
                    </Button>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Service Branding</CardTitle>
                  <p className="text-sm text-muted-foreground">
                    Customize branding for individual services
                  </p>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 border rounded">
                      <div className="flex items-center space-x-3">
                        <Globe className="h-5 w-5 text-muted-foreground" />
                        <div>
                          <p className="font-medium">Marketing Website</p>
                          <p className="text-sm text-muted-foreground">localhost:3000</p>
                        </div>
                      </div>
                      <Button size="sm" variant="outline">Edit</Button>
                    </div>
                    
                    <div className="flex items-center justify-between p-3 border rounded">
                      <div className="flex items-center space-x-3">
                        <Monitor className="h-5 w-5 text-muted-foreground" />
                        <div>
                          <p className="font-medium">Admin Dashboard</p>
                          <p className="text-sm text-muted-foreground">localhost:3005</p>
                        </div>
                      </div>
                      <Button size="sm" variant="outline">Edit</Button>
                    </div>
                    
                    <div className="flex items-center justify-between p-3 border rounded">
                      <div className="flex items-center space-x-3">
                        <FileText className="h-5 w-5 text-muted-foreground" />
                        <div>
                          <p className="font-medium">Wagtail CMS</p>
                          <p className="text-sm text-muted-foreground">localhost:8006</p>
                        </div>
                      </div>
                      <Button size="sm" variant="outline">Edit</Button>
                    </div>
                    
                    <div className="flex items-center justify-between p-3 border rounded">
                      <div className="flex items-center space-x-3">
                        <ShoppingBag className="h-5 w-5 text-muted-foreground" />
                        <div>
                          <p className="font-medium">Saleor E-commerce</p>
                          <p className="text-sm text-muted-foreground">localhost:9000</p>
                        </div>
                      </div>
                      <Button size="sm" variant="outline">Edit</Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <CardTitle>Asset Library</CardTitle>
                  <p className="text-sm text-muted-foreground">
                    Manage logos, icons, and other brand assets
                  </p>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="grid grid-cols-3 gap-4">
                      <div className="aspect-square border rounded-lg p-4 flex items-center justify-center bg-muted/30">
                        <img 
                          src="/bizoholic-logo-hq.png" 
                          alt="Logo" 
                          className="max-h-full max-w-full"
                        />
                      </div>
                      <div className="aspect-square border rounded-lg p-4 flex items-center justify-center bg-muted/30">
                        <div className="text-4xl">🚀</div>
                      </div>
                      <div className="aspect-square border-2 border-dashed border-muted-foreground/25 rounded-lg flex items-center justify-center cursor-pointer hover:bg-muted/30 transition-colors">
                        <div className="text-center">
                          <div className="text-2xl mb-2">+</div>
                          <p className="text-xs text-muted-foreground">Upload</p>
                        </div>
                      </div>
                    </div>
                    
                    <Button variant="outline" className="w-full">
                      <Package className="w-4 h-4 mr-2" />
                      Manage Asset Library
                    </Button>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Theme Settings</CardTitle>
                  <p className="text-sm text-muted-foreground">
                    Configure global theme and appearance settings
                  </p>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label>Theme Mode</Label>
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm" className="flex-1">Light</Button>
                      <Button variant="outline" size="sm" className="flex-1">Dark</Button>
                      <Button variant="default" size="sm" className="flex-1">Auto</Button>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <Label>Font Family</Label>
                    <select className="w-full p-2 border rounded">
                      <option>Inter (Default)</option>
                      <option>Roboto</option>
                      <option>Open Sans</option>
                      <option>Poppins</option>
                    </select>
                  </div>
                  
                  <div className="space-y-2">
                    <Label>Border Radius</Label>
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm">None</Button>
                      <Button variant="default" size="sm">Medium</Button>
                      <Button variant="outline" size="sm">Large</Button>
                    </div>
                  </div>
                  
                  <Button className="w-full">
                    Apply Theme Changes
                  </Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Settings Tab */}
          <TabsContent value="settings" className="space-y-6 mt-8">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-foreground">Platform Settings</h2>
                <p className="text-muted-foreground">
                  Global configuration and integrations for the entire platform.
                </p>
              </div>
            </div>
            
            <div className="grid gap-6 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle>System Configuration</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Button variant="outline" className="w-full justify-start">
                    <Settings className="w-4 h-4 mr-2" />
                    General Settings
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Database className="w-4 h-4 mr-2" />
                    Database Configuration
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Zap className="w-4 h-4 mr-2" />
                    API Configuration
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Integrations</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Button variant="outline" className="w-full justify-start">
                    <Bot className="w-4 h-4 mr-2" />
                    AI Services
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <MessageCircle className="w-4 h-4 mr-2" />
                    Communication
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <BarChart3 className="w-4 h-4 mr-2" />
                    Analytics
                  </Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}