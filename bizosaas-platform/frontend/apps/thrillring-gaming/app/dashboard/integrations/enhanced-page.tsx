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
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"
import { Textarea } from "@/components/ui/textarea"
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
  Search,
  MapPin,
  TrendingUp,
  Bot,
  Upload,
  Download,
  Activity,
  MoreHorizontal,
  Sparkles,
  Play,
  Pause,
  Calendar,
  Database,
  Link,
  ShieldCheck,
  Rocket,
  Brain,
  Workflow
} from 'lucide-react'

// Enhanced Integration Interface with AI Automation
interface Integration {
  id: string
  name: string
  category: 'social' | 'advertising' | 'analytics' | 'email' | 'payment' | 'crm' | 'communication' | 'webmaster' | 'automation' | 'ecommerce'
  description: string
  icon: React.ComponentType<{ className?: string }>
  status: 'connected' | 'disconnected' | 'error' | 'pending' | 'syncing'
  connected?: boolean
  features: string[]
  lastSync?: string
  apiKeysRequired: string[]
  webhookUrl?: string
  permissions?: string[]
  setupType: 'oauth' | 'api_key' | 'manual' | 'ai_wizard'
  priority: 'high' | 'medium' | 'low'
  dataSync?: {
    frequency: string
    lastImport?: string
    recordsCount?: number
    nextSync?: string
  }
  automationCapabilities?: string[]
  aiFeatures?: string[]
  connectionHealth?: number
  monthlyUsage?: {
    apiCalls: number
    dataTransfer: string
    cost: number
  }
}

