"use client";

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  Package,
  ShoppingCart,
  Eye,
  AlertTriangle,
  CheckCircle,
  Clock,
  ArrowRight,
  Zap,
  Target,
  BarChart3,
  Search,
  Bot,
  Users,
  Star
} from 'lucide-react';

export default function CoreLDoveAdminDashboard() {
  const [timeRange, setTimeRange] = useState('today');

  // Mock data for the dashboard
  const quickStats = {
    revenue: { value: 5840.75, change: 12.5, trend: 'up' },
    orders: { value: 47, change: 8.2, trend: 'up' },
    conversion: { value: 3.4, change: 0.8, trend: 'up' },
    profit: { value: 2456.30, change: 15.7, trend: 'up' }
  };

  const topProducts = [
    {
      id: 1,
      name: "Smart Fitness Tracker Pro",
      sku: "FIT-001",
      revenue: 1240.50,
      orders: 15,
      stock: 89,
      status: "active"
    },
    {
      id: 2,
      name: "LED Strip Lights Kit",
      sku: "HOME-002",
      revenue: 856.25,
      orders: 19,
      stock: 5,
      status: "low_stock"
    },
    {
      id: 3,
      name: "Wireless Earbuds Pro",
      sku: "TECH-003",
      revenue: 945.75,
      orders: 8,
      stock: 42,
      status: "active"
    }
  ];

  const aiInsights = [
    {
      type: 'opportunity',
      title: 'Price Optimization Available',
      description: '3 products can increase profit by 18% with dynamic pricing',
      impact: 'high',
      value: 840
    },
    {
      type: 'alert',
      title: 'Inventory Alert',
      description: '2 products are approaching stockout levels',
      impact: 'medium',
      value: null
    },
    {
      type: 'trend',
      title: 'Category Growth',
      description: 'Fitness products showing 28% growth trend',
      impact: 'high',
      value: 1250
    }
  ];

  const recentActivity = [
    { type: 'order', message: 'New order #10847 received', time: '2 min ago', status: 'success' },
    { type: 'stock', message: 'LED Strip Lights - Low stock alert', time: '5 min ago', status: 'warning' },
    { type: 'profit', message: 'Fitness Tracker price optimized', time: '12 min ago', status: 'info' },
    { type: 'sync', message: 'Product data synchronized', time: '18 min ago', status: 'success' }
  ];

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    }).format(amount);
  };

  const formatChange = (value: number) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(1)}%`;
  };

  const getChangeColor = (trend: string) => {
    return trend === 'up' ? 'text-green-600' : 'text-red-600';
  };

  const getChangeIcon = (trend: string) => {
    return trend === 'up' ? (
      <TrendingUp className="w-4 h-4 text-green-500" />
    ) : (
      <TrendingDown className="w-4 h-4 text-red-500" />
    );
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'active':
        return <Badge className="bg-green-100 text-green-800">Active</Badge>;
      case 'low_stock':
        return <Badge className="bg-yellow-100 text-yellow-800">Low Stock</Badge>;
      case 'out_of_stock':
        return <Badge className="bg-red-100 text-red-800">Out of Stock</Badge>;
      default:
        return <Badge variant="outline">Unknown</Badge>;
    }
  };

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'opportunity':
        return <Zap className="w-4 h-4 text-green-500" />;
      case 'alert':
        return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
      case 'trend':
        return <TrendingUp className="w-4 h-4 text-blue-500" />;
      default:
        return <Bot className="w-4 h-4 text-gray-500" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-600">Monitor your dropshipping business performance</p>
        </div>
        <div className="flex items-center gap-3">
          <select 
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
          >
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
          </select>
          <Button className="bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600">
            Generate Report
          </Button>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Revenue</p>
                <p className="text-2xl font-bold text-green-600">
                  {formatCurrency(quickStats.revenue.value)}
                </p>
                <div className="flex items-center gap-1 mt-1">
                  {getChangeIcon(quickStats.revenue.trend)}
                  <span className={`text-sm ${getChangeColor(quickStats.revenue.trend)}`}>
                    {formatChange(quickStats.revenue.change)}
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
                <p className="text-sm text-gray-600">Orders</p>
                <p className="text-2xl font-bold text-blue-600">
                  {quickStats.orders.value}
                </p>
                <div className="flex items-center gap-1 mt-1">
                  {getChangeIcon(quickStats.orders.trend)}
                  <span className={`text-sm ${getChangeColor(quickStats.orders.trend)}`}>
                    {formatChange(quickStats.orders.change)}
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
                <p className="text-sm text-gray-600">Conversion</p>
                <p className="text-2xl font-bold text-purple-600">
                  {quickStats.conversion.value}%
                </p>
                <div className="flex items-center gap-1 mt-1">
                  {getChangeIcon(quickStats.conversion.trend)}
                  <span className={`text-sm ${getChangeColor(quickStats.conversion.trend)}`}>
                    {formatChange(quickStats.conversion.change)}
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
                <p className="text-sm text-gray-600">Profit</p>
                <p className="text-2xl font-bold text-orange-600">
                  {formatCurrency(quickStats.profit.value)}
                </p>
                <div className="flex items-center gap-1 mt-1">
                  {getChangeIcon(quickStats.profit.trend)}
                  <span className={`text-sm ${getChangeColor(quickStats.profit.trend)}`}>
                    {formatChange(quickStats.profit.change)}
                  </span>
                </div>
              </div>
              <div className="p-2 bg-orange-100 rounded-lg">
                <TrendingUp className="w-6 h-6 text-orange-600" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* AI Insights */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bot className="w-5 h-5 text-purple-500" />
              AI Insights
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {aiInsights.map((insight, index) => (
                <div key={index} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                  {getInsightIcon(insight.type)}
                  <div className="flex-1">
                    <h3 className="font-medium text-sm">{insight.title}</h3>
                    <p className="text-sm text-gray-600 mt-1">{insight.description}</p>
                    {insight.value && (
                      <p className="text-sm font-medium text-green-600 mt-2">
                        Potential: {formatCurrency(insight.value)}
                      </p>
                    )}
                  </div>
                  <Button size="sm" variant="outline">
                    Act
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Top Products */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Star className="w-5 h-5 text-yellow-500" />
              Top Products Today
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {topProducts.map((product, index) => (
                <div key={product.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="text-lg font-bold text-gray-400">#{index + 1}</span>
                      <div>
                        <h3 className="font-medium text-sm">{product.name}</h3>
                        <p className="text-xs text-gray-500">SKU: {product.sku}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4 mt-2">
                      <span className="text-sm">{formatCurrency(product.revenue)}</span>
                      <span className="text-sm text-gray-600">{product.orders} orders</span>
                      <span className="text-sm text-gray-600">Stock: {product.stock}</span>
                    </div>
                  </div>
                  <div className="text-right">
                    {getStatusBadge(product.status)}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-3">
              <Link href="/coreldove/admin/sourcing">
                <Button variant="outline" className="w-full h-auto p-4 flex-col gap-2">
                  <Search className="w-5 h-5 text-orange-500" />
                  <span className="text-sm">Source Products</span>
                </Button>
              </Link>
              <Link href="/coreldove/admin/analytics">
                <Button variant="outline" className="w-full h-auto p-4 flex-col gap-2">
                  <BarChart3 className="w-5 h-5 text-blue-500" />
                  <span className="text-sm">View Analytics</span>
                </Button>
              </Link>
              <Link href="/coreldove/admin/inventory">
                <Button variant="outline" className="w-full h-auto p-4 flex-col gap-2">
                  <Package className="w-5 h-5 text-green-500" />
                  <span className="text-sm">Manage Inventory</span>
                </Button>
              </Link>
              <Link href="/coreldove/admin/orders">
                <Button variant="outline" className="w-full h-auto p-4 flex-col gap-2">
                  <ShoppingCart className="w-5 h-5 text-purple-500" />
                  <span className="text-sm">Process Orders</span>
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="w-5 h-5 text-gray-500" />
              Recent Activity
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {recentActivity.map((activity, index) => (
                <div key={index} className="flex items-start gap-3 p-2">
                  <div className={`w-2 h-2 rounded-full mt-2 ${
                    activity.status === 'success' ? 'bg-green-500' :
                    activity.status === 'warning' ? 'bg-yellow-500' :
                    activity.status === 'info' ? 'bg-blue-500' : 'bg-gray-500'
                  }`} />
                  <div className="flex-1">
                    <p className="text-sm text-gray-900">{activity.message}</p>
                    <p className="text-xs text-gray-500">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}