import { NextRequest, NextResponse } from 'next/server';

interface SocialMediaCampaignRequest {
  objective: {
    type: string;
    label: string;
    description: string;
    platforms: string[];
  };
  audience: {
    segments: Array<{
      id: string;
      name: string;
      selected: boolean;
      size: number;
    }>;
    interests: string[];
    geographic: {
      countries: string[];
    };
    demographics: {
      ageRange: { min: number; max: number };
      genders: string[];
    };
  };
  creative: {
    platforms: string[];
    postTypes: string[];
    content: {
      primaryText: string;
      headlines: string[];
      hashtags: string[];
      callToAction: Array<{
        text: string;
        url: string;
        style: string;
      }>;
    };
  };
  budget: {
    totalBudget: number;
    currency: string;
    budgetType: string;
    bidStrategy: string;
    optimization: string;
    duration: {
      startDate: string;
      endDate?: string;
    };
  };
  analytics: {
    objectives: Array<{
      name: string;
      type: string;
      target: number;
      priority: string;
    }>;
    tracking: {
      utmParameters: {
        source: string;
        medium: string;
        campaign: string;
        content?: string;
      };
      pixelIds: { [platform: string]: string };
    };
  };
}

interface SocialMediaCampaignResponse {
  success: boolean;
  campaignId?: string;
  platformCampaigns?: Array<{
    platform: string;
    campaignId: string;
    status: 'active' | 'pending' | 'error';
    message: string;
  }>;
  estimates: {
    totalReach: number;
    totalEngagements: number;
    totalClicks: number;
    estimatedCost: number;
    platformBreakdown: { [platform: string]: any };
  };
  tracking: {
    trackingUrls: string[];
    utmTags: string;
    pixelSetup: { [platform: string]: boolean };
  };
  recommendations: string[];
  errors?: string[];
}

// Platform-specific configurations
const PLATFORM_CONFIGS = {
  facebook: {
    name: 'Facebook',
    maxReach: 2000000000,
    avgCPC: 0.97,
    avgCTR: 0.9,
    avgEngagementRate: 0.063
  },
  instagram: {
    name: 'Instagram', 
    maxReach: 1400000000,
    avgCPC: 1.20,
    avgCTR: 0.68,
    avgEngagementRate: 1.22
  },
  twitter: {
    name: 'Twitter',
    maxReach: 450000000,
    avgCPC: 0.53,
    avgCTR: 1.23,
    avgEngagementRate: 0.045
  },
  linkedin: {
    name: 'LinkedIn',
    maxReach: 900000000,
    avgCPC: 2.74,
    avgCTR: 0.65,
    avgEngagementRate: 0.54
  },
  youtube: {
    name: 'YouTube',
    maxReach: 2700000000,
    avgCPC: 1.85,
    avgCTR: 0.84,
    avgEngagementRate: 0.68
  }
};

