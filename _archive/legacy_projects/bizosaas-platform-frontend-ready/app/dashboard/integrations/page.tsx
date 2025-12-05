'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { 
  Settings, 
  Zap, 
  Shield, 
  Globe,
  Mail,
  MessageSquare,
  BarChart3,
  CreditCard,
  Target,
  Users,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle,
  ExternalLink,
  Plus,
  Trash2,
  RefreshCw,
  Eye,
  EyeOff,
  Search
} from 'lucide-react'

interface Integration {
  id: string
  name: string
  category: 'social' | 'advertising' | 'analytics' | 'email' | 'payment' | 'crm' | 'communication' | 'seo' | 'ecommerce'
  description: string
  icon: React.ComponentType<{ className?: string }>
  status: 'connected' | 'disconnected' | 'error' | 'pending'
  connected?: boolean
  features: string[]
  lastSync?: string
  apiKeysRequired: string[]
  webhookUrl?: string
  permissions?: string[]
}

const integrations: Integration[] = [
  {
    id: 'meta-ads',
    name: 'Meta Ads',
    category: 'advertising',
    description: 'Connect Facebook and Instagram advertising accounts for campaign management',
    icon: Target,
    status: 'connected',
    connected: true,
    features: ['Campaign Management', 'Ad Creation', 'Audience Insights', 'Performance Analytics'],
    lastSync: '2024-08-26T10:30:00Z',
    apiKeysRequired: ['Meta App ID', 'Meta App Secret', 'Access Token'],
    permissions: ['ads_management', 'ads_read', 'pages_read_engagement']
  },
  {
    id: 'google-ads',
    name: 'Google Ads',
    category: 'advertising',
    description: 'Manage Google Ads campaigns and keyword optimization',
    icon: Target,
    status: 'disconnected',
    features: ['Search Campaigns', 'Display Ads', 'Shopping Campaigns', 'Performance Max'],
    apiKeysRequired: ['Client ID', 'Client Secret', 'Developer Token', 'Customer ID'],
    permissions: ['adwords']
  },
  {
    id: 'linkedin-ads',
    name: 'LinkedIn Marketing',
    category: 'advertising',
    description: 'LinkedIn advertising for B2B marketing campaigns',
    icon: Users,
    status: 'pending',
    features: ['Sponsored Content', 'Message Ads', 'Dynamic Ads', 'Lead Gen Forms'],
    apiKeysRequired: ['Client ID', 'Client Secret'],
    permissions: ['r_ads', 'rw_ads', 'r_organization_social']
  },
  {
    id: 'stripe',
    name: 'Stripe',
    category: 'payment',
    description: 'Payment processing and subscription management',
    icon: CreditCard,
    status: 'connected',
    connected: true,
    features: ['Payment Processing', 'Subscription Management', 'Invoicing', 'Analytics'],
    lastSync: '2024-08-26T09:15:00Z',
    apiKeysRequired: ['Publishable Key', 'Secret Key', 'Webhook Secret'],
    webhookUrl: 'https://api.bizoholic.com/webhooks/stripe'
  },
  {
    id: 'resend',
    name: 'Resend',
    category: 'email',
    description: 'Transactional and marketing email delivery service',
    icon: Mail,
    status: 'connected',
    connected: true,
    features: ['Email Delivery', 'Templates', 'Analytics', 'Webhooks'],
    lastSync: '2024-08-26T08:45:00Z',
    apiKeysRequired: ['API Key'],
    webhookUrl: 'https://api.bizoholic.com/webhooks/resend'
  },
  {
    id: 'hubspot',
    name: 'HubSpot',
    category: 'crm',
    description: 'CRM integration for lead management and customer data',
    icon: Users,
    status: 'error',
    features: ['Contact Management', 'Deal Tracking', 'Email Sequences', 'Analytics'],
    apiKeysRequired: ['Private App Token'],
    permissions: ['contacts', 'companies', 'deals', 'tickets']
  },
  {
    id: 'slack',
    name: 'Slack',
    category: 'communication',
    description: 'Team notifications and campaign alerts',
    icon: MessageSquare,
    status: 'disconnected',
    features: ['Notifications', 'Campaign Alerts', 'Performance Reports', 'Bot Commands'],
    apiKeysRequired: ['Bot Token', 'App Token'],
    permissions: ['chat:write', 'channels:read', 'groups:read', 'im:read']
  },
  {
    id: 'google-analytics',
    name: 'Google Analytics',
    category: 'analytics',
    description: 'Website analytics and conversion tracking',
    icon: BarChart3,
    status: 'disconnected',
    features: ['Traffic Analysis', 'Conversion Tracking', 'Custom Events', 'Reporting'],
    apiKeysRequired: ['Client ID', 'Client Secret', 'Property ID'],
    permissions: ['analytics.readonly']
  },
  {
    id: 'google-search-console',
    name: 'Google Search Console',
    category: 'seo',
    description: 'Monitor search performance, SEO health, and site indexing status',
    icon: Search,
    status: 'disconnected',
    features: ['Search Performance Analytics', 'Index Coverage Monitoring', 'Core Web Vitals', 'Sitemap Management', 'URL Inspection'],
    apiKeysRequired: ['Client ID', 'Client Secret'],
    permissions: ['webmasters.readonly']
  },
  {
    id: 'amazon-sp-api',
    name: 'Amazon SP-API',
    category: 'ecommerce',
    description: 'AI-powered Amazon marketplace operations through Brain API Gateway',
    icon: Target,
    status: 'disconnected',
    features: ['AI Product Sourcing', 'AI Pricing Optimization', 'AI Inventory Management', 'AI Order Automation', 'Multi-Marketplace Support'],
    apiKeysRequired: ['LWA Client ID', 'LWA Client Secret', 'Refresh Token', 'AWS Access Key', 'AWS Secret Key'],
    permissions: ['sellingpartner:orders', 'sellingpartner:inventory', 'sellingpartner:catalog']
  }
]

