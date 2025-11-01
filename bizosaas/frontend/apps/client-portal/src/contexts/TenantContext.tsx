'use client'

import { createContext, useContext, useEffect, ReactNode } from 'react'
import { useTenantStore } from '@/store/useTenantStore'
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

  // Load tenants on mount
  useEffect(() => {
    loadTenants()
  }, [loadTenants])

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
  const user = useTenantStore((state) => state.user)

  if (!currentTenant || !user) return false

  const roleHierarchy = ['client', 'partner', 'moderator', 'admin']
  const userRole = user.roles.find((r) => r.tenantId === currentTenant.id)

  if (!userRole) return false

  const userRoleIndex = roleHierarchy.indexOf(userRole.role)
  const requiredRoleIndex = roleHierarchy.indexOf(requiredRole)

  return userRoleIndex >= requiredRoleIndex
}
