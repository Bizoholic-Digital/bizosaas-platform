'use client';

import React, { useState } from 'react';
import {
  Key, Shield, CheckCircle, AlertCircle, Chrome, Facebook,
  Apple, Search, Star, Loader2, ExternalLink, Lock,
  Eye, EyeOff, Copy, RefreshCw, Info, AlertTriangle,
  FileText, Video, HelpCircle, Zap
} from 'lucide-react';

interface PlatformCredentials {
  id: string;
  name: string;
  icon: React.ComponentType;
  connected: boolean;
  authType: 'oauth' | 'api_key' | 'manual';
  status: 'not_started' | 'in_progress' | 'connected' | 'error';
  credentials?: any;
  lastConnected?: string;
  error?: string;
  requirements: string[];
  steps: ConnectionStep[];
  securityLevel: 'high' | 'medium' | 'basic';
  dataAccess: string[];
}

interface ConnectionStep {
  id: string;
  title: string;
  description: string;
  type: 'action' | 'input' | 'verification';
  completed: boolean;
  optional: boolean;
  helpUrl?: string;
  videoUrl?: string;
}

interface CredentialsSetupProps {
  platforms: PlatformCredentials[];
  onConnect: (platformId: string) => Promise<void>;
  onDisconnect: (platformId: string) => Promise<void>;
  isConnecting: boolean;
  businessProfile: any;
}

