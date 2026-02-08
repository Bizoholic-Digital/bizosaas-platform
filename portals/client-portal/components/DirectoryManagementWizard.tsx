'use client';

import React, { useState, useEffect } from 'react';
import {
  ArrowRight, ArrowLeft, CheckCircle, AlertCircle, Info, Star,
  MapPin, Building2, Phone, Mail, Globe, Clock, Image,
  Target, TrendingUp, Settings, Shield, Key,
  Chrome, Facebook, Apple, Search, MessageSquare,
  Users, DollarSign, Calendar, Upload, Eye, EyeOff,
  Loader2, RefreshCw, X, Plus, Minus, Edit3,
  Lightbulb, Zap, Brain, BarChart3, Gauge
} from 'lucide-react';

// Types for the wizard
interface BusinessProfile {
  name: string;
  description: string;
  category: string;
  subcategory: string;
  address: {
    street: string;
    city: string;
    state: string;
    zipCode: string;
    country: string;
  };
  contact: {
    phone: string;
    email: string;
    website: string;
  };
  hours: {
    [key: string]: {
      open: string;
      close: string;
      closed: boolean;
    };
  };
  serviceAreas: string[];
  photos: string[];
  specialHours: Array<{
    date: string;
    hours: string;
    type: 'holiday' | 'special' | 'closed';
  }>;
}

interface PlatformConfig {
  id: string;
  name: string;
  icon: React.ComponentType;
  tier: 1 | 2 | 3;
  enabled: boolean;
  connected: boolean;
  credentials?: any;
  config?: any;
  estimatedRoi: number;
  difficulty: 'easy' | 'medium' | 'hard';
  timeToSetup: string;
  features: string[];
}

interface WizardStep {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  optional: boolean;
}

interface AIRecommendations {
  recommendedPlatforms: string[];
  businessInsights: string[];
  optimizationTips: string[];
  competitorAnalysis: {
    platforms: string[];
    averageRating: number;
    gapsIdentified: string[];
  };
}

const WIZARD_STEPS: WizardStep[] = [
  {
    id: 'business-profile',
    title: 'Business Profile Setup',
    description: 'Provide your business information and verify details',
    completed: false,
    optional: false
  },
  {
    id: 'platform-selection',
    title: 'Platform Selection',
    description: 'Choose and prioritize directory platforms based on AI recommendations',
    completed: false,
    optional: false
  },
  {
    id: 'credentials-setup',
    title: 'Authentication Setup',
    description: 'Connect and authenticate with selected platforms',
    completed: false,
    optional: false
  },
  {
    id: 'platform-configuration',
    title: 'Platform Configuration',
    description: 'Configure platform-specific settings and preferences',
    completed: false,
    optional: true
  },
  {
    id: 'sync-strategy',
    title: 'Sync Strategy',
    description: 'Configure synchronization preferences and conflict resolution',
    completed: false,
    optional: false
  },
  {
    id: 'review-launch',
    title: 'Review & Launch',
    description: 'Review configuration and launch your multi-platform presence',
    completed: false,
    optional: false
  }
];

const AVAILABLE_PLATFORMS: PlatformConfig[] = [
  {
    id: 'google-business',
    name: 'Google Business Profile',
    icon: Chrome,
    tier: 1,
    enabled: false,
    connected: false,
    estimatedRoi: 95,
    difficulty: 'easy',
    timeToSetup: '10-15 minutes',
    features: ['Google Maps', 'Search Results', 'Reviews', 'Photos', 'Posts', 'Messaging']
  },
  {
    id: 'yelp',
    name: 'Yelp Business',
    icon: Star,
    tier: 1,
    enabled: false,
    connected: false,
    estimatedRoi: 85,
    difficulty: 'easy',
    timeToSetup: '5-10 minutes',
    features: ['Customer Reviews', 'Photos', 'Business Info', 'Special Offers', 'Events']
  },
  {
    id: 'facebook',
    name: 'Facebook Business',
    icon: Facebook,
    tier: 1,
    enabled: false,
    connected: false,
    estimatedRoi: 80,
    difficulty: 'medium',
    timeToSetup: '15-20 minutes',
    features: ['Business Page', 'Reviews', 'Events', 'Messaging', 'Ads Integration']
  },
  {
    id: 'apple-maps',
    name: 'Apple Maps',
    icon: Apple,
    tier: 1,
    enabled: false,
    connected: false,
    estimatedRoi: 70,
    difficulty: 'medium',
    timeToSetup: '10-15 minutes',
    features: ['Apple Maps', 'iOS Integration', 'Business Info', 'Photos']
  },
  {
    id: 'bing-places',
    name: 'Bing Places',
    icon: Search,
    tier: 2,
    enabled: false,
    connected: false,
    estimatedRoi: 60,
    difficulty: 'easy',
    timeToSetup: '5-10 minutes',
    features: ['Bing Search', 'Maps Integration', 'Business Listings']
  }
];

