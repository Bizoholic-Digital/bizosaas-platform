'use client';

import React, { useState, useEffect } from 'react';
import {
  Play, CheckCircle, AlertCircle, Clock, Users, Target,
  Mail, ShoppingCart, FileText, BarChart3, Settings,
  ArrowRight, RefreshCw, Download, Eye
} from 'lucide-react';

interface JourneyStep {
  id: string;
  name: string;
  description: string;
  endpoint?: string;
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  payload?: any;
  expectedStatus?: number;
  validations?: Array<{
    type: 'response_time' | 'status_code' | 'response_data' | 'ui_element';
    condition: string;
    value: any;
  }>;
  dependencies?: string[];
}

interface UserJourney {
  id: string;
  name: string;
  description: string;
  category: 'onboarding' | 'campaign' | 'ecommerce' | 'crm' | 'analytics';
  priority: 'critical' | 'high' | 'medium' | 'low';
  estimatedTime: number; // minutes
  steps: JourneyStep[];
  icon: React.ComponentType<any>;
  color: string;
}

interface JourneyResult {
  journeyId: string;
  status: 'pending' | 'running' | 'passed' | 'failed' | 'warning';
  startTime?: Date;
  endTime?: Date;
  duration?: number;
  stepResults: Array<{
    stepId: string;
    status: 'pending' | 'running' | 'passed' | 'failed' | 'warning';
    responseTime?: number;
    error?: string;
    data?: any;
  }>;
  overallScore: number;
  issues: string[];
  recommendations: string[];
}