// Comprehensive integration catalog with AI automation capabilities
const integrations: Integration[] = [
  // Analytics & Webmaster Tools
  {
    id: 'google-analytics-4',
    name: 'Google Analytics 4',
    category: 'analytics',
    description: 'Advanced website analytics with AI-powered insights and predictive analytics',
    icon: BarChart3,
    status: 'connected',
    connected: true,
    features: ['GA4 Analytics', 'Enhanced Ecommerce', 'Custom Events', 'Predictive Metrics', 'Audience Insights'],
    lastSync: '2024-09-13T14:30:00Z',
    apiKeysRequired: ['Client ID', 'Client Secret', 'Property ID', 'Measurement ID'],
    permissions: ['analytics.readonly', 'analytics.edit'],
    setupType: 'oauth',
    priority: 'high',
    dataSync: {
      frequency: 'Every 4 hours',
      lastImport: '2024-09-13T14:30:00Z',
      recordsCount: 125430,
      nextSync: '2024-09-13T18:30:00Z'
    },
    automationCapabilities: [
      'AI-powered anomaly detection',
      'Automated report generation',
      'Goal optimization suggestions',
      'Real-time alerts for significant changes',
      'Predictive audience insights'
    ],
    aiFeatures: [
      'Smart traffic analysis',
      'Conversion prediction',
      'User journey optimization',
      'Revenue forecasting'
    ],
    connectionHealth: 98,
    monthlyUsage: {
      apiCalls: 45000,
      dataTransfer: '2.3 GB',
      cost: 0
    }
  },
  {
    id: 'google-search-console',
    name: 'Google Search Console',
    category: 'webmaster',
    description: 'SEO performance monitoring with AI-driven optimization recommendations',
    icon: Search,
    status: 'connected',
    connected: true,
    features: ['Search Performance', 'Index Coverage', 'Core Web Vitals', 'Mobile Usability', 'Manual Actions'],
    lastSync: '2024-09-13T13:15:00Z',
    apiKeysRequired: ['Client ID', 'Client Secret'],
    permissions: ['webmasters.readonly'],
    setupType: 'oauth',
    priority: 'high',
    dataSync: {
      frequency: 'Daily',
      lastImport: '2024-09-13T13:15:00Z',
      recordsCount: 8945,
      nextSync: '2024-09-14T06:00:00Z'
    },
    automationCapabilities: [
      'AI SEO recommendations',
      'Automated issue detection',
      'Performance optimization alerts',
      'Keyword opportunity identification',
      'Technical SEO monitoring'
    ],
    aiFeatures: [
      'Smart keyword analysis',
      'Content gap identification',
      'Technical issue prediction',
      'Search visibility forecasting'
    ],
    connectionHealth: 95,
    monthlyUsage: {
      apiCalls: 12000,
      dataTransfer: '450 MB',
      cost: 0
    }
  },
  {
    id: 'bing-webmaster',
    name: 'Bing Webmaster Tools',
    category: 'webmaster',
    description: 'Microsoft search optimization with automated competitive analysis',
    icon: Search,
    status: 'disconnected',
    features: ['Search Analytics', 'Crawl Information', 'Backlink Data', 'Keywords', 'SEO Reports'],
    apiKeysRequired: ['API Key'],
    setupType: 'api_key',
    priority: 'medium',
    automationCapabilities: [
      'Bing SEO optimization',
      'Competitive analysis automation',
      'Backlink monitoring',
      'Keyword tracking'
    ],
    aiFeatures: [
      'Microsoft search insights',
      'Competitive intelligence',
      'Bing-specific optimizations'
    ]
  },
  {
    id: 'google-my-business',
    name: 'Google My Business',
    category: 'social',
    description: 'AI-powered local business profile management and reputation monitoring',
    icon: MapPin,
    status: 'pending',
    features: ['Profile Management', 'Review Responses', 'Posts', 'Insights', 'Q&A Management'],
    apiKeysRequired: ['Client ID', 'Client Secret'],
    permissions: ['business.manage'],
    setupType: 'oauth',
    priority: 'high',
    automationCapabilities: [
      'AI-powered review responses',
      'Automated post scheduling',
      'Reputation monitoring',
      'Local SEO optimization',
      'Customer engagement automation'
    ],
    aiFeatures: [
      'Sentiment-aware review responses',
      'Local market analysis',
      'Competitor monitoring',
      'Optimal posting time suggestions'
    ]
  },

  // Advertising Platforms
  {
    id: 'meta-ads-manager',
    name: 'Meta Ads Manager',
    category: 'advertising',
    description: 'Advanced Facebook & Instagram advertising with AI campaign optimization',
    icon: Target,
    status: 'connected',
    connected: true,
    features: ['Campaign Management', 'Creative Testing', 'Audience Insights', 'Performance Analytics', 'Budget Optimization'],
    lastSync: '2024-09-13T15:00:00Z',
    apiKeysRequired: ['Meta App ID', 'Meta App Secret', 'Access Token', 'Business Manager ID'],
    permissions: ['ads_management', 'ads_read', 'pages_read_engagement'],
    setupType: 'oauth',
    priority: 'high',
    dataSync: {
      frequency: 'Every hour',
      lastImport: '2024-09-13T15:00:00Z',
      recordsCount: 2340,
      nextSync: '2024-09-13T16:00:00Z'
    },
    automationCapabilities: [
      'AI campaign optimization',
      'Automated bid management',
      'Creative performance analysis',
      'Audience expansion suggestions',
      'Budget reallocation automation'
    ],
    aiFeatures: [
      'Smart audience targeting',
      'Creative optimization',
      'Predictive performance modeling',
      'Cross-platform insights'
    ],
    connectionHealth: 92,
    monthlyUsage: {
      apiCalls: 85000,
      dataTransfer: '5.2 GB',
      cost: 45.60
    }
  },
  {
    id: 'google-ads-advanced',
    name: 'Google Ads Advanced',
    category: 'advertising',
    description: 'Enterprise Google Ads management with ML-powered optimization',
    icon: Target,
    status: 'error',
    features: ['Search Campaigns', 'Performance Max', 'Shopping Campaigns', 'YouTube Ads', 'Smart Bidding'],
    apiKeysRequired: ['Client ID', 'Client Secret', 'Developer Token', 'Customer ID', 'Manager Account ID'],
    permissions: ['adwords'],
    setupType: 'oauth',
    priority: 'high',
    automationCapabilities: [
      'Machine learning bid optimization',
      'Automated keyword expansion',
      'Performance max automation',
      'Cross-campaign insights',
      'Budget optimization'
    ],
    aiFeatures: [
      'Smart bidding strategies',
      'Keyword opportunity detection',
      'Ad copy optimization',
      'Performance forecasting'
    ]
  },
  {
    id: 'linkedin-marketing',
    name: 'LinkedIn Marketing',
    category: 'advertising',
    description: 'B2B advertising platform with professional targeting capabilities',
    icon: Users,
    status: 'disconnected',
    features: ['Sponsored Content', 'Message Ads', 'Dynamic Ads', 'Lead Gen Forms', 'Account-Based Marketing'],
    apiKeysRequired: ['Client ID', 'Client Secret'],
    permissions: ['r_ads', 'rw_ads', 'r_organization_social'],
    setupType: 'oauth',
    priority: 'high',
    automationCapabilities: [
      'B2B audience optimization',
      'Lead generation automation',
      'Professional targeting',
      'Account-based campaign management'
    ],
    aiFeatures: [
      'Professional audience insights',
      'B2B conversion optimization',
      'Industry-specific targeting',
      'Lead quality scoring'
    ]
  },

  // Social Media Platforms
  {
    id: 'linkedin-business',
    name: 'LinkedIn Business',
    category: 'social',
    description: 'Professional networking and content management with AI engagement optimization',
    icon: Users,
    status: 'connected',
    connected: true,
    features: ['Page Management', 'Content Publishing', 'Analytics', 'Lead Generation', 'Company Updates'],
    lastSync: '2024-09-13T12:45:00Z',
    apiKeysRequired: ['Client ID', 'Client Secret'],
    permissions: ['w_member_social', 'r_organization_social'],
    setupType: 'oauth',
    priority: 'high',
    dataSync: {
      frequency: 'Every 6 hours',
      lastImport: '2024-09-13T12:45:00Z',
      recordsCount: 1250,
      nextSync: '2024-09-13T18:45:00Z'
    },
    automationCapabilities: [
      'AI content scheduling',
      'Engagement optimization',
      'Professional networking automation',
      'Lead tracking and nurturing',
      'Industry trend analysis'
    ],
    aiFeatures: [
      'Professional content suggestions',
      'Optimal posting times',
      'Engagement prediction',
      'Network growth optimization'
    ],
    connectionHealth: 89,
    monthlyUsage: {
      apiCalls: 25000,
      dataTransfer: '1.1 GB',
      cost: 0
    }
  },
  {
    id: 'twitter-business',
    name: 'Twitter Business',
    category: 'social',
    description: 'Real-time engagement and trend monitoring with AI-powered insights',
    icon: MessageSquare,
    status: 'disconnected',
    features: ['Tweet Management', 'Analytics', 'Audience Insights', 'Trend Monitoring', 'Engagement Tracking'],
    apiKeysRequired: ['API Key', 'API Secret', 'Access Token', 'Access Token Secret'],
    setupType: 'api_key',
    priority: 'medium',
    automationCapabilities: [
      'Smart tweet scheduling',
      'Hashtag optimization',
      'Trend analysis and alerting',
      'Engagement automation',
      'Crisis monitoring'
    ],
    aiFeatures: [
      'Viral content prediction',
      'Optimal hashtag suggestions',
      'Sentiment monitoring',
      'Trend forecasting'
    ]
  },
  {
    id: 'instagram-business',
    name: 'Instagram Business',
    category: 'social',
    description: 'Visual content management with AI-powered creative optimization',
    icon: Target,
    status: 'connected',
    connected: true,
    features: ['Content Publishing', 'Stories Management', 'Analytics', 'Shopping Integration', 'Reels Optimization'],
    lastSync: '2024-09-13T14:00:00Z',
    apiKeysRequired: ['Client ID', 'Client Secret', 'Access Token'],
    permissions: ['instagram_basic', 'instagram_content_publish'],
    setupType: 'oauth',
    priority: 'high',
    dataSync: {
      frequency: 'Every 2 hours',
      lastImport: '2024-09-13T14:00:00Z',
      recordsCount: 3450,
      nextSync: '2024-09-13T16:00:00Z'
    },
    automationCapabilities: [
      'AI content optimization',
      'Automated story creation',
      'Hashtag intelligence',
      'Shopping tag automation',
      'Reels performance optimization'
    ],
    aiFeatures: [
      'Visual content analysis',
      'Engagement prediction',
      'Optimal posting schedules',
      'Creative performance insights'
    ],
    connectionHealth: 94,
    monthlyUsage: {
      apiCalls: 35000,
      dataTransfer: '3.8 GB',
      cost: 0
    }
  },

  // Email Service Providers
  {
    id: 'mailchimp-advanced',
    name: 'Mailchimp Advanced',
    category: 'email',
    description: 'AI-driven email marketing with predictive analytics and automation',
    icon: Mail,
    status: 'connected',
    connected: true,
    features: ['Email Campaigns', 'Marketing Automation', 'Advanced Segmentation', 'A/B Testing', 'Predictive Analytics'],
    lastSync: '2024-09-13T13:30:00Z',
    apiKeysRequired: ['API Key', 'Server Prefix'],
    setupType: 'api_key',
    priority: 'high',
    dataSync: {
      frequency: 'Every 30 minutes',
      lastImport: '2024-09-13T13:30:00Z',
      recordsCount: 45600,
      nextSync: '2024-09-13T14:00:00Z'
    },
    automationCapabilities: [
      'AI email optimization',
      'Predictive send times',
      'Smart segmentation',
      'Behavioral trigger automation',
      'Content personalization'
    ],
    aiFeatures: [
      'Subject line optimization',
      'Send time optimization',
      'Customer lifetime value prediction',
      'Churn prevention campaigns'
    ],
    connectionHealth: 96,
    monthlyUsage: {
      apiCalls: 65000,
      dataTransfer: '2.1 GB',
      cost: 29.99
    }
  },
  {
    id: 'sendgrid-enterprise',
    name: 'SendGrid Enterprise',
    category: 'email',
    description: 'Enterprise email delivery with advanced deliverability optimization',
    icon: Mail,
    status: 'disconnected',
    features: ['Transactional Email', 'Marketing Campaigns', 'Email Validation', 'Deliverability Insights', 'Advanced Analytics'],
    apiKeysRequired: ['API Key'],
    setupType: 'api_key',
    priority: 'high',
    automationCapabilities: [
      'Deliverability optimization',
      'Template performance analysis',
      'Automated list hygiene',
      'Bounce handling',
      'Reputation monitoring'
    ],
    aiFeatures: [
      'Deliverability prediction',
      'Content optimization',
      'Send reputation management',
      'Spam filter avoidance'
    ]
  },

  // CRM Platforms
  {
    id: 'hubspot-enterprise',
    name: 'HubSpot Enterprise',
    category: 'crm',
    description: 'All-in-one CRM with AI-powered sales and marketing automation',
    icon: Users,
    status: 'connected',
    connected: true,
    features: ['Contact Management', 'Deal Pipeline', 'Marketing Automation', 'Sales Analytics', 'Customer Journey'],
    lastSync: '2024-09-13T14:45:00Z',
    apiKeysRequired: ['Private App Token', 'Portal ID'],
    permissions: ['contacts', 'companies', 'deals', 'tickets', 'marketing'],
    setupType: 'oauth',
    priority: 'high',
    dataSync: {
      frequency: 'Real-time',
      lastImport: '2024-09-13T14:45:00Z',
      recordsCount: 15670,
      nextSync: 'Continuous'
    },
    automationCapabilities: [
      'AI lead scoring',
      'Automated deal progression',
      'Predictive analytics',
      'Customer journey optimization',
      'Revenue forecasting'
    ],
    aiFeatures: [
      'Conversation intelligence',
      'Predictive lead scoring',
      'Deal probability analysis',
      'Customer health scoring'
    ],
    connectionHealth: 91,
    monthlyUsage: {
      apiCalls: 120000,
      dataTransfer: '8.5 GB',
      cost: 89.99
    }
  },
  {
    id: 'salesforce-enterprise',
    name: 'Salesforce Enterprise',
    category: 'crm',
    description: 'Enterprise CRM with Einstein AI and advanced automation capabilities',
    icon: Users,
    status: 'error',
    features: ['Lead Management', 'Opportunity Tracking', 'Einstein AI', 'Reports & Dashboards', 'Process Automation'],
    apiKeysRequired: ['Client ID', 'Client Secret', 'Security Token', 'Instance URL'],
    permissions: ['full'],
    setupType: 'oauth',
    priority: 'high',
    automationCapabilities: [
      'Einstein lead scoring',
      'Automated opportunity management',
      'AI-powered forecasting',
      'Process automation',
      'Advanced reporting'
    ],
    aiFeatures: [
      'Einstein Analytics',
      'Predictive forecasting',
      'Opportunity insights',
      'Next best action recommendations'
    ]
  },

  // E-commerce Platforms
  {
    id: 'shopify-plus',
    name: 'Shopify Plus',
    category: 'ecommerce',
    description: 'Enterprise e-commerce platform with advanced automation and analytics',
    icon: CreditCard,
    status: 'connected',
    connected: true,
    features: ['Store Management', 'Product Sync', 'Order Processing', 'Inventory Management', 'Analytics'],
    lastSync: '2024-09-13T15:15:00Z',
    apiKeysRequired: ['API Key', 'API Secret', 'Store URL'],
    setupType: 'api_key',
    priority: 'high',
    dataSync: {
      frequency: 'Every 15 minutes',
      lastImport: '2024-09-13T15:15:00Z',
      recordsCount: 5680,
      nextSync: '2024-09-13T15:30:00Z'
    },
    automationCapabilities: [
      'Inventory optimization',
      'Automated order processing',
      'Customer segmentation',
      'Pricing optimization',
      'Marketing automation'
    ],
    aiFeatures: [
      'Sales forecasting',
      'Product recommendations',
      'Customer lifetime value',
      'Inventory predictions'
    ],
    connectionHealth: 97,
    monthlyUsage: {
      apiCalls: 95000,
      dataTransfer: '12.3 GB',
      cost: 199.99
    }
  },

  // Payment Platforms
  {
    id: 'stripe-advanced',
    name: 'Stripe Advanced',
    category: 'payment',
    description: 'Advanced payment processing with AI fraud detection and revenue optimization',
    icon: CreditCard,
    status: 'connected',
    connected: true,
    features: ['Payment Processing', 'Subscription Management', 'Fraud Detection', 'Revenue Analytics', 'Global Payments'],
    lastSync: '2024-09-13T15:30:00Z',
    apiKeysRequired: ['Publishable Key', 'Secret Key', 'Webhook Secret'],
    webhookUrl: 'https://api.bizosaas.com/webhooks/stripe',
    setupType: 'api_key',
    priority: 'high',
    dataSync: {
      frequency: 'Real-time',
      lastImport: '2024-09-13T15:30:00Z',
      recordsCount: 8945,
      nextSync: 'Continuous'
    },
    automationCapabilities: [
      'AI fraud detection',
      'Automated dunning management',
      'Revenue optimization',
      'Subscription analytics',
      'Payment routing optimization'
    ],
    aiFeatures: [
      'Radar fraud detection',
      'Revenue recovery',
      'Churn prediction',
      'Payment optimization'
    ],
    connectionHealth: 99,
    monthlyUsage: {
      apiCalls: 250000,
      dataTransfer: '15.7 GB',
      cost: 125.45
    }
  },

  // Automation & Workflow
  {
    id: 'zapier-enterprise',
    name: 'Zapier Enterprise',
    category: 'automation',
    description: 'Advanced workflow automation with AI-powered integration suggestions',
    icon: Workflow,
    status: 'connected',
    connected: true,
    features: ['Workflow Automation', 'App Integrations', 'Data Transfer', 'Scheduled Tasks', 'Error Handling'],
    lastSync: '2024-09-13T14:20:00Z',
    apiKeysRequired: ['API Key'],
    setupType: 'api_key',
    priority: 'medium',
    dataSync: {
      frequency: 'Event-driven',
      lastImport: '2024-09-13T14:20:00Z',
      recordsCount: 1250,
      nextSync: 'On trigger'
    },
    automationCapabilities: [
      'Smart workflow suggestions',
      'Error detection and recovery',
      'Performance optimization',
      'Integration recommendations',
      'Automated testing'
    ],
    aiFeatures: [
      'Workflow optimization',
      'Integration suggestions',
      'Performance insights',
      'Anomaly detection'
    ],
    connectionHealth: 88,
    monthlyUsage: {
      apiCalls: 45000,
      dataTransfer: '1.8 GB',
      cost: 49.99
    }
  }
]

