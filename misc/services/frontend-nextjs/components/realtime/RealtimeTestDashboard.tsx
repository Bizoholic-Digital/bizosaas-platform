/**
 * Real-time Test Dashboard
 * Comprehensive testing component for all real-time analytics functionality
 */

'use client';

import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  BarChart3, 
  Zap, 
  Users, 
  TrendingUp, 
  Bell,
  Wifi,
  RefreshCw,
  Play,
  Pause,
  Square,
  Settings
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { 
  useRealtimeMetrics, 
  useRealtimeNotifications, 
  useConnectionStatus,
  useRealtimePerformance
} from '@/lib/hooks/useRealtime';
import { 
  useBatchedUpdates, 
  useThrottledUpdate, 
  useSmartUpdateScheduler,
  usePerformanceMonitor
} from '@/lib/hooks/usePerformanceOptimization';
import { RealtimeMetricsGrid, RealtimeMetricCard } from './RealtimeMetricCard';
import { RealtimeChart, RealtimeMultiSeriesChart } from './RealtimeChart';
import { RealtimeNotificationBell, RealtimeNotificationCenter } from './RealtimeNotifications';
import { 
  RealtimeConnectionStatus, 
  RealtimeSystemHealth, 
  RealtimePerformanceIndicator,
  RealtimeLiveActivity 
} from './RealtimeStatusIndicator';

interface TestScenario {
  id: string;
  name: string;
  description: string;
  active: boolean;
  config: {
    updateInterval: number;
    dataPoints: number;
    errorRate: number;
    notificationRate: number;
  };
}

