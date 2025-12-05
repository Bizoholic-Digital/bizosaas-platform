'use client'

import { useEffect, useState } from 'react'
import { Activity, DollarSign, Zap, TrendingUp, Clock, FileText } from 'lucide-react'

interface MonitoringData {
  provider_health: Record<string, any>
  routing_analytics: {
    total_requests: number
    avg_latency_ms: number
    success_rate: number
  }
  cost_summary: {
    total_cost: number
    total_savings: number
    savings_percentage: number
  }
  rag_analytics: {
    total_queries: number
    avg_latency_ms: number
    avg_results: number
  }
  recommendations: string[]
}

export default function AIUsageMonitoring() {
  const [data, setData] = useState<MonitoringData | null>(null)
  const [loading, setLoading] = useState(true)
  const [period, setPeriod] = useState('24')

  useEffect(() => {
    fetchMonitoringData()
    const interval = setInterval(fetchMonitoringData, 60000) // Refresh every minute
    return () => clearInterval(interval)
  }, [period])

  const fetchMonitoringData = async () => {
    try {
      const response = await fetch(`/api/brain/llm/monitoring?hours=${period}`)
      if (response.ok) {
        const result = await response.json()
        setData(result)
      }
    } catch (error) {
      console.error('Failed to fetch monitoring data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Activity className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    )
  }

  if (!data) {
    return (
      <div className="p-6">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-yellow-800">Unable to load monitoring data. Please try again later.</p>
        </div>
      </div>
    )
  }

  const activeProviders = Object.values(data.provider_health).filter(
    (p: any) => p.status === 'healthy'
  ).length

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">AI Usage & Performance</h1>
        <p className="text-gray-600 mt-1">Monitor your AI usage, costs, and performance metrics</p>

        <div className="mt-4 flex items-center gap-4">
          <label className="text-sm text-gray-600">Time Period:</label>
          <select
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            className="px-3 py-1.5 border border-gray-300 rounded-md text-sm"
          >
            <option value="1">Last Hour</option>
            <option value="24">Last 24 Hours</option>
            <option value="168">Last 7 Days</option>
            <option value="720">Last 30 Days</option>
          </select>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <MetricCard
          title="Total AI Requests"
          value={data.routing_analytics.total_requests.toLocaleString()}
          icon={<Activity className="w-8 h-8 text-blue-600" />}
          subtitle={`${period}h period`}
        />
        <MetricCard
          title="Success Rate"
          value={`${(data.routing_analytics.success_rate * 100).toFixed(1)}%`}
          icon={<TrendingUp className="w-8 h-8 text-green-600" />}
          subtitle="Successful responses"
        />
        <MetricCard
          title="Avg Response Time"
          value={`${data.routing_analytics.avg_latency_ms.toFixed(0)}ms`}
          icon={<Zap className="w-8 h-8 text-yellow-600" />}
          subtitle="Average latency"
        />
        <MetricCard
          title="Active Providers"
          value={`${activeProviders}`}
          icon={<Activity className="w-8 h-8 text-purple-600" />}
          subtitle="Healthy AI providers"
        />
      </div>

      {/* Cost Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <DollarSign className="w-5 h-5" />
            Cost Analysis
          </h2>
          <div className="space-y-6">
            <div>
              <div className="flex items-center justify-between mb-2">
                <p className="text-sm text-gray-600">Actual Cost</p>
                <p className="text-2xl font-bold text-gray-900">
                  ${data.cost_summary.total_cost.toFixed(2)}
                </p>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full"
                  style={{ width: '100%' }}
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <p className="text-sm text-gray-600">Cost Savings</p>
                <p className="text-2xl font-bold text-green-600">
                  ${data.cost_summary.total_savings.toFixed(2)}
                </p>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-green-600 h-2 rounded-full"
                  style={{ width: `${data.cost_summary.savings_percentage}%` }}
                />
              </div>
              <p className="text-xs text-gray-500 mt-1">
                {data.cost_summary.savings_percentage.toFixed(1)}% saved vs GPT-4 baseline
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Document Search (RAG)
          </h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-600">Total Queries</p>
              <p className="text-xl font-bold">{data.rag_analytics.total_queries}</p>
            </div>
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-600">Avg Response Time</p>
              <p className="text-xl font-bold">{data.rag_analytics.avg_latency_ms.toFixed(0)}ms</p>
            </div>
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-600">Avg Results</p>
              <p className="text-xl font-bold">{data.rag_analytics.avg_results.toFixed(1)}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Provider Performance */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">AI Provider Performance</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4">Provider</th>
                <th className="text-left py-3 px-4">Status</th>
                <th className="text-right py-3 px-4">Success Rate</th>
                <th className="text-right py-3 px-4">Avg Response</th>
                <th className="text-right py-3 px-4">Cost/M Tokens</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(data.provider_health).map(([key, provider]: [string, any]) => (
                <tr key={key} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-4 font-medium">{provider.name}</td>
                  <td className="py-3 px-4">
                    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-semibold ${
                      provider.status === 'healthy'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      <span className={`w-2 h-2 rounded-full ${
                        provider.status === 'healthy' ? 'bg-green-600' : 'bg-red-600'
                      }`} />
                      {provider.status}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right">
                    {(provider.success_rate * 100).toFixed(1)}%
                  </td>
                  <td className="py-3 px-4 text-right">
                    {provider.avg_response_time.toFixed(0)}ms
                  </td>
                  <td className="py-3 px-4 text-right">
                    ${provider.cost_per_million.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recommendations */}
      {data.recommendations.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="font-semibold text-blue-900 mb-3">💡 Optimization Tips</h3>
          <ul className="space-y-2">
            {data.recommendations.map((rec, idx) => (
              <li key={idx} className="flex items-start gap-2 text-sm text-blue-800">
                <span className="mt-1">•</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

function MetricCard({
  title,
  value,
  icon,
  subtitle
}: {
  title: string
  value: string
  icon: React.ReactNode
  subtitle: string
}) {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between mb-4">
        {icon}
      </div>
      <h3 className="text-sm text-gray-600 mb-1">{title}</h3>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      <p className="text-xs text-gray-500 mt-1">{subtitle}</p>
    </div>
  )
}
