'use client'

import { createContext, useContext, useEffect, ReactNode } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { useTenantStore } from '@/store/useTenantStore'
import { brainGateway } from '@/lib/brain-gateway-client'
import { useAuth } from '@/lib/auth'
import type { Tenant } from '@/types/tenant'

interface TenantContextValue {
  currentTenant: Tenant | null
  availableTenants: Tenant[]
  isLoading: boolean
  error: string | null
  switchTenant: (tenantId: string) => Promise<void>
  loadTenants: () => Promise<void>
}

const TenantContext = createContext<TenantContextValue | undefined>(undefined)

export function TenantProvider({ children }: { children: ReactNode }) {
  const {
    currentTenant,
    availableTenants,
    isLoading,
    error,
    switchTenant,
    loadTenants,
  } = useTenantStore()

  const { isAuthenticated } = useAuth()
  const router = useRouter()
  const pathname = usePathname()

  // Load tenants on mount
  useEffect(() => {
    loadTenants()
  }, [loadTenants])

  // Check onboarding status - ONLY for authenticated users on portal routes
  useEffect(() => {
    async function checkOnboarding() {
      // Define routes where onboarding check should NOT run
      const excludedRoutes = [
        '/onboarding',
        '/login',
        '/signup',
        '/forgot-password',
        '/reset-password',
        '/verify-email',
        '/',
      ]

      const isExcludedRoute = excludedRoutes.some(route => pathname === route || pathname.startsWith(route + '/'))

      // Only check onboarding if:
      // 1. User is authenticated
      // 2. We have a current tenant
      // 3. Not currently loading
      // 4. Not on an excluded route
      if (isAuthenticated && currentTenant && !isLoading && !isExcludedRoute) {
        try {
          const status = await brainGateway.onboarding.getStatus()
          if (status && !status.is_completed) {
            router.push('/onboarding')
          }
        } catch (err) {
          console.error('Failed to check onboarding status:', err)
        }
      }
    }
    checkOnboarding()
  }, [isAuthenticated, currentTenant, isLoading, pathname, router])

  const value: TenantContextValue = {
    currentTenant,
    availableTenants,
    isLoading,
    error,
    switchTenant,
    loadTenants,
  }

  return <TenantContext.Provider value={value}>{children}</TenantContext.Provider>
}

export function useTenant() {
  const context = useContext(TenantContext)
  if (context === undefined) {
    throw new Error('useTenant must be used within a TenantProvider')
  }
  return context
}

// Hook to check if current tenant has a specific feature enabled
export function useTenantFeature(feature: keyof Tenant['settings']['features']) {
  const { currentTenant } = useTenant()
  return currentTenant?.settings.features[feature] ?? false
}

// Hook to check if user has required role for current tenant
export function useTenantRole(requiredRole: 'client' | 'partner' | 'moderator' | 'admin') {
  const { currentTenant } = useTenant()
  const user = useTenantStore((state: any) => state.user)

  if (!currentTenant || !user) return false

  const roleHierarchy = ['client', 'partner', 'moderator', 'admin']
  const userRole = user.roles.find((r: any) => r.tenantId === currentTenant.id)

  if (!userRole) return false

  const userRoleIndex = roleHierarchy.indexOf(userRole.role)
  const requiredRoleIndex = roleHierarchy.indexOf(requiredRole)

  return userRoleIndex >= requiredRoleIndex
}
