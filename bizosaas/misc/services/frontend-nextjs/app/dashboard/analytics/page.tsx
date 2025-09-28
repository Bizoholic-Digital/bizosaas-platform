'use client';

import { useEffect, useState } from 'react';
import { 
  TrendingUp,
  TrendingDown,
  Activity,
  BarChart3,
  DollarSign,
  Users,
  Eye,
  MousePointer,
  Calendar,
  Filter,
  Download,
  RefreshCw,
  Target,
  PieChart,
  LineChart,
  AlertTriangle,
  CheckCircle,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-react';

// Mock analytics data - will be replaced with real API calls
const mockAnalyticsData = {
  overview: {
    total_revenue: 127500,
    total_leads: 2847,
    conversion_rate: 18.7,
    cost_per_lead: 24.50,
    period_comparison: {
      revenue: { current: 127500, previous: 98200, change: 29.9 },
      leads: { current: 2847, previous: 2156, change: 32.1 },
      conversion: { current: 18.7, previous: 16.2, change: 15.4 },
      cost: { current: 24.50, previous: 28.90, change: -15.2 },
    }
  },
  channels: [
    { name: 'Google Ads', revenue: 45200, leads: 1024, conversion: 22.1, cost: 21.50, trend: 'up' },
    { name: 'Facebook Ads', revenue: 38900, leads: 856, conversion: 19.3, cost: 23.80, trend: 'up' },
    { name: 'LinkedIn Ads', revenue: 28700, leads: 542, conversion: 16.8, cost: 34.20, trend: 'down' },
    { name: 'Organic Search', revenue: 14700, leads: 425, conversion: 24.7, cost: 0, trend: 'up' },
  ],
  campaigns: [
    { id: '1', name: 'Q4 Lead Generation', status: 'active', budget: 15000, spent: 12340, leads: 485, conversion: 19.2, roi: 180 },
    { id: '2', name: 'Holiday Promotion', status: 'active', budget: 8500, spent: 7200, leads: 342, conversion: 23.8, roi: 250 },
    { id: '3', name: 'Product Launch', status: 'paused', budget: 12000, spent: 9800, leads: 287, conversion: 15.4, roi: 120 },
    { id: '4', name: 'Retargeting Campaign', status: 'active', budget: 5000, spent: 4100, leads: 156, conversion: 28.1, roi: 320 },
  ],
  performance_trends: {
    last_30_days: [
      { date: '2024-01-01', leads: 45, revenue: 4200, cost: 1100 },
      { date: '2024-01-02', leads: 52, revenue: 4800, cost: 1200 },
      { date: '2024-01-03', leads: 38, revenue: 3500, cost: 950 },
      { date: '2024-01-04', leads: 61, revenue: 5600, cost: 1450 },
      { date: '2024-01-05', leads: 47, revenue: 4300, cost: 1150 },
    ]
  }
};

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
};

const formatNumber = (num: number) => {
  return new Intl.NumberFormat('en-US').format(num);
};

const formatPercentage = (value: number) => {
  return `${value}%`;
};

const getTrendIcon = (trend: string, change: number) => {
  if (change > 0) {
    return <ArrowUpRight className="h-4 w-4 text-green-600" />;
  } else if (change < 0) {
    return <ArrowDownRight className="h-4 w-4 text-red-600" />;
  }
  return null;
};

const getTrendColor = (change: number) => {
  if (change > 0) return 'text-green-600';
  if (change < 0) return 'text-red-600';
  return 'text-gray-600';
};

const getStatusColor = (status: string) => {
  switch (status.toLowerCase()) {
    case 'active':
      return 'text-green-600 bg-green-50 border-green-200';
    case 'paused':
      return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    case 'completed':
      return 'text-blue-600 bg-blue-50 border-blue-200';
    case 'error':
      return 'text-red-600 bg-red-50 border-red-200';
    default:
      return 'text-gray-600 bg-gray-50 border-gray-200';
  }
};

