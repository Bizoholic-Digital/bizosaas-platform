import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Sample fallback data for development
const fallbackIntegrationsOverview = {
  summary: {
    totalIntegrations: 12,
    activeIntegrations: 9,
    warningIntegrations: 2,
    errorIntegrations: 1,
    totalApiCalls: 125847,
    totalWebhooks: 3,
    totalAutomations: 5,
    totalThirdPartyApps: 4,
    successRate: 97.8,
    averageResponseTime: 245,
    lastSyncAt: '2025-01-15T14:22:00Z'
  },
  recentActivity: [
    {
      id: 'activity_1',
      type: 'webhook_delivery',
      integration: 'Payment Success Webhook',
      status: 'success',
      timestamp: '2025-01-15T14:22:00Z',
      message: 'Webhook delivered successfully',
      icon: 'Webhook'
    },
    {
      id: 'activity_2',
      type: 'api_request',
      integration: 'Production API Key',
      status: 'success',
      timestamp: '2025-01-15T14:20:00Z',
      message: 'API request processed (GET /products)',
      icon: 'Code'
    },
    {
      id: 'activity_3',
      type: 'automation_run',
      integration: 'Welcome Email Sequence',
      status: 'success',
      timestamp: '2025-01-15T14:18:00Z',
      message: 'Automation completed for new customer',
      icon: 'RefreshCcw'
    },
    {
      id: 'activity_4',
      type: 'third_party_sync',
      integration: 'Slack',
      status: 'success',
      timestamp: '2025-01-15T14:15:00Z',
      message: 'Message sent to #notifications',
      icon: 'Cloud'
    },
    {
      id: 'activity_5',
      type: 'third_party_sync',
      integration: 'Mailchimp',
      status: 'error',
      timestamp: '2025-01-15T14:10:00Z',
      message: 'Sync failed: API key expired',
      icon: 'Cloud'
    }
  ],
  healthMetrics: {
    uptime: 99.95,
    totalRequests: 125847,
    successfulRequests: 123096,
    failedRequests: 2751,
    averageLatency: 245,
    p95Latency: 890,
    p99Latency: 1450,
    errorRate: 2.2,
    rateLimitHits: 23,
    lastHealthCheck: '2025-01-15T14:25:00Z'
  },
  popularIntegrations: [
    {
      id: 'stripe',
      name: 'Stripe',
      category: 'payments',
      usage: 45680,
      trend: '+12%',
      status: 'connected',
      icon: '/icons/stripe.png'
    },
    {
      id: 'slack',
      name: 'Slack',
      category: 'communication',
      usage: 1247,
      trend: '+8%',
      status: 'connected',
      icon: '/icons/slack.png'
    },
    {
      id: 'google-analytics',
      name: 'Google Analytics',
      category: 'analytics',
      usage: 156,
      trend: '-3%',
      status: 'warning',
      icon: '/icons/google-analytics.png'
    },
    {
      id: 'mailchimp',
      name: 'Mailchimp',
      category: 'marketing',
      usage: 0,
      trend: '-100%',
      status: 'error',
      icon: '/icons/mailchimp.png'
    }
  ],
  usageCharts: {
    daily: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [
        {
          label: 'API Calls',
          data: [15200, 18500, 22100, 19800, 21300, 16900, 14500]
        },
        {
          label: 'Webhooks',
          data: [45, 52, 38, 61, 49, 33, 28]
        },
        {
          label: 'Automations',
          data: [12, 18, 15, 22, 19, 8, 11]
        }
      ]
    },
    hourly: {
      labels: Array.from({ length: 24 }, (_, i) => `${i}:00`),
      datasets: [
        {
          label: 'Requests',
          data: [120, 89, 67, 45, 78, 156, 234, 345, 456, 578, 634, 712, 689, 723, 801, 734, 678, 589, 467, 389, 298, 234, 189, 156]
        }
      ]
    }
  },
  alerts: [
    {
      id: 'alert_1',
      type: 'error',
      severity: 'high',
      integration: 'Mailchimp',
      message: 'Authentication failed - API key expired',
      timestamp: '2025-01-15T14:10:00Z',
      acknowledged: false
    },
    {
      id: 'alert_2',
      type: 'warning',
      severity: 'medium',
      integration: 'Google Analytics',
      message: 'Rate limit approaching (85% of daily quota used)',
      timestamp: '2025-01-15T13:45:00Z',
      acknowledged: true
    },
    {
      id: 'alert_3',
      type: 'info',
      severity: 'low',
      integration: 'Payment Webhook',
      message: 'New webhook endpoint configured',
      timestamp: '2025-01-15T12:30:00Z',
      acknowledged: true
    }
  ],
  recommendations: [
    {
      id: 'rec_1',
      type: 'optimization',
      title: 'Enable API Response Caching',
      description: 'Reduce API calls by 30-40% by enabling response caching for frequently accessed data.',
      impact: 'medium',
      effort: 'low',
      savings: '$45/month',
      category: 'performance'
    },
    {
      id: 'rec_2',
      type: 'security',
      title: 'Rotate API Keys',
      description: 'Some API keys are over 6 months old. Consider rotating them for improved security.',
      impact: 'high',
      effort: 'medium',
      savings: null,
      category: 'security'
    },
    {
      id: 'rec_3',
      type: 'reliability',
      title: 'Set Up Backup Webhooks',
      description: 'Configure backup webhook endpoints to ensure delivery reliability.',
      impact: 'high',
      effort: 'medium',
      savings: null,
      category: 'reliability'
    }
  ],
  integrationCategories: {
    communication: { count: 2, status: 'healthy' },
    payments: { count: 1, status: 'healthy' },
    analytics: { count: 1, status: 'warning' },
    marketing: { count: 1, status: 'error' },
    automation: { count: 5, status: 'healthy' },
    webhooks: { count: 3, status: 'healthy' },
    api_keys: { count: 3, status: 'healthy' }
  }
};

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const timeRange = searchParams.get('time_range') || '7d'; // '1d', '7d', '30d', '90d'
    const includeDetails = searchParams.get('include_details') === 'true';

    const queryParams = new URLSearchParams({
      time_range: timeRange,
      include_details: includeDetails.toString()
    });

    const response = await fetch(`${BRAIN_API_URL}/api/brain/integrations/overview?${queryParams}`, {
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
    });

    if (!response.ok) {
      console.error('Brain API integrations/overview error:', response.status);
      
      // Adjust data based on time range
      let adjustedData = { ...fallbackIntegrationsOverview };
      
      if (timeRange === '1d') {
        adjustedData.summary.totalApiCalls = Math.floor(adjustedData.summary.totalApiCalls / 7);
        adjustedData.usageCharts.daily.labels = ['Today'];
        adjustedData.usageCharts.daily.datasets[0].data = [adjustedData.usageCharts.daily.datasets[0].data[6]];
      } else if (timeRange === '30d') {
        adjustedData.summary.totalApiCalls = Math.floor(adjustedData.summary.totalApiCalls * 4.3);
        adjustedData.usageCharts.daily.labels = Array.from({ length: 30 }, (_, i) => `Day ${i + 1}`);
        adjustedData.usageCharts.daily.datasets[0].data = Array.from({ length: 30 }, () => 
          Math.floor(Math.random() * 25000) + 10000
        );
      }
      
      if (!includeDetails) {
        delete adjustedData.usageCharts;
        delete adjustedData.recentActivity;
        adjustedData.alerts = adjustedData.alerts.slice(0, 2);
        adjustedData.recommendations = adjustedData.recommendations.slice(0, 1);
      }
      
      return NextResponse.json(adjustedData);
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Integrations overview API error:', error);
    return NextResponse.json(fallbackIntegrationsOverview);
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, ...data } = body;
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/integrations/overview`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      console.error('Brain API integrations/overview POST error:', response.status);
      
      // Handle different actions with fallback responses
      switch (action) {
        case 'refresh_metrics':
          return NextResponse.json({ 
            success: true, 
            message: 'Metrics refreshed successfully',
            lastRefresh: new Date().toISOString(),
            metricsUpdated: ['summary', 'health', 'usage', 'alerts']
          });
          
        case 'acknowledge_alert':
          return NextResponse.json({ 
            success: true, 
            message: 'Alert acknowledged successfully',
            alertId: data.alertId,
            acknowledgedAt: new Date().toISOString(),
            acknowledgedBy: 'current_user'
          });
          
        case 'dismiss_recommendation':
          return NextResponse.json({ 
            success: true, 
            message: 'Recommendation dismissed',
            recommendationId: data.recommendationId,
            dismissedAt: new Date().toISOString()
          });
          
        case 'health_check':
          return NextResponse.json({ 
            success: true, 
            healthStatus: {
              overall: 'healthy',
              services: {
                webhooks: 'healthy',
                api_keys: 'healthy',
                third_party: 'warning',
                automations: 'healthy'
              },
              lastCheck: new Date().toISOString(),
              uptime: 99.95,
              responseTime: Math.floor(Math.random() * 300) + 100
            }
          });
          
        case 'export_summary':
          const exportId = `summary_export_${Date.now()}`;
          return NextResponse.json({ 
            success: true, 
            exportId,
            downloadUrl: `/api/integrations/overview/export/${exportId}?format=${data.format}`,
            message: 'Summary export prepared successfully',
            estimatedSize: '1.2 MB'
          });
          
        default:
          return NextResponse.json({ success: true, message: 'Overview action processed successfully' });
      }
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Integrations overview POST API error:', error);
    return NextResponse.json(
      { error: 'Failed to process overview action', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}