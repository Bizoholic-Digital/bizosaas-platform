'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ChartContainer, ChartTooltip, ChartTooltipContent, ChartLegend, ChartLegendContent } from '@/components/ui/chart'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  Funnel,
  FunnelChart
} from 'recharts'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { useDashboardMetrics, useTimeSeries, useChartData } from '@/hooks/use-analytics'
import { formatMetricValue, generateChartColors } from '@/lib/api/analytics-api'

interface MetricTrend {
  value: string
  change: string
  trend: 'up' | 'down' | 'neutral'
  color: string
}

// Revenue Chart Component
export function RevenueChart({ timeRange = '7d' }: { timeRange?: string }) {
  const { data, loading, error } = useTimeSeries('revenue', timeRange, 'day')

  const chartConfig = {
    revenue: {
      label: "Revenue",
      color: "#10B981", // emerald-500
    },
  }

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Revenue Trend</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse bg-gray-200 h-64 rounded-md"></div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Revenue Trend</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-red-600">Failed to load revenue data</div>
        </CardContent>
      </Card>
    )
  }

  const chartData = data.map(item => ({
    date: new Date(item.timestamp).toLocaleDateString(),
    revenue: item.value
  }))

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <div>
          <CardTitle>Revenue Trend</CardTitle>
          <CardDescription>Daily revenue over {timeRange}</CardDescription>
        </div>
        <div className="flex items-center space-x-1 text-sm">
          <TrendingUp className="h-4 w-4 text-green-600" />
          <span className="text-green-600">+12.5%</span>
        </div>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <AreaChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis tickFormatter={(value) => formatMetricValue(value, 'currency')} />
            <ChartTooltip 
              content={<ChartTooltipContent />}
              formatter={(value: number) => [formatMetricValue(value, 'currency'), 'Revenue']}
            />
            <Area 
              type="monotone" 
              dataKey="revenue" 
              stroke="var(--color-revenue)" 
              fill="var(--color-revenue)"
              fillOpacity={0.2}
            />
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}

// Traffic Sources Chart Component
export function TrafficSourcesChart() {
  const { data, loading, error } = useChartData('traffic-sources')

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Traffic Sources</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse bg-gray-200 h-64 rounded-md"></div>
        </CardContent>
      </Card>
    )
  }

  if (error || !data) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Traffic Sources</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-red-600">Failed to load traffic data</div>
        </CardContent>
      </Card>
    )
  }

  const chartData = data.labels.map((label, index) => ({
    name: label,
    value: data.datasets[0].data[index],
    fill: Array.isArray(data.datasets[0].backgroundColor) 
      ? data.datasets[0].backgroundColor[index] 
      : data.datasets[0].backgroundColor || generateChartColors(1)[0]
  }))

  const chartConfig = data.labels.reduce((config, label, index) => ({
    ...config,
    [label.toLowerCase().replace(/\s+/g, '_')]: {
      label: label,
      color: Array.isArray(data.datasets[0].backgroundColor) 
        ? data.datasets[0].backgroundColor[index]
        : generateChartColors(data.labels.length)[index]
    }
  }), {})

  return (
    <Card>
      <CardHeader>
        <CardTitle>Traffic Sources</CardTitle>
        <CardDescription>Where your visitors come from</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <PieChart>
            <ChartTooltip 
              content={<ChartTooltipContent />}
              formatter={(value: number, name: string) => [
                `${value.toLocaleString()} visitors`, 
                name
              ]}
            />
            <Pie
              data={chartData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={100}
              label={({ name, percent }: any) => `${name}: ${(percent * 100).toFixed(1)}%`}
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.fill} />
              ))}
            </Pie>
          </PieChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}

// Conversion Funnel Chart Component
export function ConversionFunnelChart() {
  const { data, loading, error } = useChartData('conversion-funnel')

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Conversion Funnel</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse bg-gray-200 h-64 rounded-md"></div>
        </CardContent>
      </Card>
    )
  }

  if (error || !data) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Conversion Funnel</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-red-600">Failed to load funnel data</div>
        </CardContent>
      </Card>
    )
  }

  const chartData = data.labels.map((label, index) => ({
    name: label,
    value: data.datasets[0].data[index],
    fill: generateChartColors(data.labels.length)[index]
  }))

  const chartConfig = data.labels.reduce((config, label, index) => ({
    ...config,
    [label.toLowerCase().replace(/\s+/g, '_')]: {
      label: label,
      color: generateChartColors(data.labels.length)[index]
    }
  }), {})

  return (
    <Card>
      <CardHeader>
        <CardTitle>Conversion Funnel</CardTitle>
        <CardDescription>Customer journey through your funnel</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <BarChart data={chartData} layout="horizontal">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" tickFormatter={(value) => value.toLocaleString()} />
            <YAxis dataKey="name" type="category" width={100} />
            <ChartTooltip 
              content={<ChartTooltipContent />}
              formatter={(value: number, name: string) => [
                value.toLocaleString(), 
                'Count'
              ]}
            />
            <Bar dataKey="value" radius={[0, 4, 4, 0]}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.fill} />
              ))}
            </Bar>
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}

