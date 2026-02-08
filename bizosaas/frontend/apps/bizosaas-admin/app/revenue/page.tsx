'use client'

import { useState, useEffect } from 'react'
import { 
  DollarSign, 
  TrendingUp, 
  Users, 
  Building2, 
  CreditCard, 
  Calendar,
  BarChart3,
  PieChart,
  ArrowUpRight,
  ArrowDownRight,
  Filter,
  Download,
  Eye,
  MoreHorizontal
} from 'lucide-react'

interface TenantMetrics {
  id: string
  name: string
  plan: 'starter' | 'professional' | 'enterprise'
  monthlyRevenue: number
  totalRevenue: number
  lastPayment: string
  status: 'active' | 'trial' | 'cancelled' | 'past_due'
  userCount: number
  growth: number
  churnRisk: 'low' | 'medium' | 'high'
}

interface PlatformMetrics {
  totalRevenue: number
  monthlyRecurring: number
  totalTenants: number
  activeTenants: number
  churnRate: number
  averageRevenuePerUser: number
  growthRate: number
  conversionRate: number
}

export default function MultiTenantAnalyticsPage() {
  const [tenants, setTenants] = useState<TenantMetrics[]>([])
  const [platformMetrics, setPlatformMetrics] = useState<PlatformMetrics | null>(null)
  const [selectedPeriod, setSelectedPeriod] = useState('30d')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Simulate fetching analytics data
    const fetchAnalytics = () => {
      const mockTenants: TenantMetrics[] = [
        {
          id: 'tenant-1',
          name: 'TechCorp Solutions',
          plan: 'enterprise',
          monthlyRevenue: 2500,
          totalRevenue: 45000,
          lastPayment: '2025-09-15',
          status: 'active',
          userCount: 85,
          growth: 15.2,
          churnRisk: 'low'
        },
        {
          id: 'tenant-2', 
          name: 'Digital Marketing Pro',
          plan: 'professional',
          monthlyRevenue: 899,
          totalRevenue: 12487,
          lastPayment: '2025-09-18',
          status: 'active',
          userCount: 23,
          growth: 8.7,
          churnRisk: 'low'
        },
        {
          id: 'tenant-3',
          name: 'StartupHub Inc',
          plan: 'starter',
          monthlyRevenue: 299,
          totalRevenue: 1795,
          lastPayment: '2025-09-10',
          status: 'trial',
          userCount: 8,
          growth: 32.1,
          churnRisk: 'medium'
        },
        {
          id: 'tenant-4',
          name: 'Enterprise Global',
          plan: 'enterprise',
          monthlyRevenue: 4999,
          totalRevenue: 89982,
          lastPayment: '2025-09-20',
          status: 'active',
          userCount: 156,
          growth: 5.3,
          churnRisk: 'low'
        },
        {
          id: 'tenant-5',
          name: 'Local Business Co',
          plan: 'professional',
          monthlyRevenue: 899,
          totalRevenue: 8091,
          lastPayment: '2025-08-15',
          status: 'past_due',
          userCount: 19,
          growth: -12.4,
          churnRisk: 'high'
        }
      ]

      const mockPlatformMetrics: PlatformMetrics = {
        totalRevenue: 156163,
        monthlyRecurring: 9596,
        totalTenants: 47,
        activeTenants: 43,
        churnRate: 2.3,
        averageRevenuePerUser: 204.32,
        growthRate: 12.7,
        conversionRate: 68.5
      }

      setTenants(mockTenants)
      setPlatformMetrics(mockPlatformMetrics)
      setIsLoading(false)
    }

    fetchAnalytics()
    const interval = setInterval(fetchAnalytics, 60000) // Refresh every minute

    return () => clearInterval(interval)
  }, [selectedPeriod])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100'
      case 'trial': return 'text-blue-600 bg-blue-100'
      case 'cancelled': return 'text-gray-600 bg-gray-100'
      case 'past_due': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getPlanColor = (plan: string) => {
    switch (plan) {
      case 'starter': return 'text-blue-600 bg-blue-100'
      case 'professional': return 'text-purple-600 bg-purple-100'
      case 'enterprise': return 'text-gold-600 bg-yellow-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getChurnRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'text-green-600'
      case 'medium': return 'text-yellow-600'
      case 'high': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading analytics...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Multi-Tenant Revenue Analytics</h1>
          <p className="text-gray-600">Cross-tenant performance metrics and financial insights</p>
        </div>
        <div className="flex items-center space-x-3">
          <select
            value={selectedPeriod}
            onChange={(e) => setSelectedPeriod(e.target.value)}
            className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
            <option value="1y">Last year</option>
          </select>
          <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">
            <Download className="h-4 w-4" />
            <span>Export</span>
          </button>
        </div>
      </div>

      {/* Platform Overview Metrics */}
      {platformMetrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Total Revenue</p>
                <p className="text-2xl font-bold text-gray-900">${platformMetrics.totalRevenue.toLocaleString()}</p>
                <div className="flex items-center mt-1">
                  <ArrowUpRight className="h-4 w-4 text-green-600" />
                  <span className="text-sm text-green-600 font-medium">{platformMetrics.growthRate}%</span>
                </div>
              </div>
              <div className="p-3 bg-green-100 rounded-full">
                <DollarSign className="h-6 w-6 text-green-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Monthly Recurring</p>
                <p className="text-2xl font-bold text-gray-900">${platformMetrics.monthlyRecurring.toLocaleString()}</p>
                <div className="flex items-center mt-1">
                  <ArrowUpRight className="h-4 w-4 text-green-600" />
                  <span className="text-sm text-green-600 font-medium">+{platformMetrics.growthRate}%</span>
                </div>
              </div>
              <div className="p-3 bg-blue-100 rounded-full">
                <TrendingUp className="h-6 w-6 text-blue-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Active Tenants</p>
                <p className="text-2xl font-bold text-gray-900">{platformMetrics.activeTenants}/{platformMetrics.totalTenants}</p>
                <div className="flex items-center mt-1">
                  <span className="text-sm text-gray-600">{((platformMetrics.activeTenants/platformMetrics.totalTenants)*100).toFixed(1)}% active</span>
                </div>
              </div>
              <div className="p-3 bg-purple-100 rounded-full">
                <Building2 className="h-6 w-6 text-purple-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">ARPU</p>
                <p className="text-2xl font-bold text-gray-900">${platformMetrics.averageRevenuePerUser.toFixed(0)}</p>
                <div className="flex items-center mt-1">
                  <span className="text-sm text-gray-600">per user/month</span>
                </div>
              </div>
              <div className="p-3 bg-yellow-100 rounded-full">
                <Users className="h-6 w-6 text-yellow-600" />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Secondary Metrics */}
      {platformMetrics && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">Churn Rate</h3>
              <BarChart3 className="h-5 w-5 text-gray-400" />
            </div>
            <div className="text-3xl font-bold text-gray-900">{platformMetrics.churnRate}%</div>
            <div className="flex items-center mt-2">
              <ArrowDownRight className="h-4 w-4 text-green-600" />
              <span className="text-sm text-green-600 font-medium">-0.4% from last month</span>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">Conversion Rate</h3>
              <PieChart className="h-5 w-5 text-gray-400" />
            </div>
            <div className="text-3xl font-bold text-gray-900">{platformMetrics.conversionRate}%</div>
            <div className="flex items-center mt-2">
              <ArrowUpRight className="h-4 w-4 text-green-600" />
              <span className="text-sm text-green-600 font-medium">+2.1% from last month</span>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">Growth Rate</h3>
              <TrendingUp className="h-5 w-5 text-gray-400" />
            </div>
            <div className="text-3xl font-bold text-gray-900">{platformMetrics.growthRate}%</div>
            <div className="flex items-center mt-2">
              <ArrowUpRight className="h-4 w-4 text-green-600" />
              <span className="text-sm text-green-600 font-medium">Monthly growth</span>
            </div>
          </div>
        </div>
      )}

      {/* Tenant Details Table */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium text-gray-900">Tenant Performance</h3>
            <div className="flex items-center space-x-2">
              <button className="flex items-center space-x-2 px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50">
                <Filter className="h-4 w-4" />
                <span>Filter</span>
              </button>
            </div>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tenant
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Plan
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Monthly Revenue
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Total Revenue
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Users
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Growth
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Churn Risk
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {tenants.map((tenant) => (
                <tr key={tenant.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10">
                        <div className="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                          <Building2 className="h-6 w-6 text-gray-600" />
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">{tenant.name}</div>
                        <div className="text-sm text-gray-500">{tenant.userCount} users</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${getPlanColor(tenant.plan)}`}>
                      {tenant.plan}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${tenant.monthlyRevenue.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${tenant.totalRevenue.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {tenant.userCount}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <div className="flex items-center">
                      {tenant.growth >= 0 ? (
                        <ArrowUpRight className="h-4 w-4 text-green-600 mr-1" />
                      ) : (
                        <ArrowDownRight className="h-4 w-4 text-red-600 mr-1" />
                      )}
                      <span className={tenant.growth >= 0 ? 'text-green-600' : 'text-red-600'}>
                        {Math.abs(tenant.growth)}%
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className={`capitalize font-medium ${getChurnRiskColor(tenant.churnRisk)}`}>
                      {tenant.churnRisk}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${getStatusColor(tenant.status)}`}>
                      {tenant.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex items-center space-x-2">
                      <button className="text-blue-600 hover:text-blue-900">
                        <Eye className="h-4 w-4" />
                      </button>
                      <button className="text-gray-400 hover:text-gray-600">
                        <MoreHorizontal className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}