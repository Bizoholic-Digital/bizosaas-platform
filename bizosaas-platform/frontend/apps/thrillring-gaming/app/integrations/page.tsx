'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { GoogleAnalyticsIntegration } from '@/components/integrations/google-analytics-integration'
import { GoogleAdsIntegration } from '@/components/integrations/google-ads-integration'
import { DjangoCrmIntegration } from '@/components/integrations/django-crm-integration'
import { GoogleSearchConsoleIntegration } from '@/components/integrations/google-search-console-integration'
import { 
  BarChart3, 
  Facebook, 
  Mail, 
  Search, 
  Globe, 
  MessageSquare,
  Settings,
  Plus,
  Filter,
  CheckCircle2,
  AlertCircle,
  RefreshCw,
  Users
} from 'lucide-react'
import { Input } from '@/components/ui/input'

interface Integration {
  id: string
  name: string
  category: 'analytics' | 'advertising' | 'social' | 'email' | 'seo' | 'crm' | 'other'
  description: string
  status: 'connected' | 'available' | 'error'
  icon: any
  color: string
  features?: string[]
  component?: React.ComponentType<any>
}

const integrations: Integration[] = [
  {
    id: 'django-crm',
    name: 'Django CRM',
    category: 'crm',
    description: 'Built-in AI-powered CRM with multi-tenant lead management',
    status: 'connected',
    icon: Users,
    color: 'from-green-500 to-teal-600',
    features: ['AI Lead Scoring', 'Multi-tenant', 'Activity Tracking', 'Integration Insights'],
    component: DjangoCrmIntegration
  },
  {
    id: 'google-analytics-4',
    name: 'Google Analytics 4',
    category: 'analytics',
    description: 'Advanced website analytics with AI-powered insights',
    status: 'available',
    icon: BarChart3,
    color: 'from-orange-500 to-red-600',
    features: ['Real-time Analytics', 'Goal Tracking', 'Custom Reports', 'AI Insights'],
    component: GoogleAnalyticsIntegration
  },
  {
    id: 'google-ads',
    name: 'Google Ads',
    category: 'advertising',
    description: 'Automated Google Ads campaign management and optimization',
    status: 'available',
    icon: Search,
    color: 'from-blue-500 to-green-500',
    features: ['Campaign Automation', 'Keyword Research', 'Bid Optimization', 'Performance Tracking'],
    component: GoogleAdsIntegration
  },
  {
    id: 'google-search-console',
    name: 'Google Search Console',
    category: 'seo',
    description: 'Monitor search performance, SEO health, and site indexing status',
    status: 'available',
    icon: Search,
    color: 'from-blue-500 to-indigo-600',
    features: ['Search Performance Analytics', 'Index Coverage Monitoring', 'Core Web Vitals', 'Sitemap Management', 'URL Inspection'],
    component: GoogleSearchConsoleIntegration
  },
  {
    id: 'meta-ads',
    name: 'Meta Ads Manager',
    category: 'advertising',
    description: 'Facebook & Instagram advertising with AI optimization',
    status: 'connected',
    icon: Facebook,
    color: 'from-blue-600 to-purple-600',
    features: ['Creative Testing', 'Audience Insights', 'Campaign Management', 'ROI Tracking']
  },
  {
    id: 'mailchimp',
    name: 'Mailchimp',
    category: 'email',
    description: 'Email marketing automation and campaign management',
    status: 'available',
    icon: Mail,
    color: 'from-yellow-500 to-orange-500',
    features: ['Email Automation', 'List Management', 'A/B Testing', 'Analytics']
  },
  {
    id: 'linkedin',
    name: 'LinkedIn Marketing',
    category: 'social',
    description: 'Professional networking and B2B marketing automation',
    status: 'available',
    icon: MessageSquare,
    color: 'from-blue-700 to-blue-500',
    features: ['Lead Generation', 'Content Publishing', 'Audience Targeting', 'Campaign Management']
  },
  {
    id: 'semrush',
    name: 'SEMrush',
    category: 'seo',
    description: 'SEO and content marketing optimization tools',
    status: 'error',
    icon: Globe,
    color: 'from-purple-500 to-pink-500',
    features: ['Keyword Research', 'Site Audit', 'Competitor Analysis', 'Content Optimization']
  }
]

const categories = [
  { id: 'all', name: 'All Integrations', count: integrations.length },
  { id: 'crm', name: 'CRM', count: integrations.filter(i => i.category === 'crm').length },
  { id: 'analytics', name: 'Analytics', count: integrations.filter(i => i.category === 'analytics').length },
  { id: 'advertising', name: 'Advertising', count: integrations.filter(i => i.category === 'advertising').length },
  { id: 'social', name: 'Social Media', count: integrations.filter(i => i.category === 'social').length },
  { id: 'seo', name: 'SEO', count: integrations.filter(i => i.category === 'seo').length },
  { id: 'email', name: 'Email Marketing', count: integrations.filter(i => i.category === 'email').length }
]

