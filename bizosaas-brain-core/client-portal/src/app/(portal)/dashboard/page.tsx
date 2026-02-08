'use client'

import { useEffect, useState } from 'react'
import { DollarSign, Users, TrendingUp, Target, Activity } from 'lucide-react'
import StatsCard from '@/features/dashboard/components/StatsCard'
import { brainGateway } from '@/lib/brain-gateway-client'
import { useTenant } from '@/contexts/TenantContext'

interface DashboardStats {
  revenue: {
    total: number
    change: number
  }
  users: {
    total: number
    active: number
    change: number
  }
  campaigns: {
    active: number
    change: number
  }
  roi: {
    value: number
    change: number
  }
}

interface ActivityItem {
  id: string
  type: string
  title: string
  description: string
  timestamp: string
  icon?: string
}

export default function DashboardPage() {
  const { currentTenant } = useTenant()
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [activities, setActivities] = useState<ActivityItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!currentTenant) return

    const fetchDashboardData = async () => {
      try {
        setLoading(true)
        setError(null)

        // Fetch stats from Brain Gateway
        const statsResponse = await brainGateway.getDashboardStats()
        setStats(statsResponse.data)

        // Fetch recent activity
        const activityResponse = await brainGateway.getDashboardActivity(10)
        setActivities(activityResponse.data)

        setLoading(false)
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err)

        // Use mock data for development/demo
        setStats({
          revenue: { total: 45231, change: 12.5 },
          users: { total: 1234, active: 856, change: 8.2 },
          campaigns: { active: 12, change: 3.1 },
          roi: { value: 285, change: 15.3 },
        })

        setActivities([
          {
            id: '1',
            type: 'campaign',
            title: 'New Campaign Launched',
            description: 'Summer Sale 2025 campaign is now live',
            timestamp: '2 hours ago',
          },
          {
            id: '2',
            type: 'user',
            title: 'New User Registered',
            description: 'John Doe joined your platform',
            timestamp: '4 hours ago',
          },
          {
            id: '3',
            type: 'order',
            title: 'Order Completed',
            description: 'Order #12345 has been shipped',
            timestamp: '6 hours ago',
          },
        ])

        setLoading(false)
      }
    }

    fetchDashboardData()
  }, [currentTenant])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">
          Welcome back! Here&apos;s what&apos;s happening with your business.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Revenue"
          value={`$${stats?.revenue.total.toLocaleString() || 0}`}
          change={{
            value: stats?.revenue.change || 0,
            label: 'from last month',
            positive: (stats?.revenue.change || 0) > 0,
          }}
          icon={DollarSign}
          iconColor="bg-green-500"
          loading={loading}
        />

        <StatsCard
          title="Total Users"
          value={stats?.users.total || 0}
          change={{
            value: stats?.users.change || 0,
            label: 'from last month',
            positive: (stats?.users.change || 0) > 0,
          }}
          icon={Users}
          iconColor="bg-blue-500"
          loading={loading}
        />

        <StatsCard
          title="Active Campaigns"
          value={stats?.campaigns.active || 0}
          change={{
            value: stats?.campaigns.change || 0,
            label: 'from last month',
            positive: (stats?.campaigns.change || 0) > 0,
          }}
          icon={Target}
          iconColor="bg-purple-500"
          loading={loading}
        />

        <StatsCard
          title="ROI"
          value={`${stats?.roi.value || 0}%`}
          change={{
            value: stats?.roi.change || 0,
            label: 'from last month',
            positive: (stats?.roi.change || 0) > 0,
          }}
          icon={TrendingUp}
          iconColor="bg-orange-500"
          loading={loading}
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activity */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-gray-600" />
              <h2 className="text-lg font-semibold text-gray-900">Recent Activity</h2>
            </div>
          </div>
          <div className="p-6">
            {loading ? (
              <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="animate-pulse flex gap-4">
                    <div className="h-10 w-10 bg-gray-200 rounded-full"></div>
                    <div className="flex-1">
                      <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                      <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                    </div>
                  </div>
                ))}
              </div>
            ) : activities.length > 0 ? (
              <div className="space-y-4">
                {activities.map((activity) => (
                  <div key={activity.id} className="flex gap-4 p-3 rounded-lg hover:bg-gray-50 transition-colors">
                    <div className="h-10 w-10 rounded-full bg-solid-100 flex items-center justify-center flex-shrink-0">
                      <Activity className="h-5 w-5 text-solid-900" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900">{activity.title}</p>
                      <p className="text-sm text-gray-600 mt-1">{activity.description}</p>
                      <p className="text-xs text-gray-500 mt-1">{activity.timestamp}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <Activity className="h-12 w-12 text-gray-400 mx-auto mb-3" />
                <p className="text-gray-600">No recent activity</p>
              </div>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Quick Actions</h2>
          </div>
          <div className="p-6 space-y-3">
            <button className="w-full text-left px-4 py-3 bg-solid-900 text-white rounded-lg hover:bg-solid-800 transition-colors">
              <p className="font-medium">Create Campaign</p>
              <p className="text-sm text-solid-100 mt-1">Launch a new marketing campaign</p>
            </button>
            <button className="w-full text-left px-4 py-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <p className="font-medium text-gray-900">Add Contact</p>
              <p className="text-sm text-gray-600 mt-1">Import or create new contacts</p>
            </button>
            <button className="w-full text-left px-4 py-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <p className="font-medium text-gray-900">View Analytics</p>
              <p className="text-sm text-gray-600 mt-1">Check your performance metrics</p>
            </button>
            <button className="w-full text-left px-4 py-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <p className="font-medium text-gray-900">Manage Products</p>
              <p className="text-sm text-gray-600 mt-1">Update your product catalog</p>
            </button>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}
    </div>
  )
}
