/**
 * Unified Analytics Dashboard Component for BizOSaaS Platform
 *
 * Provides comprehensive cross-platform analytics visualization with:
 * - Real-time metrics display
 * - AI-powered insights
 * - Predictive analytics
 * - Interactive charts and widgets
 * - Platform-specific views
 * - Subscription tier-based features
 */

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from 'recharts';
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  Users,
  Target,
  Activity,
  Brain,
  Download,
  RefreshCw,
  Filter,
  Calendar,
  AlertTriangle,
  CheckCircle,
  Info,
  Zap,
} from 'lucide-react';

// Types
interface PlatformMetrics {
  platform: string;
  total_revenue: number;
  active_users: number;
  conversion_rate: number;
  engagement_score: number;
  performance_index: number;
  growth_rate: number;
  key_metrics: Record<string, any>;
}

interface CrossPlatformInsight {
  insight_id: string;
  title: string;
  description: string;
  impact_score: number;
  confidence: number;
  affected_platforms: string[];
  recommended_actions: string[];
  priority: 'low' | 'medium' | 'high' | 'critical';
  generated_at: string;
}

interface AnalyticsDashboard {
  dashboard_id: string;
  tenant_id: string;
  generated_at: string;
  time_range: string;
  platform_metrics: Record<string, PlatformMetrics>;
  cross_platform_insights: CrossPlatformInsight[];
  ai_recommendations: string[];
  kpi_summary: Record<string, any>;
  subscription_tier: string;
  custom_widgets: any[];
}

interface PredictiveAnalytics {
  prediction_id: string;
  metric_name: string;
  platform: string;
  forecast_horizon: number;
  predicted_values: Array<{
    date: string;
    value: number;
    confidence: number;
  }>;
  model_accuracy: number;
}

// Platform colors for consistent theming
const PLATFORM_COLORS = {
  bizoholic: '#3B82F6',
  coreldove: '#10B981',
  business_directory: '#F59E0B',
  thrillring: '#8B5CF6',
  quanttrade: '#EF4444',
};

// Priority colors
const PRIORITY_COLORS = {
  low: '#6B7280',
  medium: '#F59E0B',
  high: '#EF4444',
  critical: '#DC2626',
};

