'use client';

import React, { useState } from 'react';
import { GoogleAdsCampaignWizard } from './wizard/GoogleAdsCampaignWizard';
import { SocialMediaCampaignWizard } from './wizard/SocialMediaCampaignWizard';
import { EmailMarketingWizard } from './wizard/EmailMarketingWizard';
import {
  Target, Users, Mail, ArrowLeft, Rocket, TrendingUp,
  DollarSign, BarChart3, Clock, Zap
} from 'lucide-react';

interface CampaignType {
  id: string;
  title: string;
  description: string;
  icon: React.ComponentType<any>;
  color: string;
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  estimatedTime: string;
  features: string[];
  metrics: {
    avgROI: string;
    setupTime: string;
    reach: string;
  };
}

const CAMPAIGN_TYPES: CampaignType[] = [
  {
    id: 'google-ads',
    title: 'Google Ads Campaign',
    description: 'Create high-converting search and display campaigns with AI-powered optimization',
    icon: Target,
    color: '#4285F4',
    difficulty: 'Intermediate',
    estimatedTime: '15-20 minutes',
    features: [
      'Keyword research & targeting',
      'Automated bid optimization',
      'A/B testing capabilities',
      'Conversion tracking',
      'Performance analytics',
      'Budget management'
    ],
    metrics: {
      avgROI: '300%',
      setupTime: '15 min',
      reach: '2.8B+ users'
    }
  },
  {
    id: 'social-media',
    title: 'Social Media Campaign',
    description: 'Launch multi-platform social campaigns across Facebook, Instagram, Twitter, LinkedIn & YouTube',
    icon: Users,
    color: '#E4405F',
    difficulty: 'Beginner',
    estimatedTime: '10-15 minutes',
    features: [
      'Multi-platform management',
      'Advanced audience targeting',
      'Creative asset optimization',
      'Engagement tracking',
      'Influencer integration',
      'Social listening'
    ],
    metrics: {
      avgROI: '250%',
      setupTime: '12 min',
      reach: '4.2B+ users'
    }
  },
  {
    id: 'email-marketing',
    title: 'Email Marketing Campaign',
    description: 'Build personalized email campaigns with automation, segmentation, and advanced analytics',
    icon: Mail,
    color: '#10B981',
    difficulty: 'Beginner',
    estimatedTime: '8-12 minutes',
    features: [
      'Drag & drop builder',
      'Advanced segmentation',
      'Automation workflows',
      'Personalization engine',
      'Deliverability optimization',
      'A/B testing'
    ],
    metrics: {
      avgROI: '420%',
      setupTime: '10 min',
      reach: '1B+ inboxes'
    }
  }
];

// Default data structures for each campaign type
const getDefaultGoogleAdsData = () => ({
  objective: null,
  targeting: {
    demographics: { ageRange: { min: 18, max: 65 }, genders: ['all'], incomeLevel: [] },
    geographic: { countries: [], regions: [], cities: [], radiusKm: 50 },
    interests: [],
    keywords: [],
    behaviors: [],
    customAudiences: []
  },
  creative: {
    type: 'text' as const,
    headlines: [],
    descriptions: [],
    callToActions: [],
    landingUrl: '',
    displayUrl: '',
    images: [],
    videos: []
  },
  budget: {
    budgetType: 'daily' as const,
    amount: 50,
    currency: 'USD',
    bidStrategy: 'target_cpa' as const,
    startDate: new Date().toISOString().split('T')[0],
    endDate: undefined,
    schedule: []
  },
  tracking: {
    goals: [],
    gtmContainer: '',
    googleAnalytics: '',
    facebookPixel: '',
    customEvents: []
  },
  review: {
    campaignName: '',
    estimatedReach: 0,
    estimatedClicks: 0,
    estimatedCost: 0,
    qualityScore: 0,
    recommendations: [],
    launchType: 'draft' as const,
    scheduledDate: undefined
  }
});

const getDefaultSocialMediaData = () => ({
  objective: null,
  audience: {
    segments: [
      { id: '1', name: 'Young Professionals', selected: false, size: 50000, criteria: { demographics: {}, behaviors: ['tech-savvy', 'career-focused'], engagement: ['high'], purchaseHistory: [] } },
      { id: '2', name: 'Small Business Owners', selected: false, size: 25000, criteria: { demographics: {}, behaviors: ['entrepreneurial', 'decision-makers'], engagement: ['medium'], purchaseHistory: ['business-tools'] } },
      { id: '3', name: 'Marketing Enthusiasts', selected: false, size: 30000, criteria: { demographics: {}, behaviors: ['marketing-interested', 'early-adopters'], engagement: ['high'], purchaseHistory: ['marketing-software'] } }
    ],
    customLists: [],
    exclusions: [],
    suppressions: [],
    demographics: { ageRange: { min: 18, max: 65 }, genders: ['all'], languages: ['en'] },
    interests: [],
    behaviors: [],
    customAudiences: [],
    lookalikeSources: [],
    geographic: { countries: [], regions: [], cities: [] }
  },
  creative: {
    platforms: [],
    postTypes: [],
    content: {
      primaryText: '',
      headlines: [],
      callToActions: [],
      hashtags: [],
      mentions: []
    },
    media: { images: [], videos: [], captions: [] },
    scheduling: { frequency: 'weekly' as const, bestTimes: [], timezone: 'UTC' }
  },
  budget: {
    totalBudget: 100,
    currency: 'USD',
    budgetType: 'daily' as const,
    bidStrategy: 'lowest_cost' as const,
    optimization: 'engagement' as const,
    platformAllocation: {},
    duration: { startDate: new Date().toISOString().split('T')[0], endDate: undefined, totalDays: 7 }
  },
  analytics: {
    objectives: [],
    tracking: {
      pixelIds: {},
      utmParameters: { source: 'social', medium: 'social', campaign: '', content: '', term: '' },
      conversionEvents: []
    },
    reporting: { frequency: 'weekly' as const, metrics: [], dashboardUrl: '' }
  }
});

