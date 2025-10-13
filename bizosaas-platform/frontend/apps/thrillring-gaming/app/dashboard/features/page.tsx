/**
 * Feature Access Demo Page
 * Shows tier-based feature restrictions in action
 */

'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Separator } from '@/components/ui/separator'
import { 
  FeatureGuard, 
  AIAgentsGuard, 
  AnalyticsGuard, 
  CustomIntegrationsGuard,
  WhiteLabelGuard 
} from '@/components/feature-guard'
import { useFeatureAccess, TIER_CONFIGS } from '@/lib/feature-access'
import { useAuthStore } from '@/lib/auth-store'
import { 
  Bot, 
  BarChart3, 
  Zap, 
  Crown, 
  Settings, 
  Users, 
  Package, 
  ShoppingCart,
  HardDrive,
  Sparkles,
  Lock
} from 'lucide-react'

export default function FeaturesPage() {
  const { user, organization } = useAuthStore()
  const featureAccess = useFeatureAccess()
  
  if (!user || !organization) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <Lock className="h-12 w-12 mx-auto mb-4 text-gray-400" />
          <p className="text-gray-600">Loading organization data...</p>
        </div>
      </div>
    )
  }

  const tierConfig = featureAccess.getTierConfig()
  const restrictions = featureAccess.getRestrictions()
  const suggestions = featureAccess.getUpgradeSuggestions()

  const getTierIcon = (tier: string) => {
    switch (tier) {
      case 'tier_2': return <Zap className="h-4 w-4" />
      case 'tier_3': return <Crown className="h-4 w-4" />
      default: return <Sparkles className="h-4 w-4" />
    }
  }

  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'tier_2': return 'bg-orange-100 text-orange-800 border-orange-200'
      case 'tier_3': return 'bg-purple-100 text-purple-800 border-purple-200'
      default: return 'bg-blue-100 text-blue-800 border-blue-200'
    }
  }

  // Mock current usage data
  const currentUsage = {
    products: 45,
    orders: 156,
    staff: 3,
    storage: 2.4
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Feature Access Control</h1>
        <p className="text-muted-foreground mt-2">
          Tier-based feature access demonstration for the BizOSaaS platform
        </p>
      </div>

      {/* Current Subscription */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                {getTierIcon(organization.subscription_tier)}
                Current Subscription
              </CardTitle>
              <CardDescription>
                {organization.name} • {tierConfig?.name || 'Unknown Tier'}
              </CardDescription>
            </div>
            <Badge className={getTierColor(organization.subscription_tier)}>
              {tierConfig?.price || 'Custom'}
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span>Products</span>
                <span>{currentUsage.products}{restrictions?.maxProducts !== -1 ? ` / ${restrictions?.maxProducts}` : ''}</span>
              </div>
              <Progress value={restrictions?.maxProducts !== -1 ? (currentUsage.products / restrictions!.maxProducts) * 100 : 0} />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span>Orders</span>
                <span>{currentUsage.orders}{restrictions?.maxOrdersPerMonth !== -1 ? ` / ${restrictions?.maxOrdersPerMonth}` : ''}</span>
              </div>
              <Progress value={restrictions?.maxOrdersPerMonth !== -1 ? (currentUsage.orders / restrictions!.maxOrdersPerMonth) * 100 : 0} />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span>Staff</span>
                <span>{currentUsage.staff}{restrictions?.maxStaffUsers !== -1 ? ` / ${restrictions?.maxStaffUsers}` : ''}</span>
              </div>
              <Progress value={restrictions?.maxStaffUsers !== -1 ? (currentUsage.staff / restrictions!.maxStaffUsers) * 100 : 0} />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span>Storage (GB)</span>
                <span>{currentUsage.storage} / {restrictions?.storageLimitGb}</span>
              </div>
              <Progress value={restrictions ? (currentUsage.storage / restrictions.storageLimitGb) * 100 : 0} />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Feature Access Demos */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* AI Agents Feature */}
        <AIAgentsGuard>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bot className="h-5 w-5" />
                AI Agents Dashboard
              </CardTitle>
              <CardDescription>
                Access to 46+ autonomous AI agents for marketing automation
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Active Agents</span>
                  <Badge variant="secondary">28 Running</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Tasks Completed</span>
                  <span className="font-mono text-sm">1,247</span>
                </div>
                <Button className="w-full">Manage AI Agents</Button>
              </div>
            </CardContent>
          </Card>
        </AIAgentsGuard>

        {/* Analytics Feature */}
        <AnalyticsGuard>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Advanced Analytics
              </CardTitle>
              <CardDescription>
                Detailed performance metrics and cross-client insights
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Revenue Growth</span>
                  <Badge variant="default">+23.4%</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Conversion Rate</span>
                  <span className="font-mono text-sm">4.2%</span>
                </div>
                <Button className="w-full">View Analytics</Button>
              </div>
            </CardContent>
          </Card>
        </AnalyticsGuard>

        {/* Custom Integrations Feature */}
        <CustomIntegrationsGuard>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="h-5 w-5" />
                Custom Integrations
              </CardTitle>
              <CardDescription>
                Build and manage custom API integrations
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Active Integrations</span>
                  <Badge variant="secondary">12 Connected</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Custom Webhooks</span>
                  <span className="font-mono text-sm">8</span>
                </div>
                <Button className="w-full">Manage Integrations</Button>
              </div>
            </CardContent>
          </Card>
        </CustomIntegrationsGuard>

        {/* White Label Feature */}
        <WhiteLabelGuard>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Crown className="h-5 w-5" />
                White Label Platform
              </CardTitle>
              <CardDescription>
                Customize branding and create client portals
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Client Portals</span>
                  <Badge variant="secondary">5 Active</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Custom Domains</span>
                  <span className="font-mono text-sm">3</span>
                </div>
                <Button className="w-full">Brand Settings</Button>
              </div>
            </CardContent>
          </Card>
        </WhiteLabelGuard>
      </div>

      {/* Basic Features (Always Available) */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Basic Features (All Tiers)</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-base">
                <Package className="h-4 w-4" />
                Basic E-commerce
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Product management, basic storefront, order processing
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-base">
                <Settings className="h-4 w-4" />
                Basic CMS
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Content management, basic templates, SEO tools
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-base">
                <Users className="h-4 w-4" />
                Basic CRM
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Contact management, basic sales pipeline, lead tracking
              </p>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Upgrade Suggestions */}
      {suggestions.shouldUpgrade && (
        <Card className="border-2 border-dashed border-primary/20 bg-primary/5">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5" />
              Unlock More Features
            </CardTitle>
            <CardDescription>
              Upgrade to {TIER_CONFIGS[suggestions.nextTier!].name} to get access to:
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 mb-4">
              {suggestions.reasons.map((reason, index) => (
                <li key={index} className="flex items-center text-sm">
                  <Sparkles className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                  {reason}
                </li>
              ))}
            </ul>
            <div className="flex gap-2">
              <Button>Upgrade to {TIER_CONFIGS[suggestions.nextTier!].name}</Button>
              <Button variant="outline">Compare Plans</Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}