'use client'

import { useState, useEffect, useCallback } from 'react'
import { analyticsApi, DashboardMetrics, TimeSeriesData, ChartData, RealtimeMetrics } from '@/lib/api/analytics-api'

// Hook for dashboard metrics
export function useDashboardMetrics(timeRange: string = '7d') {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchMetrics = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await analyticsApi.getDashboardMetrics(timeRange)
      setMetrics(data)
    } catch (err) {
      console.error('Failed to fetch dashboard metrics:', err)
      setError(err instanceof Error ? err.message : 'Failed to fetch metrics')
      
      // Fallback to mock data
      const mockMetrics: DashboardMetrics = {
        overview: {
          totalUsers: 12847,
          activeUsers: 2534,
          totalRevenue: 45678.90,
          monthlyRevenue: 12345.67,
          revenueGrowth: 12.5,
          userGrowth: 8.3,
          conversionRate: 3.2,
          churnRate: 2.1
        },
        traffic: {
          pageViews: 45623,
          uniqueVisitors: 12847,
          bounceRate: 34.2,
          avgSessionDuration: 245,
          topPages: [
            { page: '/', views: 8934 },
            { page: '/pricing', views: 5432 },
            { page: '/features', views: 3421 },
            { page: '/about', views: 2345 },
            { page: '/contact', views: 1876 }
          ],
          trafficSources: [
            { source: 'Organic Search', visitors: 5432, percentage: 42.3 },
            { source: 'Direct', visitors: 3421, percentage: 26.6 },
            { source: 'Social Media', visitors: 2345, percentage: 18.3 },
            { source: 'Referral', visitors: 1234, percentage: 9.6 },
            { source: 'Email', visitors: 415, percentage: 3.2 }
          ]
        },
        campaigns: {
          activeCampaigns: 8,
          totalImpressions: 145623,
          totalClicks: 4567,
          averageCTR: 3.14,
          topPerformingCampaigns: [
            {
              id: '1',
              name: 'Summer Sale 2024',
              impressions: 45623,
              clicks: 1234,
              ctr: 2.7,
              conversions: 89,
              cost: 1250.00
            },
            {
              id: '2', 
              name: 'Product Launch',
              impressions: 32145,
              clicks: 987,
              ctr: 3.1,
              conversions: 67,
              cost: 980.00
            }
          ]
        },
        leads: {
          totalLeads: 1234,
          newLeadsToday: 23,
          qualifiedLeads: 456,
          convertedLeads: 89,
          leadsBySource: [
            { source: 'Website Form', count: 456 },
            { source: 'LinkedIn', count: 234 },
            { source: 'Google Ads', count: 189 },
            { source: 'Social Media', count: 167 },
            { source: 'Referral', count: 123 },
            { source: 'Cold Outreach', count: 65 }
          ],
          conversionFunnel: [
            { stage: 'Visitors', count: 12847, rate: 100 },
            { stage: 'Leads', count: 1234, rate: 9.6 },
            { stage: 'Qualified', count: 456, rate: 37.0 },
            { stage: 'Opportunities', count: 123, rate: 27.0 },
            { stage: 'Customers', count: 89, rate: 72.4 }
          ]
        }
      }
      setMetrics(mockMetrics)
    } finally {
      setLoading(false)
    }
  }, [timeRange])

  useEffect(() => {
    fetchMetrics()
  }, [fetchMetrics])

  return {
    metrics,
    loading,
    error,
    refetch: fetchMetrics,
  }
}

// Hook for time series data
export function useTimeSeries(
  type: 'traffic' | 'revenue' | 'leads' | 'campaigns',
  timeRange: string = '7d',
  granularity: string = 'day'
) {
  const [data, setData] = useState<TimeSeriesData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      
      let apiData: TimeSeriesData[]
      switch (type) {
        case 'traffic':
          apiData = await analyticsApi.getTrafficTimeSeries(timeRange, granularity)
          break
        case 'revenue':
          apiData = await analyticsApi.getRevenueTimeSeries(timeRange, granularity)
          break
        case 'leads':
          apiData = await analyticsApi.getLeadsTimeSeries(timeRange, granularity)
          break
        case 'campaigns':
          apiData = await analyticsApi.getCampaignPerformanceTimeSeries(timeRange)
          break
        default:
          throw new Error('Invalid time series type')
      }
      
      setData(apiData)
    } catch (err) {
      console.error(`Failed to fetch ${type} time series:`, err)
      setError(err instanceof Error ? err.message : 'Failed to fetch data')
      
      // Generate mock time series data
      const days = timeRange === '7d' ? 7 : timeRange === '30d' ? 30 : 90
      const mockData: TimeSeriesData[] = Array.from({ length: days }, (_, i) => {
        const date = new Date()
        date.setDate(date.getDate() - (days - 1 - i))
        
        let value: number
        switch (type) {
          case 'traffic':
            value = Math.floor(Math.random() * 2000) + 800
            break
          case 'revenue':
            value = Math.floor(Math.random() * 5000) + 1000
            break
          case 'leads':
            value = Math.floor(Math.random() * 50) + 10
            break
          case 'campaigns':
            value = Math.floor(Math.random() * 100) + 20
            break
          default:
            value = 0
        }
        
        return {
          timestamp: date.toISOString(),
          value,
          label: date.toLocaleDateString()
        }
      })
      
      setData(mockData)
    } finally {
      setLoading(false)
    }
  }, [type, timeRange, granularity])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  return {
    data,
    loading,
    error,
    refetch: fetchData,
  }
}

