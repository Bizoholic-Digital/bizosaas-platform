'use client';

import { useEffect, useState } from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import { 
  BarChart3,
  Bot,
  Building,
  Calendar,
  FileText,
  Globe,
  MessageSquare,
  Settings,
  ShoppingCart,
  TrendingUp,
  Users,
  Zap,
  Activity,
  Share2,
  Target,
  Camera,
  Linkedin,
  Twitter,
  Facebook,
  Instagram,
  Youtube,
  Video,
  MapPin,
  Plus,
  Filter,
  Download,
  ExternalLink,
  AlertCircle,
  CheckCircle2,
  Clock,
  Eye,
  MessageCircle,
  Heart,
  RefreshCw,
  Layers,
  MoreHorizontal
} from 'lucide-react';

// Import our components
import CampaignManager from '../../../components/social-media/CampaignManager';
import PerformanceAnalytics from '../../../components/social-media/PerformanceAnalytics';
import AudienceAnalyzer from '../../../components/social-media/AudienceAnalyzer';

// Import hooks
import { 
  useSocialMediaDashboard, 
  useSocialMediaStore,
  usePlatforms,
  useRealtimeMetrics,
  useSocialMediaError
} from '../../../lib/hooks/useSocialMedia';

// Social Media Platform Configuration
const socialPlatforms = [
  { 
    id: 'facebook', 
    name: 'Facebook', 
    icon: Facebook, 
    color: 'text-blue-600 bg-blue-50 border-blue-200',
    connected: true,
    apiStatus: 'healthy' 
  },
  { 
    id: 'instagram', 
    name: 'Instagram', 
    icon: Instagram, 
    color: 'text-purple-600 bg-purple-50 border-purple-200',
    connected: true,
    apiStatus: 'healthy' 
  },
  { 
    id: 'twitter', 
    name: 'Twitter/X', 
    icon: Twitter, 
    color: 'text-gray-800 bg-gray-50 border-gray-200',
    connected: true,
    apiStatus: 'healthy' 
  },
  { 
    id: 'linkedin', 
    name: 'LinkedIn', 
    icon: Linkedin, 
    color: 'text-blue-700 bg-blue-50 border-blue-200',
    connected: true,
    apiStatus: 'degraded' 
  },
  { 
    id: 'tiktok', 
    name: 'TikTok', 
    icon: Video, 
    color: 'text-pink-600 bg-pink-50 border-pink-200',
    connected: false,
    apiStatus: 'healthy' 
  },
  { 
    id: 'youtube', 
    name: 'YouTube', 
    icon: Youtube, 
    color: 'text-red-600 bg-red-50 border-red-200',
    connected: true,
    apiStatus: 'healthy' 
  },
  { 
    id: 'pinterest', 
    name: 'Pinterest', 
    icon: MapPin, 
    color: 'text-red-500 bg-red-50 border-red-200',
    connected: false,
    apiStatus: 'healthy' 
  }
];

// Mock data for audience analysis
const mockAudience = [
  { platform: 'facebook', demographics: { '18-24': 15, '25-34': 35, '35-44': 30, '45-54': 15, '55+': 5 }, gender: { male: 45, female: 55 } },
  { platform: 'instagram', demographics: { '18-24': 40, '25-34': 35, '35-44': 20, '45-54': 4, '55+': 1 }, gender: { male: 35, female: 65 } },
  { platform: 'twitter', demographics: { '18-24': 20, '25-34': 40, '35-44': 25, '45-54': 12, '55+': 3 }, gender: { male: 60, female: 40 } },
  { platform: 'linkedin', demographics: { '18-24': 10, '25-34': 45, '35-44': 35, '45-54': 8, '55+': 2 }, gender: { male: 55, female: 45 } }
];

const formatNumber = (num: number) => {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
  return num.toString();
};

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
};

const formatPercentage = (value: number) => {
  return `${value.toFixed(1)}%`;
};

const getStatusColor = (status: string) => {
  switch (status.toLowerCase()) {
    case 'active':
    case 'published':
    case 'healthy':
      return 'text-green-600 bg-green-50 border-green-200';
    case 'scheduled':
    case 'pending':
    case 'degraded':
      return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    case 'paused':
    case 'draft':
    case 'down':
      return 'text-red-600 bg-red-50 border-red-200';
    default:
      return 'text-gray-600 bg-gray-50 border-gray-200';
  }
};

const getPlatformIcon = (platformId: string) => {
  const platform = socialPlatforms.find(p => p.id === platformId);
  return platform ? platform.icon : Globe;
};

// Create QueryClient instance
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
  },
});

