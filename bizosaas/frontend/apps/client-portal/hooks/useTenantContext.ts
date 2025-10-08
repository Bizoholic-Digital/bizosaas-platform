import { useState, useEffect, createContext, useContext } from 'react'

interface TenantData {
  tenant_id: string
  tenant_name: string
  industry: string
  metrics: {
    total_leads: number
    revenue: number
    orders: number
    growth: number
    [key: string]: number
  }
  features: string[]
  recent_activity: Array<{
    type: string
    message: string
    time: string
  }>
  ai_insights: string[]
  source?: string
}

interface TenantContextType {
  currentTenant: string
  tenantData: TenantData | null
  loading: boolean
  error: string | null
  switchTenant: (tenantId: string) => void
  refreshData: () => void
}

const TenantContext = createContext<TenantContextType | undefined>(undefined)

export const useTenantContext = () => {
  const context = useContext(TenantContext)
  if (!context) {
    throw new Error('useTenantContext must be used within a TenantProvider')
  }
  return context
}

export const useTenantData = (tenantId?: string) => {
  const [tenantData, setTenantData] = useState<TenantData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const currentTenant = tenantId || 'demo'

  const fetchTenantData = async () => {
    try {
      setLoading(true)
      setError(null)

      const response = await fetch(`/api/brain/tenant/dashboard?tenant=${currentTenant}`)

      if (!response.ok) {
        throw new Error(`Failed to fetch tenant data: ${response.status}`)
      }

      const data = await response.json()
      setTenantData(data)
    } catch (err) {
      console.error('Error fetching tenant data:', err)
      setError(err instanceof Error ? err.message : 'Failed to fetch tenant data')

      // Set fallback data on error
      setTenantData({
        tenant_id: currentTenant,
        tenant_name: 'Demo Client',
        industry: 'General',
        metrics: {
          total_leads: 0,
          revenue: 0,
          orders: 0,
          growth: 0
        },
        features: ['dashboard'],
        recent_activity: [],
        ai_insights: ['Unable to load AI insights at this time'],
        source: 'error_fallback'
      })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTenantData()
  }, [currentTenant])

  const refreshData = () => {
    fetchTenantData()
  }

  return {
    tenantData,
    loading,
    error,
    refreshData,
    currentTenant
  }
}