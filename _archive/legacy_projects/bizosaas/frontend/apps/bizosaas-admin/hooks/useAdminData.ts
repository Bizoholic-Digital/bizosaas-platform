import { useState, useEffect } from 'react'

interface AdminMetrics {
  totalTenants: number
  totalUsers: number
  monthlyRevenue: number
  systemHealth: number
  growth: {
    tenants: number
    users: number
    revenue: number
    health: number
  }
}

interface Activity {
  id: number
  type: string
  message: string
  timestamp: string
  status: string
  platform: string
}

interface SystemStats {
  cpuUsage: number
  memoryUsage: number
  diskUsage: number
  apiRequestsPerMin: number
  activeSessions: number
  databaseConnections: number
  maxDbConnections: number
}

interface PlatformStats {
  [key: string]: {
    active: boolean
    status: string
    [key: string]: any
  }
}

interface AdminDashboardData {
  metrics: AdminMetrics
  recentActivities: Activity[]
  systemStats: SystemStats
  platformStats: PlatformStats
}

interface AdminAPIResponse {
  success: boolean
  source: string
  data: AdminDashboardData
  meta?: any
}

export const useAdminDashboard = () => {
  const [data, setData] = useState<AdminDashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [source, setSource] = useState<string>('unknown')

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch('api/brain/unified/dashboard')
        const result: AdminAPIResponse = await response.json()

        if (result.success) {
          setData(result.data)
          setSource(result.source)
        } else {
          setError('Failed to fetch dashboard data')
        }

      } catch (err) {
        console.error('[ADMIN] Error fetching dashboard data:', err)
        setError('Network error fetching dashboard data')
      } finally {
        setLoading(false)
      }
    }

    fetchDashboardData()
    
    // Refresh every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000)
    return () => clearInterval(interval)
  }, [])

  return { data, loading, error, source }
}

export const usePlatformAnalytics = (platform = 'all') => {
  const [platforms, setPlatforms] = useState<any>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [source, setSource] = useState<string>('unknown')

  useEffect(() => {
    const fetchPlatformData = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch(`/api/brain/unified/platforms?platform=${platform}`)
        const result = await response.json()

        if (result.success) {
          setPlatforms(result.data)
          setSource(result.source)
        } else {
          setError('Failed to fetch platform analytics')
        }

      } catch (err) {
        console.error('[ADMIN] Error fetching platform analytics:', err)
        setError('Network error fetching platform analytics')
      } finally {
        setLoading(false)
      }
    }

    fetchPlatformData()
    
    // Refresh every 60 seconds for platform data
    const interval = setInterval(fetchPlatformData, 60000)
    return () => clearInterval(interval)
  }, [platform])

  return { platforms, loading, error, source }
}

export const useSystemHealth = () => {
  const { data, loading, error } = useAdminDashboard()
  
  const healthMetrics = data ? {
    overall: data.metrics.systemHealth,
    cpu: data.systemStats.cpuUsage,
    memory: data.systemStats.memoryUsage,
    disk: data.systemStats.diskUsage,
    activeSessions: data.systemStats.activeSessions,
    apiLoad: data.systemStats.apiRequestsPerMin,
    dbConnections: data.systemStats.databaseConnections,
    maxDbConnections: data.systemStats.maxDbConnections
  } : null

  return { healthMetrics, loading, error }
}

export const useRecentActivities = (limit = 10) => {
  const { data, loading, error } = useAdminDashboard()
  
  const activities = data?.recentActivities?.slice(0, limit) || []
  
  return { activities, loading, error }
}
