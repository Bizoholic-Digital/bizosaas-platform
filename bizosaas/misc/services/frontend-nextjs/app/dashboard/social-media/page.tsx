'use client';

import { useEffect, useState } from 'react';
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
  Hash,
  ThumbsUp,
  Share2,
  Target,
  PlayCircle,
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
  TrendingDown,
  RefreshCw
} from 'lucide-react';

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

// Mock data for dashboard
const mockSocialMetrics = {
  total_followers: 125847,
  total_engagement: 8.7,
  active_campaigns: 12,
  monthly_reach: 2847593,
  content_pieces: 89,
  platform_breakdown: {
    facebook: { followers: 45230, engagement: 7.2, reach: 892340 },
    instagram: { followers: 38542, engagement: 12.4, reach: 674521 },
    twitter: { followers: 28934, engagement: 6.8, reach: 423890 },
    linkedin: { followers: 12341, engagement: 5.4, reach: 234523 },
    youtube: { followers: 800, engagement: 18.2, reach: 622319 }
  }
};

const mockCampaigns = [
  {
    id: '1',
    name: 'Summer Product Launch',
    status: 'active',
    platforms: ['facebook', 'instagram', 'twitter'],
    budget: 5000,
    spent: 3240,
    impressions: 245893,
    clicks: 5834,
    conversions: 87,
    ctr: 2.38,
    created_at: '2025-09-01',
    end_date: '2025-09-30'
  },
  {
    id: '2',
    name: 'Brand Awareness Q4',
    status: 'active',
    platforms: ['linkedin', 'youtube'],
    budget: 8000,
    spent: 2100,
    impressions: 156234,
    clicks: 3421,
    conversions: 45,
    ctr: 2.19,
    created_at: '2025-09-10',
    end_date: '2025-12-31'
  },
  {
    id: '3',
    name: 'Holiday Sale Campaign',
    status: 'scheduled',
    platforms: ['facebook', 'instagram', 'twitter', 'tiktok'],
    budget: 12000,
    spent: 0,
    impressions: 0,
    clicks: 0,
    conversions: 0,
    ctr: 0,
    created_at: '2025-11-15',
    end_date: '2025-12-25'
  }
];

const mockRecentContent = [
  {
    id: '1',
    platform: 'instagram',
    type: 'image',
    content: 'New product showcase - minimalist design meets functionality',
    engagement: { likes: 1234, comments: 87, shares: 45 },
    reach: 12847,
    published_at: '2 hours ago',
    status: 'published'
  },
  {
    id: '2',
    platform: 'linkedin',
    type: 'article',
    content: 'Industry insights: The future of AI in marketing automation',
    engagement: { likes: 234, comments: 28, shares: 156 },
    reach: 8934,
    published_at: '4 hours ago',
    status: 'published'
  },
  {
    id: '3',
    platform: 'twitter',
    type: 'text',
    content: 'Excited to announce our partnership with @TechLeaders...',
    engagement: { likes: 89, comments: 12, shares: 23 },
    reach: 4521,
    published_at: '6 hours ago',
    status: 'published'
  }
];

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

