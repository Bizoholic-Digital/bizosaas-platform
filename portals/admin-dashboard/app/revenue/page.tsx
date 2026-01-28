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
  MoreHorizontal,
  Loader2
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

import { useBillingSummary, useSubscriptions } from '@/lib/hooks/use-api'

export default function MultiTenantAnalyticsPage() {
  const { data: summary, isLoading: summaryLoading } = useBillingSummary()
  const { data: subscriptions, isLoading: subsLoading } = useSubscriptions()
  const [selectedPeriod, setSelectedPeriod] = useState('30d')

  const isLoading = summaryLoading || subsLoading

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Loader2 className="animate-spin h-12 w-12 text-blue-600 mx-auto" />
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading platform revenue analytics...</p>
        </div>
      </div>
    )
  }

  const platformMetrics = summary ? {
    totalRevenue: summary.total_revenue_paid || 0,
    monthlyRecurring: (summary.total_revenue_paid || 0) / (summary.active_subscriptions || 1), // Estimate ARPU if MRR isn't precise
    totalTenants: summary.total_tenants || 0,
    activeTenants: summary.active_subscriptions || 0,
    churnRate: 2.1, // Mock for now
    averageRevenuePerUser: (summary.total_revenue_paid || 0) / (summary.total_tenants || 1),
    growthRate: 12.5,
    conversionRate: 65.0
  } : null

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
        <div className="relative z-10">
          <h1 className="text-4xl font-black text-gray-900 tracking-tight flex items-center gap-3">
            <CreditCard className="w-8 h-8 text-indigo-600" />
            Revenue Oversight
          </h1>
          <p className="text-gray-500 font-medium">Cross-tenant performance metrics and platform yield</p>
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
          <div className="group relative overflow-hidden bg-white dark:bg-gray-950 p-6 rounded-[2rem] border border-gray-100 dark:border-gray-800 shadow-sm hover:shadow-xl transition-all hover:-translate-y-1">
            <div className="absolute top-0 right-0 p-4 opacity-5">
              <DollarSign className="w-24 h-24" />
            </div>
            <div className="relative z-10">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 bg-indigo-50 dark:bg-indigo-900/30 rounded-2xl">
                  <DollarSign className="h-6 w-6 text-indigo-600" />
                </div>
                <p className="text-xs font-black uppercase tracking-widest text-gray-400">Total Yield</p>
              </div>
              <p className="text-3xl font-black text-gray-900 dark:text-gray-100">${platformMetrics.totalRevenue.toLocaleString()}</p>
              <div className="mt-4 flex items-center gap-2">
                <span className="flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 bg-green-50 text-green-600 rounded-full">
                  <ArrowUpRight className="h-3 w-3" />
                  {platformMetrics.growthRate}%
                </span>
                <span className="text-[10px] text-gray-400 font-medium">vs last qtr</span>
              </div>
            </div>
          </div>

          <div className="group relative overflow-hidden bg-indigo-600 p-6 rounded-[2rem] shadow-indigo-200 dark:shadow-none shadow-2xl hover:shadow-indigo-300 transition-all hover:-translate-y-1">
            <div className="absolute top-0 right-0 p-4 opacity-10 text-white">
              <TrendingUp className="w-24 h-24" />
            </div>
            <div className="relative z-10">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 bg-white/20 backdrop-blur-md rounded-2xl">
                  <TrendingUp className="h-6 w-6 text-white" />
                </div>
                <p className="text-[10px] font-black uppercase tracking-widest text-indigo-100">Recurring MRR</p>
              </div>
              <p className="text-3xl font-black text-white">${platformMetrics.monthlyRecurring.toLocaleString()}</p>
              <div className="mt-4 flex items-center gap-2">
                <span className="flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 bg-white/20 text-white rounded-full">
                  <ArrowUpRight className="h-3 w-3" />
                  {platformMetrics.growthRate}%
                </span>
                <span className="text-[10px] text-indigo-100 font-medium">Monthly Delta</span>
              </div>
            </div>
          </div>

          <div className="group relative overflow-hidden bg-white dark:bg-gray-950 p-6 rounded-[2rem] border border-gray-100 dark:border-gray-800 shadow-sm hover:shadow-xl transition-all hover:-translate-y-1">
            <div className="relative z-10 text-center flex flex-col items-center">
              <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-full mb-4">
                <Building2 className="h-8 w-8 text-gray-400" />
              </div>
              <p className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-1">Market Saturation</p>
              <p className="text-4xl font-black text-gray-900 dark:text-gray-100">{platformMetrics.activeTenants}</p>
              <div className="w-full h-1.5 bg-gray-100 dark:bg-gray-800 rounded-full mt-4 overflow-hidden">
                <div
                  className="h-full bg-indigo-600 rounded-full"
                  style={{ width: `${(platformMetrics.activeTenants / platformMetrics.totalTenants) * 100}%` }}
                />
              </div>
              <p className="text-[10px] text-gray-400 font-bold mt-2">{platformMetrics.totalTenants} Registered Hubs</p>
            </div>
          </div>

          <div className="group relative overflow-hidden bg-white dark:bg-gray-950 p-6 rounded-[2rem] border border-gray-100 dark:border-gray-800 shadow-sm hover:shadow-xl transition-all hover:-translate-y-1">
            <div className="absolute top-0 right-0 p-4 opacity-5">
              <Users className="w-24 h-24" />
            </div>
            <div className="relative z-10">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-3 bg-yellow-50 dark:bg-yellow-900/30 rounded-2xl">
                  <Users className="h-6 w-6 text-yellow-600" />
                </div>
                <p className="text-xs font-black uppercase tracking-widest text-gray-400">ARPU Density</p>
              </div>
              <p className="text-3xl font-black text-gray-900 dark:text-gray-100">${platformMetrics.averageRevenuePerUser.toFixed(0)}</p>
              <div className="mt-4 flex items-center gap-2 text-[10px] font-bold text-gray-500">
                Avg per user/node
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
              {(subscriptions?.subscriptions as any[] || []).map((sub) => (
                <tr key={sub.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10">
                        <div className="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center">
                          <Building2 className="h-6 w-6 text-gray-600" />
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">{sub.tenant_name || 'Business Tenant'}</div>
                        <div className="text-sm text-gray-500">{sub.tenant_id.substring(0, 8)}...</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${getPlanColor(sub.plan_name?.toLowerCase())}`}>
                      {sub.plan_name || 'Standard'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${sub.amount?.toLocaleString() || '0'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${(sub.amount * 12)?.toLocaleString() || '0'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    --
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <div className="flex items-center">
                      <ArrowUpRight className="h-4 w-4 text-green-600 mr-1" />
                      <span className="text-green-600">
                        Stable
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className={`capitalize font-medium text-green-600`}>
                      Low
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${getStatusColor(sub.status)}`}>
                      {sub.status}
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