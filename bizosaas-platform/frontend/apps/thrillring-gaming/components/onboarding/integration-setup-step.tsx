'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  CheckCircle, Clock, AlertCircle, ExternalLink, CreditCard, 
  Mail, ShoppingCart, BarChart3, Zap, Users, Globe,
  RefreshCw, ArrowRight, Shield, Rocket
} from 'lucide-react'
import { StripeSetup } from '@/components/onboarding/integrations/stripe-setup'
import { GoogleAdsSetup } from '@/components/onboarding/integrations/google-ads-setup'
import { EmailMarketingSetup } from '@/components/onboarding/integrations/email-marketing-setup'
import { EcommerceSetup } from '@/components/onboarding/integrations/ecommerce-setup'
import { AnalyticsSetup } from '@/components/onboarding/integrations/analytics-setup'

interface IntegrationStatus {
  id: string
  name: string
  description: string
  tier: 'tier1' | 'tier2' | 'tier3'
  category: string
  status: 'not_started' | 'in_progress' | 'completed' | 'error' | 'pending_approval'
  estimatedTime: string
  icon: React.ComponentType<{ className?: string }>
  priority: number
  benefits: string[]
  setupComponent?: React.ComponentType<any>
}

const INTEGRATIONS: IntegrationStatus[] = [
  // Tier 1 - Instant Access
  {
    id: 'stripe',
    name: 'Stripe Payments',
    description: 'Accept payments and manage subscriptions',
    tier: 'tier1',
    category: 'Payments',
    status: 'not_started',
    estimatedTime: '5 minutes',
    icon: CreditCard,
    priority: 1,
    benefits: [
      'Accept credit card payments',
      'Recurring billing for subscriptions',
      'Automated invoicing',
      'Fraud protection'
    ],
    setupComponent: StripeSetup
  },
  {
    id: 'email_marketing',
    name: 'Email Marketing',
    description: 'Automated email campaigns and newsletters',
    tier: 'tier1',
    category: 'Marketing',
    status: 'not_started',
    estimatedTime: '10 minutes',
    icon: Mail,
    priority: 2,
    benefits: [
      'Welcome email sequences',
      'Newsletter automation',
      'Campaign analytics',
      'A/B testing'
    ],
    setupComponent: EmailMarketingSetup
  },
  {
    id: 'basic_analytics',
    name: 'Analytics Dashboard',
    description: 'Track website and campaign performance',
    tier: 'tier1',
    category: 'Analytics',
    status: 'not_started',
    estimatedTime: '5 minutes',
    icon: BarChart3,
    priority: 3,
    benefits: [
      'Real-time traffic data',
      'Conversion tracking',
      'Custom dashboards',
      'Automated reports'
    ],
    setupComponent: AnalyticsSetup
  },
  
  // Tier 2 - Quick Setup
  {
    id: 'google_ads',
    name: 'Google Ads',
    description: 'Search and display advertising campaigns',
    tier: 'tier2',
    category: 'Advertising',
    status: 'not_started',
    estimatedTime: '30 minutes',
    icon: Globe,
    priority: 4,
    benefits: [
      'Search campaign automation',
      'Smart bidding strategies',
      'Keyword optimization',
      'Performance insights'
    ],
    setupComponent: GoogleAdsSetup
  },
  {
    id: 'ecommerce',
    name: 'E-commerce',
    description: 'Shopify and WooCommerce integrations',
    tier: 'tier2',
    category: 'E-commerce',
    status: 'not_started',
    estimatedTime: '20 minutes',
    icon: ShoppingCart,
    priority: 5,
    benefits: [
      'Product catalog sync',
      'Order management',
      'Inventory tracking',
      'Customer segmentation'
    ],
    setupComponent: EcommerceSetup
  },
  
  // Tier 3 - Application Process
  {
    id: 'meta_ads',
    name: 'Meta Ads',
    description: 'Facebook and Instagram advertising',
    tier: 'tier3',
    category: 'Advertising',
    status: 'pending_approval',
    estimatedTime: '3-7 days',
    icon: Users,
    priority: 6,
    benefits: [
      'Social media campaigns',
      'Advanced targeting',
      'Creative optimization',
      'Lookalike audiences'
    ]
  },
  {
    id: 'linkedin_ads',
    name: 'LinkedIn Ads',
    description: 'B2B advertising and lead generation',
    tier: 'tier3',
    category: 'Advertising',
    status: 'pending_approval',
    estimatedTime: '1-2 weeks',
    icon: Users,
    priority: 7,
    benefits: [
      'B2B lead generation',
      'Professional targeting',
      'Thought leadership',
      'Account-based marketing'
    ]
  }
]