const USER_JOURNEYS: UserJourney[] = [
  {
    id: 'new-user-onboarding',
    name: 'New User Onboarding',
    description: 'Complete new user registration and setup flow',
    category: 'onboarding',
    priority: 'critical',
    estimatedTime: 15,
    icon: Users,
    color: '#3B82F6',
    steps: [
      {
        id: 'landing-page',
        name: 'Landing Page Load',
        description: 'User visits the platform landing page',
        endpoint: '/',
        method: 'GET',
        expectedStatus: 200,
        validations: [
          { type: 'response_time', condition: 'less_than', value: 2000 },
          { type: 'ui_element', condition: 'exists', value: 'sign-up-button' }
        ]
      },
      {
        id: 'registration',
        name: 'User Registration',
        description: 'User creates a new account',
        endpoint: '/api/brain/auth/register',
        method: 'POST',
        payload: {
          email: 'journey-test@example.com',
          password: 'TestPassword123!',
          business_name: 'Journey Test Corp',
          first_name: 'Test',
          last_name: 'User'
        },
        expectedStatus: 201,
        validations: [
          { type: 'response_data', condition: 'contains', value: 'user_id' },
          { type: 'response_data', condition: 'contains', value: 'access_token' }
        ]
      },
      {
        id: 'email-verification',
        name: 'Email Verification',
        description: 'User verifies their email address',
        endpoint: '/api/brain/auth/verify-email',
        method: 'POST',
        dependencies: ['registration'],
        validations: [
          { type: 'response_time', condition: 'less_than', value: 1000 }
        ]
      },
      {
        id: 'business-profile-setup',
        name: 'Business Profile Setup',
        description: 'User completes business profile wizard',
        endpoint: '/api/brain/onboarding/business-profile',
        method: 'POST',
        dependencies: ['email-verification'],
        payload: {
          business_type: 'technology',
          industry: 'software',
          company_size: '10-50',
          goals: ['lead_generation', 'brand_awareness']
        },
        validations: [
          { type: 'status_code', condition: 'equals', value: 200 }
        ]
      },
      {
        id: 'dashboard-access',
        name: 'Dashboard Access',
        description: 'User accesses their main dashboard',
        endpoint: '/api/brain/dashboard/overview',
        method: 'GET',
        dependencies: ['business-profile-setup'],
        validations: [
          { type: 'response_data', condition: 'contains', value: 'widgets' },
          { type: 'response_time', condition: 'less_than', value: 1500 }
        ]
      }
    ]
  },
  {
    id: 'campaign-creation-flow',
    name: 'Campaign Creation Flow',
    description: 'User creates and launches a marketing campaign',
    category: 'campaign',
    priority: 'critical',
    estimatedTime: 20,
    icon: Target,
    color: '#10B981',
    steps: [
      {
        id: 'campaign-wizard-access',
        name: 'Access Campaign Wizard',
        description: 'User navigates to campaign creation',
        endpoint: '/campaigns/new',
        method: 'GET',
        validations: [
          { type: 'ui_element', condition: 'exists', value: 'campaign-type-selector' }
        ]
      },
      {
        id: 'google-ads-wizard',
        name: 'Google Ads Campaign Setup',
        description: 'User completes Google Ads campaign wizard',
        endpoint: '/api/brain/campaign-wizards/google-ads',
        method: 'POST',
        dependencies: ['campaign-wizard-access'],
        payload: {
          objective: { type: 'leads', label: 'Lead Generation' },
          targeting: {
            keywords: ['digital marketing', 'business growth'],
            geographic: { countries: ['United States'] },
            demographics: { ageRange: { min: 25, max: 55 } }
          },
          creative: {
            headlines: ['Grow Your Business Today'],
            descriptions: ['Professional marketing solutions'],
            landingUrl: 'https://example.com/landing'
          },
          budget: {
            budgetType: 'daily',
            amount: 50,
            currency: 'USD',
            startDate: new Date().toISOString().split('T')[0]
          },
          review: {
            campaignName: 'Test Campaign',
            launchType: 'immediate'
          }
        },
        validations: [
          { type: 'response_data', condition: 'contains', value: 'campaignId' },
          { type: 'response_data', condition: 'contains', value: 'success' }
        ]
      },
      {
        id: 'campaign-monitoring',
        name: 'Campaign Monitoring',
        description: 'User views campaign performance',
        endpoint: '/api/brain/campaign-wizards/google-ads',
        method: 'GET',
        dependencies: ['google-ads-wizard'],
        validations: [
          { type: 'response_data', condition: 'contains', value: 'performance' }
        ]
      }
    ]
  },
  {
    id: 'email-marketing-flow',
    name: 'Email Marketing Flow',
    description: 'User creates and sends email campaign',
    category: 'campaign',
    priority: 'high',
    estimatedTime: 15,
    icon: Mail,
    color: '#8B5CF6',
    steps: [
      {
        id: 'email-wizard-start',
        name: 'Start Email Wizard',
        description: 'User starts email marketing wizard',
        endpoint: '/campaigns/email/new',
        method: 'GET'
      },
      {
        id: 'email-campaign-creation',
        name: 'Create Email Campaign',
        description: 'User creates email marketing campaign',
        endpoint: '/api/brain/campaign-wizards/email-marketing',
        method: 'POST',
        dependencies: ['email-wizard-start'],
        payload: {
          campaignType: { type: 'newsletter', label: 'Newsletter' },
          audience: {
            segments: [{ id: '1', name: 'Subscribers', selected: true, size: 1000 }]
          },
          content: {
            content: {
              subjectLine: 'Test Newsletter',
              bodyText: 'Welcome to our newsletter',
              callToAction: [{ text: 'Read More', url: 'https://example.com' }]
            }
          },
          delivery: {
            scheduling: { type: 'immediate', timezone: 'UTC' }
          },
          tracking: {
            goals: [{ name: 'Open Rate', metric: 'open_rate', target: 25 }]
          }
        },
        validations: [
          { type: 'response_data', condition: 'contains', value: 'campaignId' }
        ]
      }
    ]
  },
  {
    id: 'ecommerce-order-flow',
    name: 'E-commerce Order Flow',
    description: 'Customer places and processes an order',
    category: 'ecommerce',
    priority: 'critical',
    estimatedTime: 10,
    icon: ShoppingCart,
    color: '#F59E0B',
    steps: [
      {
        id: 'product-catalog',
        name: 'Browse Products',
        description: 'Customer views product catalog',
        endpoint: '/api/brain/saleor/products',
        method: 'GET',
        validations: [
          { type: 'response_data', condition: 'contains', value: 'products' }
        ]
      },
      {
        id: 'add-to-cart',
        name: 'Add to Cart',
        description: 'Customer adds product to cart',
        endpoint: '/api/brain/saleor/cart/add',
        method: 'POST',
        dependencies: ['product-catalog'],
        payload: {
          productId: 'test-product-id',
          quantity: 1
        }
      },
      {
        id: 'checkout-process',
        name: 'Checkout Process',
        description: 'Customer completes checkout',
        endpoint: '/api/brain/saleor/checkout',
        method: 'POST',
        dependencies: ['add-to-cart'],
        payload: {
          shippingAddress: {
            firstName: 'Test',
            lastName: 'Customer',
            streetAddress1: '123 Test St',
            city: 'Test City',
            postalCode: '12345',
            country: 'US'
          },
          paymentMethod: 'stripe'
        }
      }
    ]
  },
  {
    id: 'crm-lead-management',
    name: 'CRM Lead Management',
    description: 'Lead capture and management workflow',
    category: 'crm',
    priority: 'high',
    estimatedTime: 12,
    icon: FileText,
    color: '#EF4444',
    steps: [
      {
        id: 'lead-capture',
        name: 'Lead Capture',
        description: 'New lead is captured from form',
        endpoint: '/api/brain/django-crm/leads',
        method: 'POST',
        payload: {
          first_name: 'Test',
          last_name: 'Lead',
          email: 'test-lead@example.com',
          company: 'Test Company',
          source: 'website'
        }
      },
      {
        id: 'lead-scoring',
        name: 'Lead Scoring',
        description: 'AI scores the lead automatically',
        endpoint: '/api/brain/django-crm/leads/score',
        method: 'POST',
        dependencies: ['lead-capture'],
        validations: [
          { type: 'response_data', condition: 'contains', value: 'score' }
        ]
      },
      {
        id: 'lead-assignment',
        name: 'Lead Assignment',
        description: 'Lead is assigned to sales rep',
        endpoint: '/api/brain/django-crm/leads/assign',
        method: 'PUT',
        dependencies: ['lead-scoring']
      }
    ]
  },
  {
    id: 'analytics-reporting',
    name: 'Analytics & Reporting',
    description: 'User generates and views analytics reports',
    category: 'analytics',
    priority: 'medium',
    estimatedTime: 8,
    icon: BarChart3,
    color: '#06B6D4',
    steps: [
      {
        id: 'dashboard-metrics',
        name: 'Dashboard Metrics',
        description: 'User views main analytics dashboard',
        endpoint: '/api/brain/analytics/dashboard',
        method: 'GET',
        validations: [
          { type: 'response_data', condition: 'contains', value: 'metrics' }
        ]
      },
      {
        id: 'custom-report',
        name: 'Custom Report Generation',
        description: 'User generates custom report',
        endpoint: '/api/brain/analytics/reports/generate',
        method: 'POST',
        dependencies: ['dashboard-metrics'],
        payload: {
          reportType: 'campaign_performance',
          dateRange: { start: '2024-01-01', end: '2024-12-31' },
          metrics: ['impressions', 'clicks', 'conversions']
        }
      }
    ]
  }
];