export default function IntegrationsPage() {
  const [selectedIntegration, setSelectedIntegration] = useState<Integration | null>(null)
  const [apiKeys, setApiKeys] = useState<Record<string, string>>({})
  const [showApiKey, setShowApiKey] = useState<Record<string, boolean>>({})
  const [activeTab, setActiveTab] = useState('all')

  const getStatusIcon = (status: Integration['status']) => {
    switch (status) {
      case 'connected':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'error':
        return <XCircle className="h-4 w-4 text-red-500" />
      case 'pending':
        return <AlertCircle className="h-4 w-4 text-yellow-500" />
      default:
        return <XCircle className="h-4 w-4 text-gray-400" />
    }
  }

  const getStatusBadge = (status: Integration['status']) => {
    const variants = {
      connected: 'default' as const,
      disconnected: 'secondary' as const,
      error: 'destructive' as const,
      pending: 'outline' as const
    }
    
    return (
      <Badge variant={variants[status]} className="capitalize">
        {status}
      </Badge>
    )
  }

  const getCategoryIcon = (category: Integration['category']) => {
    const icons = {
      social: Globe,
      advertising: Target,
      analytics: BarChart3,
      email: Mail,
      payment: CreditCard,
      crm: Users,
      communication: MessageSquare,
      seo: Search,
      ecommerce: Target
    }
    const Icon = icons[category]
    return <Icon className="h-4 w-4" />
  }

  const filteredIntegrations = activeTab === 'all' 
    ? integrations 
    : integrations.filter(integration => integration.category === activeTab)

  const connectedCount = integrations.filter(i => i.status === 'connected').length
  const errorCount = integrations.filter(i => i.status === 'error').length

  const handleConnect = async (integration: Integration) => {
    try {
      // API call to connect integration
      console.log('Connecting integration:', integration.id)
      // For Amazon SP-API, navigate to dedicated integration page
      if (integration.id === 'amazon-sp-api') {
        window.location.href = `/dashboard/integrations/amazon-sp-api`
      }
      // For OAuth integrations, redirect to authorization URL
      else if (['meta-ads', 'google-ads', 'linkedin-ads', 'hubspot'].includes(integration.id)) {
        window.location.href = `/api/integrations/${integration.id}/oauth/authorize`
      }
    } catch (error) {
      console.error('Failed to connect integration:', error)
    }
  }

  const handleDisconnect = async (integrationId: string) => {
    try {
      // API call to disconnect integration
      console.log('Disconnecting integration:', integrationId)
    } catch (error) {
      console.error('Failed to disconnect integration:', error)
    }
  }

  const handleSaveApiKeys = async (integrationId: string) => {
    try {
      // API call to save API keys
      console.log('Saving API keys for:', integrationId, apiKeys)
    } catch (error) {
      console.error('Failed to save API keys:', error)
    }
  }

  const handleTestConnection = async (integrationId: string) => {
    try {
      // API call to test connection
      console.log('Testing connection for:', integrationId)
    } catch (error) {
      console.error('Failed to test connection:', error)
    }
  }

  return (
    <div className="flex-1 space-y-6 p-8 pt-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Integrations</h2>
          <p className="text-muted-foreground">
            Connect your marketing tools and platforms to BizoSaaS
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-sm">
            <CheckCircle className="h-4 w-4 text-green-500" />
            <span>{connectedCount} Connected</span>
          </div>
          {errorCount > 0 && (
            <div className="flex items-center gap-2 text-sm">
              <XCircle className="h-4 w-4 text-red-500" />
              <span>{errorCount} Issues</span>
            </div>
          )}
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList>
          <TabsTrigger value="all">All Integrations</TabsTrigger>
          <TabsTrigger value="advertising">Advertising</TabsTrigger>
          <TabsTrigger value="social">Social Media</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="seo">SEO</TabsTrigger>
          <TabsTrigger value="ecommerce">E-commerce</TabsTrigger>
          <TabsTrigger value="email">Email</TabsTrigger>
          <TabsTrigger value="payment">Payments</TabsTrigger>
          <TabsTrigger value="crm">CRM</TabsTrigger>
          <TabsTrigger value="communication">Communication</TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab} className="space-y-4">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {filteredIntegrations.map((integration) => (
              <Card key={integration.id} className="relative">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                  <div className="flex items-center space-x-2">
                    {getCategoryIcon(integration.category)}
                    <CardTitle className="text-lg">{integration.name}</CardTitle>
                  </div>
                  <div className="flex items-center space-x-2">
                    {getStatusIcon(integration.status)}
                    {getStatusBadge(integration.status)}
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <CardDescription>{integration.description}</CardDescription>
                  
                  <div>
                    <h4 className="text-sm font-medium mb-2">Features</h4>
                    <div className="flex flex-wrap gap-1">
                      {integration.features.slice(0, 3).map((feature) => (
                        <Badge key={feature} variant="outline" className="text-xs">
                          {feature}
                        </Badge>
                      ))}
                      {integration.features.length > 3 && (
                        <Badge variant="outline" className="text-xs">
                          +{integration.features.length - 3} more
                        </Badge>
                      )}
                    </div>
                  </div>

                  {integration.lastSync && (
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      <Clock className="h-3 w-3" />
                      Last sync: {new Date(integration.lastSync).toLocaleString()}
                    </div>
                  )}

                  <div className="flex gap-2 pt-2">
                    {integration.status === 'connected' ? (
                      <>
                        <Button 
                          variant="outline" 
                          size="sm" 
                          onClick={() => handleTestConnection(integration.id)}
                        >
                          <RefreshCw className="h-3 w-3 mr-1" />
                          Test
                        </Button>
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button variant="outline" size="sm">
                              <Settings className="h-3 w-3 mr-1" />
                              Configure
                            </Button>
                          </DialogTrigger>
                          <DialogContent className="max-w-2xl">
                            <DialogHeader>
                              <DialogTitle>Configure {integration.name}</DialogTitle>
                              <DialogDescription>
                                Manage your integration settings and API keys
                              </DialogDescription>
                            </DialogHeader>
                            <div className="space-y-4">
                              {integration.apiKeysRequired.map((keyName) => (
                                <div key={keyName} className="space-y-2">
                                  <Label htmlFor={keyName}>{keyName}</Label>
                                  <div className="relative">
                                    <Input
                                      id={keyName}
                                      type={showApiKey[keyName] ? 'text' : 'password'}
                                      value={apiKeys[keyName] || ''}
                                      onChange={(e) => setApiKeys(prev => ({
                                        ...prev,
                                        [keyName]: e.target.value
                                      }))}
                                      placeholder={`Enter ${keyName}`}
                                    />
                                    <Button
                                      type="button"
                                      variant="ghost"
                                      size="sm"
                                      className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                                      onClick={() => setShowApiKey(prev => ({
                                        ...prev,
                                        [keyName]: !prev[keyName]
                                      }))}
                                    >
                                      {showApiKey[keyName] ? (
                                        <EyeOff className="h-4 w-4" />
                                      ) : (
                                        <Eye className="h-4 w-4" />
                                      )}
                                    </Button>
                                  </div>
                                </div>
                              ))}
                              
                              {integration.webhookUrl && (
                                <div className="space-y-2">
                                  <Label>Webhook URL</Label>
                                  <div className="flex items-center gap-2">
                                    <Input 
                                      value={integration.webhookUrl} 
                                      readOnly 
                                      className="font-mono text-sm"
                                    />
                                    <Button 
                                      variant="outline" 
                                      size="sm"
                                      onClick={() => navigator.clipboard.writeText(integration.webhookUrl!)}
                                    >
                                      Copy
                                    </Button>
                                  </div>
                                </div>
                              )}
                              
                              <div className="flex gap-2 pt-4">
                                <Button 
                                  onClick={() => handleSaveApiKeys(integration.id)}
                                  className="flex-1"
                                >
                                  Save Changes
                                </Button>
                                <AlertDialog>
                                  <AlertDialogTrigger asChild>
                                    <Button variant="outline" className="text-red-600">
                                      <Trash2 className="h-4 w-4 mr-1" />
                                      Disconnect
                                    </Button>
                                  </AlertDialogTrigger>
                                  <AlertDialogContent>
                                    <AlertDialogHeader>
                                      <AlertDialogTitle>Disconnect Integration?</AlertDialogTitle>
                                      <AlertDialogDescription>
                                        This will remove all API keys and disable {integration.name} integration. 
                                        Any active campaigns using this integration will be affected.
                                      </AlertDialogDescription>
                                    </AlertDialogHeader>
                                    <AlertDialogFooter>
                                      <AlertDialogCancel>Cancel</AlertDialogCancel>
                                      <AlertDialogAction 
                                        onClick={() => handleDisconnect(integration.id)}
                                        className="bg-red-600 hover:bg-red-700"
                                      >
                                        Disconnect
                                      </AlertDialogAction>
                                    </AlertDialogFooter>
                                  </AlertDialogContent>
                                </AlertDialog>
                              </div>
                            </div>
                          </DialogContent>
                        </Dialog>
                      </>
                    ) : (
                      <Button 
                        onClick={() => handleConnect(integration)}
                        className="w-full"
                        disabled={integration.status === 'pending'}
                      >
                        {integration.status === 'pending' ? (
                          <>
                            <RefreshCw className="h-3 w-3 mr-1 animate-spin" />
                            Connecting...
                          </>
                        ) : (
                          <>
                            <Plus className="h-3 w-3 mr-1" />
                            Connect
                          </>
                        )}
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {filteredIntegrations.length === 0 && (
            <Card className="flex flex-col items-center justify-center py-12">
              <div className="text-center space-y-4">
                <Zap className="h-12 w-12 text-muted-foreground mx-auto" />
                <div>
                  <h3 className="text-lg font-medium">No integrations found</h3>
                  <p className="text-muted-foreground">
                    No integrations match the selected category
                  </p>
                </div>
              </div>
            </Card>
          )}
        </TabsContent>
      </Tabs>

      {errorCount > 0 && (
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            {errorCount} integration{errorCount > 1 ? 's have' : ' has'} connection issues. 
            Please check your configuration and reconnect.
          </AlertDescription>
        </Alert>
      )}
    </div>
  )
}