export default function EnhancedIntegrationsPage() {
  const [selectedIntegration, setSelectedIntegration] = useState<Integration | null>(null)
  const [apiKeys, setApiKeys] = useState<Record<string, string>>({})
  const [showApiKey, setShowApiKey] = useState<Record<string, boolean>>({})
  const [activeTab, setActiveTab] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [isAIWizardOpen, setIsAIWizardOpen] = useState(false)
  const [bulkOperationMode, setBulkOperationMode] = useState(false)
  const [selectedIntegrations, setSelectedIntegrations] = useState<string[]>([])

  // Filter integrations based on active tab and search query
  const filteredIntegrations = integrations.filter(integration => {
    const matchesCategory = activeTab === 'all' || integration.category === activeTab
    const matchesSearch = integration.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         integration.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         integration.features.some(feature => feature.toLowerCase().includes(searchQuery.toLowerCase()))
    return matchesCategory && matchesSearch
  })

  // Statistics
  const connectedCount = integrations.filter(i => i.status === 'connected').length
  const errorCount = integrations.filter(i => i.status === 'error').length
  const pendingCount = integrations.filter(i => i.status === 'pending').length
  const totalCost = integrations
    .filter(i => i.monthlyUsage?.cost)
    .reduce((sum, i) => sum + (i.monthlyUsage?.cost || 0), 0)

  const getStatusIcon = (status: Integration['status']) => {
    switch (status) {
      case 'connected':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'error':
        return <XCircle className="h-4 w-4 text-red-500" />
      case 'pending':
        return <AlertCircle className="h-4 w-4 text-yellow-500" />
      case 'syncing':
        return <RefreshCw className="h-4 w-4 text-blue-500 animate-spin" />
      default:
        return <XCircle className="h-4 w-4 text-gray-400" />
    }
  }

  const getStatusBadge = (status: Integration['status']) => {
    const variants = {
      connected: 'default' as const,
      disconnected: 'secondary' as const,
      error: 'destructive' as const,
      pending: 'outline' as const,
      syncing: 'default' as const
    }
    
    return (
      <Badge variant={variants[status]} className="capitalize">
        {status === 'syncing' ? 'Syncing' : status}
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
      webmaster: Search,
      automation: Workflow,
      ecommerce: CreditCard
    }
    const Icon = icons[category]
    return <Icon className="h-4 w-4" />
  }

  const getPriorityColor = (priority: Integration['priority']) => {
    switch (priority) {
      case 'high':
        return 'text-red-600'
      case 'medium':
        return 'text-yellow-600'
      case 'low':
        return 'text-green-600'
      default:
        return 'text-gray-600'
    }
  }

  const handleConnect = async (integration: Integration) => {
    try {
      console.log('Connecting integration:', integration.id)
      
      if (integration.setupType === 'ai_wizard') {
        setSelectedIntegration(integration)
        setIsAIWizardOpen(true)
        return
      }
      
      // OAuth integrations
      if (integration.setupType === 'oauth') {
        const response = await fetch(`/api/integrations/${integration.id}/oauth/authorize`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        })
        const data = await response.json()
        if (data.authUrl) {
          window.location.href = data.authUrl
        }
      }
      
      // API key integrations
      if (integration.setupType === 'api_key') {
        setSelectedIntegration(integration)
      }
    } catch (error) {
      console.error('Failed to connect integration:', error)
    }
  }

  const handleDisconnect = async (integrationId: string) => {
    try {
      const response = await fetch(`/api/integrations/${integrationId}/disconnect`, {
        method: 'POST'
      })
      if (response.ok) {
        // Update integration status
        console.log('Integration disconnected successfully')
      }
    } catch (error) {
      console.error('Failed to disconnect integration:', error)
    }
  }

  const handleBulkConnect = async () => {
    try {
      const response = await fetch('/api/integrations/bulk-connect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ integrationIds: selectedIntegrations })
      })
      if (response.ok) {
        console.log('Bulk connection initiated')
        setSelectedIntegrations([])
        setBulkOperationMode(false)
      }
    } catch (error) {
      console.error('Failed to initiate bulk connection:', error)
    }
  }

  const handleAIWizardSetup = async (integrationId: string, requirements: any) => {
    try {
      const response = await fetch(`/api/integrations/${integrationId}/ai-setup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requirements)
      })
      if (response.ok) {
        console.log('AI wizard setup initiated')
        setIsAIWizardOpen(false)
      }
    } catch (error) {
      console.error('Failed to start AI wizard setup:', error)
    }
  }

  return (
    <div className="flex-1 space-y-6 p-8 pt-6">
      {/* Header with Enhanced Statistics */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">AI-Powered Integrations</h2>
          <p className="text-muted-foreground">
            Connect and automate your entire marketing & business ecosystem with AI
          </p>
        </div>
        <div className="flex items-center gap-6">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4 text-green-500" />
              <span className="font-medium">{connectedCount} Connected</span>
            </div>
            <div className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-blue-500" />
              <span className="font-medium">${totalCost.toFixed(2)}/mo</span>
            </div>
            {errorCount > 0 && (
              <div className="flex items-center gap-2">
                <XCircle className="h-4 w-4 text-red-500" />
                <span className="font-medium">{errorCount} Issues</span>
              </div>
            )}
            {pendingCount > 0 && (
              <div className="flex items-center gap-2">
                <AlertCircle className="h-4 w-4 text-yellow-500" />
                <span className="font-medium">{pendingCount} Pending</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* AI-Powered Quick Actions */}
      <Card className="border-2 border-dashed border-primary/20">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <Brain className="h-6 w-6 text-primary" />
              </div>
              <div>
                <h3 className="font-semibold">AI Integration Assistant</h3>
                <p className="text-sm text-muted-foreground">
                  Let AI help you set up integrations automatically
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <Button 
                variant="outline" 
                onClick={() => setIsAIWizardOpen(true)}
                className="gap-2"
              >
                <Sparkles className="h-4 w-4" />
                AI Setup Wizard
              </Button>
              <Button 
                variant="outline" 
                onClick={() => setBulkOperationMode(!bulkOperationMode)}
                className="gap-2"
              >
                <Database className="h-4 w-4" />
                Bulk Operations
              </Button>
              <Button className="gap-2">
                <Rocket className="h-4 w-4" />
                Quick Connect
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Search and Filters */}
      <div className="flex items-center gap-4">
        <div className="flex-1">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search integrations, features, or capabilities..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>
        {bulkOperationMode && (
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">
              {selectedIntegrations.length} selected
            </span>
            <Button 
              size="sm" 
              disabled={selectedIntegrations.length === 0}
              onClick={handleBulkConnect}
            >
              Connect Selected
            </Button>
          </div>
        )}
      </div>

      {/* Enhanced Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-5 lg:grid-cols-10">
          <TabsTrigger value="all">All ({integrations.length})</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="advertising">Advertising</TabsTrigger>
          <TabsTrigger value="social">Social</TabsTrigger>
          <TabsTrigger value="email">Email</TabsTrigger>
          <TabsTrigger value="webmaster">Webmaster</TabsTrigger>
          <TabsTrigger value="crm">CRM</TabsTrigger>
          <TabsTrigger value="ecommerce">E-commerce</TabsTrigger>
          <TabsTrigger value="automation">Automation</TabsTrigger>
          <TabsTrigger value="payment">Payments</TabsTrigger>
        </TabsList>

        <TabsContent value={activeTab} className="space-y-4">
          {/* Integration Grid */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {filteredIntegrations.map((integration) => (
              <Card key={integration.id} className="relative group hover:shadow-lg transition-shadow">
                {bulkOperationMode && (
                  <div className="absolute top-3 left-3 z-10">
                    <input
                      type="checkbox"
                      checked={selectedIntegrations.includes(integration.id)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedIntegrations([...selectedIntegrations, integration.id])
                        } else {
                          setSelectedIntegrations(selectedIntegrations.filter(id => id !== integration.id))
                        }
                      }}
                      className="rounded"
                    />
                  </div>
                )}
                
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                  <div className="flex items-center space-x-2">
                    {getCategoryIcon(integration.category)}
                    <div>
                      <CardTitle className="text-lg">{integration.name}</CardTitle>
                      <div className="flex items-center gap-2 mt-1">
                        <Badge variant="outline" className={`text-xs ${getPriorityColor(integration.priority)}`}>
                          {integration.priority} priority
                        </Badge>
                        {integration.aiFeatures && (
                          <Badge variant="outline" className="text-xs bg-purple-50 text-purple-700">
                            <Brain className="h-3 w-3 mr-1" />
                            AI-Powered
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    {getStatusIcon(integration.status)}
                    {getStatusBadge(integration.status)}
                  </div>
                </CardHeader>
                
                <CardContent className="space-y-4">
                  <CardDescription>{integration.description}</CardDescription>
                  
                  {/* Features */}
                  <div>
                    <h4 className="text-sm font-medium mb-2">Key Features</h4>
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

                  {/* AI Capabilities */}
                  {integration.aiFeatures && integration.aiFeatures.length > 0 && (
                    <div>
                      <h4 className="text-sm font-medium mb-2 flex items-center gap-1">
                        <Sparkles className="h-3 w-3" />
                        AI Capabilities
                      </h4>
                      <div className="flex flex-wrap gap-1">
                        {integration.aiFeatures.slice(0, 2).map((feature) => (
                          <Badge key={feature} variant="outline" className="text-xs bg-blue-50 text-blue-700">
                            {feature}
                          </Badge>
                        ))}
                        {integration.aiFeatures.length > 2 && (
                          <Badge variant="outline" className="text-xs bg-blue-50 text-blue-700">
                            +{integration.aiFeatures.length - 2} more
                          </Badge>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Connection Health & Usage */}
                  {integration.connected && (
                    <div className="space-y-2">
                      {integration.connectionHealth && (
                        <div>
                          <div className="flex justify-between text-xs mb-1">
                            <span>Connection Health</span>
                            <span>{integration.connectionHealth}%</span>
                          </div>
                          <Progress value={integration.connectionHealth} className="h-1" />
                        </div>
                      )}
                      
                      {integration.dataSync && (
                        <div className="flex items-center gap-2 text-xs text-muted-foreground">
                          <Activity className="h-3 w-3" />
                          <span>
                            {integration.dataSync.recordsCount?.toLocaleString()} records • 
                            Next sync: {integration.dataSync.nextSync ? 
                              new Date(integration.dataSync.nextSync).toLocaleTimeString() : 
                              'N/A'
                            }
                          </span>
                        </div>
                      )}

                      {integration.monthlyUsage && (
                        <div className="flex justify-between text-xs text-muted-foreground">
                          <span>{integration.monthlyUsage.apiCalls.toLocaleString()} API calls</span>
                          <span>${integration.monthlyUsage.cost.toFixed(2)}/mo</span>
                        </div>
                      )}
                    </div>
                  )}

                  {integration.lastSync && (
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      <Clock className="h-3 w-3" />
                      Last sync: {new Date(integration.lastSync).toLocaleString()}
                    </div>
                  )}

                  {/* Action Buttons */}
                  <div className="flex gap-2 pt-2">
                    {integration.status === 'connected' ? (
                      <>
                        <Button 
                          variant="outline" 
                          size="sm" 
                          onClick={() => {/* Test connection */}}
                          className="flex-1"
                        >
                          <RefreshCw className="h-3 w-3 mr-1" />
                          Test
                        </Button>
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button variant="outline" size="sm" className="flex-1">
                              <Settings className="h-3 w-3 mr-1" />
                              Configure
                            </Button>
                          </DialogTrigger>
                          <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
                            <DialogHeader>
                              <DialogTitle className="flex items-center gap-2">
                                {getCategoryIcon(integration.category)}
                                Configure {integration.name}
                              </DialogTitle>
                              <DialogDescription>
                                Manage your integration settings, automation rules, and AI features
                              </DialogDescription>
                            </DialogHeader>
                            
                            <Tabs defaultValue="settings" className="w-full">
                              <TabsList>
                                <TabsTrigger value="settings">Settings</TabsTrigger>
                                <TabsTrigger value="automation">Automation</TabsTrigger>
                                <TabsTrigger value="ai">AI Features</TabsTrigger>
                                <TabsTrigger value="analytics">Analytics</TabsTrigger>
                              </TabsList>
                              
                              <TabsContent value="settings" className="space-y-4">
                                {/* API Keys Configuration */}
                                {integration.apiKeysRequired.map((keyName) => (
                                  <div key={keyName} className="space-y-2">
                                    <Label htmlFor={keyName}>{keyName}</Label>
                                    <div className="relative">
                                      <Input
                                        id={keyName}
                                        type={showApiKey[keyName] ? 'text' : 'password'}
                                        value={apiKeys[keyName] || '••••••••••••••••'}
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
                                
                                {/* Webhook Configuration */}
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

                                {/* Sync Settings */}
                                {integration.dataSync && (
                                  <div className="space-y-3">
                                    <Label>Data Synchronization</Label>
                                    <div className="grid grid-cols-2 gap-4">
                                      <div>
                                        <Label className="text-xs">Sync Frequency</Label>
                                        <p className="text-sm">{integration.dataSync.frequency}</p>
                                      </div>
                                      <div>
                                        <Label className="text-xs">Records Synced</Label>
                                        <p className="text-sm">{integration.dataSync.recordsCount?.toLocaleString()}</p>
                                      </div>
                                    </div>
                                  </div>
                                )}
                              </TabsContent>
                              
                              <TabsContent value="automation" className="space-y-4">
                                <div>
                                  <h4 className="font-medium mb-3">Automation Capabilities</h4>
                                  <div className="space-y-3">
                                    {integration.automationCapabilities?.map((capability, index) => (
                                      <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                                        <div className="flex items-center gap-3">
                                          <Zap className="h-4 w-4 text-yellow-500" />
                                          <span className="text-sm">{capability}</span>
                                        </div>
                                        <Switch defaultChecked={index < 2} />
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              </TabsContent>
                              
                              <TabsContent value="ai" className="space-y-4">
                                <div>
                                  <h4 className="font-medium mb-3 flex items-center gap-2">
                                    <Brain className="h-4 w-4 text-purple-500" />
                                    AI-Powered Features
                                  </h4>
                                  <div className="space-y-3">
                                    {integration.aiFeatures?.map((feature, index) => (
                                      <div key={index} className="flex items-center justify-between p-3 border rounded-lg bg-purple-50/50">
                                        <div className="flex items-center gap-3">
                                          <Sparkles className="h-4 w-4 text-purple-500" />
                                          <div>
                                            <span className="text-sm font-medium">{feature}</span>
                                            <p className="text-xs text-muted-foreground">
                                              Powered by machine learning algorithms
                                            </p>
                                          </div>
                                        </div>
                                        <Switch defaultChecked={true} />
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              </TabsContent>
                              
                              <TabsContent value="analytics" className="space-y-4">
                                {integration.monthlyUsage && (
                                  <div className="grid grid-cols-3 gap-4">
                                    <Card>
                                      <CardContent className="p-4">
                                        <div className="text-2xl font-bold">{integration.monthlyUsage.apiCalls.toLocaleString()}</div>
                                        <p className="text-xs text-muted-foreground">API Calls This Month</p>
                                      </CardContent>
                                    </Card>
                                    <Card>
                                      <CardContent className="p-4">
                                        <div className="text-2xl font-bold">{integration.monthlyUsage.dataTransfer}</div>
                                        <p className="text-xs text-muted-foreground">Data Transfer</p>
                                      </CardContent>
                                    </Card>
                                    <Card>
                                      <CardContent className="p-4">
                                        <div className="text-2xl font-bold">${integration.monthlyUsage.cost.toFixed(2)}</div>
                                        <p className="text-xs text-muted-foreground">Monthly Cost</p>
                                      </CardContent>
                                    </Card>
                                  </div>
                                )}
                                
                                {integration.connectionHealth && (
                                  <div>
                                    <Label className="text-sm font-medium">Connection Health</Label>
                                    <div className="mt-2">
                                      <Progress value={integration.connectionHealth} className="h-2" />
                                      <p className="text-xs text-muted-foreground mt-1">
                                        {integration.connectionHealth}% - Excellent connection quality
                                      </p>
                                    </div>
                                  </div>
                                )}
                              </TabsContent>
                            </Tabs>
                            
                            <div className="flex gap-3 pt-4">
                              <Button className="flex-1">
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
                                      Any active automations and data syncing will be stopped.
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
                          </DialogContent>
                        </Dialog>
                      </>
                    ) : (
                      <Button 
                        onClick={() => handleConnect(integration)}
                        className="w-full"
                        disabled={integration.status === 'pending' || integration.status === 'syncing'}
                      >
                        {integration.status === 'pending' ? (
                          <>
                            <RefreshCw className="h-3 w-3 mr-1 animate-spin" />
                            Connecting...
                          </>
                        ) : integration.status === 'syncing' ? (
                          <>
                            <RefreshCw className="h-3 w-3 mr-1 animate-spin" />
                            Syncing...
                          </>
                        ) : integration.setupType === 'ai_wizard' ? (
                          <>
                            <Brain className="h-3 w-3 mr-1" />
                            AI Setup
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

          {/* No Results State */}
          {filteredIntegrations.length === 0 && (
            <Card className="flex flex-col items-center justify-center py-12">
              <div className="text-center space-y-4">
                <Search className="h-12 w-12 text-muted-foreground mx-auto" />
                <div>
                  <h3 className="text-lg font-medium">No integrations found</h3>
                  <p className="text-muted-foreground">
                    {searchQuery ? 
                      `No integrations match "${searchQuery}"` : 
                      'No integrations match the selected category'
                    }
                  </p>
                </div>
                {searchQuery && (
                  <Button variant="outline" onClick={() => setSearchQuery('')}>
                    Clear search
                  </Button>
                )}
              </div>
            </Card>
          )}
        </TabsContent>
      </Tabs>

      {/* Status Alerts */}
      {errorCount > 0 && (
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            {errorCount} integration{errorCount > 1 ? 's have' : ' has'} connection issues. 
            Click on the integration cards to review and fix the configuration.
          </AlertDescription>
        </Alert>
      )}

      {/* AI Integration Wizard Modal */}
      <Dialog open={isAIWizardOpen} onOpenChange={setIsAIWizardOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Brain className="h-5 w-5 text-purple-500" />
              AI Integration Wizard
            </DialogTitle>
            <DialogDescription>
              Let our AI assistant help you set up integrations automatically based on your business needs
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-6 py-4">
            <div className="space-y-4">
              <div>
                <Label>Business Type</Label>
                <select className="w-full p-2 border rounded-md">
                  <option value="">Select your business type</option>
                  <option value="ecommerce">E-commerce</option>
                  <option value="saas">SaaS</option>
                  <option value="agency">Marketing Agency</option>
                  <option value="consulting">Consulting</option>
                  <option value="local">Local Business</option>
                </select>
              </div>
              
              <div>
                <Label>Primary Goals</Label>
                <Textarea 
                  placeholder="Describe what you want to achieve with integrations (e.g., track customer journey from ads to purchase, automate email marketing, sync CRM data...)"
                  className="min-h-[100px]"
                />
              </div>
              
              <div>
                <Label>Current Tools (Optional)</Label>
                <Input placeholder="List tools you're already using (e.g., Shopify, Google Ads, Mailchimp...)" />
              </div>
            </div>
            
            <div className="flex gap-3">
              <Button className="flex-1" onClick={() => handleAIWizardSetup('ai-wizard', {})}>
                <Sparkles className="h-4 w-4 mr-2" />
                Start AI Setup
              </Button>
              <Button variant="outline" onClick={() => setIsAIWizardOpen(false)}>
                Cancel
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}