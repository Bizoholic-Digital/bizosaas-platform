'use client';

import React from 'react';
import {
  Users,
  Building2,
  Activity,
  DollarSign,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  Server,
  Loader2
} from 'lucide-react';
import { PlatformBranding } from '@/components/ui/platform-branding';
import { usePlatformStats } from '@/lib/hooks/use-api';

export default function AdminDashboard() {
  const { data: stats, isLoading, error } = usePlatformStats();

  const metrics = [
    {
      title: 'Total Tenants',
      value: isLoading ? '...' : stats?.tenants?.total?.toLocaleString() || '0',
      change: '+12%',
      changeType: 'positive' as const,
      icon: Building2,
      description: 'Active tenant organizations'
    },
    {
      title: 'Total Users',
      value: isLoading ? '...' : stats?.users?.total?.toLocaleString() || '0',
      change: '+18%',
      changeType: 'positive' as const,
      icon: Users,
      description: 'Registered platform users'
    },
    {
      title: 'System Health',
      value: isLoading ? '...' : '99.9%', // Mock health status for now
      change: '+0.1%',
      changeType: 'positive' as const,
      icon: Activity,
      description: 'Platform uptime'
    }
  ];

  const recentActivities = [
    {
      id: 1,
      type: 'tenant_created',
      message: 'New tenant "Acme Corp" registered',
      timestamp: '2 minutes ago',
      status: 'success'
    },
    {
      id: 2,
      type: 'system_alert',
      message: 'High CPU usage detected on server-03',
      timestamp: '15 minutes ago',
      status: 'warning'
    },
    {
      id: 4,
      type: 'user_suspended',
      message: 'User account suspended for policy violation',
      timestamp: '2 hours ago',
      status: 'error'
    },
    {
      id: 5,
      type: 'agent_deployed',
      message: 'AI Agent "Lead Scorer" deployed successfully',
      timestamp: '3 hours ago',
      status: 'success'
    }
  ];

  const systemStats = [
    { label: 'CPU Usage', value: isLoading ? '...' : `${stats?.system?.cpu_usage || 0}%`, status: (stats?.system?.cpu_usage || 0) > 80 ? 'warning' : 'normal' },
    { label: 'Memory Usage', value: isLoading ? '...' : `${stats?.system?.memory_usage || 0}%`, status: (stats?.system?.memory_usage || 0) > 80 ? 'warning' : 'normal' },
    { label: 'Platform Uptime', value: isLoading ? '...' : `${Math.floor((stats?.system?.uptime_seconds || 0) / 3600)}h ${Math.floor(((stats?.system?.uptime_seconds || 0) % 3600) / 60)}m`, status: 'normal' },
    { label: 'API Requests/min', value: '2,847', status: 'normal' },
    { label: 'Active Sessions', value: '1,234', status: 'normal' },
    { label: 'Database Status', value: 'Healthy', status: 'normal' }
  ];

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'tenant_created':
        return <Building2 className="w-4 h-4" />;
      case 'system_alert':
        return <AlertTriangle className="w-4 h-4" />;
      case 'user_suspended':
        return <Users className="w-4 h-4" />;
      case 'agent_deployed':
        return <Server className="w-4 h-4" />;
      default:
        return <Clock className="w-4 h-4" />;
    }
  };

  const getActivityStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'text-green-600 bg-green-50 dark:text-green-400 dark:bg-green-900/20';
      case 'warning':
        return 'text-yellow-600 bg-yellow-50 dark:text-yellow-400 dark:bg-yellow-900/20';
      case 'error':
        return 'text-red-600 bg-red-50 dark:text-red-400 dark:bg-red-900/20';
      default:
        return 'text-gray-600 bg-gray-50 dark:text-gray-400 dark:bg-gray-900/20';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 dark:bg-gray-900 dark:border-gray-800">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <PlatformBranding platform="BIZOSAAS" size="lg" />
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600 dark:text-gray-400">
                Super Admin Dashboard
              </span>
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-medium">SA</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="p-6">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center text-red-700">
            <AlertTriangle className="w-5 h-5 mr-3" />
            <p className="text-sm font-medium">Failed to load platform statistics. Please ensure the Brain Gateway is accessible.</p>
          </div>
        )}

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {metrics.map((metric, index) => (
            <div key={index} className="metric-card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    {metric.title}
                  </p>
                  <div className="flex items-center">
                    <p className="text-2xl font-bold text-gray-900 dark:text-white mr-2">
                      {metric.value}
                    </p>
                    {isLoading && <Loader2 className="w-4 h-4 animate-spin text-gray-400" />}
                  </div>
                  <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                    {metric.description}
                  </p>
                </div>
                <div className="flex flex-col items-end">
                  <metric.icon className="w-8 h-8 text-blue-600 mb-2" />
                  <span className={`text-sm font-medium ${metric.changeType === 'positive'
                    ? 'text-green-600 dark:text-green-400'
                    : 'text-red-600 dark:text-red-400'
                    }`}>
                    {metric.change}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Recent Activities */}
          <div className="lg:col-span-2">
            <div className="admin-card">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Recent Activities
              </h3>
              <div className="space-y-3">
                {recentActivities.map((activity) => (
                  <div key={activity.id} className="flex items-start space-x-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50">
                    <div className={`p-2 rounded-full ${getActivityStatusColor(activity.status)}`}>
                      {getActivityIcon(activity.type)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 dark:text-white">
                        {activity.message}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        {activity.timestamp}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* System Statistics */}
          <div>
            <div className="admin-card">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                System Statistics
              </h3>
              <div className="space-y-4">
                {systemStats.map((stat, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {stat.label}
                    </span>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm font-medium text-gray-900 dark:text-white">
                        {stat.value}
                      </span>
                      {stat.status === 'normal' ? (
                        <CheckCircle className="w-4 h-4 text-green-500" />
                      ) : (
                        <AlertTriangle className="w-4 h-4 text-yellow-500" />
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="admin-card mt-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Quick Actions
              </h3>
              <div className="space-y-3">
                <a href="/cms" className="block w-full text-left p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20 hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors">
                  <div className="flex items-center space-x-3">
                    <Building2 className="w-5 h-5 text-blue-600" />
                    <span className="text-sm font-medium text-blue-900 dark:text-blue-300">
                      Wagtail CMS Management
                    </span>
                  </div>
                </a>
                <button className="w-full text-left p-3 rounded-lg bg-green-50 dark:bg-green-900/20 hover:bg-green-100 dark:hover:bg-green-900/30 transition-colors">
                  <div className="flex items-center space-x-3">
                    <Server className="w-5 h-5 text-green-600" />
                    <span className="text-sm font-medium text-green-900 dark:text-green-300">
                      Deploy AI Agent
                    </span>
                  </div>
                </button>
                <button className="w-full text-left p-3 rounded-lg bg-purple-50 dark:bg-purple-900/20 hover:bg-purple-100 dark:hover:bg-purple-900/30 transition-colors">
                  <div className="flex items-center space-x-3">
                    <TrendingUp className="w-5 h-5 text-purple-600" />
                    <span className="text-sm font-medium text-purple-900 dark:text-purple-300">
                      View Analytics
                    </span>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}