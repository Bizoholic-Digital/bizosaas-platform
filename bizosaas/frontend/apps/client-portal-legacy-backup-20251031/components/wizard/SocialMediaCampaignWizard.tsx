'use client';

import React, { useState } from 'react';
import {
  Target, Users, Edit3, BarChart3, Rocket, Plus, Minus, X, Check,
  AlertCircle, CheckCircle, Calendar, Clock, MapPin, Globe,
  Smartphone, Monitor, Facebook, Instagram, Twitter, Linkedin,
  Youtube, Hash, Heart, MessageCircle, Share, Eye
} from 'lucide-react';

interface SocialPlatform {
  id: string;
  name: string;
  icon: React.ComponentType<any>;
  color: string;
  maxPostLength: number;
  imageSpecs: { width: number; height: number }[];
  videoSpecs?: { maxDuration: number; formats: string[] };
}

interface CampaignObjective {
  type: 'awareness' | 'engagement' | 'traffic' | 'leads' | 'conversions' | 'followers';
  label: string;
  description: string;
  platforms: string[];
  recommendedBudget: { min: number; max: number };
}

interface AudienceTargeting {
  demographics: {
    ageRange: { min: number; max: number };
    genders: string[];
    languages: string[];
  };
  interests: string[];
  behaviors: string[];
  customAudiences: string[];
  lookalikeSources: string[];
  geographic: {
    countries: string[];
    regions: string[];
    cities: string[];
  };
}

interface ContentCreative {
  platforms: string[];
  postTypes: ('image' | 'video' | 'carousel' | 'story' | 'reel')[];
  content: {
    primaryText: string;
    headlines: string[];
    callToActions: string[];
    hashtags: string[];
    mentions: string[];
  };
  media: {
    images: string[];
    videos: string[];
    captions: string[];
  };
  scheduling: {
    frequency: 'daily' | 'weekly' | 'custom';
    bestTimes: string[];
    timezone: string;
  };
}

interface BudgetOptimization {
  totalBudget: number;
  currency: string;
  budgetType: 'daily' | 'lifetime';
  bidStrategy: 'lowest_cost' | 'cost_cap' | 'bid_cap' | 'target_cost';
  optimization: 'reach' | 'impressions' | 'clicks' | 'conversions' | 'engagement';
  platformAllocation: { [platformId: string]: number };
  duration: {
    startDate: string;
    endDate?: string;
    totalDays: number;
  };
}

interface TrackingAnalytics {
  objectives: {
    name: string;
    type: 'clicks' | 'impressions' | 'engagements' | 'conversions' | 'reach' | 'followers';
    target: number;
    priority: 'high' | 'medium' | 'low';
  }[];
  tracking: {
    pixelIds: { [platform: string]: string };
    utmParameters: {
      source: string;
      medium: string;
      campaign: string;
      content?: string;
      term?: string;
    };
    conversionEvents: string[];
  };
  reporting: {
    frequency: 'daily' | 'weekly' | 'monthly';
    metrics: string[];
    dashboardUrl?: string;
  };
}

interface SocialMediaCampaignData {
  objective: CampaignObjective | null;
  audience: AudienceTargeting;
  creative: ContentCreative;
  budget: BudgetOptimization;
  analytics: TrackingAnalytics;
}

interface SocialMediaCampaignWizardProps {
  data: SocialMediaCampaignData;
  onUpdate: (data: SocialMediaCampaignData) => void;
  onValidate: () => boolean;
}

