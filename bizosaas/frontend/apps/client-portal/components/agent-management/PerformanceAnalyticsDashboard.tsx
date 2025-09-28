'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { 
  BarChart3,
  TrendingUp,
  TrendingDown,
  Activity,
  Clock,
  CheckCircle,
  XCircle,
  Target,
  Zap,
  Users,
  Calendar,
  Download,
  RefreshCw,
  AlertTriangle,
  Award,
  Brain,
  Cpu,
  Database,
  Globe,
  Gauge,
  LineChart,
  PieChart,
  Filter
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  LineChart as RechartsLineChart, 
  Line, 
  XAxis, 
  YAxis, 
  Tooltip, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  PieChart as RechartsPieChart, 
  Pie, 
  Cell,
  RadialBarChart,
  RadialBar,
  Legend,
  ComposedChart
} from 'recharts';

// Performance analytics interfaces
interface AgentPerformanceMetrics {
  agentId: string;
  agentName: string;
  domain: string;
  
  // Task execution metrics
  tasksCompleted: number;
  tasksInProgress: number;
  tasksFailed: number;
  averageTaskDuration: number;
  successRate: number;
  
  // Efficiency metrics
  efficiency: number; // tasks completed per hour
  throughput: number; // requests processed per minute
  errorRate: number;
  
  // Resource utilization
  cpuUtilization: number;
  memoryUtilization: number;
  responseTime: number;
  
  // Time-based performance
  uptime: number; // percentage
  availability: number; // percentage
  
  // Business impact
  costSavings: number; // USD
  revenueGenerated: number; // USD
  customerSatisfaction: number; // score out of 10
  
  // Comparative metrics
  performanceScore: number; // 0-100
  rankingPosition: number;
  improvementTrend: 'up' | 'down' | 'stable';
}

interface DomainPerformance {
  domain: string;
  totalAgents: number;
  activeAgents: number;
  
  // Aggregate metrics
  totalTasksCompleted: number;
  averageSuccessRate: number;
  averageResponseTime: number;
  totalCostSavings: number;
  
  // Performance trends
  weeklyGrowth: number;
  monthlyGrowth: number;
  quarterlyGrowth: number;
  
  // Health indicators
  healthScore: number;
  alertsCount: number;
  criticalIssues: number;
}

interface TimeSeriesData {
  timestamp: string;
  tasksCompleted: number;
  successRate: number;
  responseTime: number;
  errorRate: number;
  cpuUsage: number;
  memoryUsage: number;
  throughput: number;
}

// Mock data generation
const generateTimeSeriesData = (days: number = 30): TimeSeriesData[] => {
  const data: TimeSeriesData[] = [];
  const now = new Date();
  
  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
    data.push({
      timestamp: date.toISOString().split('T')[0],
      tasksCompleted: Math.floor(Math.random() * 500 + 300),
      successRate: Math.random() * 10 + 90,
      responseTime: Math.random() * 200 + 100,
      errorRate: Math.random() * 5,
      cpuUsage: Math.random() * 30 + 40,
      memoryUsage: Math.random() * 25 + 50,
      throughput: Math.random() * 50 + 25
    });
  }
  
  return data;
};

