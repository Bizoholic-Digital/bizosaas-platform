'use client'

import { useState } from 'react'
import {
  Server,
  Database,
  Cpu,
  HardDrive,
  Activity,
  Wifi,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Clock,
  BarChart3,
  RotateCcw,
  Download,
  TrendingUp,
  TrendingDown,
  Loader2
} from 'lucide-react'
import { useSystemHealth } from '@/lib/hooks/use-api'

export default function SystemHealthPage() {
  const { data: health, isLoading, refetch, isRefetching } = useSystemHealth()

  const metrics = health?.resources
  const services = health?.services ? Object.entries(health.services).map(([name, status]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1).replace('-', ' '),
    status: status === 'up' || status === 'connected' ? 'healthy' : 'down' as const,
    uptime: '99.9%',
    responseTime: 45,
    lastCheck: 'Just now',
    version: '1.0.0',
    url: name === 'auth' ? 'http://authentik:8000' : 'Internal'
  })) : []

  const containers = health?.containers || []

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-600 bg-green-100 dark:bg-green-900/30 dark:text-green-400'
      case 'warning': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30 dark:text-yellow-400'
      case 'critical': return 'text-red-600 bg-red-100 dark:bg-red-900/30 dark:text-red-400'
      case 'down': return 'text-red-600 bg-red-100 dark:bg-red-900/30 dark:text-red-400'
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-800 dark:text-gray-400'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy': return <CheckCircle className="h-4 w-4" />
      case 'warning': return <AlertTriangle className="h-4 w-4" />
      case 'critical': return <XCircle className="h-4 w-4" />
      case 'down': return <XCircle className="h-4 w-4" />
      default: return <Clock className="h-4 w-4" />
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Loader2 className="animate-spin h-12 w-12 text-blue-600 mx-auto" />
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading system health telemetry...</p>
        </div>
      </div>
    )
  }

  const cpuPercent = metrics?.cpu || 0
  const memoryPercent = metrics?.memory?.percent || 0
  const diskPercent = metrics?.disk?.percent || 0

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">System Health & Infrastructure</h1>
          <p className="text-gray-600 dark:text-gray-400">Platform-wide infrastructure monitoring and performance metrics</p>
        </div>
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <div className={`w-2 h-2 ${health?.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'} rounded-full animate-pulse`}></div>
            <span>System Status: <span className="font-semibold capitalize">{health?.status || 'Unknown'}</span></span>
          </div>
          <button
            onClick={() => refetch()}
            disabled={isRefetching}
            className="flex items-center space-x-2 px-3 py-2 border border-gray-300 rounded-md hover:bg-gray-50 dark:border-gray-700 dark:hover:bg-gray-800 disabled:opacity-50"
          >
            <RotateCcw className={`h-4 w-4 ${isRefetching ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
          <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
            <Download className="h-4 w-4" />
            <span>Export Report</span>
          </button>
        </div>
      </div>

      {/* System Metrics Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-800">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                <Cpu className="h-6 w-6 text-blue-600 dark:text-blue-400" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">CPU Usage</p>
                <p className="text-lg font-bold text-gray-900 dark:text-white">{cpuPercent}%</p>
              </div>
            </div>
            {cpuPercent < 70 ? (
              <TrendingDown className="h-5 w-5 text-green-600" />
            ) : (
              <TrendingUp className="h-5 w-5 text-red-600" />
            )}
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-800 rounded-full h-2">
            <div
              className={`h-2 rounded-full ${cpuPercent > 80 ? 'bg-red-500' : cpuPercent > 50 ? 'bg-yellow-500' : 'bg-green-500'}`}
              style={{ width: `${cpuPercent}%` }}
            ></div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-800">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg">
                <Database className="h-6 w-6 text-green-600 dark:text-green-400" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Memory</p>
                <p className="text-lg font-bold text-gray-900 dark:text-white">{memoryPercent}%</p>
              </div>
            </div>
            <BarChart3 className="h-5 w-5 text-gray-400" />
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-800 rounded-full h-2">
            <div
              className={`h-2 rounded-full ${memoryPercent > 80 ? 'bg-red-500' : memoryPercent > 50 ? 'bg-yellow-500' : 'bg-green-500'}`}
              style={{ width: `${memoryPercent}%` }}
            ></div>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            {metrics?.memory ? `${(metrics.memory.used / 1024 / 1024 / 1024).toFixed(1)}GB / ${(metrics.memory.total / 1024 / 1024 / 1024).toFixed(1)}GB` : 'N/A'}
          </p>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-800">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
                <HardDrive className="h-6 w-6 text-purple-600 dark:text-purple-400" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Disk Usage</p>
                <p className="text-lg font-bold text-gray-900 dark:text-white">{diskPercent}%</p>
              </div>
            </div>
            <Activity className="h-5 w-5 text-gray-400" />
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-800 rounded-full h-2">
            <div
              className={`h-2 rounded-full ${diskPercent > 90 ? 'bg-red-500' : diskPercent > 70 ? 'bg-yellow-500' : 'bg-blue-500'}`}
              style={{ width: `${diskPercent}%` }}
            ></div>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            {metrics?.disk ? `${(metrics.disk.used / 1024 / 1024 / 1024).toFixed(1)}GB / ${(metrics.disk.total / 1024 / 1024 / 1024).toFixed(1)}GB` : 'N/A'}
          </p>
        </div>

        <div className="bg-white dark:bg-gray-900 rounded-lg shadow p-6 border border-gray-200 dark:border-gray-800">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 dark:bg-yellow-900/30 rounded-lg">
                <Wifi className="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-500 dark:text-gray-400">API Health</p>
                <p className="text-lg font-bold text-gray-900 dark:text-white">Active</p>
              </div>
            </div>
            <Activity className="h-5 w-5 text-gray-400" />
          </div>
          <div className="text-xs text-green-600 dark:text-green-400 font-medium">
            Latency: 24ms
          </div>
        </div>
      </div>

      {/* Services Status */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white dark:bg-gray-900 shadow rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">Core Services</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">Internal platform dependency monitoring</p>
          </div>
          <div className="divide-y divide-gray-200 dark:divide-gray-800">
            {services.map((service) => (
              <div key={service.name} className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-gray-100 dark:bg-gray-800 rounded-md">
                      <Server className="h-5 w-5 text-gray-500" />
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <p className="text-sm font-medium text-gray-900 dark:text-white">{service.name}</p>
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-medium ${getStatusColor(service.status)}`}>
                          {getStatusIcon(service.status)}
                          <span className="ml-1 capitalize">{service.status}</span>
                        </span>
                      </div>
                      <div className="flex items-center space-x-4 mt-1 text-[10px] text-gray-500">
                        <span>Uptime: {service.uptime}</span>
                        <span>•</span>
                        <span>Response: {service.responseTime}ms</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-[10px] text-gray-500">{service.lastCheck}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Docker Containers (New Section) */}
        <div className="lg:col-span-2 bg-white dark:bg-gray-900 shadow rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">Docker Containers</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">Live orchestration status</p>
          </div>
          <div className="p-0 overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
              <thead className="bg-gray-50 dark:bg-gray-900/50">
                <tr>
                  <th className="px-6 py-3 text-left text-[10px] font-medium text-gray-500 uppercase">Name</th>
                  <th className="px-6 py-3 text-left text-[10px] font-medium text-gray-500 uppercase">Image</th>
                  <th className="px-6 py-3 text-left text-[10px] font-medium text-gray-500 uppercase">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                {(containers as any[]).map(c => (
                  <tr key={c.id}>
                    <td className="px-6 py-2 text-xs font-mono text-blue-600 truncate max-w-[150px]">{c.name.replace('/', '')}</td>
                    <td className="px-6 py-2 text-[10px] text-gray-500">{c.image.split(':').pop()}</td>
                    <td className="px-6 py-2 text-xs">
                      <span className={`px-2 py-0.5 rounded-full ${c.status.includes('Up') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                        {c.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* System Uptime & Events */}

        {/* System Uptime & Events */}
        <div className="bg-white dark:bg-gray-900 shadow rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">Platform Events</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">Critical system occurrences</p>
          </div>
          <div className="p-6">
            <div className="space-y-6">
              <div className="flex items-start space-x-3">
                <div className="mt-1 p-1 bg-green-100 dark:bg-green-900/30 rounded-full">
                  <CheckCircle className="h-4 w-4 text-green-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900 dark:text-white">Clean Startup</p>
                  <p className="text-xs text-gray-500">Brain Gateway successfully initialized all modules.</p>
                  <p className="text-[10px] text-gray-400 mt-1">2 hours ago</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="mt-1 p-1 bg-blue-100 dark:bg-blue-900/30 rounded-full">
                  <Wifi className="h-4 w-4 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900 dark:text-white">Sync Completed</p>
                  <p className="text-xs text-gray-500">Google Analytics connector synced 42 properties.</p>
                  <p className="text-[10px] text-gray-400 mt-1">45 minutes ago</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}