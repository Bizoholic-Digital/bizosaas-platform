'use client';

import React, { useState } from 'react';
import {
  Target, Users, Edit3, BarChart3, Rocket, Plus, Minus, X, Check,
  AlertCircle, CheckCircle, Calendar, Clock, Mail, Send, UserPlus,
  Zap, Filter, Eye, MousePointer, TrendingUp, Settings
} from 'lucide-react';

interface CampaignType {
  type: 'newsletter' | 'promotional' | 'welcome' | 'abandoned_cart' | 'drip' | 'announcement';
  label: string;
  description: string;
  recommended: boolean;
  frequency: string;
}

interface AudienceSegmentation {
  segments: {
    id: string;
    name: string;
    criteria: {
      demographics: { [key: string]: any };
      behaviors: string[];
      engagement: string[];
      purchaseHistory: string[];
    };
    size: number;
    selected: boolean;
  }[];
  customLists: string[];
  exclusions: string[];
  suppressions: string[];
}

interface EmailContent {
  template: {
    type: 'custom' | 'newsletter' | 'promotional' | 'welcome' | 'transactional';
    style: 'minimal' | 'corporate' | 'creative' | 'ecommerce';
    colors: {
      primary: string;
      secondary: string;
      accent: string;
      background: string;
    };
  };
  content: {
    subjectLine: string;
    preheader: string;
    headline: string;
    bodyText: string;
    callToAction: {
      text: string;
      url: string;
      style: 'button' | 'link' | 'banner';
    }[];
    footer: string;
  };
  personalization: {
    useFirstName: boolean;
    useCompanyName: boolean;
    usePurchaseHistory: boolean;
    customFields: string[];
    dynamicContent: boolean;
  };
  media: {
    logo: string;
    headerImage?: string;
    productImages: string[];
    socialIcons: boolean;
  };
}

interface DeliveryOptimization {
  scheduling: {
    type: 'immediate' | 'scheduled' | 'optimized' | 'drip';
    scheduleDate?: string;
    scheduleTime?: string;
    timezone: string;
    frequency?: 'daily' | 'weekly' | 'monthly' | 'custom';
    dripSequence?: {
      delay: number;
      unit: 'minutes' | 'hours' | 'days' | 'weeks';
    }[];
  };
  optimization: {
    sendTimeOptimization: boolean;
    subjectLineTests: string[];
    contentTests: string[];
    frequencyOptimization: boolean;
    deliverabilityOptimization: boolean;
  };
  limits: {
    maxPerHour: number;
    maxPerDay: number;
    respectUnsubscribes: boolean;
    honorOptouts: boolean;
  };
}

interface PerformanceTracking {
  tracking: {
    opens: boolean;
    clicks: boolean;
    conversions: boolean;
    revenue: boolean;
    unsubscribes: boolean;
    forwards: boolean;
    socialShares: boolean;
  };
  goals: {
    name: string;
    metric: 'open_rate' | 'click_rate' | 'conversion_rate' | 'revenue' | 'unsubscribe_rate';
    target: number;
    priority: 'high' | 'medium' | 'low';
  }[];
  integration: {
    googleAnalytics?: string;
    facebookPixel?: string;
    customEvents: string[];
    webhooks: string[];
  };
  automation: {
    autoResponders: boolean;
    listManagement: boolean;
    segmentUpdates: boolean;
    reportingSchedule: 'daily' | 'weekly' | 'monthly';
  };
}

interface EmailMarketingData {
  campaignType: CampaignType | null;
  audience: AudienceSegmentation;
  content: EmailContent;
  delivery: DeliveryOptimization;
  tracking: PerformanceTracking;
}

interface EmailMarketingWizardProps {
  data: EmailMarketingData;
  onUpdate: (data: EmailMarketingData) => void;
  onValidate: () => boolean;
}