const mockAgentMetrics: AgentPerformanceMetrics[] = [
  {
    agentId: 'lead-scoring',
    agentName: 'Lead Scoring Agent',
    domain: 'CRM',
    tasksCompleted: 2847,
    tasksInProgress: 12,
    tasksFailed: 28,
    averageTaskDuration: 4.2,
    successRate: 96.8,
    efficiency: 42.5,
    throughput: 15.2,
    errorRate: 1.2,
    cpuUtilization: 45,
    memoryUtilization: 62,
    responseTime: 89,
    uptime: 99.7,
    availability: 99.9,
    costSavings: 12500,
    revenueGenerated: 45000,
    customerSatisfaction: 8.9,
    performanceScore: 94,
    rankingPosition: 1,
    improvementTrend: 'up'
  },
  {
    agentId: 'content-creation',
    agentName: 'Content Creation Agent',
    domain: 'CMS',
    tasksCompleted: 1234,
    tasksInProgress: 3,
    tasksFailed: 67,
    averageTaskDuration: 12.5,
    successRate: 93.4,
    efficiency: 18.7,
    throughput: 8.5,
    errorRate: 4.2,
    cpuUtilization: 67,
    memoryUtilization: 89,
    responseTime: 234,
    uptime: 98.2,
    availability: 99.1,
    costSavings: 8900,
    revenueGenerated: 28000,
    customerSatisfaction: 8.1,
    performanceScore: 87,
    rankingPosition: 3,
    improvementTrend: 'stable'
  },
  {
    agentId: 'product-recommendation',
    agentName: 'Product Recommendation Agent',
    domain: 'E-commerce',
    tasksCompleted: 5642,
    tasksInProgress: 8,
    tasksFailed: 128,
    averageTaskDuration: 2.1,
    successRate: 92.3,
    efficiency: 65.8,
    throughput: 32.1,
    errorRate: 2.8,
    cpuUtilization: 58,
    memoryUtilization: 71,
    responseTime: 156,
    uptime: 99.1,
    availability: 99.5,
    costSavings: 18600,
    revenueGenerated: 87500,
    customerSatisfaction: 9.2,
    performanceScore: 91,
    rankingPosition: 2,
    improvementTrend: 'up'
  },
  {
    agentId: 'payment-processing',
    agentName: 'Payment Processing Agent',
    domain: 'Billing',
    tasksCompleted: 8923,
    tasksInProgress: 5,
    tasksFailed: 12,
    averageTaskDuration: 1.8,
    successRate: 99.9,
    efficiency: 89.4,
    throughput: 48.7,
    errorRate: 0.1,
    cpuUtilization: 28,
    memoryUtilization: 34,
    responseTime: 45,
    uptime: 99.9,
    availability: 100,
    costSavings: 25400,
    revenueGenerated: 156000,
    customerSatisfaction: 9.8,
    performanceScore: 98,
    rankingPosition: 1,
    improvementTrend: 'up'
  }
];

const mockDomainPerformance: DomainPerformance[] = [
  {
    domain: 'CRM',
    totalAgents: 6,
    activeAgents: 6,
    totalTasksCompleted: 12450,
    averageSuccessRate: 94.2,
    averageResponseTime: 145,
    totalCostSavings: 45600,
    weeklyGrowth: 12.5,
    monthlyGrowth: 34.2,
    quarterlyGrowth: 89.7,
    healthScore: 95,
    alertsCount: 2,
    criticalIssues: 0
  },
  {
    domain: 'E-commerce',
    totalAgents: 6,
    activeAgents: 4,
    totalTasksCompleted: 8932,
    averageSuccessRate: 89.4,
    averageResponseTime: 189,
    totalCostSavings: 32100,
    weeklyGrowth: 8.3,
    monthlyGrowth: 22.1,
    quarterlyGrowth: 56.8,
    healthScore: 78,
    alertsCount: 5,
    criticalIssues: 1
  },
  {
    domain: 'Analytics',
    totalAgents: 6,
    activeAgents: 5,
    totalTasksCompleted: 23456,
    averageSuccessRate: 96.1,
    averageResponseTime: 89,
    totalCostSavings: 67800,
    weeklyGrowth: 15.7,
    monthlyGrowth: 41.3,
    quarterlyGrowth: 123.4,
    healthScore: 92,
    alertsCount: 1,
    criticalIssues: 0
  },
  {
    domain: 'Billing',
    totalAgents: 6,
    activeAgents: 6,
    totalTasksCompleted: 34567,
    averageSuccessRate: 99.8,
    averageResponseTime: 67,
    totalCostSavings: 89200,
    weeklyGrowth: 6.2,
    monthlyGrowth: 18.9,
    quarterlyGrowth: 45.6,
    healthScore: 99,
    alertsCount: 0,
    criticalIssues: 0
  }
];

