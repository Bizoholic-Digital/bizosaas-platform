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
    companyName: 'CorelDove',
    logo: '/images/Coreldove-Simple-transparent.png',
    primaryColor: '#ef4444', // red-500
    secondaryColor: '#2563eb', // blue-600
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
      setLoading(true)
      // In production, this would fetch from Brain API
      // const response = await fetch('/api/brain/tenant/config')
      // const data = await response.json()
      // setConfig({ ...defaultConfig, ...data })
      
      // Simulate quick config load with timeout
      await new Promise(resolve => setTimeout(resolve, 100))
      
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