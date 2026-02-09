"use client"

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown,
  Users, 
  Eye,
  MousePointer,
  DollarSign,
  Target,
  Download,
  RefreshCw,
  Activity
} from 'lucide-react'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useDashboardMetrics, useDataExport } from '@/hooks/use-analytics'
import { formatMetricValue } from '@/lib/api/analytics-api'
import { 
  RevenueChart, 
  TrafficSourcesChart, 
  ConversionFunnelChart, 
  CampaignPerformanceChart,
  LeadsTimelineChart,
  RealTimeMetrics
} from '@/components/analytics/dashboard-charts'
import { RealTimeAnalytics } from '@/components/analytics/real-time-analytics'
import { TenantMetricsStream } from '@/components/analytics/tenant-metrics-stream'
import { useAuth } from '@/hooks/use-auth'
import { useWebSocket } from '@/lib/websocket-client'


export default function AnalyticsPage() {
  const [dateRange, setDateRange] = useState('7d')
  const [activeTab, setActiveTab] = useState('overview')
  
  // Auth and WebSocket
  const { user } = useAuth()
  const { isConnected } = useWebSocket({
    tenantId: user?.user.tenant_id || 'demo',
    userRole: user?.user.role || 'user',
    userId: user?.user.id || 'demo-user'
  })
  
  // Live data hooks
  const { metrics, loading, error, refetch } = useDashboardMetrics(dateRange)
  const { exportData, loading: exportLoading } = useDataExport()

  const handleExport = async () => {
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - (dateRange === '7d' ? 7 : dateRange === '30d' ? 30 : 90))
    
    await exportData({
      type: 'dashboard',
      dateRange: {
        start: startDate.toISOString(),
        end: new Date().toISOString()
      },
      format: 'xlsx'
    })
  }

  const getTrendIcon = (trend: number) => {
    if (trend > 0) return <TrendingUp className="h-4 w-4 text-green-600" />
    if (trend < 0) return <TrendingDown className="h-4 w-4 text-red-600" />
    return <div className="h-4 w-4" />
  }

  const getTrendColor = (trend: number) => {
    if (trend > 0) return 'text-green-600'
    if (trend < 0) return 'text-red-600'
    return 'text-muted-foreground'
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Analytics</h1>
          <p className="text-muted-foreground">
            Performance insights and campaign analytics
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Select value={dateRange} onValueChange={setDateRange}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7d">Last 7 days</SelectItem>
              <SelectItem value="30d">Last 30 days</SelectItem>
              <SelectItem value="90d">Last 90 days</SelectItem>
            </SelectContent>
          </Select>
          <Button 
            variant="outline" 
            size="icon" 
            onClick={refetch}
            disabled={loading}
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
          <Button 
            variant="outline" 
            onClick={handleExport}
            disabled={exportLoading}
          >
            <Download className="mr-2 h-4 w-4" />
            {exportLoading ? 'Exporting...' : 'Export'}
          </Button>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-600 text-sm">Error loading analytics: {error}</p>
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Impressions</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {loading ? (
                <div className="animate-pulse bg-gray-200 h-6 w-20 rounded"></div>
              ) : (
                metrics?.campaigns.totalImpressions.toLocaleString() || '0'
              )}
            </div>
            <div className="flex items-center text-xs">
              {getTrendIcon(12.5)}
              <span className={`ml-1 ${getTrendColor(12.5)}`}>
                +12.5% from last period
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Clicks</CardTitle>
            <MousePointer className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {loading ? (
                <div className="animate-pulse bg-gray-200 h-6 w-20 rounded"></div>
              ) : (
                metrics?.campaigns.totalClicks.toLocaleString() || '0'
              )}
            </div>
            <div className="flex items-center text-xs">
              {getTrendIcon(8.2)}
              <span className={`ml-1 ${getTrendColor(8.2)}`}>
                +8.2% from last period
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversions</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {loading ? (
                <div className="animate-pulse bg-gray-200 h-6 w-20 rounded"></div>
              ) : (
                metrics?.leads.convertedLeads.toLocaleString() || '0'
              )}
            </div>
            <div className="flex items-center text-xs">
              {getTrendIcon(15.7)}
              <span className={`ml-1 ${getTrendColor(15.7)}`}>
                +15.7% from last period
              </span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Monthly Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {loading ? (
                <div className="animate-pulse bg-gray-200 h-6 w-20 rounded"></div>
              ) : (
                metrics ? formatMetricValue(metrics.overview.monthlyRevenue, 'currency') : '$0'
              )}
            </div>
            <div className="flex items-center text-xs">
              {getTrendIcon(metrics?.overview.revenueGrowth || 0)}
              <span className={`ml-1 ${getTrendColor(metrics?.overview.revenueGrowth || 0)}`}>
                {metrics?.overview.revenueGrowth || 0 > 0 ? '+' : ''}{metrics?.overview.revenueGrowth?.toFixed(1) || '0'}% from last period
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="realtime">Real-Time</TabsTrigger>
          <TabsTrigger value="tenant-metrics">Tenant Metrics</TabsTrigger>
          <TabsTrigger value="campaigns">Campaign Performance</TabsTrigger>
          <TabsTrigger value="audience">Audience Insights</TabsTrigger>
          <TabsTrigger value="trends">Trends</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <div className="grid gap-6">
            {/* Real-time Metrics */}
            <RealTimeMetrics />
            
            {/* Charts Grid */}
            <div className="grid gap-6 md:grid-cols-2">
              <RevenueChart timeRange={dateRange} />
              <TrafficSourcesChart />
              <CampaignPerformanceChart timeRange={dateRange} />
              <LeadsTimelineChart timeRange={dateRange} />
            </div>
          </div>
        </TabsContent>

        <TabsContent value="realtime">
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-medium">Real-Time Analytics Dashboard</h3>
                <p className="text-sm text-muted-foreground">
                  Live performance metrics with WebSocket connectivity
                </p>
              </div>
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${
                  isConnected ? 'bg-green-500' : 'bg-red-500'
                }`} />
                <span className="text-sm text-muted-foreground">
                  {isConnected ? 'Live Data' : 'Connection Lost'}
                </span>
              </div>
            </div>
            <RealTimeAnalytics />
          </div>
        </TabsContent>

        <TabsContent value="tenant-metrics">
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-medium">Multi-Tenant Analytics</h3>
                <p className="text-sm text-muted-foreground">
                  Tenant-specific performance metrics and cross-tenant comparisons
                </p>
              </div>
              <div className="flex items-center space-x-2">
                <Activity className="w-4 h-4" />
                <span className="text-sm text-muted-foreground">
                  {user?.user.role === 'super_admin' ? 'Full Access' : 'Tenant Scoped'}
                </span>
              </div>
            </div>
            <TenantMetricsStream 
              role={user?.user.role}
              allowedTenants={user?.user.role === 'super_admin' ? [] : [user?.user.tenant_id || 'demo']}
              defaultView="detailed"
            />
          </div>
        </TabsContent>

        <TabsContent value="campaigns">
          <div className="grid gap-6">
            <CampaignPerformanceChart timeRange={dateRange} />
            
            <Card>
              <CardHeader>
                <CardTitle>Top Performing Campaigns</CardTitle>
                <CardDescription>Individual campaign metrics and ROI</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {loading ? (
                    [...Array(3)].map((_, i) => (
                      <div key={i} className="animate-pulse">
                        <div className="h-16 bg-gray-200 rounded-lg"></div>
                      </div>
                    ))
                  ) : (
                    metrics?.campaigns.topPerformingCampaigns.map((campaign) => (
                      <div key={campaign.id} className="flex items-center justify-between p-4 border rounded-lg">
                        <div className="flex-1">
                          <div className="font-medium">{campaign.name}</div>
                          <div className="text-sm text-muted-foreground">
                            {campaign.impressions.toLocaleString()} impressions • {campaign.clicks.toLocaleString()} clicks
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="font-medium">{campaign.ctr.toFixed(1)}% CTR</div>
                          <div className="text-sm text-muted-foreground">
                            {formatMetricValue(campaign.cost, 'currency')}
                          </div>
                        </div>
                      </div>
                    )) || (
                      <div className="text-center py-8 text-muted-foreground">
                        <BarChart3 className="h-12 w-12 mx-auto mb-4" />
                        <p>No campaign data available</p>
                      </div>
                    )
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="audience">
          <div className="grid gap-6 md:grid-cols-2">
            <TrafficSourcesChart />
            
            <Card>
              <CardHeader>
                <CardTitle>Audience Demographics</CardTitle>
                <CardDescription>User behavior and demographics</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Unique Visitors</span>
                    <span className="font-medium">
                      {metrics ? metrics.traffic.uniqueVisitors.toLocaleString() : '...'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Page Views</span>
                    <span className="font-medium">
                      {metrics ? metrics.traffic.pageViews.toLocaleString() : '...'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Avg Session Duration</span>
                    <span className="font-medium">
                      {metrics ? `${Math.floor(metrics.traffic.avgSessionDuration / 60)}m ${metrics.traffic.avgSessionDuration % 60}s` : '...'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Bounce Rate</span>
                    <span className="font-medium">
                      {metrics ? `${metrics.traffic.bounceRate}%` : '...'}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="trends">
          <div className="grid gap-6">
            <ConversionFunnelChart />
            
            <div className="grid gap-6 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle>Growth Metrics</CardTitle>
                  <CardDescription>Key growth indicators</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Activity className="h-4 w-4 text-blue-600" />
                        <span className="text-sm">User Growth</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <TrendingUp className="h-4 w-4 text-green-600" />
                        <span className="font-medium text-green-600">
                          +{metrics?.overview.userGrowth?.toFixed(1) || '0'}%
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <DollarSign className="h-4 w-4 text-green-600" />
                        <span className="text-sm">Revenue Growth</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <TrendingUp className="h-4 w-4 text-green-600" />
                        <span className="font-medium text-green-600">
                          +{metrics?.overview.revenueGrowth?.toFixed(1) || '0'}%
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Target className="h-4 w-4 text-purple-600" />
                        <span className="text-sm">Conversion Rate</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <span className="font-medium">
                          {metrics?.overview.conversionRate || '0'}%
                        </span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <CardTitle>Performance Summary</CardTitle>
                  <CardDescription>Overall platform health</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="text-center">
                      <div className="text-3xl font-bold text-green-600">
                        {metrics ? '92%' : '...'}
                      </div>
                      <div className="text-sm text-muted-foreground">Overall Health Score</div>
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Traffic Quality</span>
                        <span className="text-green-600">Excellent</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Conversion Optimization</span>
                        <span className="text-blue-600">Good</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>User Engagement</span>
                        <span className="text-green-600">High</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}