const SOCIAL_PLATFORMS: SocialPlatform[] = [
  {
    id: 'facebook',
    name: 'Facebook',
    icon: Facebook,
    color: '#1877F2',
    maxPostLength: 63206,
    imageSpecs: [{ width: 1200, height: 630 }, { width: 1080, height: 1080 }],
    videoSpecs: { maxDuration: 240, formats: ['MP4', 'MOV', 'AVI'] }
  },
  {
    id: 'instagram',
    name: 'Instagram',
    icon: Instagram,
    color: '#E4405F',
    maxPostLength: 2200,
    imageSpecs: [{ width: 1080, height: 1080 }, { width: 1080, height: 1350 }],
    videoSpecs: { maxDuration: 60, formats: ['MP4', 'MOV'] }
  },
  {
    id: 'twitter',
    name: 'Twitter',
    icon: Twitter,
    color: '#1DA1F2',
    maxPostLength: 280,
    imageSpecs: [{ width: 1200, height: 675 }, { width: 1080, height: 1080 }],
    videoSpecs: { maxDuration: 140, formats: ['MP4', 'MOV'] }
  },
  {
    id: 'linkedin',
    name: 'LinkedIn',
    icon: Linkedin,
    color: '#0A66C2',
    maxPostLength: 3000,
    imageSpecs: [{ width: 1200, height: 627 }, { width: 1080, height: 1080 }],
    videoSpecs: { maxDuration: 600, formats: ['MP4', 'MOV', 'WMV'] }
  },
  {
    id: 'youtube',
    name: 'YouTube',
    icon: Youtube,
    color: '#FF0000',
    maxPostLength: 5000,
    imageSpecs: [{ width: 1280, height: 720 }],
    videoSpecs: { maxDuration: 43200, formats: ['MP4', 'MOV', 'AVI', 'WMV'] }
  }
];

const CAMPAIGN_OBJECTIVES: CampaignObjective[] = [
  {
    type: 'awareness',
    label: 'Brand Awareness',
    description: 'Increase visibility and brand recognition',
    platforms: ['facebook', 'instagram', 'twitter', 'linkedin', 'youtube'],
    recommendedBudget: { min: 20, max: 100 }
  },
  {
    type: 'engagement',
    label: 'Engagement',
    description: 'Increase likes, comments, shares, and interactions',
    platforms: ['facebook', 'instagram', 'twitter', 'linkedin'],
    recommendedBudget: { min: 15, max: 75 }
  },
  {
    type: 'traffic',
    label: 'Website Traffic',
    description: 'Drive visitors to your website or landing page',
    platforms: ['facebook', 'instagram', 'twitter', 'linkedin', 'youtube'],
    recommendedBudget: { min: 25, max: 125 }
  },
  {
    type: 'leads',
    label: 'Lead Generation',
    description: 'Collect leads and contact information',
    platforms: ['facebook', 'instagram', 'linkedin'],
    recommendedBudget: { min: 30, max: 150 }
  },
  {
    type: 'conversions',
    label: 'Conversions',
    description: 'Drive purchases and sales',
    platforms: ['facebook', 'instagram', 'twitter', 'linkedin'],
    recommendedBudget: { min: 40, max: 200 }
  },
  {
    type: 'followers',
    label: 'Followers',
    description: 'Grow your social media following',
    platforms: ['facebook', 'instagram', 'twitter', 'linkedin', 'youtube'],
    recommendedBudget: { min: 10, max: 50 }
  }
];

const BID_STRATEGIES = [
  { value: 'lowest_cost', label: 'Lowest Cost', description: 'Get the most results for your budget' },
  { value: 'cost_cap', label: 'Cost Cap', description: 'Control average cost per result' },
  { value: 'bid_cap', label: 'Bid Cap', description: 'Control maximum bid amount' },
  { value: 'target_cost', label: 'Target Cost', description: 'Maintain stable cost per result' }
];

const POST_TYPES = [
  { value: 'image', label: 'Image Posts', description: 'Single image with text' },
  { value: 'video', label: 'Video Posts', description: 'Video content with captions' },
  { value: 'carousel', label: 'Carousel', description: 'Multiple images/videos' },
  { value: 'story', label: 'Stories', description: 'Temporary 24-hour content' },
  { value: 'reel', label: 'Reels/Shorts', description: 'Short-form vertical videos' }
];

