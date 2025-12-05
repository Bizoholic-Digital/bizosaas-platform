"use client";

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { Skeleton } from '@/components/ui/skeleton';
import { 
  TrendingUp, TrendingDown, DollarSign, Package, ShoppingCart, Eye,
  BarChart3, PieChart, LineChart, Calendar, Download, RefreshCw,
  Brain, Zap, Target, AlertTriangle, CheckCircle, Star, Users,
  ArrowUp, ArrowDown, Activity, Clock, Filter, Share
} from 'lucide-react';

interface AnalyticsData {
  overview: {
    total_revenue: number;
    revenue_change: number;
    total_orders: number;
    orders_change: number;
    conversion_rate: number;
    conversion_change: number;
    average_order_value: number;
    aov_change: number;
    profit_margin: number;
    margin_change: number;
  };
  product_performance: {
    top_performers: Array<{
      id: string;
      title: string;
      sku: string;
      revenue: number;
      orders: number;
      conversion_rate: number;
      profit_margin: number;
      ai_score: number;
    }>;
    categories: Array<{
      name: string;
      revenue: number;
      orders: number;
      growth: number;
    }>;
  };
  ai_insights: {
    optimization_opportunities: Array<{
      type: 'pricing' | 'inventory' | 'marketing' | 'sourcing';
      title: string;
      description: string;
      impact: 'HIGH' | 'MEDIUM' | 'LOW';
      estimated_revenue: number;
    }>;
    market_trends: Array<{
      category: string;
      trend: 'GROWING' | 'STABLE' | 'DECLINING';
      growth_rate: number;
      recommendation: string;
    }>;
    risk_alerts: Array<{
      type: 'inventory' | 'competition' | 'market' | 'supplier';
      severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
      message: string;
      action_required: string;
    }>;
  };
  financial_health: {
    gross_profit: number;
    operating_expenses: number;
    net_profit: number;
    cash_flow: number;
    inventory_value: number;
    inventory_turnover: number;
    customer_acquisition_cost: number;
    customer_lifetime_value: number;
  };
  time_series: {
    daily_revenue: Array<{ date: string; revenue: number; orders: number }>;
    monthly_growth: Array<{ month: string; revenue: number; profit: number }>;
  };
}

