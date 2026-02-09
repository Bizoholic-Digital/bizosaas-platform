'use client'

import { useSession } from 'next-auth/react'

export interface Tenant {
    id: string
    name: string
    slug: string
    subscription_tier: 'free' | 'starter' | 'professional' | 'enterprise'
    features: string[]
}

export function useTenant() {
    const { data: session, status } = useSession()

    // Mock tenant data for now, or extract from session if available
    const tenant: Tenant | null = session ? {
        id: (session as any)?.tenant || 'default',
        name: 'Default Tenant',
        slug: 'default',
        subscription_tier: 'enterprise', // Default to enterprise to unlock features
        features: ['*']
    } : null

    return {
        tenant,
        isLoading: status === 'loading'
    }
}