// Performance metric card component
const MetricCard: React.FC<{
  title: string;
  value: number | string;
  unit?: string;
  icon: React.ElementType;
  color: string;
  trend?: 'up' | 'down' | 'stable';
  trendValue?: number;
  format?: 'number' | 'percentage' | 'currency' | 'duration';
}> = ({ title, value, unit, icon: Icon, color, trend, trendValue, format = 'number' }) => {
  const formatValue = (val: number | string) => {
    if (typeof val === 'string') return val;
    
    switch (format) {
      case 'percentage':
        return `${val.toFixed(1)}%`;
      case 'currency':
        return `$${val.toLocaleString()}`;
      case 'duration':
        return `${val.toFixed(1)}${unit || 'm'}`;
      default:
        return val.toLocaleString();
    }
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
          <div className="flex items-center space-x-1">
            {getTrendIcon()}
            {trendValue && (
              <span className={`text-xs ${trend === 'up' ? 'text-green-600' : trend === 'down' ? 'text-red-600' : 'text-gray-600'}`}>
                {trendValue > 0 ? '+' : ''}{trendValue.toFixed(1)}%
              </span>
            )}
          </div>
        </div>
        <div className="mt-2">
          <span className="text-2xl font-bold">{formatValue(value)}</span>
          {unit && format === 'number' && (
            <span className="text-sm text-gray-500 ml-1">{unit}</span>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

// Agent performance comparison chart
const AgentComparisonChart: React.FC<{ agents: AgentPerformanceMetrics[] }> = ({ agents }) => {
  const data = agents.map(agent => ({
    name: agent.agentName.split(' ')[0],
    performance: agent.performanceScore,
    successRate: agent.successRate,
    efficiency: agent.efficiency,
    domain: agent.domain
  }));

  const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#8dd1e1', '#d084d0'];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="performance" fill="#8884d8" name="Performance Score" />
        <Bar dataKey="successRate" fill="#82ca9d" name="Success Rate %" />
      </BarChart>
    </ResponsiveContainer>
  );
};

// Domain performance pie chart
const DomainPerformancePie: React.FC<{ domains: DomainPerformance[] }> = ({ domains }) => {
  const data = domains.map(domain => ({
    name: domain.domain,
    value: domain.totalTasksCompleted,
    healthScore: domain.healthScore
  }));

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <RechartsPieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
      </RechartsPieChart>
    </ResponsiveContainer>
  );
};

// Performance trends chart
const PerformanceTrendsChart: React.FC<{ data: TimeSeriesData[] }> = ({ data }) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <ComposedChart data={data}>
        <XAxis dataKey="timestamp" />
        <YAxis yAxisId="left" />
        <YAxis yAxisId="right" orientation="right" />
        <Tooltip />
        <Area 
          yAxisId="left"
          type="monotone" 
          dataKey="tasksCompleted" 
          fill="#8884d8" 
          fillOpacity={0.6}
          name="Tasks Completed"
        />
        <Line 
          yAxisId="right"
          type="monotone" 
          dataKey="successRate" 
          stroke="#82ca9d" 
          strokeWidth={2}
          name="Success Rate %"
        />
      </ComposedChart>
    </ResponsiveContainer>
  );
};

