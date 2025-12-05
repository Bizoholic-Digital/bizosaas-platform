'use client';

import { useEffect, useState } from 'react';
import { 
  Target,
  Plus,
  Search,
  Filter,
  MoreHorizontal,
  Play,
  Pause,
  Edit,
  Trash2,
  Eye,
  TrendingUp,
  TrendingDown,
  DollarSign,
  Users,
  Calendar,
  RefreshCw,
  Settings,
  CheckCircle,
  AlertCircle,
  Clock,
  BarChart3,
  Activity
} from 'lucide-react';

// Mock campaigns data - will be replaced with real API calls
const mockCampaigns = [
  {
    id: '1',
    name: 'Q4 Lead Generation Campaign',
    status: 'active',
    type: 'lead_generation',
    platform: 'Google Ads',
    budget: 15000,
    spent: 12340,
    remaining: 2660,
    start_date: '2024-01-01',
    end_date: '2024-03-31',
    leads_generated: 485,
    conversions: 93,
    conversion_rate: 19.2,
    cost_per_lead: 25.43,
    roi: 180,
    impressions: 124500,
    clicks: 3420,
    ctr: 2.75,
    created_at: '2023-12-15T00:00:00Z',
    last_updated: '2024-01-15T14:30:00Z'
  },
  {
    id: '2',
    name: 'Holiday Season Promotion',
    status: 'active',
    type: 'promotional',
    platform: 'Facebook Ads',
    budget: 8500,
    spent: 7200,
    remaining: 1300,
    start_date: '2023-12-01',
    end_date: '2024-01-15',
    leads_generated: 342,
    conversions: 81,
    conversion_rate: 23.8,
    cost_per_lead: 21.05,
    roi: 250,
    impressions: 89200,
    clicks: 2156,
    ctr: 2.42,
    created_at: '2023-11-20T00:00:00Z',
    last_updated: '2024-01-14T10:15:00Z'
  },
  {
    id: '3',
    name: 'Product Launch - AI Tools',
    status: 'paused',
    type: 'product_launch',
    platform: 'LinkedIn Ads',
    budget: 12000,
    spent: 9800,
    remaining: 2200,
    start_date: '2023-11-15',
    end_date: '2024-02-15',
    leads_generated: 287,
    conversions: 44,
    conversion_rate: 15.4,
    cost_per_lead: 34.15,
    roi: 120,
    impressions: 45600,
    clicks: 1234,
    ctr: 2.71,
    created_at: '2023-11-01T00:00:00Z',
    last_updated: '2024-01-10T16:45:00Z'
  },
  {
    id: '4',
    name: 'Retargeting - Website Visitors',
    status: 'active',
    type: 'retargeting',
    platform: 'Google Ads',
    budget: 5000,
    spent: 4100,
    remaining: 900,
    start_date: '2024-01-01',
    end_date: '2024-06-30',
    leads_generated: 156,
    conversions: 44,
    conversion_rate: 28.1,
    cost_per_lead: 26.28,
    roi: 320,
    impressions: 23400,
    clicks: 892,
    ctr: 3.81,
    created_at: '2023-12-20T00:00:00Z',
    last_updated: '2024-01-15T11:20:00Z'
  },
  {
    id: '5',
    name: 'Brand Awareness - Video Campaign',
    status: 'completed',
    type: 'brand_awareness',
    platform: 'YouTube Ads',
    budget: 7500,
    spent: 7500,
    remaining: 0,
    start_date: '2023-10-01',
    end_date: '2023-12-31',
    leads_generated: 198,
    conversions: 23,
    conversion_rate: 11.6,
    cost_per_lead: 37.88,
    roi: 95,
    impressions: 156700,
    clicks: 1890,
    ctr: 1.21,
    created_at: '2023-09-15T00:00:00Z',
    last_updated: '2023-12-31T23:59:00Z'
  },
  {
    id: '6',
    name: 'Local Business Outreach',
    status: 'draft',
    type: 'local_marketing',
    platform: 'Facebook Ads',
    budget: 3500,
    spent: 0,
    remaining: 3500,
    start_date: '2024-02-01',
    end_date: '2024-04-30',
    leads_generated: 0,
    conversions: 0,
    conversion_rate: 0,
    cost_per_lead: 0,
    roi: 0,
    impressions: 0,
    clicks: 0,
    ctr: 0,
    created_at: '2024-01-10T00:00:00Z',
    last_updated: '2024-01-12T09:30:00Z'
  }
];

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