const PLATFORM_CREDENTIALS: PlatformCredentials[] = [
  {
    id: 'google-business',
    name: 'Google Business Profile',
    icon: Chrome,
    connected: false,
    authType: 'oauth',
    status: 'not_started',
    requirements: [
      'Google account with business email',
      'Business verification documents',
      'Physical business address',
      'Phone number verification'
    ],
    steps: [
      {
        id: 'signin',
        title: 'Sign in to Google',
        description: 'Authenticate with your Google account',
        type: 'action',
        completed: false,
        optional: false
      },
      {
        id: 'permissions',
        title: 'Grant Permissions',
        description: 'Allow access to Google Business Profile',
        type: 'verification',
        completed: false,
        optional: false
      },
      {
        id: 'business_select',
        title: 'Select Business',
        description: 'Choose or create your business listing',
        type: 'input',
        completed: false,
        optional: false
      },
      {
        id: 'verify_ownership',
        title: 'Verify Ownership',
        description: 'Complete business verification process',
        type: 'verification',
        completed: false,
        optional: false,
        helpUrl: 'https://support.google.com/business/answer/2911778'
      }
    ],
    securityLevel: 'high',
    dataAccess: ['Business information', 'Customer reviews', 'Analytics data', 'Photos and posts']
  },
  {
    id: 'yelp',
    name: 'Yelp Business',
    icon: Star,
    connected: false,
    authType: 'oauth',
    status: 'not_started',
    requirements: [
      'Yelp business account',
      'Claimed business listing',
      'Business verification',
      'Valid business information'
    ],
    steps: [
      {
        id: 'yelp_signin',
        title: 'Sign in to Yelp',
        description: 'Authenticate with your Yelp business account',
        type: 'action',
        completed: false,
        optional: false
      },
      {
        id: 'claim_business',
        title: 'Claim Business',
        description: 'Claim your business listing on Yelp',
        type: 'verification',
        completed: false,
        optional: false,
        helpUrl: 'https://biz.yelp.com/support/claiming_a_business_page'
      },
      {
        id: 'api_access',
        title: 'API Access',
        description: 'Grant API access permissions',
        type: 'verification',
        completed: false,
        optional: false
      },
      {
        id: 'verify_info',
        title: 'Verify Information',
        description: 'Confirm business details are accurate',
        type: 'input',
        completed: false,
        optional: false
      }
    ],
    securityLevel: 'medium',
    dataAccess: ['Business profile', 'Customer reviews', 'Photos', 'Basic analytics']
  },
  {
    id: 'facebook',
    name: 'Facebook Business',
    icon: Facebook,
    connected: false,
    authType: 'oauth',
    status: 'not_started',
    requirements: [
      'Facebook personal account',
      'Facebook business page',
      'Page admin permissions',
      'Business verification (optional)'
    ],
    steps: [
      {
        id: 'fb_signin',
        title: 'Sign in to Facebook',
        description: 'Authenticate with your Facebook account',
        type: 'action',
        completed: false,
        optional: false
      },
      {
        id: 'select_page',
        title: 'Select Business Page',
        description: 'Choose your business page or create new',
        type: 'input',
        completed: false,
        optional: false
      },
      {
        id: 'page_permissions',
        title: 'Page Permissions',
        description: 'Grant page management permissions',
        type: 'verification',
        completed: false,
        optional: false
      },
      {
        id: 'business_info',
        title: 'Configure Business Info',
        description: 'Set up business information and settings',
        type: 'input',
        completed: false,
        optional: true,
        helpUrl: 'https://www.facebook.com/business/help'
      }
    ],
    securityLevel: 'medium',
    dataAccess: ['Page information', 'Posts and updates', 'Page insights', 'Customer messages']
  },
  {
    id: 'apple-maps',
    name: 'Apple Maps Business',
    icon: Apple,
    connected: false,
    authType: 'manual',
    status: 'not_started',
    requirements: [
      'Apple ID',
      'Apple Developer account (recommended)',
      'Business verification documents',
      'High-quality business photos'
    ],
    steps: [
      {
        id: 'apple_signin',
        title: 'Sign in with Apple ID',
        description: 'Authenticate with your Apple ID',
        type: 'action',
        completed: false,
        optional: false
      },
      {
        id: 'business_register',
        title: 'Register Business',
        description: 'Submit business information to Apple',
        type: 'input',
        completed: false,
        optional: false,
        helpUrl: 'https://mapsconnect.apple.com'
      },
      {
        id: 'verification_docs',
        title: 'Upload Verification',
        description: 'Provide business verification documents',
        type: 'verification',
        completed: false,
        optional: false
      },
      {
        id: 'review_approval',
        title: 'Apple Review',
        description: 'Wait for Apple to review and approve',
        type: 'verification',
        completed: false,
        optional: false
      }
    ],
    securityLevel: 'high',
    dataAccess: ['Business location', 'Contact information', 'Photos', 'Basic business details']
  },
  {
    id: 'bing-places',
    name: 'Bing Places for Business',
    icon: Search,
    connected: false,
    authType: 'oauth',
    status: 'not_started',
    requirements: [
      'Microsoft account',
      'Business verification',
      'Accurate business data',
      'Business ownership proof'
    ],
    steps: [
      {
        id: 'ms_signin',
        title: 'Sign in to Microsoft',
        description: 'Authenticate with your Microsoft account',
        type: 'action',
        completed: false,
        optional: false
      },
      {
        id: 'add_business',
        title: 'Add Business',
        description: 'Add your business to Bing Places',
        type: 'input',
        completed: false,
        optional: false
      },
      {
        id: 'verify_business',
        title: 'Verify Business',
        description: 'Complete business verification process',
        type: 'verification',
        completed: false,
        optional: false,
        helpUrl: 'https://www.bingplaces.com/help'
      }
    ],
    securityLevel: 'basic',
    dataAccess: ['Business listing', 'Contact information', 'Photos', 'Customer reviews']
  }
];

