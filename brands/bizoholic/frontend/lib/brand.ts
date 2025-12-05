'use client'

/**
 * Brand Detection and Configuration
 * Supports: Bizoholic, Coreldove, Thrillring
 */

export type Brand = 'bizoholic' | 'coreldove' | 'thrillring'

export interface BrandConfig {
  name: string
  logo: string
  primaryColor: string
  description: string
  tagline: string
  dashboardType: 'marketing' | 'ecommerce' | 'gaming'
  className: string
}

export function getCurrentBrand(): Brand {
  // Server-side: use environment variable
  if (typeof window === 'undefined') {
    const envBrand = process.env.NEXT_PUBLIC_BRAND as Brand
    return envBrand || 'bizoholic'
  }
  
  // Client-side: detect from hostname and port
  const hostname = window.location.hostname
  const port = window.location.port
  
  // Port-based detection (development)
  if (port === '3001') return 'bizoholic'
  if (port === '3002') return 'coreldove'
  if (port === '3003') return 'thrillring'
  
  // Hostname-based detection (production)
  if (hostname.includes('bizoholic')) return 'bizoholic'
  if (hostname.includes('coreldove')) return 'coreldove'
  if (hostname.includes('thrillring')) return 'thrillring'
  
  // Environment variable fallback
  const envBrand = process.env.NEXT_PUBLIC_BRAND as Brand
  return envBrand || 'bizoholic'
}

export function getBrandConfig(brand: Brand): BrandConfig {
  const configs: Record<Brand, BrandConfig> = {
    bizoholic: {
      name: 'Bizoholic Digital',
      logo: '/bizoholic-logo-hq.png',
      primaryColor: '#2563eb',
      description: 'AI-Powered Marketing Platform',
      tagline: 'Access your AI-powered marketing platform with 28+ autonomous agents',
      dashboardType: 'marketing',
      className: 'brand-bizoholic'
    },
    coreldove: {
      name: 'Coreldove Digital',
      logo: '/coreldove-logo.png',
      primaryColor: '#10b981',
      description: 'E-commerce Excellence',
      tagline: 'Manage your online store with powerful e-commerce tools',
      dashboardType: 'ecommerce',
      className: 'brand-coreldove'
    },
    thrillring: {
      name: 'Thrillring Gaming',
      logo: '/thrillring-logo.png',
      primaryColor: '#f59e0b',
      description: 'Gaming Platform',
      tagline: 'Your ultimate gaming and entertainment hub',
      dashboardType: 'gaming',
      className: 'brand-thrillring'
    }
  }
  
  return configs[brand]
}

export function useBrand() {
  const brand = getCurrentBrand()
  const config = getBrandConfig(brand)
  
  return { brand, config }
}
