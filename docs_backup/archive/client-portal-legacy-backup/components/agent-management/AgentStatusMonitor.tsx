'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Activity,
  Zap,
  Cpu,
  Layers,
  HardDrive,
  Network,
  Clock,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Pause,
  Play,
  RotateCcw,
  Calendar,
  BarChart3,
  LineChart as LucideLineChart,
  Gauge,
  Wifi,
  WifiOff,
  Database,
  Server,
  MonitorSpeaker
} from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';

// Real-time metrics interface
interface RealTimeMetrics {
  timestamp: Date;
  cpuUsage: number;
  memoryUsage: number;
  diskUsage: number;
  networkIn: number;
  networkOut: number;
  responseTime: number;
  requestsPerSecond: number;
  errorRate: number;
  successRate: number;
}

// Agent performance data
interface AgentPerformance {
  agentId: string;
  agentName: string;
  status: 'active' | 'idle' | 'error' | 'maintenance';
  uptime: number; // in seconds
  lastActivity: Date;
  metrics: RealTimeMetrics[];
  alerts: Alert[];
  healthScore: number;
  sla: {
    targetUptime: number;
    currentUptime: number;
    targetResponseTime: number;
    currentResponseTime: number;
    targetSuccessRate: number;
    currentSuccessRate: number;
  };
}

// Alert interface
interface Alert {
  id: string;
  type: 'critical' | 'warning' | 'info';
  message: string;
  timestamp: Date;
  acknowledged: boolean;
  agentId: string;
}

// Mock real-time data generator
const generateMockMetrics = (baseMetrics?: RealTimeMetrics): RealTimeMetrics => {
  const now = new Date();
  const variance = 0.1; // 10% variance

  const base = baseMetrics || {
    timestamp: now,
    cpuUsage: 45,
    memoryUsage: 60,
    diskUsage: 30,
    networkIn: 1024,
    networkOut: 512,
    responseTime: 120,
    requestsPerSecond: 25,
    errorRate: 0.5,
    successRate: 99.5
  };

  return {
    timestamp: now,
    cpuUsage: Math.max(0, Math.min(100, base.cpuUsage + (Math.random() - 0.5) * 20)),
    memoryUsage: Math.max(0, Math.min(100, base.memoryUsage + (Math.random() - 0.5) * 15)),
    diskUsage: Math.max(0, Math.min(100, base.diskUsage + (Math.random() - 0.5) * 5)),
    networkIn: Math.max(0, base.networkIn + (Math.random() - 0.5) * 2048),
    networkOut: Math.max(0, base.networkOut + (Math.random() - 0.5) * 1024),
    responseTime: Math.max(10, base.responseTime + (Math.random() - 0.5) * 50),
    requestsPerSecond: Math.max(0, base.requestsPerSecond + (Math.random() - 0.5) * 10),
    errorRate: Math.max(0, Math.min(10, base.errorRate + (Math.random() - 0.5) * 1)),
    successRate: Math.max(85, Math.min(100, base.successRate + (Math.random() - 0.5) * 2))
  };
};

// Mock agent performance data
const createMockAgentPerformance = (agentId: string, agentName: string): AgentPerformance => {
  const metrics: RealTimeMetrics[] = [];
  const now = new Date();

  // Generate last 30 data points (30 minutes of data)
  for (let i = 29; i >= 0; i--) {
    const timestamp = new Date(now.getTime() - i * 60000); // 1 minute intervals
    metrics.push({
      ...generateMockMetrics(),
      timestamp
    });
  }

  const alerts: Alert[] = [
    {
      id: '1',
      type: 'warning',
      message: 'High memory usage detected (85%)',
      timestamp: new Date(now.getTime() - 300000), // 5 minutes ago
      acknowledged: false,
      agentId
    },
    {
      id: '2',
      type: 'info',
      message: 'Successfully processed 1000 tasks',
      timestamp: new Date(now.getTime() - 600000), // 10 minutes ago
      acknowledged: true,
      agentId
    }
  ];

  return {
    agentId,
    agentName,
    status: 'active',
    uptime: 432000, // 5 days in seconds
    lastActivity: now,
    metrics,
    alerts,
    healthScore: 92,
    sla: {
      targetUptime: 99.9,
      currentUptime: 99.7,
      targetResponseTime: 200,
      currentResponseTime: 145,
      targetSuccessRate: 99.0,
      currentSuccessRate: 99.5
    }
  };
};