export function CredentialsSetup({
  platforms,
  onConnect,
  onDisconnect,
  isConnecting,
  businessProfile
}: CredentialsSetupProps) {
  const [showCredentials, setShowCredentials] = useState<string | null>(null);
  const [activeStep, setActiveStep] = useState<{[key: string]: string}>({});

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected': return 'text-green-600 bg-green-100 dark:bg-green-900/30 dark:text-green-400';
      case 'in_progress': return 'text-blue-600 bg-blue-100 dark:bg-blue-900/30 dark:text-blue-400';
      case 'error': return 'text-red-600 bg-red-100 dark:bg-red-900/30 dark:text-red-400';
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-700 dark:text-gray-400';
    }
  };

  const getSecurityColor = (level: string) => {
    switch (level) {
      case 'high': return 'text-red-600 bg-red-100 dark:bg-red-900/30 dark:text-red-400';
      case 'medium': return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30 dark:text-yellow-400';
      case 'basic': return 'text-green-600 bg-green-100 dark:bg-green-900/30 dark:text-green-400';
      default: return 'text-gray-600 bg-gray-100 dark:bg-gray-700 dark:text-gray-400';
    }
  };

  const getStepIcon = (step: ConnectionStep) => {
    if (step.completed) return <CheckCircle className="w-4 h-4 text-green-500" />;
    if (step.type === 'action') return <Zap className="w-4 h-4 text-blue-500" />;
    if (step.type === 'input') return <FileText className="w-4 h-4 text-purple-500" />;
    if (step.type === 'verification') return <Shield className="w-4 h-4 text-orange-500" />;
    return <AlertCircle className="w-4 h-4 text-gray-500" />;
  };

  const getOverallProgress = () => {
    const enabledPlatforms = platforms.filter(p => p.connected || p.status !== 'not_started');
    const connectedPlatforms = platforms.filter(p => p.connected);
    return {
      total: enabledPlatforms.length,
      connected: connectedPlatforms.length,
      percentage: enabledPlatforms.length > 0 ? Math.round((connectedPlatforms.length / enabledPlatforms.length) * 100) : 0
    };
  };

  const startConnection = async (platformId: string) => {
    try {
      await onConnect(platformId);
    } catch (error) {
      console.error(`Failed to connect to ${platformId}:`, error);
    }
  };

  const disconnectPlatform = async (platformId: string) => {
    try {
      await onDisconnect(platformId);
    } catch (error) {
      console.error(`Failed to disconnect from ${platformId}:`, error);
    }
  };

  const renderConnectionSteps = (platform: PlatformCredentials) => (
    <div className="mt-4 space-y-3">
      <h5 className="font-medium text-gray-900 dark:text-white">Connection Steps:</h5>
      {platform.steps.map((step, index) => (
        <div
          key={step.id}
          className={`flex items-start p-3 rounded-lg border ${
            step.completed ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800' :
            activeStep[platform.id] === step.id ? 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800' :
            'bg-gray-50 dark:bg-gray-800 border-gray-200 dark:border-gray-700'
          }`}
        >
          <div className="flex items-center mr-3">
            <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium ${
              step.completed ? 'bg-green-500 text-white' :
              activeStep[platform.id] === step.id ? 'bg-blue-500 text-white' :
              'bg-gray-300 dark:bg-gray-600 text-gray-600 dark:text-gray-400'
            }`}>
              {step.completed ? '✓' : index + 1}
            </div>
          </div>
          <div className="flex-1">
            <div className="flex items-center justify-between mb-1">
              <h6 className="font-medium text-gray-900 dark:text-white">{step.title}</h6>
              <div className="flex items-center space-x-2">
                {step.optional && (
                  <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 text-xs rounded-full">
                    Optional
                  </span>
                )}
                {step.helpUrl && (
                  <a
                    href={step.helpUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-700 dark:text-blue-400"
                  >
                    <HelpCircle className="w-4 h-4" />
                  </a>
                )}
                {step.videoUrl && (
                  <a
                    href={step.videoUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-purple-600 hover:text-purple-700 dark:text-purple-400"
                  >
                    <Video className="w-4 h-4" />
                  </a>
                )}
              </div>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">{step.description}</p>
            
            {!step.completed && !step.optional && (
              <div className="mt-2">
                {step.type === 'action' && (
                  <button
                    onClick={() => startConnection(platform.id)}
                    disabled={isConnecting}
                    className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 disabled:opacity-50 flex items-center"
                  >
                    {isConnecting ? (
                      <Loader2 className="w-3 h-3 mr-1 animate-spin" />
                    ) : (
                      <ExternalLink className="w-3 h-3 mr-1" />
                    )}
                    Start
                  </button>
                )}
                {step.type === 'input' && (
                  <div className="mt-2 p-2 bg-blue-50 dark:bg-blue-900/20 rounded text-sm text-blue-800 dark:text-blue-400">
                    <Info className="w-4 h-4 inline mr-1" />
                    Complete the previous step to unlock this step
                  </div>
                )}
                {step.type === 'verification' && (
                  <div className="mt-2 p-2 bg-orange-50 dark:bg-orange-900/20 rounded text-sm text-orange-800 dark:text-orange-400">
                    <AlertTriangle className="w-4 h-4 inline mr-1" />
                    Verification required - this may take 1-3 business days
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );

  const renderSecurityInfo = (platform: PlatformCredentials) => (
    <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
      <div className="flex items-center justify-between mb-3">
        <h5 className="font-medium text-gray-900 dark:text-white flex items-center">
          <Lock className="w-4 h-4 mr-2" />
          Security & Privacy
        </h5>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSecurityColor(platform.securityLevel)}`}>
          {platform.securityLevel.toUpperCase()} Security
        </span>
      </div>
      
      <div className="space-y-3">
        <div>
          <h6 className="text-sm font-medium text-gray-900 dark:text-white mb-1">Data Access:</h6>
          <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
            {platform.dataAccess.map((access, index) => (
              <li key={index} className="flex items-center">
                <Shield className="w-3 h-3 text-blue-500 mr-2" />
                {access}
              </li>
            ))}
          </ul>
        </div>
        
        <div>
          <h6 className="text-sm font-medium text-gray-900 dark:text-white mb-1">Security Features:</h6>
          <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
            <li className="flex items-center">
              <CheckCircle className="w-3 h-3 text-green-500 mr-2" />
              {platform.authType === 'oauth' ? 'OAuth 2.0 Authentication' : 'Secure API Key Management'}
            </li>
            <li className="flex items-center">
              <CheckCircle className="w-3 h-3 text-green-500 mr-2" />
              Encrypted credential storage
            </li>
            <li className="flex items-center">
              <CheckCircle className="w-3 h-3 text-green-500 mr-2" />
              Revocable access permissions
            </li>
            <li className="flex items-center">
              <CheckCircle className="w-3 h-3 text-green-500 mr-2" />
              Regular security audits
            </li>
          </ul>
        </div>
      </div>
    </div>
  );

  const progress = getOverallProgress();

  return (
    <div className="space-y-6">
      {/* Progress Overview */}
      <div className="bg-gradient-to-r from-blue-50 to-green-50 dark:from-blue-900/20 dark:to-green-900/20 p-6 rounded-lg border border-blue-200 dark:border-blue-800">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Connection Progress</h3>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            {progress.connected} of {progress.total} platforms connected
          </div>
        </div>
        
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 mb-4">
          <div 
            className="bg-gradient-to-r from-blue-500 to-green-500 h-3 rounded-full transition-all duration-300"
            style={{ width: `${progress.percentage}%` }}
          ></div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{progress.connected}</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Connected</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
              {progress.total - progress.connected}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Pending</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600 dark:text-green-400">{progress.percentage}%</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Complete</div>
          </div>
        </div>
      </div>

      {/* Platform Connections */}
      <div className="space-y-4">
        {platforms.map(platform => {
          const Icon = platform.icon;
          return (
            <div
              key={platform.id}
              className="bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700"
            >
              {/* Platform Header */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center">
                  <div className="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center mr-4">
                    <Icon className="w-8 h-8 text-gray-600 dark:text-gray-400" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-gray-900 dark:text-white">{platform.name}</h4>
                    <div className="flex items-center space-x-3 mt-1">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(platform.status)}`}>
                        {platform.status.replace('_', ' ').toUpperCase()}
                      </span>
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        {platform.authType === 'oauth' ? 'OAuth 2.0' : 
                         platform.authType === 'api_key' ? 'API Key' : 'Manual Setup'}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  {platform.connected ? (
                    <>
                      <div className="flex items-center text-green-600 dark:text-green-400">
                        <CheckCircle className="w-5 h-5 mr-2" />
                        <span className="text-sm font-medium">Connected</span>
                      </div>
                      <button
                        onClick={() => disconnectPlatform(platform.id)}
                        className="text-red-600 hover:text-red-700 dark:text-red-400 text-sm font-medium"
                      >
                        Disconnect
                      </button>
                    </>
                  ) : (
                    <button
                      onClick={() => startConnection(platform.id)}
                      disabled={isConnecting}
                      className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center"
                    >
                      {isConnecting ? (
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      ) : (
                        <Shield className="w-4 h-4 mr-2" />
                      )}
                      Connect
                    </button>
                  )}
                </div>
              </div>

              {/* Connection Status */}
              {platform.connected && platform.lastConnected && (
                <div className="mb-4 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-green-800 dark:text-green-400">
                      Last synchronized: {new Date(platform.lastConnected).toLocaleDateString()}
                    </span>
                    <button
                      onClick={() => startConnection(platform.id)}
                      className="text-green-600 hover:text-green-700 dark:text-green-400 flex items-center text-sm"
                    >
                      <RefreshCw className="w-3 h-3 mr-1" />
                      Refresh
                    </button>
                  </div>
                </div>
              )}

              {/* Error State */}
              {platform.status === 'error' && platform.error && (
                <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
                  <div className="flex items-start">
                    <AlertTriangle className="w-5 h-5 text-red-500 mr-3 mt-0.5" />
                    <div>
                      <h5 className="font-medium text-red-900 dark:text-red-300">Connection Error</h5>
                      <p className="text-sm text-red-800 dark:text-red-400 mt-1">{platform.error}</p>
                      <button
                        onClick={() => startConnection(platform.id)}
                        className="mt-2 bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700"
                      >
                        Retry Connection
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* Requirements */}
              <div className="mb-4">
                <h5 className="font-medium text-gray-900 dark:text-white mb-2">Requirements:</h5>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {platform.requirements.map((req, index) => (
                    <div key={index} className="flex items-center text-sm">
                      <AlertTriangle className="w-3 h-3 text-yellow-500 mr-2 flex-shrink-0" />
                      <span className="text-gray-600 dark:text-gray-400">{req}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Connection Steps */}
              {!platform.connected && renderConnectionSteps(platform)}

              {/* Security Information */}
              <div className="mt-4">
                <button
                  onClick={() => setShowCredentials(showCredentials === platform.id ? null : platform.id)}
                  className="flex items-center text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400"
                >
                  <Lock className="w-4 h-4 mr-1" />
                  {showCredentials === platform.id ? 'Hide' : 'View'} Security Details
                </button>
                {showCredentials === platform.id && renderSecurityInfo(platform)}
              </div>
            </div>
          );
        })}
      </div>

      {/* Security Notice */}
      <div className="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg border border-blue-200 dark:border-blue-800">
        <div className="flex items-start">
          <Shield className="w-6 h-6 text-blue-600 dark:text-blue-400 mr-3 mt-0.5" />
          <div>
            <h4 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">Security & Privacy Commitment</h4>
            <div className="text-sm text-blue-800 dark:text-blue-400 space-y-2">
              <p>
                Your credentials are secured using industry-standard encryption and stored in our SOC 2 compliant infrastructure.
              </p>
              <ul className="list-disc list-inside space-y-1 ml-4">
                <li>All connections use OAuth 2.0 or encrypted API keys</li>
                <li>Credentials are never stored in plain text</li>
                <li>You can revoke access at any time</li>
                <li>Regular security audits and monitoring</li>
                <li>Compliance with GDPR and CCPA requirements</li>
              </ul>
              <div className="mt-3 pt-3 border-t border-blue-200 dark:border-blue-700">
                <a
                  href="/privacy-policy"
                  target="_blank"
                  className="text-blue-600 hover:text-blue-700 dark:text-blue-400 text-sm font-medium"
                >
                  Read our Privacy Policy →
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Help Section */}
      <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg">
        <h4 className="font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <HelpCircle className="w-5 h-5 mr-2" />
          Need Help?
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center">
            <Video className="w-8 h-8 text-purple-500 mx-auto mb-2" />
            <h5 className="font-medium text-gray-900 dark:text-white mb-1">Video Tutorials</h5>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
              Step-by-step video guides for each platform
            </p>
            <button className="text-purple-600 hover:text-purple-700 dark:text-purple-400 text-sm font-medium">
              Watch Videos
            </button>
          </div>
          
          <div className="text-center">
            <FileText className="w-8 h-8 text-blue-500 mx-auto mb-2" />
            <h5 className="font-medium text-gray-900 dark:text-white mb-1">Documentation</h5>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
              Detailed setup guides and troubleshooting
            </p>
            <button className="text-blue-600 hover:text-blue-700 dark:text-blue-400 text-sm font-medium">
              View Docs
            </button>
          </div>
          
          <div className="text-center">
            <Shield className="w-8 h-8 text-green-500 mx-auto mb-2" />
            <h5 className="font-medium text-gray-900 dark:text-white mb-1">Live Support</h5>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
              Get help from our support team
            </p>
            <button className="text-green-600 hover:text-green-700 dark:text-green-400 text-sm font-medium">
              Contact Support
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}