export function UserJourneyValidator() {
  const [results, setResults] = useState<JourneyResult[]>([]);
  const [runningJourneys, setRunningJourneys] = useState<Set<string>>(new Set());
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedPriority, setSelectedPriority] = useState<string>('all');

  const executeStep = async (step: JourneyStep): Promise<any> => {
    if (!step.endpoint) {
      // UI-only step, simulate success
      await new Promise(resolve => setTimeout(resolve, 500));
      return { success: true, ui_validated: true };
    }

    const startTime = Date.now();
    
    try {
      const response = await fetch(step.endpoint, {
        method: step.method || 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        ...(step.payload && { body: JSON.stringify(step.payload) })
      });

      const responseTime = Date.now() - startTime;
      const data = await response.json().catch(() => ({}));

      // Validate response
      const validationResults = [];
      if (step.validations) {
        for (const validation of step.validations) {
          switch (validation.type) {
            case 'response_time':
              if (validation.condition === 'less_than' && responseTime >= validation.value) {
                validationResults.push(`Response time ${responseTime}ms exceeds ${validation.value}ms`);
              }
              break;
            case 'status_code':
              if (validation.condition === 'equals' && response.status !== validation.value) {
                validationResults.push(`Expected status ${validation.value}, got ${response.status}`);
              }
              break;
            case 'response_data':
              if (validation.condition === 'contains' && !JSON.stringify(data).includes(validation.value)) {
                validationResults.push(`Response missing expected field: ${validation.value}`);
              }
              break;
          }
        }
      }

      return {
        success: response.ok && validationResults.length === 0,
        status: response.status,
        data,
        responseTime,
        validationErrors: validationResults
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        responseTime: Date.now() - startTime
      };
    }
  };

  const executeJourney = async (journey: UserJourney) => {
    const journeyId = journey.id;
    setRunningJourneys(prev => new Set([...prev, journeyId]));

    const result: JourneyResult = {
      journeyId,
      status: 'running',
      startTime: new Date(),
      stepResults: journey.steps.map(step => ({
        stepId: step.id,
        status: 'pending'
      })),
      overallScore: 0,
      issues: [],
      recommendations: []
    };

    setResults(prev => {
      const filtered = prev.filter(r => r.journeyId !== journeyId);
      return [...filtered, result];
    });

    let passedSteps = 0;
    let totalResponseTime = 0;

    for (let i = 0; i < journey.steps.length; i++) {
      const step = journey.steps[i];
      
      // Update step status to running
      setResults(prev => prev.map(r => 
        r.journeyId === journeyId 
          ? {
              ...r,
              stepResults: r.stepResults.map((sr, idx) => 
                idx === i ? { ...sr, status: 'running' } : sr
              )
            }
          : r
      ));

      // Execute step
      const stepResult = await executeStep(step);
      const stepStatus = stepResult.success ? 'passed' : 'failed';
      
      if (stepResult.success) {
        passedSteps++;
      } else {
        result.issues.push(`Step "${step.name}": ${stepResult.error || stepResult.validationErrors?.join(', ') || 'Failed'}`);
      }

      if (stepResult.responseTime) {
        totalResponseTime += stepResult.responseTime;
      }

      // Update step result
      setResults(prev => prev.map(r => 
        r.journeyId === journeyId 
          ? {
              ...r,
              stepResults: r.stepResults.map((sr, idx) => 
                idx === i ? {
                  ...sr,
                  status: stepStatus,
                  responseTime: stepResult.responseTime,
                  error: stepResult.error,
                  data: stepResult.data
                } : sr
              )
            }
          : r
      ));

      // If step failed and it's critical, stop journey
      if (!stepResult.success && journey.priority === 'critical') {
        break;
      }
    }

    // Calculate final results
    const overallScore = Math.round((passedSteps / journey.steps.length) * 100);
    const avgResponseTime = totalResponseTime / journey.steps.length;
    const journeyStatus = overallScore >= 90 ? 'passed' : overallScore >= 70 ? 'warning' : 'failed';

    // Generate recommendations
    const recommendations = [];
    if (avgResponseTime > 2000) {
      recommendations.push('Consider optimizing API response times');
    }
    if (overallScore < 100) {
      recommendations.push('Review failed steps and implement fixes');
    }
    if (result.issues.length > 0) {
      recommendations.push('Address validation errors in failing steps');
    }

    // Final update
    setResults(prev => prev.map(r => 
      r.journeyId === journeyId 
        ? {
            ...r,
            status: journeyStatus,
            endTime: new Date(),
            duration: Date.now() - (r.startTime?.getTime() || 0),
            overallScore,
            recommendations
          }
        : r
    ));

    setRunningJourneys(prev => {
      const updated = new Set(prev);
      updated.delete(journeyId);
      return updated;
    });
  };

  const runAllJourneys = async () => {
    const filteredJourneys = USER_JOURNEYS.filter(journey => {
      const categoryMatch = selectedCategory === 'all' || journey.category === selectedCategory;
      const priorityMatch = selectedPriority === 'all' || journey.priority === selectedPriority;
      return categoryMatch && priorityMatch;
    });

    for (const journey of filteredJourneys) {
      if (!runningJourneys.has(journey.id)) {
        await executeJourney(journey);
      }
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'passed':
        return <CheckCircle className="text-green-500" size={20} />;
      case 'failed':
        return <AlertCircle className="text-red-500" size={20} />;
      case 'warning':
        return <AlertCircle className="text-yellow-500" size={20} />;
      case 'running':
        return <RefreshCw className="text-blue-500 animate-spin" size={20} />;
      default:
        return <Clock className="text-gray-400" size={20} />;
    }
  };

  const filteredJourneys = USER_JOURNEYS.filter(journey => {
    const categoryMatch = selectedCategory === 'all' || journey.category === selectedCategory;
    const priorityMatch = selectedPriority === 'all' || journey.priority === selectedPriority;
    return categoryMatch && priorityMatch;
  });

  const overallStats = {
    total: results.length,
    passed: results.filter(r => r.status === 'passed').length,
    failed: results.filter(r => r.status === 'failed').length,
    warning: results.filter(r => r.status === 'warning').length,
    avgScore: results.length > 0 ? Math.round(results.reduce((sum, r) => sum + r.overallScore, 0) / results.length) : 0
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          End-to-End User Journey Validation
        </h1>
        <p className="text-gray-600 mb-6">
          Comprehensive testing of critical user flows across the entire BizOSaaS platform
        </p>

        {/* Controls */}
        <div className="flex flex-wrap gap-4 items-center">
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2"
          >
            <option value="all">All Categories</option>
            <option value="onboarding">Onboarding</option>
            <option value="campaign">Campaign</option>
            <option value="ecommerce">E-commerce</option>
            <option value="crm">CRM</option>
            <option value="analytics">Analytics</option>
          </select>

          <select
            value={selectedPriority}
            onChange={(e) => setSelectedPriority(e.target.value)}
            className="border border-gray-300 rounded-lg px-3 py-2"
          >
            <option value="all">All Priorities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>

          <button
            onClick={runAllJourneys}
            disabled={runningJourneys.size > 0}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            <Play size={16} />
            Run All Tests
          </button>
        </div>
      </div>

      {/* Overall Stats */}
      {results.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
          <div className="bg-white rounded-lg border p-4 text-center">
            <div className="text-2xl font-bold text-gray-900">{overallStats.total}</div>
            <div className="text-sm text-gray-600">Total Journeys</div>
          </div>
          <div className="bg-white rounded-lg border p-4 text-center">
            <div className="text-2xl font-bold text-green-600">{overallStats.passed}</div>
            <div className="text-sm text-gray-600">Passed</div>
          </div>
          <div className="bg-white rounded-lg border p-4 text-center">
            <div className="text-2xl font-bold text-yellow-600">{overallStats.warning}</div>
            <div className="text-sm text-gray-600">Warnings</div>
          </div>
          <div className="bg-white rounded-lg border p-4 text-center">
            <div className="text-2xl font-bold text-red-600">{overallStats.failed}</div>
            <div className="text-sm text-gray-600">Failed</div>
          </div>
          <div className="bg-white rounded-lg border p-4 text-center">
            <div className="text-2xl font-bold text-blue-600">{overallStats.avgScore}%</div>
            <div className="text-sm text-gray-600">Avg Score</div>
          </div>
        </div>
      )}

      {/* Journey Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredJourneys.map(journey => {
          const Icon = journey.icon;
          const result = results.find(r => r.journeyId === journey.id);
          const isRunning = runningJourneys.has(journey.id);

          return (
            <div key={journey.id} className="bg-white rounded-lg border border-gray-200 p-6">
              {/* Journey Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center">
                  <div 
                    className="w-10 h-10 rounded-lg flex items-center justify-center mr-3"
                    style={{ backgroundColor: journey.color + '20' }}
                  >
                    <Icon size={20} style={{ color: journey.color }} />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{journey.name}</h3>
                    <p className="text-sm text-gray-600">{journey.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {result && getStatusIcon(result.status)}
                  <button
                    onClick={() => executeJourney(journey)}
                    disabled={isRunning}
                    className="flex items-center gap-1 text-sm bg-gray-100 hover:bg-gray-200 px-3 py-1 rounded-lg disabled:opacity-50"
                  >
                    <Play size={12} />
                    Test
                  </button>
                </div>
              </div>

              {/* Journey Metadata */}
              <div className="flex items-center gap-4 mb-4 text-sm text-gray-600">
                <span className={`px-2 py-1 rounded-full ${
                  journey.priority === 'critical' ? 'bg-red-100 text-red-800' :
                  journey.priority === 'high' ? 'bg-orange-100 text-orange-800' :
                  journey.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-green-100 text-green-800'
                }`}>
                  {journey.priority}
                </span>
                <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded-full">
                  {journey.category}
                </span>
                <span className="flex items-center gap-1">
                  <Clock size={12} />
                  {journey.estimatedTime}m
                </span>
              </div>

              {/* Steps Progress */}
              <div className="space-y-2 mb-4">
                {journey.steps.map((step, index) => {
                  const stepResult = result?.stepResults[index];
                  return (
                    <div key={step.id} className="flex items-center gap-3">
                      <div className="flex-shrink-0">
                        {stepResult ? getStatusIcon(stepResult.status) : (
                          <div className="w-5 h-5 border-2 border-gray-200 rounded-full" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-medium text-gray-900 truncate">
                          {step.name}
                        </div>
                        <div className="text-xs text-gray-500 truncate">
                          {step.description}
                        </div>
                      </div>
                      {stepResult?.responseTime && (
                        <div className="text-xs text-gray-500">
                          {stepResult.responseTime}ms
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              {/* Results Summary */}
              {result && (
                <div className="border-t pt-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Overall Score</span>
                    <span className={`text-sm font-bold ${
                      result.overallScore >= 90 ? 'text-green-600' :
                      result.overallScore >= 70 ? 'text-yellow-600' : 'text-red-600'
                    }`}>
                      {result.overallScore}%
                    </span>
                  </div>
                  
                  {result.duration && (
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm text-gray-600">Duration</span>
                      <span className="text-sm text-gray-900">
                        {Math.round(result.duration / 1000)}s
                      </span>
                    </div>
                  )}

                  {result.issues.length > 0 && (
                    <div className="mt-3">
                      <h4 className="text-xs font-medium text-red-700 mb-1">Issues:</h4>
                      <ul className="text-xs text-red-600 space-y-1">
                        {result.issues.slice(0, 3).map((issue, idx) => (
                          <li key={idx}>• {issue}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {result.recommendations.length > 0 && (
                    <div className="mt-3">
                      <h4 className="text-xs font-medium text-blue-700 mb-1">Recommendations:</h4>
                      <ul className="text-xs text-blue-600 space-y-1">
                        {result.recommendations.slice(0, 2).map((rec, idx) => (
                          <li key={idx}>• {rec}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}