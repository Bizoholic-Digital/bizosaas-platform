'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import { Textarea } from '@/components/ui/textarea'
import { Progress } from '@/components/ui/progress'
import { 
  Globe, 
  Database, 
  Cloud, 
  Settings, 
  CheckCircle, 
  AlertCircle, 
  Clock, 
  Activity,
  Zap,
  Shield,
  Key,
  RefreshCw,
  Play,
  Pause,
  Eye,
  EyeOff,
  Plus,
  Trash2,
  Edit,
  Search,
  Filter,
  Download,
  Upload,
  Link,
  Unlink,
  BarChart3,
  TrendingUp,
  Users,
  MessageSquare,
  Mail,
  ShoppingCart,
  CreditCard,
  FileText,
  Calendar,
  Phone,
  Video,
  Image,
  Music,
  Map,
  Cpu,
  Code,
  ExternalLink,
  AlertTriangle,
  Info
} from 'lucide-react'

// API Integration types
interface APIIntegration {
  id: string
  name: string
  description: string
  category: string
  provider: string
  status: 'connected' | 'disconnected' | 'error' | 'configuring'
  healthStatus: 'healthy' | 'degraded' | 'down'
  lastHealthCheck: Date
  responseTime: number
  uptime: number
  rateLimitUsed: number
  rateLimitTotal: number
  requestsToday: number
  errorsToday: number
  successRate: number
  credentials: {
    type: 'api_key' | 'oauth' | 'basic_auth' | 'bearer_token'
    configured: boolean
    expiresAt?: Date
  }
  endpoints: APIEndpoint[]
  webhooks: Webhook[]
  configuration: Record<string, any>
}

interface APIEndpoint {
  id: string
  name: string
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
  path: string
  description: string
  lastUsed: Date
  requestCount: number
  avgResponseTime: number
  errorRate: number
}

interface Webhook {
  id: string
  name: string
  url: string
  events: string[]
  isActive: boolean
  lastTriggered?: Date
  successRate: number
}

// Business category definitions with icons and colors
const BUSINESS_CATEGORIES = {
  'social-media': { 
    name: 'Social Media', 
    icon: Users, 
    color: 'bg-pink-500',
    integrations: [
      'Facebook Graph API', 'Instagram Basic Display', 'Twitter API v2', 'LinkedIn Marketing API',
      'TikTok Business API', 'YouTube Data API', 'Pinterest API', 'Snapchat Marketing API',
      'Discord Bot API', 'Reddit API', 'Telegram Bot API', 'WhatsApp Business API'
    ]
  },
  'e-commerce': { 
    name: 'E-commerce', 
    icon: ShoppingCart, 
    color: 'bg-green-500',
    integrations: [
      'Shopify API', 'WooCommerce REST API', 'Amazon MWS', 'eBay Trading API',
      'Etsy Open API', 'BigCommerce API', 'Magento REST API', 'Square API',
      'Stripe API', 'PayPal API', 'Klarna API', 'Saleor GraphQL API'
    ]
  },
  'llm-providers': { 
    name: 'LLM Providers', 
    icon: Cpu, 
    color: 'bg-purple-500',
    integrations: [
      'OpenAI API', 'Anthropic Claude API', 'Google PaLM API', 'Cohere API',
      'Hugging Face API', 'Azure OpenAI', 'AWS Bedrock', 'Mistral AI API'
    ]
  },
  'productivity': { 
    name: 'Productivity', 
    icon: FileText, 
    color: 'bg-blue-500',
    integrations: [
      'Google Workspace API', 'Microsoft Graph API', 'Slack API', 'Notion API',
      'Airtable API', 'Trello API', 'Asana API', 'Monday.com API', 'Zapier API'
    ]
  },
  'email-marketing': { 
    name: 'Email Marketing', 
    icon: Mail, 
    color: 'bg-red-500',
    integrations: [
      'Mailchimp API', 'SendGrid API', 'Constant Contact API', 'Campaign Monitor API',
      'ConvertKit API', 'AWeber API', 'GetResponse API'
    ]
  },
  'analytics': { 
    name: 'Analytics', 
    icon: BarChart3, 
    color: 'bg-yellow-500',
    integrations: [
      'Google Analytics API', 'Adobe Analytics API', 'Mixpanel API', 'Amplitude API',
      'Hotjar API', 'Crazy Egg API', 'Segment API', 'Heap Analytics API'
    ]
  },
  'crm-sales': { 
    name: 'CRM & Sales', 
    icon: Users, 
    color: 'bg-indigo-500',
    integrations: [
      'Salesforce API', 'HubSpot API', 'Pipedrive API', 'Zoho CRM API',
      'Freshsales API', 'ActiveCampaign API', 'Intercom API', 'Zendesk API',
      'Calendly API', 'Acuity Scheduling API', 'Close.com API'
    ]
  },
  'content-creation': { 
    name: 'Content Creation', 
    icon: Image, 
    color: 'bg-teal-500',
    integrations: [
      'Canva API', 'Adobe Creative SDK', 'Unsplash API', 'Pexels API',
      'Figma API', 'Loom API'
    ]
  },
  'seo-tools': { 
    name: 'SEO Tools', 
    icon: TrendingUp, 
    color: 'bg-gray-500',
    integrations: [
      'Google Search Console API', 'SEMrush API', 'Ahrefs API', 'Moz API',
      'Screaming Frog API'
    ]
  },
  'advertising': { 
    name: 'Advertising', 
    icon: Globe, 
    color: 'bg-orange-500',
    integrations: [
      'Google Ads API', 'Facebook Marketing API', 'Microsoft Advertising API',
      'LinkedIn Marketing API', 'Twitter Ads API', 'TikTok Marketing API',
      'Pinterest Business API'
    ]
  },
  'communication': { 
    name: 'Communication', 
    icon: MessageSquare, 
    color: 'bg-cyan-500',
    integrations: [
      'Twilio API', 'Zoom API', 'Microsoft Teams API', 'Slack API'
    ]
  },
  'automation': { 
    name: 'Automation', 
    icon: Zap, 
    color: 'bg-lime-500',
    integrations: [
      'Zapier API', 'IFTTT API', 'Microsoft Power Automate', 'n8n API',
      'Make (Integromat) API', 'Automate.io API', 'Workato API', 'Temporal API'
    ]
  },
  'project-management': { 
    name: 'Project Management', 
    icon: Calendar, 
    color: 'bg-rose-500',
    integrations: [
      'Jira API', 'GitHub API', 'GitLab API'
    ]
  }
}

