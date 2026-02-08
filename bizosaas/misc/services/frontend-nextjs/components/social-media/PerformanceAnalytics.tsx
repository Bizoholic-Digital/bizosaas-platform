'use client';

import { useState } from 'react';
import { 
  BarChart3,
  TrendingUp,
  TrendingDown,
  Eye,
  MessageCircle,
  Heart,
  Share2,
  Users,
  Target,
  DollarSign,
  Calendar,
  Filter,
  Download,
  RefreshCw,
  ArrowUpRight,
  ArrowDownRight,
  Facebook,
  Instagram,
  Twitter,
  Linkedin,
  Youtube,
  Video,
  MapPin,
  Clock,
  Zap,
  Globe
} from 'lucide-react';

interface AnalyticsData {
  timeRange: string;
  totalReach: number;
  totalEngagement: number;
  totalImpressions: number;
  totalClicks: number;
  totalSpend: number;
  averageCTR: number;
  averageCPC: number;
  averageCPM: number;
  conversionRate: number;
  platformBreakdown: {
    [platform: string]: {
      reach: number;
      engagement: number;
      impressions: number;
      clicks: number;
      spend: number;
      ctr: number;
      followers: number;
      growth: number;
    };
  };
  timeSeriesData: {
    date: string;
    reach: number;
    engagement: number;
    impressions: number;
    clicks: number;
    spend: number;
  }[];
  topContent: {
    id: string;
    platform: string;
    type: string;
    content: string;
    engagement: number;
    reach: number;
    clicks: number;
    published_at: string;
  }[];
  audienceDemographics: {
    ageGroups: { [age: string]: number };
    genders: { [gender: string]: number };
    locations: { [location: string]: number };
    interests: { [interest: string]: number };
  };
}

const socialPlatforms = [
  { id: 'facebook', name: 'Facebook', icon: Facebook, color: 'text-blue-600 bg-blue-50' },
  { id: 'instagram', name: 'Instagram', icon: Instagram, color: 'text-purple-600 bg-purple-50' },
  { id: 'twitter', name: 'Twitter/X', icon: Twitter, color: 'text-gray-800 bg-gray-50' },
  { id: 'linkedin', name: 'LinkedIn', icon: Linkedin, color: 'text-blue-700 bg-blue-50' },
  { id: 'youtube', name: 'YouTube', icon: Youtube, color: 'text-red-600 bg-red-50' }
];