export function RealtimeTestDashboard() {
  const [showNotifications, setShowNotifications] = useState(false);
  const [testScenarios, setTestScenarios] = useState<TestScenario[]>([
    {
      id: 'normal',
      name: 'Normal Load',
      description: 'Standard update frequency with minimal errors',
      active: true,
      config: { updateInterval: 5000, dataPoints: 20, errorRate: 0.01, notificationRate: 0.1 }
    },
    {
      id: 'high_frequency',
      name: 'High Frequency',
      description: 'Rapid updates to test performance',
      active: false,
      config: { updateInterval: 1000, dataPoints: 50, errorRate: 0.02, notificationRate: 0.2 }
    },
    {
      id: 'stress_test',
      name: 'Stress Test',
      description: 'Maximum load with frequent updates',
      active: false,
      config: { updateInterval: 100, dataPoints: 100, errorRate: 0.05, notificationRate: 0.5 }
    }
  ]);

  const [simulationRunning, setSimulationRunning] = useState(true);
  const [testMetrics, setTestMetrics] = useState({
    messagesReceived: 0,
    errorsEncountered: 0,
    notificationsSent: 0,
    averageLatency: 0
  });

  // Real-time hooks
  const { isConnected, statusText, timeSinceLastUpdate } = useConnectionStatus();
  const { updateFrequency } = useRealtimePerformance();
  const { notifications, unreadCount } = useRealtimeNotifications();
  const { dashboardMetrics, socialMediaMetrics, lastUpdateTime } = useRealtimeMetrics();

  // Performance monitoring
  const { metrics, startRender, endRender, resetMetrics } = usePerformanceMonitor();

  // Mock data generation
  const [mockData, setMockData] = useState(() => ({
    revenue: Array.from({ length: 20 }, (_, i) => ({
      timestamp: Date.now() - (19 - i) * 60000,
      value: Math.floor(Math.random() * 1000) + 500,
      leads: Math.floor(Math.random() * 50) + 20,
      conversions: Math.floor(Math.random() * 20) + 5
    })),
    systemHealth: [
      { name: 'API Gateway', status: 'healthy', responseTime: 45, uptime: 99.9 },
      { name: 'WebSocket Server', status: 'healthy', responseTime: 25, uptime: 99.8 },
      { name: 'Database', status: 'healthy', responseTime: 80, uptime: 99.95 },
      { name: 'Cache Layer', status: 'healthy', responseTime: 15, uptime: 99.99 }
    ]
  }));

  // Performance optimized update function
  const updateData = useSmartUpdateScheduler(
    (newData: any) => {
      startRender();
      setMockData(prev => ({
        ...prev,
        revenue: [...prev.revenue.slice(1), newData]
      }));
      endRender();
    },
    {
      maxFrequency: 30,
      batchSize: 5,
      adaptiveThrottling: true,
      priorityFunction: (data) => data.priority || 1
    }
  );

  // Throttled metrics update
  const updateMetrics = useThrottledUpdate((metrics: any) => {
    setTestMetrics(prev => ({
      ...prev,
      ...metrics
    }));
  }, 100);

  // Batched notifications
  const addNotifications = useBatchedUpdates((notifications: any[]) => {
    // In a real implementation, this would dispatch to the notification system
    console.log('Batch processed notifications:', notifications.length);
  }, 2000, 10);

  // Simulation effect
  useEffect(() => {
    if (!simulationRunning) return;

    const activeScenario = testScenarios.find(s => s.active);
    if (!activeScenario) return;

    const interval = setInterval(() => {
      // Generate new data point
      const newDataPoint = {
        timestamp: Date.now(),
        value: Math.floor(Math.random() * 1000) + 500,
        leads: Math.floor(Math.random() * 50) + 20,
        conversions: Math.floor(Math.random() * 20) + 5,
        priority: Math.random() > 0.8 ? 2 : 1 // 20% high priority
      };

      updateData.scheduleUpdate(newDataPoint);

      // Update test metrics
      updateMetrics({
        messagesReceived: testMetrics.messagesReceived + 1,
        averageLatency: Math.random() * 100 + 20
      });

      // Simulate errors
      if (Math.random() < activeScenario.config.errorRate) {
        updateMetrics({
          errorsEncountered: testMetrics.errorsEncountered + 1
        });
      }

      // Simulate notifications
      if (Math.random() < activeScenario.config.notificationRate) {
        addNotifications({
          id: `test_${Date.now()}`,
          title: 'Test Notification',
          message: `Generated from ${activeScenario.name} scenario`,
          severity: 'info',
          timestamp: Date.now(),
          category: 'system'
        });
        
        updateMetrics({
          notificationsSent: testMetrics.notificationsSent + 1
        });
      }
    }, activeScenario.config.updateInterval);

    return () => clearInterval(interval);
  }, [simulationRunning, testScenarios, updateData, updateMetrics, addNotifications]);

  const metricsData = [
    {
      id: 'messages',
      title: 'Messages Received',
      value: testMetrics.messagesReceived,
      icon: <Activity className="h-6 w-6" />,
      color: 'blue' as const,
      lastUpdated: Date.now()
    },
    {
      id: 'errors',
      title: 'Errors',
      value: testMetrics.errorsEncountered,
      icon: <Zap className="h-6 w-6" />,
      color: 'red' as const,
      lastUpdated: Date.now()
    },
    {
      id: 'notifications',
      title: 'Notifications',
      value: testMetrics.notificationsSent,
      icon: <Bell className="h-6 w-6" />,
      color: 'purple' as const,
      lastUpdated: Date.now()
    },
    {
      id: 'latency',
      title: 'Avg Latency',
      value: testMetrics.averageLatency,
      icon: <TrendingUp className="h-6 w-6" />,
      color: 'green' as const,
      format: 'number' as const,
      subtitle: 'ms',
      lastUpdated: Date.now()
    }
  ];

  const toggleScenario = (scenarioId: string) => {
    setTestScenarios(prev => prev.map(scenario => ({
      ...scenario,
      active: scenario.id === scenarioId
    })));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Real-time Analytics Test Dashboard</h1>
            <p className="text-sm text-gray-600">Comprehensive testing and performance monitoring</p>
          </div>
          
          <div className="flex items-center space-x-4">
            {/* Simulation Controls */}
            <div className="flex items-center space-x-2 border border-gray-200 rounded-lg p-2">
              <button
                onClick={() => setSimulationRunning(!simulationRunning)}
                className={cn(
                  "p-2 rounded",
                  simulationRunning ? "bg-red-100 text-red-600" : "bg-green-100 text-green-600"
                )}
              >
                {simulationRunning ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
              </button>
              <button
                onClick={() => {
                  setTestMetrics({
                    messagesReceived: 0,
                    errorsEncountered: 0,
                    notificationsSent: 0,
                    averageLatency: 0
                  });
                  resetMetrics();
                }}
                className="p-2 rounded bg-gray-100 text-gray-600"
              >
                <Square className="h-4 w-4" />
              </button>
            </div>

            <RealtimeConnectionStatus showText />
            <RealtimeNotificationBell onClick={() => setShowNotifications(true)} />
          </div>
        </div>
      </header>

      <div className="p-6 space-y-6">
        {/* Test Scenarios */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Test Scenarios</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {testScenarios.map((scenario) => (
              <div
                key={scenario.id}
                className={cn(
                  "p-4 border rounded-lg cursor-pointer transition-all",
                  scenario.active ? "border-blue-500 bg-blue-50" : "border-gray-200 hover:border-gray-300"
                )}
                onClick={() => toggleScenario(scenario.id)}
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium text-gray-900">{scenario.name}</h3>
                  {scenario.active && (
                    <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
                  )}
                </div>
                <p className="text-sm text-gray-600 mb-3">{scenario.description}</p>
                <div className="grid grid-cols-2 gap-2 text-xs text-gray-500">
                  <div>Interval: {scenario.config.updateInterval}ms</div>
                  <div>Points: {scenario.config.dataPoints}</div>
                  <div>Error Rate: {(scenario.config.errorRate * 100).toFixed(1)}%</div>
                  <div>Notifications: {(scenario.config.notificationRate * 100).toFixed(1)}%</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Test Metrics */}
        <RealtimeMetricsGrid 
          metrics={metricsData}
          columns={4}
          isLoading={!simulationRunning}
        />

        {/* Performance Metrics */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Metrics</h3>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Avg Render Time:</span>
                <span className="font-medium">{metrics.averageRenderTime.toFixed(2)}ms</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Max Render Time:</span>
                <span className="font-medium">{metrics.maxRenderTime.toFixed(2)}ms</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Total Renders:</span>
                <span className="font-medium">{metrics.totalRenders}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Dropped Frames:</span>
                <span className={cn(
                  "font-medium",
                  metrics.droppedFrames > 5 ? "text-red-600" : "text-green-600"
                )}>
                  {metrics.droppedFrames}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Memory Usage:</span>
                <span className="font-medium">
                  {(metrics.memoryUsage / 1024 / 1024).toFixed(1)}MB
                </span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Update Statistics</h3>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Update Frequency:</span>
                <span className="font-medium">{updateFrequency.toFixed(2)}/s</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Queue Length:</span>
                <span className="font-medium">{updateData.queueLength}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Throttle Delay:</span>
                <span className="font-medium">{updateData.currentThrottleDelay}ms</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Connection:</span>
                <span className={cn(
                  "font-medium",
                  isConnected ? "text-green-600" : "text-red-600"
                )}>
                  {statusText}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Last Update:</span>
                <span className="font-medium">
                  {timeSinceLastUpdate !== null ? `${timeSinceLastUpdate}s ago` : 'Never'}
                </span>
              </div>
            </div>
          </div>

          <RealtimeSystemHealth
            services={mockData.systemHealth}
            showDetails
          />
        </div>

        {/* Real-time Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <RealtimeChart
            data={mockData.revenue}
            type="line"
            title="Revenue Stream (Real-time)"
            color="#3B82F6"
            height={300}
            isRealtime={simulationRunning}
            formatValue={(value) => `$${value.toFixed(0)}`}
          />

          <RealtimeMultiSeriesChart
            data={mockData.revenue.map(d => ({
              ...d,
              formattedTime: new Date(d.timestamp).toLocaleTimeString('en-US', {
                hour12: false,
                hour: '2-digit',
                minute: '2-digit'
              })
            }))}
            series={[
              { key: 'leads', name: 'Leads', color: '#10B981' },
              { key: 'conversions', name: 'Conversions', color: '#8B5CF6' }
            ]}
            height={300}
            title="Leads vs Conversions"
          />
        </div>

        {/* Live Activity Feed */}
        <div className="bg-white rounded-lg border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">Live Activity Feed</h2>
              <RealtimeLiveActivity 
                isActive={simulationRunning}
                lastActivity={lastUpdateTime}
                activityType="test updates"
              />
            </div>
          </div>
          <div className="p-6">
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {notifications.slice(0, 10).map((notification) => (
                <div key={notification.id} className="flex items-center justify-between text-sm py-2 border-b border-gray-100 last:border-b-0">
                  <div className="flex items-center space-x-3">
                    <div className={cn(
                      "w-2 h-2 rounded-full",
                      notification.severity === 'info' && "bg-blue-500",
                      notification.severity === 'success' && "bg-green-500",
                      notification.severity === 'warning' && "bg-yellow-500",
                      notification.severity === 'error' && "bg-red-500"
                    )} />
                    <span className="text-gray-900">{notification.title}</span>
                    <span className="text-gray-500">{notification.message}</span>
                  </div>
                  <span className="text-gray-400 text-xs">
                    {new Date(notification.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Notification Center */}
      <RealtimeNotificationCenter 
        isOpen={showNotifications} 
        onClose={() => setShowNotifications(false)} 
      />
    </div>
  );
}

export default RealtimeTestDashboard;