// Generate mock integrations
const generateMockIntegrations = (): APIIntegration[] => {
  const integrations: APIIntegration[] = []
  let integrationId = 1

  Object.entries(BUSINESS_CATEGORIES).forEach(([categoryKey, category]) => {
    category.integrations.forEach((integrationName) => {
      const status = ['connected', 'disconnected', 'error', 'configuring'][Math.floor(Math.random() * 4)] as any
      const healthStatus = status === 'connected' 
        ? (['healthy', 'degraded', 'down'][Math.floor(Math.random() * 3)]) as any
        : 'down'
      
      integrations.push({
        id: `integration-${integrationId++}`,
        name: integrationName,
        description: `${integrationName} integration for ${category.name.toLowerCase()}`,
        category: categoryKey,
        provider: integrationName.split(' ')[0],
        status,
        healthStatus,
        lastHealthCheck: new Date(Date.now() - Math.random() * 3600000),
        responseTime: Math.floor(Math.random() * 500) + 50,
        uptime: Math.floor(Math.random() * 20) + 80,
        rateLimitUsed: Math.floor(Math.random() * 800),
        rateLimitTotal: 1000,
        requestsToday: Math.floor(Math.random() * 5000),
        errorsToday: Math.floor(Math.random() * 50),
        successRate: Math.floor(Math.random() * 20) + 80,
        credentials: {
          type: ['api_key', 'oauth', 'basic_auth', 'bearer_token'][Math.floor(Math.random() * 4)] as any,
          configured: status !== 'disconnected',
          expiresAt: Math.random() > 0.5 ? new Date(Date.now() + 30 * 24 * 3600000) : undefined
        },
        endpoints: [
          {
            id: 'endpoint-1',
            name: 'GET Data',
            method: 'GET',
            path: '/api/v1/data',
            description: 'Retrieve data',
            lastUsed: new Date(),
            requestCount: Math.floor(Math.random() * 1000),
            avgResponseTime: Math.floor(Math.random() * 300) + 100,
            errorRate: Math.random() * 5
          }
        ],
        webhooks: [
          {
            id: 'webhook-1',
            name: 'Data Update Webhook',
            url: 'https://api.bizosaas.com/webhooks/data-update',
            events: ['data.created', 'data.updated'],
            isActive: Math.random() > 0.3,
            lastTriggered: Math.random() > 0.5 ? new Date() : undefined,
            successRate: Math.floor(Math.random() * 20) + 80
          }
        ],
        configuration: {}
      })
    })
  })

  return integrations
}