// Real-time metric card component
const MetricCard: React.FC<{
  title: string;
  value: number;
  unit: string;
  icon: React.ElementType;
  color: string;
  trend?: 'up' | 'down' | 'stable';
  threshold?: { warning: number; critical: number };
}> = ({ title, value, unit, icon: Icon, color, trend, threshold }) => {
  const getStatusColor = () => {
    if (threshold) {
      if (value >= threshold.critical) return 'text-red-600';
      if (value >= threshold.warning) return 'text-yellow-600';
    }
    return color;
  };

  const getTrendIcon = () => {
    switch (trend) {
      case 'up': return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'down': return <TrendingDown className="w-4 h-4 text-red-500" />;
      default: return null;
    }
  };

  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Icon className={`w-5 h-5 ${color}`} />
            <span className="text-sm font-medium">{title}</span>
          </div>
          {getTrendIcon()}
        </div>
        <div className="mt-2">
          <span className={`text-2xl font-bold ${getStatusColor()}`}>
            {typeof value === 'number' ? value.toFixed(1) : value}
          </span>
          <span className="text-sm text-gray-500 ml-1">{unit}</span>
        </div>
        {threshold && (
          <div className="mt-2">
            <Progress
              value={value}
              className="h-2"
              max={100}
            />
          </div>
        )}
      </CardContent>
    </Card>
  );
};

