import { NextRequest, NextResponse } from 'next/server';

// Backend API configuration
const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';
const ANALYTICS_DASHBOARD_URL = 'http://localhost:3009';

// Mock analytics data for fallback
const mockAnalyticsData = {
  overview: {
    total_campaigns: 12,
    active_campaigns: 5,
    total_leads: 847,
    conversion_rate: 28.3,
    total_revenue: 67890,
    roi: 285.4
  },
  campaign_performance: [
    {
      campaign_id: 'camp_001',
      name: 'Google Ads - Q4 2024',
      channel: 'google_ads',
      status: 'active',
      spend: 3200,
      leads: 89,
      conversions: 24,
      revenue: 9650,
      roi: 301.6,
      last_updated: '2024-09-23T15:45:00Z'
    },
    {
      campaign_id: 'camp_002',
      name: 'Facebook Marketing Campaign',
      channel: 'facebook_ads', 
      status: 'active',
      spend: 2100,
      leads: 67,
      conversions: 19,
      revenue: 7230,
      roi: 344.3,
      last_updated: '2024-09-23T15:30:00Z'
    },
    {
      campaign_id: 'camp_003',
      name: 'LinkedIn B2B Outreach',
      channel: 'linkedin_ads',
      status: 'paused',
      spend: 1850,
      leads: 34,
      conversions: 12,
      revenue: 4560,
      roi: 246.5,
      last_updated: '2024-09-23T14:20:00Z'
    }
  ],
  channel_performance: {
    google_ads: {
      leads: 89,
      spend: 3200,
      revenue: 9650,
      roi: 301.6,
      trend: 'up'
    },
    facebook_ads: {
      leads: 67,
      spend: 2100, 
      revenue: 7230,
      roi: 344.3,
      trend: 'up'
    },
    linkedin_ads: {
      leads: 34,
      spend: 1850,
      revenue: 4560,
      roi: 246.5,
      trend: 'down'
    },
    email_marketing: {
      leads: 45,
      spend: 680,
      revenue: 2890,
      roi: 425.0,
      trend: 'stable'
    }
  },
  real_time_metrics: {
    active_visitors: 847,
    live_conversions_today: 12,
    revenue_today: 3420,
    top_performing_campaign: 'Facebook Marketing Campaign',
    alerts: [
      {
        type: 'warning',
        message: 'LinkedIn campaign conversion rate dropped 15% today',
        timestamp: '2024-09-23T15:30:00Z'
      },
      {
        type: 'success',
        message: 'Google Ads campaign exceeded daily target by 25%',
        timestamp: '2024-09-23T14:45:00Z'
      }
    ]
  },
  recent_activity: [
    {
      timestamp: '2024-09-23T15:45:00Z',
      type: 'conversion',
      campaign: 'Google Ads - Q4 2024',
      value: 425,
      description: 'Lead converted to customer - $425 revenue'
    },
    {
      timestamp: '2024-09-23T15:30:00Z',
      type: 'lead',
      campaign: 'Facebook Marketing Campaign',
      value: 0,
      description: 'New qualified lead from Facebook ad'
    },
    {
      timestamp: '2024-09-23T15:15:00Z',
      type: 'optimization',
      campaign: 'Google Ads - Q4 2024',
      value: 0,
      description: 'Bid adjustment applied based on performance data'
    }
  ],
  last_updated: '2024-09-23T15:47:00Z'
};

export async function GET(request: NextRequest) {
  try {
    console.log('[CLIENT-PORTAL] GET analytics dashboard data');

    // Try to get data from analytics dashboard service first
    try {
      const analyticsUrl = `${ANALYTICS_DASHBOARD_URL}/api/analytics/dashboard`;
      const response = await fetch(analyticsUrl, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Client-Portal/1.0.0'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('[CLIENT-PORTAL] Analytics dashboard data retrieved successfully');
        return NextResponse.json(data);
      } else {
        console.warn(`[CLIENT-PORTAL] Analytics dashboard error: ${response.status}`);
        throw new Error(`Analytics dashboard API error: ${response.status}`);
      }
    } catch (analyticsError) {
      console.warn('[CLIENT-PORTAL] Analytics dashboard connection failed, trying Brain Gateway:', analyticsError);
      
      // Fallback to Brain Gateway
      try {
        const brainUrl = `${BRAIN_API_URL}/api/analytics/dashboards`;
        const brainResponse = await fetch(brainUrl, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'User-Agent': 'Client-Portal/1.0.0',
            'X-Tenant-ID': request.headers.get('X-Tenant-ID') || 'default'
          }
        });

        if (brainResponse.ok) {
          const data = await brainResponse.json();
          console.log('[CLIENT-PORTAL] Analytics data retrieved from Brain Gateway');
          return NextResponse.json(data);
        } else {
          throw new Error(`Brain Gateway analytics error: ${brainResponse.status}`);
        }
      } catch (brainError) {
        console.warn('[CLIENT-PORTAL] Brain Gateway analytics failed:', brainError);
        console.log('[CLIENT-PORTAL] Using fallback analytics data');
        
        return NextResponse.json(mockAnalyticsData);
      }
    }
  } catch (error) {
    console.error('[CLIENT-PORTAL] Analytics dashboard API error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch analytics data', details: error.message },
      { status: 500 }
    );
  }
}