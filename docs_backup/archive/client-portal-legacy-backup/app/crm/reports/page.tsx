'use client';

import React, { useState, useEffect } from 'react';
import { 
  BarChart3, Plus, Search, Filter, Download, RefreshCw, 
  TrendingUp, TrendingDown, Users, Target, DollarSign,
  Calendar, Eye, Share2, FileText, PieChart, Activity,
  Mail, Phone, Globe, MousePointer, ShoppingCart
} from 'lucide-react';
import DashboardLayout from '../../../components/ui/dashboard-layout';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart as RechartsPieChart, Cell } from 'recharts';

const ReportsPage = () => {
  const [loading, setLoading] = useState(true);
  const [reports, setReports] = useState<any[]>([]);
  const [analytics, setAnalytics] = useState<any>(null);
  const [selectedPeriod, setSelectedPeriod] = useState('30d');

  useEffect(() => {
    const fetchReports = async () => {
      try {
        setLoading(true);
        // Mock API call - replace with actual Brain Hub API calls
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setReports([
          {
            id: '1',
            name: 'Monthly Sales Report',
            type: 'sales',
            description: 'Comprehensive sales performance analysis',
            lastGenerated: '2024-09-24T09:00:00Z',
            frequency: 'monthly',
            status: 'ready',
            size: '2.4 MB',
            downloads: 47
          },
          {
            id: '2',
            name: 'Lead Generation Analysis',
            type: 'leads',
            description: 'Lead quality and conversion tracking',
            lastGenerated: '2024-09-24T08:30:00Z',
            frequency: 'weekly',
            status: 'ready',
            size: '1.8 MB',
            downloads: 23
          },
          {
            id: '3',
            name: 'Campaign Performance Report',
            type: 'campaigns',
            description: 'ROI and engagement metrics for all campaigns',
            lastGenerated: '2024-09-23T16:45:00Z',
            frequency: 'weekly',
            status: 'generating',
            size: null,
            downloads: 31
          },
          {
            id: '4',
            name: 'Customer Behavior Analysis',
            type: 'analytics',
            description: 'User journey and interaction patterns',
            lastGenerated: '2024-09-22T14:20:00Z',
            frequency: 'daily',
            status: 'ready',
            size: '3.7 MB',
            downloads: 89
          }
        ]);

        setAnalytics({
          overview: {
            totalLeads: 1247,
            leadsGrowth: 15.3,
            totalRevenue: 425000,
            revenueGrowth: 22.8,
            conversionRate: 18.5,
            conversionGrowth: -2.1,
            avgDealSize: 3400,
            dealSizeGrowth: 8.7
          },
          leadsOverTime: [
            { month: 'Jan', leads: 85, revenue: 28500 },
            { month: 'Feb', leads: 92, revenue: 31200 },
            { month: 'Mar', leads: 78, revenue: 26500 },
            { month: 'Apr', leads: 105, revenue: 35700 },
            { month: 'May', leads: 118, revenue: 40100 },
            { month: 'Jun', leads: 134, revenue: 45500 },
            { month: 'Jul', leads: 142, revenue: 48200 },
            { month: 'Aug', leads: 156, revenue: 53000 },
            { month: 'Sep', leads: 178, revenue: 60400 }
          ],
          sourceBreakdown: [
            { name: 'Website', value: 35, color: '#3B82F6' },
            { name: 'Google Ads', value: 28, color: '#10B981' },
            { name: 'Social Media', value: 18, color: '#8B5CF6' },
            { name: 'Referrals', value: 12, color: '#F59E0B' },
            { name: 'Email', value: 7, color: '#EF4444' }
          ],
          campaignPerformance: [
            { name: 'Q4 Lead Gen', spent: 8750, revenue: 125000, roas: 14.3 },
            { name: 'Holiday Promo', spent: 5200, revenue: 78000, roas: 15.0 },
            { name: 'Product Launch', spent: 11500, revenue: 195000, roas: 17.0 },
            { name: 'Retargeting', spent: 2100, revenue: 15000, roas: 7.1 }
          ]
        });
      } catch (error) {
        console.error('Failed to fetch reports:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, [selectedPeriod]);

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      ready: { color: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300', label: 'Ready' },
      generating: { color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300', label: 'Generating' },
      failed: { color: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300', label: 'Failed' },
      scheduled: { color: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300', label: 'Scheduled' }
    };

    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.ready;
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
        {config.label}
      </span>
    );
  };

  const getTypeIcon = (type: string) => {
    const icons = {
      sales: <DollarSign className="w-4 h-4" />,
      leads: <Target className="w-4 h-4" />,
      campaigns: <BarChart3 className="w-4 h-4" />,
      analytics: <Activity className="w-4 h-4" />
    };

    return icons[type as keyof typeof icons] || <FileText className="w-4 h-4" />;
  };

  const formatGrowth = (growth: number) => {
    const isPositive = growth >= 0;
    const Icon = isPositive ? TrendingUp : TrendingDown;
    const color = isPositive ? 'text-green-600' : 'text-red-600';
    
    return (
      <div className={`flex items-center gap-1 ${color}`}>
        <Icon className="w-4 h-4" />
        <span className="text-sm font-medium">{Math.abs(growth).toFixed(1)}%</span>
      </div>
    );
  };

  if (loading) {
    return (
      <DashboardLayout title="Reports" description="Analytics and reporting dashboard">
        <div className="p-6 animate-pulse">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/4 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-24 bg-gray-200 dark:bg-gray-700 rounded"></div>
            ))}
          </div>
          <div className="h-96 bg-gray-200 dark:bg-gray-700 rounded"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout title="Reports" description="Analytics and reporting dashboard">
      <div className="p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Reports & Analytics</h1>
            <p className="text-gray-600 dark:text-gray-300">Track performance and generate insights</p>
          </div>
          <div className="flex items-center gap-3">
            <select
              value={selectedPeriod}
              onChange={(e) => setSelectedPeriod(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            >
              <option value="7d">Last 7 days</option>
              <option value="30d">Last 30 days</option>
              <option value="90d">Last 90 days</option>
              <option value="1y">Last year</option>
            </select>
            <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              <Plus className="w-4 h-4" />
              New Report
            </button>
          </div>
        </div>

        {/* Overview Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-2">
              <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
                <Target className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              {formatGrowth(analytics?.overview.leadsGrowth || 0)}
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Total Leads</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{analytics?.overview.totalLeads.toLocaleString()}</p>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-2">
              <div className="p-3 bg-green-100 dark:bg-green-900 rounded-lg">
                <DollarSign className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              {formatGrowth(analytics?.overview.revenueGrowth || 0)}
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Total Revenue</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">${analytics?.overview.totalRevenue.toLocaleString()}</p>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-2">
              <div className="p-3 bg-purple-100 dark:bg-purple-900 rounded-lg">
                <TrendingUp className="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              {formatGrowth(analytics?.overview.conversionGrowth || 0)}
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Conversion Rate</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{analytics?.overview.conversionRate}%</p>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-2">
              <div className="p-3 bg-orange-100 dark:bg-orange-900 rounded-lg">
                <ShoppingCart className="w-6 h-6 text-orange-600 dark:text-orange-400" />
              </div>
              {formatGrowth(analytics?.overview.dealSizeGrowth || 0)}
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-300">Avg Deal Size</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">${analytics?.overview.avgDealSize.toLocaleString()}</p>
            </div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Leads Over Time */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Leads & Revenue Trend</h3>
              <button className="text-blue-600 hover:text-blue-700 dark:text-blue-400">
                <Share2 className="w-4 h-4" />
              </button>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={analytics?.leadsOverTime}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Bar yAxisId="left" dataKey="leads" fill="#3B82F6" />
                <Line yAxisId="right" type="monotone" dataKey="revenue" stroke="#10B981" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Lead Sources */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Lead Sources</h3>
              <button className="text-blue-600 hover:text-blue-700 dark:text-blue-400">
                <Share2 className="w-4 h-4" />
              </button>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <RechartsPieChart>
                <Tooltip />
                <RechartsPieChart dataKey="value" data={analytics?.sourceBreakdown} cx="50%" cy="50%" outerRadius={80}>
                  {analytics?.sourceBreakdown?.map((entry: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </RechartsPieChart>
              </RechartsPieChart>
            </ResponsiveContainer>
            <div className="mt-4 grid grid-cols-2 gap-2">
              {analytics?.sourceBreakdown?.map((source: any) => (
                <div key={source.name} className="flex items-center gap-2">
                  <div 
                    className="w-3 h-3 rounded-full" 
                    style={{ backgroundColor: source.color }}
                  ></div>
                  <span className="text-sm text-gray-600 dark:text-gray-300">
                    {source.name}: {source.value}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Campaign Performance */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Campaign Performance</h3>
            <button className="text-blue-600 hover:text-blue-700 dark:text-blue-400">
              <Eye className="w-4 h-4" />
            </button>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analytics?.campaignPerformance}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="revenue" fill="#10B981" />
              <Bar dataKey="spent" fill="#EF4444" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Reports List */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">Available Reports</h3>
              <div className="flex items-center gap-3">
                <div className="relative">
                  <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                  <input
                    type="text"
                    placeholder="Search reports..."
                    className="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>
          </div>
          
          <div className="divide-y divide-gray-200 dark:divide-gray-700">
            {reports.map((report) => (
              <div key={report.id} className="px-6 py-4 hover:bg-gray-50 dark:hover:bg-gray-700">
                <div className="flex items-center justify-between">
                  <div className="flex items-start gap-4">
                    <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
                      {getTypeIcon(report.type)}
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-900 dark:text-white">{report.name}</h4>
                      <p className="text-sm text-gray-500 dark:text-gray-400">{report.description}</p>
                      <div className="flex items-center gap-4 mt-2 text-xs text-gray-500 dark:text-gray-400">
                        <span>Generated: {new Date(report.lastGenerated).toLocaleDateString()}</span>
                        <span>Frequency: {report.frequency}</span>
                        {report.size && <span>Size: {report.size}</span>}
                        <span>{report.downloads} downloads</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    {getStatusBadge(report.status)}
                    <div className="flex items-center gap-2">
                      <button className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300">
                        <Eye className="w-4 h-4" />
                      </button>
                      {report.status === 'ready' && (
                        <button className="text-green-600 hover:text-green-900 dark:text-green-400 dark:hover:text-green-300">
                          <Download className="w-4 h-4" />
                        </button>
                      )}
                      <button className="text-purple-600 hover:text-purple-900 dark:text-purple-400 dark:hover:text-purple-300">
                        <Share2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default ReportsPage;