const CAMPAIGN_TYPES: CampaignType[] = [
  {
    type: 'newsletter',
    label: 'Newsletter',
    description: 'Regular updates with valuable content and news',
    recommended: true,
    frequency: 'Weekly/Monthly'
  },
  {
    type: 'promotional',
    label: 'Promotional Campaign',
    description: 'Sales announcements, discounts, and special offers',
    recommended: true,
    frequency: 'As needed'
  },
  {
    type: 'welcome',
    label: 'Welcome Series',
    description: 'Onboard new subscribers with automated sequence',
    recommended: true,
    frequency: 'Triggered'
  },
  {
    type: 'abandoned_cart',
    label: 'Abandoned Cart',
    description: 'Recover lost sales with targeted reminders',
    recommended: false,
    frequency: 'Triggered'
  },
  {
    type: 'drip',
    label: 'Drip Campaign',
    description: 'Nurture leads with scheduled content series',
    recommended: false,
    frequency: 'Scheduled'
  },
  {
    type: 'announcement',
    label: 'Announcements',
    description: 'Product launches, company news, and updates',
    recommended: false,
    frequency: 'As needed'
  }
];

const EMAIL_TEMPLATES = [
  { value: 'custom', label: 'Custom Design', description: 'Build from scratch' },
  { value: 'newsletter', label: 'Newsletter Template', description: 'Clean content-focused layout' },
  { value: 'promotional', label: 'Promotional Template', description: 'Sales and offer-focused design' },
  { value: 'welcome', label: 'Welcome Template', description: 'Onboarding and introduction layout' },
  { value: 'transactional', label: 'Transactional Template', description: 'Receipts and confirmations' }
];

const TEMPLATE_STYLES = [
  { value: 'minimal', label: 'Minimal', description: 'Clean and simple design' },
  { value: 'corporate', label: 'Corporate', description: 'Professional business style' },
  { value: 'creative', label: 'Creative', description: 'Bold and artistic design' },
  { value: 'ecommerce', label: 'E-commerce', description: 'Product-focused layout' }
];

