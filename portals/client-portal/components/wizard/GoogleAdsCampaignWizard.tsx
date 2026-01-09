'use client';

import React, { useState } from 'react';
import {
  Target, DollarSign, Users, Edit3, BarChart3, Rocket,
  Plus, Minus, X, Check, AlertCircle, CheckCircle,
  Calendar, Clock, MapPin, Globe, Smartphone, Monitor, Sparkles
} from 'lucide-react';

interface CampaignObjective {
  type: 'awareness' | 'traffic' | 'leads' | 'sales' | 'app_promotion' | 'brand_consideration';
  label: string;
  description: string;
  recommendedBudget: { min: number; max: number };
}

interface TargetingCriteria {
  demographics: {
    ageRange: { min: number; max: number };
    genders: string[];
    incomeLevel: string[];
  };
  geographic: {
    countries: string[];
    regions: string[];
    cities: string[];
    radiusKm: number;
  };
  interests: string[];
  keywords: string[];
  behaviors: string[];
  customAudiences: string[];
}

interface AdCreative {
  type: 'text' | 'display' | 'video' | 'shopping' | 'performance_max';
  headlines: string[];
  descriptions: string[];
  callToActions: string[];
  landingUrl: string;
  displayUrl?: string;
  images: string[];
  videos: string[];
}

interface BudgetSchedule {
  budgetType: 'daily' | 'total';
  amount: number;
  currency: string;
  bidStrategy: 'manual_cpc' | 'target_cpa' | 'target_roas' | 'maximize_clicks' | 'maximize_conversions';
  startDate: string;
  endDate?: string;
  schedule: {
    dayOfWeek: string;
    startTime: string;
    endTime: string;
    active: boolean;
  }[];
}

interface ConversionTracking {
  goals: {
    name: string;
    type: 'purchase' | 'lead' | 'signup' | 'download' | 'call' | 'custom';
    value: number;
    currency: string;
  }[];
  gtmContainer?: string;
  googleAnalytics?: string;
  facebookPixel?: string;
  customEvents: string[];
}

interface ReviewLaunch {
  campaignName: string;
  estimatedReach: number;
  estimatedClicks: number;
  estimatedCost: number;
  qualityScore: number;
  recommendations: string[];
  launchType: 'immediate' | 'scheduled' | 'draft';
  scheduledDate?: string;
}

interface GoogleAdsCampaignData {
  objective: CampaignObjective | null;
  targeting: TargetingCriteria;
  creative: AdCreative;
  budget: BudgetSchedule;
  tracking: ConversionTracking;
  review: ReviewLaunch;
}

interface GoogleAdsCampaignWizardProps {
  data: GoogleAdsCampaignData;
  onUpdate: (data: GoogleAdsCampaignData) => void;
  onValidate: () => boolean;
}

const CAMPAIGN_OBJECTIVES: CampaignObjective[] = [
  {
    type: 'awareness',
    label: 'Brand Awareness',
    description: 'Increase visibility and reach for your brand',
    recommendedBudget: { min: 20, max: 100 }
  },
  {
    type: 'traffic',
    label: 'Website Traffic',
    description: 'Drive visitors to your website or landing page',
    recommendedBudget: { min: 15, max: 75 }
  },
  {
    type: 'leads',
    label: 'Lead Generation',
    description: 'Collect leads and contact information',
    recommendedBudget: { min: 25, max: 150 }
  },
  {
    type: 'sales',
    label: 'Sales & Conversions',
    description: 'Drive purchases and revenue',
    recommendedBudget: { min: 30, max: 200 }
  },
  {
    type: 'app_promotion',
    label: 'App Promotion',
    description: 'Increase app downloads and engagement',
    recommendedBudget: { min: 20, max: 120 }
  },
  {
    type: 'brand_consideration',
    label: 'Brand Consideration',
    description: 'Encourage people to learn more about your brand',
    recommendedBudget: { min: 18, max: 90 }
  }
];

const BID_STRATEGIES = [
  { value: 'manual_cpc', label: 'Manual CPC', description: 'You set the maximum cost per click' },
  { value: 'target_cpa', label: 'Target CPA', description: 'Google optimizes for cost per acquisition' },
  { value: 'target_roas', label: 'Target ROAS', description: 'Optimize for return on ad spend' },
  { value: 'maximize_clicks', label: 'Maximize Clicks', description: 'Get the most clicks within budget' },
  { value: 'maximize_conversions', label: 'Maximize Conversions', description: 'Get the most conversions within budget' }
];

