'use client';

import React, { useState, useEffect } from 'react';
import { 
  Zap, Plus, Search, Filter, Download, RefreshCw, 
  Play, Pause, Square, Calendar, Users, Mail,
  Eye, Edit, Trash2, MoreHorizontal, Target, TrendingUp,
  BarChart3, Activity, Clock, CheckCircle, AlertCircle
} from 'lucide-react';
import DashboardLayout from '../../../components/ui/dashboard-layout';

const CampaignsPage = () => {
  const [loading, setLoading] = useState(true);
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        setLoading(true);
        // Mock API call - replace with actual Brain Hub API calls
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        setCampaigns([
          {
            id: '1',
            name: 'Q4 Lead Generation',
            type: 'email',
            status: 'active',
            channel: 'Email Marketing',
            startDate: '2024-09-01T00:00:00Z',
            endDate: '2024-12-31T23:59:59Z',
            budget: 15000,
            spent: 8750,
            audience: 2500,
            sent: 2500,
            delivered: 2425,
            opened: 875,
            clicked: 234,
            converted: 43,
            revenue: 125000,
            ctr: 26.74, // clicked/opened * 100
            conversionRate: 18.38, // converted/clicked * 100
            roas: 14.29, // revenue/spent
            progress: 58 // spent/budget * 100
          },
          {
            id: '2',
            name: 'Holiday Promotion 2024',
            type: 'social',
            status: 'scheduled',
            channel: 'Social Media',
            startDate: '2024-11-15T00:00:00Z',
            endDate: '2024-12-25T23:59:59Z',
            budget: 8000,
            spent: 0,
            audience: 5000,
            sent: 0,
            delivered: 0,
            opened: 0,
            clicked: 0,
            converted: 0,
            revenue: 0,
            ctr: 0,
            conversionRate: 0,
            roas: 0,
            progress: 0
          },
          {
            id: '3',
            name: 'Product Launch Campaign',
            type: 'ppc',
            status: 'completed',
            channel: 'Google Ads',
            startDate: '2024-08-01T00:00:00Z',
            endDate: '2024-08-31T23:59:59Z',
            budget: 12000,
            spent: 11500,
            audience: 15000,
            sent: 15000,
            delivered: 14850,
            opened: 4455,
            clicked: 890,
            converted: 156,
            revenue: 195000,
            ctr: 19.98,
            conversionRate: 17.53,
            roas: 16.96,
            progress: 100
          },
          {
            id: '4',
            name: 'Retargeting Campaign',
            type: 'display',
            status: 'paused',
            channel: 'Display Ads',
            startDate: '2024-09-15T00:00:00Z',
            endDate: '2024-10-15T23:59:59Z',
            budget: 5000,
            spent: 2100,
            audience: 800,
            sent: 800,
            delivered: 796,
            opened: 159,
            clicked: 32,
            converted: 8,
            revenue: 15000,
            ctr: 20.13,
            conversionRate: 25.00,
            roas: 7.14,
            progress: 42
          }
        ]);
      } catch (error) {
        console.error('Failed to fetch campaigns:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCampaigns();
  }, []);

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      active: { color: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300', icon: <Play className="w-3 h-3" />, label: 'Active' },
      paused: { color: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300', icon: <Pause className="w-3 h-3" />, label: 'Paused' },
      completed: { color: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300', icon: <CheckCircle className="w-3 h-3" />, label: 'Completed' },
      scheduled: { color: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300', icon: <Clock className="w-3 h-3" />, label: 'Scheduled' },
      draft: { color: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300', icon: <Edit className="w-3 h-3" />, label: 'Draft' }
    };

    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.draft;
    
    return (
      <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
        {config.icon}
        {config.label}
      </span>
    );
  };

  const getChannelBadge = (channel: string) => {
    const channelConfig = {
      'Email Marketing': { color: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300' },
      'Social Media': { color: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300' },
      'Google Ads': { color: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300' },
      'Display Ads': { color: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300' },
      'Facebook Ads': { color: 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-300' }
    };

    const config = channelConfig[channel as keyof typeof channelConfig] || { color: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300' };
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
        {channel}
      </span>
    );
  };

  const filteredCampaigns = campaigns.filter(campaign => {
    const matchesSearch = campaign.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         campaign.channel.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = selectedFilter === 'all' || campaign.status === selectedFilter;
    return matchesSearch && matchesFilter;
  });

  const stats = {
    total: campaigns.length,
    active: campaigns.filter(c => c.status === 'active').length,
    completed: campaigns.filter(c => c.status === 'completed').length,
    totalBudget: campaigns.reduce((sum, c) => sum + c.budget, 0),
    totalSpent: campaigns.reduce((sum, c) => sum + c.spent, 0),
    totalRevenue: campaigns.reduce((sum, c) => sum + c.revenue, 0),
    averageROAS: campaigns.length > 0 ? (campaigns.reduce((sum, c) => sum + c.roas, 0) / campaigns.length) : 0
  };

  if (loading) {
    return (
      <DashboardLayout title="Campaigns" description="Manage your marketing campaigns">
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
    <DashboardLayout title="Campaigns" description="Manage and track your marketing campaigns">
      <div className="p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Campaign Management</h1>
            <p className="text-gray-600 dark:text-gray-300">Create, manage and analyze your marketing campaigns</p>
          </div>
          <div className="flex items-center gap-3">
            <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
              <Download className="w-4 h-4" />
              Export
            </button>
            <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              <Plus className="w-4 h-4" />
              Create Campaign
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
                <Zap className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Total Campaigns</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">{stats.active} active</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-green-100 dark:bg-green-900 rounded-lg">
                <Target className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Total Budget</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">${stats.totalBudget.toLocaleString()}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">${stats.totalSpent.toLocaleString()} spent</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-purple-100 dark:bg-purple-900 rounded-lg">
                <TrendingUp className="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Total Revenue</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">${stats.totalRevenue.toLocaleString()}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">Generated</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-orange-100 dark:bg-orange-900 rounded-lg">
                <BarChart3 className="w-6 h-6 text-orange-600 dark:text-orange-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-300">Avg ROAS</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.averageROAS.toFixed(2)}x</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">Return on Ad Spend</p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search campaigns by name or channel..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 w-full border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
            <select
              value={selectedFilter}
              onChange={(e) => setSelectedFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="paused">Paused</option>
              <option value="completed">Completed</option>
              <option value="scheduled">Scheduled</option>
              <option value="draft">Draft</option>
            </select>
            <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg">
              <RefreshCw className="w-4 h-4 text-gray-600 dark:text-gray-300" />
            </button>
          </div>
        </div>

        {/* Campaigns Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredCampaigns.map((campaign) => (
            <div key={campaign.id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{campaign.name}</h3>
                    {getStatusBadge(campaign.status)}
                  </div>
                  <div className="flex items-center gap-2 mb-3">
                    {getChannelBadge(campaign.channel)}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button className="p-2 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900 rounded-lg">
                    <Eye className="w-4 h-4" />
                  </button>
                  <button className="p-2 text-green-600 hover:bg-green-50 dark:hover:bg-green-900 rounded-lg">
                    <Edit className="w-4 h-4" />
                  </button>
                  <button className="p-2 text-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg">
                    <MoreHorizontal className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="mb-4">
                <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-300 mb-1">
                  <span>Budget Progress</span>
                  <span>{campaign.progress}%</span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full" 
                    style={{ width: `${Math.min(campaign.progress, 100)}%` }}
                  ></div>
                </div>
              </div>

              {/* Campaign Metrics */}
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Budget</p>
                  <p className="text-lg font-semibold text-gray-900 dark:text-white">
                    ${campaign.budget.toLocaleString()}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Spent</p>
                  <p className="text-lg font-semibold text-gray-900 dark:text-white">
                    ${campaign.spent.toLocaleString()}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Revenue</p>
                  <p className="text-lg font-semibold text-green-600 dark:text-green-400">
                    ${campaign.revenue.toLocaleString()}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">ROAS</p>
                  <p className="text-lg font-semibold text-purple-600 dark:text-purple-400">
                    {campaign.roas.toFixed(2)}x
                  </p>
                </div>
              </div>

              {/* Performance Metrics */}
              <div className="grid grid-cols-4 gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                <div className="text-center">
                  <p className="text-sm text-gray-500 dark:text-gray-400">Sent</p>
                  <p className="text-sm font-medium text-gray-900 dark:text-white">{campaign.sent.toLocaleString()}</p>
                </div>
                <div className="text-center">
                  <p className="text-sm text-gray-500 dark:text-gray-400">Opened</p>
                  <p className="text-sm font-medium text-gray-900 dark:text-white">{campaign.opened.toLocaleString()}</p>
                </div>
                <div className="text-center">
                  <p className="text-sm text-gray-500 dark:text-gray-400">CTR</p>
                  <p className="text-sm font-medium text-gray-900 dark:text-white">{campaign.ctr.toFixed(1)}%</p>
                </div>
                <div className="text-center">
                  <p className="text-sm text-gray-500 dark:text-gray-400">Conv.</p>
                  <p className="text-sm font-medium text-gray-900 dark:text-white">{campaign.converted}</p>
                </div>
              </div>

              {/* Campaign Duration */}
              <div className="flex items-center gap-2 mt-4 text-sm text-gray-500 dark:text-gray-400">
                <Calendar className="w-4 h-4" />
                <span>
                  {new Date(campaign.startDate).toLocaleDateString()} - {new Date(campaign.endDate).toLocaleDateString()}
                </span>
              </div>
            </div>
          ))}
        </div>

        {filteredCampaigns.length === 0 && (
          <div className="text-center py-12">
            <Zap className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">No campaigns found</h3>
            <p className="text-gray-500 dark:text-gray-400">
              {searchTerm ? 'Try adjusting your search terms' : 'Get started by creating your first campaign'}
            </p>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default CampaignsPage;