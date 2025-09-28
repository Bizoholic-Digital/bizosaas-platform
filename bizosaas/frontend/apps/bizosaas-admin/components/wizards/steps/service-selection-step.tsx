"use client"

import React, { useState } from 'react'
import { UseFormReturn } from 'react-hook-form'
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from '../../ui/card'
import { Button } from '../../ui/button'
import { Badge } from '../../ui/badge'
import { Input } from '../../ui/input'
import { 
  CreditCard, 
  Target, 
  Brain, 
  BarChart3, 
  Server,
  Search,
  Filter,
  CheckCircle,
  Info,
  Star,
  Shield,
  Zap,
  Globe,
  DollarSign
} from 'lucide-react'
import { cn } from '../../../lib/utils'
import { APIService } from '../api-key-management-wizard'

// Comprehensive service catalog
const SERVICE_CATALOG: APIService[] = [
  // Payment Services
  {
    id: 'stripe',
    name: 'Stripe',
    category: 'payment',
    icon: <CreditCard className="h-5 w-5" />,
    description: 'Online payment processing with global reach',
    requiredKeys: ['publishable_key', 'secret_key', 'webhook_secret'],
    testEndpoints: ['/v1/payment_methods', '/v1/customers'],
    documentation: 'https://stripe.com/docs/api',
    securityLevel: 'enterprise',
    compliance: ['PCI-DSS', 'SOC2', 'GDPR']
  },
  {
    id: 'paypal',
    name: 'PayPal',
    category: 'payment',
    icon: <CreditCard className="h-5 w-5" />,
    description: 'Global digital payments and merchant services',
    requiredKeys: ['client_id', 'client_secret'],
    testEndpoints: ['/v2/payments', '/v1/identity/oauth2/token'],
    documentation: 'https://developer.paypal.com',
    securityLevel: 'enterprise',
    compliance: ['PCI-DSS', 'SOC2']
  },
  {
    id: 'razorpay',
    name: 'Razorpay',
    category: 'payment',
    icon: <CreditCard className="h-5 w-5" />,
    description: 'India-focused payment gateway with UPI support',
    requiredKeys: ['key_id', 'key_secret'],
    testEndpoints: ['/v1/payments', '/v1/customers'],
    documentation: 'https://razorpay.com/docs',
    securityLevel: 'enhanced',
    compliance: ['PCI-DSS', 'RBI']
  },
  {
    id: 'payu',
    name: 'PayU',
    category: 'payment',
    icon: <CreditCard className="h-5 w-5" />,
    description: 'Emerging markets payment solution',
    requiredKeys: ['merchant_key', 'salt'],
    testEndpoints: ['/merchant/postservice', '/get_transaction_details'],
    documentation: 'https://devguide.payu.in',
    securityLevel: 'enhanced',
    compliance: ['PCI-DSS']
  },
  {
    id: 'ccavenue',
    name: 'CCAvenue',
    category: 'payment',
    icon: <CreditCard className="h-5 w-5" />,
    description: 'Indian payment gateway with multiple options',
    requiredKeys: ['merchant_id', 'access_code', 'working_key'],
    testEndpoints: ['/transaction/transaction.do'],
    documentation: 'https://www.ccavenue.com/developers',
    securityLevel: 'enhanced',
    compliance: ['PCI-DSS']
  },

  // Marketing Services
  {
    id: 'google-ads',
    name: 'Google Ads',
    category: 'marketing',
    icon: <Target className="h-5 w-5" />,
    description: 'Google advertising platform for search and display ads',
    requiredKeys: ['developer_token', 'client_id', 'client_secret', 'refresh_token'],
    testEndpoints: ['/googleads/v14/customers', '/googleads/v14/campaigns'],
    documentation: 'https://developers.google.com/google-ads',
    securityLevel: 'enterprise',
    compliance: ['SOC2', 'GDPR']
  },
  {
    id: 'facebook-ads',
    name: 'Meta Ads',
    category: 'marketing',
    icon: <Target className="h-5 w-5" />,
    description: 'Facebook and Instagram advertising platform',
    requiredKeys: ['app_id', 'app_secret', 'access_token'],
    testEndpoints: ['/v18.0/me/adaccounts', '/v18.0/campaigns'],
    documentation: 'https://developers.facebook.com/docs/marketing-apis',
    securityLevel: 'enterprise',
    compliance: ['SOC2', 'GDPR']
  },
  {
    id: 'linkedin-ads',
    name: 'LinkedIn Marketing',
    category: 'marketing',
    icon: <Target className="h-5 w-5" />,
    description: 'Professional network advertising platform',
    requiredKeys: ['client_id', 'client_secret', 'access_token'],
    testEndpoints: ['/v2/adAccountsV2', '/v2/campaignGroups'],
    documentation: 'https://docs.microsoft.com/linkedin',
    securityLevel: 'enhanced',
    compliance: ['SOC2', 'GDPR']
  },
  {
    id: 'tiktok-ads',
    name: 'TikTok Ads',
    category: 'marketing',
    icon: <Target className="h-5 w-5" />,
    description: 'Short-form video advertising platform',
    requiredKeys: ['app_id', 'secret', 'access_token'],
    testEndpoints: ['/open_api/v1.3/advertiser/get', '/open_api/v1.3/campaign/get'],
    documentation: 'https://ads.tiktok.com/marketing_api/docs',
    securityLevel: 'enhanced',
    compliance: ['SOC2']
  },
  {
    id: 'twitter-ads',
    name: 'X Ads (Twitter)',
    category: 'marketing',
    icon: <Target className="h-5 w-5" />,
    description: 'Social media advertising on X platform',
    requiredKeys: ['api_key', 'api_secret', 'access_token', 'access_secret'],
    testEndpoints: ['/12/accounts', '/12/campaigns'],
    documentation: 'https://developer.twitter.com/en/docs/twitter-ads-api',
    securityLevel: 'enhanced',
    compliance: ['SOC2']
  },

  // AI Services
  {
    id: 'openai',
    name: 'OpenAI',
    category: 'ai',
    icon: <Brain className="h-5 w-5" />,
    description: 'GPT models and AI-powered applications',
    requiredKeys: ['api_key', 'organization'],
    testEndpoints: ['/v1/models', '/v1/chat/completions'],
    documentation: 'https://platform.openai.com/docs',
    securityLevel: 'enterprise',
    compliance: ['SOC2', 'GDPR']
  },
  {
    id: 'anthropic',
    name: 'Anthropic Claude',
    category: 'ai',
    icon: <Brain className="h-5 w-5" />,
    description: 'Advanced AI assistant and language model',
    requiredKeys: ['api_key'],
    testEndpoints: ['/v1/messages', '/v1/models'],
    documentation: 'https://docs.anthropic.com',
    securityLevel: 'enterprise',
    compliance: ['SOC2', 'GDPR']
  },
  {
    id: 'synthesia',
    name: 'Synthesia.io',
    category: 'ai',
    icon: <Brain className="h-5 w-5" />,
    description: 'AI video generation and avatar creation',
    requiredKeys: ['api_key'],
    testEndpoints: ['/v2/videos', '/v2/avatars'],
    documentation: 'https://docs.synthesia.io',
    securityLevel: 'enhanced',
    compliance: ['GDPR']
  },
  {
    id: 'midjourney',
    name: 'Midjourney',
    category: 'ai',
    icon: <Brain className="h-5 w-5" />,
    description: 'AI-powered image generation and art creation',
    requiredKeys: ['api_key'],
    testEndpoints: ['/v1/imagine', '/v1/upscale'],
    documentation: 'https://docs.midjourney.com',
    securityLevel: 'enhanced',
    compliance: ['SOC2']
  },

  // Analytics Services
  {
    id: 'google-analytics',
    name: 'Google Analytics',
    category: 'analytics',
    icon: <BarChart3 className="h-5 w-5" />,
    description: 'Web analytics and user behavior tracking',
    requiredKeys: ['measurement_id', 'api_secret'],
    testEndpoints: ['/v1beta/properties', '/v1beta/reports'],
    documentation: 'https://developers.google.com/analytics',
    securityLevel: 'enterprise',
    compliance: ['SOC2', 'GDPR']
  },
  {
    id: 'facebook-pixel',
    name: 'Meta Pixel',
    category: 'analytics',
    icon: <BarChart3 className="h-5 w-5" />,
    description: 'Facebook advertising pixel for conversion tracking',
    requiredKeys: ['pixel_id', 'access_token'],
    testEndpoints: ['/v18.0/pixel/events', '/v18.0/pixel/stats'],
    documentation: 'https://developers.facebook.com/docs/meta-pixel',
    securityLevel: 'enhanced',
    compliance: ['SOC2', 'GDPR']
  },

  // Infrastructure Services
  {
    id: 'aws-s3',
    name: 'AWS S3',
    category: 'infrastructure',
    icon: <Server className="h-5 w-5" />,
    description: 'Amazon cloud storage and file management',
    requiredKeys: ['access_key', 'secret_key', 'region'],
    testEndpoints: ['/v2/buckets', '/v2/objects'],
    documentation: 'https://docs.aws.amazon.com/s3',
    securityLevel: 'enterprise',
    compliance: ['SOC2', 'GDPR', 'HIPAA']
  },
  {
    id: 'cloudflare',
    name: 'Cloudflare',
    category: 'infrastructure',
    icon: <Server className="h-5 w-5" />,
    description: 'CDN, DNS, and web performance optimization',
    requiredKeys: ['api_token', 'zone_id'],
    testEndpoints: ['/client/v4/zones', '/client/v4/user'],
    documentation: 'https://developers.cloudflare.com',
    securityLevel: 'enterprise',
    compliance: ['SOC2', 'GDPR']
  },
  {
    id: 'digitalocean',
    name: 'DigitalOcean',
    category: 'infrastructure',
    icon: <Server className="h-5 w-5" />,
    description: 'Cloud infrastructure and container services',
    requiredKeys: ['access_token'],
    testEndpoints: ['/v2/droplets', '/v2/kubernetes/clusters'],
    documentation: 'https://docs.digitalocean.com/reference/api',
    securityLevel: 'enhanced',
    compliance: ['SOC2']
  }
]

