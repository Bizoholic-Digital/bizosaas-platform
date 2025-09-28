'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface BrandConfig {
  name: string;
  logo: string;
  primaryColor: string;
  secondaryColor: string;
  theme: 'light' | 'dark';
}

interface BrandContextType {
  currentBrand: BrandConfig;
  setBrand: (brand: BrandConfig) => void;
  brands: BrandConfig[];
}

const defaultBrand: BrandConfig = {
  name: 'BizOSaaS',
  logo: '/logos/bizosaas-logo.svg',
  primaryColor: '#3b82f6',
  secondaryColor: '#1e40af',
  theme: 'light'
};

const BrandContext = createContext<BrandContextType | undefined>(undefined);

interface BrandProviderProps {
  children: ReactNode;
  initialBrand?: BrandConfig;
}

export function BrandProvider({ children, initialBrand = defaultBrand }: BrandProviderProps) {
  const [currentBrand, setCurrentBrand] = useState<BrandConfig>(initialBrand);
  
  const brands: BrandConfig[] = [
    defaultBrand,
    {
      name: 'Bizoholic',
      logo: '/logos/bizoholic-logo.svg',
      primaryColor: '#059669',
      secondaryColor: '#047857',
      theme: 'light'
    },
    {
      name: 'CoreLDove',
      logo: '/logos/coreldove-logo.svg',
      primaryColor: '#dc2626',
      secondaryColor: '#b91c1c',
      theme: 'light'
    }
  ];

  const setBrand = (brand: BrandConfig) => {
    setCurrentBrand(brand);
    // Apply CSS variables for theming
    const root = document.documentElement;
    root.style.setProperty('--brand-primary', brand.primaryColor);
    root.style.setProperty('--brand-secondary', brand.secondaryColor);
  };

  return (
    <BrandContext.Provider value={{ currentBrand, setBrand, brands }}>
      {children}
    </BrandContext.Provider>
  );
}

export function useBrand() {
  const context = useContext(BrandContext);
  if (context === undefined) {
    throw new Error('useBrand must be used within a BrandProvider');
  }
  return context;
}