export default function SocialMediaDashboard() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(['all']);
  const [timeRange, setTimeRange] = useState('7d');

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

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
                <h1 className="text-2xl font-bold text-gray-900">Social Media Dashboard</h1>
                <p className="text-sm text-gray-600">Unified social media management across all platforms</p>
              </div>
              <div className="flex items-center space-x-4">
                <button className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
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
                <button className="flex items-center px-3 py-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-md hover:bg-gray-50">
                  <RefreshCw className="mr-2 h-4 w-4" />
                  Refresh
                </button>
                <button className="flex items-center px-3 py-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-md hover:bg-gray-50">
                  <Download className="mr-2 h-4 w-4" />
                  Export
                </button>
              </div>
            </div>
          </div>

          {/* Platform Connection Status */}
          <div className="bg-white rounded-lg shadow border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                <Share2 className="mr-2 h-5 w-5" />
                Platform Connections
              </h2>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {socialPlatforms.map((platform) => {
                  const IconComponent = platform.icon;
                  return (
                    <div key={platform.id} className="p-4 border border-gray-200 rounded-lg">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          <IconComponent className="h-6 w-6" />
                          <span className="font-medium text-gray-900">{platform.name}</span>
                        </div>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(platform.apiStatus)}`}>
                          {platform.apiStatus}
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        {platform.connected ? (
                          <CheckCircle2 className="h-4 w-4 text-green-600" />
                        ) : (
                          <AlertCircle className="h-4 w-4 text-red-600" />
                        )}
                        <span className={`text-sm ${platform.connected ? 'text-green-600' : 'text-red-600'}`}>
                          {platform.connected ? 'Connected' : 'Not Connected'}
                        </span>
                      </div>
                      {platform.connected && mockSocialMetrics.platform_breakdown[platform.id as keyof typeof mockSocialMetrics.platform_breakdown] && (
                        <div className="mt-2 text-xs text-gray-600">
                          <div>Followers: {formatNumber(mockSocialMetrics.platform_breakdown[platform.id as keyof typeof mockSocialMetrics.platform_breakdown].followers)}</div>
                          <div>Engagement: {formatPercentage(mockSocialMetrics.platform_breakdown[platform.id as keyof typeof mockSocialMetrics.platform_breakdown].engagement)}</div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Key Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <Users className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{formatNumber(mockSocialMetrics.total_followers)}</h3>
                  <p className="text-sm text-gray-600">Total Followers</p>
                  <p className="text-xs text-green-600">+5.2% this month</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <Heart className="h-8 w-8 text-pink-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{formatPercentage(mockSocialMetrics.total_engagement)}</h3>
                  <p className="text-sm text-gray-600">Avg Engagement</p>
                  <p className="text-xs text-green-600">+1.3% this month</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <Target className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{mockSocialMetrics.active_campaigns}</h3>
                  <p className="text-sm text-gray-600">Active Campaigns</p>
                  <p className="text-xs text-green-600">3 new this week</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <Eye className="h-8 w-8 text-purple-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{formatNumber(mockSocialMetrics.monthly_reach)}</h3>
                  <p className="text-sm text-gray-600">Monthly Reach</p>
                  <p className="text-xs text-green-600">+12.8% this month</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
              <div className="flex items-center">
                <FileText className="h-8 w-8 text-orange-600" />
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">{mockSocialMetrics.content_pieces}</h3>
                  <p className="text-sm text-gray-600">Content Pieces</p>
                  <p className="text-xs text-green-600">+15 this week</p>
                </div>
              </div>
            </div>
          </div>

          {/* Active Campaigns */}
          <div className="bg-white rounded-lg shadow border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                  <Target className="mr-2 h-5 w-5" />
                  Active Campaigns
                </h2>
                <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                  View All Campaigns
                </button>
              </div>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {mockCampaigns.map((campaign) => (
                  <div key={campaign.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <h3 className="font-semibold text-gray-900">{campaign.name}</h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(campaign.status)}`}>
                          {campaign.status}
                        </span>
                      </div>
                      <button className="text-gray-400 hover:text-gray-600">
                        <ExternalLink className="h-4 w-4" />
                      </button>
                    </div>
                    
                    <div className="flex items-center space-x-4 mb-3">
                      <div className="flex items-center space-x-1">
                        {campaign.platforms.map(platformId => {
                          const IconComponent = getPlatformIcon(platformId);
                          return <IconComponent key={platformId} className="h-4 w-4 text-gray-600" />;
                        })}
                      </div>
                      <span className="text-sm text-gray-600">{campaign.platforms.length} platforms</span>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-6 gap-4 text-sm">
                      <div>
                        <span className="text-gray-600">Budget:</span>
                        <div className="font-medium">{formatCurrency(campaign.budget)}</div>
                      </div>
                      <div>
                        <span className="text-gray-600">Spent:</span>
                        <div className="font-medium">{formatCurrency(campaign.spent)}</div>
                      </div>
                      <div>
                        <span className="text-gray-600">Impressions:</span>
                        <div className="font-medium">{formatNumber(campaign.impressions)}</div>
                      </div>
                      <div>
                        <span className="text-gray-600">Clicks:</span>
                        <div className="font-medium">{formatNumber(campaign.clicks)}</div>
                      </div>
                      <div>
                        <span className="text-gray-600">CTR:</span>
                        <div className="font-medium">{formatPercentage(campaign.ctr)}</div>
                      </div>
                      <div>
                        <span className="text-gray-600">Conversions:</span>
                        <div className="font-medium">{campaign.conversions}</div>
                      </div>
                    </div>
                    
                    <div className="mt-3 w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full" 
                        style={{ width: `${(campaign.spent / campaign.budget) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Recent Content & Audience Analysis */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Recent Content */}
            <div className="bg-white rounded-lg shadow border border-gray-200">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                  <MessageSquare className="mr-2 h-5 w-5" />
                  Recent Content
                </h2>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {mockRecentContent.map((content) => {
                    const IconComponent = getPlatformIcon(content.platform);
                    return (
                      <div key={content.id} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center space-x-2">
                            <IconComponent className="h-4 w-4" />
                            <span className="text-sm font-medium text-gray-700 capitalize">
                              {content.platform}
                            </span>
                            <span className="text-xs text-gray-500">{content.type}</span>
                          </div>
                          <span className="text-xs text-gray-500">{content.published_at}</span>
                        </div>
                        
                        <p className="text-sm text-gray-800 mb-3 line-clamp-2">{content.content}</p>
                        
                        <div className="flex items-center justify-between text-xs text-gray-600">
                          <div className="flex items-center space-x-4">
                            <span className="flex items-center">
                              <Heart className="h-3 w-3 mr-1" />
                              {formatNumber(content.engagement.likes)}
                            </span>
                            <span className="flex items-center">
                              <MessageCircle className="h-3 w-3 mr-1" />
                              {content.engagement.comments}
                            </span>
                            <span className="flex items-center">
                              <Share2 className="h-3 w-3 mr-1" />
                              {content.engagement.shares}
                            </span>
                          </div>
                          <div className="flex items-center">
                            <Eye className="h-3 w-3 mr-1" />
                            {formatNumber(content.reach)} reach
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Audience Analysis */}
            <div className="bg-white rounded-lg shadow border border-gray-200">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                  <Users className="mr-2 h-5 w-5" />
                  Audience Analysis
                </h2>
              </div>
              <div className="p-6">
                <div className="space-y-6">
                  {mockAudience.map((platform) => {
                    const IconComponent = getPlatformIcon(platform.platform);
                    return (
                      <div key={platform.platform}>
                        <div className="flex items-center space-x-2 mb-3">
                          <IconComponent className="h-4 w-4" />
                          <span className="font-medium text-gray-900 capitalize">{platform.platform}</span>
                        </div>
                        
                        <div className="mb-3">
                          <span className="text-xs text-gray-600 mb-1 block">Age Demographics</span>
                          <div className="flex space-x-1">
                            {Object.entries(platform.demographics).map(([age, percentage]) => (
                              <div key={age} className="flex-1">
                                <div 
                                  className="bg-blue-500 rounded text-xs text-white text-center py-1"
                                  style={{ height: `${Math.max(percentage / 2, 10)}px` }}
                                ></div>
                                <span className="text-xs text-gray-600 block text-center mt-1">{age}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                        
                        <div>
                          <span className="text-xs text-gray-600 mb-1 block">Gender Distribution</span>
                          <div className="flex space-x-2">
                            <div className="flex items-center text-xs">
                              <div className="w-3 h-3 bg-blue-500 rounded mr-1"></div>
                              Male {platform.gender.male}%
                            </div>
                            <div className="flex items-center text-xs">
                              <div className="w-3 h-3 bg-pink-500 rounded mr-1"></div>
                              Female {platform.gender.female}%
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900">Quick Actions</h2>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <button className="flex items-center justify-center p-4 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors">
                  <Plus className="mr-2 h-5 w-5" />
                  Create Campaign
                </button>
                <button className="flex items-center justify-center p-4 bg-green-50 text-green-600 rounded-lg hover:bg-green-100 transition-colors">
                  <Camera className="mr-2 h-5 w-5" />
                  Schedule Content
                </button>
                <button className="flex items-center justify-center p-4 bg-purple-50 text-purple-600 rounded-lg hover:bg-purple-100 transition-colors">
                  <BarChart3 className="mr-2 h-5 w-5" />
                  View Analytics
                </button>
                <button className="flex items-center justify-center p-4 bg-orange-50 text-orange-600 rounded-lg hover:bg-orange-100 transition-colors">
                  <Settings className="mr-2 h-5 w-5" />
                  Manage Accounts
                </button>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}