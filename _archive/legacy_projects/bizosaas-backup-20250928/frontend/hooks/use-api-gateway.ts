/**
 * API Gateway Integration Hook
 * Connects dashboards to Enhanced Multi-Tenant API Gateway (Port 8080)
 */

import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'

const API_GATEWAY_BASE = 'http://localhost:8080'

// Types for API Gateway data
export interface TierConfig {
  name: string
  price: number
  allowed_services: string[]
  allowed_routes: string[]
  rate_limit: {
    requests: number
    window: number
  }
  features: string[]
  description: string
}

export interface ApiGatewayTiers {
  tiers: {
    tier_1: TierConfig
    tier_2: TierConfig  
    tier_3: TierConfig
  }
  default_tier: string
  timestamp: string
}

export interface ServiceHealth {
  status: string
  available: boolean
  circuit_state: string
  response_time?: number
  error?: string
}

export interface GatewayMetrics {
  total_requests: number
  requests_by_service: Record<string, number>
  average_response_time: number
  response_times_by_service: Record<string, number>
  status_codes: Record<string, number>
  circuit_breaker_states: Record<string, string>
  redis_available: boolean
  timestamp: string
}

export interface EnhancedMetrics extends GatewayMetrics {
  tier_metrics: Record<string, any>
  tenant_metrics: Record<string, any>
}

// Custom hooks for API Gateway data
export const useApiGatewayHealth = () => {
  return useQuery({
    queryKey: ['api-gateway', 'health'],
    queryFn: async () => {
      const response = await fetch(`${API_GATEWAY_BASE}/health`)
      if (!response.ok) throw new Error('API Gateway health check failed')
      return response.json()
    },
    refetchInterval: 10000, // Refetch every 10 seconds
  })
}

export const useApiGatewayTiers = () => {
  return useQuery({
    queryKey: ['api-gateway', 'tiers'],
    queryFn: async (): Promise<ApiGatewayTiers> => {
      const response = await fetch(`${API_GATEWAY_BASE}/gateway/tiers`)
      if (!response.ok) throw new Error('Failed to fetch tiers')
      return response.json()
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export const useApiGatewayServices = () => {
  return useQuery({
    queryKey: ['api-gateway', 'services'],
    queryFn: async (): Promise<Record<string, ServiceHealth>> => {
      const response = await fetch(`${API_GATEWAY_BASE}/health/services`)
      if (!response.ok) throw new Error('Failed to fetch service health')
      const data = await response.json()
      return data.services
    },
    refetchInterval: 15000, // Refetch every 15 seconds
  })
}

export const useApiGatewayMetrics = () => {
  return useQuery({
    queryKey: ['api-gateway', 'metrics'],
    queryFn: async (): Promise<GatewayMetrics> => {
      const response = await fetch(`${API_GATEWAY_BASE}/gateway/enhanced-metrics`)
      if (!response.ok) throw new Error('Failed to fetch metrics')
      return response.json()
    },
    refetchInterval: 30000, // Refetch every 30 seconds
  })
}

// Enhanced metrics with tenant breakdown
export const useEnhancedGatewayMetrics = () => {
  return useQuery({
    queryKey: ['api-gateway', 'enhanced-metrics'],
    queryFn: async (): Promise<EnhancedMetrics> => {
      const response = await fetch(`${API_GATEWAY_BASE}/gateway/enhanced-metrics`)
      if (!response.ok) {
        // Fallback to basic metrics if enhanced not available
        const basicResponse = await fetch(`${API_GATEWAY_BASE}/gateway/metrics`)
        if (!basicResponse.ok) throw new Error('Failed to fetch any metrics')
        return basicResponse.json()
      }
      return response.json()
    },
    refetchInterval: 30000,
  })
}

// Tenant health check
export const useTenantHealth = (tenantId: string) => {
  return useQuery({
    queryKey: ['api-gateway', 'tenant-health', tenantId],
    queryFn: async () => {
      const response = await fetch(`${API_GATEWAY_BASE}/health/tenant/${tenantId}`)
      if (!response.ok) throw new Error(`Tenant ${tenantId} health check failed`)
      return response.json()
    },
    refetchInterval: 30000,
    enabled: !!tenantId,
  })
}

// Combined dashboard data hook
export const useApiGatewayDashboard = () => {
  const { data: health, isLoading: healthLoading } = useApiGatewayHealth()
  const { data: tiers, isLoading: tiersLoading } = useApiGatewayTiers()  
  const { data: services, isLoading: servicesLoading } = useApiGatewayServices()
  const { data: metrics, isLoading: metricsLoading } = useEnhancedGatewayMetrics()

  const isLoading = healthLoading || tiersLoading || servicesLoading || metricsLoading

  // Transform data for dashboard consumption
  const dashboardData = {
    gateway: {
      status: health?.status || 'unknown',
      timestamp: health?.timestamp || new Date().toISOString()
    },
    tiers: {
      tier_1: {
        name: tiers?.tiers?.tier_1?.name || 'Static Site Tier',
        price: tiers?.tiers?.tier_1?.price || 97,
        features: tiers?.tiers?.tier_1?.features || ['static_sites', 'basic_cms'],
        clients: 0 // Will be populated from real tenant data
      },
      tier_2: {
        name: tiers?.tiers?.tier_2?.name || 'Dynamic CMS Tier',
        price: tiers?.tiers?.tier_2?.price || 297,
        features: tiers?.tiers?.tier_2?.features || ['dynamic_cms', 'ai_content'],
        clients: 0
      },
      tier_3: {
        name: tiers?.tiers?.tier_3?.name || 'Full Platform Tier',
        price: tiers?.tiers?.tier_3?.price || 997,
        features: tiers?.tiers?.tier_3?.features || ['full_cms', 'ecommerce', 'ai_agents'],
        clients: 0
      }
    },
    services: Object.entries(services || {}).map(([name, health]) => ({
      name,
      status: health.status,
      available: health.available,
      circuit_state: health.circuit_state,
      response_time: health.response_time
    })),
    metrics: {
      total_requests: metrics?.total_requests || 0,
      average_response_time: metrics?.average_response_time || 0,
      requests_by_service: metrics?.requests_by_service || {},
      circuit_breaker_states: metrics?.circuit_breaker_states || {},
      redis_available: metrics?.redis_available || false
    }
  }

  return {
    data: dashboardData,
    isLoading,
    error: null // TODO: Add proper error handling
  }
}

// Real-time updates hook using WebSocket (future implementation)
export const useApiGatewayRealtime = () => {
  const [realtimeData, setRealtimeData] = useState(null)
  const [connected, setConnected] = useState(false)

  useEffect(() => {
    // WebSocket connection to API Gateway for real-time updates
    // Implementation pending - API Gateway doesn't expose WebSocket yet
    setConnected(false)
  }, [])

  return {
    data: realtimeData,
    connected
  }
}