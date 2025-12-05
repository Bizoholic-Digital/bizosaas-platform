'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { ThemeProvider as NextThemeProvider } from 'next-themes';
import { TenantConfig, TenantType, TENANT_CONFIGS } from '../../types';

interface TenantThemeContextType {
  tenant: TenantType;
  config: TenantConfig;
  switchTenant: (tenant: TenantType) => void;
}

const TenantThemeContext = createContext<TenantThemeContextType | undefined>(undefined);

interface TenantThemeProviderProps {
  children: React.ReactNode;
  defaultTenant: TenantType;
  customConfig?: Partial<TenantConfig>;
}

export function TenantThemeProvider({ 
  children, 
  defaultTenant,
  customConfig 
}: TenantThemeProviderProps) {
  const [tenant, setTenant] = useState<TenantType>(defaultTenant);
  const [config, setConfig] = useState<TenantConfig>(() => ({
    ...TENANT_CONFIGS[defaultTenant],
    ...customConfig
  }));

  const switchTenant = (newTenant: TenantType) => {
    setTenant(newTenant);
    setConfig({
      ...TENANT_CONFIGS[newTenant],
      ...customConfig
    });
  };

  // Apply tenant-specific CSS custom properties
  useEffect(() => {
    const root = document.documentElement;
    const theme = config.theme;
    
    // Set CSS custom properties for the tenant theme
    root.style.setProperty('--tenant-primary', theme.primaryColor);
    root.style.setProperty('--tenant-secondary', theme.secondaryColor);
    root.style.setProperty('--tenant-accent', theme.accentColor);
    root.style.setProperty('--tenant-background', theme.backgroundColor);
    root.style.setProperty('--tenant-text', theme.textColor);
    
    // Set Tailwind CSS variables for consistent theming
    root.style.setProperty('--primary-50', generateColorShade(theme.primaryColor, 50));
    root.style.setProperty('--primary-100', generateColorShade(theme.primaryColor, 100));
    root.style.setProperty('--primary-200', generateColorShade(theme.primaryColor, 200));
    root.style.setProperty('--primary-300', generateColorShade(theme.primaryColor, 300));
    root.style.setProperty('--primary-400', generateColorShade(theme.primaryColor, 400));
    root.style.setProperty('--primary-500', theme.primaryColor);
    root.style.setProperty('--primary-600', generateColorShade(theme.primaryColor, 600));
    root.style.setProperty('--primary-700', generateColorShade(theme.primaryColor, 700));
    root.style.setProperty('--primary-800', generateColorShade(theme.primaryColor, 800));
    root.style.setProperty('--primary-900', generateColorShade(theme.primaryColor, 900));

    // Apply custom CSS if provided
    if (theme.customCSS) {
      const styleElement = document.getElementById('tenant-custom-css') || document.createElement('style');
      styleElement.id = 'tenant-custom-css';
      styleElement.textContent = theme.customCSS;
      if (!document.getElementById('tenant-custom-css')) {
        document.head.appendChild(styleElement);
      }
    }

    // Set document title and favicon
    document.title = config.branding.companyName;
    
    const favicon = document.querySelector<HTMLLinkElement>('link[rel="icon"]');
    if (favicon) {
      favicon.href = config.branding.favicon;
    }
  }, [config]);

  return (
    <TenantThemeContext.Provider value={{ tenant, config, switchTenant }}>
      <NextThemeProvider
        attribute="class"
        defaultTheme={config.theme.darkMode ? 'dark' : 'light'}
        enableSystem
        disableTransitionOnChange
      >
        <div className={`tenant-${tenant}`} data-tenant={tenant}>
          {children}
        </div>
      </NextThemeProvider>
    </TenantThemeContext.Provider>
  );
}

export function useTenantTheme() {
  const context = useContext(TenantThemeContext);
  if (context === undefined) {
    throw new Error('useTenantTheme must be used within a TenantThemeProvider');
  }
  return context;
}

// Helper function to generate color shades (simplified version)
function generateColorShade(baseColor: string, shade: number): string {
  // This is a simplified version - in production, you'd want a more robust color manipulation library
  const hex = baseColor.replace('#', '');
  const num = parseInt(hex, 16);
  const r = (num >> 16) & 255;
  const g = (num >> 8) & 255;
  const b = num & 255;
  
  const factor = shade < 500 ? (500 - shade) / 500 : -(shade - 500) / 500;
  const newR = Math.round(r + (255 - r) * Math.max(0, factor));
  const newG = Math.round(g + (255 - g) * Math.max(0, factor));
  const newB = Math.round(b + (255 - b) * Math.max(0, factor));
  
  return `rgb(${newR}, ${newG}, ${newB})`;
}