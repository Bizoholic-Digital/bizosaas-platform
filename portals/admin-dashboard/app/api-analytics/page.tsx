'use client';
import { TrendingUp, Activity, Clock, AlertCircle, Loader2 } from 'lucide-react'
import { useAPIAnalytics } from '@/lib/hooks/use-api'

export default function APIAnalyticsPage() {
  const { data: metrics, isLoading, error } = useAPIAnalytics()

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Loader2 className="animate-spin h-12 w-12 text-blue-600 mx-auto" />
          <p className="mt-4 text-gray-600">Loading live API analytics...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">API Analytics</h1>
        <p className="text-gray-600">Real-time API usage and performance metrics from Brain Gateway</p>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          <p>Error loading analytics. Please ensure the Brain Gateway metrics endpoint is accessible.</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <TrendingUp className="h-8 w-8 text-blue-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-500">Requests/min</p>
              <p className="text-2xl font-bold text-gray-900">{(metrics?.requests_per_minute || 0).toLocaleString()}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <Clock className="h-8 w-8 text-green-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-500">Avg Response</p>
              <p className="text-2xl font-bold text-gray-900">{metrics?.response_time_avg || 0}ms</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <AlertCircle className="h-8 w-8 text-red-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-500">Error Rate</p>
              <p className="text-2xl font-bold text-gray-900">{metrics?.error_rate || 0}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <Activity className="h-8 w-8 text-purple-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-500">Estimated Load</p>
              <p className="text-2xl font-bold text-gray-900">{(metrics?.active_sessions || 0).toLocaleString()}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Traffic Insights</h3>
        <div className="flex items-center justify-center h-64 text-gray-500 border-2 border-dashed border-gray-100 rounded-lg">
          <div className="text-center">
            <Activity className="h-12 w-12 mx-auto mb-4 text-gray-400" />
            <p>Real-time traffic charts will appear here as platform activity increases.</p>
            <p className="text-xs mt-2 italic text-gray-400">Target metrics: http_request_duration_seconds</p>
          </div>
        </div>
      </div>
    </div>
  )
}