// Hook for chart data
export function useChartData(type: 'traffic-sources' | 'conversion-funnel' | 'revenue-breakdown' | 'campaign-roi') {
  const [data, setData] = useState<ChartData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      
      let chartData: ChartData
      switch (type) {
        case 'traffic-sources':
          chartData = await analyticsApi.getTrafficSourcesChart()
          break
        case 'conversion-funnel':
          chartData = await analyticsApi.getConversionFunnelChart()
          break
        case 'revenue-breakdown':
          chartData = await analyticsApi.getRevenueBreakdownChart()
          break
        case 'campaign-roi':
          chartData = await analyticsApi.getCampaignROIChart()
          break
        default:
          throw new Error('Invalid chart type')
      }
      
      setData(chartData)
    } catch (err) {
      console.error(`Failed to fetch ${type} chart:`, err)
      setError(err instanceof Error ? err.message : 'Failed to fetch chart data')
      
      // Mock chart data
      let mockData: ChartData
      switch (type) {
        case 'traffic-sources':
          mockData = {
            labels: ['Organic Search', 'Direct', 'Social Media', 'Referral', 'Email'],
            datasets: [{
              label: 'Visitors',
              data: [5432, 3421, 2345, 1234, 415],
              backgroundColor: ['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6']
            }]
          }
          break
        case 'conversion-funnel':
          mockData = {
            labels: ['Visitors', 'Leads', 'Qualified', 'Opportunities', 'Customers'],
            datasets: [{
              label: 'Count',
              data: [12847, 1234, 456, 123, 89],
              backgroundColor: '#3B82F6'
            }]
          }
          break
        case 'revenue-breakdown':
          mockData = {
            labels: ['Subscriptions', 'One-time', 'Services', 'Add-ons'],
            datasets: [{
              label: 'Revenue',
              data: [28500, 12300, 8900, 4560],
              backgroundColor: ['#10B981', '#3B82F6', '#F59E0B', '#8B5CF6']
            }]
          }
          break
        case 'campaign-roi':
          mockData = {
            labels: ['Google Ads', 'Facebook', 'LinkedIn', 'Twitter', 'Email'],
            datasets: [{
              label: 'ROI %',
              data: [245, 189, 167, 134, 298],
              backgroundColor: '#10B981'
            }]
          }
          break
        default:
          mockData = { labels: [], datasets: [] }
      }
      
      setData(mockData)
    } finally {
      setLoading(false)
    }
  }, [type])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  return {
    data,
    loading,
    error,
    refetch: fetchData,
  }
}

// Hook for real-time metrics
export function useRealtimeMetrics() {
  const [metrics, setMetrics] = useState<RealtimeMetrics | null>(null)
  const [connected, setConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const cleanup = analyticsApi.connectRealtime((data) => {
      setMetrics(data)
      setConnected(true)
      setError(null)
    })

    // Mock real-time data fallback
    const mockInterval = setInterval(() => {
      if (!connected) {
        const mockData: RealtimeMetrics = {
          currentUsers: Math.floor(Math.random() * 100) + 50,
          pageViews: Math.floor(Math.random() * 1000) + 500,
          revenue: Math.floor(Math.random() * 500) + 100,
          leads: Math.floor(Math.random() * 10) + 1,
          campaigns: {
            impressions: Math.floor(Math.random() * 5000) + 1000,
            clicks: Math.floor(Math.random() * 200) + 50,
            conversions: Math.floor(Math.random() * 20) + 5
          },
          alerts: [
            {
              id: '1',
              type: 'success',
              message: 'New high-value lead generated',
              timestamp: new Date().toISOString()
            }
          ]
        }
        setMetrics(mockData)
      }
    }, 5000)

    return () => {
      cleanup()
      clearInterval(mockInterval)
    }
  }, [connected])

  return {
    metrics,
    connected,
    error,
  }
}

// Hook for custom event tracking
export function useEventTracking() {
  const trackEvent = useCallback(async (eventName: string, properties: Record<string, any> = {}) => {
    try {
      await analyticsApi.trackEvent({
        name: eventName,
        properties,
        userId: localStorage.getItem('user_id') || undefined,
        timestamp: new Date().toISOString()
      })
    } catch (error) {
      console.error('Failed to track event:', error)
    }
  }, [])

  return { trackEvent }
}

// Hook for exporting data
export function useDataExport() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const exportData = useCallback(async (config: {
    type: 'dashboard' | 'traffic' | 'revenue' | 'campaigns' | 'leads'
    dateRange: { start: string; end: string }
    format: 'json' | 'csv' | 'xlsx'
  }) => {
    try {
      setLoading(true)
      setError(null)
      const blob = await analyticsApi.exportData(config)
      
      // Create download link
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `analytics-${config.type}-${new Date().toISOString().split('T')[0]}.${config.format}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error('Failed to export data:', err)
      setError(err instanceof Error ? err.message : 'Failed to export data')
    } finally {
      setLoading(false)
    }
  }, [])

  return {
    exportData,
    loading,
    error,
  }
}