// Main performance analytics dashboard
export default function PerformanceAnalyticsDashboard() {
  const [timeRange, setTimeRange] = useState<'7d' | '30d' | '90d' | '1y'>('30d');
  const [selectedDomain, setSelectedDomain] = useState<string>('all');
  const [timeSeriesData, setTimeSeriesData] = useState<TimeSeriesData[]>(generateTimeSeriesData(30));
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // Update data when time range changes
  useEffect(() => {
    const days = timeRange === '7d' ? 7 : timeRange === '30d' ? 30 : timeRange === '90d' ? 90 : 365;
    setTimeSeriesData(generateTimeSeriesData(days));
  }, [timeRange]);

  // Filter agents by domain
  const filteredAgents = selectedDomain === 'all' 
    ? mockAgentMetrics 
    : mockAgentMetrics.filter(agent => agent.domain === selectedDomain);

  // Calculate overall metrics
  const overallMetrics = {
    totalAgents: mockAgentMetrics.length,
    totalTasks: mockAgentMetrics.reduce((sum, agent) => sum + agent.tasksCompleted, 0),
    averageSuccessRate: mockAgentMetrics.reduce((sum, agent) => sum + agent.successRate, 0) / mockAgentMetrics.length,
    totalCostSavings: mockAgentMetrics.reduce((sum, agent) => sum + agent.costSavings, 0),
    totalRevenue: mockAgentMetrics.reduce((sum, agent) => sum + agent.revenueGenerated, 0),
    averagePerformanceScore: mockAgentMetrics.reduce((sum, agent) => sum + agent.performanceScore, 0) / mockAgentMetrics.length,
    averageResponseTime: mockAgentMetrics.reduce((sum, agent) => sum + agent.responseTime, 0) / mockAgentMetrics.length,
    totalUptime: mockAgentMetrics.reduce((sum, agent) => sum + agent.uptime, 0) / mockAgentMetrics.length
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold flex items-center">
            <BarChart3 className="w-6 h-6 mr-2" />
            Performance Analytics
          </h2>
          <p className="text-gray-600">Monitor and analyze AI agent performance across the ecosystem</p>
        </div>
        <div className="flex items-center space-x-2">
          <Select value={timeRange} onValueChange={(value) => setTimeRange(value as any)}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7d">Last 7 days</SelectItem>
              <SelectItem value="30d">Last 30 days</SelectItem>
              <SelectItem value="90d">Last 90 days</SelectItem>
              <SelectItem value="1y">Last year</SelectItem>
            </SelectContent>
          </Select>
          <Select value={selectedDomain} onValueChange={setSelectedDomain}>
            <SelectTrigger className="w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Domains</SelectItem>
              <SelectItem value="CRM">CRM</SelectItem>
              <SelectItem value="E-commerce">E-commerce</SelectItem>
              <SelectItem value="Analytics">Analytics</SelectItem>
              <SelectItem value="Billing">Billing</SelectItem>
              <SelectItem value="CMS">CMS</SelectItem>
              <SelectItem value="Integration">Integration</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" size="sm" onClick={() => setLastUpdate(new Date())}>
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
          <Button variant="outline" size="sm">
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* Overall Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
        <MetricCard
          title="Total Agents"
          value={overallMetrics.totalAgents}
          icon={Users}
          color="text-blue-600"
        />
        <MetricCard
          title="Tasks Completed"
          value={overallMetrics.totalTasks}
          icon={CheckCircle}
          color="text-green-600"
          trend="up"
          trendValue={12.5}
        />
        <MetricCard
          title="Success Rate"
          value={overallMetrics.averageSuccessRate}
          icon={Target}
          color="text-purple-600"
          format="percentage"
          trend="up"
          trendValue={2.1}
        />
        <MetricCard
          title="Cost Savings"
          value={overallMetrics.totalCostSavings}
          icon={TrendingUp}
          color="text-emerald-600"
          format="currency"
          trend="up"
          trendValue={18.7}
        />
        <MetricCard
          title="Revenue"
          value={overallMetrics.totalRevenue}
          icon={BarChart3}
          color="text-orange-600"
          format="currency"
          trend="up"
          trendValue={25.3}
        />
        <MetricCard
          title="Performance"
          value={overallMetrics.averagePerformanceScore}
          icon={Award}
          color="text-yellow-600"
          format="number"
          trend="stable"
          trendValue={0.8}
        />
        <MetricCard
          title="Response Time"
          value={overallMetrics.averageResponseTime}
          unit="ms"
          icon={Clock}
          color="text-red-600"
          trend="down"
          trendValue={-5.2}
        />
        <MetricCard
          title="Uptime"
          value={overallMetrics.totalUptime}
          icon={Activity}
          color="text-teal-600"
          format="percentage"
          trend="up"
          trendValue={0.3}
        />
      </div>

      {/* Main Analytics */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="agents">Agent Performance</TabsTrigger>
          <TabsTrigger value="domains">Domain Analysis</TabsTrigger>
          <TabsTrigger value="trends">Trends</TabsTrigger>
          <TabsTrigger value="efficiency">Efficiency</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle>Performance Trends</CardTitle>
                <CardDescription>Tasks completed and success rate over time</CardDescription>
              </CardHeader>
              <CardContent>
                <PerformanceTrendsChart data={timeSeriesData} />
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Domain Task Distribution</CardTitle>
                <CardDescription>Tasks completed by domain</CardDescription>
              </CardHeader>
              <CardContent>
                <DomainPerformancePie domains={mockDomainPerformance} />
              </CardContent>
            </Card>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            {mockDomainPerformance.map((domain) => (
              <Card key={domain.domain}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">{domain.domain} Domain</CardTitle>
                    <Badge variant={domain.healthScore > 90 ? "default" : domain.healthScore > 75 ? "secondary" : "destructive"}>
                      Health: {domain.healthScore}%
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div>
                      <p className="text-gray-500">Active Agents</p>
                      <p className="font-medium">{domain.activeAgents}/{domain.totalAgents}</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Tasks Completed</p>
                      <p className="font-medium">{domain.totalTasksCompleted.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Success Rate</p>
                      <p className="font-medium">{domain.averageSuccessRate.toFixed(1)}%</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Cost Savings</p>
                      <p className="font-medium">${domain.totalCostSavings.toLocaleString()}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between text-xs">
                    <span className="flex items-center">
                      <TrendingUp className="w-3 h-3 mr-1 text-green-500" />
                      Monthly: +{domain.monthlyGrowth.toFixed(1)}%
                    </span>
                    {domain.alertsCount > 0 && (
                      <span className="flex items-center text-orange-600">
                        <AlertTriangle className="w-3 h-3 mr-1" />
                        {domain.alertsCount} alerts
                      </span>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="agents" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Agent Performance Comparison</CardTitle>
              <CardDescription>Performance scores and success rates across agents</CardDescription>
            </CardHeader>
            <CardContent>
              <AgentComparisonChart agents={filteredAgents} />
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {filteredAgents.map((agent) => (
              <Card key={agent.agentId}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="text-lg">{agent.agentName}</CardTitle>
                      <CardDescription>{agent.domain} Domain</CardDescription>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge variant={agent.performanceScore > 90 ? "default" : "secondary"}>
                        Score: {agent.performanceScore}
                      </Badge>
                      <Badge variant="outline">
                        #{agent.rankingPosition}
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-gray-500">Tasks Completed</p>
                      <p className="font-medium">{agent.tasksCompleted.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Success Rate</p>
                      <p className="font-medium">{agent.successRate.toFixed(1)}%</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Avg Duration</p>
                      <p className="font-medium">{agent.averageTaskDuration.toFixed(1)}m</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Response Time</p>
                      <p className="font-medium">{agent.responseTime}ms</p>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span>CPU Usage</span>
                      <span>{agent.cpuUtilization}%</span>
                    </div>
                    <Progress value={agent.cpuUtilization} className="h-2" />
                    
                    <div className="flex justify-between text-xs">
                      <span>Memory Usage</span>
                      <span>{agent.memoryUtilization}%</span>
                    </div>
                    <Progress value={agent.memoryUtilization} className="h-2" />
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-gray-500">Cost Savings</p>
                      <p className="font-medium text-green-600">${agent.costSavings.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Revenue Generated</p>
                      <p className="font-medium text-blue-600">${agent.revenueGenerated.toLocaleString()}</p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <span className="text-xs text-gray-500">Customer Satisfaction:</span>
                      <span className="text-sm font-medium">{agent.customerSatisfaction}/10</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      {agent.improvementTrend === 'up' ? (
                        <TrendingUp className="w-4 h-4 text-green-500" />
                      ) : agent.improvementTrend === 'down' ? (
                        <TrendingDown className="w-4 h-4 text-red-500" />
                      ) : (
                        <Activity className="w-4 h-4 text-gray-400" />
                      )}
                      <span className="text-xs text-gray-500">
                        {agent.improvementTrend === 'up' ? 'Improving' : 
                         agent.improvementTrend === 'down' ? 'Declining' : 'Stable'}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="domains">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle>Domain Health Scores</CardTitle>
                <CardDescription>Overall health metrics by domain</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {mockDomainPerformance.map((domain) => (
                    <div key={domain.domain} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="font-medium">{domain.domain}</span>
                        <span className="text-sm">{domain.healthScore}%</span>
                      </div>
                      <Progress 
                        value={domain.healthScore} 
                        className="h-3" 
                      />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Growth Trends</CardTitle>
                <CardDescription>Performance growth by domain</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={mockDomainPerformance}>
                    <XAxis dataKey="domain" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="weeklyGrowth" fill="#8884d8" name="Weekly %" />
                    <Bar dataKey="monthlyGrowth" fill="#82ca9d" name="Monthly %" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="trends">
          <Card>
            <CardHeader>
              <CardTitle>Historical Performance Trends</CardTitle>
              <CardDescription>Long-term performance analysis and predictions</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium mb-3">Task Completion Trends</h4>
                  <ResponsiveContainer width="100%" height={200}>
                    <RechartsLineChart data={timeSeriesData}>
                      <XAxis dataKey="timestamp" />
                      <YAxis />
                      <Tooltip />
                      <Line 
                        type="monotone" 
                        dataKey="tasksCompleted" 
                        stroke="#8884d8" 
                        strokeWidth={2}
                      />
                    </RechartsLineChart>
                  </ResponsiveContainer>
                </div>
                
                <div>
                  <h4 className="font-medium mb-3">Error Rate Trends</h4>
                  <ResponsiveContainer width="100%" height={200}>
                    <AreaChart data={timeSeriesData}>
                      <XAxis dataKey="timestamp" />
                      <YAxis />
                      <Tooltip />
                      <Area 
                        type="monotone" 
                        dataKey="errorRate" 
                        stroke="#ff7300" 
                        fill="#ff7300" 
                        fillOpacity={0.6}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="efficiency">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle>Efficiency vs Resource Usage</CardTitle>
                <CardDescription>Task efficiency compared to resource consumption</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={filteredAgents}>
                    <XAxis dataKey="agentName" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="efficiency" fill="#8884d8" name="Efficiency (tasks/hour)" />
                    <Bar dataKey="cpuUtilization" fill="#82ca9d" name="CPU Usage %" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>ROI Analysis</CardTitle>
                <CardDescription>Return on investment by agent</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {filteredAgents.map((agent) => {
                    const roi = ((agent.revenueGenerated + agent.costSavings) / 50000) * 100; // Assuming 50k cost
                    return (
                      <div key={agent.agentId} className="space-y-2">
                        <div className="flex justify-between items-center">
                          <span className="font-medium">{agent.agentName}</span>
                          <span className="text-sm font-bold text-green-600">{roi.toFixed(0)}% ROI</span>
                        </div>
                        <div className="text-xs text-gray-500 flex justify-between">
                          <span>Revenue: ${agent.revenueGenerated.toLocaleString()}</span>
                          <span>Savings: ${agent.costSavings.toLocaleString()}</span>
                        </div>
                        <Progress value={Math.min(roi, 100)} className="h-2" />
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}