export function EmailMarketingWizard({ data, onUpdate, onValidate }: EmailMarketingWizardProps) {
  const [currentStep, setCurrentStep] = useState(1);
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  const steps = [
    { number: 1, title: 'Campaign Type', icon: Target },
    { number: 2, title: 'Audience Selection', icon: Users },
    { number: 3, title: 'Email Content', icon: Edit3 },
    { number: 4, title: 'Delivery Setup', icon: BarChart3 },
    { number: 5, title: 'Tracking & Launch', icon: Rocket }
  ];

  const updateData = (updates: Partial<EmailMarketingData>) => {
    onUpdate({ ...data, ...updates });
  };

  const validateStep = (step: number): boolean => {
    const errors: Record<string, string> = {};

    switch (step) {
      case 1:
        if (!data.campaignType) errors.campaignType = 'Please select a campaign type';
        break;
      case 2:
        if (data.audience.segments.filter(s => s.selected).length === 0) errors.segments = 'Select at least one audience segment';
        break;
      case 3:
        if (!data.content.content.subjectLine) errors.subjectLine = 'Subject line is required';
        if (!data.content.content.bodyText) errors.bodyText = 'Email content is required';
        break;
      case 4:
        if (data.delivery.scheduling.type === 'scheduled' && !data.delivery.scheduling.scheduleDate) {
          errors.scheduleDate = 'Schedule date is required';
        }
        break;
      case 5:
        if (data.tracking.goals.length === 0) errors.goals = 'Add at least one performance goal';
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

  const toggleSegment = (segmentId: string) => {
    const updatedSegments = data.audience.segments.map(segment =>
      segment.id === segmentId ? { ...segment, selected: !segment.selected } : segment
    );
    updateData({
      audience: { ...data.audience, segments: updatedSegments }
    });
  };

  const addCallToAction = () => {
    updateData({
      content: {
        ...data.content,
        content: {
          ...data.content.content,
          callToAction: [...data.content.content.callToAction, {
            text: '',
            url: '',
            style: 'button'
          }]
        }
      }
    });
  };

  const updateCallToAction = (index: number, updates: Partial<EmailContent['content']['callToAction'][0]>) => {
    const newCTAs = [...data.content.content.callToAction];
    newCTAs[index] = { ...newCTAs[index], ...updates };
    updateData({
      content: {
        ...data.content,
        content: {
          ...data.content.content,
          callToAction: newCTAs
        }
      }
    });
  };

  const removeCallToAction = (index: number) => {
    updateData({
      content: {
        ...data.content,
        content: {
          ...data.content.content,
          callToAction: data.content.content.callToAction.filter((_, i) => i !== index)
        }
      }
    });
  };

  const addPerformanceGoal = () => {
    updateData({
      tracking: {
        ...data.tracking,
        goals: [...data.tracking.goals, {
          name: '',
          metric: 'open_rate',
          target: 25,
          priority: 'medium'
        }]
      }
    });
  };

  const updatePerformanceGoal = (index: number, updates: Partial<PerformanceTracking['goals'][0]>) => {
    const newGoals = [...data.tracking.goals];
    newGoals[index] = { ...newGoals[index], ...updates };
    updateData({
      tracking: {
        ...data.tracking,
        goals: newGoals
      }
    });
  };

  const removePerformanceGoal = (index: number) => {
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
        <h3 className="text-lg font-semibold mb-4">Choose your email campaign type</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {CAMPAIGN_TYPES.map((campaign) => (
            <div
              key={campaign.type}
              className={`border rounded-lg p-4 cursor-pointer transition-all relative ${
                data.campaignType?.type === campaign.type
                  ? 'border-green-500 bg-green-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => updateData({ campaignType: campaign })}
            >
              {campaign.recommended && (
                <div className="absolute -top-2 -right-2">
                  <span className="bg-green-500 text-white text-xs px-2 py-1 rounded-full">
                    Recommended
                  </span>
                </div>
              )}
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900">{campaign.label}</h4>
                  <p className="text-sm text-gray-600 mt-1">{campaign.description}</p>
                  <p className="text-xs text-gray-500 mt-2">
                    Frequency: {campaign.frequency}
                  </p>
                </div>
                {data.campaignType?.type === campaign.type && (
                  <Check size={20} className="text-green-500 ml-2" />
                )}
              </div>
            </div>
          ))}
        </div>
        {validationErrors.campaignType && (
          <p className="text-red-500 text-sm mt-2">{validationErrors.campaignType}</p>
        )}
      </div>
    </div>
  );

  const renderStep2 = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Select your audience segments</h3>
        
        {/* Predefined Segments */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-3">Available Segments</label>
          <div className="space-y-3">
            {data.audience.segments.map((segment) => (
              <div
                key={segment.id}
                className={`border rounded-lg p-4 cursor-pointer transition-all ${
                  segment.selected
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => toggleSegment(segment.id)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900">{segment.name}</h4>
                    <p className="text-sm text-gray-600 mt-1">
                      {segment.size.toLocaleString()} subscribers
                    </p>
                    <div className="mt-2">
                      <div className="flex flex-wrap gap-2">
                        {segment.criteria.behaviors.slice(0, 3).map((behavior, index) => (
                          <span key={index} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                            {behavior}
                          </span>
                        ))}
                        {segment.criteria.behaviors.length > 3 && (
                          <span className="text-xs text-gray-500">
                            +{segment.criteria.behaviors.length - 3} more
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="ml-4">
                    {segment.selected ? (
                      <Check size={20} className="text-blue-500" />
                    ) : (
                      <div className="w-5 h-5 border border-gray-300 rounded" />
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
          {validationErrors.segments && (
            <p className="text-red-500 text-sm mt-2">{validationErrors.segments}</p>
          )}
        </div>

        {/* Custom Lists */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Custom Email Lists</label>
          <div className="space-y-2">
            {data.audience.customLists.map((list, index) => (
              <div key={index} className="flex items-center gap-2">
                <input
                  type="text"
                  value={list}
                  onChange={(e) => {
                    const newLists = [...data.audience.customLists];
                    newLists[index] = e.target.value;
                    updateData({
                      audience: { ...data.audience, customLists: newLists }
                    });
                  }}
                  className="flex-1 border border-gray-300 rounded-lg px-3 py-2"
                  placeholder="Enter custom list name or upload CSV"
                />
                <button
                  onClick={() => {
                    const newLists = data.audience.customLists.filter((_, i) => i !== index);
                    updateData({
                      audience: { ...data.audience, customLists: newLists }
                    });
                  }}
                  className="px-3 py-2 text-red-600 hover:text-red-700"
                >
                  <X size={16} />
                </button>
              </div>
            ))}
            <button
              onClick={() => updateData({
                audience: {
                  ...data.audience,
                  customLists: [...data.audience.customLists, '']
                }
              })}
              className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-gray-600 hover:text-gray-700"
            >
              <Plus size={16} />
              Add Custom List
            </button>
          </div>
        </div>

        {/* Exclusions */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Exclude Segments</label>
          <div className="space-y-2">
            <div className="flex flex-wrap gap-2">
              {data.audience.exclusions.map((exclusion, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-red-100 text-red-800"
                >
                  {exclusion}
                  <button
                    onClick={() => {
                      const newExclusions = data.audience.exclusions.filter((_, i) => i !== index);
                      updateData({
                        audience: { ...data.audience, exclusions: newExclusions }
                      });
                    }}
                    className="ml-2 hover:text-red-600"
                  >
                    <X size={14} />
                  </button>
                </span>
              ))}
            </div>
            <input
              type="text"
              placeholder="Add exclusion (e.g., 'unsubscribed', 'bounced')"
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  const exclusion = (e.target as HTMLInputElement).value;
                  if (exclusion && !data.audience.exclusions.includes(exclusion)) {
                    updateData({
                      audience: {
                        ...data.audience,
                        exclusions: [...data.audience.exclusions, exclusion]
                      }
                    });
                    (e.target as HTMLInputElement).value = '';
                  }
                }
              }}
            />
          </div>
        </div>

        {/* Summary */}
        <div className="bg-blue-50 rounded-lg p-4">
          <h4 className="font-medium text-blue-900 mb-2">Audience Summary</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-blue-700 font-medium">Selected Segments:</span>
              <span className="text-blue-600 ml-2">
                {data.audience.segments.filter(s => s.selected).length}
              </span>
            </div>
            <div>
              <span className="text-blue-700 font-medium">Total Reach:</span>
              <span className="text-blue-600 ml-2">
                {data.audience.segments
                  .filter(s => s.selected)
                  .reduce((sum, s) => sum + s.size, 0)
                  .toLocaleString()}
              </span>
            </div>
            <div>
              <span className="text-blue-700 font-medium">Custom Lists:</span>
              <span className="text-blue-600 ml-2">
                {data.audience.customLists.filter(l => l.trim()).length}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderStep3 = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Design your email content</h3>
        
        {/* Template Selection */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Email Template</label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {EMAIL_TEMPLATES.map((template) => (
              <div
                key={template.value}
                className={`border rounded-lg p-3 cursor-pointer transition-all ${
                  data.content.template.type === template.value
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => updateData({
                  content: {
                    ...data.content,
                    template: {
                      ...data.content.template,
                      type: template.value as EmailContent['template']['type']
                    }
                  }
                })}
              >
                <h4 className="font-medium text-gray-900">{template.label}</h4>
                <p className="text-sm text-gray-600">{template.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Template Style */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Template Style</label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {TEMPLATE_STYLES.map((style) => (
              <div
                key={style.value}
                className={`border rounded-lg p-3 cursor-pointer transition-all text-center ${
                  data.content.template.style === style.value
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => updateData({
                  content: {
                    ...data.content,
                    template: {
                      ...data.content.template,
                      style: style.value as EmailContent['template']['style']
                    }
                  }
                })}
              >
                <h4 className="font-medium text-gray-900">{style.label}</h4>
                <p className="text-xs text-gray-600">{style.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Email Content */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Subject Line</label>
          <input
            type="text"
            value={data.content.content.subjectLine}
            onChange={(e) => updateData({
              content: {
                ...data.content,
                content: {
                  ...data.content.content,
                  subjectLine: e.target.value
                }
              }
            })}
            maxLength={100}
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
            placeholder="Enter compelling subject line"
          />
          <div className="text-sm text-gray-500 mt-1">
            {data.content.content.subjectLine.length}/100 characters
          </div>
          {validationErrors.subjectLine && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.subjectLine}</p>
          )}
        </div>

        {/* Preheader */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Preheader Text</label>
          <input
            type="text"
            value={data.content.content.preheader}
            onChange={(e) => updateData({
              content: {
                ...data.content,
                content: {
                  ...data.content.content,
                  preheader: e.target.value
                }
              }
            })}
            maxLength={150}
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
            placeholder="Preview text that appears after subject line"
          />
          <div className="text-sm text-gray-500 mt-1">
            {data.content.content.preheader.length}/150 characters
          </div>
        </div>

        {/* Main Content */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Email Content</label>
          <div className="space-y-3">
            <input
              type="text"
              value={data.content.content.headline}
              onChange={(e) => updateData({
                content: {
                  ...data.content,
                  content: {
                    ...data.content.content,
                    headline: e.target.value
                  }
                }
              })}
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
              placeholder="Main headline"
            />
            <textarea
              value={data.content.content.bodyText}
              onChange={(e) => updateData({
                content: {
                  ...data.content,
                  content: {
                    ...data.content.content,
                    bodyText: e.target.value
                  }
                }
              })}
              rows={6}
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
              placeholder="Write your email content here..."
            />
          </div>
          {validationErrors.bodyText && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.bodyText}</p>
          )}
        </div>

        {/* Call to Actions */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Call to Actions</label>
          <div className="space-y-3">
            {data.content.content.callToAction.map((cta, index) => (
              <div key={index} className="border rounded-lg p-3">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  <input
                    type="text"
                    value={cta.text}
                    onChange={(e) => updateCallToAction(index, { text: e.target.value })}
                    placeholder="Button text"
                    className="border border-gray-300 rounded-lg px-3 py-2"
                  />
                  <input
                    type="url"
                    value={cta.url}
                    onChange={(e) => updateCallToAction(index, { url: e.target.value })}
                    placeholder="https://your-website.com"
                    className="border border-gray-300 rounded-lg px-3 py-2"
                  />
                  <div className="flex gap-2">
                    <select
                      value={cta.style}
                      onChange={(e) => updateCallToAction(index, { style: e.target.value as EmailContent['content']['callToAction'][0]['style'] })}
                      className="flex-1 border border-gray-300 rounded-lg px-3 py-2"
                    >
                      <option value="button">Button</option>
                      <option value="link">Text Link</option>
                      <option value="banner">Banner</option>
                    </select>
                    <button
                      onClick={() => removeCallToAction(index)}
                      className="px-3 py-2 text-red-600 hover:text-red-700"
                    >
                      <X size={16} />
                    </button>
                  </div>
                </div>
              </div>
            ))}
            <button
              onClick={addCallToAction}
              className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-gray-600 hover:text-gray-700"
            >
              <Plus size={16} />
              Add Call to Action
            </button>
          </div>
        </div>

        {/* Personalization */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Personalization</label>
          <div className="space-y-2">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={data.content.personalization.useFirstName}
                onChange={(e) => updateData({
                  content: {
                    ...data.content,
                    personalization: {
                      ...data.content.personalization,
                      useFirstName: e.target.checked
                    }
                  }
                })}
                className="mr-2"
              />
              Use first name in greeting
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={data.content.personalization.useCompanyName}
                onChange={(e) => updateData({
                  content: {
                    ...data.content,
                    personalization: {
                      ...data.content.personalization,
                      useCompanyName: e.target.checked
                    }
                  }
                })}
                className="mr-2"
              />
              Include company name
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={data.content.personalization.dynamicContent}
                onChange={(e) => updateData({
                  content: {
                    ...data.content,
                    personalization: {
                      ...data.content.personalization,
                      dynamicContent: e.target.checked
                    }
                  }
                })}
                className="mr-2"
              />
              Enable dynamic content based on user behavior
            </label>
          </div>
        </div>
      </div>
    </div>
  );

  const renderStep4 = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4">Configure delivery and optimization</h3>
        
        {/* Scheduling */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Send Schedule</label>
          <div className="space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
              <label className="flex items-center">
                <input
                  type="radio"
                  checked={data.delivery.scheduling.type === 'immediate'}
                  onChange={() => updateData({
                    delivery: {
                      ...data.delivery,
                      scheduling: { ...data.delivery.scheduling, type: 'immediate' }
                    }
                  })}
                  className="mr-2"
                />
                Send Now
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  checked={data.delivery.scheduling.type === 'scheduled'}
                  onChange={() => updateData({
                    delivery: {
                      ...data.delivery,
                      scheduling: { ...data.delivery.scheduling, type: 'scheduled' }
                    }
                  })}
                  className="mr-2"
                />
                Schedule
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  checked={data.delivery.scheduling.type === 'optimized'}
                  onChange={() => updateData({
                    delivery: {
                      ...data.delivery,
                      scheduling: { ...data.delivery.scheduling, type: 'optimized' }
                    }
                  })}
                  className="mr-2"
                />
                Optimized
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  checked={data.delivery.scheduling.type === 'drip'}
                  onChange={() => updateData({
                    delivery: {
                      ...data.delivery,
                      scheduling: { ...data.delivery.scheduling, type: 'drip' }
                    }
                  })}
                  className="mr-2"
                />
                Drip Series
              </label>
            </div>
            
            {data.delivery.scheduling.type === 'scheduled' && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <input
                  type="date"
                  value={data.delivery.scheduling.scheduleDate || ''}
                  onChange={(e) => updateData({
                    delivery: {
                      ...data.delivery,
                      scheduling: {
                        ...data.delivery.scheduling,
                        scheduleDate: e.target.value
                      }
                    }
                  })}
                  className="border border-gray-300 rounded-lg px-3 py-2"
                />
                <input
                  type="time"
                  value={data.delivery.scheduling.scheduleTime || ''}
                  onChange={(e) => updateData({
                    delivery: {
                      ...data.delivery,
                      scheduling: {
                        ...data.delivery.scheduling,
                        scheduleTime: e.target.value
                      }
                    }
                  })}
                  className="border border-gray-300 rounded-lg px-3 py-2"
                />
                <select
                  value={data.delivery.scheduling.timezone}
                  onChange={(e) => updateData({
                    delivery: {
                      ...data.delivery,
                      scheduling: {
                        ...data.delivery.scheduling,
                        timezone: e.target.value
                      }
                    }
                  })}
                  className="border border-gray-300 rounded-lg px-3 py-2"
                >
                  <option value="UTC">UTC</option>
                  <option value="EST">Eastern Time</option>
                  <option value="CST">Central Time</option>
                  <option value="MST">Mountain Time</option>
                  <option value="PST">Pacific Time</option>
                </select>
              </div>
            )}
            {validationErrors.scheduleDate && (
              <p className="text-red-500 text-sm mt-1">{validationErrors.scheduleDate}</p>
            )}
          </div>
        </div>

        {/* Optimization Settings */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Optimization Settings</label>
          <div className="space-y-2">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={data.delivery.optimization.sendTimeOptimization}
                onChange={(e) => updateData({
                  delivery: {
                    ...data.delivery,
                    optimization: {
                      ...data.delivery.optimization,
                      sendTimeOptimization: e.target.checked
                    }
                  }
                })}
                className="mr-2"
              />
              Optimize send times for each recipient
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={data.delivery.optimization.deliverabilityOptimization}
                onChange={(e) => updateData({
                  delivery: {
                    ...data.delivery,
                    optimization: {
                      ...data.delivery.optimization,
                      deliverabilityOptimization: e.target.checked
                    }
                  }
                })}
                className="mr-2"
              />
              Enable deliverability optimization
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={data.delivery.optimization.frequencyOptimization}
                onChange={(e) => updateData({
                  delivery: {
                    ...data.delivery,
                    optimization: {
                      ...data.delivery.optimization,
                      frequencyOptimization: e.target.checked
                    }
                  }
                })}
                className="mr-2"
              />
              Optimize frequency to prevent fatigue
            </label>
          </div>
        </div>

        {/* A/B Testing */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">A/B Testing (Optional)</label>
          <div className="space-y-3">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Subject Line Tests</label>
              <div className="space-y-2">
                {data.delivery.optimization.subjectLineTests.map((test, index) => (
                  <div key={index} className="flex gap-2">
                    <input
                      type="text"
                      value={test}
                      onChange={(e) => {
                        const newTests = [...data.delivery.optimization.subjectLineTests];
                        newTests[index] = e.target.value;
                        updateData({
                          delivery: {
                            ...data.delivery,
                            optimization: {
                              ...data.delivery.optimization,
                              subjectLineTests: newTests
                            }
                          }
                        });
                      }}
                      placeholder={`Subject line variant ${index + 1}`}
                      className="flex-1 border border-gray-300 rounded-lg px-3 py-2"
                    />
                    <button
                      onClick={() => {
                        const newTests = data.delivery.optimization.subjectLineTests.filter((_, i) => i !== index);
                        updateData({
                          delivery: {
                            ...data.delivery,
                            optimization: {
                              ...data.delivery.optimization,
                              subjectLineTests: newTests
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
                <button
                  onClick={() => updateData({
                    delivery: {
                      ...data.delivery,
                      optimization: {
                        ...data.delivery.optimization,
                        subjectLineTests: [...data.delivery.optimization.subjectLineTests, '']
                      }
                    }
                  })}
                  className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-gray-600 hover:text-gray-700"
                >
                  <Plus size={16} />
                  Add Subject Line Variant
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Send Limits */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Send Limits</label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Max emails per hour</label>
              <input
                type="number"
                value={data.delivery.limits.maxPerHour}
                onChange={(e) => updateData({
                  delivery: {
                    ...data.delivery,
                    limits: {
                      ...data.delivery.limits,
                      maxPerHour: parseInt(e.target.value) || 0
                    }
                  }
                })}
                min="1"
                max="10000"
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Max emails per day</label>
              <input
                type="number"
                value={data.delivery.limits.maxPerDay}
                onChange={(e) => updateData({
                  delivery: {
                    ...data.delivery,
                    limits: {
                      ...data.delivery.limits,
                      maxPerDay: parseInt(e.target.value) || 0
                    }
                  }
                })}
                min="1"
                max="100000"
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
        
        {/* Performance Goals */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Performance Goals</label>
          <div className="space-y-3">
            {data.tracking.goals.map((goal, index) => (
              <div key={index} className="border rounded-lg p-4">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
                  <input
                    type="text"
                    value={goal.name}
                    onChange={(e) => updatePerformanceGoal(index, { name: e.target.value })}
                    placeholder="Goal name"
                    className="border border-gray-300 rounded-lg px-3 py-2"
                  />
                  <select
                    value={goal.metric}
                    onChange={(e) => updatePerformanceGoal(index, { metric: e.target.value as PerformanceTracking['goals'][0]['metric'] })}
                    className="border border-gray-300 rounded-lg px-3 py-2"
                  >
                    <option value="open_rate">Open Rate (%)</option>
                    <option value="click_rate">Click Rate (%)</option>
                    <option value="conversion_rate">Conversion Rate (%)</option>
                    <option value="revenue">Revenue ($)</option>
                    <option value="unsubscribe_rate">Unsubscribe Rate (%)</option>
                  </select>
                  <input
                    type="number"
                    value={goal.target}
                    onChange={(e) => updatePerformanceGoal(index, { target: parseFloat(e.target.value) || 0 })}
                    placeholder="Target"
                    className="border border-gray-300 rounded-lg px-3 py-2"
                  />
                  <div className="flex gap-2">
                    <select
                      value={goal.priority}
                      onChange={(e) => updatePerformanceGoal(index, { priority: e.target.value as PerformanceTracking['goals'][0]['priority'] })}
                      className="border border-gray-300 rounded-lg px-3 py-2"
                    >
                      <option value="high">High</option>
                      <option value="medium">Medium</option>
                      <option value="low">Low</option>
                    </select>
                    <button
                      onClick={() => removePerformanceGoal(index)}
                      className="px-3 py-2 text-red-600 hover:text-red-700"
                    >
                      <X size={16} />
                    </button>
                  </div>
                </div>
              </div>
            ))}
            <button
              onClick={addPerformanceGoal}
              className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-gray-600 hover:text-gray-700"
            >
              <Plus size={16} />
              Add Performance Goal
            </button>
          </div>
          {validationErrors.goals && (
            <p className="text-red-500 text-sm mt-1">{validationErrors.goals}</p>
          )}
        </div>

        {/* Tracking Settings */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Tracking Options</label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={data.tracking.tracking.opens}
                onChange={(e) => updateData({
                  tracking: {
                    ...data.tracking,
                    tracking: { ...data.tracking.tracking, opens: e.target.checked }
                  }
                })}
                className="mr-2"
              />
              <Eye size={16} className="mr-1" />
              Track Opens
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={data.tracking.tracking.clicks}
                onChange={(e) => updateData({
                  tracking: {
                    ...data.tracking,
                    tracking: { ...data.tracking.tracking, clicks: e.target.checked }
                  }
                })}
                className="mr-2"
              />
              <MousePointer size={16} className="mr-1" />
              Track Clicks
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={data.tracking.tracking.conversions}
                onChange={(e) => updateData({
                  tracking: {
                    ...data.tracking,
                    tracking: { ...data.tracking.tracking, conversions: e.target.checked }
                  }
                })}
                className="mr-2"
              />
              <TrendingUp size={16} className="mr-1" />
              Track Conversions
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={data.tracking.tracking.revenue}
                onChange={(e) => updateData({
                  tracking: {
                    ...data.tracking,
                    tracking: { ...data.tracking.tracking, revenue: e.target.checked }
                  }
                })}
                className="mr-2"
              />
              💰 Track Revenue
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={data.tracking.tracking.socialShares}
                onChange={(e) => updateData({
                  tracking: {
                    ...data.tracking,
                    tracking: { ...data.tracking.tracking, socialShares: e.target.checked }
                  }
                })}
                className="mr-2"
              />
              📱 Social Shares
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={data.tracking.tracking.forwards}
                onChange={(e) => updateData({
                  tracking: {
                    ...data.tracking,
                    tracking: { ...data.tracking.tracking, forwards: e.target.checked }
                  }
                })}
                className="mr-2"
              />
              📤 Email Forwards
            </label>
          </div>
        </div>

        {/* Integration Setup */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Analytics Integration</label>
          <div className="space-y-3">
            <input
              type="text"
              value={data.tracking.integration.googleAnalytics || ''}
              onChange={(e) => updateData({
                tracking: {
                  ...data.tracking,
                  integration: {
                    ...data.tracking.integration,
                    googleAnalytics: e.target.value
                  }
                }
              })}
              placeholder="Google Analytics ID (G-XXXXXXXXXX)"
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            />
            <input
              type="text"
              value={data.tracking.integration.facebookPixel || ''}
              onChange={(e) => updateData({
                tracking: {
                  ...data.tracking,
                  integration: {
                    ...data.tracking.integration,
                    facebookPixel: e.target.value
                  }
                }
              })}
              placeholder="Facebook Pixel ID"
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            />
          </div>
        </div>

        {/* Campaign Summary */}
        <div className="bg-green-50 rounded-lg p-6">
          <h4 className="font-medium text-green-900 mb-4">Campaign Summary</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h5 className="text-sm font-medium text-green-700 mb-2">Campaign Type</h5>
              <p className="text-green-900">{data.campaignType?.label || 'Not selected'}</p>
            </div>
            <div>
              <h5 className="text-sm font-medium text-green-700 mb-2">Audience</h5>
              <p className="text-green-900">
                {data.audience.segments.filter(s => s.selected).length} segments,{' '}
                {data.audience.segments
                  .filter(s => s.selected)
                  .reduce((sum, s) => sum + s.size, 0)
                  .toLocaleString()} recipients
              </p>
            </div>
            <div>
              <h5 className="text-sm font-medium text-green-700 mb-2">Subject Line</h5>
              <p className="text-green-900">{data.content.content.subjectLine || 'Not set'}</p>
            </div>
            <div>
              <h5 className="text-sm font-medium text-green-700 mb-2">Send Schedule</h5>
              <p className="text-green-900 capitalize">
                {data.delivery.scheduling.type === 'scheduled' 
                  ? `${data.delivery.scheduling.scheduleDate} ${data.delivery.scheduling.scheduleTime}`
                  : data.delivery.scheduling.type
                }
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
                  ? 'bg-green-600 text-white'
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
                  currentStep > step.number ? 'bg-green-600' : 'bg-gray-200'
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
            className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
          >
            Next
          </button>
        ) : (
          <button
            onClick={() => {
              if (validateStep(currentStep)) {
                // Handle campaign launch
                console.log('Launching Email Marketing campaign:', data);
              }
            }}
            className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2"
          >
            <Send size={16} />
            Launch Campaign
          </button>
        )}
      </div>
    </div>
  );
}