// Mock social media API integration
async function createSocialMediaCampaign(campaignData: SocialMediaCampaignRequest): Promise<SocialMediaCampaignResponse> {
  // Simulate API processing delay
  await new Promise(resolve => setTimeout(resolve, 3000));

  const campaignId = `social_${Date.now()}_${Math.random().toString(36).substr(2, 8)}`;
  const platformCampaigns = [];
  const platformBreakdown: { [platform: string]: any } = {};

  let totalReach = 0;
  let totalClicks = 0;
  let totalEngagements = 0;
  let estimatedCost = 0;

  // Calculate estimates for each platform
  for (const platformId of campaignData.creative.platforms) {
    const config = PLATFORM_CONFIGS[platformId as keyof typeof PLATFORM_CONFIGS];
    if (!config) continue;

    // Calculate platform-specific reach
    const audienceSize = campaignData.audience.segments
      .filter(s => s.selected)
      .reduce((sum, s) => sum + s.size, 0);
    
    const platformReach = Math.min(
      audienceSize * 0.7, // Assume 70% of audience is on this platform
      config.maxReach * 0.001 // Small fraction of total platform users
    );

    const platformBudget = campaignData.budget.totalBudget / campaignData.creative.platforms.length;
    const platformClicks = Math.round(platformBudget / config.avgCPC);
    const platformEngagements = Math.round(platformReach * config.avgEngagementRate);
    const platformCost = platformBudget;

    totalReach += platformReach;
    totalClicks += platformClicks;
    totalEngagements += platformEngagements;
    estimatedCost += platformCost;

    platformBreakdown[platformId] = {
      reach: Math.round(platformReach),
      clicks: platformClicks,
      engagements: platformEngagements,
      cost: platformCost,
      cpc: config.avgCPC,
      ctr: config.avgCTR,
      engagementRate: config.avgEngagementRate
    };

    // Simulate platform campaign creation
    const platformSuccess = Math.random() > 0.1; // 90% success rate
    platformCampaigns.push({
      platform: platformId,
      campaignId: `${platformId}_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`,
      status: platformSuccess ? 'active' : 'error',
      message: platformSuccess 
        ? `Campaign successfully created on ${config.name}`
        : `Failed to create campaign on ${config.name} - please check API credentials`
    });
  }

  // Generate tracking setup
  const trackingUrls = campaignData.creative.content.callToAction.map(cta => {
    const url = new URL(cta.url);
    url.searchParams.set('utm_source', campaignData.analytics.tracking.utmParameters.source);
    url.searchParams.set('utm_medium', campaignData.analytics.tracking.utmParameters.medium);
    url.searchParams.set('utm_campaign', campaignData.analytics.tracking.utmParameters.campaign);
    if (campaignData.analytics.tracking.utmParameters.content) {
      url.searchParams.set('utm_content', campaignData.analytics.tracking.utmParameters.content);
    }
    return url.toString();
  });

  const utmTags = `utm_source=${campaignData.analytics.tracking.utmParameters.source}&utm_medium=${campaignData.analytics.tracking.utmParameters.medium}&utm_campaign=${campaignData.analytics.tracking.utmParameters.campaign}`;
  
  const pixelSetup: { [platform: string]: boolean } = {};
  for (const platformId of campaignData.creative.platforms) {
    pixelSetup[platformId] = !!campaignData.analytics.tracking.pixelIds[platformId];
  }

  // Generate recommendations
  const recommendations: string[] = [];
  
  if (campaignData.creative.content.hashtags.length < 5) {
    recommendations.push('Add more relevant hashtags to increase discoverability');
  }
  
  if (campaignData.creative.content.primaryText.length < 100) {
    recommendations.push('Consider expanding your primary text for better engagement');
  }
  
  if (campaignData.creative.postTypes.length === 1) {
    recommendations.push('Try multiple post types (image, video, carousel) for better performance');
  }
  
  if (campaignData.audience.interests.length < 5) {
    recommendations.push('Add more interest targeting to expand your audience reach');
  }
  
  if (campaignData.budget.totalBudget < 50) {
    recommendations.push('Consider increasing your budget for better reach and engagement');
  }

  // Check for missing pixel tracking
  const missingPixels = campaignData.creative.platforms.filter(p => !campaignData.analytics.tracking.pixelIds[p]);
  if (missingPixels.length > 0) {
    recommendations.push(`Set up tracking pixels for: ${missingPixels.join(', ')}`);
  }

  return {
    success: true,
    campaignId,
    platformCampaigns,
    estimates: {
      totalReach: Math.round(totalReach),
      totalEngagements: Math.round(totalEngagements),
      totalClicks: Math.round(totalClicks),
      estimatedCost: Math.round(estimatedCost * 100) / 100,
      platformBreakdown
    },
    tracking: {
      trackingUrls,
      utmTags,
      pixelSetup
    },
    recommendations
  };
}

export async function POST(request: NextRequest) {
  try {
    const campaignData: SocialMediaCampaignRequest = await request.json();
    
    // Validate required fields
    if (!campaignData.objective || !campaignData.audience || !campaignData.creative || !campaignData.budget) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'Missing required campaign data',
          errors: ['Objective, audience, creative, and budget are required']
        },
        { status: 400 }
      );
    }

    // Validate platforms
    if (!campaignData.creative.platforms || campaignData.creative.platforms.length === 0) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'Platforms are required',
          errors: ['At least one social media platform must be selected']
        },
        { status: 400 }
      );
    }

    // Validate audience
    const selectedSegments = campaignData.audience.segments.filter(s => s.selected);
    if (selectedSegments.length === 0) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'Audience segments are required',
          errors: ['At least one audience segment must be selected']
        },
        { status: 400 }
      );
    }

    // Validate content
    if (!campaignData.creative.content.primaryText) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'Primary content is required',
          errors: ['Primary text content cannot be empty']
        },
        { status: 400 }
      );
    }

    // Validate budget
    if (!campaignData.budget.totalBudget || campaignData.budget.totalBudget <= 0) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'Valid budget amount is required',
          errors: ['Budget amount must be greater than 0']
        },
        { status: 400 }
      );
    }

    // Validate tracking objectives
    if (!campaignData.analytics.objectives || campaignData.analytics.objectives.length === 0) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'Tracking objectives are required',
          errors: ['At least one performance objective must be defined']
        },
        { status: 400 }
      );
    }

    // Create the campaign
    const result = await createSocialMediaCampaign(campaignData);
    
    // Log campaign creation
    console.log(`Social Media campaign created: ${result.campaignId}`, {
      objective: campaignData.objective.type,
      platforms: campaignData.creative.platforms,
      budget: `${campaignData.budget.currency} ${campaignData.budget.totalBudget}`,
      audienceSize: campaignData.audience.segments.filter(s => s.selected).reduce((sum, s) => sum + s.size, 0),
      timestamp: new Date().toISOString()
    });

    return NextResponse.json(result);
    
  } catch (error) {
    console.error('Error creating Social Media campaign:', error);
    return NextResponse.json(
      { 
        success: false,
        error: 'Failed to create campaign due to internal error',
        errors: ['An unexpected error occurred. Please try again.'],
        details: process.env.NODE_ENV === 'development' ? String(error) : undefined
      },
      { status: 500 }
    );
  }
}