export function SocialMediaCampaignWizard({ data, onUpdate, onValidate }: SocialMediaCampaignWizardProps) {
  const [currentStep, setCurrentStep] = useState(1);
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  const steps = [
    { number: 1, title: 'Campaign Objective', icon: Target },
    { number: 2, title: 'Audience Targeting', icon: Users },
    { number: 3, title: 'Content & Creative', icon: Edit3 },
    { number: 4, title: 'Budget & Optimization', icon: BarChart3 },
    { number: 5, title: 'Tracking & Launch', icon: Rocket }
  ];

  const updateData = (updates: Partial<SocialMediaCampaignData>) => {
    onUpdate({ ...data, ...updates });
  };

  const validateStep = (step: number): boolean => {
    const errors: Record<string, string> = {};

    switch (step) {
      case 1:
        if (!data.objective) errors.objective = 'Please select a campaign objective';
        if (data.creative.platforms.length === 0) errors.platforms = 'Select at least one platform';
        break;
      case 2:
        if (data.audience.interests.length === 0) errors.interests = 'Add at least one interest';
        if (data.audience.geographic.countries.length === 0) errors.location = 'Select at least one location';
        break;
      case 3:
        if (!data.creative.content.primaryText) errors.primaryText = 'Primary text is required';
        if (data.creative.postTypes.length === 0) errors.postTypes = 'Select at least one post type';
        break;
      case 4:
        if (data.budget.totalBudget <= 0) errors.budget = 'Budget must be greater than 0';
        if (!data.budget.duration.startDate) errors.startDate = 'Start date is required';
        break;
      case 5:
        if (data.analytics.objectives.length === 0) errors.objectives = 'Add at least one tracking objective';
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

  const togglePlatform = (platformId: string) => {
    const platforms = data.creative.platforms.includes(platformId)
      ? data.creative.platforms.filter(p => p !== platformId)
      : [...data.creative.platforms, platformId];
    
    updateData({
      creative: { ...data.creative, platforms }
    });
  };

  const addInterest = (interest: string) => {
    if (interest && !data.audience.interests.includes(interest)) {
      updateData({
        audience: {
          ...data.audience,
          interests: [...data.audience.interests, interest]
        }
      });
    }
  };

  const removeInterest = (interest: string) => {
    updateData({
      audience: {
        ...data.audience,
        interests: data.audience.interests.filter(i => i !== interest)
      }
    });
  };

  const addHashtag = (hashtag: string) => {
    if (hashtag && !data.creative.content.hashtags.includes(hashtag)) {
      const formattedHashtag = hashtag.startsWith('#') ? hashtag : `#${hashtag}`;
      updateData({
        creative: {
          ...data.creative,
          content: {
            ...data.creative.content,
            hashtags: [...data.creative.content.hashtags, formattedHashtag]
          }
        }
      });
    }
  };

  const removeHashtag = (hashtag: string) => {
    updateData({
      creative: {
        ...data.creative,
        content: {
          ...data.creative.content,
          hashtags: data.creative.content.hashtags.filter(h => h !== hashtag)
        }
      }
    });
  };

  const addTrackingObjective = () => {
    updateData({
      analytics: {
        ...data.analytics,
        objectives: [...data.analytics.objectives, {
          name: '',
          type: 'clicks',
          target: 1000,
          priority: 'medium'
        }]
      }
    });
  };

  const updateTrackingObjective = (index: number, updates: Partial<TrackingAnalytics['objectives'][0]>) => {
    const newObjectives = [...data.analytics.objectives];
    newObjectives[index] = { ...newObjectives[index], ...updates };
    updateData({
      analytics: {
        ...data.analytics,
        objectives: newObjectives
      }
    });
  };

  const removeTrackingObjective = (index: number) => {
    updateData({
      analytics: {
        ...data.analytics,
        objectives: data.analytics.objectives.filter((_, i) => i !== index)
      }
    });
  };

  const renderStep1 = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">What's your social media campaign objective?</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          {CAMPAIGN_OBJECTIVES.map((objective) => (
            <div
              key={objective.type}
              className={`border rounded-lg p-4 cursor-pointer transition-all ${
                data.objective?.type === objective.type
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => updateData({ objective })}
            >
              <h4 className="font-medium text-gray-900">{objective.label}</h4>
              <p className="text-sm text-gray-600 mt-1">{objective.description}</p>
              <p className="text-xs text-gray-500 mt-2">
                Recommended: ${objective.recommendedBudget.min}-${objective.recommendedBudget.max}/day
              </p>
            </div>
          ))}
        </div>
        {validationErrors.objective && (
          <p className="text-red-500 text-sm mt-2">{validationErrors.objective}</p>
        )}

        <div className="mt-6">
          <h4 className="font-medium text-gray-900 mb-3">Select platforms for this campaign</h4>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
            {SOCIAL_PLATFORMS.map((platform) => {
              const Icon = platform.icon;
              const isSelected = data.creative.platforms.includes(platform.id);
              const isAvailable = !data.objective || data.objective.platforms.includes(platform.id);
              
              return (
                <div
                  key={platform.id}
                  className={`border rounded-lg p-3 cursor-pointer transition-all text-center ${
                    !isAvailable ? 'opacity-50 cursor-not-allowed' :
                    isSelected ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => isAvailable && togglePlatform(platform.id)}
                >
                  <Icon size={24} style={{ color: platform.color, margin: '0 auto' }} />
                  <p className="text-sm font-medium mt-2">{platform.name}</p>
                  {isSelected && <Check size={16} className="text-blue-500 mx-auto mt-1" />}
                </div>
              );
            })}
          </div>
          {validationErrors.platforms && (
            <p className="text-red-500 text-sm mt-2">{validationErrors.platforms}</p>
          )}
        </div>
      </div>
    </div>
  );

  const renderStep2 = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Define your target audience</h3>
        
        {/* Demographics */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Demographics</label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Age Range</label>
              <div className="flex gap-2">
                <select
                  value={data.audience.demographics.ageRange.min}
                  onChange={(e) => updateData({
                    audience: {
                      ...data.audience,
                      demographics: {
                        ...data.audience.demographics,
                        ageRange: {
                          ...data.audience.demographics.ageRange,
                          min: parseInt(e.target.value)
                        }
                      }
                    }
                  })}
                  className="border border-gray-300 rounded-lg px-3 py-2"
                >
                  {[13, 18, 25, 35, 45, 55, 65].map(age => (
                    <option key={age} value={age}>{age}+</option>
                  ))}
                </select>
                <span className="py-2">to</span>
                <select
                  value={data.audience.demographics.ageRange.max}
                  onChange={(e) => updateData({
                    audience: {
                      ...data.audience,
                      demographics: {
                        ...data.audience.demographics,
                        ageRange: {
                          ...data.audience.demographics.ageRange,
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
            <div>
              <label className="block text-sm text-gray-600 mb-1">Gender</label>
              <div className="flex gap-4">
                {['all', 'male', 'female', 'non-binary'].map(gender => (
                  <label key={gender} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={data.audience.demographics.genders.includes(gender)}
                      onChange={(e) => {
                        const genders = e.target.checked
                          ? [...data.audience.demographics.genders, gender]
                          : data.audience.demographics.genders.filter(g => g !== gender);
                        updateData({
                          audience: {
                            ...data.audience,
                            demographics: {
                              ...data.audience.demographics,
                              genders
                            }
                          }
                        });
                      }}
                      className="mr-1"
                    />
                    {gender.charAt(0).toUpperCase() + gender.slice(1)}
                  </label>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Interests */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Interests & Behaviors
          </label>
          <div className="flex flex-wrap gap-2 mb-2">
            {data.audience.interests.map((interest, index) => (
              <span
                key={index}
                className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-purple-100 text-purple-800"
              >
                {interest}
                <button
                  onClick={() => removeInterest(interest)}
                  className="ml-2 hover:text-purple-600"
                >
                  <X size={14} />
                </button>
              </span>
            ))}
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Add interest (e.g., 'fitness', 'technology')"
              className="flex-1 border border-gray-300 rounded-lg px-3 py-2"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  addInterest((e.target as HTMLInputElement).value);
                  (e.target as HTMLInputElement).value = '';
                }
              }}
            />
            <button
              onClick={() => {
                const input = document.querySelector('input[placeholder*="Add interest"]') as HTMLInputElement;
                if (input.value) {
                  addInterest(input.value);
                  input.value = '';
                }
              }}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
            >
              <Plus size={16} />
            </button>
          </div>
          {validationErrors.interests && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.interests}</p>
          )}
        </div>

        {/* Location */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Geographic Targeting</label>
          <div className="space-y-2">
            <input
              type="text"
              placeholder="Add countries, regions, or cities"
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  const location = (e.target as HTMLInputElement).value;
                  if (location) {
                    updateData({
                      audience: {
                        ...data.audience,
                        geographic: {
                          ...data.audience.geographic,
                          countries: [...data.audience.geographic.countries, location]
                        }
                      }
                    });
                    (e.target as HTMLInputElement).value = '';
                  }
                }
              }}
            />
            <div className="flex flex-wrap gap-2">
              {data.audience.geographic.countries.map((location, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-green-100 text-green-800"
                >
                  <MapPin size={12} className="mr-1" />
                  {location}
                  <button
                    onClick={() => updateData({
                      audience: {
                        ...data.audience,
                        geographic: {
                          ...data.audience.geographic,
                          countries: data.audience.geographic.countries.filter((_, i) => i !== index)
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
        <h3 className="text-lg font-semibold mb-4">Create your content and creative</h3>
        
        {/* Post Types */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Content Types</label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {POST_TYPES.map((type) => (
              <div
                key={type.value}
                className={`border rounded-lg p-3 cursor-pointer transition-all ${
                  data.creative.postTypes.includes(type.value as any)
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => {
                  const postTypes = data.creative.postTypes.includes(type.value as any)
                    ? data.creative.postTypes.filter(t => t !== type.value)
                    : [...data.creative.postTypes, type.value as any];
                  updateData({
                    creative: { ...data.creative, postTypes }
                  });
                }}
              >
                <h4 className="font-medium text-gray-900">{type.label}</h4>
                <p className="text-sm text-gray-600">{type.description}</p>
              </div>
            ))}
          </div>
          {validationErrors.postTypes && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.postTypes}</p>
          )}
        </div>

        {/* Primary Content */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Primary Text</label>
          <textarea
            value={data.creative.content.primaryText}
            onChange={(e) => updateData({
              creative: {
                ...data.creative,
                content: {
                  ...data.creative.content,
                  primaryText: e.target.value
                }
              }
            })}
            rows={4}
            maxLength={2200}
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
            placeholder="Write your main post content here..."
          />
          <div className="text-sm text-gray-500 mt-1">
            {data.creative.content.primaryText.length}/2200 characters
          </div>
          {validationErrors.primaryText && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.primaryText}</p>
          )}
        </div>

        {/* Headlines */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Headlines (Optional)</label>
          <div className="space-y-2">
            {data.creative.content.headlines.map((headline, index) => (
              <div key={index} className="flex gap-2">
                <input
                  type="text"
                  value={headline}
                  onChange={(e) => {
                    const newHeadlines = [...data.creative.content.headlines];
                    newHeadlines[index] = e.target.value;
                    updateData({
                      creative: {
                        ...data.creative,
                        content: {
                          ...data.creative.content,
                          headlines: newHeadlines
                        }
                      }
                    });
                  }}
                  maxLength={125}
                  className="flex-1 border border-gray-300 rounded-lg px-3 py-2"
                  placeholder={`Headline ${index + 1}`}
                />
                <button
                  onClick={() => {
                    const newHeadlines = data.creative.content.headlines.filter((_, i) => i !== index);
                    updateData({
                      creative: {
                        ...data.creative,
                        content: {
                          ...data.creative.content,
                          headlines: newHeadlines
                        }
                      }
                    });
                  }}
                  className="px-3 py-2 text-red-600 hover:text-red-700"
                >
                  <X size={16} />
                </button>
              </div>
            ))}
            {data.creative.content.headlines.length < 5 && (
              <button
                onClick={() => updateData({
                  creative: {
                    ...data.creative,
                    content: {
                      ...data.creative.content,
                      headlines: [...data.creative.content.headlines, '']
                    }
                  }
                })}
                className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-gray-600 hover:text-gray-700"
              >
                <Plus size={16} />
                Add Headline
              </button>
            )}
          </div>
        </div>

        {/* Hashtags */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Hashtags
          </label>
          <div className="flex flex-wrap gap-2 mb-2">
            {data.creative.content.hashtags.map((hashtag, index) => (
              <span
                key={index}
                className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800"
              >
                <Hash size={12} className="mr-1" />
                {hashtag}
                <button
                  onClick={() => removeHashtag(hashtag)}
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
              placeholder="Add hashtag (e.g., 'marketing', 'business')"
              className="flex-1 border border-gray-300 rounded-lg px-3 py-2"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  addHashtag((e.target as HTMLInputElement).value);
                  (e.target as HTMLInputElement).value = '';
                }
              }}
            />
            <button
              onClick={() => {
                const input = document.querySelector('input[placeholder*="Add hashtag"]') as HTMLInputElement;
                if (input.value) {
                  addHashtag(input.value);
                  input.value = '';
                }
              }}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              <Plus size={16} />
            </button>
          </div>
        </div>

        {/* Call to Actions */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Call to Action</label>
          <select
            value={data.creative.content.callToActions[0] || ''}
            onChange={(e) => updateData({
              creative: {
                ...data.creative,
                content: {
                  ...data.creative.content,
                  callToActions: e.target.value ? [e.target.value] : []
                }
              }
            })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
          >
            <option value="">Select a call to action</option>
            <option value="Learn More">Learn More</option>
            <option value="Shop Now">Shop Now</option>
            <option value="Sign Up">Sign Up</option>
            <option value="Download">Download</option>
            <option value="Contact Us">Contact Us</option>
            <option value="Get Quote">Get Quote</option>
            <option value="Book Now">Book Now</option>
            <option value="Subscribe">Subscribe</option>
          </select>
        </div>
      </div>
    </div>
  );

  const renderStep4 = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Set your budget and optimization</h3>
        
        {/* Budget Configuration */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Campaign Budget</label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Budget Type</label>
              <select
                value={data.budget.budgetType}
                onChange={(e) => updateData({
                  budget: { ...data.budget, budgetType: e.target.value as BudgetOptimization['budgetType'] }
                })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
              >
                <option value="daily">Daily Budget</option>
                <option value="lifetime">Lifetime Budget</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Currency</label>
              <select
                value={data.budget.currency}
                onChange={(e) => updateData({
                  budget: { ...data.budget, currency: e.target.value }
                })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
              >
                <option value="USD">USD</option>
                <option value="EUR">EUR</option>
                <option value="GBP">GBP</option>
                <option value="INR">INR</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Amount</label>
              <input
                type="number"
                value={data.budget.totalBudget}
                onChange={(e) => updateData({
                  budget: { ...data.budget, totalBudget: parseFloat(e.target.value) || 0 }
                })}
                min="1"
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
                placeholder="Enter amount"
              />
            </div>
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
                className={`border rounded-lg p-3 cursor-pointer transition-all ${
                  data.budget.bidStrategy === strategy.value
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => updateData({
                  budget: { ...data.budget, bidStrategy: strategy.value as BudgetOptimization['bidStrategy'] }
                })}
              >
                <h4 className="font-medium text-gray-900">{strategy.label}</h4>
                <p className="text-sm text-gray-600">{strategy.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Optimization Goal */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Optimization Goal</label>
          <select
            value={data.budget.optimization}
            onChange={(e) => updateData({
              budget: { ...data.budget, optimization: e.target.value as BudgetOptimization['optimization'] }
            })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
          >
            <option value="reach">Reach - Show ads to the maximum number of people</option>
            <option value="impressions">Impressions - Maximize total ad views</option>
            <option value="clicks">Clicks - Drive the most clicks to your website</option>
            <option value="conversions">Conversions - Optimize for purchases or actions</option>
            <option value="engagement">Engagement - Maximize likes, comments, and shares</option>
          </select>
        </div>

        {/* Campaign Duration */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Campaign Duration</label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Start Date</label>
              <input
                type="date"
                value={data.budget.duration.startDate}
                onChange={(e) => updateData({
                  budget: {
                    ...data.budget,
                    duration: {
                      ...data.budget.duration,
                      startDate: e.target.value
                    }
                  }
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
                value={data.budget.duration.endDate || ''}
                onChange={(e) => updateData({
                  budget: {
                    ...data.budget,
                    duration: {
                      ...data.budget.duration,
                      endDate: e.target.value || undefined
                    }
                  }
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
        <h3 className="text-lg font-semibold mb-4">Set up tracking and launch</h3>
        
        {/* Tracking Objectives */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Campaign Objectives & Tracking</label>
          <div className="space-y-3">
            {data.analytics.objectives.map((objective, index) => (
              <div key={index} className="border rounded-lg p-4">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
                  <input
                    type="text"
                    value={objective.name}
                    onChange={(e) => updateTrackingObjective(index, { name: e.target.value })}
                    placeholder="Objective name"
                    className="border border-gray-300 rounded-lg px-3 py-2"
                  />
                  <select
                    value={objective.type}
                    onChange={(e) => updateTrackingObjective(index, { type: e.target.value as TrackingAnalytics['objectives'][0]['type'] })}
                    className="border border-gray-300 rounded-lg px-3 py-2"
                  >
                    <option value="clicks">Clicks</option>
                    <option value="impressions">Impressions</option>
                    <option value="engagements">Engagements</option>
                    <option value="conversions">Conversions</option>
                    <option value="reach">Reach</option>
                    <option value="followers">Followers</option>
                  </select>
                  <input
                    type="number"
                    value={objective.target}
                    onChange={(e) => updateTrackingObjective(index, { target: parseInt(e.target.value) || 0 })}
                    placeholder="Target"
                    className="border border-gray-300 rounded-lg px-3 py-2"
                  />
                  <div className="flex gap-2">
                    <select
                      value={objective.priority}
                      onChange={(e) => updateTrackingObjective(index, { priority: e.target.value as TrackingAnalytics['objectives'][0]['priority'] })}
                      className="border border-gray-300 rounded-lg px-3 py-2"
                    >
                      <option value="high">High</option>
                      <option value="medium">Medium</option>
                      <option value="low">Low</option>
                    </select>
                    <button
                      onClick={() => removeTrackingObjective(index)}
                      className="px-3 py-2 text-red-600 hover:text-red-700"
                    >
                      <X size={16} />
                    </button>
                  </div>
                </div>
              </div>
            ))}
            <button
              onClick={addTrackingObjective}
              className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-gray-600 hover:text-gray-700"
            >
              <Plus size={16} />
              Add Tracking Objective
            </button>
          </div>
          {validationErrors.objectives && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.objectives}</p>
          )}
        </div>

        {/* UTM Parameters */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">UTM Parameters</label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              type="text"
              value={data.analytics.tracking.utmParameters.source}
              onChange={(e) => updateData({
                analytics: {
                  ...data.analytics,
                  tracking: {
                    ...data.analytics.tracking,
                    utmParameters: {
                      ...data.analytics.tracking.utmParameters,
                      source: e.target.value
                    }
                  }
                }
              })}
              placeholder="UTM Source (e.g., facebook)"
              className="border border-gray-300 rounded-lg px-3 py-2"
            />
            <input
              type="text"
              value={data.analytics.tracking.utmParameters.medium}
              onChange={(e) => updateData({
                analytics: {
                  ...data.analytics,
                  tracking: {
                    ...data.analytics.tracking,
                    utmParameters: {
                      ...data.analytics.tracking.utmParameters,
                      medium: e.target.value
                    }
                  }
                }
              })}
              placeholder="UTM Medium (e.g., social)"
              className="border border-gray-300 rounded-lg px-3 py-2"
            />
            <input
              type="text"
              value={data.analytics.tracking.utmParameters.campaign}
              onChange={(e) => updateData({
                analytics: {
                  ...data.analytics,
                  tracking: {
                    ...data.analytics.tracking,
                    utmParameters: {
                      ...data.analytics.tracking.utmParameters,
                      campaign: e.target.value
                    }
                  }
                }
              })}
              placeholder="UTM Campaign (e.g., summer-sale)"
              className="border border-gray-300 rounded-lg px-3 py-2"
            />
            <input
              type="text"
              value={data.analytics.tracking.utmParameters.content || ''}
              onChange={(e) => updateData({
                analytics: {
                  ...data.analytics,
                  tracking: {
                    ...data.analytics.tracking,
                    utmParameters: {
                      ...data.analytics.tracking.utmParameters,
                      content: e.target.value
                    }
                  }
                }
              })}
              placeholder="UTM Content (optional)"
              className="border border-gray-300 rounded-lg px-3 py-2"
            />
          </div>
        </div>

        {/* Pixel Integration */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Tracking Pixels</label>
          <div className="space-y-3">
            {data.creative.platforms.map(platformId => {
              const platform = SOCIAL_PLATFORMS.find(p => p.id === platformId);
              return platform ? (
                <div key={platformId} className="flex items-center gap-3">
                  <div className="w-6 h-6">
                    <platform.icon size={20} style={{ color: platform.color }} />
                  </div>
                  <label className="text-sm font-medium text-gray-700 w-20">
                    {platform.name}:
                  </label>
                  <input
                    type="text"
                    value={data.analytics.tracking.pixelIds[platformId] || ''}
                    onChange={(e) => updateData({
                      analytics: {
                        ...data.analytics,
                        tracking: {
                          ...data.analytics.tracking,
                          pixelIds: {
                            ...data.analytics.tracking.pixelIds,
                            [platformId]: e.target.value
                          }
                        }
                      }
                    })}
                    placeholder={`${platform.name} Pixel ID`}
                    className="flex-1 border border-gray-300 rounded-lg px-3 py-2"
                  />
                </div>
              ) : null;
            })}
          </div>
        </div>

        {/* Campaign Summary */}
        <div className="bg-gray-50 rounded-lg p-6">
          <h4 className="font-medium text-gray-900 mb-4">Campaign Summary</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h5 className="text-sm font-medium text-gray-700 mb-2">Objective</h5>
              <p className="text-gray-900">{data.objective?.label || 'Not selected'}</p>
            </div>
            <div>
              <h5 className="text-sm font-medium text-gray-700 mb-2">Platforms</h5>
              <p className="text-gray-900">{data.creative.platforms.length} platforms selected</p>
            </div>
            <div>
              <h5 className="text-sm font-medium text-gray-700 mb-2">Budget</h5>
              <p className="text-gray-900">
                {data.budget.currency} {data.budget.totalBudget}/{data.budget.budgetType}
              </p>
            </div>
            <div>
              <h5 className="text-sm font-medium text-gray-700 mb-2">Duration</h5>
              <p className="text-gray-900">
                {data.budget.duration.startDate} - {data.budget.duration.endDate || 'Ongoing'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Progress Steps */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {steps.map((step, index) => (
            <div key={step.number} className="flex items-center">
              <div className={`flex items-center justify-center w-8 h-8 rounded-full ${
                currentStep >= step.number
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-200 text-gray-600'
              }`}>
                {currentStep > step.number ? (
                  <Check size={16} />
                ) : (
                  <step.icon size={16} />
                )}
              </div>
              {index < steps.length - 1 && (
                <div className={`w-full h-0.5 mx-2 ${
                  currentStep > step.number ? 'bg-purple-600' : 'bg-gray-200'
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
            className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Next
          </button>
        ) : (
          <button
            onClick={() => {
              if (validateStep(currentStep)) {
                // Handle campaign launch
                console.log('Launching Social Media campaign:', data);
              }
            }}
            className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2"
          >
            <Rocket size={16} />
            Launch Campaign
          </button>
        )}
      </div>
    </div>
  );
}