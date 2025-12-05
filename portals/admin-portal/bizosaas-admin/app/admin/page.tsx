'use client'

import { useState, useEffect } from 'react'
import { 
  Shield, 
  Users, 
  Building2, 
  Activity, 
  DollarSign, 
  Database, 
  Brain, 
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  Zap,
  Settings,
  BarChart3
} from 'lucide-react'

interface PlatformStats {
  totalTenants: number
  activeUsers: number
  totalRevenue: number
  systemUptime: number
  aiAgentsActive: number
  securityScore: number
  apiRequests: number
  storageUsed: number
}

interface SystemHealth {
  brain: 'healthy' | 'degraded' | 'down'
  database: 'healthy' | 'degraded' | 'down'
  cache: 'healthy' | 'degraded' | 'down'
  storage: 'healthy' | 'degraded' | 'down'
  ai_agents: 'healthy' | 'degraded' | 'down'
}

export default function AdminPage() {
  const [stats, setStats] = useState<PlatformStats | null>(null)
  const [systemHealth, setSystemHealth] = useState<SystemHealth | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        // Simulate fetching admin dashboard data
        const mockStats: PlatformStats = {
          totalTenants: 247,
          activeUsers: 8429,
          totalRevenue: 127543,
          systemUptime: 99.97,
          aiAgentsActive: 18,
          securityScore: 94,
          apiRequests: 2847693,
          storageUsed: 78.3
        }

        const mockHealth: SystemHealth = {
          brain: 'healthy',
          database: 'healthy', 
          cache: 'healthy',
          storage: 'degraded',
          ai_agents: 'healthy'
        }

        setStats(mockStats)
        setSystemHealth(mockHealth)
      } catch (error) {
        console.error('Error fetching admin data:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchAdminData()
    const interval = setInterval(fetchAdminData, 30000)
    return () => clearInterval(interval)
  }, [])

  const getHealthColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-600 bg-green-100'
      case 'degraded': return 'text-yellow-600 bg-yellow-100'
      case 'down': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getHealthIcon = (status: string) => {
    switch (status) {
      case 'healthy': return <CheckCircle className="h-4 w-4" />
      case 'degraded': return <AlertTriangle className="h-4 w-4" />
      case 'down': return <AlertTriangle className="h-4 w-4" />
      default: return <Clock className="h-4 w-4" />
    }
  }

  if (isLoading) {
    return (
      <div className="space-y-6 p-6">
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading admin dashboard...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Platform Administration</h1>
          <p className="text-gray-600">Super admin dashboard for platform-wide management and monitoring</p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-600">Live monitoring</span>
          </div>
        </div>
      </div>

      {/* Platform Overview Stats */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Building2 className="h-8 w-8 text-blue-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Total Tenants</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalTenants}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Users className="h-8 w-8 text-green-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Active Users</p>
                <p className="text-2xl font-bold text-gray-900">{stats.activeUsers.toLocaleString()}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <DollarSign className="h-8 w-8 text-green-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Total Revenue</p>
                <p className="text-2xl font-bold text-gray-900">${stats.totalRevenue.toLocaleString()}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Activity className="h-8 w-8 text-purple-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">System Uptime</p>
                <p className="text-2xl font-bold text-gray-900">{stats.systemUptime}%</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Secondary Metrics */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Brain className="h-8 w-8 text-purple-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">AI Agents Active</p>
                <p className="text-2xl font-bold text-gray-900">{stats.aiAgentsActive}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Shield className="h-8 w-8 text-green-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Security Score</p>
                <p className="text-2xl font-bold text-gray-900">{stats.securityScore}%</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <TrendingUp className="h-8 w-8 text-blue-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">API Requests</p>
                <p className="text-2xl font-bold text-gray-900">{stats.apiRequests.toLocaleString()}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <Database className="h-8 w-8 text-yellow-600" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500">Storage Used</p>
                <p className="text-2xl font-bold text-gray-900">{stats.storageUsed}%</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* System Health Status */}
      {systemHealth && (
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">System Health Status</h3>
            <p className="text-sm text-gray-500">Real-time monitoring of platform components</p>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
              <div className="text-center">
                <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-3">
                  <Brain className="h-8 w-8 text-purple-600" />
                </div>
                <h4 className="text-sm font-medium text-gray-900">Brain Hub</h4>
                <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium mt-2 ${getHealthColor(systemHealth.brain)}`}>
                  {getHealthIcon(systemHealth.brain)}
                  <span className="ml-1 capitalize">{systemHealth.brain}</span>
                </div>
              </div>

              <div className="text-center">
                <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-3">
                  <Database className="h-8 w-8 text-blue-600" />
                </div>
                <h4 className="text-sm font-medium text-gray-900">Database</h4>
                <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium mt-2 ${getHealthColor(systemHealth.database)}`}>
                  {getHealthIcon(systemHealth.database)}
                  <span className="ml-1 capitalize">{systemHealth.database}</span>
                </div>
              </div>

              <div className="text-center">
                <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-3">
                  <Zap className="h-8 w-8 text-yellow-600" />
                </div>
                <h4 className="text-sm font-medium text-gray-900">Cache</h4>
                <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium mt-2 ${getHealthColor(systemHealth.cache)}`}>
                  {getHealthIcon(systemHealth.cache)}
                  <span className="ml-1 capitalize">{systemHealth.cache}</span>
                </div>
              </div>

              <div className="text-center">
                <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-3">
                  <Database className="h-8 w-8 text-green-600" />
                </div>
                <h4 className="text-sm font-medium text-gray-900">Storage</h4>
                <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium mt-2 ${getHealthColor(systemHealth.storage)}`}>
                  {getHealthIcon(systemHealth.storage)}
                  <span className="ml-1 capitalize">{systemHealth.storage}</span>
                </div>
              </div>

              <div className="text-center">
                <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-3">
                  <Brain className="h-8 w-8 text-purple-600" />
                </div>
                <h4 className="text-sm font-medium text-gray-900">AI Agents</h4>
                <div className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium mt-2 ${getHealthColor(systemHealth.ai_agents)}`}>
                  {getHealthIcon(systemHealth.ai_agents)}
                  <span className="ml-1 capitalize">{systemHealth.ai_agents}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Admin Quick Actions</h3>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <button className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <Building2 className="h-6 w-6 text-blue-600 mb-2" />
              <h4 className="text-sm font-medium text-gray-900">Manage Tenants</h4>
              <p className="text-xs text-gray-500">View and manage all tenant organizations</p>
            </button>

            <button className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <Users className="h-6 w-6 text-green-600 mb-2" />
              <h4 className="text-sm font-medium text-gray-900">User Management</h4>
              <p className="text-xs text-gray-500">Manage platform users and permissions</p>
            </button>

            <button className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <BarChart3 className="h-6 w-6 text-purple-600 mb-2" />
              <h4 className="text-sm font-medium text-gray-900">Analytics</h4>
              <p className="text-xs text-gray-500">View platform analytics and insights</p>
            </button>

            <button className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <Settings className="h-6 w-6 text-gray-600 mb-2" />
              <h4 className="text-sm font-medium text-gray-900">System Settings</h4>
              <p className="text-xs text-gray-500">Configure platform settings</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}