const mockAnalyticsData: AnalyticsData = {
  timeRange: '30d',
  totalReach: 2847593,
  totalEngagement: 156743,
  totalImpressions: 4523781,
  totalClicks: 98453,
  totalSpend: 15420,
  averageCTR: 2.18,
  averageCPC: 0.67,
  averageCPM: 14.25,
  conversionRate: 3.42,
  platformBreakdown: {
    facebook: {
      reach: 892340,
      engagement: 64523,
      impressions: 1234567,
      clicks: 26890,
      spend: 4500,
      ctr: 2.18,
      followers: 45230,
      growth: 5.2
    },
    instagram: {
      reach: 674521,
      engagement: 83467,
      impressions: 987654,
      clicks: 31245,
      spend: 3800,
      ctr: 3.16,
      followers: 38542,
      growth: 8.7
    },
    twitter: {
      reach: 423890,
      engagement: 28934,
      impressions: 765432,
      clicks: 18970,
      spend: 2900,
      ctr: 2.48,
      followers: 28934,
      growth: 3.1
    },
    linkedin: {
      reach: 234523,
      engagement: 15672,
      impressions: 456789,
      clicks: 12456,
      spend: 3200,
      ctr: 2.73,
      followers: 12341,
      growth: 12.3
    },
    youtube: {
      reach: 622319,
      engagement: 45621,
      impressions: 1079339,
      clicks: 8892,
      spend: 1020,
      ctr: 0.82,
      followers: 8934,
      growth: 18.9
    }
  },
  timeSeriesData: [
    { date: '2025-08-15', reach: 145000, engagement: 8500, impressions: 234000, clicks: 5200, spend: 820 },
    { date: '2025-08-22', reach: 162000, engagement: 9800, impressions: 267000, clicks: 6100, spend: 950 },
    { date: '2025-08-29', reach: 178000, engagement: 11200, impressions: 298000, clicks: 6800, spend: 1100 },
    { date: '2025-09-05', reach: 195000, engagement: 12600, impressions: 325000, clicks: 7500, spend: 1250 },
    { date: '2025-09-12', reach: 187000, engagement: 11900, impressions: 312000, clicks: 7200, spend: 1180 }
  ],
  topContent: [
    {
      id: '1',
      platform: 'instagram',
      type: 'image',
      content: 'New product showcase - minimalist design meets functionality',
      engagement: 1234,
      reach: 45621,
      clicks: 892,
      published_at: '2025-09-10T14:30:00Z'
    },
    {
      id: '2',
      platform: 'linkedin',
      type: 'article',
      content: 'Industry insights: The future of AI in marketing automation',
      engagement: 1156,
      reach: 38934,
      clicks: 1456,
      published_at: '2025-09-08T09:15:00Z'
    },
    {
      id: '3',
      platform: 'facebook',
      type: 'video',
      content: 'Behind the scenes: How our team creates innovative solutions',
      engagement: 2145,
      reach: 67821,
      clicks: 1789,
      published_at: '2025-09-05T16:45:00Z'
    }
  ],
  audienceDemographics: {
    ageGroups: {
      '18-24': 18,
      '25-34': 35,
      '35-44': 28,
      '45-54': 14,
      '55+': 5
    },
    genders: {
      'Male': 45,
      'Female': 52,
      'Other': 3
    },
    locations: {
      'United States': 45,
      'Canada': 15,
      'United Kingdom': 12,
      'Australia': 8,
      'Germany': 6,
      'Other': 14
    },
    interests: {
      'Technology': 28,
      'Business': 22,
      'Marketing': 18,
      'Design': 15,
      'Lifestyle': 12,
      'Other': 5
    }
  }
};

const timeRanges = [
  { id: '24h', name: 'Last 24 Hours' },
  { id: '7d', name: 'Last 7 Days' },
  { id: '30d', name: 'Last 30 Days' },
  { id: '90d', name: 'Last 90 Days' },
  { id: '1y', name: 'Last Year' }
];

const metricTypes = [
  { id: 'reach', name: 'Reach', icon: Eye, color: 'text-blue-600' },
  { id: 'engagement', name: 'Engagement', icon: Heart, color: 'text-pink-600' },
  { id: 'impressions', name: 'Impressions', icon: BarChart3, color: 'text-green-600' },
  { id: 'clicks', name: 'Clicks', icon: MessageCircle, color: 'text-purple-600' },
  { id: 'spend', name: 'Spend', icon: DollarSign, color: 'text-yellow-600' }
];

interface PerformanceAnalyticsProps {
  onClose?: () => void;
}

