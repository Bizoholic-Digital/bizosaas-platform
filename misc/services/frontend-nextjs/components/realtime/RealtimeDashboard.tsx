/**
 * Real-time Enhanced Dashboard
 * Integrates real-time functionality with existing dashboard components
 */

'use client';

import React, { useState, useEffect } from 'react';
import { 
  Activity,
  BarChart3,
  Bot,
  Building,
  Calendar,
  FileText,
  Globe,
  MessageSquare,
  Settings,
  ShoppingCart,
  TrendingUp,
  Users,
  Zap,
  Bell,
  RefreshCw
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useRealtimeMetrics, useRealtimeConnection } from '@/lib/hooks/useRealtime';
import { RealtimeMetricsGrid, RealtimeMetricCard } from './RealtimeMetricCard';
import { RealtimeChart, RealtimeMultiSeriesChart } from './RealtimeChart';
import { RealtimeNotificationBell, RealtimeNotificationCenter } from './RealtimeNotifications';
import { RealtimeConnectionStatus, RealtimeStatusBar } from './RealtimeStatusIndicator';

interface RealtimeDashboardProps {
  className?: string;
}

export function RealtimeDashboard({ className }: RealtimeDashboardProps) {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [showNotifications, setShowNotifications] = useState(false);
  const [selectedTimeRange, setSelectedTimeRange] = useState('7d');

  const { 
    dashboardMetrics, 
    systemHealthMetrics, 
    aiAgentMetrics,
    isConnected,
    lastUpdateTime 
  } = useRealtimeMetrics();

  const { reconnect } = useRealtimeConnection();

  // Update current time every second
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Generate mock chart data for demonstration
  const [chartData, setChartData] = useState(() => {
    const now = Date.now();
    return Array.from({ length: 20 }, (_, i) => ({
      timestamp: now - (19 - i) * 60000, // Last 20 minutes
      value: Math.floor(Math.random() * 100) + 50,
      revenue: Math.floor(Math.random() * 1000) + 500,
      leads: Math.floor(Math.random() * 20) + 10,
    }));
  });

  // Simulate real-time chart updates
  useEffect(() => {
    if (!isConnected) return;

    const interval = setInterval(() => {
      setChartData(prev => {
        const newPoint = {
          timestamp: Date.now(),
          value: Math.floor(Math.random() * 100) + 50,
          revenue: Math.floor(Math.random() * 1000) + 500,
          leads: Math.floor(Math.random() * 20) + 10,
        };
        return [...prev.slice(1), newPoint];
      });
    }, 5000);

    return () => clearInterval(interval);
  }, [isConnected]);

  // Prepare metrics for display
  const metricsData = [
    {
      id: 'campaigns',
      title: 'Total Campaigns',
      value: dashboardMetrics?.total_campaigns || 24,
      previousValue: dashboardMetrics?.period_comparison?.campaigns?.previous || 18,
      change: dashboardMetrics?.period_comparison?.campaigns?.change || 33.3,
      icon: <MessageSquare className="h-6 w-6" />,
      color: 'blue' as const,
      lastUpdated: lastUpdateTime
    },
    {
      id: 'leads',
      title: 'Active Leads',
      value: dashboardMetrics?.active_leads || 156,
      previousValue: dashboardMetrics?.period_comparison?.leads?.previous || 142,
      change: dashboardMetrics?.period_comparison?.leads?.change || 9.9,
      icon: <Users className="h-6 w-6" />,
      color: 'green' as const,
      lastUpdated: lastUpdateTime
    },
    {
      id: 'revenue',
      title: 'Revenue Generated',
      value: dashboardMetrics?.revenue_generated || 47500,
      previousValue: dashboardMetrics?.period_comparison?.revenue?.previous || 41200,
      change: dashboardMetrics?.period_comparison?.revenue?.change || 15.3,
      icon: <TrendingUp className="h-6 w-6" />,
      color: 'purple' as const,
      format: 'currency' as const,
      lastUpdated: lastUpdateTime
    },
    {
      id: 'efficiency',
      title: 'AI Agent Efficiency',
      value: dashboardMetrics?.ai_agent_efficiency || 89,
      previousValue: dashboardMetrics?.period_comparison?.efficiency?.previous || 82,
      change: dashboardMetrics?.period_comparison?.efficiency?.change || 8.5,
      icon: <Zap className="h-6 w-6" />,
      color: 'yellow' as const,
      format: 'percentage' as const,
      lastUpdated: lastUpdateTime
    }
  ];

  return (
    <div className={cn("min-h-screen bg-gray-50", className)}>
      {/* Navigation Sidebar */}
      <div className="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg border-r border-gray-200">
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-center h-16 px-4 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <Bot className="h-8 w-8 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">BizOSaaS</span>
            </div>
          </div>

          {/* Navigation Menu */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            <a href="/dashboard" className="flex items-center px-3 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-md">
              <BarChart3 className="mr-3 h-5 w-5" />
              Overview
            </a>
            <a href="/dashboard/ai-agents" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Bot className="mr-3 h-5 w-5" />
              AI Agents
            </a>
            <a href="/dashboard/leads" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Users className="mr-3 h-5 w-5" />
              Leads
            </a>
            <a href="/dashboard/customers" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Building className="mr-3 h-5 w-5" />
              Customers
            </a>
            <a href="/dashboard/campaigns" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <MessageSquare className="mr-3 h-5 w-5" />
              Campaigns
            </a>
            <a href="/dashboard/social-media" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Globe className="mr-3 h-5 w-5" />
              Social Media
            </a>
            <a href="/coreldove" target="_blank" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <ShoppingCart className="mr-3 h-5 w-5" />
              Amazon Sourcing
            </a>
            <a href="/dashboard/analytics" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <TrendingUp className="mr-3 h-5 w-5" />
              Analytics
            </a>
            <a href="/dashboard/system" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Activity className="mr-3 h-5 w-5" />
              System Status
            </a>
            <a href="/dashboard/settings" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Settings className="mr-3 h-5 w-5" />
              Settings
            </a>
          </nav>

          {/* Real-time Connection Status */}
          <div className="p-4 border-t border-gray-200">
            <RealtimeConnectionStatus showDetails />
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="pl-64">
        {/* Top Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="px-6 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Dashboard Overview</h1>
                <p className="text-sm text-gray-600">Real-time Autonomous AI Agents Platform Control Center</p>
              </div>
              <div className="flex items-center space-x-4">
                {/* Reconnect Button */}
                {!isConnected && (
                  <button
                    onClick={reconnect}
                    className="flex items-center px-3 py-2 text-sm font-medium text-blue-600 hover:text-blue-700 border border-blue-200 rounded-md hover:bg-blue-50"
                  >
                    <RefreshCw className="mr-2 h-4 w-4" />
                    Reconnect
                  </button>
                )}

                {/* Notifications */}
                <RealtimeNotificationBell 
                  onClick={() => setShowNotifications(true)} 
                />

                {/* Date */}
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Calendar className="h-4 w-4" />
                  <span>{currentTime.toLocaleDateString()}</span>
                </div>

                {/* User Avatar */}
                <div className="h-8 w-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                  A
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="p-6 space-y-6">
          {/* Real-time Metrics Grid */}
          <RealtimeMetricsGrid 
            metrics={metricsData}
            columns={4}
            isLoading={!isConnected}
          />

          {/* Real-time Charts Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Revenue Chart */}
            <RealtimeChart
              data={chartData}
              type="area"
              title="Revenue Over Time"
              color="#3B82F6"
              height={300}
              isRealtime={isConnected}
              formatValue={(value) => `$${(value * 10).toFixed(0)}`}
            />

            {/* Multi-series Chart */}
            <RealtimeMultiSeriesChart
              data={chartData.map(d => ({
                ...d,
                formattedTime: new Date(d.timestamp).toLocaleTimeString('en-US', {
                  hour12: false,
                  hour: '2-digit',
                  minute: '2-digit'
                })
              }))}
              series={[
                { key: 'leads', name: 'Leads', color: '#10B981' },
                { key: 'value', name: 'Conversions', color: '#8B5CF6' }
              ]}
              height={300}
              title="Leads vs Conversions"
            />
          </div>

          {/* AI Agents Status - Real-time */}
          <div className="bg-white rounded-lg shadow border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                  <Bot className="mr-2 h-5 w-5" />
                  AI Agents Status
                  {isConnected && (
                    <div className="ml-3 flex items-center space-x-1">
                      <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                      <span className="text-xs text-green-600 font-medium">Live</span>
                    </div>
                  )}
                </h2>
                <div className="text-sm text-gray-500">
                  {aiAgentMetrics?.active_agents || 0} active • {aiAgentMetrics?.idle_agents || 0} idle
                </div>
              </div>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {(aiAgentMetrics?.agents || [
                  { id: '1', name: 'Campaign Optimizer', type: 'campaign_optimizer', status: 'active', current_task: 'Optimizing Facebook Ads Campaign', efficiency: 89, tasks_completed: 12, last_activity: new Date().toISOString() },
                  { id: '2', name: 'Lead Scorer', type: 'lead_scorer', status: 'busy', current_task: 'Processing new lead batch (25 leads)', efficiency: 95, tasks_completed: 8, last_activity: new Date().toISOString() },
                  { id: '3', name: 'Content Generator', type: 'content_generator', status: 'idle', current_task: null, efficiency: 78, tasks_completed: 5, last_activity: new Date().toISOString() }
                ]).map((agent) => (
                  <div key={agent.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-4">
                      <Bot className="h-6 w-6 text-gray-600" />
                      <div>
                        <h3 className="font-medium text-gray-900">{agent.name}</h3>
                        <p className="text-sm text-gray-600">{agent.current_task || 'No active task'}</p>
                        <div className="flex items-center space-x-4 text-xs text-gray-500 mt-1">
                          <span>Efficiency: {agent.efficiency}%</span>
                          <span>Tasks: {agent.tasks_completed}</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-3">
                      <span className={cn(
                        "px-3 py-1 rounded-full text-xs font-medium border",
                        agent.status === 'active' && "text-green-600 bg-green-50 border-green-200",
                        agent.status === 'busy' && "text-yellow-600 bg-yellow-50 border-yellow-200",
                        agent.status === 'idle' && "text-gray-600 bg-gray-50 border-gray-200"
                      )}>
                        {agent.status.charAt(0).toUpperCase() + agent.status.slice(1)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900">Quick Actions</h2>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button className="flex items-center justify-center p-4 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors">
                  <MessageSquare className="mr-2 h-5 w-5" />
                  Create Campaign
                </button>
                <button className="flex items-center justify-center p-4 bg-green-50 text-green-600 rounded-lg hover:bg-green-100 transition-colors">
                  <Bot className="mr-2 h-5 w-5" />
                  Deploy AI Agent
                </button>
                <button className="flex items-center justify-center p-4 bg-purple-50 text-purple-600 rounded-lg hover:bg-purple-100 transition-colors">
                  <FileText className="mr-2 h-5 w-5" />
                  Generate Report
                </button>
              </div>
            </div>
          </div>
        </main>

        {/* Status Bar */}
        <RealtimeStatusBar />
      </div>

      {/* Notification Center */}
      <RealtimeNotificationCenter 
        isOpen={showNotifications} 
        onClose={() => setShowNotifications(false)} 
      />
    </div>
  );
}

export default RealtimeDashboard;