function SocialMediaDashboardContent() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [activeComponent, setActiveComponent] = useState<'dashboard' | 'campaigns' | 'analytics' | 'audience' | null>('dashboard');
  
  // Zustand store state
  const { 
    selectedPlatforms, 
    timeRange, 
    setSelectedPlatforms, 
    setTimeRange,
    syncStatus,
    lastSync
  } = useSocialMediaStore();
  
  // Error handling
  const { error, clearError, hasError } = useSocialMediaError();
  
  // Real-time data
  const { platforms, metrics, campaigns, content, isLoading, refetch } = useSocialMediaDashboard();
  const realtimeQuery = useRealtimeMetrics(
    selectedPlatforms.includes('all') ? [] : selectedPlatforms
  );

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);
  
  // Auto-refresh data every 5 minutes
  useEffect(() => {
    const interval = setInterval(() => {
      if (!isLoading) {
        refetch();
      }
    }, 5 * 60 * 1000);
    
    return () => clearInterval(interval);
  }, [isLoading, refetch]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Sidebar */}
      <div className="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg border-r border-gray-200">
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-center h-16 px-4 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <Bot className="h-8 w-8 text-blue-600" />
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
              <Bot className="mr-3 h-5 w-5" />
              AI Agents
            </a>
            <a href="/dashboard/leads" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Users className="mr-3 h-5 w-5" />
              Leads
            </a>
            <a href="/dashboard/customers" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Building className="mr-3 h-5 w-5" />
              Customers
            </a>
            <a href="/dashboard/campaigns" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <MessageSquare className="mr-3 h-5 w-5" />
              Campaigns
            </a>
            <a href="/dashboard/social-media" className="flex items-center px-3 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-md">
              <Share2 className="mr-3 h-5 w-5" />
              Social Media
            </a>
            <a href="/coreldove" target="_blank" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <ShoppingCart className="mr-3 h-5 w-5" />
              Amazon Sourcing
            </a>
            <a href="/dashboard/analytics" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <TrendingUp className="mr-3 h-5 w-5" />
              Analytics
            </a>
            <a href="/dashboard/system" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Activity className="mr-3 h-5 w-5" />
              System Status
            </a>
            <a href="/dashboard/settings" className="flex items-center px-3 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-md">
              <Settings className="mr-3 h-5 w-5" />
              Settings
            </a>
          </nav>

          {/* Real-time Status */}
          <div className="p-4 border-t border-gray-200">
            <div className="flex items-center space-x-2 text-sm text-green-600">
              <div className={`w-2 h-2 rounded-full animate-pulse ${
                syncStatus === 'success' ? 'bg-green-500' : 
                syncStatus === 'error' ? 'bg-red-500' : 
                syncStatus === 'syncing' ? 'bg-yellow-500' : 'bg-gray-500'
              }`}></div>
              <span>
                {syncStatus === 'success' ? 'Real-time Connected' :
                 syncStatus === 'error' ? 'Connection Error' :
                 syncStatus === 'syncing' ? 'Syncing...' : 'Idle'}
              </span>
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
                <h1 className="text-2xl font-bold text-gray-900">Social Media Dashboard</h1>
                <p className="text-sm text-gray-600">Unified social media management across all platforms</p>
              </div>
              <div className="flex items-center space-x-4">
                <button 
                  onClick={() => setActiveComponent('campaigns')}
                  className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <Plus className="mr-2 h-4 w-4" />
                  Create Campaign
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
          {/* Filters & Controls */}
          <div className="bg-white p-4 rounded-lg shadow border border-gray-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <Filter className="h-4 w-4 text-gray-500" />
                  <span className="text-sm font-medium text-gray-700">Platforms:</span>
                  <select 
                    value={selectedPlatforms[0]} 
                    onChange={(e) => setSelectedPlatforms([e.target.value])}
                    className="border border-gray-300 rounded-md px-3 py-1 text-sm"
                  >
                    <option value="all">All Platforms</option>
                    {socialPlatforms.map(platform => (
                      <option key={platform.id} value={platform.id}>{platform.name}</option>
                    ))}
                  </select>
                </div>
                <div className="flex items-center space-x-2">
                  <Clock className="h-4 w-4 text-gray-500" />
                  <span className="text-sm font-medium text-gray-700">Time Range:</span>
                  <select 
                    value={timeRange} 
                    onChange={(e) => setTimeRange(e.target.value)}
                    className="border border-gray-300 rounded-md px-3 py-1 text-sm"
                  >
                    <option value="24h">Last 24 Hours</option>
                    <option value="7d">Last 7 Days</option>
                    <option value="30d">Last 30 Days</option>
                    <option value="90d">Last 90 Days</option>
                  </select>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <button 
                  onClick={refetch}
                  disabled={isLoading}
                  className="flex items-center px-3 py-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
                >
                  <RefreshCw className={`mr-2 h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
                  Refresh
                </button>
                <button className="flex items-center px-3 py-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-md hover:bg-gray-50">
                  <Download className="mr-2 h-4 w-4" />
                  Export
                </button>
              </div>
            </div>
          </div>

          {/* Error Banner */}
          {hasError && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <AlertCircle className="h-5 w-5 text-red-600" />
                  <span className="text-red-800 font-medium">Error</span>
                  <span className="text-red-700">{error}</span>
                </div>
                <button 
                  onClick={clearError}
                  className="text-red-600 hover:text-red-700 text-sm font-medium"
                >
                  Dismiss
                </button>
              </div>
            </div>
          )}
          
          {/* Component Switcher */}
          <div className="bg-white rounded-lg shadow border border-gray-200 mb-6">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900">Social Media Management</h2>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => setActiveComponent('dashboard')}
                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      activeComponent === 'dashboard'
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    }`}
                  >
                    <BarChart3 className="h-4 w-4 mr-1 inline" />
                    Dashboard
                  </button>
                  <button
                    onClick={() => setActiveComponent('campaigns')}
                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      activeComponent === 'campaigns'
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    }`}
                  >
                    <Target className="h-4 w-4 mr-1 inline" />
                    Campaigns
                  </button>
                  <button
                    onClick={() => setActiveComponent('analytics')}
                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      activeComponent === 'analytics'
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    }`}
                  >
                    <TrendingUp className="h-4 w-4 mr-1 inline" />
                    Analytics
                  </button>
                  <button
                    onClick={() => setActiveComponent('audience')}
                    className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      activeComponent === 'audience'
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    }`}
                  >
                    <Users className="h-4 w-4 mr-1 inline" />
                    Audience
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          {/* Render Active Component */}
          {activeComponent === 'campaigns' && (
            <CampaignManager onClose={() => setActiveComponent('dashboard')} />
          )}
          
          {activeComponent === 'analytics' && (
            <PerformanceAnalytics onClose={() => setActiveComponent('dashboard')} />
          )}
          
          {activeComponent === 'audience' && (
            <AudienceAnalyzer onClose={() => setActiveComponent('dashboard')} />
          )}
          
          {activeComponent === 'dashboard' && (
            <div className="space-y-6">
              {/* Platform Connections */}
              <div className="bg-white rounded-lg shadow border border-gray-200">
                <div className="px-6 py-4 border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                      <Share2 className="mr-2 h-5 w-5" />
                      Platform Connections
                      {syncStatus === 'syncing' && (
                        <RefreshCw className="ml-2 h-4 w-4 animate-spin text-blue-600" />
                      )}
                    </h2>
                    {lastSync && (
                      <span className="text-sm text-gray-500">
                        Last synced: {new Date(lastSync).toLocaleTimeString()}
                      </span>
                    )}
                  </div>
                </div>
                <div className="p-6">
                  {isLoading ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                      {Array.from({ length: 4 }, (_, i) => (
                        <div key={i} className="p-4 border border-gray-200 rounded-lg animate-pulse">
                          <div className="h-6 bg-gray-200 rounded mb-2"></div>
                          <div className="h-4 bg-gray-200 rounded mb-2"></div>
                          <div className="h-3 bg-gray-200 rounded"></div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                      {socialPlatforms.map((platform) => {
                        const connectedPlatform = platforms.find(p => p.id === platform.id);
                        const IconComponent = platform.icon;
                        const platformMetrics = metrics.find(m => m.platform === platform.id);
                        
                        return (
                          <div key={platform.id} className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                            <div className="flex items-center justify-between mb-3">
                              <div className="flex items-center space-x-2">
                                <IconComponent className="h-6 w-6" />
                                <span className="font-medium text-gray-900">{platform.name}</span>
                              </div>
                              <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(connectedPlatform?.apiStatus || 'down')}`}>
                                {connectedPlatform?.apiStatus || 'disconnected'}
                              </span>
                            </div>
                            <div className="flex items-center space-x-2 mb-3">
                              {connectedPlatform?.connected ? (
                                <CheckCircle2 className="h-4 w-4 text-green-600" />
                              ) : (
                                <AlertCircle className="h-4 w-4 text-red-600" />
                              )}
                              <span className={`text-sm ${connectedPlatform?.connected ? 'text-green-600' : 'text-red-600'}`}>
                                {connectedPlatform?.connected ? 'Connected' : 'Not Connected'}
                              </span>
                            </div>
                            {platformMetrics && (
                              <div className="mt-2 text-xs text-gray-600 space-y-1">
                                <div>Followers: {formatNumber(platformMetrics.followers)}</div>
                                <div>Engagement: {formatPercentage(platformMetrics.engagement)}</div>
                                <div>Reach: {formatNumber(platformMetrics.reach)}</div>
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              </div>

              {/* Key Metrics */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
                {isLoading ? (
                  Array.from({ length: 5 }, (_, i) => (
                    <div key={i} className="bg-white p-6 rounded-lg shadow border border-gray-200 animate-pulse">
                      <div className="flex items-center">
                        <div className="h-8 w-8 bg-gray-200 rounded"></div>
                        <div className="ml-4 flex-1">
                          <div className="h-6 bg-gray-200 rounded mb-1"></div>
                          <div className="h-4 bg-gray-200 rounded mb-1"></div>
                          <div className="h-3 bg-gray-200 rounded"></div>
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <>
                    <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
                      <div className="flex items-center">
                        <Users className="h-8 w-8 text-blue-600" />
                        <div className="ml-4">
                          <h3 className="text-lg font-semibold text-gray-900">
                            {formatNumber(metrics.reduce((sum, m) => sum + m.followers, 0))}
                          </h3>
                          <p className="text-sm text-gray-600">Total Followers</p>
                          <p className="text-xs text-green-600">+5.2% this month</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
                      <div className="flex items-center">
                        <Heart className="h-8 w-8 text-pink-600" />
                        <div className="ml-4">
                          <h3 className="text-lg font-semibold text-gray-900">
                            {formatPercentage(metrics.reduce((sum, m) => sum + m.engagement, 0) / (metrics.length || 1))}
                          </h3>
                          <p className="text-sm text-gray-600">Avg Engagement</p>
                          <p className="text-xs text-green-600">+1.3% this month</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
                      <div className="flex items-center">
                        <Target className="h-8 w-8 text-green-600" />
                        <div className="ml-4">
                          <h3 className="text-lg font-semibold text-gray-900">
                            {campaigns.filter(c => c.status === 'active').length}
                          </h3>
                          <p className="text-sm text-gray-600">Active Campaigns</p>
                          <p className="text-xs text-green-600">3 new this week</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
                      <div className="flex items-center">
                        <Eye className="h-8 w-8 text-purple-600" />
                        <div className="ml-4">
                          <h3 className="text-lg font-semibold text-gray-900">
                            {formatNumber(metrics.reduce((sum, m) => sum + m.reach, 0))}
                          </h3>
                          <p className="text-sm text-gray-600">Total Reach</p>
                          <p className="text-xs text-green-600">+12.8% this month</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
                      <div className="flex items-center">
                        <FileText className="h-8 w-8 text-orange-600" />
                        <div className="ml-4">
                          <h3 className="text-lg font-semibold text-gray-900">
                            {content.length}
                          </h3>
                          <p className="text-sm text-gray-600">Content Pieces</p>
                          <p className="text-xs text-green-600">+15 this week</p>
                        </div>
                      </div>
                    </div>
                  </>
                )}
              </div>

              {/* Quick Actions */}
              <div className="bg-white rounded-lg shadow border border-gray-200">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h2 className="text-xl font-semibold text-gray-900">Quick Actions</h2>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <button 
                      onClick={() => setActiveComponent('campaigns')}
                      className="flex items-center justify-center p-4 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors"
                    >
                      <Plus className="mr-2 h-5 w-5" />
                      Create Campaign
                    </button>
                    <button className="flex items-center justify-center p-4 bg-green-50 text-green-600 rounded-lg hover:bg-green-100 transition-colors">
                      <Camera className="mr-2 h-5 w-5" />
                      Schedule Content
                    </button>
                    <button 
                      onClick={() => setActiveComponent('analytics')}
                      className="flex items-center justify-center p-4 bg-purple-50 text-purple-600 rounded-lg hover:bg-purple-100 transition-colors"
                    >
                      <BarChart3 className="mr-2 h-5 w-5" />
                      View Analytics
                    </button>
                    <button 
                      onClick={() => setActiveComponent('audience')}
                      className="flex items-center justify-center p-4 bg-orange-50 text-orange-600 rounded-lg hover:bg-orange-100 transition-colors"
                    >
                      <Users className="mr-2 h-5 w-5" />
                      Analyze Audience
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

// Main component with QueryClient provider
export default function SocialMediaDashboard() {
  return (
    <QueryClientProvider client={queryClient}>
      <SocialMediaDashboardContent />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}