// GET endpoint to retrieve campaign status
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const campaignId = searchParams.get('campaignId');
    
    if (!campaignId) {
      return NextResponse.json(
        { error: 'Campaign ID is required' },
        { status: 400 }
      );
    }

    // Mock campaign status retrieval
    const mockStatus = {
      campaignId,
      status: 'active',
      performance: {
        reach: 45632,
        impressions: 156789,
        engagements: 3421,
        clicks: 892,
        shares: 156,
        comments: 234,
        likes: 2876,
        cost: 167.83,
        ctr: 0.57,
        engagementRate: 2.18,
        cpc: 0.19
      },
      platformPerformance: {
        facebook: {
          reach: 23456,
          engagements: 1567,
          clicks: 445,
          cost: 78.92
        },
        instagram: {
          reach: 18976,
          engagements: 1654,
          clicks: 389,
          cost: 67.45
        },
        twitter: {
          reach: 3200,
          engagements: 200,
          clicks: 58,
          cost: 21.46
        }
      },
      lastUpdated: new Date().toISOString(),
      budget: {
        total: 500.00,
        spent: 167.83,
        remaining: 332.17,
        dailySpent: 23.97
      }
    };
    
    return NextResponse.json(mockStatus);
    
  } catch (error) {
    console.error('Error retrieving social media campaign status:', error);
    return NextResponse.json(
      { error: 'Failed to retrieve campaign status' },
      { status: 500 }
    );
  }
}

// PUT endpoint to update campaign
export async function PUT(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const campaignId = searchParams.get('campaignId');
    const updateData = await request.json();
    
    if (!campaignId) {
      return NextResponse.json(
        { error: 'Campaign ID is required' },
        { status: 400 }
      );
    }

    // Mock campaign update
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const result = {
      success: true,
      campaignId,
      message: 'Social media campaign updated successfully',
      updatedFields: Object.keys(updateData),
      platformsUpdated: updateData.platforms || [],
      lastUpdated: new Date().toISOString()
    };
    
    console.log(`Social Media campaign updated: ${campaignId}`, updateData);
    
    return NextResponse.json(result);
    
  } catch (error) {
    console.error('Error updating Social Media campaign:', error);
    return NextResponse.json(
      { 
        success: false,
        error: 'Failed to update campaign'
      },
      { status: 500 }
    );
  }
}

// DELETE endpoint to pause/delete campaign
export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const campaignId = searchParams.get('campaignId');
    const action = searchParams.get('action') || 'pause';
    
    if (!campaignId) {
      return NextResponse.json(
        { error: 'Campaign ID is required' },
        { status: 400 }
      );
    }

    // Mock campaign pause/delete across platforms
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const result = {
      success: true,
      campaignId,
      action,
      message: action === 'delete' 
        ? 'Social media campaign deleted across all platforms' 
        : 'Social media campaign paused across all platforms',
      platformResults: [
        { platform: 'facebook', success: true, message: `Campaign ${action}d successfully` },
        { platform: 'instagram', success: true, message: `Campaign ${action}d successfully` },
        { platform: 'twitter', success: true, message: `Campaign ${action}d successfully` }
      ],
      timestamp: new Date().toISOString()
    };
    
    console.log(`Social Media campaign ${action}d: ${campaignId}`);
    
    return NextResponse.json(result);
    
  } catch (error) {
    console.error(`Error ${searchParams.get('action') || 'pausing'} Social Media campaign:`, error);
    return NextResponse.json(
      { 
        success: false,
        error: `Failed to ${searchParams.get('action') || 'pause'} campaign`
      },
      { status: 500 }
    );
  }
}