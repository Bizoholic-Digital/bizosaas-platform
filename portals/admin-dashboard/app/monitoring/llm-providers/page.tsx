'use client'

import { useEffect, useState } from 'react'
import { Activity, TrendingUp, DollarSign, Zap, AlertTriangle, CheckCircle, XCircle, Server } from 'lucide-react'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

interface ProviderHealth {
  name: string
  status: 'healthy' | 'unhealthy'
  success_rate: number
  avg_response_time: number
  consecutive_failures: number
  cost_per_million: number
  capabilities: string[]
}

interface MonitoringDashboard {
  provider_health: Record<string, ProviderHealth>
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

export default function LLMProvidersMonitoring() {
  const [dashboard, setDashboard] = useState<MonitoringDashboard | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [autoRefresh, setAutoRefresh] = useState(true)

  useEffect(() => {
    fetchDashboardData()

    if (autoRefresh) {
      const interval = setInterval(fetchDashboardData, 30000) // Refresh every 30s
      return () => clearInterval(interval)
    }
  }, [autoRefresh])

  const fetchDashboardData = async () => {
    try {
      const response = await fetch(`${BRAIN_API_URL}/api/brain/llm/monitoring/dashboard`)

      if (!response.ok) {
        throw new Error('Failed to fetch monitoring data')
      }

      const data = await response.json()
      setDashboard(data)
      setError(null)
    } catch (err) {
      console.error('Monitoring fetch error:', err)
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <Activity className="w-12 h-12 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">Loading monitoring data...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center text-red-600">
          <AlertTriangle className="w-12 h-12 mx-auto mb-4" />
          <p className="font-semibold">Error loading monitoring data</p>
          <p className="text-sm">{error}</p>
          <button
            onClick={fetchDashboardData}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  if (!dashboard) return null

  const healthyProviders = Object.values(dashboard.provider_health).filter(
    p => p.status === 'healthy'
  ).length
  const totalProviders = Object.keys(dashboard.provider_health).length

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">LLM Provider Monitoring</h1>
            <p className="text-gray-600 mt-1">Real-time monitoring of all LLM providers and routing</p>
          </div>
          <div className="flex items-center gap-4">
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={autoRefresh}
                onChange={(e) => setAutoRefresh(e.target.checked)}
                className="rounded"
              />
              Auto-refresh (30s)
            </label>
            <button
              onClick={fetchDashboardData}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 flex items-center gap-2"
            >
              <Activity className="w-4 h-4" />
              Refresh Now
            </button>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <MetricCard
          title="Provider Health"
          value={`${healthyProviders}/${totalProviders}`}
          subtitle="Healthy Providers"
          icon={<Server className="w-8 h-8 text-green-600" />}
          trend={healthyProviders === totalProviders ? 'up' : 'down'}
        />
        <MetricCard
          title="Success Rate"
          value={`${(dashboard.routing_analytics.success_rate * 100).toFixed(1)}%`}
          subtitle="Overall Success"
          icon={<CheckCircle className="w-8 h-8 text-blue-600" />}
          trend="up"
        />
        <MetricCard
          title="Cost Savings"
          value={`$${dashboard.cost_summary.total_savings.toFixed(2)}`}
          subtitle={`${dashboard.cost_summary.savings_percentage.toFixed(0)}% saved vs GPT-4`}
          icon={<DollarSign className="w-8 h-8 text-purple-600" />}
          trend="up"
        />
        <MetricCard
          title="Avg Response Time"
          value={`${dashboard.routing_analytics.avg_latency_ms.toFixed(0)}ms`}
          subtitle="Routing Latency"
          icon={<Zap className="w-8 h-8 text-yellow-600" />}
          trend={dashboard.routing_analytics.avg_latency_ms < 1000 ? 'up' : 'down'}
        />
      </div>

      {/* Provider Health Status */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Server className="w-5 h-5" />
          Provider Health Status
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {Object.entries(dashboard.provider_health).map(([key, provider]) => (
            <ProviderHealthCard key={key} provider={provider} />
          ))}
        </div>
      </div>

      {/* RAG Analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">RAG Performance</h2>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-600">Total Queries</p>
              <p className="text-2xl font-bold">{dashboard.rag_analytics.total_queries}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Average Latency</p>
              <p className="text-2xl font-bold">{dashboard.rag_analytics.avg_latency_ms.toFixed(0)}ms</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Average Results</p>
              <p className="text-2xl font-bold">{dashboard.rag_analytics.avg_results.toFixed(1)}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">Cost Summary</h2>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-600">Total Cost (24h)</p>
              <p className="text-2xl font-bold text-red-600">
                ${dashboard.cost_summary.total_cost.toFixed(2)}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Total Savings (24h)</p>
              <p className="text-2xl font-bold text-green-600">
                ${dashboard.cost_summary.total_savings.toFixed(2)}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Savings Percentage</p>
              <p className="text-2xl font-bold text-green-600">
                {dashboard.cost_summary.savings_percentage.toFixed(1)}%
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      {dashboard.recommendations.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-yellow-600" />
            System Recommendations
          </h2>
          <ul className="space-y-2">
            {dashboard.recommendations.map((rec, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-yellow-600 mt-1">•</span>
                <span className="text-gray-700">{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* External Monitoring Links */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <MonitoringLink
          title="Grafana Dashboards"
          url="http://localhost:3030"
          description="Detailed metrics and visualizations"
        />
        <MonitoringLink
          title="Prometheus Metrics"
          url="http://localhost:9090"
          description="Raw metrics and queries"
        />
        <MonitoringLink
          title="Kibana (Elasticsearch)"
          url="http://localhost:5601"
          description="Document search and analytics"
        />
      </div>
    </div>
  )
}

// ==================== COMPONENTS ====================

function MetricCard({
  title,
  value,
  subtitle,
  icon,
  trend
}: {
  title: string
  value: string
  subtitle: string
  icon: React.ReactNode
  trend: 'up' | 'down'
}) {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between mb-4">
        {icon}
        <div className={`text-sm font-semibold ${trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
          {trend === 'up' ? '↑' : '↓'}
        </div>
      </div>
      <h3 className="text-sm text-gray-600 mb-1">{title}</h3>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      <p className="text-xs text-gray-500 mt-1">{subtitle}</p>
    </div>
  )
}

function ProviderHealthCard({ provider }: { provider: ProviderHealth }) {
  const isHealthy = provider.status === 'healthy'

  return (
    <div className={`border rounded-lg p-4 ${isHealthy ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          {isHealthy ? (
            <CheckCircle className="w-5 h-5 text-green-600" />
          ) : (
            <XCircle className="w-5 h-5 text-red-600" />
          )}
          <h3 className="font-semibold text-gray-900">{provider.name}</h3>
        </div>
        <span className={`text-xs px-2 py-1 rounded ${isHealthy ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'}`}>
          {provider.status}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div>
          <p className="text-gray-600">Success Rate</p>
          <p className="font-semibold">{(provider.success_rate * 100).toFixed(1)}%</p>
        </div>
        <div>
          <p className="text-gray-600">Avg Response</p>
          <p className="font-semibold">{provider.avg_response_time.toFixed(0)}ms</p>
        </div>
        <div>
          <p className="text-gray-600">Cost/M Tokens</p>
          <p className="font-semibold">${provider.cost_per_million.toFixed(2)}</p>
        </div>
        <div>
          <p className="text-gray-600">Failures</p>
          <p className={`font-semibold ${provider.consecutive_failures > 2 ? 'text-red-600' : 'text-gray-900'}`}>
            {provider.consecutive_failures}
          </p>
        </div>
      </div>

      <div className="mt-3">
        <p className="text-xs text-gray-600 mb-1">Capabilities:</p>
        <div className="flex flex-wrap gap-1">
          {provider.capabilities.map((cap) => (
            <span key={cap} className="text-xs px-2 py-0.5 bg-white rounded border border-gray-200">
              {cap}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}

function MonitoringLink({
  title,
  url,
  description
}: {
  title: string
  url: string
  description: string
}) {
  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className="block bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow"
    >
      <h3 className="font-semibold text-gray-900 mb-1">{title}</h3>
      <p className="text-sm text-gray-600 mb-3">{description}</p>
      <div className="flex items-center gap-2 text-blue-600 text-sm font-semibold">
        Open Dashboard
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
        </svg>
      </div>
    </a>
  )
}