const getDefaultEmailMarketingData = () => ({
  campaignType: null,
  audience: {
    segments: [
      { id: '1', name: 'Newsletter Subscribers', selected: false, size: 15000, criteria: { demographics: {}, behaviors: ['engaged'], engagement: ['newsletter-opens'], purchaseHistory: [] } },
      { id: '2', name: 'Recent Customers', selected: false, size: 8500, criteria: { demographics: {}, behaviors: ['purchased'], engagement: ['recent-buyers'], purchaseHistory: ['last-30-days'] } },
      { id: '3', name: 'Trial Users', selected: false, size: 12000, criteria: { demographics: {}, behaviors: ['trial-users'], engagement: ['product-interested'], purchaseHistory: [] } }
    ],
    customLists: [],
    exclusions: [],
    suppressions: []
  },
  content: {
    template: {
      type: 'newsletter' as const,
      style: 'minimal' as const,
      colors: { primary: '#3B82F6', secondary: '#64748B', accent: '#10B981', background: '#FFFFFF' }
    },
    content: {
      subjectLine: '',
      preheader: '',
      headline: '',
      bodyText: '',
      callToAction: [],
      footer: 'You received this email because you subscribed to our newsletter. Unsubscribe anytime.'
    },
    personalization: {
      useFirstName: false,
      useCompanyName: false,
      usePurchaseHistory: false,
      customFields: [],
      dynamicContent: false
    },
    media: { logo: '', headerImage: '', productImages: [], socialIcons: true }
  },
  delivery: {
    scheduling: {
      type: 'immediate' as const,
      scheduleDate: undefined,
      scheduleTime: undefined,
      timezone: 'UTC',
      frequency: undefined,
      dripSequence: []
    },
    optimization: {
      sendTimeOptimization: false,
      subjectLineTests: [],
      contentTests: [],
      frequencyOptimization: false,
      deliverabilityOptimization: true
    },
    limits: {
      maxPerHour: 1000,
      maxPerDay: 10000,
      respectUnsubscribes: true,
      honorOptouts: true
    }
  },
  tracking: {
    tracking: {
      opens: true,
      clicks: true,
      conversions: true,
      revenue: false,
      unsubscribes: true,
      forwards: false,
      socialShares: false
    },
    goals: [],
    integration: {
      googleAnalytics: '',
      facebookPixel: '',
      customEvents: [],
      webhooks: []
    },
    automation: {
      autoResponders: false,
      listManagement: true,
      segmentUpdates: true,
      reportingSchedule: 'weekly' as const
    }
  }
});