export default function AnalyticsPage() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [refreshing, setRefreshing] = useState(false);
  const [selectedPeriod, setSelectedPeriod] = useState('30d');

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const handleRefresh = async () => {
    setRefreshing(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    setRefreshing(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Sidebar */}
      <div className="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg border-r border-gray-200">
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-center h-16 px-4 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <BarChart3 className="h-8 w-8 text-violet-600" />
              <span className="text-xl font-bold text-gray-900">BizOSaaS</span>
            </div>
          </div>

          {/* Navigation Menu */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            <a href="/dashboard" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <BarChart3 className="mr-3 h-5 w-5" />
              Overview
            </a>
            <a href="/dashboard/ai-agents" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Activity className="mr-3 h-5 w-5" />
              AI Agents
            </a>
            <a href="/dashboard/leads" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Users className="mr-3 h-5 w-5" />
              Leads
            </a>
            <a href="/dashboard/customers" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Users className="mr-3 h-5 w-5" />
              Customers
            </a>
            <a href="/dashboard/campaigns" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Target className="mr-3 h-5 w-5" />
              Campaigns
            </a>
            <a href="/dashboard/analytics" className="flex items-center px-3 py-2 text-sm font-medium text-violet-600 bg-violet-50 rounded-md">
              <TrendingUp className="mr-3 h-5 w-5" />
              Analytics
            </a>
          </nav>

          {/* Real-time Status */}
          <div className="p-4 border-t border-gray-200">
            <div className="flex items-center space-x-2 text-sm text-green-600">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span>Real-time Connected</span>
            </div>
            <div className="text-xs text-gray-500 mt-1">
              Last updated: {currentTime.toLocaleTimeString()}
            </div>
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
                <h1 className="text-2xl font-bold text-gray-900">Analytics & Insights</h1>
                <p className="text-sm text-gray-600">Real-time performance metrics and business intelligence</p>
              </div>
              <div className="flex items-center space-x-4">
                {/* Period Selector */}
                <select 
                  value={selectedPeriod}
                  onChange={(e) => setSelectedPeriod(e.target.value)}
                  className="px-3 py-2 border border-gray-200 rounded-md text-sm focus:ring-2 focus:ring-violet-500"
                >
                  <option value="7d">Last 7 days</option>
                  <option value="30d">Last 30 days</option>
                  <option value="90d">Last 90 days</option>
                  <option value="12m">Last 12 months</option>
                </select>
                
                {/* Action Buttons */}
                <button className="flex items-center space-x-2 px-3 py-2 bg-gray-50 text-gray-600 rounded-md hover:bg-gray-100">
                  <Download className="h-4 w-4" />
                  <span>Export</span>
                </button>
                
                <button
                  onClick={handleRefresh}
                  disabled={refreshing}
                  className="flex items-center space-x-2 px-3 py-2 bg-violet-50 text-violet-600 rounded-md hover:bg-violet-100 disabled:opacity-50"
                >
                  <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
                  <span>{refreshing ? 'Refreshing...' : 'Refresh'}</span>
                </button>
                
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Calendar className="h-4 w-4" />
                  <span>{currentTime.toLocaleDateString()}</span>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="p-6 space-y-6">
          {/* Key Performance Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {formatCurrency(mockAnalyticsData.overview.total_revenue)}
                  </h3>
                  <p className="text-sm text-gray-600">Total Revenue</p>
                  <div className="flex items-center mt-1">
                    {getTrendIcon('up', mockAnalyticsData.overview.period_comparison.revenue.change)}
                    <p className={`text-xs ml-1 ${getTrendColor(mockAnalyticsData.overview.period_comparison.revenue.change)}`}>
                      +{mockAnalyticsData.overview.period_comparison.revenue.change}% from last period
                    </p>
                  </div>
                </div>
                <DollarSign className="h-8 w-8 text-green-600" />
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {formatNumber(mockAnalyticsData.overview.total_leads)}
                  </h3>
                  <p className="text-sm text-gray-600">Total Leads</p>
                  <div className="flex items-center mt-1">
                    {getTrendIcon('up', mockAnalyticsData.overview.period_comparison.leads.change)}
                    <p className={`text-xs ml-1 ${getTrendColor(mockAnalyticsData.overview.period_comparison.leads.change)}`}>
                      +{mockAnalyticsData.overview.period_comparison.leads.change}% from last period
                    </p>
                  </div>
                </div>
                <Users className="h-8 w-8 text-blue-600" />
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {formatPercentage(mockAnalyticsData.overview.conversion_rate)}
                  </h3>
                  <p className="text-sm text-gray-600">Conversion Rate</p>
                  <div className="flex items-center mt-1">
                    {getTrendIcon('up', mockAnalyticsData.overview.period_comparison.conversion.change)}
                    <p className={`text-xs ml-1 ${getTrendColor(mockAnalyticsData.overview.period_comparison.conversion.change)}`}>
                      +{mockAnalyticsData.overview.period_comparison.conversion.change}% from last period
                    </p>
                  </div>
                </div>
                <Target className="h-8 w-8 text-purple-600" />
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {formatCurrency(mockAnalyticsData.overview.cost_per_lead)}
                  </h3>
                  <p className="text-sm text-gray-600">Cost Per Lead</p>
                  <div className="flex items-center mt-1">
                    {getTrendIcon('down', mockAnalyticsData.overview.period_comparison.cost.change)}
                    <p className={`text-xs ml-1 ${getTrendColor(mockAnalyticsData.overview.period_comparison.cost.change)}`}>
                      {mockAnalyticsData.overview.period_comparison.cost.change}% from last period
                    </p>
                  </div>
                </div>
                <MousePointer className="h-8 w-8 text-orange-600" />
              </div>
            </div>
          </div>

          {/* Channel Performance */}
          <div className="bg-white rounded-lg shadow border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                <PieChart className="mr-2 h-5 w-5" />
                Channel Performance
              </h2>
            </div>
            <div className="p-6">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-3 px-4 font-medium text-gray-900">Channel</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">Revenue</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">Leads</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">Conversion</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">Cost/Lead</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">Trend</th>
                    </tr>
                  </thead>
                  <tbody>
                    {mockAnalyticsData.channels.map((channel, index) => (
                      <tr key={index} className="border-b border-gray-100 hover:bg-gray-50">
                        <td className="py-3 px-4">
                          <span className="font-medium">{channel.name}</span>
                        </td>
                        <td className="py-3 px-4">{formatCurrency(channel.revenue)}</td>
                        <td className="py-3 px-4">{formatNumber(channel.leads)}</td>
                        <td className="py-3 px-4">{formatPercentage(channel.conversion)}</td>
                        <td className="py-3 px-4">
                          {channel.cost > 0 ? formatCurrency(channel.cost) : 'Free'}
                        </td>
                        <td className="py-3 px-4">
                          {channel.trend === 'up' ? (
                            <TrendingUp className="h-4 w-4 text-green-600" />
                          ) : (
                            <TrendingDown className="h-4 w-4 text-red-600" />
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Campaign Performance */}
          <div className="bg-white rounded-lg shadow border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                <Target className="mr-2 h-5 w-5" />
                Campaign Performance
              </h2>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {mockAnalyticsData.campaigns.map((campaign) => (
                  <div key={campaign.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <h3 className="font-medium text-gray-900">{campaign.name}</h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(campaign.status)}`}>
                          {campaign.status}
                        </span>
                      </div>
                      <div className="text-sm text-gray-600">
                        ROI: <span className="font-medium text-green-600">{campaign.roi}%</span>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-sm">
                      <div>
                        <span className="text-gray-500">Budget:</span>
                        <div className="font-medium">{formatCurrency(campaign.budget)}</div>
                      </div>
                      <div>
                        <span className="text-gray-500">Spent:</span>
                        <div className="font-medium">{formatCurrency(campaign.spent)}</div>
                      </div>
                      <div>
                        <span className="text-gray-500">Leads:</span>
                        <div className="font-medium">{formatNumber(campaign.leads)}</div>
                      </div>
                      <div>
                        <span className="text-gray-500">Conversion:</span>
                        <div className="font-medium">{formatPercentage(campaign.conversion)}</div>
                      </div>
                      <div>
                        <span className="text-gray-500">Remaining:</span>
                        <div className="font-medium">{formatCurrency(campaign.budget - campaign.spent)}</div>
                      </div>
                    </div>
                    
                    {/* Budget Progress Bar */}
                    <div className="mt-3">
                      <div className="flex justify-between text-xs text-gray-500 mb-1">
                        <span>Budget Usage</span>
                        <span>{Math.round((campaign.spent / campaign.budget) * 100)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-violet-600 h-2 rounded-full transition-all duration-300" 
                          style={{ width: `${Math.min((campaign.spent / campaign.budget) * 100, 100)}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Performance Chart Placeholder */}
          <div className="bg-white rounded-lg shadow border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                <LineChart className="mr-2 h-5 w-5" />
                Performance Trends
              </h2>
            </div>
            <div className="p-6">
              <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
                <div className="text-center">
                  <LineChart className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">Interactive Charts Coming Soon</h3>
                  <p className="text-gray-600 mb-4">
                    Advanced analytics charts with Chart.js integration will be available here.
                  </p>
                  <div className="flex justify-center space-x-4 text-sm text-gray-500">
                    <div>• Revenue trends over time</div>
                    <div>• Lead generation patterns</div>
                    <div>• Conversion rate analysis</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}