// Alert component
const AlertItem: React.FC<{
  alert: Alert;
  onAcknowledge: (alertId: string) => void;
}> = ({ alert, onAcknowledge }) => {
  const getAlertIcon = () => {
    switch (alert.type) {
      case 'critical': return <XCircle className="w-5 h-5 text-red-500" />;
      case 'warning': return <AlertTriangle className="w-5 h-5 text-yellow-500" />;
      case 'info': return <CheckCircle className="w-5 h-5 text-blue-500" />;
    }
  };

  const getAlertColor = () => {
    switch (alert.type) {
      case 'critical': return 'border-red-200 bg-red-50';
      case 'warning': return 'border-yellow-200 bg-yellow-50';
      case 'info': return 'border-blue-200 bg-blue-50';
    }
  };

  return (
    <div className={`p-3 border rounded-lg ${getAlertColor()}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          {getAlertIcon()}
          <span className="text-sm font-medium">{alert.message}</span>
        </div>
        {!alert.acknowledged && (
          <Button
            size="sm"
            variant="outline"
            onClick={() => onAcknowledge(alert.id)}
          >
            Acknowledge
          </Button>
        )}
      </div>
      <p className="text-xs text-gray-500 mt-1">
        {alert.timestamp.toLocaleTimeString()}
      </p>
    </div>
  );
};

// SLA monitoring component
const SLAMonitor: React.FC<{ sla: AgentPerformance['sla'] }> = ({ sla }) => {
  const slaItems = [
    {
      name: 'Uptime',
      target: sla.targetUptime,
      current: sla.currentUptime,
      unit: '%',
      color: 'text-green-600'
    },
    {
      name: 'Response Time',
      target: sla.targetResponseTime,
      current: sla.currentResponseTime,
      unit: 'ms',
      color: 'text-blue-600',
      inverse: true // Lower is better
    },
    {
      name: 'Success Rate',
      target: sla.targetSuccessRate,
      current: sla.currentSuccessRate,
      unit: '%',
      color: 'text-purple-600'
    }
  ];

  return (
    <div className="space-y-4">
      {slaItems.map((item) => {
        const isOnTarget = item.inverse
          ? item.current <= item.target
          : item.current >= item.target;

        return (
          <div key={item.name} className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium">{item.name}</span>
              <div className="flex items-center space-x-2">
                <span className={`text-sm ${item.color}`}>
                  {item.current.toFixed(1)}{item.unit}
                </span>
                <span className="text-xs text-gray-500">
                  / {item.target.toFixed(1)}{item.unit}
                </span>
                {isOnTarget ? (
                  <CheckCircle className="w-4 h-4 text-green-500" />
                ) : (
                  <XCircle className="w-4 h-4 text-red-500" />
                )}
              </div>
            </div>
            <Progress
              value={item.inverse
                ? Math.max(0, 100 - (item.current / item.target) * 100)
                : (item.current / item.target) * 100
              }
              className="h-2"
            />
          </div>
        );
      })}
    </div>
  );
};

// Main agent status monitor component
export default function AgentStatusMonitor({ agentId }: { agentId: string }) {
  const [agentPerformance, setAgentPerformance] = useState<AgentPerformance>(
    createMockAgentPerformance(agentId, 'Lead Scoring Agent')
  );
  const [isRealTime, setIsRealTime] = useState(true);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  // Real-time data updates
  useEffect(() => {
    if (isRealTime) {
      intervalRef.current = setInterval(() => {
        setAgentPerformance(prev => {
          const newMetric = generateMockMetrics(prev.metrics[prev.metrics.length - 1]);
          const newMetrics = [...prev.metrics.slice(1), newMetric];

          return {
            ...prev,
            metrics: newMetrics,
            lastActivity: new Date(),
            healthScore: Math.max(70, Math.min(100, prev.healthScore + (Math.random() - 0.5) * 4))
          };
        });
      }, 5000); // Update every 5 seconds
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isRealTime]);

  const handleAcknowledgeAlert = (alertId: string) => {
    setAgentPerformance(prev => ({
      ...prev,
      alerts: prev.alerts.map(alert =>
        alert.id === alertId ? { ...alert, acknowledged: true } : alert
      )
    }));
  };

  const toggleRealTime = () => {
    setIsRealTime(!isRealTime);
  };

  const latestMetrics = agentPerformance.metrics[agentPerformance.metrics.length - 1];
  const previousMetrics = agentPerformance.metrics[agentPerformance.metrics.length - 2];

  // Calculate trends
  const getTrend = (current: number, previous: number): 'up' | 'down' | 'stable' => {
    const diff = current - previous;
    if (Math.abs(diff) < 0.1) return 'stable';
    return diff > 0 ? 'up' : 'down';
  };

  const unacknowledgedAlerts = agentPerformance.alerts.filter(alert => !alert.acknowledged);

  // Prepare chart data
  const chartData = agentPerformance.metrics.slice(-20).map(metric => ({
    time: metric.timestamp.toLocaleTimeString(),
    cpu: metric.cpuUsage,
    memory: metric.memoryUsage,
    responseTime: metric.responseTime,
    successRate: metric.successRate,
    errorRate: metric.errorRate,
    requests: metric.requestsPerSecond
  }));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold flex items-center">
            <Activity className="w-6 h-6 mr-2" />
            {agentPerformance.agentName} - Real-time Monitoring
          </h2>
          <p className="text-gray-600">
            Status: <Badge variant="outline" className="bg-green-100 text-green-800">
              {agentPerformance.status}
            </Badge>
            | Health Score: <span className="font-semibold">{agentPerformance.healthScore}%</span>
            | Uptime: <span className="font-semibold">
              {Math.floor(agentPerformance.uptime / 86400)}d {Math.floor((agentPerformance.uptime % 86400) / 3600)}h
            </span>
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button
            variant={isRealTime ? "default" : "outline"}
            size="sm"
            onClick={toggleRealTime}
          >
            {isRealTime ? <Pause className="w-4 h-4 mr-2" /> : <Play className="w-4 h-4 mr-2" />}
            {isRealTime ? 'Pause' : 'Resume'} Real-time
          </Button>
          <div className="flex items-center space-x-1">
            {isRealTime ? <Wifi className="w-4 h-4 text-green-500" /> : <WifiOff className="w-4 h-4 text-gray-400" />}
            <span className="text-xs text-gray-500">
              {isRealTime ? 'Live' : 'Paused'}
            </span>
          </div>
        </div>
      </div>

      {/* Alerts */}
      {unacknowledgedAlerts.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center">
              <AlertTriangle className="w-5 h-5 mr-2 text-yellow-500" />
              Active Alerts ({unacknowledgedAlerts.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {unacknowledgedAlerts.map(alert => (
              <AlertItem
                key={alert.id}
                alert={alert}
                onAcknowledge={handleAcknowledgeAlert}
              />
            ))}
          </CardContent>
        </Card>
      )}

      {/* Real-time Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <MetricCard
          title="CPU Usage"
          value={latestMetrics.cpuUsage}
          unit="%"
          icon={Cpu}
          color="text-blue-600"
          trend={previousMetrics ? getTrend(latestMetrics.cpuUsage, previousMetrics.cpuUsage) : 'stable'}
          threshold={{ warning: 70, critical: 85 }}
        />
        <MetricCard
          title="Memory"
          value={latestMetrics.memoryUsage}
          unit="%"
          icon={Layers}
          color="text-green-600"
          trend={previousMetrics ? getTrend(latestMetrics.memoryUsage, previousMetrics.memoryUsage) : 'stable'}
          threshold={{ warning: 75, critical: 90 }}
        />
        <MetricCard
          title="Disk Usage"
          value={latestMetrics.diskUsage}
          unit="%"
          icon={HardDrive}
          color="text-purple-600"
          trend={previousMetrics ? getTrend(latestMetrics.diskUsage, previousMetrics.diskUsage) : 'stable'}
          threshold={{ warning: 80, critical: 95 }}
        />
        <MetricCard
          title="Response Time"
          value={latestMetrics.responseTime}
          unit="ms"
          icon={Clock}
          color="text-orange-600"
          trend={previousMetrics ? getTrend(latestMetrics.responseTime, previousMetrics.responseTime) : 'stable'}
        />
        <MetricCard
          title="Requests/sec"
          value={latestMetrics.requestsPerSecond}
          unit="req/s"
          icon={Zap}
          color="text-yellow-600"
          trend={previousMetrics ? getTrend(latestMetrics.requestsPerSecond, previousMetrics.requestsPerSecond) : 'stable'}
        />
        <MetricCard
          title="Success Rate"
          value={latestMetrics.successRate}
          unit="%"
          icon={CheckCircle}
          color="text-green-600"
          trend={previousMetrics ? getTrend(latestMetrics.successRate, previousMetrics.successRate) : 'stable'}
        />
      </div>

      {/* Charts and Analytics */}
      <Tabs defaultValue="performance" className="space-y-4">
        <TabsList>
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="resources">Resources</TabsTrigger>
          <TabsTrigger value="sla">SLA Monitoring</TabsTrigger>
          <TabsTrigger value="network">Network</TabsTrigger>
        </TabsList>

        <TabsContent value="performance" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Response Time Trend</CardTitle>
                <CardDescription>Last 20 measurements</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <LineChart data={chartData}>
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="responseTime"
                      stroke="#f59e0b"
                      strokeWidth={2}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Success vs Error Rate</CardTitle>
                <CardDescription>Real-time performance tracking</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <AreaChart data={chartData}>
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Area
                      type="monotone"
                      dataKey="successRate"
                      stackId="1"
                      stroke="#10b981"
                      fill="#10b981"
                      fillOpacity={0.6}
                    />
                    <Area
                      type="monotone"
                      dataKey="errorRate"
                      stackId="2"
                      stroke="#ef4444"
                      fill="#ef4444"
                      fillOpacity={0.6}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="resources" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Resource Utilization</CardTitle>
                <CardDescription>CPU and Memory usage over time</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <LineChart data={chartData}>
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="cpu"
                      stroke="#3b82f6"
                      strokeWidth={2}
                      name="CPU %"
                    />
                    <Line
                      type="monotone"
                      dataKey="memory"
                      stroke="#10b981"
                      strokeWidth={2}
                      name="Memory %"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Request Load</CardTitle>
                <CardDescription>Requests per second</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={chartData.slice(-10)}>
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="requests" fill="#8b5cf6" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="sla">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">SLA Compliance</CardTitle>
              <CardDescription>Service Level Agreement monitoring</CardDescription>
            </CardHeader>
            <CardContent>
              <SLAMonitor sla={agentPerformance.sla} />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="network">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Network Activity</CardTitle>
              <CardDescription>Incoming and outgoing network traffic</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4 mb-4">
                <MetricCard
                  title="Network In"
                  value={latestMetrics.networkIn / 1024}
                  unit="KB/s"
                  icon={Network}
                  color="text-blue-600"
                />
                <MetricCard
                  title="Network Out"
                  value={latestMetrics.networkOut / 1024}
                  unit="KB/s"
                  icon={Network}
                  color="text-green-600"
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}