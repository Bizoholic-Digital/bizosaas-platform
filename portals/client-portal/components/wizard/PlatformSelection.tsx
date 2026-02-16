'use client';

import React, { useState, useEffect } from 'react';
import {
  Target, TrendingUp, Clock, CheckCircle, Star, Lightbulb,
  Zap, BarChart3, DollarSign, Users, Search, MapPin,
  Chrome, Facebook, Apple, MessageSquare, Camera,
  AlertTriangle, Info, Filter, SortAsc, Eye
} from 'lucide-react';

interface PlatformFeature {
  name: string;
  description: string;
  importance: 'high' | 'medium' | 'low';
}

interface PlatformConfig {
  id: string;
  name: string;
  description: string;
  icon: React.ComponentType;
  tier: 1 | 2 | 3;
  enabled: boolean;
  connected: boolean;
  estimatedRoi: number;
  difficulty: 'easy' | 'medium' | 'hard';
  timeToSetup: string;
  monthlyViews: number;
  averageRating: number;
  reviewCount: number;
  features: PlatformFeature[];
  pricing: {
    free: boolean;
    monthlyFee?: number;
    setupFee?: number;
  };
  requirements: string[];
  benefits: string[];
  businessTypes: string[];
  demographics: {
    primaryAge: string;
    income: string;
    usage: string;
  };
}

interface AIRecommendations {
  recommendedPlatforms: string[];
  businessInsights: string[];
  optimizationTips: string[];
  competitorAnalysis: {
    platforms: string[];
    averageRating: number;
    gapsIdentified: string[];
    marketOpportunities: string[];
  };
  roiProjections: {
    [platformId: string]: {
      estimatedLeads: number;
      estimatedRevenue: number;
      confidence: number;
    };
  };
}

interface PlatformSelectionProps {
  platforms: PlatformConfig[];
  onUpdate: (platforms: PlatformConfig[]) => void;
  aiRecommendations: AIRecommendations | null;
  businessProfile: any;
  onAnalyze: () => void;
  isAnalyzing: boolean;
}