const AD_TYPES = [
  { value: 'text', label: 'Search Ads', description: 'Text ads that appear in search results' },
  { value: 'display', label: 'Display Ads', description: 'Visual ads on websites and apps' },
  { value: 'video', label: 'Video Ads', description: 'Video ads on YouTube and partner sites' },
  { value: 'shopping', label: 'Shopping Ads', description: 'Product ads with images and pricing' },
  { value: 'performance_max', label: 'Performance Max', description: 'AI-optimized ads across all channels' }
];

export function GoogleAdsCampaignWizard({ data, onUpdate, onValidate }: GoogleAdsCampaignWizardProps) {
  const [currentStep, setCurrentStep] = useState(1);
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  const steps = [
    { number: 1, title: 'Campaign Objective', icon: Target },
    { number: 2, title: 'Audience Targeting', icon: Users },
    { number: 3, title: 'Ad Creative', icon: Edit3 },
    { number: 4, title: 'Budget & Schedule', icon: DollarSign },
    { number: 5, title: 'Conversion Tracking', icon: BarChart3 },
    { number: 6, title: 'Review & Launch', icon: Rocket }
  ];

  const updateData = (updates: Partial<GoogleAdsCampaignData>) => {
    onUpdate({ ...data, ...updates });
  };

  const validateStep = (step: number): boolean => {
    const errors: Record<string, string> = {};

    switch (step) {
      case 1:
        if (!data.objective) errors.objective = 'Please select a campaign objective';
        break;
      case 2:
        if (data.targeting.keywords.length === 0) errors.keywords = 'Add at least one keyword';
        if (data.targeting.geographic.countries.length === 0) errors.location = 'Select at least one location';
        break;
      case 3:
        if (data.creative.headlines.length === 0) errors.headlines = 'Add at least one headline';
        if (data.creative.descriptions.length === 0) errors.descriptions = 'Add at least one description';
        if (!data.creative.landingUrl) errors.landingUrl = 'Landing URL is required';
        break;
      case 4:
        if (data.budget.amount <= 0) errors.budget = 'Budget must be greater than 0';
        if (!data.budget.startDate) errors.startDate = 'Start date is required';
        break;
      case 5:
        if (data.tracking.goals.length === 0) errors.goals = 'Add at least one conversion goal';
        break;
      case 6:
        if (!data.review.campaignName) errors.campaignName = 'Campaign name is required';
        break;
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const nextStep = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(Math.min(currentStep + 1, steps.length));
    }
  };

  const prevStep = () => {
    setCurrentStep(Math.max(currentStep - 1, 1));
  };

  const addKeyword = (keyword: string) => {
    if (keyword && !data.targeting.keywords.includes(keyword)) {
      updateData({
        targeting: {
          ...data.targeting,
          keywords: [...data.targeting.keywords, keyword]
        }
      });
    }
  };

  const removeKeyword = (keyword: string) => {
    updateData({
      targeting: {
        ...data.targeting,
        keywords: data.targeting.keywords.filter(k => k !== keyword)
      }
    });
  };

  const addHeadline = (headline: string) => {
    if (headline && data.creative.headlines.length < 15) {
      updateData({
        creative: {
          ...data.creative,
          headlines: [...data.creative.headlines, headline]
        }
      });
    }
  };

  const removeHeadline = (index: number) => {
    updateData({
      creative: {
        ...data.creative,
        headlines: data.creative.headlines.filter((_, i) => i !== index)
      }
    });
  };

  const addDescription = (description: string) => {
    if (description && data.creative.descriptions.length < 4) {
      updateData({
        creative: {
          ...data.creative,
          descriptions: [...data.creative.descriptions, description]
        }
      });
    }
  };

  const removeDescription = (index: number) => {
    updateData({
      creative: {
        ...data.creative,
        descriptions: data.creative.descriptions.filter((_, i) => i !== index)
      }
    });
  };

  const addConversionGoal = () => {
    updateData({
      tracking: {
        ...data.tracking,
        goals: [...data.tracking.goals, {
          name: '',
          type: 'purchase',
          value: 0,
          currency: 'USD'
        }]
      }
    });
  };

  const updateConversionGoal = (index: number, updates: Partial<ConversionTracking['goals'][0]>) => {
    const newGoals = [...data.tracking.goals];
    newGoals[index] = { ...newGoals[index], ...updates };
    updateData({
      tracking: {
        ...data.tracking,
        goals: newGoals
      }
    });
  };

  const removeConversionGoal = (index: number) => {
    updateData({
      tracking: {
        ...data.tracking,
        goals: data.tracking.goals.filter((_, i) => i !== index)
      }
    });
  };

  const renderStep1 = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">What's your main campaign objective?</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {CAMPAIGN_OBJECTIVES.map((objective) => (
            <div
              key={objective.type}
              className={`border rounded-lg p-4 cursor-pointer transition-all ${data.objective?.type === objective.type
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300'
                }`}
              onClick={() => updateData({ objective })}
            >
              <h4 className="font-medium text-gray-900 dark:text-white">{objective.label}</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{objective.description}</p>
              <p className="text-xs text-gray-500 mt-2">
                Recommended: ${objective.recommendedBudget.min}-${objective.recommendedBudget.max}/day
              </p>
            </div>
          ))}
        </div>
        {validationErrors.objective && (
          <p className="text-red-500 text-sm mt-2">{validationErrors.objective}</p>
        )}
      </div>
    </div>
  );

  const renderStep2 = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Define your target audience</h3>

        {/* Keywords */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Keywords (what people search for)
          </label>
          <div className="flex flex-wrap gap-2 mb-2">
            {data.targeting.keywords.map((keyword, index) => (
              <span
                key={index}
                className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800"
              >
                {keyword}
                <button
                  onClick={() => removeKeyword(keyword)}
                  className="ml-2 hover:text-blue-600"
                >
                  <X size={14} />
                </button>
              </span>
            ))}
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Add keyword (e.g., 'digital marketing')"
              className="flex-1 border border-gray-300 rounded-lg px-3 py-2"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  addKeyword((e.target as HTMLInputElement).value);
                  (e.target as HTMLInputElement).value = '';
                }
              }}
            />
            <button
              onClick={() => {
                const input = document.querySelector('input[placeholder*="Add keyword"]') as HTMLInputElement;
                if (input.value) {
                  addKeyword(input.value);
                  input.value = '';
                }
              }}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              <Plus size={16} />
            </button>
          </div>
          <div className="mt-2">
            <button
              onClick={() => {
                const suggestions = ['digital marketing', 'online advertising', 'ppc agency', 'social media ads', 'google ads expert'];
                suggestions.forEach(k => addKeyword(k));
              }}
              className="text-sm text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1"
            >
              <Sparkles size={14} /> Auto-suggest from website
            </button>
          </div>
          {validationErrors.keywords && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.keywords}</p>
          )}
        </div>

        {/* Demographics */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Age Range</label>
          <div className="flex gap-4">
            <select
              value={data.targeting.demographics.ageRange.min}
              onChange={(e) => updateData({
                targeting: {
                  ...data.targeting,
                  demographics: {
                    ...data.targeting.demographics,
                    ageRange: {
                      ...data.targeting.demographics.ageRange,
                      min: parseInt(e.target.value)
                    }
                  }
                }
              })}
              className="border border-gray-300 rounded-lg px-3 py-2"
            >
              {[18, 25, 35, 45, 55, 65].map(age => (
                <option key={age} value={age}>{age}+</option>
              ))}
            </select>
            <span className="py-2">to</span>
            <select
              value={data.targeting.demographics.ageRange.max}
              onChange={(e) => updateData({
                targeting: {
                  ...data.targeting,
                  demographics: {
                    ...data.targeting.demographics,
                    ageRange: {
                      ...data.targeting.demographics.ageRange,
                      max: parseInt(e.target.value)
                    }
                  }
                }
              })}
              className="border border-gray-300 rounded-lg px-3 py-2"
            >
              {[25, 35, 45, 55, 65, 100].map(age => (
                <option key={age} value={age}>{age === 100 ? '65+' : age}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Location */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Geographic Targeting</label>
          <div className="space-y-2">
            <select
              className="w-full border border-gray-300 dark:border-gray-700 rounded-lg px-3 py-2 bg-white dark:bg-slate-900 dark:text-white"
              onChange={(e) => {
                const location = e.target.value;
                if (location && !data.targeting.geographic.countries.includes(location)) {
                  updateData({
                    targeting: {
                      ...data.targeting,
                      geographic: {
                        ...data.targeting.geographic,
                        countries: [...data.targeting.geographic.countries, location]
                      }
                    }
                  });
                }
                e.target.value = '';
              }}
            >
              <option value="">Select a Country...</option>
              <option value="United States">United States</option>
              <option value="United Kingdom">United Kingdom</option>
              <option value="Canada">Canada</option>
              <option value="Australia">Australia</option>
              <option value="India">India</option>
              <option value="Germany">Germany</option>
              <option value="France">France</option>
            </select>
            <div className="flex flex-wrap gap-2">
              {data.targeting.geographic.countries.map((location, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-green-100 text-green-800"
                >
                  <MapPin size={12} className="mr-1" />
                  {location}
                  <button
                    onClick={() => updateData({
                      targeting: {
                        ...data.targeting,
                        geographic: {
                          ...data.targeting.geographic,
                          countries: data.targeting.geographic.countries.filter((_, i) => i !== index)
                        }
                      }
                    })}
                    className="ml-2 hover:text-green-600"
                  >
                    <X size={14} />
                  </button>
                </span>
              ))}
            </div>
          </div>
          {validationErrors.location && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.location}</p>
          )}
        </div>
      </div>
    </div>
  );

  const renderStep3 = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Create your ad creative</h3>

        {/* Ad Type */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Ad Type</label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {AD_TYPES.map((type) => (
              <div
                key={type.value}
                className={`border rounded-lg p-3 cursor-pointer transition-all ${data.creative.type === type.value
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
                  }`}
                onClick={() => updateData({
                  creative: { ...data.creative, type: type.value as AdCreative['type'] }
                })}
              >
                <h4 className="font-medium text-gray-900">{type.label}</h4>
                <p className="text-sm text-gray-600">{type.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Headlines */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Headlines (up to 15, 30 characters each)
          </label>
          <div className="space-y-2">
            {data.creative.headlines.map((headline, index) => (
              <div key={index} className="flex gap-2">
                <input
                  type="text"
                  value={headline}
                  onChange={(e) => {
                    const newHeadlines = [...data.creative.headlines];
                    newHeadlines[index] = e.target.value;
                    updateData({
                      creative: { ...data.creative, headlines: newHeadlines }
                    });
                  }}
                  maxLength={30}
                  className="flex-1 border border-gray-300 rounded-lg px-3 py-2"
                  placeholder={`Headline ${index + 1}`}
                />
                <button
                  onClick={() => removeHeadline(index)}
                  className="px-3 py-2 text-red-600 hover:text-red-700"
                >
                  <X size={16} />
                </button>
              </div>
            ))}
            {data.creative.headlines.length < 15 && (
              <button
                onClick={() => addHeadline('')}
                className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-gray-600 hover:text-gray-700"
              >
                <Plus size={16} />
                Add Headline
              </button>
            )}
          </div>
          {validationErrors.headlines && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.headlines}</p>
          )}
        </div>

        {/* Descriptions */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Descriptions (up to 4, 90 characters each)
          </label>
          <div className="space-y-2">
            {data.creative.descriptions.map((description, index) => (
              <div key={index} className="flex gap-2">
                <textarea
                  value={description}
                  onChange={(e) => {
                    const newDescriptions = [...data.creative.descriptions];
                    newDescriptions[index] = e.target.value;
                    updateData({
                      creative: { ...data.creative, descriptions: newDescriptions }
                    });
                  }}
                  maxLength={90}
                  rows={2}
                  className="flex-1 border border-gray-300 rounded-lg px-3 py-2"
                  placeholder={`Description ${index + 1}`}
                />
                <button
                  onClick={() => removeDescription(index)}
                  className="px-3 py-2 text-red-600 hover:text-red-700"
                >
                  <X size={16} />
                </button>
              </div>
            ))}
            {data.creative.descriptions.length < 4 && (
              <button
                onClick={() => addDescription('')}
                className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-gray-600 hover:text-gray-700"
              >
                <Plus size={16} />
                Add Description
              </button>
            )}
          </div>
          {validationErrors.descriptions && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.descriptions}</p>
          )}
        </div>

        {/* Landing URL */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Landing Page URL</label>
          <input
            type="url"
            value={data.creative.landingUrl}
            onChange={(e) => updateData({
              creative: { ...data.creative, landingUrl: e.target.value }
            })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
            placeholder="https://your-website.com/landing-page"
          />
          {validationErrors.landingUrl && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.landingUrl}</p>
          )}
        </div>
      </div>
    </div>
  );

  const renderStep4 = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Set your budget and schedule</h3>

        {/* Budget */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Budget Type</label>
          <div className="flex gap-4 mb-4">
            <label className="flex items-center">
              <input
                type="radio"
                checked={data.budget.budgetType === 'daily'}
                onChange={() => updateData({
                  budget: { ...data.budget, budgetType: 'daily' }
                })}
                className="mr-2"
              />
              Daily Budget
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                checked={data.budget.budgetType === 'total'}
                onChange={() => updateData({
                  budget: { ...data.budget, budgetType: 'total' }
                })}
                className="mr-2"
              />
              Total Budget
            </label>
          </div>
          <div className="flex gap-2">
            <select
              value={data.budget.currency}
              onChange={(e) => updateData({
                budget: { ...data.budget, currency: e.target.value }
              })}
              className="border border-gray-300 rounded-lg px-3 py-2"
            >
              <option value="USD">USD</option>
              <option value="EUR">EUR</option>
              <option value="GBP">GBP</option>
              <option value="INR">INR</option>
            </select>
            <input
              type="number"
              value={data.budget.amount}
              onChange={(e) => updateData({
                budget: { ...data.budget, amount: parseFloat(e.target.value) || 0 }
              })}
              min="1"
              className="flex-1 border border-gray-300 rounded-lg px-3 py-2"
              placeholder="Enter amount"
            />
          </div>
          {validationErrors.budget && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.budget}</p>
          )}
        </div>

        {/* Bidding Strategy */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Bidding Strategy</label>
          <div className="space-y-2">
            {BID_STRATEGIES.map((strategy) => (
              <div
                key={strategy.value}
                className={`border rounded-lg p-3 cursor-pointer transition-all ${data.budget.bidStrategy === strategy.value
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
                  }`}
                onClick={() => updateData({
                  budget: { ...data.budget, bidStrategy: strategy.value as BudgetSchedule['bidStrategy'] }
                })}
              >
                <h4 className="font-medium text-gray-900">{strategy.label}</h4>
                <p className="text-sm text-gray-600">{strategy.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Schedule */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Campaign Schedule</label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Start Date</label>
              <input
                type="date"
                value={data.budget.startDate}
                onChange={(e) => updateData({
                  budget: { ...data.budget, startDate: e.target.value }
                })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
              />
              {validationErrors.startDate && (
                <p className="text-red-500 text-sm mt-1">{validationErrors.startDate}</p>
              )}
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">End Date (Optional)</label>
              <input
                type="date"
                value={data.budget.endDate || ''}
                onChange={(e) => updateData({
                  budget: { ...data.budget, endDate: e.target.value || undefined }
                })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderStep5 = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Set up conversion tracking</h3>

        {/* Conversion Goals */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Conversion Goals</label>
          <div className="space-y-3">
            {data.tracking.goals.map((goal, index) => (
              <div key={index} className="border rounded-lg p-4">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
                  <input
                    type="text"
                    value={goal.name}
                    onChange={(e) => updateConversionGoal(index, { name: e.target.value })}
                    placeholder="Goal name"
                    className="border border-gray-300 rounded-lg px-3 py-2"
                  />
                  <select
                    value={goal.type}
                    onChange={(e) => updateConversionGoal(index, { type: e.target.value as ConversionTracking['goals'][0]['type'] })}
                    className="border border-gray-300 rounded-lg px-3 py-2"
                  >
                    <option value="purchase">Purchase</option>
                    <option value="lead">Lead</option>
                    <option value="signup">Sign Up</option>
                    <option value="download">Download</option>
                    <option value="call">Phone Call</option>
                    <option value="custom">Custom</option>
                  </select>
                  <input
                    type="number"
                    value={goal.value}
                    onChange={(e) => updateConversionGoal(index, { value: parseFloat(e.target.value) || 0 })}
                    placeholder="Value"
                    className="border border-gray-300 rounded-lg px-3 py-2"
                  />
                  <div className="flex gap-2">
                    <select
                      value={goal.currency}
                      onChange={(e) => updateConversionGoal(index, { currency: e.target.value })}
                      className="border border-gray-300 rounded-lg px-3 py-2"
                    >
                      <option value="USD">USD</option>
                      <option value="EUR">EUR</option>
                      <option value="GBP">GBP</option>
                      <option value="INR">INR</option>
                    </select>
                    <button
                      onClick={() => removeConversionGoal(index)}
                      className="px-3 py-2 text-red-600 hover:text-red-700"
                    >
                      <X size={16} />
                    </button>
                  </div>
                </div>
              </div>
            ))}
            <button
              onClick={addConversionGoal}
              className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-gray-600 hover:text-gray-700"
            >
              <Plus size={16} />
              Add Conversion Goal
            </button>
          </div>
          {validationErrors.goals && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.goals}</p>
          )}
        </div>

        {/* Tracking Integration */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Tracking Integration</label>
          <div className="space-y-3">
            <input
              type="text"
              value={data.tracking.gtmContainer || ''}
              onChange={(e) => updateData({
                tracking: { ...data.tracking, gtmContainer: e.target.value }
              })}
              placeholder="Google Tag Manager Container ID (GTM-XXXXXXX)"
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            />
            <input
              type="text"
              value={data.tracking.googleAnalytics || ''}
              onChange={(e) => updateData({
                tracking: { ...data.tracking, googleAnalytics: e.target.value }
              })}
              placeholder="Google Analytics ID (G-XXXXXXXXXX)"
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            />
            <input
              type="text"
              value={data.tracking.facebookPixel || ''}
              onChange={(e) => updateData({
                tracking: { ...data.tracking, facebookPixel: e.target.value }
              })}
              placeholder="Facebook Pixel ID"
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            />
          </div>
        </div>
      </div>
    </div>
  );

  const renderStep6 = () => {
    // Calculate estimates based on data
    const estimatedReach = data.objective && data.budget.amount > 0
      ? Math.round(data.budget.amount * 100 * (data.objective.type === 'awareness' ? 2 : 1))
      : 0;

    const estimatedClicks = Math.round(estimatedReach * 0.02);
    const estimatedCost = data.budget.budgetType === 'daily' ? data.budget.amount * 30 : data.budget.amount;

    const qualityScore = Math.min(95, Math.max(60,
      70 +
      (data.creative.headlines.length * 2) +
      (data.creative.descriptions.length * 3) +
      (data.targeting.keywords.length * 1) +
      (data.tracking.goals.length * 5)
    ));

    const recommendations = [];
    if (data.creative.headlines.length < 5) recommendations.push('Add more headlines for better performance');
    if (data.targeting.keywords.length < 10) recommendations.push('Add more keywords to expand reach');
    if (data.tracking.goals.length === 0) recommendations.push('Set up conversion tracking for better optimization');
    if (data.budget.amount < 20) recommendations.push('Consider increasing budget for better results');

    return (
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold mb-4">Review and launch your campaign</h3>

          {/* Campaign Name */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">Campaign Name</label>
            <input
              type="text"
              value={data.review.campaignName}
              onChange={(e) => updateData({
                review: { ...data.review, campaignName: e.target.value }
              })}
              placeholder="Enter a descriptive campaign name"
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            />
            {validationErrors.campaignName && (
              <p className="text-red-500 text-sm mt-1">{validationErrors.campaignName}</p>
            )}
          </div>

          {/* Campaign Summary */}
          <div className="bg-gray-50 rounded-lg p-6 mb-6">
            <h4 className="font-medium text-gray-900 mb-4">Campaign Summary</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h5 className="text-sm font-medium text-gray-700 mb-2">Objective</h5>
                <p className="text-gray-900">{data.objective?.label || 'Not selected'}</p>
              </div>
              <div>
                <h5 className="text-sm font-medium text-gray-700 mb-2">Budget</h5>
                <p className="text-gray-900">
                  {data.budget.currency} {data.budget.amount}/{data.budget.budgetType}
                </p>
              </div>
              <div>
                <h5 className="text-sm font-medium text-gray-700 mb-2">Keywords</h5>
                <p className="text-gray-900">{data.targeting.keywords.length} keywords</p>
              </div>
              <div>
                <h5 className="text-sm font-medium text-gray-700 mb-2">Ad Creatives</h5>
                <p className="text-gray-900">
                  {data.creative.headlines.length} headlines, {data.creative.descriptions.length} descriptions
                </p>
              </div>
            </div>
          </div>

          {/* Performance Estimates */}
          <div className="bg-blue-50 rounded-lg p-6 mb-6">
            <h4 className="font-medium text-gray-900 mb-4">Performance Estimates</h4>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{estimatedReach.toLocaleString()}</div>
                <div className="text-sm text-gray-600">Estimated Reach</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{estimatedClicks.toLocaleString()}</div>
                <div className="text-sm text-gray-600">Estimated Clicks</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">{qualityScore}/100</div>
                <div className="text-sm text-gray-600">Quality Score</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">{data.budget.currency} {estimatedCost}</div>
                <div className="text-sm text-gray-600">Total Cost</div>
              </div>
            </div>
          </div>

          {/* Recommendations */}
          {recommendations.length > 0 && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
              <h4 className="font-medium text-yellow-800 mb-2 flex items-center">
                <AlertCircle size={16} className="mr-2" />
                Optimization Recommendations
              </h4>
              <ul className="list-disc list-inside space-y-1">
                {recommendations.map((rec, index) => (
                  <li key={index} className="text-yellow-700 text-sm">{rec}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Launch Options */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">Launch Option</label>
            <div className="space-y-2">
              <label className="flex items-center">
                <input
                  type="radio"
                  checked={data.review.launchType === 'immediate'}
                  onChange={() => updateData({
                    review: { ...data.review, launchType: 'immediate' }
                  })}
                  className="mr-2"
                />
                Launch immediately
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  checked={data.review.launchType === 'scheduled'}
                  onChange={() => updateData({
                    review: { ...data.review, launchType: 'scheduled' }
                  })}
                  className="mr-2"
                />
                Schedule for later
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  checked={data.review.launchType === 'draft'}
                  onChange={() => updateData({
                    review: { ...data.review, launchType: 'draft' }
                  })}
                  className="mr-2"
                />
                Save as draft
              </label>
            </div>

            {data.review.launchType === 'scheduled' && (
              <div className="mt-3">
                <input
                  type="datetime-local"
                  value={data.review.scheduledDate || ''}
                  onChange={(e) => updateData({
                    review: { ...data.review, scheduledDate: e.target.value }
                  })}
                  className="border border-gray-300 rounded-lg px-3 py-2"
                />
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Progress Steps */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {steps.map((step, index) => (
            <div key={step.number} className="flex items-center w-full">
              <div className={`flex items-center justify-center w-8 h-8 rounded-full shrink-0 ${currentStep >= step.number
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-600'
                }`}>
                {currentStep > step.number ? (
                  <Check size={16} />
                ) : (
                  <step.icon size={16} />
                )}
              </div>
              {index < steps.length - 1 && (
                <div className={`w-full h-0.5 mx-2 ${currentStep > step.number ? 'bg-blue-600' : 'bg-gray-200'
                  }`} />
              )}
            </div>
          ))}
        </div>
        <div className="flex justify-between mt-2">
          {steps.map((step) => (
            <div key={step.number} className="text-xs text-gray-600 text-center">
              {step.title}
            </div>
          ))}
        </div>
      </div>

      {/* Step Content */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
        {currentStep === 1 && renderStep1()}
        {currentStep === 2 && renderStep2()}
        {currentStep === 3 && renderStep3()}
        {currentStep === 4 && renderStep4()}
        {currentStep === 5 && renderStep5()}
        {currentStep === 6 && renderStep6()}
      </div>

      {/* Navigation */}
      <div className="flex justify-between">
        <button
          onClick={prevStep}
          disabled={currentStep === 1}
          className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>

        {currentStep < steps.length ? (
          <button
            onClick={nextStep}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Next
          </button>
        ) : (
          <button
            onClick={() => {
              if (validateStep(currentStep)) {
                // Handle campaign launch
                console.log('Launching Google Ads campaign:', data);
              }
            }}
            className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2"
          >
            <Rocket size={16} />
            {data.review.launchType === 'immediate' ? 'Launch Campaign' :
              data.review.launchType === 'scheduled' ? 'Schedule Campaign' : 'Save Draft'}
          </button>
        )}
      </div>
    </div>
  );
}