const CATEGORY_CONFIG = {
  payment: {
    name: 'Payment Processing',
    icon: DollarSign,
    color: 'bg-green-100 text-green-800 border-green-200',
    description: 'Secure payment gateways and transaction processing'
  },
  marketing: {
    name: 'Marketing & Advertising',
    icon: Target,
    color: 'bg-blue-100 text-blue-800 border-blue-200',
    description: 'Digital advertising platforms and campaign management'
  },
  ai: {
    name: 'AI & Machine Learning',
    icon: Brain,
    color: 'bg-purple-100 text-purple-800 border-purple-200',
    description: 'Artificial intelligence and automation services'
  },
  analytics: {
    name: 'Analytics & Tracking',
    icon: BarChart3,
    color: 'bg-orange-100 text-orange-800 border-orange-200',
    description: 'Data analytics and performance monitoring'
  },
  infrastructure: {
    name: 'Infrastructure & Cloud',
    icon: Server,
    color: 'bg-gray-100 text-gray-800 border-gray-200',
    description: 'Cloud services and infrastructure management'
  }
}

interface ServiceSelectionStepProps {
  form: UseFormReturn<any>
  configurations: any[]
  setConfigurations: React.Dispatch<React.SetStateAction<any[]>>
}

export function ServiceSelectionStep({ 
  form,
  configurations,
  setConfigurations
}: ServiceSelectionStepProps) {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [bulkMode, setBulkMode] = useState(false)
  const [selectedServices, setSelectedServices] = useState<Set<string>>(
    new Set(form.getValues('selectedServices') || [])
  )

  const filteredServices = SERVICE_CATALOG.filter(service => {
    const matchesSearch = service.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         service.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = !selectedCategory || service.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  const handleServiceToggle = (serviceId: string) => {
    const newSelected = new Set(selectedServices)
    if (newSelected.has(serviceId)) {
      newSelected.delete(serviceId)
    } else {
      newSelected.add(serviceId)
    }
    setSelectedServices(newSelected)
    form.setValue('selectedServices', Array.from(newSelected))
  }

  const handleBulkSelectCategory = (category: string) => {
    if (!bulkMode) return
    
    const categoryServices = SERVICE_CATALOG
      .filter(service => service.category === category)
      .map(service => service.id)
    
    const newSelected = new Set([...selectedServices, ...categoryServices])
    setSelectedServices(newSelected)
    form.setValue('selectedServices', Array.from(newSelected))
  }

  const getServiceById = (id: string) => SERVICE_CATALOG.find(s => s.id === id)

  const getRecommendations = () => {
    if (selectedServices.size === 0) return []
    
    const recommendations = []
    
    // If payment service selected, recommend analytics
    if (Array.from(selectedServices).some(id => getServiceById(id)?.category === 'payment')) {
      recommendations.push({
        type: 'analytics',
        message: 'Consider adding Google Analytics to track payment conversions'
      })
    }
    
    // If marketing service selected, recommend AI
    if (Array.from(selectedServices).some(id => getServiceById(id)?.category === 'marketing')) {
      recommendations.push({
        type: 'ai',
        message: 'AI services can help optimize your advertising campaigns'
      })
    }
    
    return recommendations
  }

  return (
    <div className="space-y-6">
      {/* Search and Filters */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
              placeholder="Search services..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant={bulkMode ? "default" : "outline"}
              size="sm"
              onClick={() => setBulkMode(!bulkMode)}
            >
              <Filter className="h-4 w-4 mr-2" />
              Bulk Select
            </Button>
          </div>
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap gap-2">
          <Button
            variant={selectedCategory === null ? "default" : "outline"}
            size="sm"
            onClick={() => setSelectedCategory(null)}
          >
            All Categories
          </Button>
          {Object.entries(CATEGORY_CONFIG).map(([key, config]) => {
            const Icon = config.icon
            return (
              <Button
                key={key}
                variant={selectedCategory === key ? "default" : "outline"}
                size="sm"
                onClick={() => setSelectedCategory(key)}
              >
                <Icon className="h-4 w-4 mr-2" />
                {config.name}
              </Button>
            )
          })}
        </div>
      </div>

      {/* Selection Summary */}
      {selectedServices.size > 0 && (
        <Card className="border-blue-200 bg-blue-50 dark:bg-blue-950 dark:border-blue-800">
          <CardContent className="pt-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-5 w-5 text-blue-600" />
                <span className="font-medium text-blue-800 dark:text-blue-200">
                  {selectedServices.size} service{selectedServices.size !== 1 ? 's' : ''} selected
                </span>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  setSelectedServices(new Set())
                  form.setValue('selectedServices', [])
                }}
              >
                Clear All
              </Button>
            </div>
            <div className="mt-3 flex flex-wrap gap-2">
              {Array.from(selectedServices).map(serviceId => {
                const service = getServiceById(serviceId)
                if (!service) return null
                return (
                  <Badge key={serviceId} variant="secondary" className="flex items-center space-x-1">
                    {service.icon}
                    <span>{service.name}</span>
                  </Badge>
                )
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Service Categories */}
      <div className="space-y-6">
        {Object.entries(CATEGORY_CONFIG).map(([categoryKey, categoryConfig]) => {
          const categoryServices = filteredServices.filter(service => service.category === categoryKey)
          if (categoryServices.length === 0) return null

          const Icon = categoryConfig.icon
          const selectedCount = categoryServices.filter(service => selectedServices.has(service.id)).length

          return (
            <Card key={categoryKey}>
              <CardHeader 
                className={cn(
                  "cursor-pointer transition-colors",
                  bulkMode && "hover:bg-gray-50 dark:hover:bg-gray-800"
                )}
                onClick={() => bulkMode && handleBulkSelectCategory(categoryKey)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={cn("p-2 rounded-lg", categoryConfig.color)}>
                      <Icon className="h-5 w-5" />
                    </div>
                    <div>
                      <CardTitle className="text-lg">{categoryConfig.name}</CardTitle>
                      <CardDescription>{categoryConfig.description}</CardDescription>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    {selectedCount > 0 && (
                      <Badge variant="secondary">
                        {selectedCount} selected
                      </Badge>
                    )}
                    {bulkMode && (
                      <Button variant="outline" size="sm">
                        Select All
                      </Button>
                    )}
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {categoryServices.map(service => {
                    const isSelected = selectedServices.has(service.id)
                    return (
                      <Card
                        key={service.id}
                        className={cn(
                          "cursor-pointer transition-all duration-200 hover:shadow-md",
                          isSelected 
                            ? "ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-950" 
                            : "hover:ring-1 hover:ring-gray-300"
                        )}
                        onClick={() => handleServiceToggle(service.id)}
                      >
                        <CardContent className="p-4">
                          <div className="flex items-start justify-between">
                            <div className="flex items-start space-x-3">
                              <div className="p-2 bg-gray-100 dark:bg-gray-800 rounded-lg">
                                {service.icon}
                              </div>
                              <div className="flex-1 min-w-0">
                                <h3 className="font-medium text-gray-900 dark:text-white">
                                  {service.name}
                                </h3>
                                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                                  {service.description}
                                </p>
                                <div className="flex flex-wrap gap-1 mt-2">
                                  <Badge 
                                    variant="outline" 
                                    className={cn(
                                      "text-xs",
                                      service.securityLevel === 'enterprise' 
                                        ? 'border-green-300 text-green-700'
                                        : 'border-blue-300 text-blue-700'
                                    )}
                                  >
                                    <Shield className="h-3 w-3 mr-1" />
                                    {service.securityLevel}
                                  </Badge>
                                  {service.compliance.map(comp => (
                                    <Badge key={comp} variant="outline" className="text-xs">
                                      {comp}
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              {isSelected && (
                                <CheckCircle className="h-5 w-5 text-blue-600" />
                              )}
                              <Button variant="ghost" size="sm">
                                <Info className="h-4 w-4" />
                              </Button>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    )
                  })}
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Recommendations */}
      {getRecommendations().length > 0 && (
        <Card className="border-yellow-200 bg-yellow-50 dark:bg-yellow-950 dark:border-yellow-800">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2 text-yellow-800 dark:text-yellow-200">
              <Star className="h-5 w-5" />
              <span>Smart Recommendations</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {getRecommendations().map((rec, index) => (
                <div key={index} className="flex items-center space-x-2 text-yellow-700 dark:text-yellow-300">
                  <Zap className="h-4 w-4" />
                  <span className="text-sm">{rec.message}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Integration Requirements */}
      {selectedServices.size > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Integration Requirements Analysis</CardTitle>
            <CardDescription>
              Review the requirements for your selected services
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Array.from(selectedServices).map(serviceId => {
                const service = getServiceById(serviceId)
                if (!service) return null
                
                return (
                  <div key={serviceId} className="border rounded-lg p-4">
                    <div className="flex items-center space-x-3 mb-3">
                      {service.icon}
                      <h4 className="font-medium">{service.name}</h4>
                      <Badge variant="outline">{service.category}</Badge>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="font-medium text-gray-600 dark:text-gray-400 mb-1">
                          Required Keys:
                        </p>
                        <ul className="space-y-1">
                          {service.requiredKeys.map(key => (
                            <li key={key} className="flex items-center space-x-2">
                              <Key className="h-3 w-3 text-gray-400" />
                              <span className="font-mono">{key}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <p className="font-medium text-gray-600 dark:text-gray-400 mb-1">
                          Test Endpoints:
                        </p>
                        <ul className="space-y-1">
                          {service.testEndpoints.map(endpoint => (
                            <li key={endpoint} className="flex items-center space-x-2">
                              <Globe className="h-3 w-3 text-gray-400" />
                              <span className="font-mono text-xs">{endpoint}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default ServiceSelectionStep