const TIER_CONFIG = {
  tier1: {
    label: 'Tier 1: Instant Access',
    description: 'Get started immediately with core functionality',
    color: 'bg-green-500',
    textColor: 'text-green-700',
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200',
    icon: Zap
  },
  tier2: {
    label: 'Tier 2: Quick Setup',
    description: 'Guided setup with immediate activation',
    color: 'bg-yellow-500',
    textColor: 'text-yellow-700',
    bgColor: 'bg-yellow-50',
    borderColor: 'border-yellow-200',
    icon: Clock
  },
  tier3: {
    label: 'Tier 3: Application Process',
    description: 'Premium features requiring platform approval',
    color: 'bg-orange-500',
    textColor: 'text-orange-700',
    bgColor: 'bg-orange-50',
    borderColor: 'border-orange-200',
    icon: Shield
  }
}

interface IntegrationSetupStepProps {
  businessData: any
  onComplete: (data: any) => void
  initialData?: any
}

export function IntegrationSetupStep({ businessData, onComplete, initialData = {} }: IntegrationSetupStepProps) {
  const [integrations, setIntegrations] = useState<IntegrationStatus[]>(INTEGRATIONS)
  const [activeTab, setActiveTab] = useState<string>('tier1')
  const [selectedIntegration, setSelectedIntegration] = useState<string | null>(null)
  const [completedIntegrations, setCompletedIntegrations] = useState(new Set<string>())

  // Calculate progress
  const tier1Integrations = integrations.filter(i => i.tier === 'tier1')
  const tier1Completed = tier1Integrations.filter(i => completedIntegrations.has(i.id))
  const tier1Progress = (tier1Completed.length / tier1Integrations.length) * 100

  const totalCompleted = Array.from(completedIntegrations).length
  const canProceed = tier1Completed.length >= 1 // At least one Tier 1 integration

  const updateIntegrationStatus = (integrationId: string, status: IntegrationStatus['status'], data?: any) => {
    setIntegrations(prev => 
      prev.map(integration => 
        integration.id === integrationId 
          ? { ...integration, status }
          : integration
      )
    )

    if (status === 'completed') {
      setCompletedIntegrations(prev => new Set(Array.from(prev).concat([integrationId])))
    }
  }

  const handleSetupComplete = (integrationId: string, setupData: any) => {
    updateIntegrationStatus(integrationId, 'completed', setupData)
    setSelectedIntegration(null)
  }

  const handleContinue = () => {
    const completedData = {
      completedIntegrations: Array.from(completedIntegrations),
      tier1Progress: tier1Progress,
      totalIntegrations: integrations.length
    }
    onComplete(completedData)
  }

  const renderIntegrationCard = (integration: IntegrationStatus) => {
    const tierConfig = TIER_CONFIG[integration.tier]
    const StatusIcon = integration.status === 'completed' ? CheckCircle :
                      integration.status === 'in_progress' ? RefreshCw :
                      integration.status === 'pending_approval' ? Clock :
                      integration.status === 'error' ? AlertCircle :
                      integration.icon

    return (
      <Card 
        key={integration.id}
        className={`
          transition-all duration-200 cursor-pointer hover:shadow-md
          ${selectedIntegration === integration.id ? 'ring-2 ring-blue-500' : ''}
          ${integration.status === 'completed' ? 'bg-green-50 border-green-200' : ''}
          ${integration.status === 'error' ? 'bg-red-50 border-red-200' : ''}
        `}
        onClick={() => {
          if (integration.tier === 'tier1' || integration.tier === 'tier2') {
            setSelectedIntegration(selectedIntegration === integration.id ? null : integration.id)
          }
        }}
      >
        <CardContent className="p-4">
          <div className="flex items-start justify-between mb-3">
            <div className="flex items-start gap-3">
              <div className={`
                flex h-10 w-10 items-center justify-center rounded-lg
                ${integration.status === 'completed' ? 'bg-green-500 text-white' : 
                  integration.status === 'error' ? 'bg-red-500 text-white' :
                  integration.status === 'in_progress' ? 'bg-blue-500 text-white' :
                  'bg-gray-100 text-gray-600'
                }
              `}>
                <StatusIcon className={`h-5 w-5 ${integration.status === 'in_progress' ? 'animate-spin' : ''}`} />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="font-semibold">{integration.name}</h4>
                  <Badge 
                    variant="outline" 
                    className={`${tierConfig.textColor} ${tierConfig.borderColor} text-xs`}
                  >
                    {integration.tier.toUpperCase()}
                  </Badge>
                </div>
                <p className="text-sm text-muted-foreground mb-2">
                  {integration.description}
                </p>
                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                  <span>⏱️ {integration.estimatedTime}</span>
                  <span>📂 {integration.category}</span>
                </div>
              </div>
            </div>
            
            {integration.status === 'completed' && (
              <Badge variant="default" className="bg-green-500">
                ✓ Connected
              </Badge>
            )}
            {integration.status === 'pending_approval' && (
              <Badge variant="outline" className="text-orange-600 border-orange-300">
                Approval Pending
              </Badge>
            )}
            {(integration.tier === 'tier1' || integration.tier === 'tier2') && 
             integration.status === 'not_started' && (
              <Button variant="outline" size="sm">
                Set Up
              </Button>
            )}
          </div>

          {/* Benefits */}
          <div className="space-y-1">
            {integration.benefits.slice(0, 2).map((benefit, index) => (
              <div key={index} className="flex items-center gap-2 text-xs text-muted-foreground">
                <div className="w-1 h-1 bg-gray-400 rounded-full" />
                {benefit}
              </div>
            ))}
          </div>

          {/* Setup Component */}
          {selectedIntegration === integration.id && integration.setupComponent && (
            <div className="mt-4 pt-4 border-t">
              <integration.setupComponent
                businessData={businessData}
                onComplete={(data: any) => handleSetupComplete(integration.id, data)}
                onCancel={() => setSelectedIntegration(null)}
              />
            </div>
          )}
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      {/* Progress Overview */}
      <Alert className="border-blue-200 bg-blue-50 dark:border-blue-800 dark:bg-blue-950/30">
        <Rocket className="h-4 w-4 text-blue-600" />
        <AlertDescription className="text-blue-700 dark:text-blue-300">
          <div className="space-y-3">
            <div>
              <strong>Quick Start Strategy:</strong> We'll get you live with Tier 1 integrations first, 
              then add advanced features as they become available.
            </div>
            <div className="flex items-center gap-4">
              <div className="flex-1">
                <div className="flex justify-between text-sm mb-1">
                  <span>Tier 1 Progress ({tier1Completed.length}/{tier1Integrations.length})</span>
                  <span>{Math.round(tier1Progress)}%</span>
                </div>
                <Progress value={tier1Progress} className="h-2" />
              </div>
              <Badge 
                variant={canProceed ? "default" : "secondary"}
                className={canProceed ? "bg-green-500" : ""}
              >
                {canProceed ? "Ready to Launch" : "Setup Required"}
              </Badge>
            </div>
          </div>
        </AlertDescription>
      </Alert>

      {/* Integration Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          {Object.entries(TIER_CONFIG).map(([tier, config]) => {
            const tierIntegrations = integrations.filter(i => i.tier === tier)
            const tierCompleted = tierIntegrations.filter(i => completedIntegrations.has(i.id))
            const TierIcon = config.icon
            
            return (
              <TabsTrigger key={tier} value={tier} className="relative">
                <div className="flex items-center gap-2">
                  <TierIcon className="h-4 w-4" />
                  <span className="hidden sm:inline">{config.label.split(':')[1]}</span>
                  <span className="sm:hidden">{tier.toUpperCase()}</span>
                  <Badge variant="outline" className="text-xs">
                    {tierCompleted.length}/{tierIntegrations.length}
                  </Badge>
                </div>
              </TabsTrigger>
            )
          })}
        </TabsList>

        {Object.entries(TIER_CONFIG).map(([tier, config]) => {
          const tierIntegrations = integrations.filter(i => i.tier === tier)
          const TierIcon = config.icon

          return (
            <TabsContent key={tier} value={tier} className="space-y-4">
              <Card className={`${config.bgColor} ${config.borderColor}`}>
                <CardHeader className="pb-3">
                  <CardTitle className={`flex items-center gap-2 ${config.textColor}`}>
                    <TierIcon className="h-5 w-5" />
                    {config.label}
                  </CardTitle>
                  <CardDescription className={config.textColor}>
                    {config.description}
                  </CardDescription>
                </CardHeader>
              </Card>

              <div className="grid grid-cols-1 gap-4">
                {tierIntegrations.map(renderIntegrationCard)}
              </div>

              {tier === 'tier3' && (
                <Alert>
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>
                    <strong>Tier 3 integrations require platform approval.</strong> We've already started 
                    the application process for you. You'll receive updates as approvals come through, 
                    and features will be automatically activated.
                  </AlertDescription>
                </Alert>
              )}
            </TabsContent>
          )
        })}
      </Tabs>

      {/* Action Buttons */}
      <div className="flex justify-between items-center pt-6 border-t">
        <div className="text-sm text-muted-foreground">
          {totalCompleted > 0 && (
            <>✅ {totalCompleted} integration{totalCompleted !== 1 ? 's' : ''} completed</>
          )}
        </div>
        
        <div className="flex gap-3">
          {canProceed && (
            <Button onClick={handleContinue} size="lg" className="min-w-[200px]">
              Continue to Dashboard
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          )}
          
          {!canProceed && (
            <Button 
              disabled 
              size="lg" 
              className="min-w-[200px]"
              title="Complete at least one Tier 1 integration to continue"
            >
              Setup Required
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}