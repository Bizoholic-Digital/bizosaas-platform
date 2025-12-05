import { NextRequest, NextResponse } from 'next/server';

interface ConnectionResult {
  success: boolean;
  platformId: string;
  status: 'connected' | 'in_progress' | 'error';
  credentials?: any;
  error?: string;
  steps?: Array<{
    id: string;
    completed: boolean;
    data?: any;
  }>;
}

// Mock OAuth URLs and connection logic
const PLATFORM_CONFIG = {
  'google-business': {
    oauthUrl: 'https://accounts.google.com/oauth/authorize',
    scopes: ['business.manage', 'reviews.read'],
    requiresVerification: true
  },
  'yelp': {
    oauthUrl: 'https://api.yelp.com/oauth2/authorize',
    scopes: ['business.read', 'business.write'],
    requiresVerification: true
  },
  'facebook': {
    oauthUrl: 'https://www.facebook.com/dialog/oauth',
    scopes: ['pages_manage_business', 'pages_read_engagement'],
    requiresVerification: false
  },
  'apple-maps': {
    manualSetup: true,
    requiresVerification: true,
    verificationMethods: ['phone', 'postcard', 'email']
  },
  'bing-places': {
    oauthUrl: 'https://login.microsoftonline.com/oauth2/authorize',
    scopes: ['business.read', 'business.write'],
    requiresVerification: true
  }
};

// Simulate OAuth flow and connection process
async function connectToPlatform(platformId: string, businessProfile: any): Promise<ConnectionResult> {
  const config = PLATFORM_CONFIG[platformId as keyof typeof PLATFORM_CONFIG];
  
  if (!config) {
    return {
      success: false,
      platformId,
      status: 'error',
      error: 'Platform not supported'
    };
  }
  
  // Simulate connection process delay
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  try {
    // For demonstration, we'll simulate different connection scenarios
    const connectionScenarios = [
      { success: true, immediate: true },
      { success: true, immediate: false }, // Requires verification
      { success: false, error: 'Authentication failed' }
    ];
    
    // Randomly select scenario for demo (in real app, this would be actual OAuth flow)
    const scenario = connectionScenarios[Math.floor(Math.random() * connectionScenarios.length)];
    
    if (!scenario.success) {
      return {
        success: false,
        platformId,
        status: 'error',
        error: scenario.error
      };
    }
    
    // Generate mock credentials and connection data
    const credentials = {
      accessToken: `mock_token_${platformId}_${Date.now()}`,
      refreshToken: `refresh_token_${platformId}_${Date.now()}`,
      expiresAt: Date.now() + (3600 * 1000), // 1 hour
      scopes: 'scopes' in config ? config.scopes : [],
      platformUserId: `user_${platformId}_${Math.random().toString(36).substr(2, 9)}`
    };
    
    // Simulate connection steps completion
    const steps = [];
    
    if (platformId === 'google-business') {
      steps.push(
        { id: 'signin', completed: true, data: { email: businessProfile.contact?.email } },
        { id: 'permissions', completed: true, data: { scopes: 'scopes' in config ? config.scopes : [] } },
        { id: 'business_select', completed: scenario.immediate, data: { businessId: scenario.immediate ? 'business_123' : null } },
        { id: 'verify_ownership', completed: false, data: { verificationMethod: 'phone' } }
      );
    } else if (platformId === 'yelp') {
      steps.push(
        { id: 'yelp_signin', completed: true, data: { userId: credentials.platformUserId } },
        { id: 'claim_business', completed: scenario.immediate, data: { businessId: scenario.immediate ? 'yelp_biz_456' : null } },
        { id: 'api_access', completed: true, data: { scopes: 'scopes' in config ? config.scopes : [] } },
        { id: 'verify_info', completed: scenario.immediate, data: { verified: scenario.immediate } }
      );
    } else if (platformId === 'facebook') {
      steps.push(
        { id: 'fb_signin', completed: true, data: { userId: credentials.platformUserId } },
        { id: 'select_page', completed: true, data: { pageId: 'page_789', pageName: businessProfile.name } },
        { id: 'page_permissions', completed: true, data: { permissions: 'scopes' in config ? config.scopes : [] } },
        { id: 'business_info', completed: scenario.immediate, data: { configured: scenario.immediate } }
      );
    } else if (platformId === 'apple-maps') {
      steps.push(
        { id: 'apple_signin', completed: true, data: { appleId: credentials.platformUserId } },
        { id: 'business_register', completed: true, data: { submissionId: 'apple_sub_101' } },
        { id: 'verification_docs', completed: false, data: { documentsRequired: true } },
        { id: 'review_approval', completed: false, data: { estimatedDays: '3-5' } }
      );
    } else if (platformId === 'bing-places') {
      steps.push(
        { id: 'ms_signin', completed: true, data: { microsoftId: credentials.platformUserId } },
        { id: 'add_business', completed: true, data: { businessId: 'bing_biz_202' } },
        { id: 'verify_business', completed: scenario.immediate, data: { verified: scenario.immediate } }
      );
    }
    
    return {
      success: true,
      platformId,
      status: scenario.immediate ? 'connected' : 'in_progress',
      credentials: scenario.immediate ? credentials : undefined,
      steps
    };
    
  } catch (error) {
    console.error(`Error connecting to ${platformId}:`, error);
    return {
      success: false,
      platformId,
      status: 'error',
      error: 'Connection failed due to technical error'
    };
  }
}

export async function POST(
  request: NextRequest,
  context: { params: Promise<{ platform: string }> }
) {
  try {
    const params = await context.params;
    const platformId = params.platform;
    const body = await request.json();
    const businessProfile = body.businessProfile;
    
    if (!platformId) {
      return NextResponse.json(
        { error: 'Platform ID is required' },
        { status: 400 }
      );
    }
    
    if (!businessProfile) {
      return NextResponse.json(
        { error: 'Business profile is required' },
        { status: 400 }
      );
    }
    
    // Validate business profile has minimum required information
    if (!businessProfile.name || !businessProfile.contact?.email) {
      return NextResponse.json(
        { error: 'Business name and email are required for platform connection' },
        { status: 400 }
      );
    }
    
    const result = await connectToPlatform(platformId, businessProfile);
    
    // Return appropriate status code based on result
    if (!result.success) {
      return NextResponse.json(result, { status: 400 });
    }
    
    return NextResponse.json(result);
    
  } catch (error) {
    console.error('Error in platform connection:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}