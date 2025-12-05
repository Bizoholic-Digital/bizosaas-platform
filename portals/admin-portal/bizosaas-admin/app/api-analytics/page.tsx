'use client'

import { useState, useEffect } from 'react'
import { TrendingUp, Activity, Clock, AlertCircle } from 'lucide-react'

interface APIMetrics {
  requests_per_minute: number
  response_time_avg: number
  error_rate: number
  active_sessions: number
}

export default function APIAnalyticsPage() {
  const [metrics, setMetrics] = useState<APIMetrics>({
    requests_per_minute: 2847,
    response_time_avg: 234,
    error_rate: 0.2,
    active_sessions: 1234
  })

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">API Analytics</h1>
        <p className="text-gray-600">API usage and performance metrics dashboard</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <TrendingUp className="h-8 w-8 text-blue-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-500">Requests/min</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.requests_per_minute.toLocaleString()}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <Clock className="h-8 w-8 text-green-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-500">Avg Response</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.response_time_avg}ms</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <AlertCircle className="h-8 w-8 text-red-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-500">Error Rate</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.error_rate}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <Activity className="h-8 w-8 text-purple-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-500">Active Sessions</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.active_sessions.toLocaleString()}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">API Performance Monitoring</h3>
        <div className="flex items-center justify-center h-64 text-gray-500">
          <div className="text-center">
            <Activity className="h-12 w-12 mx-auto mb-4 text-gray-400" />
            <p>API analytics charts will be displayed here</p>
          </div>
        </div>
      </div>
    </div>
  )
}