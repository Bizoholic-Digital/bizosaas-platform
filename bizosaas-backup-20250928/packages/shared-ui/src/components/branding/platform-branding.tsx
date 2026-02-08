'use client';

import React from 'react';
import { PLATFORM_BRANDS, type PlatformBrand } from '../../lib/constants/branding';

interface PlatformBrandingProps {
  platform: PlatformBrand;
  variant?: 'full' | 'logo' | 'text';
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
}

export function PlatformBranding({ 
  platform, 
  variant = 'full', 
  size = 'md', 
  className = '' 
}: PlatformBrandingProps) {
  const brandConfig = PLATFORM_BRANDS[platform];
  
  const sizeClasses = {
    sm: 'h-6',
    md: 'h-8',
    lg: 'h-12',
    xl: 'h-16'
  };

  const textSizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-xl',
    xl: 'text-3xl'
  };

  const taglineSizeClasses = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base',
    xl: 'text-lg'
  };

  if (variant === 'logo') {
    return (
      <img
        src={brandConfig.logoPath}
        alt={`${brandConfig.name} Logo`}
        className={`${sizeClasses[size]} w-auto ${className}`}
        style={{ filter: `hue-rotate(${brandConfig.primaryColor})` }}
      />
    );
  }

  if (variant === 'text') {
    return (
      <span
        className={`font-bold ${textSizeClasses[size]} ${className}`}
        style={{ color: brandConfig.primaryColor }}
      >
        {brandConfig.name}
      </span>
    );
  }

  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      <img
        src={brandConfig.logoPath}
        alt={`${brandConfig.name} Logo`}
        className={`${sizeClasses[size]} w-auto`}
        style={{ filter: `hue-rotate(${brandConfig.primaryColor})` }}
      />
      <div className="flex flex-col">
        <span
          className={`font-bold ${textSizeClasses[size]}`}
          style={{ color: brandConfig.primaryColor }}
        >
          {brandConfig.name}
        </span>
        <span
          className={`${taglineSizeClasses[size]} opacity-75`}
          style={{ color: brandConfig.secondaryColor }}
        >
          {brandConfig.tagline}
        </span>
      </div>
    </div>
  );
}

interface PlatformThemeProviderProps {
  platform: PlatformBrand;
  children: React.ReactNode;
}

export function PlatformThemeProvider({ platform, children }: PlatformThemeProviderProps) {
  const brandConfig = PLATFORM_BRANDS[platform];

  React.useEffect(() => {
    const root = document.documentElement;
    root.style.setProperty('--primary-color', brandConfig.primaryColor);
    root.style.setProperty('--secondary-color', brandConfig.secondaryColor);
    root.style.setProperty('--accent-color', brandConfig.accentColor);
    
    // Update favicon
    const favicon = document.querySelector('link[rel=\"icon\"]') as HTMLLinkElement;
    if (favicon) {
      favicon.href = brandConfig.faviconPath;
    }
    
    // Update page title prefix
    const title = document.title;
    if (!title.startsWith(brandConfig.name)) {
      document.title = `${brandConfig.name} - ${title}`;
    }
  }, [platform]);

  return <>{children}</>;
}