export function DirectoryManagementWizard() {
  const [currentStep, setCurrentStep] = useState(0);
  const [wizardSteps, setWizardSteps] = useState<WizardStep[]>(WIZARD_STEPS);
  const [businessProfile, setBusinessProfile] = useState<BusinessProfile>({
    name: '',
    description: '',
    category: '',
    subcategory: '',
    address: {
      street: '',
      city: '',
      state: '',
      zipCode: '',
      country: 'US'
    },
    contact: {
      phone: '',
      email: '',
      website: ''
    },
    hours: {
      monday: { open: '09:00', close: '17:00', closed: false },
      tuesday: { open: '09:00', close: '17:00', closed: false },
      wednesday: { open: '09:00', close: '17:00', closed: false },
      thursday: { open: '09:00', close: '17:00', closed: false },
      friday: { open: '09:00', close: '17:00', closed: false },
      saturday: { open: '10:00', close: '16:00', closed: false },
      sunday: { open: '10:00', close: '16:00', closed: true }
    },
    serviceAreas: [],
    photos: [],
    specialHours: []
  });
  const [platforms, setPlatforms] = useState<PlatformConfig[]>(AVAILABLE_PLATFORMS);
  const [aiRecommendations, setAiRecommendations] = useState<AIRecommendations | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [syncFrequency, setSyncFrequency] = useState<'realtime' | 'daily' | 'weekly'>('daily');
  const [conflictResolution, setConflictResolution] = useState<'auto' | 'manual'>('auto');

  // Handle step navigation
  const goToNextStep = () => {
    if (currentStep < wizardSteps.length - 1) {
      // Mark current step as completed
      const updatedSteps = [...wizardSteps];
      updatedSteps[currentStep].completed = true;
      setWizardSteps(updatedSteps);
      setCurrentStep(currentStep + 1);
    }
  };

  const goToPreviousStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const goToStep = (stepIndex: number) => {
    setCurrentStep(stepIndex);
  };

  // AI-powered business analysis
  const analyzeBusinessProfile = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/brain/directory-wizard/analyze-business', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(businessProfile)
      });
      const recommendations = await response.json();
      setAiRecommendations(recommendations);
      
      // Update platform recommendations
      const updatedPlatforms = platforms.map(platform => ({
        ...platform,
        enabled: recommendations.recommendedPlatforms.includes(platform.id)
      }));
      setPlatforms(updatedPlatforms);
    } catch (error) {
      console.error('Error analyzing business profile:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Platform connection handlers
  const connectPlatform = async (platformId: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`/api/brain/directory-wizard/connect/${platformId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ businessProfile })
      });
      const result = await response.json();
      
      if (result.success) {
        const updatedPlatforms = platforms.map(p => 
          p.id === platformId ? { ...p, connected: true, credentials: result.credentials } : p
        );
        setPlatforms(updatedPlatforms);
      }
    } catch (error) {
      console.error(`Error connecting to ${platformId}:`, error);
    } finally {
      setIsLoading(false);
    }
  };

  // Launch multi-platform sync
  const launchDirectorySetup = async () => {
    setIsLoading(true);
    try {
      const connectedPlatforms = platforms.filter(p => p.connected && p.enabled);
      
      const response = await fetch('/api/brain/directory-wizard/launch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          businessProfile,
          platforms: connectedPlatforms,
          syncStrategy: {
            frequency: syncFrequency,
            conflictResolution
          }
        })
      });
      
      const result = await response.json();
      
      if (result.success) {
        // Mark final step as completed
        const updatedSteps = [...wizardSteps];
        updatedSteps[currentStep].completed = true;
        setWizardSteps(updatedSteps);
        
        // Show success state or redirect
        console.log('Directory setup launched successfully!');
      }
    } catch (error) {
      console.error('Error launching directory setup:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Step content renderers
  const renderBusinessProfileStep = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
          <Building2 className="w-8 h-8 text-blue-600 dark:text-blue-400" />
        </div>
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white">Business Profile Setup</h3>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Let's start by gathering your business information. This will be used across all directory platforms.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Basic Information */}
        <div className="space-y-4">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white">Basic Information</h4>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Business Name *
            </label>
            <input
              type="text"
              value={businessProfile.name}
              onChange={(e) => setBusinessProfile(prev => ({ ...prev, name: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              placeholder="Enter your business name"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Business Description *
            </label>
            <textarea
              value={businessProfile.description}
              onChange={(e) => setBusinessProfile(prev => ({ ...prev, description: e.target.value }))}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              placeholder="Describe your business in a few sentences"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Category *
              </label>
              <select
                value={businessProfile.category}
                onChange={(e) => setBusinessProfile(prev => ({ ...prev, category: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              >
                <option value="">Select category</option>
                <option value="restaurant">Restaurant</option>
                <option value="retail">Retail</option>
                <option value="service">Service</option>
                <option value="healthcare">Healthcare</option>
                <option value="professional">Professional Services</option>
                <option value="automotive">Automotive</option>
                <option value="beauty">Beauty & Spa</option>
                <option value="fitness">Fitness & Recreation</option>
                <option value="education">Education</option>
                <option value="real-estate">Real Estate</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Subcategory
              </label>
              <input
                type="text"
                value={businessProfile.subcategory}
                onChange={(e) => setBusinessProfile(prev => ({ ...prev, subcategory: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                placeholder="e.g., Italian Restaurant"
              />
            </div>
          </div>
        </div>

        {/* Contact Information */}
        <div className="space-y-4">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white">Contact Information</h4>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Phone Number *
            </label>
            <input
              type="tel"
              value={businessProfile.contact.phone}
              onChange={(e) => setBusinessProfile(prev => ({ 
                ...prev, 
                contact: { ...prev.contact, phone: e.target.value }
              }))}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              placeholder="(555) 123-4567"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Email Address *
            </label>
            <input
              type="email"
              value={businessProfile.contact.email}
              onChange={(e) => setBusinessProfile(prev => ({ 
                ...prev, 
                contact: { ...prev.contact, email: e.target.value }
              }))}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              placeholder="business@example.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Website
            </label>
            <input
              type="url"
              value={businessProfile.contact.website}
              onChange={(e) => setBusinessProfile(prev => ({ 
                ...prev, 
                contact: { ...prev.contact, website: e.target.value }
              }))}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              placeholder="https://www.yourbusiness.com"
            />
          </div>

          {/* Address */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Street Address *
            </label>
            <input
              type="text"
              value={businessProfile.address.street}
              onChange={(e) => setBusinessProfile(prev => ({ 
                ...prev, 
                address: { ...prev.address, street: e.target.value }
              }))}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              placeholder="123 Main Street"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                City *
              </label>
              <input
                type="text"
                value={businessProfile.address.city}
                onChange={(e) => setBusinessProfile(prev => ({ 
                  ...prev, 
                  address: { ...prev.address, city: e.target.value }
                }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                placeholder="City"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                State *
              </label>
              <input
                type="text"
                value={businessProfile.address.state}
                onChange={(e) => setBusinessProfile(prev => ({ 
                  ...prev, 
                  address: { ...prev.address, state: e.target.value }
                }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                placeholder="State"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              ZIP Code *
            </label>
            <input
              type="text"
              value={businessProfile.address.zipCode}
              onChange={(e) => setBusinessProfile(prev => ({ 
                ...prev, 
                address: { ...prev.address, zipCode: e.target.value }
              }))}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              placeholder="12345"
            />
          </div>
        </div>
      </div>

      {/* Business Hours */}
      <div className="mt-8">
        <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Business Hours</h4>
        <div className="space-y-3">
          {Object.entries(businessProfile.hours).map(([day, hours]) => (
            <div key={day} className="flex items-center space-x-4">
              <div className="w-24">
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300 capitalize">
                  {day}
                </span>
              </div>
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={!hours.closed}
                  onChange={(e) => setBusinessProfile(prev => ({
                    ...prev,
                    hours: {
                      ...prev.hours,
                      [day]: { ...prev.hours[day], closed: !e.target.checked }
                    }
                  }))}
                  className="rounded border-gray-300"
                />
                <span className="text-sm text-gray-600 dark:text-gray-400">Open</span>
              </div>
              {!hours.closed && (
                <>
                  <input
                    type="time"
                    value={hours.open}
                    onChange={(e) => setBusinessProfile(prev => ({
                      ...prev,
                      hours: {
                        ...prev.hours,
                        [day]: { ...prev.hours[day], open: e.target.value }
                      }
                    }))}
                    className="px-2 py-1 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
                  />
                  <span className="text-gray-500">to</span>
                  <input
                    type="time"
                    value={hours.close}
                    onChange={(e) => setBusinessProfile(prev => ({
                      ...prev,
                      hours: {
                        ...prev.hours,
                        [day]: { ...prev.hours[day], close: e.target.value }
                      }
                    }))}
                    className="px-2 py-1 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
                  />
                </>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* AI Analysis Button */}
      <div className="mt-8 text-center">
        <button
          onClick={analyzeBusinessProfile}
          disabled={!businessProfile.name || !businessProfile.category || isLoading}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center mx-auto"
        >
          {isLoading ? (
            <Loader2 className="w-5 h-5 mr-2 animate-spin" />
          ) : (
            <Brain className="w-5 h-5 mr-2" />
          )}
          Analyze Business & Get AI Recommendations
        </button>
      </div>
    </div>
  );

  const renderPlatformSelectionStep = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
          <Target className="w-8 h-8 text-purple-600 dark:text-purple-400" />
        </div>
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white">Platform Selection & Prioritization</h3>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Based on your business profile, here are our AI-powered platform recommendations.
        </p>
      </div>

      {/* AI Recommendations */}
      {aiRecommendations && (
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 p-6 rounded-lg border border-blue-200 dark:border-blue-800 mb-6">
          <div className="flex items-center mb-4">
            <Lightbulb className="w-6 h-6 text-blue-600 dark:text-blue-400 mr-3" />
            <h4 className="text-lg font-semibold text-gray-900 dark:text-white">AI Insights & Recommendations</h4>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg">
              <h5 className="font-medium text-gray-900 dark:text-white mb-2">Business Insights</h5>
              <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                {aiRecommendations.businessInsights.map((insight, index) => (
                  <li key={index} className="flex items-start">
                    <CheckCircle className="w-3 h-3 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                    {insight}
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg">
              <h5 className="font-medium text-gray-900 dark:text-white mb-2">Optimization Tips</h5>
              <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                {aiRecommendations.optimizationTips.map((tip, index) => (
                  <li key={index} className="flex items-start">
                    <Zap className="w-3 h-3 text-yellow-500 mr-2 mt-0.5 flex-shrink-0" />
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg">
              <h5 className="font-medium text-gray-900 dark:text-white mb-2">Competitor Analysis</h5>
              <div className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                <div className="flex items-center">
                  <Star className="w-3 h-3 text-yellow-500 mr-2" />
                  Avg Rating: {aiRecommendations.competitorAnalysis.averageRating}
                </div>
                <div className="flex items-center">
                  <BarChart3 className="w-3 h-3 text-blue-500 mr-2" />
                  Active Platforms: {aiRecommendations.competitorAnalysis.platforms.length}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Platform Grid */}
      <div className="space-y-6">
        {[1, 2, 3].map(tier => (
          <div key={tier}>
            <div className="flex items-center mb-4">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-3 ${
                tier === 1 ? 'bg-gold-100 text-gold-600' :
                tier === 2 ? 'bg-silver-100 text-silver-600' :
                'bg-bronze-100 text-bronze-600'
              }`}>
                {tier}
              </div>
              <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
                Tier {tier} Platforms
                {tier === 1 && ' (Highest Priority)'}
                {tier === 2 && ' (Medium Priority)'}
                {tier === 3 && ' (Optional)'}
              </h4>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {platforms.filter(p => p.tier === tier).map(platform => {
                const Icon = platform.icon;
                return (
                  <div
                    key={platform.id}
                    className={`p-6 rounded-lg border-2 transition-all cursor-pointer ${
                      platform.enabled
                        ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                        : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-gray-300 dark:hover:border-gray-600'
                    }`}
                    onClick={() => {
                      const updatedPlatforms = platforms.map(p =>
                        p.id === platform.id ? { ...p, enabled: !p.enabled } : p
                      );
                      setPlatforms(updatedPlatforms);
                    }}
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center">
                        <div className="w-12 h-12 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center mr-4">
                          <Icon className="w-6 h-6 text-gray-600 dark:text-gray-400" />
                        </div>
                        <div>
                          <h5 className="font-semibold text-gray-900 dark:text-white">{platform.name}</h5>
                          <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
                            <span className="flex items-center">
                              <TrendingUp className="w-3 h-3 mr-1" />
                              {platform.estimatedRoi}% ROI
                            </span>
                            <span className="flex items-center">
                              <Clock className="w-3 h-3 mr-1" />
                              {platform.timeToSetup}
                            </span>
                            <span className={`px-2 py-1 rounded-full text-xs ${
                              platform.difficulty === 'easy' ? 'bg-green-100 text-green-700' :
                              platform.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                              'bg-red-100 text-red-700'
                            }`}>
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
                    
                    <div className="space-y-2">
                      <h6 className="font-medium text-gray-900 dark:text-white text-sm">Features:</h6>
                      <div className="flex flex-wrap gap-2">
                        {platform.features.map((feature, index) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 text-xs rounded-full"
                          >
                            {feature}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Platform Summary */}
      <div className="mt-8 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <h5 className="font-semibold text-gray-900 dark:text-white mb-2">Selection Summary</h5>
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-600 dark:text-gray-400">
            {platforms.filter(p => p.enabled).length} platforms selected
          </span>
          <span className="text-gray-600 dark:text-gray-400">
            Estimated combined ROI: {Math.round(platforms.filter(p => p.enabled).reduce((sum, p) => sum + p.estimatedRoi, 0) / Math.max(platforms.filter(p => p.enabled).length, 1))}%
          </span>
        </div>
      </div>
    </div>
  );

  const renderCredentialsSetupStep = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
          <Key className="w-8 h-8 text-green-600 dark:text-green-400" />
        </div>
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white">Authentication & Credentials Setup</h3>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Connect to your selected platforms securely. We'll guide you through each authentication process.
        </p>
      </div>

      <div className="space-y-4">
        {platforms.filter(p => p.enabled).map(platform => {
          const Icon = platform.icon;
          return (
            <div
              key={platform.id}
              className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center mr-4">
                    <Icon className="w-6 h-6 text-gray-600 dark:text-gray-400" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 dark:text-white">{platform.name}</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {platform.connected ? 'Connected successfully' : 'Ready to connect'}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  {platform.connected ? (
                    <div className="flex items-center text-green-600 dark:text-green-400">
                      <CheckCircle className="w-5 h-5 mr-2" />
                      <span className="text-sm font-medium">Connected</span>
                    </div>
                  ) : (
                    <button
                      onClick={() => connectPlatform(platform.id)}
                      disabled={isLoading}
                      className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center"
                    >
                      {isLoading ? (
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      ) : (
                        <Shield className="w-4 h-4 mr-2" />
                      )}
                      Connect
                    </button>
                  )}
                </div>
              </div>

              {/* Platform-specific instructions */}
              <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                <h5 className="font-medium text-gray-900 dark:text-white mb-2">Connection Steps:</h5>
                <ol className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                  {platform.id === 'google-business' && (
                    <>
                      <li>1. Sign in to your Google account</li>
                      <li>2. Grant access to Google Business Profile</li>
                      <li>3. Select or create your business listing</li>
                      <li>4. Verify ownership if required</li>
                    </>
                  )}
                  {platform.id === 'yelp' && (
                    <>
                      <li>1. Sign in to your Yelp Business account</li>
                      <li>2. Claim your business if not already claimed</li>
                      <li>3. Grant API access permissions</li>
                      <li>4. Verify business information</li>
                    </>
                  )}
                  {platform.id === 'facebook' && (
                    <>
                      <li>1. Sign in to your Facebook account</li>
                      <li>2. Select your business page or create new</li>
                      <li>3. Grant page management permissions</li>
                      <li>4. Configure business information</li>
                    </>
                  )}
                  {/* Add more platform-specific instructions */}
                </ol>
              </div>
            </div>
          );
        })}
      </div>

      {/* Connection Status Summary */}
      <div className="mt-8 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Shield className="w-5 h-5 text-blue-600 dark:text-blue-400 mr-3" />
            <span className="font-medium text-gray-900 dark:text-white">
              Connection Status: {platforms.filter(p => p.enabled && p.connected).length} of {platforms.filter(p => p.enabled).length} platforms connected
            </span>
          </div>
          <div className="text-sm text-blue-600 dark:text-blue-400">
            All connections are secured with OAuth 2.0
          </div>
        </div>
      </div>
    </div>
  );

  const renderSyncStrategyStep = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-orange-100 dark:bg-orange-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
          <RefreshCw className="w-8 h-8 text-orange-600 dark:text-orange-400" />
        </div>
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white">Sync Strategy Configuration</h3>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Configure how your business information stays synchronized across all platforms.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Sync Frequency */}
        <div>
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Sync Frequency</h4>
          <div className="space-y-3">
            {[
              {
                id: 'realtime',
                title: 'Real-time Sync',
                description: 'Instant updates across all platforms',
                price: '$29/month',
                features: ['Instant propagation', 'Conflict alerts', 'Priority support']
              },
              {
                id: 'daily',
                title: 'Daily Sync',
                description: 'Updates once per day at scheduled time',
                price: '$9/month',
                features: ['Daily updates', 'Basic reporting', 'Email notifications']
              },
              {
                id: 'weekly',
                title: 'Weekly Sync',
                description: 'Updates once per week',
                price: 'Free',
                features: ['Weekly updates', 'Basic sync status', 'Limited support']
              }
            ].map(option => (
              <div
                key={option.id}
                className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                  syncFrequency === option.id
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                    : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-gray-300'
                }`}
                onClick={() => setSyncFrequency(option.id as any)}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center">
                    <div className={`w-4 h-4 rounded-full border-2 mr-3 ${
                      syncFrequency === option.id ? 'border-blue-500 bg-blue-500' : 'border-gray-300'
                    }`}>
                      {syncFrequency === option.id && (
                        <div className="w-2 h-2 bg-white rounded-full mx-auto mt-0.5"></div>
                      )}
                    </div>
                    <h5 className="font-semibold text-gray-900 dark:text-white">{option.title}</h5>
                  </div>
                  <span className="text-sm font-medium text-green-600 dark:text-green-400">
                    {option.price}
                  </span>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 ml-7">
                  {option.description}
                </p>
                <ul className="text-xs text-gray-500 dark:text-gray-400 ml-7 space-y-1">
                  {option.features.map((feature, index) => (
                    <li key={index} className="flex items-center">
                      <CheckCircle className="w-3 h-3 text-green-500 mr-2" />
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* Conflict Resolution */}
        <div>
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Conflict Resolution</h4>
          <div className="space-y-3">
            <div
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                conflictResolution === 'auto'
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                  : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-gray-300'
              }`}
              onClick={() => setConflictResolution('auto')}
            >
              <div className="flex items-center mb-2">
                <div className={`w-4 h-4 rounded-full border-2 mr-3 ${
                  conflictResolution === 'auto' ? 'border-blue-500 bg-blue-500' : 'border-gray-300'
                }`}>
                  {conflictResolution === 'auto' && (
                    <div className="w-2 h-2 bg-white rounded-full mx-auto mt-0.5"></div>
                  )}
                </div>
                <h5 className="font-semibold text-gray-900 dark:text-white">Automatic Resolution</h5>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 ml-7">
                AI automatically resolves conflicts using smart rules and business logic
              </p>
            </div>

            <div
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                conflictResolution === 'manual'
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                  : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-gray-300'
              }`}
              onClick={() => setConflictResolution('manual')}
            >
              <div className="flex items-center mb-2">
                <div className={`w-4 h-4 rounded-full border-2 mr-3 ${
                  conflictResolution === 'manual' ? 'border-blue-500 bg-blue-500' : 'border-gray-300'
                }`}>
                  {conflictResolution === 'manual' && (
                    <div className="w-2 h-2 bg-white rounded-full mx-auto mt-0.5"></div>
                  )}
                </div>
                <h5 className="font-semibold text-gray-900 dark:text-white">Manual Review</h5>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 ml-7">
                You review and approve all changes before they're applied to platforms
              </p>
            </div>
          </div>

          {/* Source Priority */}
          <div className="mt-6">
            <h5 className="font-medium text-gray-900 dark:text-white mb-3">Platform Priority</h5>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Set which platform takes precedence when information conflicts occur:
            </p>
            <div className="space-y-2">
              {platforms.filter(p => p.enabled).map((platform, index) => (
                <div key={platform.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="flex items-center">
                    <div className="w-6 h-6 bg-blue-100 dark:bg-blue-900/30 rounded flex items-center justify-center mr-3">
                      <span className="text-xs font-medium text-blue-600 dark:text-blue-400">{index + 1}</span>
                    </div>
                    <span className="text-sm font-medium text-gray-900 dark:text-white">{platform.name}</span>
                  </div>
                  <div className="flex space-x-1">
                    <button className="p-1 hover:bg-gray-200 dark:hover:bg-gray-600 rounded">
                      <ArrowLeft className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                    </button>
                    <button className="p-1 hover:bg-gray-200 dark:hover:bg-gray-600 rounded">
                      <ArrowRight className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Configuration Summary */}
      <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-green-50 dark:from-blue-900/20 dark:to-green-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
        <h4 className="font-semibold text-gray-900 dark:text-white mb-4">Configuration Summary</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <h5 className="font-medium text-gray-900 dark:text-white mb-2">Sync Frequency</h5>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {syncFrequency === 'realtime' ? 'Real-time updates' : 
               syncFrequency === 'daily' ? 'Daily synchronization' : 
               'Weekly synchronization'}
            </p>
          </div>
          <div>
            <h5 className="font-medium text-gray-900 dark:text-white mb-2">Conflict Resolution</h5>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {conflictResolution === 'auto' ? 'Automatic AI resolution' : 'Manual review required'}
            </p>
          </div>
          <div>
            <h5 className="font-medium text-gray-900 dark:text-white mb-2">Connected Platforms</h5>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {platforms.filter(p => p.enabled && p.connected).length} platforms ready for sync
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderReviewLaunchStep = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
          <CheckCircle className="w-8 h-8 text-green-600 dark:text-green-400" />
        </div>
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white">Review & Launch</h3>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Review your configuration and launch your multi-platform directory presence.
        </p>
      </div>

      {/* Configuration Review */}
      <div className="space-y-6">
        {/* Business Profile Summary */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <Building2 className="w-5 h-5 mr-2" />
            Business Profile
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600 dark:text-gray-400">Business Name:</span>
              <span className="ml-2 font-medium text-gray-900 dark:text-white">{businessProfile.name}</span>
            </div>
            <div>
              <span className="text-gray-600 dark:text-gray-400">Category:</span>
              <span className="ml-2 font-medium text-gray-900 dark:text-white">{businessProfile.category}</span>
            </div>
            <div>
              <span className="text-gray-600 dark:text-gray-400">Address:</span>
              <span className="ml-2 font-medium text-gray-900 dark:text-white">
                {businessProfile.address.street}, {businessProfile.address.city}, {businessProfile.address.state}
              </span>
            </div>
            <div>
              <span className="text-gray-600 dark:text-gray-400">Phone:</span>
              <span className="ml-2 font-medium text-gray-900 dark:text-white">{businessProfile.contact.phone}</span>
            </div>
          </div>
        </div>

        {/* Platform Summary */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <Target className="w-5 h-5 mr-2" />
            Selected Platforms
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {platforms.filter(p => p.enabled).map(platform => {
              const Icon = platform.icon;
              return (
                <div key={platform.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="flex items-center">
                    <Icon className="w-5 h-5 text-gray-600 dark:text-gray-400 mr-3" />
                    <span className="font-medium text-gray-900 dark:text-white">{platform.name}</span>
                  </div>
                  <div className="flex items-center">
                    {platform.connected ? (
                      <CheckCircle className="w-5 h-5 text-green-500" />
                    ) : (
                      <AlertCircle className="w-5 h-5 text-yellow-500" />
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Sync Configuration Summary */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <RefreshCw className="w-5 h-5 mr-2" />
            Sync Configuration
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-gray-600 dark:text-gray-400">Frequency:</span>
              <span className="ml-2 font-medium text-gray-900 dark:text-white capitalize">{syncFrequency}</span>
            </div>
            <div>
              <span className="text-gray-600 dark:text-gray-400">Conflict Resolution:</span>
              <span className="ml-2 font-medium text-gray-900 dark:text-white capitalize">{conflictResolution}</span>
            </div>
            <div>
              <span className="text-gray-600 dark:text-gray-400">Connected Platforms:</span>
              <span className="ml-2 font-medium text-gray-900 dark:text-white">
                {platforms.filter(p => p.enabled && p.connected).length} of {platforms.filter(p => p.enabled).length}
              </span>
            </div>
          </div>
        </div>

        {/* Pre-launch Checklist */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700">
          <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <CheckCircle className="w-5 h-5 mr-2" />
            Pre-launch Checklist
          </h4>
          <div className="space-y-3">
            {[
              { item: 'Business profile completed', status: businessProfile.name && businessProfile.category },
              { item: 'At least one platform selected', status: platforms.some(p => p.enabled) },
              { item: 'Platform authentication completed', status: platforms.some(p => p.enabled && p.connected) },
              { item: 'Sync strategy configured', status: syncFrequency && conflictResolution },
              { item: 'Business hours configured', status: Object.values(businessProfile.hours).some(h => !h.closed) }
            ].map((check, index) => (
              <div key={index} className="flex items-center">
                {check.status ? (
                  <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                ) : (
                  <AlertCircle className="w-5 h-5 text-yellow-500 mr-3" />
                )}
                <span className={`text-sm ${check.status ? 'text-gray-900 dark:text-white' : 'text-gray-600 dark:text-gray-400'}`}>
                  {check.item}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Launch Button */}
        <div className="text-center">
          <button
            onClick={launchDirectorySetup}
            disabled={isLoading || !platforms.some(p => p.enabled && p.connected)}
            className="bg-green-600 text-white px-8 py-4 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center mx-auto text-lg font-semibold"
          >
            {isLoading ? (
              <Loader2 className="w-6 h-6 mr-3 animate-spin" />
            ) : (
              <Zap className="w-6 h-6 mr-3" />
            )}
            Launch Multi-Platform Directory Setup
          </button>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-3">
            This will begin synchronizing your business information across all connected platforms.
          </p>
        </div>
      </div>
    </div>
  );

  // Main render function
  const renderStepContent = () => {
    switch (currentStep) {
      case 0: return renderBusinessProfileStep();
      case 1: return renderPlatformSelectionStep();
      case 2: return renderCredentialsSetupStep();
      case 3: return renderPlatformSelectionStep(); // Platform Configuration (simplified for now)
      case 4: return renderSyncStrategyStep();
      case 5: return renderReviewLaunchStep();
      default: return renderBusinessProfileStep();
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Directory Management Wizard</h2>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Step {currentStep + 1} of {wizardSteps.length}
          </div>
        </div>
        
        <div className="flex items-center space-x-4 mb-6">
          {wizardSteps.map((step, index) => (
            <div key={step.id} className="flex items-center">
              <button
                onClick={() => goToStep(index)}
                className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all ${
                  index < currentStep || step.completed
                    ? 'bg-green-500 border-green-500 text-white'
                    : index === currentStep
                    ? 'bg-blue-500 border-blue-500 text-white'
                    : 'bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400'
                }`}
              >
                {index < currentStep || step.completed ? (
                  <CheckCircle className="w-5 h-5" />
                ) : (
                  <span className="text-sm font-medium">{index + 1}</span>
                )}
              </button>
              {index < wizardSteps.length - 1 && (
                <div className={`w-16 h-0.5 ${
                  index < currentStep ? 'bg-green-500' : 'bg-gray-300 dark:bg-gray-600'
                }`} />
              )}
            </div>
          ))}
        </div>

        <div className="flex items-center space-x-4">
          <div className="text-lg font-semibold text-gray-900 dark:text-white">
            {wizardSteps[currentStep].title}
          </div>
          {wizardSteps[currentStep].optional && (
            <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 text-xs rounded-full">
              Optional
            </span>
          )}
        </div>
        <p className="text-gray-600 dark:text-gray-400 mt-1">
          {wizardSteps[currentStep].description}
        </p>
      </div>

      {/* Step Content */}
      <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 p-8">
        {renderStepContent()}
      </div>

      {/* Navigation */}
      <div className="flex items-center justify-between mt-8">
        <button
          onClick={goToPreviousStep}
          disabled={currentStep === 0}
          className="flex items-center px-6 py-3 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Previous
        </button>

        <div className="text-sm text-gray-600 dark:text-gray-400">
          {currentStep + 1} of {wizardSteps.length} steps completed
        </div>

        <button
          onClick={goToNextStep}
          disabled={currentStep === wizardSteps.length - 1}
          className="flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
          <ArrowRight className="w-4 h-4 ml-2" />
        </button>
      </div>
    </div>
  );
}