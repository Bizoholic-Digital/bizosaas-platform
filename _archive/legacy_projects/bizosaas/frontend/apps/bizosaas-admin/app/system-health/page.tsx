'use client'

import { useState, useEffect } from 'react'
import { 
  Server, 
  Database, 
  Cpu, 
  HardDrive, 
  Activity, 
  Wifi, 
  AlertTriangle, 
  CheckCircle, 
  XCircle,
  Clock,
  BarChart3,
  Zap,
  Globe,
  Shield,
  RotateCcw,
  Download,
  TrendingUp,
  TrendingDown
} from 'lucide-react'

interface ServiceStatus {
  name: string
  status: 'healthy' | 'warning' | 'critical' | 'down'
  uptime: string
  responseTime: number
  lastCheck: string
  version: string
  url: string
}

interface SystemMetrics {
  cpu: {
    usage: number
    cores: number
    temperature: number
  }
  memory: {
    used: number
    total: number
    percentage: number
  }
  disk: {
    used: number
    total: number
    percentage: number
  }
  network: {
    inbound: number
    outbound: number
    latency: number
  }
}

interface AlertItem {
  id: string
  type: 'error' | 'warning' | 'info'
  message: string
  timestamp: string
  service: string
  resolved: boolean
}

export default function SystemHealthPage() {
  const [services, setServices] = useState<ServiceStatus[]>([])
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null)
  const [alerts, setAlerts] = useState<AlertItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState<string>('')

  useEffect(() => {
    const fetchSystemHealth = () => {
      const mockServices: ServiceStatus[] = [
        {
          name: 'PostgreSQL Database',
          status: 'healthy',
          uptime: '99.9%',
          responseTime: 12,
          lastCheck: '30 seconds ago',
          version: '15.4',
          url: 'postgresql://localhost:5433'
        },
        {
          name: 'Redis Cache',
          status: 'healthy',
          uptime: '99.8%',
          responseTime: 3,
          lastCheck: '45 seconds ago',
          version: '7.0',
          url: 'redis://localhost:6379'
        },
        {
          name: 'FastAPI Brain Gateway',
          status: 'healthy',
          uptime: '99.5%',
          responseTime: 85,
          lastCheck: '1 minute ago',
          version: '0.104.1',
          url: 'http://localhost:8001'
        },
        {
          name: 'Wagtail CMS',
          status: 'warning',
          uptime: '98.2%',
          responseTime: 245,
          lastCheck: '2 minutes ago',
          version: '5.2',
          url: 'http://localhost:8006'
        },
        {
          name: 'Saleor E-commerce',
          status: 'healthy',
          uptime: '99.1%',
          responseTime: 156,
          lastCheck: '1 minute ago',
          version: '3.20',
          url: 'http://localhost:8003'
        },
        {
          name: 'Django CRM',
          status: 'critical',
          uptime: '95.8%',
          responseTime: 0,
          lastCheck: '5 minutes ago',
          version: '4.2',
          url: 'http://localhost:8000'
        }
      ]

      const mockMetrics: SystemMetrics = {
        cpu: {
          usage: 45.2,
          cores: 8,
          temperature: 62
        },
        memory: {
          used: 12.4,
          total: 32,
          percentage: 38.8
        },
        disk: {
          used: 145,
          total: 500,
          percentage: 29.0
        },
        network: {
          inbound: 125.4,
          outbound: 89.2,
          latency: 15
        }
      }

      const mockAlerts: AlertItem[] = [
        {
          id: 'alert-1',
          type: 'error',
          message: 'Django CRM service is not responding',
          timestamp: '5 minutes ago',
          service: 'Django CRM',
          resolved: false
        },
        {
          id: 'alert-2',
          type: 'warning',
          message: 'Wagtail CMS response time exceeding threshold (>200ms)',
          timestamp: '12 minutes ago',
          service: 'Wagtail CMS',
          resolved: false
        },
        {
          id: 'alert-3',
          type: 'info',
          message: 'System backup completed successfully',
          timestamp: '1 hour ago',
          service: 'System',
          resolved: true
        }
      ]

      setServices(mockServices)
      setMetrics(mockMetrics)
      setAlerts(mockAlerts)
      setLastUpdate(new Date().toLocaleTimeString())
      setIsLoading(false)
    }

    fetchSystemHealth()
    const interval = setInterval(fetchSystemHealth, 30000) // RotateCcw every 30 seconds

    return () => clearInterval(interval)
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-600 bg-green-100'
      case 'warning': return 'text-yellow-600 bg-yellow-100'
      case 'critical': return 'text-red-600 bg-red-100'
      case 'down': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy': return <CheckCircle className="h-4 w-4" />
      case 'warning': return <AlertTriangle className="h-4 w-4" />
      case 'critical': return <XCircle className="h-4 w-4" />
      case 'down': return <XCircle className="h-4 w-4" />
      default: return <Clock className="h-4 w-4" />
    }
  }

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'error': return <XCircle className="h-5 w-5 text-red-600" />
      case 'warning': return <AlertTriangle className="h-5 w-5 text-yellow-600" />
      case 'info': return <CheckCircle className="h-5 w-5 text-blue-600" />
      default: return <Clock className="h-5 w-5 text-gray-600" />
    }
  }

  const getMetricColor = (percentage: number, isInverted = false) => {
    if (isInverted) {
      if (percentage < 50) return 'text-green-600'
      if (percentage < 80) return 'text-yellow-600'
      return 'text-red-600'
    } else {
      if (percentage < 50) return 'text-green-600'
      if (percentage < 80) return 'text-yellow-600'
      return 'text-red-600'
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading system health...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">System Health & Infrastructure</h1>
          <p className="text-gray-600">Platform-wide infrastructure monitoring and performance metrics</p>
        </div>
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span>Last updated: {lastUpdate}</span>
          </div>
          <button className="flex items-center space-x-2 px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50">
            <RotateCcw className="h-4 w-4" />
            <span>RotateCcw</span>
          </button>
          <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
            <Download className="h-4 w-4" />
            <span>Export Report</span>
          </button>
        </div>
      </div>

      {/* System Metrics Overview */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Cpu className="h-6 w-6 text-blue-600" />
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-500">CPU Usage</p>
                  <p className="text-lg font-bold text-gray-900">{metrics.cpu.usage}%</p>
                </div>
              </div>
              {metrics.cpu.usage < 70 ? (
                <TrendingDown className="h-5 w-5 text-green-600" />
              ) : (
                <TrendingUp className="h-5 w-5 text-red-600" />
              )}
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Cores:</span>
                <span className="font-medium">{metrics.cpu.cores}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Temperature:</span>
                <span className="font-medium">{metrics.cpu.temperature}°C</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Database className="h-6 w-6 text-green-600" />
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-500">Memory Usage</p>
                  <p className="text-lg font-bold text-gray-900">{metrics.memory.percentage}%</p>
                </div>
              </div>
              <BarChart3 className="h-5 w-5 text-gray-400" />
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Used:</span>
                <span className="font-medium">{metrics.memory.used} GB</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Total:</span>
                <span className="font-medium">{metrics.memory.total} GB</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <HardDrive className="h-6 w-6 text-purple-600" />
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-500">Disk Usage</p>
                  <p className="text-lg font-bold text-gray-900">{metrics.disk.percentage}%</p>
                </div>
              </div>
              <Activity className="h-5 w-5 text-gray-400" />
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Used:</span>
                <span className="font-medium">{metrics.disk.used} GB</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Total:</span>
                <span className="font-medium">{metrics.disk.total} GB</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <Wifi className="h-6 w-6 text-yellow-600" />
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-500">Network</p>
                  <p className="text-lg font-bold text-gray-900">{metrics.network.latency}ms</p>
                </div>
              </div>
              <Globe className="h-5 w-5 text-gray-400" />
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Inbound:</span>
                <span className="font-medium">{metrics.network.inbound} MB/s</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Outbound:</span>
                <span className="font-medium">{metrics.network.outbound} MB/s</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Services Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Service Status</h3>
            <p className="text-sm text-gray-500">Real-time monitoring of critical services</p>
          </div>
          <div className="divide-y divide-gray-200">
            {services.map((service) => (
              <div key={service.name} className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="flex-shrink-0">
                      <Server className="h-6 w-6 text-gray-400" />
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <p className="text-sm font-medium text-gray-900">{service.name}</p>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(service.status)}`}>
                          {getStatusIcon(service.status)}
                          <span className="ml-1 capitalize">{service.status}</span>
                        </span>
                      </div>
                      <div className="flex items-center space-x-4 mt-1 text-xs text-gray-500">
                        <span>v{service.version}</span>
                        <span>•</span>
                        <span>Uptime: {service.uptime}</span>
                        <span>•</span>
                        <span>Response: {service.responseTime}ms</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-gray-500">{service.lastCheck}</p>
                    <a 
                      href={service.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-xs text-blue-600 hover:text-blue-800"
                    >
                      {service.url}
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Alerts */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Recent Alerts</h3>
            <p className="text-sm text-gray-500">Latest system alerts and notifications</p>
          </div>
          <div className="divide-y divide-gray-200 max-h-96 overflow-y-auto">
            {alerts.map((alert) => (
              <div key={alert.id} className={`p-4 ${alert.resolved ? 'opacity-60' : ''}`}>
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0">
                    {getAlertIcon(alert.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">{alert.message}</p>
                    <div className="flex items-center space-x-2 mt-1">
                      <span className="text-xs text-gray-500">{alert.service}</span>
                      <span className="text-xs text-gray-500">•</span>
                      <span className="text-xs text-gray-500">{alert.timestamp}</span>
                      {alert.resolved && (
                        <>
                          <span className="text-xs text-gray-500">•</span>
                          <span className="text-xs text-green-600 font-medium">Resolved</span>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <button className="flex items-center space-x-3 p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            <RotateCcw className="h-5 w-5 text-blue-600" />
            <span className="text-sm font-medium">Restart Services</span>
          </button>
          <button className="flex items-center space-x-3 p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            <Database className="h-5 w-5 text-green-600" />
            <span className="text-sm font-medium">Database Backup</span>
          </button>
          <button className="flex items-center space-x-3 p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            <Shield className="h-5 w-5 text-purple-600" />
            <span className="text-sm font-medium">Security Scan</span>
          </button>
          <button className="flex items-center space-x-3 p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            <Download className="h-5 w-5 text-gray-600" />
            <span className="text-sm font-medium">Generate Report</span>
          </button>
        </div>
      </div>
    </div>
  )
}