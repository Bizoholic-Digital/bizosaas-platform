'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Badge } from '../ui/badge'
import { Activity, AlertCircle, CheckCircle2, XCircle, Clock } from 'lucide-react'

interface ServiceStatus {
  name: string
  endpoint: string
  status: 'healthy' | 'unhealthy' | 'unknown' | 'checking'
  port: number
  responseTime?: number
  lastChecked?: string
  error?: string
  details?: any
}

const SERVICES: Omit<ServiceStatus, 'status' | 'responseTime' | 'lastChecked'>[] = [
  { name: 'Central Hub', endpoint: 'http://localhost:8001/health', port: 8001 },
  { name: 'Amazon Sourcing', endpoint: 'http://localhost:8085/health', port: 8085 },
  { name: 'Vault', endpoint: 'http://localhost:8200/v1/sys/health', port: 8200 },
  { name: 'Wagtail CMS', endpoint: 'http://localhost:8006/health', port: 8006 },
  { name: 'Django CRM', endpoint: 'http://localhost:8003/health', port: 8003 },
  { name: 'Saleor API', endpoint: 'http://localhost:8000/health/', port: 8000 },
  { name: 'AI Agents', endpoint: 'http://localhost:8010/health', port: 8010 },
  { name: 'Auth Service', endpoint: 'http://localhost:8007/health', port: 8007 },
  { name: 'Business Directory', endpoint: 'http://localhost:9002/health', port: 9002 },
]

export default function ServiceHealthMonitor() {
  const [services, setServices] = useState<ServiceStatus[]>(
    SERVICES.map(s => ({ ...s, status: 'checking' as const }))
  )
  const [isRefreshing, setIsRefreshing] = useState(false)

  const checkServiceHealth = async (service: typeof SERVICES[0]): Promise<ServiceStatus> => {
    const startTime = Date.now()

    try {
      const response = await fetch(service.endpoint, {
        method: 'GET',
        signal: AbortSignal.timeout(5000),
        headers: {
          'Accept': 'application/json',
        },
      })

      const responseTime = Date.now() - startTime

      if (response.ok) {
        let details
        try {
          details = await response.json()
        } catch {
          // Response might not be JSON
        }

        return {
          ...service,
          status: 'healthy',
          responseTime,
          lastChecked: new Date().toISOString(),
          details,
        }
      } else {
        return {
          ...service,
          status: 'unhealthy',
          responseTime,
          lastChecked: new Date().toISOString(),
          error: `HTTP ${response.status}`,
        }
      }
    } catch (error) {
      return {
        ...service,
        status: 'unhealthy',
        responseTime: Date.now() - startTime,
        lastChecked: new Date().toISOString(),
        error: error instanceof Error ? error.message : 'Connection failed',
      }
    }
  }

  const checkAllServices = async () => {
    setIsRefreshing(true)
    setServices(prev => prev.map(s => ({ ...s, status: 'checking' as const })))

    const results = await Promise.all(
      SERVICES.map(service => checkServiceHealth(service))
    )

    setServices(results)
    setIsRefreshing(false)
  }

  useEffect(() => {
    checkAllServices()

    // Refresh every 30 seconds
    const interval = setInterval(checkAllServices, 30000)
    return () => clearInterval(interval)
  }, [])

  const getStatusIcon = (status: ServiceStatus['status']) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle2 className="h-5 w-5 text-green-600" />
      case 'unhealthy':
        return <XCircle className="h-5 w-5 text-red-600" />
      case 'checking':
        return <Clock className="h-5 w-5 text-blue-600 animate-spin" />
      default:
        return <AlertCircle className="h-5 w-5 text-gray-400" />
    }
  }

  const getStatusBadge = (status: ServiceStatus['status']) => {
    switch (status) {
      case 'healthy':
        return <Badge className="bg-green-100 text-green-800 hover:bg-green-100">Healthy</Badge>
      case 'unhealthy':
        return <Badge className="bg-red-100 text-red-800 hover:bg-red-100">Unhealthy</Badge>
      case 'checking':
        return <Badge className="bg-blue-100 text-blue-800 hover:bg-blue-100">Checking...</Badge>
      default:
        return <Badge className="bg-gray-100 text-gray-800 hover:bg-gray-100">Unknown</Badge>
    }
  }

  const healthyCount = services.filter(s => s.status === 'healthy').length
  const unhealthyCount = services.filter(s => s.status === 'unhealthy').length
  const totalCount = services.length

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Services</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalCount}</div>
            <p className="text-xs text-muted-foreground">Backend services</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Healthy</CardTitle>
            <CheckCircle2 className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{healthyCount}</div>
            <p className="text-xs text-muted-foreground">
              {((healthyCount / totalCount) * 100).toFixed(0)}% operational
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Issues</CardTitle>
            <AlertCircle className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{unhealthyCount}</div>
            <p className="text-xs text-muted-foreground">
              {unhealthyCount > 0 ? 'Attention required' : 'No issues detected'}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Service Status List */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Service Health Status</CardTitle>
              <CardDescription>Real-time backend service monitoring</CardDescription>
            </div>
            <button
              onClick={checkAllServices}
              disabled={isRefreshing}
              className="px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-700 disabled:text-gray-400 disabled:cursor-not-allowed"
            >
              {isRefreshing ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {services.map((service) => (
              <div
                key={service.name}
                className="flex items-center justify-between border-b pb-4 last:border-0 last:pb-0"
              >
                <div className="flex items-center space-x-4">
                  {getStatusIcon(service.status)}
                  <div>
                    <p className="text-sm font-medium">{service.name}</p>
                    <p className="text-xs text-muted-foreground">Port {service.port}</p>
                  </div>
                </div>

                <div className="flex items-center space-x-4">
                  {service.responseTime !== undefined && (
                    <p className="text-xs text-muted-foreground">
                      {service.responseTime}ms
                    </p>
                  )}
                  {getStatusBadge(service.status)}
                </div>

                {service.error && (
                  <div className="mt-2 text-xs text-red-600">
                    Error: {service.error}
                  </div>
                )}
              </div>
            ))}
          </div>

          {services.length === 0 && (
            <p className="text-center text-sm text-muted-foreground py-8">
              No services configured
            </p>
          )}

          <div className="mt-4 pt-4 border-t">
            <p className="text-xs text-muted-foreground">
              Last updated: {new Date().toLocaleTimeString()} • Auto-refresh every 30 seconds
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
