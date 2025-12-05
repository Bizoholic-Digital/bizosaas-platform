'use client';

import { useState } from 'react';
import { 
  Users,
  Target,
  MapPin,
  Clock,
  Heart,
  TrendingUp,
  BarChart3,
  PieChart,
  Filter,
  Download,
  RefreshCw,
  Calendar,
  Globe,
  Briefcase,
  GraduationCap,
  ShoppingBag,
  Smartphone,
  Monitor,
  Tablet,
  Facebook,
  Instagram,
  Twitter,
  Linkedin,
  Youtube,
  Video,
  Eye,
  MessageCircle,
  Share2,
  ArrowUpRight,
  ArrowDownRight,
  Settings
} from 'lucide-react';

interface AudienceInsight {
  totalAudience: number;
  audienceGrowth: number;
  platformBreakdown: {
    [platform: string]: {
      followers: number;
      growth: number;
      engagement: number;
      demographics: {
        ageGroups: { [age: string]: number };
        genders: { [gender: string]: number };
        locations: { [location: string]: number };
        devices: { [device: string]: number };
      };
      interests: { [interest: string]: number };
      behaviors: { [behavior: string]: number };
      activeHours: { [hour: string]: number };
      bestPostingTimes: string[];
    };
  };
  crossPlatformInsights: {
    overlapAnalysis: {
      [combination: string]: {
        overlap: number;
        uniqueToFirst: number;
        uniqueToSecond: number;
      };
    };
    loyaltyScore: number;
    engagementConsistency: number;
  };
  recommendedTargeting: {
    ageRange: { min: number; max: number };
    topLocations: string[];
    bestInterests: string[];
    optimalBehaviors: string[];
    recommendedBudgetAllocation: { [platform: string]: number };
  };
  competitorComparison: {
    [competitor: string]: {
      followers: number;
      engagement: number;
      contentStrategy: string[];
      strengths: string[];
      opportunities: string[];
    };
  };
}

const socialPlatforms = [
  { id: 'facebook', name: 'Facebook', icon: Facebook, color: 'text-blue-600 bg-blue-50' },
  { id: 'instagram', name: 'Instagram', icon: Instagram, color: 'text-purple-600 bg-purple-50' },
  { id: 'twitter', name: 'Twitter/X', icon: Twitter, color: 'text-gray-800 bg-gray-50' },
  { id: 'linkedin', name: 'LinkedIn', icon: Linkedin, color: 'text-blue-700 bg-blue-50' },
  { id: 'youtube', name: 'YouTube', icon: Youtube, color: 'text-red-600 bg-red-50' }
];

