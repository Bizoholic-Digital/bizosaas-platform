'use client'

import { ReactNode } from 'react'
import { useTenant } from '@/hooks/use-tenant'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Lock } from 'lucide-react'

interface FeatureGateProps {
  feature: string
  children: ReactNode
  fallback?: ReactNode
  subscriptionTier?: 'free' | 'starter' | 'professional' | 'enterprise'
  showUpgrade?: boolean
}

export function FeatureGate({ 
  feature, 
  children, 
  fallback, 
  subscriptionTier,
  showUpgrade = false 
}: FeatureGateProps) {
  const { tenant, isLoading } = useTenant()

  if (isLoading) {
    return (
      <div className="animate-pulse bg-gray-200 rounded-lg h-32 flex items-center justify-center">
        <span className="text-gray-500">Loading...</span>
      </div>
    )
  }

  if (!tenant) {
    return (
      <Alert>
        <Lock className="h-4 w-4" />
        <AlertDescription>
          Unable to verify tenant access. Please try again.
        </AlertDescription>
      </Alert>
    )
  }

  // Check if feature is enabled for tenant
  const hasFeature = tenant.features.includes('*') || tenant.features.includes(feature)
  
  // Check subscription tier if specified
  const tierHierarchy = {
    'free': 0,
    'starter': 1, 
    'professional': 2,
    'enterprise': 3
  }

  const hasRequiredTier = !subscriptionTier || 
    tierHierarchy[tenant.subscription_tier] >= tierHierarchy[subscriptionTier]

  const hasAccess = hasFeature && hasRequiredTier

  if (hasAccess) {
    return <>{children}</>
  }

  if (fallback) {
    return <>{fallback}</>
  }

  if (showUpgrade) {
    return (
      <Alert className="border-amber-200 bg-amber-50">
        <Lock className="h-4 w-4 text-amber-600" />
        <AlertDescription className="text-amber-800">
          <div className="space-y-2">
            <p>This feature requires a {subscriptionTier || 'higher'} plan or the "{feature}" feature.</p>
            <p className="text-sm">
              Current plan: <strong>{tenant.subscription_tier}</strong>
              {!hasFeature && (
                <span className="ml-2 text-xs bg-red-100 text-red-700 px-2 py-1 rounded">
                  Feature not enabled
                </span>
              )}
            </p>
          </div>
        </AlertDescription>
      </Alert>
    )
  }

  return null
}

// Hook for programmatic feature checking
export function useFeatureAccess() {
  const { tenant } = useTenant()

  const hasFeature = (feature: string): boolean => {
    if (!tenant) return false
    return tenant.features.includes('*') || tenant.features.includes(feature)
  }

  const hasSubscriptionTier = (requiredTier: 'free' | 'starter' | 'professional' | 'enterprise'): boolean => {
    if (!tenant) return false
    
    const tierHierarchy = {
      'free': 0,
      'starter': 1,
      'professional': 2, 
      'enterprise': 3
    }

    return tierHierarchy[tenant.subscription_tier] >= tierHierarchy[requiredTier]
  }

  const hasAccess = (feature: string, subscriptionTier?: string): boolean => {
    return hasFeature(feature) && (!subscriptionTier || hasSubscriptionTier(subscriptionTier as any))
  }

  return {
    tenant,
    hasFeature,
    hasSubscriptionTier,
    hasAccess
  }
}