const PLATFORM_DATA: PlatformConfig[] = [
  {
    id: 'google-business',
    name: 'Google Business Profile',
    description: 'Essential for local search visibility and Google Maps presence',
    icon: Chrome,
    tier: 1,
    enabled: false,
    connected: false,
    estimatedRoi: 95,
    difficulty: 'easy',
    timeToSetup: '10-15 minutes',
    monthlyViews: 125000,
    averageRating: 4.8,
    reviewCount: 50000,
    features: [
      { name: 'Google Maps Listing', description: 'Appear in local map searches', importance: 'high' },
      { name: 'Google Search Results', description: 'Show in business search results', importance: 'high' },
      { name: 'Customer Reviews', description: 'Collect and respond to reviews', importance: 'high' },
      { name: 'Business Posts', description: 'Share updates and offers', importance: 'medium' },
      { name: 'Q&A Section', description: 'Answer customer questions', importance: 'medium' },
      { name: 'Analytics Dashboard', description: 'Track views and engagement', importance: 'high' }
    ],
    pricing: { free: true },
    requirements: ['Business address', 'Phone number', 'Business verification'],
    benefits: [
      'Highest local search visibility',
      'Free to use and maintain',
      'Integrated with Google Ads',
      'Real-time analytics',
      'Mobile-optimized'
    ],
    businessTypes: ['retail', 'restaurant', 'service', 'healthcare', 'all'],
    demographics: {
      primaryAge: '25-65',
      income: 'All income levels',
      usage: '92% of local searches'
    }
  },
  {
    id: 'yelp',
    name: 'Yelp Business',
    description: 'Leading review platform for restaurants and local services',
    icon: Star,
    tier: 1,
    enabled: false,
    connected: false,
    estimatedRoi: 85,
    difficulty: 'easy',
    timeToSetup: '5-10 minutes',
    monthlyViews: 45000,
    averageRating: 4.5,
    reviewCount: 30000,
    features: [
      { name: 'Customer Reviews', description: 'Detailed customer feedback system', importance: 'high' },
      { name: 'Photo Sharing', description: 'Customer and business photos', importance: 'high' },
      { name: 'Business Information', description: 'Detailed business profiles', importance: 'high' },
      { name: 'Special Offers', description: 'Promote deals and discounts', importance: 'medium' },
      { name: 'Events Listing', description: 'Promote business events', importance: 'medium' },
      { name: 'Message Center', description: 'Direct customer communication', importance: 'low' }
    ],
    pricing: { free: true, monthlyFee: 299 },
    requirements: ['Business verification', 'Quality photos', 'Accurate business info'],
    benefits: [
      'Strong review ecosystem',
      'High consumer trust',
      'Mobile app integration',
      'Advertising opportunities',
      'Detailed analytics'
    ],
    businessTypes: ['restaurant', 'retail', 'service', 'beauty', 'healthcare'],
    demographics: {
      primaryAge: '25-45',
      income: 'Middle to high income',
      usage: '35% of local searches'
    }
  },
  {
    id: 'facebook',
    name: 'Facebook Business',
    description: 'Social media presence with business page and local features',
    icon: Facebook,
    tier: 1,
    enabled: false,
    connected: false,
    estimatedRoi: 80,
    difficulty: 'medium',
    timeToSetup: '15-20 minutes',
    monthlyViews: 38000,
    averageRating: 4.3,
    reviewCount: 25000,
    features: [
      { name: 'Business Page', description: 'Professional business presence', importance: 'high' },
      { name: 'Customer Reviews', description: 'Facebook review system', importance: 'high' },
      { name: 'Events Creation', description: 'Promote and manage events', importance: 'medium' },
      { name: 'Messenger Integration', description: 'Customer support via Messenger', importance: 'medium' },
      { name: 'Facebook Ads', description: 'Integrated advertising platform', importance: 'high' },
      { name: 'Insights Analytics', description: 'Detailed audience analytics', importance: 'medium' }
    ],
    pricing: { free: true },
    requirements: ['Facebook account', 'Business verification', 'Content strategy'],
    benefits: [
      'Massive user base',
      'Advanced targeting options',
      'Event promotion capabilities',
      'Social proof through likes/shares',
      'Integration with Instagram'
    ],
    businessTypes: ['retail', 'restaurant', 'service', 'entertainment', 'all'],
    demographics: {
      primaryAge: '25-55',
      income: 'All income levels',
      usage: '68% of adults use Facebook'
    }
  },
  {
    id: 'apple-maps',
    name: 'Apple Maps Business',
    description: 'iOS and Mac users local search and navigation',
    icon: Apple,
    tier: 1,
    enabled: false,
    connected: false,
    estimatedRoi: 70,
    difficulty: 'medium',
    timeToSetup: '10-15 minutes',
    monthlyViews: 22000,
    averageRating: 4.4,
    reviewCount: 15000,
    features: [
      { name: 'Apple Maps Listing', description: 'Appear in Apple Maps searches', importance: 'high' },
      { name: 'iOS Integration', description: 'Native iOS experience', importance: 'high' },
      { name: 'Business Information', description: 'Detailed business profiles', importance: 'high' },
      { name: 'Photos Gallery', description: 'Business photo showcase', importance: 'medium' },
      { name: 'Hours and Contact', description: 'Operating hours and contact info', importance: 'high' },
      { name: 'Navigation Integration', description: 'Turn-by-turn directions', importance: 'medium' }
    ],
    pricing: { free: true },
    requirements: ['Apple Developer account', 'Business verification', 'High-quality photos'],
    benefits: [
      'High-income iOS user base',
      'Premium user experience',
      'Native device integration',
      'Less competition than other platforms',
      'Strong local search presence'
    ],
    businessTypes: ['retail', 'restaurant', 'service', 'professional'],
    demographics: {
      primaryAge: '25-50',
      income: 'Higher income demographic',
      usage: '25% of smartphone users'
    }
  },
  {
    id: 'bing-places',
    name: 'Bing Places for Business',
    description: 'Microsoft search engine and Windows integration',
    icon: Search,
    tier: 2,
    enabled: false,
    connected: false,
    estimatedRoi: 60,
    difficulty: 'easy',
    timeToSetup: '5-10 minutes',
    monthlyViews: 8500,
    averageRating: 4.1,
    reviewCount: 8000,
    features: [
      { name: 'Bing Search Results', description: 'Appear in Bing search results', importance: 'medium' },
      { name: 'Maps Integration', description: 'Bing Maps business listing', importance: 'medium' },
      { name: 'Business Information', description: 'Complete business profiles', importance: 'high' },
      { name: 'Photos and Videos', description: 'Media showcase capabilities', importance: 'low' },
      { name: 'Customer Reviews', description: 'Review collection system', importance: 'medium' },
      { name: 'Analytics Dashboard', description: 'Performance tracking', importance: 'low' }
    ],
    pricing: { free: true },
    requirements: ['Microsoft account', 'Business verification', 'Accurate business data'],
    benefits: [
      'Less competitive than Google',
      'Good for B2B businesses',
      'Windows integration',
      'Free to use',
      'Quick setup process'
    ],
    businessTypes: ['professional', 'service', 'b2b', 'retail'],
    demographics: {
      primaryAge: '35-65',
      income: 'Business professionals',
      usage: '12% of search market'
    }
  }
];