export default function AnalyticsPage() {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState('last_30_days');
  const [selectedCategory, setSelectedCategory] = useState('all');

  // Mock data - Replace with actual API call
  useEffect(() => {
    const mockAnalyticsData: AnalyticsData = {
      overview: {
        total_revenue: 145780.50,
        revenue_change: 23.5,
        total_orders: 892,
        orders_change: 18.2,
        conversion_rate: 3.4,
        conversion_change: 0.8,
        average_order_value: 163.45,
        aov_change: 5.2,
        profit_margin: 42.3,
        margin_change: 2.1
      },
      product_performance: {
        top_performers: [
          {
            id: '1',
            title: 'Smart Fitness Tracker with Heart Rate Monitor',
            sku: 'FIT-001',
            revenue: 28450.75,
            orders: 335,
            conversion_rate: 4.2,
            profit_margin: 68.5,
            ai_score: 92
          },
          {
            id: '2',
            title: 'LED Strip Lights Kit with Smart Control',
            sku: 'HOME-002',
            revenue: 18220.60,
            orders: 405,
            conversion_rate: 2.8,
            profit_margin: 75.2,
            ai_score: 78
          },
          {
            id: '3',
            title: 'Wireless Bluetooth Earbuds Pro',
            sku: 'TECH-003',
            revenue: 15680.25,
            orders: 131,
            conversion_rate: 5.1,
            profit_margin: 38.7,
            ai_score: 85
          }
        ],
        categories: [
          { name: 'Fitness', revenue: 45280.75, orders: 456, growth: 28.5 },
          { name: 'Home Decor', revenue: 38420.60, orders: 523, growth: 15.8 },
          { name: 'Electronics', revenue: 32650.25, orders: 287, growth: 31.2 },
          { name: 'Fashion', revenue: 18920.40, orders: 198, growth: -5.3 },
        ]
      },
      ai_insights: {
        optimization_opportunities: [
          {
            type: 'pricing',
            title: 'Dynamic Pricing Optimization',
            description: 'AI analysis suggests price adjustments on 12 products could increase revenue by 18%',
            impact: 'HIGH',
            estimated_revenue: 26400
          },
          {
            type: 'inventory',
            title: 'Inventory Rebalancing',
            description: 'Redistribute stock levels based on demand patterns to reduce stockouts',
            impact: 'MEDIUM',
            estimated_revenue: 15800
          },
          {
            type: 'marketing',
            title: 'Cross-selling Campaigns',
            description: 'Launch targeted cross-sell campaigns for high-performing product combinations',
            impact: 'HIGH',
            estimated_revenue: 22100
          }
        ],
        market_trends: [
          {
            category: 'Fitness',
            trend: 'GROWING',
            growth_rate: 28.5,
            recommendation: 'Increase inventory and expand product range'
          },
          {
            category: 'Electronics',
            trend: 'GROWING',
            growth_rate: 31.2,
            recommendation: 'Focus on premium products with higher margins'
          },
          {
            category: 'Fashion',
            trend: 'DECLINING',
            growth_rate: -5.3,
            recommendation: 'Review product selection and consider exit strategy'
          }
        ],
        risk_alerts: [
          {
            type: 'inventory',
            severity: 'HIGH',
            message: '8 products are approaching stockout levels',
            action_required: 'Place reorders within 3 days'
          },
          {
            type: 'competition',
            severity: 'MEDIUM',
            message: 'Increased competition in LED lighting category',
            action_required: 'Review pricing and differentiation strategy'
          }
        ]
      },
      financial_health: {
        gross_profit: 61650.30,
        operating_expenses: 18495.50,
        net_profit: 43154.80,
        cash_flow: 38920.15,
        inventory_value: 125680.75,
        inventory_turnover: 4.2,
        customer_acquisition_cost: 28.50,
        customer_lifetime_value: 485.60
      },
      time_series: {
        daily_revenue: [
          { date: '2025-01-01', revenue: 4250.75, orders: 28 },
          { date: '2025-01-02', revenue: 3890.40, orders: 24 },
          { date: '2025-01-03', revenue: 5120.80, orders: 32 },
          { date: '2025-01-04', revenue: 4680.25, orders: 29 },
          { date: '2025-01-05', revenue: 5450.60, orders: 35 }
        ],
        monthly_growth: [
          { month: 'Aug', revenue: 95420.50, profit: 38520.75 },
          { month: 'Sep', revenue: 108750.80, profit: 43890.25 },
          { month: 'Oct', revenue: 125680.40, profit: 52145.60 },
          { month: 'Nov', revenue: 138920.75, profit: 58720.80 },
          { month: 'Dec', revenue: 145780.50, profit: 61650.30 }
        ]
      }
    };

    setTimeout(() => {
      setAnalyticsData(mockAnalyticsData);
      setLoading(false);
    }, 1000);
  }, [dateRange]);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  const formatPercentage = (value: number) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(1)}%`;
  };

  const getChangeIcon = (value: number) => {
    return value >= 0 ? (
      <ArrowUp className="w-4 h-4 text-green-500" />
    ) : (
      <ArrowDown className="w-4 h-4 text-red-500" />
    );
  };

  const getChangeColor = (value: number) => {
    return value >= 0 ? 'text-green-600' : 'text-red-600';
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'HIGH': return 'bg-red-100 text-red-800 border-red-200';
      case 'MEDIUM': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'LOW': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'CRITICAL': return 'bg-red-200 text-red-900 border-red-300';
      case 'HIGH': return 'bg-red-100 text-red-800 border-red-200';
      case 'MEDIUM': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'LOW': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'GROWING': return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'DECLINING': return <TrendingDown className="w-4 h-4 text-red-500" />;
      default: return <Activity className="w-4 h-4 text-blue-500" />;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 via-red-50 to-orange-100 p-6">
        <div className="container mx-auto space-y-6">
          <div className="space-y-4">
            <Skeleton className="h-8 w-64" />
            <Skeleton className="h-4 w-96" />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {[...Array(5)].map((_, i) => (
              <Skeleton key={i} className="h-32" />
            ))}
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {[...Array(4)].map((_, i) => (
              <Skeleton key={i} className="h-96" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (!analyticsData) return null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-red-50 to-orange-100">
      <div className="container mx-auto p-6 space-y-8">
        {/* Header */}
        <div className="space-y-4">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Performance Analytics</h1>
              <p className="text-gray-600 mt-1">
                AI-powered business intelligence and performance insights
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Select value={dateRange} onValueChange={setDateRange}>
                <SelectTrigger className="w-40">
                  <Calendar className="w-4 h-4 mr-2" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="last_7_days">Last 7 days</SelectItem>
                  <SelectItem value="last_30_days">Last 30 days</SelectItem>
                  <SelectItem value="last_90_days">Last 90 days</SelectItem>
                  <SelectItem value="last_year">Last year</SelectItem>
                </SelectContent>
              </Select>
              <Button variant="outline">
                <Download className="w-4 h-4 mr-2" />
                Export Report
              </Button>
              <Button variant="outline">
                <RefreshCw className="w-4 h-4 mr-2" />
                Refresh
              </Button>
            </div>
          </div>

          {/* Key Metrics Overview */}
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Revenue</p>
                    <p className="text-2xl font-bold text-green-600">
                      {formatCurrency(analyticsData.overview.total_revenue)}
                    </p>
                    <div className="flex items-center gap-1 mt-1">
                      {getChangeIcon(analyticsData.overview.revenue_change)}
                      <span className={`text-sm ${getChangeColor(analyticsData.overview.revenue_change)}`}>
                        {formatPercentage(analyticsData.overview.revenue_change)}
                      </span>
                    </div>
                  </div>
                  <div className="p-2 bg-green-100 rounded-lg">
                    <DollarSign className="w-6 h-6 text-green-600" />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Orders</p>
                    <p className="text-2xl font-bold text-blue-600">
                      {analyticsData.overview.total_orders.toLocaleString()}
                    </p>
                    <div className="flex items-center gap-1 mt-1">
                      {getChangeIcon(analyticsData.overview.orders_change)}
                      <span className={`text-sm ${getChangeColor(analyticsData.overview.orders_change)}`}>
                        {formatPercentage(analyticsData.overview.orders_change)}
                      </span>
                    </div>
                  </div>
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <ShoppingCart className="w-6 h-6 text-blue-600" />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Conversion Rate</p>
                    <p className="text-2xl font-bold text-purple-600">
                      {analyticsData.overview.conversion_rate}%
                    </p>
                    <div className="flex items-center gap-1 mt-1">
                      {getChangeIcon(analyticsData.overview.conversion_change)}
                      <span className={`text-sm ${getChangeColor(analyticsData.overview.conversion_change)}`}>
                        {formatPercentage(analyticsData.overview.conversion_change)}
                      </span>
                    </div>
                  </div>
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <Target className="w-6 h-6 text-purple-600" />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Avg Order Value</p>
                    <p className="text-2xl font-bold text-orange-600">
                      {formatCurrency(analyticsData.overview.average_order_value)}
                    </p>
                    <div className="flex items-center gap-1 mt-1">
                      {getChangeIcon(analyticsData.overview.aov_change)}
                      <span className={`text-sm ${getChangeColor(analyticsData.overview.aov_change)}`}>
                        {formatPercentage(analyticsData.overview.aov_change)}
                      </span>
                    </div>
                  </div>
                  <div className="p-2 bg-orange-100 rounded-lg">
                    <BarChart3 className="w-6 h-6 text-orange-600" />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Profit Margin</p>
                    <p className="text-2xl font-bold text-pink-600">
                      {analyticsData.overview.profit_margin}%
                    </p>
                    <div className="flex items-center gap-1 mt-1">
                      {getChangeIcon(analyticsData.overview.margin_change)}
                      <span className={`text-sm ${getChangeColor(analyticsData.overview.margin_change)}`}>
                        {formatPercentage(analyticsData.overview.margin_change)}
                      </span>
                    </div>
                  </div>
                  <div className="p-2 bg-pink-100 rounded-lg">
                    <TrendingUp className="w-6 h-6 text-pink-600" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* AI Insights Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Brain className="w-5 h-5 text-purple-500" />
              AI-Powered Insights
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="opportunities" className="space-y-4">
              <TabsList>
                <TabsTrigger value="opportunities">Opportunities</TabsTrigger>
                <TabsTrigger value="trends">Market Trends</TabsTrigger>
                <TabsTrigger value="alerts">Risk Alerts</TabsTrigger>
              </TabsList>

              <TabsContent value="opportunities" className="space-y-4">
                <div className="grid gap-4">
                  {analyticsData.ai_insights.optimization_opportunities.map((opportunity, index) => (
                    <Card key={index} className="border-l-4 border-l-purple-500">
                      <CardContent className="p-4">
                        <div className="flex items-start justify-between">
                          <div className="space-y-2">
                            <div className="flex items-center gap-2">
                              <Zap className="w-4 h-4 text-purple-500" />
                              <h3 className="font-semibold">{opportunity.title}</h3>
                              <Badge className={getImpactColor(opportunity.impact)} variant="outline">
                                {opportunity.impact} IMPACT
                              </Badge>
                            </div>
                            <p className="text-sm text-gray-600">{opportunity.description}</p>
                            <div className="text-sm">
                              <span className="text-gray-500">Potential Revenue:</span>
                              <span className="font-bold text-green-600 ml-2">
                                {formatCurrency(opportunity.estimated_revenue)}
                              </span>
                            </div>
                          </div>
                          <Button size="sm" className="bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600">
                            Implement
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>

              <TabsContent value="trends" className="space-y-4">
                <div className="grid gap-4">
                  {analyticsData.ai_insights.market_trends.map((trend, index) => (
                    <Card key={index}>
                      <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            {getTrendIcon(trend.trend)}
                            <div>
                              <h3 className="font-semibold">{trend.category} Category</h3>
                              <p className="text-sm text-gray-600">{trend.recommendation}</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <div className={`text-lg font-bold ${getChangeColor(trend.growth_rate)}`}>
                              {formatPercentage(trend.growth_rate)}
                            </div>
                            <Badge 
                              className={
                                trend.trend === 'GROWING' ? 'bg-green-100 text-green-800' :
                                trend.trend === 'DECLINING' ? 'bg-red-100 text-red-800' :
                                'bg-blue-100 text-blue-800'
                              }
                              variant="outline"
                            >
                              {trend.trend}
                            </Badge>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>

              <TabsContent value="alerts" className="space-y-4">
                <div className="grid gap-4">
                  {analyticsData.ai_insights.risk_alerts.map((alert, index) => (
                    <Card key={index} className="border-l-4 border-l-red-500">
                      <CardContent className="p-4">
                        <div className="flex items-start justify-between">
                          <div className="space-y-2">
                            <div className="flex items-center gap-2">
                              <AlertTriangle className="w-4 h-4 text-red-500" />
                              <h3 className="font-semibold capitalize">{alert.type} Risk</h3>
                              <Badge className={getSeverityColor(alert.severity)} variant="outline">
                                {alert.severity}
                              </Badge>
                            </div>
                            <p className="text-sm text-gray-900">{alert.message}</p>
                            <p className="text-sm text-gray-600">
                              <strong>Action:</strong> {alert.action_required}
                            </p>
                          </div>
                          <Button size="sm" variant="outline">
                            Take Action
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>

        {/* Performance Analysis */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Top Performing Products */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Star className="w-5 h-5 text-yellow-500" />
                Top Performing Products
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {analyticsData.product_performance.top_performers.map((product, index) => (
                  <div key={product.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="text-lg font-bold text-gray-400">#{index + 1}</span>
                        <h3 className="font-semibold text-sm">{product.title}</h3>
                      </div>
                      <div className="flex items-center gap-4 text-xs text-gray-600">
                        <span>SKU: {product.sku}</span>
                        <span>CVR: {product.conversion_rate}%</span>
                        <span>AI Score: {product.ai_score}</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-bold text-green-600">{formatCurrency(product.revenue)}</div>
                      <div className="text-sm text-gray-600">{product.orders} orders</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Category Performance */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <PieChart className="w-5 h-5 text-blue-500" />
                Category Performance
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {analyticsData.product_performance.categories.map((category, index) => (
                  <div key={index} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="font-medium">{category.name}</span>
                      <div className="flex items-center gap-2">
                        <span className="font-bold">{formatCurrency(category.revenue)}</span>
                        <div className={`flex items-center gap-1 ${getChangeColor(category.growth)}`}>
                          {getChangeIcon(category.growth)}
                          <span className="text-sm">{formatPercentage(category.growth)}</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex justify-between text-sm text-gray-600">
                      <span>{category.orders} orders</span>
                      <Progress value={Math.abs(category.growth)} className="w-24 h-2" />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Financial Health */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <LineChart className="w-5 h-5 text-green-500" />
              Financial Health Dashboard
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">
                  {formatCurrency(analyticsData.financial_health.gross_profit)}
                </div>
                <div className="text-sm text-green-700">Gross Profit</div>
              </div>
              <div className="text-center p-4 bg-red-50 rounded-lg">
                <div className="text-2xl font-bold text-red-600">
                  {formatCurrency(analyticsData.financial_health.operating_expenses)}
                </div>
                <div className="text-sm text-red-700">Operating Expenses</div>
              </div>
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">
                  {formatCurrency(analyticsData.financial_health.net_profit)}
                </div>
                <div className="text-sm text-blue-700">Net Profit</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">
                  {formatCurrency(analyticsData.financial_health.cash_flow)}
                </div>
                <div className="text-sm text-purple-700">Cash Flow</div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
              <div className="space-y-4">
                <h3 className="font-semibold">Inventory Metrics</h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Inventory Value:</span>
                    <span className="font-bold">{formatCurrency(analyticsData.financial_health.inventory_value)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Turnover Rate:</span>
                    <span className="font-bold">{analyticsData.financial_health.inventory_turnover}x</span>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <h3 className="font-semibold">Customer Metrics</h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Acquisition Cost:</span>
                    <span className="font-bold">{formatCurrency(analyticsData.financial_health.customer_acquisition_cost)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Lifetime Value:</span>
                    <span className="font-bold">{formatCurrency(analyticsData.financial_health.customer_lifetime_value)}</span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Revenue Trend Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-orange-500" />
              Revenue Trends
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {/* Monthly Growth */}
              <div>
                <h3 className="font-semibold mb-4">Monthly Performance</h3>
                <div className="grid grid-cols-5 gap-4">
                  {analyticsData.time_series.monthly_growth.map((month, index) => (
                    <div key={index} className="text-center p-4 bg-gray-50 rounded-lg">
                      <div className="text-lg font-bold text-orange-600">
                        {formatCurrency(month.revenue)}
                      </div>
                      <div className="text-sm text-gray-600">{month.month}</div>
                      <div className="text-sm text-green-600 mt-1">
                        Profit: {formatCurrency(month.profit)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Daily Revenue */}
              <div>
                <h3 className="font-semibold mb-4">Recent Daily Performance</h3>
                <div className="grid grid-cols-5 gap-4">
                  {analyticsData.time_series.daily_revenue.map((day, index) => (
                    <div key={index} className="text-center p-3 border rounded-lg">
                      <div className="text-sm font-bold text-blue-600">
                        {formatCurrency(day.revenue)}
                      </div>
                      <div className="text-xs text-gray-600">
                        {new Date(day.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                      </div>
                      <div className="text-xs text-gray-500 mt-1">
                        {day.orders} orders
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Action Items */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-500" />
              Recommended Actions
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-3">
                <h3 className="font-semibold text-green-600">Quick Wins</h3>
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-sm">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span>Implement dynamic pricing on top 5 products</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span>Launch cross-sell campaign for fitness category</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span>Increase inventory for growing categories</span>
                  </div>
                </div>
              </div>
              
              <div className="space-y-3">
                <h3 className="font-semibold text-orange-600">Strategic Actions</h3>
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-sm">
                    <Clock className="w-4 h-4 text-orange-500" />
                    <span>Review and optimize underperforming categories</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Clock className="w-4 h-4 text-orange-500" />
                    <span>Develop supplier diversification strategy</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Clock className="w-4 h-4 text-orange-500" />
                    <span>Implement inventory automation rules</span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}