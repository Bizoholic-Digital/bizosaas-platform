'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  TrendingUp, 
  TrendingDown, 
  Users, 
  DollarSign, 
  Target, 
  Activity,
  ExternalLink,
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  BarChart3
} from 'lucide-react'

interface AnalyticsData {
  overview: {
    total_campaigns: number
    active_campaigns: number
    total_leads: number
    conversion_rate: number
    total_revenue: number
    roi: number
  }
  campaign_performance: Array<{
    campaign_id: string
    name: string
    channel: string
    status: string
    spend: number
    leads: number
    conversions: number
    revenue: number
    roi: number
    last_updated: string
  }>
  channel_performance: Record<string, {
    leads: number
    spend: number
    revenue: number
    roi: number
    trend: 'up' | 'down' | 'stable'
  }>
  real_time_metrics: {
    active_visitors: number
    live_conversions_today: number
    revenue_today: number
    top_performing_campaign: string
    alerts: Array<{
      type: 'warning' | 'success' | 'info'
      message: string
      timestamp: string
    }>
  }
  recent_activity: Array<{
    timestamp: string
    type: string
    campaign: string
    value: number
    description: string
  }>
  last_updated: string
}

export function AnalyticsDashboard() {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [lastRefresh, setLastRefresh] = useState<Date>(new Date())

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/brain/analytics/dashboard')
      if (response.ok) {
        const data = await response.json()
        setAnalytics(data)
        setLastRefresh(new Date())
      } else {
        console.error('Failed to fetch analytics data:', response.status)
      }
    } catch (error) {
      console.error('Error fetching analytics data:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchAnalyticsData()
    
    // Set up auto-refresh every 30 seconds for real-time data
    const interval = setInterval(fetchAnalyticsData, 30000)
    return () => clearInterval(interval)
  }, [])

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount)
  }

  const formatPercentage = (value: number) => {
    return `${value.toFixed(1)}%`
  }

  const getChannelIcon = (channel: string) => {
    switch (channel) {
      case 'google_ads': return '🔍'
      case 'facebook_ads': return '👤'
      case 'linkedin_ads': return '💼'
      case 'email_marketing': return '✉️'
      default: return '📊'
    }
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return <TrendingUp className="w-4 h-4 text-green-500" />
      case 'down': return <TrendingDown className="w-4 h-4 text-red-500" />
      default: return <Activity className="w-4 h-4 text-gray-500" />
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'active':
        return <Badge className="bg-green-100 text-green-800">Active</Badge>
      case 'paused':
        return <Badge className="bg-yellow-100 text-yellow-800">Paused</Badge>
      case 'completed':
        return <Badge className="bg-blue-100 text-blue-800">Completed</Badge>
      default:
        return <Badge className="bg-gray-100 text-gray-800">{status}</Badge>
    }
  }

  if (loading && !analytics) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-8 h-8 animate-spin text-blue-600" />
        <span className="ml-2 text-gray-600">Loading analytics dashboard...</span>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h2>
          <p className="text-gray-600">Real-time campaign performance and insights</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="text-sm text-gray-500">
            Last updated: {lastRefresh.toLocaleTimeString()}
          </div>
          <Button
            onClick={fetchAnalyticsData}
            variant="outline"
            size="sm"
            disabled={loading}
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button asChild size="sm">
            <a href="http://localhost:3009/admin" target="_blank" rel="noopener noreferrer">
              <ExternalLink className="w-4 h-4 mr-2" />
              Full Analytics
            </a>
          </Button>
        </div>
      </div>

      {/* Key Metrics Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Leads</p>
                <p className="text-2xl font-bold text-gray-900">
                  {analytics?.overview.total_leads.toLocaleString() || 0}
                </p>
              </div>
              <Users className="w-8 h-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Revenue</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatCurrency(analytics?.overview.total_revenue || 0)}
                </p>
              </div>
              <DollarSign className="w-8 h-8 text-green-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Conversion Rate</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatPercentage(analytics?.overview.conversion_rate || 0)}
                </p>
              </div>
              <Target className="w-8 h-8 text-purple-600" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">ROI</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatPercentage(analytics?.overview.roi || 0)}
                </p>
              </div>
              <BarChart3 className="w-8 h-8 text-orange-600" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Real-time Alerts */}
      {analytics?.real_time_metrics.alerts && analytics.real_time_metrics.alerts.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <AlertTriangle className="w-5 h-5 mr-2" />
              Real-time Alerts
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {analytics.real_time_metrics.alerts.map((alert, index) => (
                <div
                  key={index}
                  className={`p-3 rounded-lg border ${
                    alert.type === 'success' 
                      ? 'bg-green-50 border-green-200' 
                      : alert.type === 'warning'
                      ? 'bg-yellow-50 border-yellow-200'
                      : 'bg-blue-50 border-blue-200'
                  }`}
                >
                  <div className="flex items-center">
                    {alert.type === 'success' ? (
                      <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                    ) : (
                      <AlertTriangle className="w-4 h-4 text-yellow-500 mr-2" />
                    )}
                    <span className="text-sm font-medium">{alert.message}</span>
                    <span className="text-xs text-gray-500 ml-auto">
                      {new Date(alert.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Campaign Performance */}
      <Card>
        <CardHeader>
          <CardTitle>Campaign Performance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-2">Campaign</th>
                  <th className="text-left py-2">Channel</th>
                  <th className="text-left py-2">Status</th>
                  <th className="text-right py-2">Spend</th>
                  <th className="text-right py-2">Leads</th>
                  <th className="text-right py-2">Revenue</th>
                  <th className="text-right py-2">ROI</th>
                </tr>
              </thead>
              <tbody>
                {analytics?.campaign_performance.map((campaign) => (
                  <tr key={campaign.campaign_id} className="border-b hover:bg-gray-50">
                    <td className="py-3">
                      <div>
                        <div className="font-medium text-gray-900">{campaign.name}</div>
                        <div className="text-sm text-gray-500">ID: {campaign.campaign_id}</div>
                      </div>
                    </td>
                    <td className="py-3">
                      <div className="flex items-center">
                        <span className="mr-2">{getChannelIcon(campaign.channel)}</span>
                        <span className="capitalize">{campaign.channel.replace('_', ' ')}</span>
                      </div>
                    </td>
                    <td className="py-3">{getStatusBadge(campaign.status)}</td>
                    <td className="py-3 text-right">{formatCurrency(campaign.spend)}</td>
                    <td className="py-3 text-right">{campaign.leads}</td>
                    <td className="py-3 text-right">{formatCurrency(campaign.revenue)}</td>
                    <td className="py-3 text-right font-medium">
                      {formatPercentage(campaign.roi)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Channel Performance */}
      <Card>
        <CardHeader>
          <CardTitle>Channel Performance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {analytics && Object.entries(analytics.channel_performance).map(([channel, data]) => (
              <div key={channel} className="p-4 border rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center">
                    <span className="mr-2">{getChannelIcon(channel)}</span>
                    <span className="font-medium capitalize">
                      {channel.replace('_', ' ')}
                    </span>
                  </div>
                  {getTrendIcon(data.trend)}
                </div>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Leads:</span>
                    <span className="font-medium">{data.leads}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Revenue:</span>
                    <span className="font-medium">{formatCurrency(data.revenue)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">ROI:</span>
                    <span className="font-medium">{formatPercentage(data.roi)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {analytics?.recent_activity.map((activity, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center">
                  <div className={`w-2 h-2 rounded-full mr-3 ${
                    activity.type === 'conversion' ? 'bg-green-500' :
                    activity.type === 'lead' ? 'bg-blue-500' : 'bg-purple-500'
                  }`}></div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">{activity.description}</p>
                    <p className="text-xs text-gray-500">{activity.campaign}</p>
                  </div>
                </div>
                <div className="text-right">
                  {activity.value > 0 && (
                    <p className="text-sm font-medium text-green-600">
                      {formatCurrency(activity.value)}
                    </p>
                  )}
                  <p className="text-xs text-gray-500">
                    {new Date(activity.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}