export function CampaignWizardSelector() {
  const [selectedCampaign, setSelectedCampaign] = useState<string | null>(null);
  const [googleAdsData, setGoogleAdsData] = useState(getDefaultGoogleAdsData());
  const [socialMediaData, setSocialMediaData] = useState(getDefaultSocialMediaData());
  const [emailMarketingData, setEmailMarketingData] = useState(getDefaultEmailMarketingData());

  const handleBack = () => {
    setSelectedCampaign(null);
  };

  const validateData = () => {
    // Basic validation - each wizard handles its own detailed validation
    return true;
  };

  if (selectedCampaign === 'google-ads') {
    return (
      <div>
        <div className="mb-6">
          <button
            onClick={handleBack}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-4"
          >
            <ArrowLeft size={16} />
            Back to Campaign Selection
          </button>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Google Ads Campaign Wizard</h1>
          <p className="text-gray-600 dark:text-gray-400">Create and launch your Google Ads campaign in 6 easy steps</p>
        </div>
        <GoogleAdsCampaignWizard
          data={googleAdsData}
          onUpdate={setGoogleAdsData}
          onValidate={validateData}
        />
      </div>
    );
  }

  if (selectedCampaign === 'social-media') {
    return (
      <div>
        <div className="mb-6">
          <button
            onClick={handleBack}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-4"
          >
            <ArrowLeft size={16} />
            Back to Campaign Selection
          </button>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Social Media Campaign Wizard</h1>
          <p className="text-gray-600 dark:text-gray-400">Launch your multi-platform social media campaign in 5 steps</p>
        </div>
        <SocialMediaCampaignWizard
          data={socialMediaData}
          onUpdate={setSocialMediaData}
          onValidate={validateData}
        />
      </div>
    );
  }

  if (selectedCampaign === 'email-marketing') {
    return (
      <div>
        <div className="mb-6">
          <button
            onClick={handleBack}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-4"
          >
            <ArrowLeft size={16} />
            Back to Campaign Selection
          </button>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Email Marketing Campaign Wizard</h1>
          <p className="text-gray-600 dark:text-gray-400">Create your personalized email campaign in 5 steps</p>
        </div>
        <EmailMarketingWizard
          data={emailMarketingData}
          onUpdate={setEmailMarketingData}
          onValidate={validateData}
        />
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Campaign Creation Wizards
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          Choose your campaign type and launch professional marketing campaigns with our
          step-by-step wizards powered by AI optimization.
        </p>
      </div>

      {/* Campaign Type Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
        {CAMPAIGN_TYPES.map((campaign) => {
          const Icon = campaign.icon;
          return (
            <div
              key={campaign.id}
              className="bg-white dark:bg-slate-900 rounded-xl border border-gray-200 dark:border-slate-800 p-6 hover:shadow-lg transition-all cursor-pointer group"
              onClick={() => setSelectedCampaign(campaign.id)}
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center">
                  <div
                    className="w-12 h-12 rounded-lg flex items-center justify-center mr-4"
                    style={{ backgroundColor: campaign.color + '20' }}
                  >
                    <Icon size={24} style={{ color: campaign.color }} />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white group-hover:text-gray-700 dark:group-hover:text-gray-300">
                      {campaign.title}
                    </h3>
                    <div className="flex items-center gap-2 mt-1">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${campaign.difficulty === 'Beginner' ? 'bg-green-100 text-green-800' :
                          campaign.difficulty === 'Intermediate' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                        }`}>
                        {campaign.difficulty}
                      </span>
                      <span className="text-xs text-gray-500 flex items-center">
                        <Clock size={12} className="mr-1" />
                        {campaign.estimatedTime}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Description */}
              <p className="text-gray-600 dark:text-gray-400 text-sm mb-4 leading-relaxed">
                {campaign.description}
              </p>

              {/* Metrics */}
              <div className="grid grid-cols-3 gap-3 mb-4">
                <div className="text-center">
                  <div className="text-lg font-bold text-gray-900 dark:text-white">{campaign.metrics.avgROI}</div>
                  <div className="text-xs text-gray-500">Avg ROI</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-gray-900 dark:text-white">{campaign.metrics.setupTime}</div>
                  <div className="text-xs text-gray-500">Setup</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-gray-900 dark:text-white">{campaign.metrics.reach}</div>
                  <div className="text-xs text-gray-500">Reach</div>
                </div>
              </div>

              {/* Features */}
              <div className="mb-6">
                <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-2">Key Features:</h4>
                <div className="space-y-1">
                  {campaign.features.slice(0, 4).map((feature, index) => (
                    <div key={index} className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                      <div className="w-1.5 h-1.5 rounded-full bg-gray-400 mr-2"></div>
                      {feature}
                    </div>
                  ))}
                  {campaign.features.length > 4 && (
                    <div className="text-sm text-gray-500">
                      +{campaign.features.length - 4} more features
                    </div>
                  )}
                </div>
              </div>

              {/* Action Button */}
              <button
                className="w-full bg-gray-900 text-white py-3 px-4 rounded-lg font-medium hover:bg-gray-800 transition-colors flex items-center justify-center gap-2 group-hover:bg-gray-800"
                style={{ backgroundColor: campaign.color }}
              >
                <Rocket size={16} />
                Start {campaign.title}
              </button>
            </div>
          );
        })}
      </div>

      {/* Benefits Section */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-xl p-8">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Why Use Our Campaign Wizards?
          </h2>
          <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Our AI-powered wizards simplify complex campaign creation while ensuring
            professional results and optimal performance.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center mx-auto mb-3">
              <Zap size={24} className="text-blue-600 dark:text-blue-400" />
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Fast Setup</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Launch campaigns in minutes, not hours, with our streamlined process.
            </p>
          </div>

          <div className="text-center">
            <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center mx-auto mb-3">
              <TrendingUp size={24} className="text-green-600 dark:text-green-400" />
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">AI Optimization</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Benefit from AI-powered recommendations and automatic optimizations.
            </p>
          </div>

          <div className="text-center">
            <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center mx-auto mb-3">
              <BarChart3 size={24} className="text-purple-600 dark:text-purple-400" />
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Advanced Analytics</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Track performance with comprehensive analytics and reporting.
            </p>
          </div>

          <div className="text-center">
            <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center mx-auto mb-3">
              <DollarSign size={24} className="text-orange-600 dark:text-orange-400" />
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">ROI Focused</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Every feature is designed to maximize your return on investment.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}