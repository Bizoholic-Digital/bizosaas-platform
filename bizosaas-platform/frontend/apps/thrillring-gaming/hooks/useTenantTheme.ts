import { useState, useEffect } from 'react'

interface TenantConfig {
  branding: {
    companyName: string
    primaryColor: string
    secondaryColor: string
    logo?: string
  }
  features: {
    enableAnalytics: boolean
    enableReviews: boolean
    enableWishlist: boolean
  }
  customization: {
    theme: 'light' | 'dark' | 'auto'
    layout: 'default' | 'compact' | 'minimal'
  }
}

const defaultConfig: TenantConfig = {
  branding: {
    companyName: 'Bizoholic',
    logo: '/logos/bizoholic-logo.png',
    primaryColor: '#0f172a', // slate-900 
    secondaryColor: '#3b82f6', // blue-500
  },
  features: {
    enableAnalytics: true,
    enableReviews: true,
    enableWishlist: true,
  },
  customization: {
    theme: 'light',
    layout: 'default',
  },
}

export function useTenantTheme() {
  const [config, setConfig] = useState<TenantConfig>(defaultConfig)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTenantConfig()
  }, [])

  const fetchTenantConfig = async () => {
    try {
      // In production, this would fetch from Brain API
      // const response = await fetch('/api/brain/tenant/config')
      // const data = await response.json()
      // setConfig({ ...defaultConfig, ...data })
      
      // For now, use default config
      setConfig(defaultConfig)
    } catch (error) {
      console.error('Error fetching tenant config:', error)
      setConfig(defaultConfig)
    } finally {
      setLoading(false)
    }
  }

  return { config, loading, refetch: fetchTenantConfig }
}