const UnifiedAnalyticsDashboard: React.FC = () => {
  // State management
  const [dashboard, setDashboard] = useState<AnalyticsDashboard | null>(null);
  const [predictions, setPredictions] = useState<PredictiveAnalytics[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTimeRange, setSelectedTimeRange] = useState('30d');
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState('overview');
  const [refreshing, setRefreshing] = useState(false);

  // Fetch dashboard data
  const fetchDashboard = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch('/api/analytics/dashboard', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Tenant-ID': 'current-tenant', // In real app, get from auth context
        },
        body: JSON.stringify({
          platforms: selectedPlatforms,
          time_range: selectedTimeRange,
          include_predictions: true,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setDashboard(data.dashboard);

      // Fetch predictions separately
      const predictionsResponse = await fetch('/api/analytics/predictions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Tenant-ID': 'current-tenant',
        },
        body: JSON.stringify({
          platforms: selectedPlatforms,
          time_range: selectedTimeRange,
        }),
      });

      if (predictionsResponse.ok) {
        const predictionsData = await predictionsResponse.json();
        setPredictions(predictionsData.predictions);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, [selectedTimeRange, selectedPlatforms]);

  // Initial load and refresh
  useEffect(() => {
    fetchDashboard();
  }, [fetchDashboard]);

  // Manual refresh
  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchDashboard();
    setRefreshing(false);
  };

  // Export dashboard data
  const handleExport = async (format: string) => {
    try {
      const response = await fetch('/api/analytics/export', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Tenant-ID': 'current-tenant',
        },
        body: JSON.stringify({
          format,
          platforms: selectedPlatforms,
          time_range: selectedTimeRange,
        }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `analytics_${format}_${new Date().toISOString().split('T')[0]}.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      }
    } catch (err) {
      console.error('Export failed:', err);
    }
  };

  // Prepare chart data
  const chartData = useMemo(() => {
    if (!dashboard) return null;

    const platformMetrics = Object.values(dashboard.platform_metrics);

    return {
      revenue: platformMetrics.map(p => ({
        platform: p.platform,
        revenue: p.total_revenue,
        users: p.active_users,
      })),
      engagement: platformMetrics.map(p => ({
        platform: p.platform,
        engagement: p.engagement_score,
        performance: p.performance_index,
        conversion: p.conversion_rate,
      })),
      comparison: platformMetrics.map(p => ({
        platform: p.platform,
        revenue: p.total_revenue,
        engagement: p.engagement_score,
        performance: p.performance_index,
      })),
    };
  }, [dashboard]);

  // Loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <Alert className="m-4">
        <AlertTriangle className="h-4 w-4" />
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  if (!dashboard) {
    return (
      <Alert className="m-4">
        <Info className="h-4 w-4" />
        <AlertTitle>No Data</AlertTitle>
        <AlertDescription>No analytics data available for the selected criteria.</AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="text-gray-500">
            Cross-platform insights powered by AI • Last updated: {new Date(dashboard.generated_at).toLocaleString()}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Select value={selectedTimeRange} onValueChange={setSelectedTimeRange}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select time range" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="24h">Last 24 Hours</SelectItem>
              <SelectItem value="7d">Last 7 Days</SelectItem>
              <SelectItem value="30d">Last 30 Days</SelectItem>
              <SelectItem value="90d">Last 90 Days</SelectItem>
              <SelectItem value="1y">Last Year</SelectItem>
            </SelectContent>
          </Select>

          <Button
            variant="outline"
            size="icon"
            onClick={handleRefresh}
            disabled={refreshing}
          >
            <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
          </Button>

          <Button
            variant="outline"
            onClick={() => handleExport('csv')}
          >
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* KPI Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${dashboard.kpi_summary.total_revenue?.toLocaleString() || '0'}
            </div>
            <p className="text-xs text-muted-foreground">
              Across {dashboard.kpi_summary.active_platforms} platforms
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Engagement</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {dashboard.kpi_summary.avg_engagement_score?.toFixed(1) || '0'}%
            </div>
            <p className="text-xs text-muted-foreground">
              Performance score: {dashboard.kpi_summary.avg_performance_index?.toFixed(1) || '0'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {dashboard.kpi_summary.avg_conversion_rate?.toFixed(2) || '0'}%
            </div>
            <p className="text-xs text-muted-foreground">
              Top platform: {dashboard.kpi_summary.top_performing_platform || 'N/A'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">AI Insights</CardTitle>
            <Brain className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {dashboard.cross_platform_insights.length}
            </div>
            <p className="text-xs text-muted-foreground">
              {dashboard.cross_platform_insights.filter(i => i.priority === 'high' || i.priority === 'critical').length} high priority
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="platforms">Platforms</TabsTrigger>
          <TabsTrigger value="insights">AI Insights</TabsTrigger>
          <TabsTrigger value="predictions">Predictions</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="reports">Reports</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Revenue Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Revenue by Platform</CardTitle>
                <CardDescription>Revenue distribution across all platforms</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={chartData?.revenue}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="platform" />
                    <YAxis />
                    <Tooltip formatter={(value) => [`$${value?.toLocaleString()}`, 'Revenue']} />
                    <Bar dataKey="revenue" fill="#3B82F6" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Engagement Radar Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Platform Performance Matrix</CardTitle>
                <CardDescription>Multi-dimensional performance comparison</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={chartData?.engagement}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="platform" />
                    <PolarRadiusAxis />
                    <Radar
                      name="Engagement"
                      dataKey="engagement"
                      stroke="#10B981"
                      fill="#10B981"
                      fillOpacity={0.3}
                    />
                    <Radar
                      name="Performance"
                      dataKey="performance"
                      stroke="#3B82F6"
                      fill="#3B82F6"
                      fillOpacity={0.3}
                    />
                    <Tooltip />
                    <Legend />
                  </RadarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* AI Recommendations */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="h-5 w-5" />
                AI Recommendations
              </CardTitle>
              <CardDescription>Actionable insights powered by AI analysis</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {dashboard.ai_recommendations.slice(0, 5).map((recommendation, index) => (
                  <div key={index} className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
                    <CheckCircle className="h-5 w-5 text-blue-600 mt-0.5" />
                    <p className="text-sm text-gray-700">{recommendation}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Platforms Tab */}
        <TabsContent value="platforms" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(dashboard.platform_metrics).map(([platform, metrics]) => (
              <Card key={platform}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span className="capitalize">{platform.replace('_', ' ')}</span>
                    <Badge
                      style={{ backgroundColor: PLATFORM_COLORS[platform as keyof typeof PLATFORM_COLORS] }}
                      className="text-white"
                    >
                      {metrics.performance_index.toFixed(1)}
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-500">Revenue</span>
                    <span className="font-medium">${metrics.total_revenue.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-500">Active Users</span>
                    <span className="font-medium">{metrics.active_users.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-500">Conversion Rate</span>
                    <span className="font-medium">{metrics.conversion_rate.toFixed(2)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-500">Engagement</span>
                    <span className="font-medium">{metrics.engagement_score.toFixed(1)}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* AI Insights Tab */}
        <TabsContent value="insights" className="space-y-4">
          <div className="space-y-4">
            {dashboard.cross_platform_insights.map((insight) => (
              <Card key={insight.insight_id}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-lg">{insight.title}</CardTitle>
                      <CardDescription className="mt-1">{insight.description}</CardDescription>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge
                        style={{ backgroundColor: PRIORITY_COLORS[insight.priority] }}
                        className="text-white"
                      >
                        {insight.priority}
                      </Badge>
                      <Badge variant="outline">
                        {(insight.confidence * 100).toFixed(0)}% confidence
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-medium text-sm mb-2">Affected Platforms:</h4>
                      <div className="flex gap-2">
                        {insight.affected_platforms.map((platform) => (
                          <Badge key={platform} variant="secondary">
                            {platform.replace('_', ' ')}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    <div>
                      <h4 className="font-medium text-sm mb-2">Recommended Actions:</h4>
                      <ul className="list-disc list-inside space-y-1">
                        {insight.recommended_actions.map((action, index) => (
                          <li key={index} className="text-sm text-gray-600">{action}</li>
                        ))}
                      </ul>
                    </div>

                    <div className="flex justify-between text-xs text-gray-500">
                      <span>Impact Score: {(insight.impact_score * 100).toFixed(0)}%</span>
                      <span>Generated: {new Date(insight.generated_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Predictions Tab */}
        <TabsContent value="predictions" className="space-y-4">
          {predictions.length > 0 ? (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {predictions.map((prediction) => (
                <Card key={prediction.prediction_id}>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span>{prediction.metric_name}</span>
                      <Badge variant="outline">
                        {(prediction.model_accuracy * 100).toFixed(0)}% accuracy
                      </Badge>
                    </CardTitle>
                    <CardDescription>
                      {prediction.platform && `${prediction.platform} • `}
                      {prediction.forecast_horizon} day forecast
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={200}>
                      <LineChart data={prediction.predicted_values.slice(0, 14)}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis
                          dataKey="date"
                          tickFormatter={(value) => new Date(value).toLocaleDateString()}
                        />
                        <YAxis />
                        <Tooltip
                          labelFormatter={(value) => new Date(value).toLocaleDateString()}
                          formatter={(value) => [value.toFixed(2), 'Predicted Value']}
                        />
                        <Line
                          type="monotone"
                          dataKey="value"
                          stroke="#3B82F6"
                          strokeWidth={2}
                          dot={{ r: 3 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="text-center py-8">
                <Brain className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No Predictions Available</h3>
                <p className="text-gray-500">Predictive analytics requires Professional or higher subscription.</p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Performance Tab */}
        <TabsContent value="performance" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Cross-Platform Performance Comparison</CardTitle>
              <CardDescription>Comprehensive performance metrics across all platforms</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={400}>
                <AreaChart data={chartData?.comparison}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="platform" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Area
                    type="monotone"
                    dataKey="revenue"
                    stackId="1"
                    stroke="#3B82F6"
                    fill="#3B82F6"
                    fillOpacity={0.6}
                  />
                  <Area
                    type="monotone"
                    dataKey="engagement"
                    stackId="2"
                    stroke="#10B981"
                    fill="#10B981"
                    fillOpacity={0.6}
                  />
                  <Area
                    type="monotone"
                    dataKey="performance"
                    stackId="3"
                    stroke="#F59E0B"
                    fill="#F59E0B"
                    fillOpacity={0.6}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Reports Tab */}
        <TabsContent value="reports" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader>
                <CardTitle>Export Options</CardTitle>
                <CardDescription>Download analytics data in various formats</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => handleExport('csv')}
                >
                  <Download className="h-4 w-4 mr-2" />
                  Export as CSV
                </Button>
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => handleExport('excel')}
                >
                  <Download className="h-4 w-4 mr-2" />
                  Export as Excel
                </Button>
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => handleExport('json')}
                >
                  <Download className="h-4 w-4 mr-2" />
                  Export as JSON
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Scheduled Reports</CardTitle>
                <CardDescription>Automated report delivery</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-500 mb-4">
                  Schedule automated reports to be delivered to your email.
                </p>
                <Button className="w-full">
                  <Calendar className="h-4 w-4 mr-2" />
                  Set up Schedule
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Custom Dashboards</CardTitle>
                <CardDescription>Create personalized views</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-500 mb-4">
                  Build custom dashboard layouts with your preferred widgets.
                </p>
                <Button className="w-full">
                  <Filter className="h-4 w-4 mr-2" />
                  Customize Layout
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default UnifiedAnalyticsDashboard;