export default function APIIntegrationManager() {
  const [integrations, setIntegrations] = useState<APIIntegration[]>([])
  const [filteredIntegrations, setFilteredIntegrations] = useState<APIIntegration[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [selectedStatus, setSelectedStatus] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedIntegration, setSelectedIntegration] = useState<APIIntegration | null>(null)
  const [showCredentials, setShowCredentials] = useState(false)
  const [autoRefresh, setAutoRefresh] = useState(true)

  // Initialize integrations
  useEffect(() => {
    const mockIntegrations = generateMockIntegrations()
    setIntegrations(mockIntegrations)
    setFilteredIntegrations(mockIntegrations)
  }, [])

  // Auto refresh health checks
  useEffect(() => {
    if (!autoRefresh) return

    const interval = setInterval(() => {
      setIntegrations(prev => prev.map(integration => ({
        ...integration,
        lastHealthCheck: new Date(),
        responseTime: Math.max(50, integration.responseTime + (Math.random() - 0.5) * 50),
        requestsToday: integration.requestsToday + Math.floor(Math.random() * 10),
        errorsToday: integration.errorsToday + (Math.random() > 0.9 ? 1 : 0)
      })))
    }, 10000) // Every 10 seconds

    return () => clearInterval(interval)
  }, [autoRefresh])

  // Filter integrations
  useEffect(() => {
    let filtered = integrations

    if (selectedCategory !== 'all') {
      filtered = filtered.filter(integration => integration.category === selectedCategory)
    }

    if (selectedStatus !== 'all') {
      filtered = filtered.filter(integration => integration.status === selectedStatus)
    }

    if (searchQuery) {
      filtered = filtered.filter(integration => 
        integration.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        integration.provider.toLowerCase().includes(searchQuery.toLowerCase())
      )
    }

    setFilteredIntegrations(filtered)
  }, [integrations, selectedCategory, selectedStatus, searchQuery])

  // Calculate summary stats
  const summaryStats = {
    total: integrations.length,
    connected: integrations.filter(i => i.status === 'connected').length,
    healthy: integrations.filter(i => i.healthStatus === 'healthy').length,
    errors: integrations.filter(i => i.status === 'error').length,
    avgResponseTime: Math.round(integrations.reduce((sum, i) => sum + i.responseTime, 0) / integrations.length),
    totalRequests: integrations.reduce((sum, i) => sum + i.requestsToday, 0),
    avgSuccessRate: Math.round(integrations.reduce((sum, i) => sum + i.successRate, 0) / integrations.length)
  }

  // Handle integration actions
  const handleIntegrationAction = (integrationId: string, action: 'connect' | 'disconnect' | 'test' | 'configure') => {
    setIntegrations(prev => prev.map(integration => {
      if (integration.id === integrationId) {
        switch (action) {
          case 'connect':
            return { ...integration, status: 'connected', healthStatus: 'healthy' }
          case 'disconnect':
            return { ...integration, status: 'disconnected', healthStatus: 'down' }
          case 'test':
            return { ...integration, lastHealthCheck: new Date() }
          default:
            return integration
        }
      }
      return integration
    }))
  }

  // Status badge component
  const StatusBadge = ({ status, healthStatus }: { status: string; healthStatus?: string }) => {
    const statusColors = {
      connected: 'bg-green-500',
      disconnected: 'bg-gray-500',
      error: 'bg-red-500',
      configuring: 'bg-yellow-500'
    }

    const healthColors = {
      healthy: 'bg-green-500',
      degraded: 'bg-yellow-500',
      down: 'bg-red-500'
    }

    return (
      <div className="flex items-center space-x-1">
        <Badge variant="outline" className={`${statusColors[status as keyof typeof statusColors]} text-white border-0`}>
          {status}
        </Badge>
        {healthStatus && status === 'connected' && (
          <Badge variant="outline" className={`${healthColors[healthStatus as keyof typeof healthColors]} text-white border-0 text-xs`}>
            {healthStatus}
          </Badge>
        )}
      </div>
    )
  }

  // Integration card component
  const IntegrationCard = ({ integration }: { integration: APIIntegration }) => {
    const categoryData = BUSINESS_CATEGORIES[integration.category as keyof typeof BUSINESS_CATEGORIES]
    const CategoryIcon = categoryData?.icon || Globe
    
    return (
      <Card className="hover:shadow-lg transition-shadow cursor-pointer"
            onClick={() => setSelectedIntegration(integration)}>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className={`p-2 rounded ${categoryData?.color || 'bg-gray-500'}`}>
                <CategoryIcon className="w-4 h-4 text-white" />
              </div>
              <div>
                <CardTitle className="text-sm">{integration.name}</CardTitle>
                <div className="text-xs text-muted-foreground">{integration.provider}</div>
              </div>
            </div>
            <StatusBadge status={integration.status} healthStatus={integration.healthStatus} />
          </div>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="flex items-center space-x-2">
              <Activity className="w-3 h-3 text-muted-foreground" />
              <span>{integration.responseTime}ms</span>
            </div>
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-3 h-3 text-muted-foreground" />
              <span>{integration.uptime}%</span>
            </div>
            <div className="flex items-center space-x-2">
              <BarChart3 className="w-3 h-3 text-muted-foreground" />
              <span>{integration.requestsToday}</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-3 h-3 text-muted-foreground" />
              <span>{integration.successRate}%</span>
            </div>
          </div>

          {/* Rate Limit Indicator */}
          <div className="space-y-1">
            <div className="flex justify-between text-xs">
              <span>Rate Limit</span>
              <span>{integration.rateLimitUsed}/{integration.rateLimitTotal}</span>
            </div>
            <Progress value={(integration.rateLimitUsed / integration.rateLimitTotal) * 100} className="h-1" />
          </div>

          {/* Credentials Status */}
          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center space-x-1">
              <Key className="w-3 h-3" />
              <span>{integration.credentials.type}</span>
            </div>
            {integration.credentials.configured ? (
              <Badge variant="outline" className="text-xs bg-green-50 text-green-700">
                <CheckCircle className="w-2 h-2 mr-1" />
                Configured
              </Badge>
            ) : (
              <Badge variant="outline" className="text-xs bg-red-50 text-red-700">
                <AlertCircle className="w-2 h-2 mr-1" />
                Not Configured
              </Badge>
            )}
          </div>

          <div className="flex space-x-1 pt-2">
            <Button size="sm" variant="outline" className="flex-1 text-xs"
                    onClick={(e) => {
                      e.stopPropagation()
                      handleIntegrationAction(integration.id, integration.status === 'connected' ? 'disconnect' : 'connect')
                    }}>
              {integration.status === 'connected' ? <Unlink className="w-3 h-3" /> : <Link className="w-3 h-3" />}
            </Button>
            <Button size="sm" variant="outline" className="flex-1 text-xs"
                    onClick={(e) => {
                      e.stopPropagation()
                      handleIntegrationAction(integration.id, 'test')
                    }}>
              <RefreshCw className="w-3 h-3" />
            </Button>
            <Button size="sm" variant="outline" className="flex-1 text-xs"
                    onClick={(e) => {
                      e.stopPropagation()
                      handleIntegrationAction(integration.id, 'configure')
                    }}>
              <Settings className="w-3 h-3" />
            </Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">API Integration Manager</h2>
          <p className="text-muted-foreground">
            Monitor and manage 47+ API integrations across 13 business categories with Vault security
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Switch checked={autoRefresh} onCheckedChange={setAutoRefresh} />
            <span className="text-sm">Auto Refresh</span>
          </div>
          <Button>
            <Plus className="w-4 h-4 mr-2" />
            Add Integration
          </Button>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-7">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Globe className="w-4 h-4 text-blue-600" />
              <div className="text-2xl font-bold">{summaryStats.total}</div>
            </div>
            <div className="text-xs text-muted-foreground">Total APIs</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-4 h-4 text-green-600" />
              <div className="text-2xl font-bold">{summaryStats.connected}</div>
            </div>
            <div className="text-xs text-muted-foreground">Connected</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Activity className="w-4 h-4 text-green-600" />
              <div className="text-2xl font-bold">{summaryStats.healthy}</div>
            </div>
            <div className="text-xs text-muted-foreground">Healthy</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 text-red-600" />
              <div className="text-2xl font-bold">{summaryStats.errors}</div>
            </div>
            <div className="text-xs text-muted-foreground">Errors</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-blue-600" />
              <div className="text-2xl font-bold">{summaryStats.avgResponseTime}ms</div>
            </div>
            <div className="text-xs text-muted-foreground">Avg Response</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <BarChart3 className="w-4 h-4 text-purple-600" />
              <div className="text-2xl font-bold">{summaryStats.totalRequests.toLocaleString()}</div>
            </div>
            <div className="text-xs text-muted-foreground">Requests Today</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-4 h-4 text-green-600" />
              <div className="text-2xl font-bold">{summaryStats.avgSuccessRate}%</div>
            </div>
            <div className="text-xs text-muted-foreground">Success Rate</div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="categories">By Category</TabsTrigger>
          <TabsTrigger value="health">Health Monitor</TabsTrigger>
          <TabsTrigger value="security">Security & Vault</TabsTrigger>
          <TabsTrigger value="webhooks">Webhooks</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Filters */}
          <div className="flex flex-wrap items-center gap-4 p-4 bg-muted rounded-lg">
            <div className="flex items-center space-x-2">
              <Search className="w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search integrations..."
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

            <Select value={selectedStatus} onValueChange={setSelectedStatus}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="All Statuses" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Statuses</SelectItem>
                <SelectItem value="connected">Connected</SelectItem>
                <SelectItem value="disconnected">Disconnected</SelectItem>
                <SelectItem value="error">Error</SelectItem>
                <SelectItem value="configuring">Configuring</SelectItem>
              </SelectContent>
            </Select>

            <div className="flex items-center space-x-2 ml-auto">
              <span className="text-sm text-muted-foreground">
                {filteredIntegrations.length} of {integrations.length} integrations
              </span>
            </div>
          </div>

          {/* Integrations Grid */}
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {filteredIntegrations.map(integration => (
              <IntegrationCard key={integration.id} integration={integration} />
            ))}
          </div>
        </TabsContent>

        {/* Categories Tab */}
        <TabsContent value="categories" className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {Object.entries(BUSINESS_CATEGORIES).map(([categoryKey, category]) => {
              const categoryIntegrations = integrations.filter(i => i.category === categoryKey)
              const connectedCount = categoryIntegrations.filter(i => i.status === 'connected').length
              const healthyCount = categoryIntegrations.filter(i => i.healthStatus === 'healthy').length
              
              return (
                <Card key={categoryKey}>
                  <CardHeader>
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 rounded ${category.color}`}>
                        <category.icon className="w-6 h-6 text-white" />
                      </div>
                      <div>
                        <CardTitle className="text-lg">{category.name}</CardTitle>
                        <div className="text-sm text-muted-foreground">
                          {categoryIntegrations.length} integrations
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="text-center p-3 bg-green-50 rounded">
                          <div className="text-lg font-bold text-green-600">{connectedCount}</div>
                          <div className="text-xs text-muted-foreground">Connected</div>
                        </div>
                        <div className="text-center p-3 bg-blue-50 rounded">
                          <div className="text-lg font-bold text-blue-600">{healthyCount}</div>
                          <div className="text-xs text-muted-foreground">Healthy</div>
                        </div>
                      </div>
                      
                      <Progress value={(connectedCount / categoryIntegrations.length) * 100} className="h-2" />
                      
                      <Button variant="outline" size="sm" className="w-full"
                              onClick={() => setSelectedCategory(categoryKey)}>
                        <Eye className="w-4 h-4 mr-2" />
                        View Integrations
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </TabsContent>

        {/* Health Monitor Tab */}
        <TabsContent value="health" className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Response Time Distribution</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {['<100ms', '100-200ms', '200-300ms', '300-500ms', '>500ms'].map((range, index) => {
                    const [min, max] = range === '<100ms' ? [0, 99] : 
                                      range === '>500ms' ? [500, Infinity] :
                                      range.split('-').map(r => parseInt(r.replace('ms', '')))
                    
                    const count = integrations.filter(i => {
                      if (range === '<100ms') return i.responseTime < 100
                      if (range === '>500ms') return i.responseTime > 500
                      return i.responseTime >= min && i.responseTime <= max
                    }).length
                    
                    const percentage = (count / integrations.length) * 100
                    
                    return (
                      <div key={range} className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>{range}</span>
                          <span>{count} APIs ({percentage.toFixed(1)}%)</span>
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
                <CardTitle>Health Status Overview</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-3 gap-4 text-center">
                    <div className="p-4 bg-green-50 rounded">
                      <div className="text-2xl font-bold text-green-600">
                        {integrations.filter(i => i.healthStatus === 'healthy').length}
                      </div>
                      <div className="text-sm text-muted-foreground">Healthy</div>
                    </div>
                    <div className="p-4 bg-yellow-50 rounded">
                      <div className="text-2xl font-bold text-yellow-600">
                        {integrations.filter(i => i.healthStatus === 'degraded').length}
                      </div>
                      <div className="text-sm text-muted-foreground">Degraded</div>
                    </div>
                    <div className="p-4 bg-red-50 rounded">
                      <div className="text-2xl font-bold text-red-600">
                        {integrations.filter(i => i.healthStatus === 'down').length}
                      </div>
                      <div className="text-sm text-muted-foreground">Down</div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="text-sm font-medium">Critical Issues</div>
                    {integrations.filter(i => i.healthStatus === 'down' || i.status === 'error').slice(0, 3).map(integration => (
                      <div key={integration.id} className="flex items-center justify-between p-2 bg-red-50 rounded">
                        <span className="text-sm text-red-700">{integration.name}</span>
                        <Badge variant="destructive" className="text-xs">
                          {integration.status === 'error' ? 'Error' : 'Down'}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Security & Vault Tab */}
        <TabsContent value="security" className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Shield className="w-5 h-5" />
                  <span>Vault Integration Status</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded">
                    <div className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-600" />
                      <span className="text-sm">HashiCorp Vault Connected</span>
                    </div>
                    <Badge className="bg-green-500">Active</Badge>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Secrets Stored</span>
                      <span className="font-medium">{integrations.filter(i => i.credentials.configured).length}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Vault Policies</span>
                      <span className="font-medium">12 Active</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Token Rotation</span>
                      <span className="font-medium">Enabled</span>
                    </div>
                  </div>
                  
                  <Button variant="outline" className="w-full">
                    <ExternalLink className="w-4 h-4 mr-2" />
                    Open Vault UI
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Credential Types</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {['api_key', 'oauth', 'basic_auth', 'bearer_token'].map(type => {
                    const count = integrations.filter(i => i.credentials.type === type).length
                    const configured = integrations.filter(i => i.credentials.type === type && i.credentials.configured).length
                    
                    return (
                      <div key={type} className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="capitalize">{type.replace('_', ' ')}</span>
                          <span>{configured}/{count} configured</span>
                        </div>
                        <Progress value={(configured / count) * 100} className="h-2" />
                      </div>
                    )
                  })}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Webhooks Tab */}
        <TabsContent value="webhooks" className="space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Webhook Management</h3>
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              Add Webhook
            </Button>
          </div>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {integrations.flatMap(i => i.webhooks).map(webhook => (
              <Card key={webhook.id}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-sm">{webhook.name}</CardTitle>
                    <Badge variant={webhook.isActive ? 'default' : 'secondary'}>
                      {webhook.isActive ? 'Active' : 'Inactive'}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="text-xs text-muted-foreground">
                      <div className="font-medium">URL:</div>
                      <div className="truncate">{webhook.url}</div>
                    </div>
                    <div className="text-xs">
                      <div className="font-medium">Events:</div>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {webhook.events.map(event => (
                          <Badge key={event} variant="outline" className="text-xs">
                            {event}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span>Success Rate:</span>
                      <span className="font-medium">{webhook.successRate}%</span>
                    </div>
                    {webhook.lastTriggered && (
                      <div className="flex justify-between text-xs">
                        <span>Last Triggered:</span>
                        <span>{webhook.lastTriggered.toLocaleString()}</span>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      {/* Integration Detail Modal */}
      {selectedIntegration && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
             onClick={() => setSelectedIntegration(null)}>
          <div className="bg-white rounded-lg p-6 max-w-4xl w-full m-4 max-h-[80vh] overflow-y-auto" 
               onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <h3 className="text-xl font-semibold">{selectedIntegration.name}</h3>
                <StatusBadge status={selectedIntegration.status} healthStatus={selectedIntegration.healthStatus} />
              </div>
              <Button variant="ghost" size="sm" onClick={() => setSelectedIntegration(null)}>×</Button>
            </div>
            
            <Tabs defaultValue="overview" className="space-y-4">
              <TabsList>
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="endpoints">Endpoints</TabsTrigger>
                <TabsTrigger value="credentials">Credentials</TabsTrigger>
                <TabsTrigger value="logs">Logs</TabsTrigger>
              </TabsList>
              
              <TabsContent value="overview" className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                  <div className="p-4 border rounded">
                    <div className="text-2xl font-bold">{selectedIntegration.responseTime}ms</div>
                    <div className="text-sm text-muted-foreground">Response Time</div>
                  </div>
                  <div className="p-4 border rounded">
                    <div className="text-2xl font-bold">{selectedIntegration.uptime}%</div>
                    <div className="text-sm text-muted-foreground">Uptime</div>
                  </div>
                  <div className="p-4 border rounded">
                    <div className="text-2xl font-bold">{selectedIntegration.requestsToday}</div>
                    <div className="text-sm text-muted-foreground">Requests Today</div>
                  </div>
                  <div className="p-4 border rounded">
                    <div className="text-2xl font-bold">{selectedIntegration.successRate}%</div>
                    <div className="text-sm text-muted-foreground">Success Rate</div>
                  </div>
                </div>
              </TabsContent>
              
              <TabsContent value="endpoints" className="space-y-4">
                <div className="space-y-2">
                  {selectedIntegration.endpoints.map(endpoint => (
                    <div key={endpoint.id} className="p-4 border rounded">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <Badge>{endpoint.method}</Badge>
                          <span className="font-medium">{endpoint.name}</span>
                          <code className="text-sm bg-muted px-2 py-1 rounded">{endpoint.path}</code>
                        </div>
                        <div className="text-right text-sm">
                          <div>{endpoint.requestCount} requests</div>
                          <div className="text-muted-foreground">{endpoint.avgResponseTime}ms avg</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </TabsContent>
              
              <TabsContent value="credentials" className="space-y-4">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium">Credential Management</h4>
                    <div className="flex items-center space-x-2">
                      <Switch checked={showCredentials} onCheckedChange={setShowCredentials} />
                      <span className="text-sm">Show Values</span>
                    </div>
                  </div>
                  
                  <div className="p-4 border rounded">
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span>Type:</span>
                        <Badge>{selectedIntegration.credentials.type}</Badge>
                      </div>
                      <div className="flex justify-between">
                        <span>Status:</span>
                        <Badge variant={selectedIntegration.credentials.configured ? 'default' : 'destructive'}>
                          {selectedIntegration.credentials.configured ? 'Configured' : 'Not Configured'}
                        </Badge>
                      </div>
                      {selectedIntegration.credentials.expiresAt && (
                        <div className="flex justify-between">
                          <span>Expires:</span>
                          <span>{selectedIntegration.credentials.expiresAt.toLocaleDateString()}</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </TabsContent>
              
              <TabsContent value="logs" className="space-y-4">
                <div className="bg-black text-green-400 p-4 rounded font-mono text-sm h-64 overflow-y-auto">
                  <div>[{new Date().toISOString()}] INFO: Health check completed successfully</div>
                  <div>[{new Date().toISOString()}] INFO: API request processed in {selectedIntegration.responseTime}ms</div>
                  <div>[{new Date().toISOString()}] INFO: Rate limit: {selectedIntegration.rateLimitUsed}/{selectedIntegration.rateLimitTotal}</div>
                  {selectedIntegration.errorsToday > 0 && (
                    <div>[{new Date().toISOString()}] ERROR: {selectedIntegration.errorsToday} errors occurred today</div>
                  )}
                </div>
              </TabsContent>
            </Tabs>
            
            <div className="flex justify-between mt-6">
              <div className="flex space-x-2">
                <Button variant="outline">
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Test Connection
                </Button>
                <Button variant="outline">
                  <Download className="w-4 h-4 mr-2" />
                  Export Logs
                </Button>
              </div>
              <div className="flex space-x-2">
                <Button variant="outline">
                  <Settings className="w-4 h-4 mr-2" />
                  Configure
                </Button>
                <Button>
                  <Play className="w-4 h-4 mr-2" />
                  Activate
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}