export default function IntegrationsPage() {
  const [activeCategory, setActiveCategory] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedIntegration, setSelectedIntegration] = useState<Integration | null>(null)

  const filteredIntegrations = integrations.filter(integration => {
    const matchesCategory = activeCategory === 'all' || integration.category === activeCategory
    const matchesSearch = integration.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         integration.description.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesCategory && matchesSearch
  })

  const StatusIcon = ({ status }: { status: Integration['status'] }) => {
    switch (status) {
      case 'connected':
        return <CheckCircle2 className="w-4 h-4 text-green-500" />
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-500" />
      default:
        return <RefreshCw className="w-4 h-4 text-gray-400" />
    }
  }

  const StatusBadge = ({ status }: { status: Integration['status'] }) => {
    const config = {
      connected: { variant: "default" as const, text: "Connected" },
      available: { variant: "secondary" as const, text: "Available" },
      error: { variant: "destructive" as const, text: "Error" }
    }
    
    return <Badge variant={config[status].variant}>{config[status].text}</Badge>
  }

  if (selectedIntegration?.component) {
    const IntegrationComponent = selectedIntegration.component
    return (
      <div className="container mx-auto py-6">
        <div className="flex items-center gap-4 mb-6">
          <Button variant="ghost" onClick={() => setSelectedIntegration(null)}>
            ← Back to Integrations
          </Button>
          <div>
            <h1 className="text-2xl font-bold">{selectedIntegration.name}</h1>
            <p className="text-muted-foreground">{selectedIntegration.description}</p>
          </div>
        </div>
        <IntegrationComponent />
      </div>
    )
  }

  return (
    <div className="container mx-auto py-6">
      <div className="flex flex-col gap-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold">Integrations</h1>
            <p className="text-muted-foreground">
              Connect your favorite tools and automate your marketing workflows
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline">
              <Filter className="w-4 h-4 mr-2" />
              Filter
            </Button>
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              Add Integration
            </Button>
          </div>
        </div>

        {/* Search */}
        <div className="max-w-md">
          <Input
            placeholder="Search integrations..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full"
          />
        </div>

        {/* Categories */}
        <Tabs value={activeCategory} onValueChange={setActiveCategory}>
          <TabsList className="grid grid-cols-7 w-full max-w-5xl">
            {categories.map((category) => (
              <TabsTrigger key={category.id} value={category.id} className="text-xs">
                {category.name}
                <Badge variant="secondary" className="ml-1 text-xs">
                  {category.count}
                </Badge>
              </TabsTrigger>
            ))}
          </TabsList>

          <TabsContent value={activeCategory} className="mt-6">
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {filteredIntegrations.map((integration) => {
                const Icon = integration.icon
                return (
                  <Card 
                    key={integration.id} 
                    className="cursor-pointer transition-all hover:shadow-md border-2 hover:border-primary/20"
                    onClick={() => integration.component ? setSelectedIntegration(integration) : null}
                  >
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <div className={`w-12 h-12 bg-gradient-to-br ${integration.color} rounded-lg flex items-center justify-center`}>
                            <Icon className="w-6 h-6 text-white" />
                          </div>
                          <div>
                            <CardTitle className="text-lg">{integration.name}</CardTitle>
                            <div className="flex items-center gap-2 mt-1">
                              <StatusIcon status={integration.status} />
                              <span className="text-xs text-muted-foreground capitalize">
                                {integration.category}
                              </span>
                            </div>
                          </div>
                        </div>
                        <StatusBadge status={integration.status} />
                      </div>
                    </CardHeader>
                    <CardContent>
                      <CardDescription className="mb-4">
                        {integration.description}
                      </CardDescription>
                      
                      {integration.features && (
                        <div className="space-y-2">
                          <p className="text-sm font-medium">Key Features:</p>
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
                      )}

                      <div className="mt-4">
                        {integration.status === 'connected' ? (
                          <Button variant="outline" className="w-full">
                            <Settings className="w-4 h-4 mr-2" />
                            Manage
                          </Button>
                        ) : integration.component ? (
                          <Button className="w-full">
                            <Plus className="w-4 h-4 mr-2" />
                            Connect
                          </Button>
                        ) : (
                          <Button variant="outline" className="w-full" disabled>
                            Coming Soon
                          </Button>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                )
              })}
            </div>

            {filteredIntegrations.length === 0 && (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Search className="w-6 h-6 text-gray-400" />
                </div>
                <h3 className="text-lg font-medium mb-2">No integrations found</h3>
                <p className="text-muted-foreground">
                  Try adjusting your search or category filter
                </p>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}