const mockAudienceData: AudienceInsight = {
  totalAudience: 125847,
  audienceGrowth: 8.5,
  platformBreakdown: {
    facebook: {
      followers: 45230,
      growth: 5.2,
      engagement: 7.2,
      demographics: {
        ageGroups: { '18-24': 15, '25-34': 35, '35-44': 30, '45-54': 15, '55+': 5 },
        genders: { 'Male': 45, 'Female': 53, 'Other': 2 },
        locations: { 'United States': 45, 'Canada': 15, 'United Kingdom': 12, 'Australia': 10, 'Germany': 8, 'Other': 10 },
        devices: { 'Mobile': 78, 'Desktop': 18, 'Tablet': 4 }
      },
      interests: { 'Business': 35, 'Technology': 28, 'Lifestyle': 22, 'Marketing': 20, 'Design': 18, 'Travel': 15 },
      behaviors: { 'Online Shoppers': 45, 'Tech Early Adopters': 38, 'Frequent Travelers': 25, 'Business Decision Makers': 30 },
      activeHours: { '9': 15, '10': 22, '11': 28, '12': 35, '13': 32, '14': 28, '15': 25, '16': 22, '17': 18, '18': 20, '19': 25, '20': 30 },
      bestPostingTimes: ['12:00 PM', '2:00 PM', '8:00 PM']
    },
    instagram: {
      followers: 38542,
      growth: 12.4,
      engagement: 12.4,
      demographics: {
        ageGroups: { '18-24': 40, '25-34': 35, '35-44': 20, '45-54': 4, '55+': 1 },
        genders: { 'Male': 35, 'Female': 63, 'Other': 2 },
        locations: { 'United States': 42, 'Canada': 18, 'United Kingdom': 15, 'Australia': 12, 'Brazil': 6, 'Other': 7 },
        devices: { 'Mobile': 92, 'Desktop': 6, 'Tablet': 2 }
      },
      interests: { 'Fashion': 45, 'Lifestyle': 40, 'Photography': 35, 'Food': 30, 'Travel': 28, 'Art': 25 },
      behaviors: { 'Frequent App Users': 85, 'Visual Content Consumers': 78, 'Brand Followers': 65, 'Influencer Audiences': 55 },
      activeHours: { '7': 18, '8': 25, '9': 20, '12': 22, '17': 28, '18': 35, '19': 40, '20': 45, '21': 38, '22': 25 },
      bestPostingTimes: ['8:00 PM', '7:00 PM', '12:00 PM']
    },
    twitter: {
      followers: 28934,
      growth: 6.8,
      engagement: 6.8,
      demographics: {
        ageGroups: { '18-24': 25, '25-34': 40, '35-44': 25, '45-54': 8, '55+': 2 },
        genders: { 'Male': 58, 'Female': 40, 'Other': 2 },
        locations: { 'United States': 50, 'United Kingdom': 20, 'Canada': 12, 'India': 8, 'Australia': 5, 'Other': 5 },
        devices: { 'Mobile': 82, 'Desktop': 16, 'Tablet': 2 }
      },
      interests: { 'Technology': 55, 'News': 48, 'Politics': 35, 'Sports': 30, 'Business': 28, 'Entertainment': 25 },
      behaviors: { 'News Consumers': 65, 'Opinion Leaders': 45, 'Real-time Engagers': 55, 'Link Clickers': 40 },
      activeHours: { '8': 22, '9': 35, '10': 28, '11': 25, '12': 30, '17': 32, '18': 28, '19': 25, '20': 22, '21': 18 },
      bestPostingTimes: ['9:00 AM', '12:00 PM', '5:00 PM']
    },
    linkedin: {
      followers: 12341,
      growth: 15.3,
      engagement: 5.4,
      demographics: {
        ageGroups: { '18-24': 8, '25-34': 45, '35-44': 35, '45-54': 10, '55+': 2 },
        genders: { 'Male': 55, 'Female': 44, 'Other': 1 },
        locations: { 'United States': 55, 'Canada': 18, 'United Kingdom': 12, 'Germany': 8, 'Netherlands': 4, 'Other': 3 },
        devices: { 'Desktop': 45, 'Mobile': 50, 'Tablet': 5 }
      },
      interests: { 'Professional Development': 65, 'Leadership': 55, 'Industry Trends': 50, 'Networking': 45, 'Recruiting': 35, 'Sales': 30 },
      behaviors: { 'B2B Decision Makers': 55, 'Job Seekers': 35, 'Industry Thought Leaders': 40, 'Professional Networkers': 60 },
      activeHours: { '9': 35, '10': 42, '11': 38, '14': 28, '15': 32, '16': 25, '17': 20, '19': 18, '20': 15 },
      bestPostingTimes: ['10:00 AM', '2:00 PM', '9:00 AM']
    },
    youtube: {
      followers: 8934,
      growth: 18.9,
      engagement: 18.2,
      demographics: {
        ageGroups: { '18-24': 35, '25-34': 30, '35-44': 25, '45-54': 8, '55+': 2 },
        genders: { 'Male': 60, 'Female': 38, 'Other': 2 },
        locations: { 'United States': 48, 'India': 15, 'United Kingdom': 12, 'Canada': 10, 'Germany': 8, 'Other': 7 },
        devices: { 'Mobile': 70, 'Desktop': 25, 'Tablet': 3, 'TV': 2 }
      },
      interests: { 'Technology Reviews': 58, 'Tutorials': 45, 'Entertainment': 40, 'Gaming': 35, 'Education': 30, 'Music': 25 },
      behaviors: { 'Video Consumers': 85, 'Subscribers': 65, 'Comment Engagers': 45, 'Playlist Creators': 30 },
      activeHours: { '18': 25, '19': 40, '20': 55, '21': 48, '22': 35, '15': 22, '16': 28, '17': 32 },
      bestPostingTimes: ['8:00 PM', '7:00 PM', '4:00 PM']
    }
  },
  crossPlatformInsights: {
    overlapAnalysis: {
      'facebook-instagram': { overlap: 35, uniqueToFirst: 45, uniqueToSecond: 20 },
      'twitter-linkedin': { overlap: 25, uniqueToFirst: 55, uniqueToSecond: 20 },
      'instagram-youtube': { overlap: 40, uniqueToFirst: 35, uniqueToSecond: 25 }
    },
    loyaltyScore: 72,
    engagementConsistency: 68
  },
  recommendedTargeting: {
    ageRange: { min: 25, max: 44 },
    topLocations: ['United States', 'Canada', 'United Kingdom', 'Australia'],
    bestInterests: ['Technology', 'Business', 'Marketing', 'Lifestyle', 'Professional Development'],
    optimalBehaviors: ['Online Shoppers', 'Tech Early Adopters', 'Business Decision Makers', 'Professional Networkers'],
    recommendedBudgetAllocation: { 
      facebook: 30, 
      instagram: 25, 
      linkedin: 20, 
      twitter: 15, 
      youtube: 10 
    }
  },
  competitorComparison: {
    'Competitor A': {
      followers: 156000,
      engagement: 9.2,
      contentStrategy: ['Video Content', 'User-Generated Content', 'Behind-the-Scenes'],
      strengths: ['High engagement rate', 'Strong video content', 'Consistent posting'],
      opportunities: ['Limited platform diversity', 'Weak LinkedIn presence', 'Less interactive content']
    },
    'Competitor B': {
      followers: 89000,
      engagement: 6.8,
      contentStrategy: ['Educational Content', 'Industry News', 'Product Showcases'],
      strengths: ['Educational focus', 'Strong LinkedIn presence', 'Professional tone'],
      opportunities: ['Lower engagement', 'Limited visual content', 'Infrequent posting']
    }
  }
};

