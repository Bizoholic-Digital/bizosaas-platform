/**
 * Real-time Social Media Dashboard
 * Enhanced version of the social media dashboard with real-time updates
 */

'use client';

import React, { useState, useEffect } from 'react';
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
import { cn } from '@/lib/utils';
import { useSocialMediaMetrics, useRealtimeConnection } from '@/lib/hooks/useRealtime';
import { RealtimeMetricsGrid } from './RealtimeMetricCard';
import { RealtimeChart } from './RealtimeChart';
import { RealtimeNotificationBell, RealtimeNotificationCenter } from './RealtimeNotifications';
import { RealtimeConnectionStatus, RealtimeStatusBar } from './RealtimeStatusIndicator';

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

export function RealtimeSocialMediaDashboard() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [showNotifications, setShowNotifications] = useState(false);
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(['all']);
  const [timeRange, setTimeRange] = useState('7d');

  const { socialMediaMetrics, isConnected, lastUpdateTime } = useSocialMediaMetrics();
  const { reconnect } = useRealtimeConnection();

  // Update current time every second
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Generate mock chart data for engagement over time
  const [engagementData, setEngagementData] = useState(() => {
    const now = Date.now();
    return Array.from({ length: 24 }, (_, i) => ({
      timestamp: now - (23 - i) * 60000, // Last 24 hours
      value: Math.floor(Math.random() * 100) + 50,
      facebook: Math.floor(Math.random() * 50) + 20,
      instagram: Math.floor(Math.random() * 80) + 40,
      twitter: Math.floor(Math.random() * 30) + 15,
      linkedin: Math.floor(Math.random() * 25) + 10,
    }));
  });

  // Simulate real-time chart updates
  useEffect(() => {
    if (!isConnected) return;

    const interval = setInterval(() => {
      setEngagementData(prev => {
        const newPoint = {
          timestamp: Date.now(),
          value: Math.floor(Math.random() * 100) + 50,
          facebook: Math.floor(Math.random() * 50) + 20,
          instagram: Math.floor(Math.random() * 80) + 40,
          twitter: Math.floor(Math.random() * 30) + 15,
          linkedin: Math.floor(Math.random() * 25) + 10,
        };
        return [...prev.slice(1), newPoint];
      });
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, [isConnected]);

  // Prepare metrics data
  const metricsData = [
    {
      id: 'followers',
      title: 'Total Followers',
      value: socialMediaMetrics?.total_followers || 125847,
      change: 5.2,
      icon: <Users className="h-6 w-6" />,
      color: 'blue' as const,
      subtitle: '+5.2% this month',
      lastUpdated: lastUpdateTime
    },
    {
      id: 'engagement',
      title: 'Avg Engagement',
      value: socialMediaMetrics?.total_engagement || 8.7,
      change: 1.3,
      icon: <Heart className="h-6 w-6" />,
      color: 'purple' as const,
      format: 'percentage' as const,
      subtitle: '+1.3% this month',
      lastUpdated: lastUpdateTime
    },
    {
      id: 'campaigns',
      title: 'Active Campaigns',
      value: socialMediaMetrics?.active_campaigns || 12,
      change: 3,
      changeType: 'absolute' as const,
      icon: <Target className="h-6 w-6" />,
      color: 'green' as const,
      subtitle: '3 new this week',
      lastUpdated: lastUpdateTime
    },
    {
      id: 'reach',
      title: 'Monthly Reach',
      value: socialMediaMetrics?.monthly_reach || 2847593,
      change: 12.8,
      icon: <Eye className="h-6 w-6" />,
      color: 'orange' as const,
      subtitle: '+12.8% this month',
      lastUpdated: lastUpdateTime
    },
    {
      id: 'content',
      title: 'Content Pieces',
      value: socialMediaMetrics?.content_pieces || 89,
      change: 15,
      changeType: 'absolute' as const,
      icon: <FileText className="h-6 w-6" />,
      color: 'yellow' as const,
      subtitle: '+15 this week',
      lastUpdated: lastUpdateTime
    }
  ];

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

          {/* Real-time Connection Status */}
          <div className="p-4 border-t border-gray-200">
            <RealtimeConnectionStatus showDetails />
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
                <p className="text-sm text-gray-600">Real-time unified social media management across all platforms</p>
              </div>
              <div className="flex items-center space-x-4">
                {/* Reconnect Button */}
                {!isConnected && (
                  <button
                    onClick={reconnect}
                    className="flex items-center px-3 py-2 text-sm font-medium text-blue-600 hover:text-blue-700 border border-blue-200 rounded-md hover:bg-blue-50"
                  >
                    <RefreshCw className="mr-2 h-4 w-4" />
                    Reconnect
                  </button>
                )}

                <button className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  <Plus className="mr-2 h-4 w-4" />
                  Create Campaign
                </button>

                {/* Notifications */}
                <RealtimeNotificationBell 
                  onClick={() => setShowNotifications(true)} 
                />

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

          {/* Real-time Metrics Grid */}
          <RealtimeMetricsGrid 
            metrics={metricsData}
            columns={5}
            isLoading={!isConnected}
          />

          {/* Real-time Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Engagement Over Time */}
            <RealtimeChart
              data={engagementData}
              type="line"
              title="Engagement Rate Over Time"
              color="#8B5CF6"
              height={300}
              isRealtime={isConnected}
              formatValue={(value) => `${value.toFixed(1)}%`}
            />

            {/* Platform Comparison */}
            <RealtimeChart
              data={engagementData}
              type="bar"
              title="Platform Performance"
              color="#10B981"
              height={300}
              isRealtime={isConnected}
            />
          </div>

          {/* Platform Connection Status */}
          <div className="bg-white rounded-lg shadow border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                  <Share2 className="mr-2 h-5 w-5" />
                  Platform Connections
                  {isConnected && (
                    <div className="ml-3 flex items-center space-x-1">
                      <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                      <span className="text-xs text-green-600 font-medium">Live</span>
                    </div>
                  )}
                </h2>
              </div>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {socialPlatforms.map((platform) => {
                  const IconComponent = platform.icon;
                  const platformData = socialMediaMetrics?.platform_breakdown?.[platform.id];
                  
                  return (
                    <div key={platform.id} className="p-4 border border-gray-200 rounded-lg">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          <IconComponent className="h-6 w-6" />
                          <span className="font-medium text-gray-900">{platform.name}</span>
                        </div>
                        <span className={cn(
                          "px-2 py-1 rounded-full text-xs font-medium border",
                          platform.apiStatus === 'healthy' && "text-green-600 bg-green-50 border-green-200",
                          platform.apiStatus === 'degraded' && "text-yellow-600 bg-yellow-50 border-yellow-200"
                        )}>
                          {platform.apiStatus}
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        {platform.connected ? (
                          <CheckCircle2 className="h-4 w-4 text-green-600" />
                        ) : (
                          <AlertCircle className="h-4 w-4 text-red-600" />
                        )}
                        <span className={cn(
                          "text-sm",
                          platform.connected ? 'text-green-600' : 'text-red-600'
                        )}>
                          {platform.connected ? 'Connected' : 'Not Connected'}
                        </span>
                      </div>
                      {platform.connected && platformData && (
                        <div className="mt-2 text-xs text-gray-600 space-y-1">
                          <div className="flex justify-between">
                            <span>Followers:</span>
                            <span className="font-medium">{platformData.followers.toLocaleString()}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Engagement:</span>
                            <span className="font-medium">{platformData.engagement.toFixed(1)}%</span>
                          </div>
                          {platformData.interactions_last_hour !== undefined && (
                            <div className="flex justify-between">
                              <span>Last hour:</span>
                              <span className="font-medium text-green-600">
                                +{platformData.interactions_last_hour}
                              </span>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
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

        {/* Status Bar */}
        <RealtimeStatusBar />
      </div>

      {/* Notification Center */}
      <RealtimeNotificationCenter 
        isOpen={showNotifications} 
        onClose={() => setShowNotifications(false)} 
      />
    </div>
  );
}

export default RealtimeSocialMediaDashboard;