export default function PerformanceAnalytics({ onClose }: PerformanceAnalyticsProps) {
  const [selectedTimeRange, setSelectedTimeRange] = useState('30d');
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(['all']);
  const [selectedMetric, setSelectedMetric] = useState('reach');
  const [data] = useState<AnalyticsData>(mockAnalyticsData);

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
    return `${value.toFixed(2)}%`;
  };

  const getPlatformIcon = (platformId: string) => {
    const platform = socialPlatforms.find(p => p.id === platformId);
    return platform ? platform.icon : Globe;
  };

  const getChangeIndicator = (value: number) => {
    if (value > 0) {
      return (
        <span className="flex items-center text-green-600 text-sm">
          <ArrowUpRight className="h-4 w-4 mr-1" />
          +{formatPercentage(value)}
        </span>
      );
    } else if (value < 0) {
      return (
        <span className="flex items-center text-red-600 text-sm">
          <ArrowDownRight className="h-4 w-4 mr-1" />
          {formatPercentage(value)}
        </span>
      );
    }
    return <span className="text-gray-500 text-sm">No change</span>;
  };

  const calculateEngagementRate = (engagement: number, reach: number) => {
    return reach > 0 ? (engagement / reach) * 100 : 0;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg border border-gray-200">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-semibold text-gray-900 flex items-center">
            <BarChart3 className="mr-2 h-6 w-6" />
            Performance Analytics
          </h2>
          <div className="flex items-center space-x-3">
            <button className="flex items-center px-3 py-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-md hover:bg-gray-50">
              <RefreshCw className="mr-2 h-4 w-4" />
              Refresh
            </button>
            <button className="flex items-center px-3 py-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-md hover:bg-gray-50">
              <Download className="mr-2 h-4 w-4" />
              Export
            </button>
            {onClose && (
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600"
              >
                ×
              </button>
            )}
          </div>
        </div>

        {/* Filters */}
        <div className="flex items-center space-x-4 mt-4">
          <div className="flex items-center space-x-2">
            <Calendar className="h-4 w-4 text-gray-500" />
            <select
              value={selectedTimeRange}
              onChange={(e) => setSelectedTimeRange(e.target.value)}
              className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {timeRanges.map(range => (
                <option key={range.id} value={range.id}>{range.name}</option>
              ))}
            </select>
          </div>
          <div className="flex items-center space-x-2">
            <Filter className="h-4 w-4 text-gray-500" />
            <select
              value={selectedPlatforms[0]}
              onChange={(e) => setSelectedPlatforms([e.target.value])}
              className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Platforms</option>
              {socialPlatforms.map(platform => (
                <option key={platform.id} value={platform.id}>{platform.name}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-6 space-y-8">
        {/* Key Metrics Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
          <div className="bg-blue-50 p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-2xl font-bold text-gray-900">{formatNumber(data.totalReach)}</h3>
                <p className="text-sm text-gray-600">Total Reach</p>
              </div>
              <Eye className="h-8 w-8 text-blue-600" />
            </div>
            {getChangeIndicator(8.5)}
          </div>
          
          <div className="bg-pink-50 p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-2xl font-bold text-gray-900">{formatNumber(data.totalEngagement)}</h3>
                <p className="text-sm text-gray-600">Total Engagement</p>
              </div>
              <Heart className="h-8 w-8 text-pink-600" />
            </div>
            {getChangeIndicator(12.3)}
          </div>
          
          <div className="bg-green-50 p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-2xl font-bold text-gray-900">{formatNumber(data.totalImpressions)}</h3>
                <p className="text-sm text-gray-600">Total Impressions</p>
              </div>
              <BarChart3 className="h-8 w-8 text-green-600" />
            </div>
            {getChangeIndicator(5.7)}
          </div>
          
          <div className="bg-purple-50 p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-2xl font-bold text-gray-900">{formatNumber(data.totalClicks)}</h3>
                <p className="text-sm text-gray-600">Total Clicks</p>
              </div>
              <MessageCircle className="h-8 w-8 text-purple-600" />
            </div>
            {getChangeIndicator(15.2)}
          </div>
          
          <div className="bg-yellow-50 p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-2xl font-bold text-gray-900">{formatCurrency(data.totalSpend)}</h3>
                <p className="text-sm text-gray-600">Total Spend</p>
              </div>
              <DollarSign className="h-8 w-8 text-yellow-600" />
            </div>
            {getChangeIndicator(-2.1)}
          </div>
        </div>

        {/* Performance Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white p-6 rounded-lg border border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <h4 className="text-sm font-medium text-gray-700">Average CTR</h4>
              <TrendingUp className="h-4 w-4 text-green-600" />
            </div>
            <div className="text-2xl font-bold text-gray-900">{formatPercentage(data.averageCTR)}</div>
            <div className="text-xs text-green-600 mt-1">+0.3% from last period</div>
          </div>
          
          <div className="bg-white p-6 rounded-lg border border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <h4 className="text-sm font-medium text-gray-700">Average CPC</h4>
              <TrendingDown className="h-4 w-4 text-green-600" />
            </div>
            <div className="text-2xl font-bold text-gray-900">{formatCurrency(data.averageCPC)}</div>
            <div className="text-xs text-green-600 mt-1">-$0.08 from last period</div>
          </div>
          
          <div className="bg-white p-6 rounded-lg border border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <h4 className="text-sm font-medium text-gray-700">Average CPM</h4>
              <TrendingUp className="h-4 w-4 text-red-600" />
            </div>
            <div className="text-2xl font-bold text-gray-900">{formatCurrency(data.averageCPM)}</div>
            <div className="text-xs text-red-600 mt-1">+$1.25 from last period</div>
          </div>
          
          <div className="bg-white p-6 rounded-lg border border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <h4 className="text-sm font-medium text-gray-700">Conversion Rate</h4>
              <Target className="h-4 w-4 text-blue-600" />
            </div>
            <div className="text-2xl font-bold text-gray-900">{formatPercentage(data.conversionRate)}</div>
            <div className="text-xs text-blue-600 mt-1">+0.4% from last period</div>
          </div>
        </div>

        {/* Platform Performance Breakdown */}
        <div className="bg-white rounded-lg border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Platform Performance</h3>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {Object.entries(data.platformBreakdown).map(([platformId, metrics]) => {
                const platform = socialPlatforms.find(p => p.id === platformId);
                if (!platform) return null;
                
                const IconComponent = platform.icon;
                const engagementRate = calculateEngagementRate(metrics.engagement, metrics.reach);
                
                return (
                  <div key={platformId} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-3">
                        <div className={`p-2 rounded-lg ${platform.color}`}>
                          <IconComponent className="h-5 w-5" />
                        </div>
                        <div>
                          <h4 className="font-semibold text-gray-900">{platform.name}</h4>
                          <p className="text-sm text-gray-600">{formatNumber(metrics.followers)} followers</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm text-gray-600">Growth Rate</div>
                        {getChangeIndicator(metrics.growth)}
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-6 gap-4 text-sm">
                      <div>
                        <span className="text-gray-600">Reach</span>
                        <div className="font-medium text-lg">{formatNumber(metrics.reach)}</div>
                      </div>
                      <div>
                        <span className="text-gray-600">Engagement</span>
                        <div className="font-medium text-lg">{formatNumber(metrics.engagement)}</div>
                      </div>
                      <div>
                        <span className="text-gray-600">Impressions</span>
                        <div className="font-medium text-lg">{formatNumber(metrics.impressions)}</div>
                      </div>
                      <div>
                        <span className="text-gray-600">Clicks</span>
                        <div className="font-medium text-lg">{formatNumber(metrics.clicks)}</div>
                      </div>
                      <div>
                        <span className="text-gray-600">CTR</span>
                        <div className="font-medium text-lg">{formatPercentage(metrics.ctr)}</div>
                      </div>
                      <div>
                        <span className="text-gray-600">Spend</span>
                        <div className="font-medium text-lg">{formatCurrency(metrics.spend)}</div>
                      </div>
                    </div>
                    
                    <div className="mt-3">
                      <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
                        <span>Engagement Rate</span>
                        <span>{formatPercentage(engagementRate)}</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-pink-500 h-2 rounded-full transition-all duration-300" 
                          style={{ width: `${Math.min(engagementRate * 10, 100)}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Top Performing Content & Audience Demographics */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Top Content */}
          <div className="bg-white rounded-lg border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                <TrendingUp className="mr-2 h-5 w-5" />
                Top Performing Content
              </h3>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {data.topContent.map((content, index) => {
                  const IconComponent = getPlatformIcon(content.platform);
                  return (
                    <div key={content.id} className="flex items-start space-x-3 p-3 rounded-lg bg-gray-50">
                      <div className="flex items-center space-x-2">
                        <span className="flex items-center justify-center w-6 h-6 bg-blue-100 text-blue-600 rounded-full text-sm font-medium">
                          {index + 1}
                        </span>
                        <IconComponent className="h-4 w-4 text-gray-600" />
                      </div>
                      <div className="flex-1">
                        <p className="text-sm text-gray-800 line-clamp-2 mb-2">{content.content}</p>
                        <div className="flex items-center space-x-4 text-xs text-gray-600">
                          <span className="flex items-center">
                            <Heart className="h-3 w-3 mr-1" />
                            {formatNumber(content.engagement)}
                          </span>
                          <span className="flex items-center">
                            <Eye className="h-3 w-3 mr-1" />
                            {formatNumber(content.reach)}
                          </span>
                          <span className="flex items-center">
                            <MessageCircle className="h-3 w-3 mr-1" />
                            {formatNumber(content.clicks)}
                          </span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Audience Demographics */}
          <div className="bg-white rounded-lg border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                <Users className="mr-2 h-5 w-5" />
                Audience Demographics
              </h3>
            </div>
            <div className="p-6 space-y-6">
              {/* Age Groups */}
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-3">Age Distribution</h4>
                <div className="space-y-2">
                  {Object.entries(data.audienceDemographics.ageGroups).map(([age, percentage]) => (
                    <div key={age} className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">{age}</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-500 h-2 rounded-full" 
                            style={{ width: `${(percentage / 40) * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-sm text-gray-900 w-10 text-right">{percentage}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Gender Distribution */}
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-3">Gender Distribution</h4>
                <div className="space-y-2">
                  {Object.entries(data.audienceDemographics.genders).map(([gender, percentage]) => (
                    <div key={gender} className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">{gender}</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-pink-500 h-2 rounded-full" 
                            style={{ width: `${(percentage / 60) * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-sm text-gray-900 w-10 text-right">{percentage}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Top Locations */}
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-3">Top Locations</h4>
                <div className="space-y-2">
                  {Object.entries(data.audienceDemographics.locations).map(([location, percentage]) => (
                    <div key={location} className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">{location}</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-green-500 h-2 rounded-full" 
                            style={{ width: `${(percentage / 50) * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-sm text-gray-900 w-10 text-right">{percentage}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Time Series Chart Placeholder */}
        <div className="bg-white rounded-lg border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Performance Trends</h3>
              <div className="flex items-center space-x-2">
                {metricTypes.map(metric => {
                  const IconComponent = metric.icon;
                  return (
                    <button
                      key={metric.id}
                      onClick={() => setSelectedMetric(metric.id)}
                      className={`flex items-center px-3 py-1 rounded-lg text-sm transition-colors ${
                        selectedMetric === metric.id
                          ? 'bg-blue-100 text-blue-700'
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                      }`}
                    >
                      <IconComponent className="h-4 w-4 mr-1" />
                      {metric.name}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
          <div className="p-6">
            {/* Simplified chart representation */}
            <div className="h-64 flex items-end justify-between space-x-2">
              {data.timeSeriesData.map((point, index) => {
                const value = point[selectedMetric as keyof typeof point] as number;
                const maxValue = Math.max(...data.timeSeriesData.map(p => p[selectedMetric as keyof typeof p] as number));
                const height = (value / maxValue) * 200;
                
                return (
                  <div key={index} className="flex-1 flex flex-col items-center">
                    <div 
                      className="w-full bg-blue-500 rounded-t-lg transition-all duration-500"
                      style={{ height: `${height}px` }}
                    ></div>
                    <div className="text-xs text-gray-600 mt-2 transform rotate-45">
                      {new Date(point.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}