const getStatusColor = (status: string) => {
  switch (status.toLowerCase()) {
    case 'active':
      return 'text-green-600 bg-green-50 border-green-200';
    case 'paused':
      return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    case 'completed':
      return 'text-blue-600 bg-blue-50 border-blue-200';
    case 'draft':
      return 'text-gray-600 bg-gray-50 border-gray-200';
    case 'error':
      return 'text-red-600 bg-red-50 border-red-200';
    default:
      return 'text-gray-600 bg-gray-50 border-gray-200';
  }
};

const getStatusIcon = (status: string) => {
  switch (status.toLowerCase()) {
    case 'active':
      return <CheckCircle className="h-4 w-4" />;
    case 'paused':
      return <Pause className="h-4 w-4" />;
    case 'completed':
      return <CheckCircle className="h-4 w-4" />;
    case 'draft':
      return <Clock className="h-4 w-4" />;
    case 'error':
      return <AlertCircle className="h-4 w-4" />;
    default:
      return <Clock className="h-4 w-4" />;
  }
};

const getPlatformColor = (platform: string) => {
  switch (platform.toLowerCase()) {
    case 'google ads':
      return 'bg-blue-100 text-blue-800';
    case 'facebook ads':
      return 'bg-blue-600 text-white';
    case 'linkedin ads':
      return 'bg-blue-800 text-white';
    case 'youtube ads':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

export default function CampaignsPage() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [refreshing, setRefreshing] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [campaigns, setCampaigns] = useState(mockCampaigns);

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

  const filteredCampaigns = campaigns.filter(campaign => {
    const matchesSearch = campaign.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         campaign.platform.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'all' || campaign.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  const campaignStats = {
    total: campaigns.length,
    active: campaigns.filter(c => c.status === 'active').length,
    paused: campaigns.filter(c => c.status === 'paused').length,
    completed: campaigns.filter(c => c.status === 'completed').length,
    draft: campaigns.filter(c => c.status === 'draft').length
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Sidebar */}
      <div className="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg border-r border-gray-200">
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-center h-16 px-4 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <Target className="h-8 w-8 text-violet-600" />
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
            <a href="/dashboard/campaigns" className="flex items-center px-3 py-2 text-sm font-medium text-violet-600 bg-violet-50 rounded-md">
              <Target className="mr-3 h-5 w-5" />
              Campaigns
            </a>
            <a href="/dashboard/analytics" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
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
                <h1 className="text-2xl font-bold text-gray-900">Campaign Management</h1>
                <p className="text-sm text-gray-600">Manage and optimize your marketing campaigns</p>
              </div>
              <div className="flex items-center space-x-4">
                <button
                  onClick={handleRefresh}
                  disabled={refreshing}
                  className="flex items-center space-x-2 px-3 py-2 bg-gray-50 text-gray-600 rounded-md hover:bg-gray-100 disabled:opacity-50"
                >
                  <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
                  <span>{refreshing ? 'Refreshing...' : 'Refresh'}</span>
                </button>
                
                <button className="flex items-center space-x-2 px-4 py-2 bg-violet-600 text-white rounded-md hover:bg-violet-700">
                  <Plus className="h-4 w-4" />
                  <span>Create Campaign</span>
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
          {/* Campaign Statistics */}
          <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <Target className="h-8 w-8 text-violet-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{campaignStats.total}</h3>
                  <p className="text-sm text-gray-600">Total Campaigns</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <CheckCircle className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{campaignStats.active}</h3>
                  <p className="text-sm text-gray-600">Active</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <Pause className="h-8 w-8 text-yellow-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{campaignStats.paused}</h3>
                  <p className="text-sm text-gray-600">Paused</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <CheckCircle className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{campaignStats.completed}</h3>
                  <p className="text-sm text-gray-600">Completed</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <Clock className="h-8 w-8 text-gray-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{campaignStats.draft}</h3>
                  <p className="text-sm text-gray-600">Draft</p>
                </div>
              </div>
            </div>
          </div>

          {/* Filters and Search */}
          <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
              <div className="flex items-center space-x-4">
                {/* Search */}
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search campaigns..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-violet-500 focus:border-violet-500"
                  />
                </div>
                
                {/* Status Filter */}
                <div className="flex items-center space-x-2">
                  <Filter className="h-4 w-4 text-gray-500" />
                  <select
                    value={filterStatus}
                    onChange={(e) => setFilterStatus(e.target.value)}
                    className="border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-violet-500"
                  >
                    <option value="all">All Status</option>
                    <option value="active">Active</option>
                    <option value="paused">Paused</option>
                    <option value="completed">Completed</option>
                    <option value="draft">Draft</option>
                  </select>
                </div>
              </div>

              <div className="text-sm text-gray-600">
                Showing {filteredCampaigns.length} of {campaigns.length} campaigns
              </div>
            </div>
          </div>

          {/* Campaigns List */}
          <div className="bg-white rounded-lg shadow border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                <Target className="mr-2 h-5 w-5" />
                Active Campaigns
              </h2>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {filteredCampaigns.map((campaign) => (
                  <div key={campaign.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="text-lg font-semibold text-gray-900">{campaign.name}</h3>
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getStatusColor(campaign.status)}`}>
                            {getStatusIcon(campaign.status)}
                            <span className="ml-1 capitalize">{campaign.status}</span>
                          </span>
                          <span className={`px-2 py-1 rounded-md text-xs font-medium ${getPlatformColor(campaign.platform)}`}>
                            {campaign.platform}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 capitalize">
                          {campaign.type.replace('_', ' ')} • {new Date(campaign.start_date).toLocaleDateString()} - {new Date(campaign.end_date).toLocaleDateString()}
                        </p>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <button className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-md">
                          <Eye className="h-4 w-4" />
                        </button>
                        <button className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-md">
                          <Edit className="h-4 w-4" />
                        </button>
                        <button className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-md">
                          {campaign.status === 'active' ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                        </button>
                        <button className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-md">
                          <MoreHorizontal className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                    
                    {/* Campaign Metrics */}
                    <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-4">
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{formatCurrency(campaign.budget)}</div>
                        <div className="text-xs text-gray-500">Budget</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{formatCurrency(campaign.spent)}</div>
                        <div className="text-xs text-gray-500">Spent</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{formatNumber(campaign.leads_generated)}</div>
                        <div className="text-xs text-gray-500">Leads</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{formatPercentage(campaign.conversion_rate)}</div>
                        <div className="text-xs text-gray-500">Conv. Rate</div>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-semibold text-gray-900">{formatCurrency(campaign.cost_per_lead)}</div>
                        <div className="text-xs text-gray-500">Cost/Lead</div>
                      </div>
                      <div className="text-center">
                        <div className={`text-lg font-semibold ${campaign.roi >= 150 ? 'text-green-600' : campaign.roi >= 100 ? 'text-yellow-600' : 'text-red-600'}`}>
                          {campaign.roi}%
                        </div>
                        <div className="text-xs text-gray-500">ROI</div>
                      </div>
                    </div>
                    
                    {/* Budget Progress Bar */}
                    {campaign.status !== 'draft' && (
                      <div className="mb-4">
                        <div className="flex justify-between text-xs text-gray-500 mb-1">
                          <span>Budget Usage</span>
                          <span>{Math.round((campaign.spent / campaign.budget) * 100)}% used</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full transition-all duration-300 ${
                              (campaign.spent / campaign.budget) >= 0.9 ? 'bg-red-500' :
                              (campaign.spent / campaign.budget) >= 0.7 ? 'bg-yellow-500' : 'bg-violet-600'
                            }`} 
                            style={{ width: `${Math.min((campaign.spent / campaign.budget) * 100, 100)}%` }}
                          />
                        </div>
                      </div>
                    )}
                    
                    {/* Additional Metrics */}
                    <div className="grid grid-cols-3 gap-4 text-sm text-gray-600">
                      <div>
                        <span className="font-medium">Impressions:</span> {formatNumber(campaign.impressions)}
                      </div>
                      <div>
                        <span className="font-medium">Clicks:</span> {formatNumber(campaign.clicks)}
                      </div>
                      <div>
                        <span className="font-medium">CTR:</span> {formatPercentage(campaign.ctr)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              {filteredCampaigns.length === 0 && (
                <div className="text-center py-8">
                  <Target className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">No campaigns found</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    {searchTerm || filterStatus !== 'all' 
                      ? 'Try adjusting your search or filter criteria.' 
                      : 'Get started by creating your first campaign.'}
                  </p>
                  {!searchTerm && filterStatus === 'all' && (
                    <div className="mt-6">
                      <button className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-violet-600 hover:bg-violet-700">
                        <Plus className="h-4 w-4 mr-2" />
                        Create Campaign
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}