// Campaign Performance Chart Component
export function CampaignPerformanceChart({ timeRange = '7d' }: { timeRange?: string }) {
  const { data, loading, error } = useTimeSeries('campaigns', timeRange, 'day')

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Campaign Performance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse bg-gray-200 h-64 rounded-md"></div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Campaign Performance</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-red-600">Failed to load campaign data</div>
        </CardContent>
      </Card>
    )
  }

  const chartData = data.map(item => ({
    date: new Date(item.timestamp).toLocaleDateString(),
    performance: item.value
  }))

  const chartConfig = {
    performance: {
      label: "Performance Score",
      color: "#3B82F6", // blue-500
    },
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Campaign Performance</CardTitle>
        <CardDescription>Daily performance metrics</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <ChartTooltip 
              content={<ChartTooltipContent />}
              formatter={(value: number) => [value.toFixed(1), 'Performance Score']}
            />
            <Line 
              type="monotone" 
              dataKey="performance" 
              stroke="var(--color-performance)"
              strokeWidth={2}
              dot={{ r: 4 }}
            />
          </LineChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}

// Leads Timeline Chart Component
export function LeadsTimelineChart({ timeRange = '7d' }: { timeRange?: string }) {
  const { data, loading, error } = useTimeSeries('leads', timeRange, 'day')

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Lead Generation</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse bg-gray-200 h-64 rounded-md"></div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Lead Generation</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-red-600">Failed to load leads data</div>
        </CardContent>
      </Card>
    )
  }

  const chartData = data.map(item => ({
    date: new Date(item.timestamp).toLocaleDateString(),
    leads: item.value
  }))

  const chartConfig = {
    leads: {
      label: "New Leads",
      color: "#F59E0B", // amber-500
    },
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Lead Generation</CardTitle>
        <CardDescription>New leads over time</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <ChartTooltip 
              content={<ChartTooltipContent />}
              formatter={(value: number) => [value, 'New Leads']}
            />
            <Bar 
              dataKey="leads" 
              fill="var(--color-leads)"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}

// Real-time Metrics Component
export function RealTimeMetrics() {
  const { metrics } = useDashboardMetrics()

  if (!metrics) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Real-time Overview</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse bg-gray-200 h-32 rounded-md"></div>
        </CardContent>
      </Card>
    )
  }

  const realTimeStats = [
    {
      label: 'Active Users',
      value: metrics.overview.activeUsers.toLocaleString(),
      trend: 'up' as const,
      color: 'text-green-600'
    },
    {
      label: 'Page Views',
      value: metrics.traffic.pageViews.toLocaleString(),
      trend: 'up' as const,
      color: 'text-blue-600'
    },
    {
      label: 'Conversion Rate',
      value: `${metrics.overview.conversionRate}%`,
      trend: metrics.overview.conversionRate > 3 ? 'up' as const : 'down' as const,
      color: metrics.overview.conversionRate > 3 ? 'text-green-600' : 'text-red-600'
    },
    {
      label: 'Bounce Rate',
      value: `${metrics.traffic.bounceRate}%`,
      trend: metrics.traffic.bounceRate < 40 ? 'up' as const : 'down' as const,
      color: metrics.traffic.bounceRate < 40 ? 'text-green-600' : 'text-red-600'
    },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>Real-time Overview</CardTitle>
        <CardDescription>Live metrics updating automatically</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {realTimeStats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className={`text-2xl font-bold ${stat.color}`}>
                {stat.value}
              </div>
              <div className="text-sm text-muted-foreground flex items-center justify-center">
                {stat.trend === 'up' ? (
                  <TrendingUp className="h-3 w-3 mr-1" />
                ) : stat.trend === 'down' ? (
                  <TrendingDown className="h-3 w-3 mr-1" />
                ) : (
                  <Minus className="h-3 w-3 mr-1" />
                )}
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}