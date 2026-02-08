'use client'

import { useState, useEffect } from 'react'
import { tenantAPI, TenantInfo, DEFAULT_TENANT } from '@/lib/tenant-api'

/**
 * Lightweight frontend tenant hook
 * Relies on backend tenant_context_service.py for heavy lifting
 */
export function useTenant() {
  const [tenant, setTenant] = useState<TenantInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadTenantContext()
  }, [])

  const loadTenantContext = async () => {
    try {
      setLoading(true)
      const result = await tenantAPI.getTenantContext()
      
      if (result.success && result.tenant) {
        setTenant(result.tenant)
        applyTenantBranding(result.tenant)
        setError(null)
      } else {
        setTenant(DEFAULT_TENANT)
        setError(result.error || 'Failed to load tenant')
      }
    } catch (err) {
      setTenant(DEFAULT_TENANT)
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  const applyTenantBranding = (tenantInfo: TenantInfo) => {
    const { branding } = tenantInfo
    
    if (branding.primary_color) {
      document.documentElement.style.setProperty('--primary', branding.primary_color)
    }
    
    if (branding.secondary_color) {
      document.documentElement.style.setProperty('--secondary', branding.secondary_color)  
    }
    
    // Update favicon if available
    if (branding.logo_url) {
      const favicon = document.querySelector('link[rel="icon"]') as HTMLLinkElement
      if (favicon) {
        favicon.href = branding.logo_url
      }
    }
    
    // Update page title
    if (branding.brand_name) {
      document.title = `${branding.brand_name} - Platform`
    }
  }

  const hasFeature = (feature: string): boolean => {
    return tenantAPI.hasFeature(tenant, feature)
  }

  const getTenantApiUrl = (service: string): string => {
    return tenantAPI.getTenantApiUrl(tenant, service)
  }

  return {
    tenant,
    loading,
    error,
    hasFeature,
    getTenantApiUrl,
    refresh: loadTenantContext
  }
}

/**
 * Hook for tenant-specific theming and branding
 */
export function useTenantTheme() {
  const { tenant, loading } = useTenant()

  const config = {
    branding: {
      companyName: tenant?.branding?.brand_name || 'BizOSaaS',
      primaryColor: tenant?.branding?.primary_color || '#0066CC',
      secondaryColor: tenant?.branding?.secondary_color || '#22C55E',
      logoUrl: tenant?.branding?.logo_url || '/logo.svg'
    }
  }

  return {
    config,
    loading,
    tenant
  }
}