export function PlatformSelection({
  platforms,
  onUpdate,
  aiRecommendations,
  businessProfile,
  onAnalyze,
  isAnalyzing
}: PlatformSelectionProps) {
  const [sortBy, setSortBy] = useState<'roi' | 'tier' | 'popularity' | 'difficulty'>('tier');
  const [filterTier, setFilterTier] = useState<number | null>(null);
  const [showDetails, setShowDetails] = useState<string | null>(null);

  const sortedPlatforms = [...platforms].sort((a, b) => {
    switch (sortBy) {
      case 'roi':
        return b.estimatedRoi - a.estimatedRoi;
      case 'tier':
        return a.tier - b.tier;
      case 'popularity':
        return b.monthlyViews - a.monthlyViews;
      case 'difficulty':
        const difficultyOrder = { 'easy': 1, 'medium': 2, 'hard': 3 };
        return difficultyOrder[a.difficulty] - difficultyOrder[b.difficulty];
      default:
        return 0;
    }
  });

  const filteredPlatforms = filterTier 
    ? sortedPlatforms.filter(p => p.tier === filterTier)
    : sortedPlatforms;

  const togglePlatform = (platformId: string) => {
    const updatedPlatforms = platforms.map(p =>
      p.id === platformId ? { ...p, enabled: !p.enabled } : p
    );
    onUpdate(updatedPlatforms);
  };

  const getSelectedPlatformsStats = () => {
    const selected = platforms.filter(p => p.enabled);
    return {
      count: selected.length,
      avgRoi: selected.length > 0 ? Math.round(selected.reduce((sum, p) => sum + p.estimatedRoi, 0) / selected.length) : 0,
      totalViews: selected.reduce((sum, p) => sum + p.monthlyViews, 0),
      estimatedCost: selected.reduce((sum, p) => sum + (p.pricing.monthlyFee || 0), 0)
    };
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'text-green-600 bg-green-100 dark:bg-green-900/30 dark:text-green-400';
      case 'medium': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30 dark:text-yellow-400';
      case 'hard': return 'text-red-600 bg-red-100 dark:bg-red-900/30 dark:text-red-400';
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-700 dark:text-gray-400';
    }
  };

  const getTierLabel = (tier: number) => {
    switch (tier) {
      case 1: return { label: 'Essential', color: 'text-gold-600 bg-gold-100 dark:bg-gold-900/30' };
      case 2: return { label: 'Recommended', color: 'text-silver-600 bg-silver-100 dark:bg-silver-900/30' };
      case 3: return { label: 'Optional', color: 'text-bronze-600 bg-bronze-100 dark:bg-bronze-900/30' };
      default: return { label: 'Standard', color: 'text-gray-600 bg-gray-100 dark:bg-gray-700' };
    }
  };

  return (
    <div className="space-y-6">
      {/* AI Recommendations Panel */}
      {aiRecommendations && (
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 p-6 rounded-lg border border-blue-200 dark:border-blue-800">
          <div className="flex items-center mb-4">
            <Lightbulb className="w-6 h-6 text-blue-600 dark:text-blue-400 mr-3" />
            <h4 className="text-lg font-semibold text-gray-900 dark:text-white">AI-Powered Platform Recommendations</h4>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg">
              <h5 className="font-medium text-gray-900 dark:text-white mb-3 flex items-center">
                <Zap className="w-4 h-4 mr-2 text-yellow-500" />
                Business Insights
              </h5>
              <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-2">
                {aiRecommendations.businessInsights.map((insight, index) => (
                  <li key={index} className="flex items-start">
                    <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                    {insight}
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg">
              <h5 className="font-medium text-gray-900 dark:text-white mb-3 flex items-center">
                <TrendingUp className="w-4 h-4 mr-2 text-blue-500" />
                Market Opportunities
              </h5>
              <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-2">
                {aiRecommendations.competitorAnalysis.marketOpportunities.map((opportunity, index) => (
                  <li key={index} className="flex items-start">
                    <Target className="w-4 h-4 text-blue-500 mr-2 mt-0.5 flex-shrink-0" />
                    {opportunity}
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg">
              <h5 className="font-medium text-gray-900 dark:text-white mb-3 flex items-center">
                <BarChart3 className="w-4 h-4 mr-2 text-purple-500" />
                Competitor Analysis
              </h5>
              <div className="text-sm text-gray-600 dark:text-gray-400 space-y-2">
                <div className="flex items-center justify-between">
                  <span>Avg Competitor Rating:</span>
                  <div className="flex items-center">
                    <Star className="w-3 h-3 text-yellow-500 mr-1" />
                    <span className="font-medium">{aiRecommendations.competitorAnalysis.averageRating}</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span>Active Platforms:</span>
                  <span className="font-medium">{aiRecommendations.competitorAnalysis.platforms.length}</span>
                </div>
                <div className="text-xs text-purple-600 dark:text-purple-400 mt-2">
                  {aiRecommendations.competitorAnalysis.gapsIdentified.length} gaps identified
                </div>
              </div>
            </div>
          </div>

          <div className="bg-blue-600 text-white p-4 rounded-lg">
            <h5 className="font-semibold mb-2 flex items-center">
              <Target className="w-4 h-4 mr-2" />
              Recommended Platform Strategy
            </h5>
            <p className="text-sm text-blue-100 mb-3">
              Based on your business profile, we recommend focusing on these platforms for maximum impact:
            </p>
            <div className="flex flex-wrap gap-2">
              {aiRecommendations.recommendedPlatforms.map(platformId => {
                const platform = platforms.find(p => p.id === platformId);
                return platform ? (
                  <span key={platformId} className="px-3 py-1 bg-blue-500 rounded-full text-sm font-medium">
                    {platform.name}
                  </span>
                ) : null;
              })}
            </div>
          </div>
        </div>
      )}

      {/* Analysis Trigger */}
      {!aiRecommendations && (
        <div className="text-center bg-gray-50 dark:bg-gray-800 p-8 rounded-lg">
          <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
            <Lightbulb className="w-8 h-8 text-blue-600 dark:text-blue-400" />
          </div>
          <h4 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Get AI-Powered Recommendations</h4>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Let our AI analyze your business profile and provide personalized platform recommendations.
          </p>
          <button
            onClick={onAnalyze}
            disabled={isAnalyzing || !businessProfile?.name}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center mx-auto"
          >
            {isAnalyzing ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                Analyzing Business Profile...
              </>
            ) : (
              <>
                <Lightbulb className="w-5 h-5 mr-2" />
                Analyze & Get Recommendations
              </>
            )}
          </button>
        </div>
      )}

      {/* Filters and Sorting */}
      <div className="flex items-center justify-between bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-gray-600 dark:text-gray-400" />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Filter by Tier:</span>
            <select
              value={filterTier || ''}
              onChange={(e) => setFilterTier(e.target.value ? parseInt(e.target.value) : null)}
              className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
            >
              <option value="">All Tiers</option>
              <option value="1">Tier 1 - Essential</option>
              <option value="2">Tier 2 - Recommended</option>
              <option value="3">Tier 3 - Optional</option>
            </select>
          </div>

          <div className="flex items-center space-x-2">
            <SortAsc className="w-4 h-4 text-gray-600 dark:text-gray-400" />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Sort by:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-sm"
            >
              <option value="tier">Tier</option>
              <option value="roi">ROI Potential</option>
              <option value="popularity">Popularity</option>
              <option value="difficulty">Difficulty</option>
            </select>
          </div>
        </div>

        <div className="text-sm text-gray-600 dark:text-gray-400">
          {getSelectedPlatformsStats().count} platforms selected
        </div>
      </div>

      {/* Platform Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredPlatforms.map(platform => {
          const Icon = platform.icon;
          const tierInfo = getTierLabel(platform.tier);
          const isRecommended = aiRecommendations?.recommendedPlatforms.includes(platform.id);
          const roiProjection = aiRecommendations?.roiProjections[platform.id];

          return (
            <div
              key={platform.id}
              className={`relative p-6 rounded-lg border-2 transition-all cursor-pointer ${
                platform.enabled
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                  : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-gray-300 dark:hover:border-gray-600'
              } ${isRecommended ? 'ring-2 ring-green-500 ring-opacity-50' : ''}`}
              onClick={() => togglePlatform(platform.id)}
            >
              {/* Recommendation Badge */}
              {isRecommended && (
                <div className="absolute -top-2 -right-2 bg-green-500 text-white px-3 py-1 rounded-full text-xs font-semibold">
                  AI Recommended
                </div>
              )}

              {/* Platform Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center">
                  <div className="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center mr-4">
                    <Icon className="w-8 h-8 text-gray-600 dark:text-gray-400" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{platform.name}</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">{platform.description}</p>
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${tierInfo.color}`}>
                        {tierInfo.label}
                      </span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(platform.difficulty)}`}>
                        {platform.difficulty}
                      </span>
                    </div>
                  </div>
                </div>
                <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                  platform.enabled
                    ? 'border-blue-500 bg-blue-500'
                    : 'border-gray-300 dark:border-gray-600'
                }`}>
                  {platform.enabled && <CheckCircle className="w-4 h-4 text-white" />}
                </div>
              </div>

              {/* Platform Stats */}
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div className="text-center">
                  <div className="flex items-center justify-center mb-1">
                    <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
                    <span className="text-lg font-bold text-gray-900 dark:text-white">{platform.estimatedRoi}%</span>
                  </div>
                  <span className="text-xs text-gray-600 dark:text-gray-400">ROI Potential</span>
                </div>
                <div className="text-center">
                  <div className="flex items-center justify-center mb-1">
                    <Eye className="w-4 h-4 text-blue-500 mr-1" />
                    <span className="text-lg font-bold text-gray-900 dark:text-white">
                      {(platform.monthlyViews / 1000).toFixed(0)}K
                    </span>
                  </div>
                  <span className="text-xs text-gray-600 dark:text-gray-400">Monthly Views</span>
                </div>
                <div className="text-center">
                  <div className="flex items-center justify-center mb-1">
                    <Clock className="w-4 h-4 text-purple-500 mr-1" />
                    <span className="text-lg font-bold text-gray-900 dark:text-white">{platform.timeToSetup}</span>
                  </div>
                  <span className="text-xs text-gray-600 dark:text-gray-400">Setup Time</span>
                </div>
              </div>

              {/* ROI Projection */}
              {roiProjection && (
                <div className="bg-green-50 dark:bg-green-900/20 p-3 rounded-lg mb-4">
                  <h5 className="font-semibold text-green-900 dark:text-green-300 text-sm mb-2">AI Projection</h5>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-green-700 dark:text-green-400">Est. Monthly Leads:</span>
                      <span className="ml-2 font-bold">{roiProjection.estimatedLeads}</span>
                    </div>
                    <div>
                      <span className="text-green-700 dark:text-green-400">Est. Monthly Revenue:</span>
                      <span className="ml-2 font-bold">${roiProjection.estimatedRevenue.toLocaleString()}</span>
                    </div>
                  </div>
                  <div className="mt-2">
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-green-600 dark:text-green-400">Confidence Level</span>
                      <span className="font-medium">{roiProjection.confidence}%</span>
                    </div>
                    <div className="w-full bg-green-200 dark:bg-green-800 rounded-full h-1 mt-1">
                      <div 
                        className="bg-green-500 h-1 rounded-full" 
                        style={{ width: `${roiProjection.confidence}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              )}

              {/* Key Features */}
              <div className="mb-4">
                <h5 className="font-medium text-gray-900 dark:text-white mb-2 text-sm">Key Features:</h5>
                <div className="grid grid-cols-2 gap-1">
                  {platform.features.slice(0, 4).map((feature, index) => (
                    <div key={index} className="flex items-center text-xs">
                      <CheckCircle className="w-3 h-3 text-green-500 mr-1 flex-shrink-0" />
                      <span className="text-gray-600 dark:text-gray-400 truncate">{feature.name}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Pricing */}
              <div className="flex items-center justify-between mb-4">
                <div>
                  <span className="text-sm text-gray-600 dark:text-gray-400">Pricing: </span>
                  {platform.pricing.free ? (
                    <span className="text-green-600 dark:text-green-400 font-medium">Free</span>
                  ) : (
                    <span className="text-gray-900 dark:text-white font-medium">
                      ${platform.pricing.monthlyFee}/month
                    </span>
                  )}
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowDetails(showDetails === platform.id ? null : platform.id);
                  }}
                  className="text-blue-600 hover:text-blue-700 dark:text-blue-400 text-sm font-medium"
                >
                  {showDetails === platform.id ? 'Hide Details' : 'View Details'}
                </button>
              </div>

              {/* Detailed Information */}
              {showDetails === platform.id && (
                <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 space-y-4">
                  <div>
                    <h6 className="font-medium text-gray-900 dark:text-white mb-2">All Features:</h6>
                    <div className="space-y-2">
                      {platform.features.map((feature, index) => (
                        <div key={index} className="flex items-start">
                          <div className={`w-2 h-2 rounded-full mt-2 mr-3 ${
                            feature.importance === 'high' ? 'bg-red-500' :
                            feature.importance === 'medium' ? 'bg-yellow-500' :
                            'bg-green-500'
                          }`} />
                          <div>
                            <div className="text-sm font-medium text-gray-900 dark:text-white">{feature.name}</div>
                            <div className="text-xs text-gray-600 dark:text-gray-400">{feature.description}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h6 className="font-medium text-gray-900 dark:text-white mb-2">Requirements:</h6>
                    <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                      {platform.requirements.map((req, index) => (
                        <li key={index} className="flex items-center">
                          <AlertTriangle className="w-3 h-3 text-yellow-500 mr-2" />
                          {req}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h6 className="font-medium text-gray-900 dark:text-white mb-2">Demographics:</h6>
                    <div className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                      <div><strong>Primary Age:</strong> {platform.demographics.primaryAge}</div>
                      <div><strong>Income Level:</strong> {platform.demographics.income}</div>
                      <div><strong>Market Share:</strong> {platform.demographics.usage}</div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Selection Summary */}
      <div className="bg-gradient-to-r from-blue-50 to-green-50 dark:from-blue-900/20 dark:to-green-900/20 p-6 rounded-lg border border-blue-200 dark:border-blue-800">
        <h4 className="font-semibold text-gray-900 dark:text-white mb-4">Selection Summary</h4>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{getSelectedPlatformsStats().count}</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Platforms Selected</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600 dark:text-green-400">{getSelectedPlatformsStats().avgRoi}%</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Average ROI</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
              {(getSelectedPlatformsStats().totalViews / 1000).toFixed(0)}K
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Total Monthly Views</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
              ${getSelectedPlatformsStats().estimatedCost}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Monthly Cost</div>
          </div>
        </div>
      </div>
    </div>
  );
}