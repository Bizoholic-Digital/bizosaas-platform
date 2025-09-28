/**
 * Feature Guard Component
 * Conditionally renders content based on organization tier and feature access
 */

'use client'

import React from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Lock, Zap, Crown, Sparkles } from 'lucide-react'
import { useFeatureAccess, SubscriptionTier, TIER_CONFIGS } from '@/lib/feature-access'
import { useAuthStore } from '@/lib/auth-store'

interface FeatureGuardProps {
  feature: string
  children: React.ReactNode
  fallback?: React.ReactNode
  showUpgradePrompt?: boolean
}

export function FeatureGuard({ 
  feature, 
  children, 
  fallback,
  showUpgradePrompt = true
}: FeatureGuardProps) {
  const featureAccess = useFeatureAccess()
  const { user } = useAuthStore()

  // For demo purposes, use the user's organization from auth store
  // In production, this would come from API
  const hasAccess = featureAccess.hasFeature(feature)

  if (hasAccess) {
    return <>{children}</>
  }

  if (fallback) {
    return <>{fallback}</>
  }

  if (showUpgradePrompt) {
    return <UpgradePrompt feature={feature} />
  }

  return null
}

interface UpgradePromptProps {
  feature: string
}

function UpgradePrompt({ feature }: UpgradePromptProps) {
  const featureAccess = useFeatureAccess()
  const suggestions = featureAccess.getUpgradeSuggestions()

  const getTierIcon = (tier: SubscriptionTier) => {
    switch (tier) {
      case 'tier_2': return <Zap className="h-4 w-4" />
      case 'tier_3': return <Crown className="h-4 w-4" />
      default: return <Sparkles className="h-4 w-4" />
    }
  }

  const getTierColor = (tier: SubscriptionTier) => {
    switch (tier) {
      case 'tier_2': return 'bg-orange-100 text-orange-800 border-orange-200'
      case 'tier_3': return 'bg-purple-100 text-purple-800 border-purple-200'
      default: return 'bg-blue-100 text-blue-800 border-blue-200'
    }
  }

  if (!suggestions.shouldUpgrade || !suggestions.nextTier) {
    return null
  }

  const nextTierConfig = TIER_CONFIGS[suggestions.nextTier]

  return (
    <Card className="border-2 border-dashed border-gray-300 bg-gray-50">
      <CardHeader className="text-center">
        <div className="mx-auto w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center mb-2">
          <Lock className="h-6 w-6 text-gray-500" />
        </div>
        <CardTitle className="text-lg">Premium Feature</CardTitle>
        <CardDescription>
          This feature requires a higher subscription tier
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="text-center">
          <Badge className={`mb-2 ${getTierColor(suggestions.nextTier)}`}>
            {getTierIcon(suggestions.nextTier)}
            <span className="ml-1">{nextTierConfig.name}</span>
          </Badge>
          <p className="text-sm text-gray-600 mb-4">
            Upgrade to <strong>{nextTierConfig.name}</strong> ({nextTierConfig.price}) to access:
          </p>
        </div>
        
        <ul className="space-y-2">
          {suggestions.reasons.slice(0, 3).map((reason, index) => (
            <li key={index} className="flex items-center text-sm">
              <Sparkles className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
              {reason}
            </li>
          ))}
        </ul>

        <div className="pt-4 flex gap-2">
          <Button className="flex-1" size="sm">
            Upgrade Now
          </Button>
          <Button variant="outline" size="sm">
            Learn More
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

// Specific feature guards for common use cases
export function AIAgentsGuard({ children, fallback }: Omit<FeatureGuardProps, 'feature'>) {
  return (
    <FeatureGuard feature="ai_agents" fallback={fallback}>
      {children}
    </FeatureGuard>
  )
}

export function AnalyticsGuard({ children, fallback }: Omit<FeatureGuardProps, 'feature'>) {
  return (
    <FeatureGuard feature="analytics" fallback={fallback}>
      {children}
    </FeatureGuard>
  )
}

export function CustomIntegrationsGuard({ children, fallback }: Omit<FeatureGuardProps, 'feature'>) {
  return (
    <FeatureGuard feature="custom_integrations" fallback={fallback}>
      {children}
    </FeatureGuard>
  )
}

export function WhiteLabelGuard({ children, fallback }: Omit<FeatureGuardProps, 'feature'>) {
  return (
    <FeatureGuard feature="white_label" fallback={fallback}>
      {children}
    </FeatureGuard>
  )
}