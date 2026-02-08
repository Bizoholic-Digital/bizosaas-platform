'use client'

import React, { createContext, useContext } from 'react'
import { getPlatformConfig, getCurrentPlatform, type Platform } from '@/lib/platform'

interface TenantThemeContextType {
  platform: Platform
  config: ReturnType<typeof getPlatformConfig>
}

const TenantThemeContext = createContext<TenantThemeContextType | undefined>(undefined)

interface TenantThemeProviderProps {
  children: React.ReactNode
  defaultTenant?: Platform
}

export function TenantThemeProvider({ children, defaultTenant = 'bizosaas' }: TenantThemeProviderProps) {
  const platform = getCurrentPlatform() || defaultTenant
  const config = getPlatformConfig(platform)

  React.useEffect(() => {
    // Apply platform class to body
    document.body.className = document.body.className.replace(/platform-\w+/g, '')
    document.body.classList.add(config.className)
  }, [config.className])

  return (
    <TenantThemeContext.Provider value={{ platform, config }}>
      {children}
    </TenantThemeContext.Provider>
  )
}

export function useTenantTheme() {
  const context = useContext(TenantThemeContext)
  if (context === undefined) {
    throw new Error('useTenantTheme must be used within a TenantThemeProvider')
  }
  return context
}