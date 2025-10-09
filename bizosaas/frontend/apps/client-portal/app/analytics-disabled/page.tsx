'use client';

import React, { useState, useEffect } from 'react';
import { 
  BarChart3, TrendingUp, TrendingDown, Eye, Users, 
  DollarSign, Target, Brain, Zap, RefreshCw, 
  Calendar, Filter, Download, Settings,
  Activity, Lightbulb, AlertTriangle, CheckCircle,
  ArrowUp, ArrowDown, ArrowRight
} from 'lucide-react';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import DashboardLayout from '../../components/ui/dashboard-layout';

interface AIInsight {
  id: string;
  type: 'opportunity' | 'warning' | 'recommendation' | 'trend';
  title: string;
  description: string;
  impact: 'high' | 'medium' | 'low';
  confidence: number;
  createdAt: string;
}

interface MetricCard {
  title: string;
  value: string;
  change: number;
  changeType: 'increase' | 'decrease' | 'neutral';
  icon: React.ReactNode;
  color: string;
}

const AnalyticsPage = () => {
  const [insights, setInsights] = useState<AIInsight[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState('30d');
  const [selectedMetrics, setSelectedMetrics] = useState<string[]>(['all']);

  // Mock data for charts
  const trafficData = [
    { date: '2024-01-01', visitors: 1200, pageviews: 3400, sessions: 1800 },
    { date: '2024-01-02', visitors: 1400, pageviews: 3800, sessions: 2100 },
    { date: '2024-01-03', visitors: 1100, pageviews: 3200, sessions: 1600 },
    { date: '2024-01-04', visitors: 1600, pageviews: 4200, sessions: 2400 },
    { date: '2024-01-05', visitors: 1800, pageviews: 4800, sessions: 2700 },
    { date: '2024-01-06', visitors: 1500, pageviews: 4100, sessions: 2200 },
    { date: '2024-01-07', visitors: 1700, pageviews: 4500, sessions: 2500 },
  ];

  const conversionData = [
    { name: 'Website', visitors: 5000, leads: 250, conversions: 25 },
    { name: 'Social Media', visitors: 3200, leads: 180, conversions: 32 },
    { name: 'Email', visitors: 1800, leads: 160, conversions: 45 },
    { name: 'Paid Ads', visitors: 2500, leads: 200, conversions: 38 },
    { name: 'Referral', visitors: 1200, leads: 90, conversions: 28 },
  ];

  const revenueData = [
    { month: 'Jan', revenue: 15000, target: 18000 },
    { month: 'Feb', revenue: 18500, target: 20000 },
    { month: 'Mar', revenue: 22000, target: 22000 },
    { month: 'Apr', revenue: 25500, target: 24000 },
    { month: 'May', revenue: 28000, target: 26000 },
    { month: 'Jun', revenue: 31200, target: 28000 },
  ];

  const channelDistribution = [
    { name: 'Organic Search', value: 35, color: '#3B82F6' },
    { name: 'Direct', value: 25, color: '#10B981' },
    { name: 'Social Media', value: 20, color: '#F59E0B' },
    { name: 'Paid Ads', value: 15, color: '#EF4444' },
    { name: 'Email', value: 5, color: '#8B5CF6' },
  ];

  // Mock AI insights
  const mockInsights: AIInsight[] = [
    {
      id: '1',
      type: 'opportunity',
      title: 'High-Converting Keywords Identified',
      description: 'Our AI analysis found 12 new keywords with high conversion potential. Implementing these could increase traffic by 25%.',
      impact: 'high',
      confidence: 0.92,
      createdAt: '2024-01-15T10:00:00Z'
    },
    {
      id: '2',
      type: 'warning',
      title: 'Bounce Rate Spike Detected',
      description: 'Mobile bounce rate increased by 15% this week. This may be due to slow loading times on mobile devices.',
      impact: 'medium',
      confidence: 0.87,
      createdAt: '2024-01-15T09:30:00Z'
    },
    {
      id: '3',
      type: 'recommendation',
      title: 'Optimize Email Campaign Timing',
      description: 'Analysis shows your audience is most engaged on Tuesday and Thursday between 10-11 AM. Consider scheduling campaigns accordingly.',
      impact: 'medium',
      confidence: 0.78,
      createdAt: '2024-01-14T16:20:00Z'
    },
    {
      id: '4',
      type: 'trend',
      title: 'Social Media Growth Trend',
      description: 'Instagram engagement has grown 45% over the past month, significantly outperforming other channels.',
      impact: 'high',
      confidence: 0.94,
      createdAt: '2024-01-14T14:15:00Z'
    }
  ];

  const metricCards: MetricCard[] = [
    {
      title: 'Total Visitors',
      value: '12.5K',
      change: 12.5,
      changeType: 'increase',
      icon: <Users className="w-6 h-6" />,
      color: 'text-blue-600'
    },
    {
      title: 'Conversion Rate',
      value: '3.2%',
      change: 0.8,
      changeType: 'increase',
      icon: <Target className="w-6 h-6" />,
      color: 'text-green-600'
    },
    {
      title: 'Revenue',
      value: '$31.2K',
      change: 8.3,
      changeType: 'increase',
      icon: <DollarSign className="w-6 h-6" />,
      color: 'text-purple-600'
    },
    {
      title: 'Bounce Rate',
      value: '42.1%',
      change: 5.2,
      changeType: 'decrease',
      icon: <Activity className="w-6 h-6" />,
      color: 'text-orange-600'
    }
  ];

  useEffect(() => {
    // Simulate API call
    const fetchInsights = async () => {
      try {
        setLoading(true);
        // Replace with actual API call to /api/brain/agents/analytics
        await new Promise(resolve => setTimeout(resolve, 1500));
        setInsights(mockInsights);
      } catch (err) {
        setError('Failed to fetch analytics insights');
        console.error('Error fetching insights:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchInsights();
  }, [timeRange]);

  const getInsightIcon = (type: string) => {
    const icons = {
      opportunity: <Lightbulb className="w-5 h-5 text-yellow-600" />,
      warning: <AlertTriangle className="w-5 h-5 text-red-600" />,
      recommendation: <Brain className="w-5 h-5 text-blue-600" />,
      trend: <TrendingUp className="w-5 h-5 text-green-600" />
    };
    return icons[type as keyof typeof icons] || <Brain className="w-5 h-5" />;
  };

  const getInsightColor = (type: string) => {
    const colors = {
      opportunity: 'bg-yellow-50 border-yellow-200',
      warning: 'bg-red-50 border-red-200',
      recommendation: 'bg-blue-50 border-blue-200',
      trend: 'bg-green-50 border-green-200'
    };
    return colors[type as keyof typeof colors] || 'bg-gray-50 border-gray-200';
  };

  const getChangeIcon = (changeType: string) => {
    switch (changeType) {
      case 'increase':
        return <ArrowUp className="w-4 h-4 text-green-600" />;
      case 'decrease':
        return <ArrowDown className="w-4 h-4 text-red-600" />;
      default:
        return <ArrowRight className="w-4 h-4 text-gray-600" />;
    }
  };

  const getChangeColor = (changeType: string) => {
    switch (changeType) {
      case 'increase':
        return 'text-green-600';
      case 'decrease':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  if (loading) {
    return (
      <DashboardLayout title="AI Analytics" description="AI-powered insights and business analytics">
        <div className="p-6">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/4 mb-6"></div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-24 bg-gray-200 dark:bg-gray-700 rounded"></div>
              ))}
            </div>
            <div className="space-y-6">
              <div className="h-64 bg-gray-200 dark:bg-gray-700 rounded"></div>
              <div className="h-48 bg-gray-200 dark:bg-gray-700 rounded"></div>
            </div>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="AI Analytics" description="AI-powered insights and business analytics">
      <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI Analytics</h1>
          <p className="text-gray-600 mt-1">AI-powered insights and business analytics</p>
        </div>
        <div className="flex gap-3">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
            <option value="1y">Last year</option>
          </select>
          <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
            <Download className="w-4 h-4" />
            Export
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            <RefreshCw className="w-4 h-4" />
            Refresh Insights
          </button>
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {metricCards.map((metric, index) => (
          <div key={index} className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-4">
              <div className={`p-2 rounded-lg bg-gray-100 ${metric.color}`}>
                {metric.icon}
              </div>
              <div className={`flex items-center gap-1 text-sm ${getChangeColor(metric.changeType)}`}>
                {getChangeIcon(metric.changeType)}
                <span>{Math.abs(metric.change)}%</span>
              </div>
            </div>
            <div>
              <p className="text-gray-600 text-sm">{metric.title}</p>
              <p className="text-2xl font-bold text-gray-900">{metric.value}</p>
            </div>
          </div>
        ))}
      </div>

      {/* AI Insights Section */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center gap-2">
            <Brain className="w-6 h-6 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900">AI Insights</h2>
            <Zap className="w-5 h-5 text-yellow-500" />
          </div>
        </div>
        <div className="p-6 space-y-4">
          {insights.map((insight) => (
            <div key={insight.id} className={`p-4 rounded-lg border ${getInsightColor(insight.type)}`}>
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3 flex-1">
                  {getInsightIcon(insight.type)}
                  <div>
                    <h3 className="font-medium text-gray-900 mb-1">{insight.title}</h3>
                    <p className="text-sm text-gray-600 mb-2">{insight.description}</p>
                    <div className="flex items-center gap-4 text-xs text-gray-500">
                      <span>Impact: {insight.impact}</span>
                      <span>Confidence: {(insight.confidence * 100).toFixed(0)}%</span>
                      <span>{new Date(insight.createdAt).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
                <button className="text-gray-400 hover:text-gray-600">
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Traffic Trends */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Traffic Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trafficData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" tickFormatter={(date) => new Date(date).toLocaleDateString()} />
              <YAxis />
              <Tooltip labelFormatter={(date) => new Date(date).toLocaleDateString()} />
              <Legend />
              <Line type="monotone" dataKey="visitors" stroke="#3B82F6" strokeWidth={2} />
              <Line type="monotone" dataKey="sessions" stroke="#10B981" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Channel Distribution */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Traffic Sources</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={channelDistribution}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={120}
                paddingAngle={5}
                dataKey="value"
              >
                {channelDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${value}%`, 'Share']} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Revenue vs Target */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Revenue vs Target</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={revenueData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis tickFormatter={(value) => `$${value/1000}K`} />
              <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, '']} />
              <Legend />
              <Bar dataKey="revenue" fill="#3B82F6" />
              <Bar dataKey="target" fill="#E5E7EB" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Conversion Funnel */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Conversion Funnel</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={conversionData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Area type="monotone" dataKey="visitors" stackId="1" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.6} />
              <Area type="monotone" dataKey="leads" stackId="1" stroke="#10B981" fill="#10B981" fillOpacity={0.6} />
              <Area type="monotone" dataKey="conversions" stackId="1" stroke="#F59E0B" fill="#F59E0B" fillOpacity={0.6} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

        {error && (
          <div className="bg-red-50 dark:bg-red-900 border border-red-200 dark:border-red-700 rounded-lg p-4">
            <div className="flex items-center">
              <AlertTriangle className="w-5 h-5 text-red-600 mr-2" />
              <span className="text-red-700 dark:text-red-300">{error}</span>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default AnalyticsPage;