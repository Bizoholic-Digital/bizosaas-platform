'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { brainApi } from '@/lib/brain-api';

interface BrandingConfig {
    portal_title: string;
    logo_url: string;
    favicon_url: string;
    primary_color: string;
    secondary_color: string;
    font_family: string;
}

interface BrandingContextType {
    config: BrandingConfig;
    isLoading: boolean;
}

const BrandingContext = createContext<BrandingContextType | undefined>(undefined);

export function BrandingProvider({ children }: { children: React.ReactNode }) {
    const [config, setConfig] = useState<BrandingConfig>({
        portal_title: 'BizOSaaS Platform',
        logo_url: '',
        favicon_url: '',
        primary_color: '#2563eb',
        secondary_color: '#475569',
        font_family: 'Inter'
    });
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function loadBranding() {
            try {
                // For Admin, we use the private admin config endpoint
                const data = await brainApi.admin.getTenantConfig();
                if (data) {
                    setConfig({
                        portal_title: data.portal_title || 'BizOSaaS Platform',
                        logo_url: data.logo_url || '',
                        favicon_url: data.favicon_url || '',
                        primary_color: data.primary_color || '#2563eb',
                        secondary_color: data.secondary_color || '#475569',
                        font_family: data.font_family || 'Inter'
                    });
                }
            } catch (error) {
                console.error("Failed to load branding in Admin Provider", error);
            } finally {
                setIsLoading(false);
            }
        }
        loadBranding();
    }, []);

    return (
        <BrandingContext.Provider value={{ config, isLoading }}>
            {children}
        </BrandingContext.Provider>
    );
}

export function useBranding() {
    const context = useContext(BrandingContext);
    if (context === undefined) {
        throw new Error('useBranding must be used within a BrandingProvider');
    }
    return context;
}