const timeRanges = [
  { id: '7d', name: 'Last 7 Days' },
  { id: '30d', name: 'Last 30 Days' },
  { id: '90d', name: 'Last 90 Days' },
  { id: '1y', name: 'Last Year' }
];

interface AudienceAnalyzerProps {
  onClose?: () => void;
}

export default function AudienceAnalyzer({ onClose }: AudienceAnalyzerProps) {
  const [selectedTimeRange, setSelectedTimeRange] = useState('30d');
  const [selectedPlatform, setSelectedPlatform] = useState('all');
  const [activeTab, setActiveTab] = useState<'overview' | 'demographics' | 'behavior' | 'competitor' | 'recommendations'>('overview');
  const [data] = useState<AudienceInsight>(mockAudienceData);

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  const formatPercentage = (value: number) => {
    return `${value.toFixed(1)}%`;
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

  const getPlatformIcon = (platformId: string) => {
    const platform = socialPlatforms.find(p => p.id === platformId);
    return platform ? platform.icon : Globe;
  };

  const getPlatformData = () => {
    if (selectedPlatform === 'all') {
      return null;
    }
    return data.platformBreakdown[selectedPlatform];
  };

  return (
    <div className="bg-white rounded-lg shadow-lg border border-gray-200">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-semibold text-gray-900 flex items-center">
            <Users className="mr-2 h-6 w-6" />
            Audience Analyzer
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
              value={selectedPlatform}
              onChange={(e) => setSelectedPlatform(e.target.value)}
              className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Platforms</option>
              {socialPlatforms.map(platform => (
                <option key={platform.id} value={platform.id}>{platform.name}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex space-x-6 mt-4">
          {[
            { id: 'overview', name: 'Overview', icon: BarChart3 },
            { id: 'demographics', name: 'Demographics', icon: Users },
            { id: 'behavior', name: 'Behavior', icon: Target },
            { id: 'competitor', name: 'Competitor Analysis', icon: TrendingUp },
            { id: 'recommendations', name: 'Recommendations', icon: Settings }
          ].map(tab => {
            const IconComponent = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center pb-2 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <IconComponent className="mr-2 h-4 w-4" />
                {tab.name}
              </button>
            );
          })}
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {activeTab === 'overview' && (
          <div className="space-y-8">
            {/* Audience Overview Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-blue-50 p-6 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900">{formatNumber(data.totalAudience)}</h3>
                    <p className="text-sm text-gray-600">Total Audience</p>
                  </div>
                  <Users className="h-8 w-8 text-blue-600" />
                </div>
                {getChangeIndicator(data.audienceGrowth)}
              </div>
              
              <div className="bg-green-50 p-6 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900">{data.crossPlatformInsights.loyaltyScore}</h3>
                    <p className="text-sm text-gray-600">Loyalty Score</p>
                  </div>
                  <Heart className="h-8 w-8 text-green-600" />
                </div>
                <span className="text-green-600 text-sm">Strong loyalty</span>
              </div>
              
              <div className="bg-purple-50 p-6 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900">{data.crossPlatformInsights.engagementConsistency}</h3>
                    <p className="text-sm text-gray-600">Engagement Consistency</p>
                  </div>
                  <BarChart3 className="h-8 w-8 text-purple-600" />
                </div>
                <span className="text-purple-600 text-sm">Good consistency</span>
              </div>
              
              <div className="bg-orange-50 p-6 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900">{socialPlatforms.length}</h3>
                    <p className="text-sm text-gray-600">Active Platforms</p>
                  </div>
                  <Globe className="h-8 w-8 text-orange-600" />
                </div>
                <span className="text-orange-600 text-sm">Multi-platform presence</span>
              </div>
            </div>

            {/* Platform Breakdown */}
            <div className="bg-white rounded-lg border border-gray-200">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">Platform Audience Breakdown</h3>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {Object.entries(data.platformBreakdown).map(([platformId, metrics]) => {
                    const platform = socialPlatforms.find(p => p.id === platformId);
                    if (!platform) return null;
                    
                    const IconComponent = platform.icon;
                    
                    return (
                      <div key={platformId} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                        <div className="flex items-center space-x-4">
                          <div className={`p-2 rounded-lg ${platform.color}`}>
                            <IconComponent className="h-5 w-5" />
                          </div>
                          <div>
                            <h4 className="font-semibold text-gray-900">{platform.name}</h4>
                            <p className="text-sm text-gray-600">{formatNumber(metrics.followers)} followers</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-6 text-sm">
                          <div className="text-center">
                            <div className="font-medium text-gray-900">{formatPercentage(metrics.engagement)}</div>
                            <div className="text-gray-600">Engagement</div>
                          </div>
                          <div className="text-center">
                            {getChangeIndicator(metrics.growth)}
                            <div className="text-gray-600">Growth</div>
                          </div>
                          <div className="text-center">
                            <div className="font-medium text-gray-900">{metrics.bestPostingTimes[0]}</div>
                            <div className="text-gray-600">Best Time</div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Cross-Platform Insights */}
            <div className="bg-white rounded-lg border border-gray-200">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">Cross-Platform Audience Overlap</h3>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {Object.entries(data.crossPlatformInsights.overlapAnalysis).map(([combination, overlap]) => {
                    const [platform1, platform2] = combination.split('-');
                    const Icon1 = getPlatformIcon(platform1);
                    const Icon2 = getPlatformIcon(platform2);
                    
                    return (
                      <div key={combination} className="p-4 bg-gray-50 rounded-lg">
                        <div className="flex items-center justify-between mb-3">
                          <div className="flex items-center space-x-2">
                            <Icon1 className="h-4 w-4" />
                            <span className="text-sm text-gray-600">×</span>
                            <Icon2 className="h-4 w-4" />
                          </div>
                          <span className="text-lg font-semibold text-blue-600">{overlap.overlap}%</span>
                        </div>
                        <div className="text-xs text-gray-600 space-y-1">
                          <div>Unique to {platform1}: {overlap.uniqueToFirst}%</div>
                          <div>Unique to {platform2}: {overlap.uniqueToSecond}%</div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'demographics' && (
          <div className="space-y-8">
            {selectedPlatform === 'all' ? (
              <div className="text-center py-8">
                <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Select a Platform</h3>
                <p className="text-gray-600">Choose a specific platform to view detailed demographic data.</p>
              </div>
            ) : (
              (() => {
                const platformData = getPlatformData();
                if (!platformData) return null;
                
                return (
                  <div className="space-y-8">
                    {/* Age Demographics */}
                    <div className="bg-white rounded-lg border border-gray-200">
                      <div className="px-6 py-4 border-b border-gray-200">
                        <h3 className="text-lg font-semibold text-gray-900">Age Distribution</h3>
                      </div>
                      <div className="p-6">
                        <div className="space-y-4">
                          {Object.entries(platformData.demographics.ageGroups).map(([age, percentage]) => (
                            <div key={age} className="flex items-center justify-between">
                              <span className="text-sm font-medium text-gray-700">{age} years</span>
                              <div className="flex items-center space-x-3 flex-1 ml-4">
                                <div className="flex-1 bg-gray-200 rounded-full h-3">
                                  <div 
                                    className="bg-blue-500 h-3 rounded-full transition-all duration-300" 
                                    style={{ width: `${(percentage / 45) * 100}%` }}
                                  ></div>
                                </div>
                                <span className="text-sm font-medium text-gray-900 w-12 text-right">{percentage}%</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>

                    {/* Gender & Location */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                      <div className="bg-white rounded-lg border border-gray-200">
                        <div className="px-6 py-4 border-b border-gray-200">
                          <h3 className="text-lg font-semibold text-gray-900">Gender Distribution</h3>
                        </div>
                        <div className="p-6">
                          <div className="space-y-4">
                            {Object.entries(platformData.demographics.genders).map(([gender, percentage]) => (
                              <div key={gender} className="flex items-center justify-between">
                                <span className="text-sm font-medium text-gray-700">{gender}</span>
                                <div className="flex items-center space-x-3 flex-1 ml-4">
                                  <div className="flex-1 bg-gray-200 rounded-full h-3">
                                    <div 
                                      className={`h-3 rounded-full transition-all duration-300 ${
                                        gender === 'Male' ? 'bg-blue-500' : 
                                        gender === 'Female' ? 'bg-pink-500' : 'bg-purple-500'
                                      }`}
                                      style={{ width: `${(percentage / 65) * 100}%` }}
                                    ></div>
                                  </div>
                                  <span className="text-sm font-medium text-gray-900 w-12 text-right">{percentage}%</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>

                      <div className="bg-white rounded-lg border border-gray-200">
                        <div className="px-6 py-4 border-b border-gray-200">
                          <h3 className="text-lg font-semibold text-gray-900">Top Locations</h3>
                        </div>
                        <div className="p-6">
                          <div className="space-y-4">
                            {Object.entries(platformData.demographics.locations).map(([location, percentage]) => (
                              <div key={location} className="flex items-center justify-between">
                                <span className="text-sm font-medium text-gray-700">{location}</span>
                                <div className="flex items-center space-x-3 flex-1 ml-4">
                                  <div className="flex-1 bg-gray-200 rounded-full h-3">
                                    <div 
                                      className="bg-green-500 h-3 rounded-full transition-all duration-300" 
                                      style={{ width: `${(percentage / 55) * 100}%` }}
                                    ></div>
                                  </div>
                                  <span className="text-sm font-medium text-gray-900 w-12 text-right">{percentage}%</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Device Usage */}
                    <div className="bg-white rounded-lg border border-gray-200">
                      <div className="px-6 py-4 border-b border-gray-200">
                        <h3 className="text-lg font-semibold text-gray-900">Device Usage</h3>
                      </div>
                      <div className="p-6">
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                          {Object.entries(platformData.demographics.devices).map(([device, percentage]) => {
                            const DeviceIcon = device === 'Mobile' ? Smartphone : 
                                             device === 'Desktop' ? Monitor : 
                                             device === 'Tablet' ? Tablet : Monitor;
                            
                            return (
                              <div key={device} className="text-center">
                                <div className="flex items-center justify-center mb-2">
                                  <DeviceIcon className="h-8 w-8 text-gray-600" />
                                </div>
                                <div className="text-2xl font-bold text-gray-900">{percentage}%</div>
                                <div className="text-sm text-gray-600">{device}</div>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })()
            )}
          </div>
        )}

        {activeTab === 'behavior' && (
          <div className="space-y-8">
            {selectedPlatform === 'all' ? (
              <div className="text-center py-8">
                <Target className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Select a Platform</h3>
                <p className="text-gray-600">Choose a specific platform to view detailed behavioral data.</p>
              </div>
            ) : (
              (() => {
                const platformData = getPlatformData();
                if (!platformData) return null;
                
                return (
                  <div className="space-y-8">
                    {/* Interests & Behaviors */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                      <div className="bg-white rounded-lg border border-gray-200">
                        <div className="px-6 py-4 border-b border-gray-200">
                          <h3 className="text-lg font-semibold text-gray-900">Top Interests</h3>
                        </div>
                        <div className="p-6">
                          <div className="space-y-4">
                            {Object.entries(platformData.interests).map(([interest, percentage]) => (
                              <div key={interest} className="flex items-center justify-between">
                                <span className="text-sm font-medium text-gray-700">{interest}</span>
                                <div className="flex items-center space-x-3 flex-1 ml-4">
                                  <div className="flex-1 bg-gray-200 rounded-full h-3">
                                    <div 
                                      className="bg-purple-500 h-3 rounded-full transition-all duration-300" 
                                      style={{ width: `${(percentage / 65) * 100}%` }}
                                    ></div>
                                  </div>
                                  <span className="text-sm font-medium text-gray-900 w-12 text-right">{percentage}%</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>

                      <div className="bg-white rounded-lg border border-gray-200">
                        <div className="px-6 py-4 border-b border-gray-200">
                          <h3 className="text-lg font-semibold text-gray-900">User Behaviors</h3>
                        </div>
                        <div className="p-6">
                          <div className="space-y-4">
                            {Object.entries(platformData.behaviors).map(([behavior, percentage]) => (
                              <div key={behavior} className="flex items-center justify-between">
                                <span className="text-sm font-medium text-gray-700">{behavior}</span>
                                <div className="flex items-center space-x-3 flex-1 ml-4">
                                  <div className="flex-1 bg-gray-200 rounded-full h-3">
                                    <div 
                                      className="bg-orange-500 h-3 rounded-full transition-all duration-300" 
                                      style={{ width: `${(percentage / 85) * 100}%` }}
                                    ></div>
                                  </div>
                                  <span className="text-sm font-medium text-gray-900 w-12 text-right">{percentage}%</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Active Hours */}
                    <div className="bg-white rounded-lg border border-gray-200">
                      <div className="px-6 py-4 border-b border-gray-200">
                        <h3 className="text-lg font-semibold text-gray-900">Audience Activity by Hour</h3>
                      </div>
                      <div className="p-6">
                        <div className="flex items-end justify-between space-x-1 h-64">
                          {Object.entries(platformData.activeHours).map(([hour, activity]) => {
                            const maxActivity = Math.max(...Object.values(platformData.activeHours));
                            const height = (activity / maxActivity) * 200;
                            const hourNum = parseInt(hour);
                            const timeLabel = hourNum === 0 ? '12 AM' : 
                                            hourNum < 12 ? `${hourNum} AM` : 
                                            hourNum === 12 ? '12 PM' : `${hourNum - 12} PM`;
                            
                            return (
                              <div key={hour} className="flex-1 flex flex-col items-center">
                                <div 
                                  className="w-full bg-blue-500 rounded-t-lg transition-all duration-500 relative group cursor-pointer"
                                  style={{ height: `${height}px` }}
                                >
                                  <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity">
                                    {activity}% active
                                  </div>
                                </div>
                                <div className="text-xs text-gray-600 mt-2 transform rotate-45 origin-left">
                                  {timeLabel}
                                </div>
                              </div>
                            );
                          })}
                        </div>
                        <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                          <h4 className="font-medium text-gray-900 mb-2">Recommended Posting Times:</h4>
                          <div className="flex items-center space-x-4">
                            {platformData.bestPostingTimes.map((time, index) => (
                              <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                                {time}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })()
            )}
          </div>
        )}

        {activeTab === 'competitor' && (
          <div className="space-y-8">
            <div className="grid gap-6">
              {Object.entries(data.competitorComparison).map(([competitor, metrics]) => (
                <div key={competitor} className="bg-white rounded-lg border border-gray-200">
                  <div className="px-6 py-4 border-b border-gray-200">
                    <h3 className="text-lg font-semibold text-gray-900">{competitor}</h3>
                  </div>
                  <div className="p-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-medium text-gray-900 mb-3">Performance Metrics</h4>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span className="text-gray-600">Followers:</span>
                            <span className="font-medium">{formatNumber(metrics.followers)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Engagement Rate:</span>
                            <span className="font-medium">{formatPercentage(metrics.engagement)}</span>
                          </div>
                        </div>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900 mb-3">Content Strategy</h4>
                        <div className="flex flex-wrap gap-2">
                          {metrics.contentStrategy.map((strategy, index) => (
                            <span key={index} className="px-2 py-1 bg-gray-100 text-gray-800 rounded text-sm">
                              {strategy}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
                      <div>
                        <h4 className="font-medium text-gray-900 mb-3">Strengths</h4>
                        <ul className="space-y-1">
                          {metrics.strengths.map((strength, index) => (
                            <li key={index} className="text-sm text-green-700 flex items-center">
                              <TrendingUp className="h-3 w-3 mr-2" />
                              {strength}
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900 mb-3">Opportunities</h4>
                        <ul className="space-y-1">
                          {metrics.opportunities.map((opportunity, index) => (
                            <li key={index} className="text-sm text-orange-700 flex items-center">
                              <Target className="h-3 w-3 mr-2" />
                              {opportunity}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'recommendations' && (
          <div className="space-y-8">
            {/* Targeting Recommendations */}
            <div className="bg-white rounded-lg border border-gray-200">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">Recommended Targeting</h3>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-3">Demographics</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Age Range:</span>
                        <span className="font-medium">
                          {data.recommendedTargeting.ageRange.min}-{data.recommendedTargeting.ageRange.max} years
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-600 block mb-2">Top Locations:</span>
                        <div className="flex flex-wrap gap-2">
                          {data.recommendedTargeting.topLocations.map((location, index) => (
                            <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">
                              {location}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900 mb-3">Interests & Behaviors</h4>
                    <div className="space-y-3">
                      <div>
                        <span className="text-gray-600 block mb-2">Best Interests:</span>
                        <div className="flex flex-wrap gap-2">
                          {data.recommendedTargeting.bestInterests.map((interest, index) => (
                            <span key={index} className="px-2 py-1 bg-green-100 text-green-800 rounded text-sm">
                              {interest}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div>
                        <span className="text-gray-600 block mb-2">Optimal Behaviors:</span>
                        <div className="flex flex-wrap gap-2">
                          {data.recommendedTargeting.optimalBehaviors.map((behavior, index) => (
                            <span key={index} className="px-2 py-1 bg-purple-100 text-purple-800 rounded text-sm">
                              {behavior}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Budget Allocation */}
            <div className="bg-white rounded-lg border border-gray-200">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">Recommended Budget Allocation</h3>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {Object.entries(data.recommendedTargeting.recommendedBudgetAllocation).map(([platform, percentage]) => {
                    const platformInfo = socialPlatforms.find(p => p.id === platform);
                    if (!platformInfo) return null;
                    
                    const IconComponent = platformInfo.icon;
                    
                    return (
                      <div key={platform} className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <IconComponent className="h-5 w-5" />
                          <span className="font-medium text-gray-700">{platformInfo.name}</span>
                        </div>
                        <div className="flex items-center space-x-3 flex-1 ml-4">
                          <div className="flex-1 bg-gray-200 rounded-full h-3">
                            <div 
                              className="bg-blue-500 h-3 rounded-full transition-all duration-300" 
                              style={{ width: `${percentage * 2}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-medium text-gray-900 w-12 text-right">{percentage}%</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
                <div className="mt-6 p-4 bg-yellow-50 rounded-lg">
                  <h4 className="font-medium text-yellow-800 mb-2">Budget Allocation Tips:</h4>
                  <ul className="text-sm text-yellow-700 space-y-1">
                    <li>• Allocate more budget to platforms with higher engagement rates</li>
                    <li>• Consider your target demographic preferences for each platform</li>
                    <li>• Test small budgets initially before scaling successful campaigns</li>
                    <li>• Monitor performance and adjust allocation based on ROI</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}