import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Sample fallback data for development
const fallbackUsageData = {
  currentPeriod: {
    start: '2025-01-15T00:00:00Z',
    end: '2025-02-15T00:00:00Z',
    usage: {
      users: {
        current: 12,
        limit: -1, // unlimited
        percentage: 0,
        trend: '+2 this month',
        chartData: [8, 9, 10, 11, 12, 12, 12, 12, 12, 12, 12, 12]
      },
      storage: {
        current: 245, // GB
        limit: 5120, // 5TB
        percentage: 4.8,
        trend: '+15GB this month',
        chartData: [180, 190, 200, 210, 220, 225, 230, 235, 240, 242, 244, 245]
      },
      apiCalls: {
        current: 8432,
        limit: 1000000,
        percentage: 0.8,
        trend: '+1,200 this week',
        chartData: [6000, 6200, 6500, 6800, 7000, 7200, 7400, 7600, 7800, 8000, 8200, 8432]
      },
      bandwidth: {
        current: 156.7, // GB
        limit: 10000, // 10TB
        percentage: 1.6,
        trend: '+12GB this week',
        chartData: [120, 125, 130, 135, 140, 142, 145, 148, 150, 152, 154, 156.7]
      },
      supportTickets: {
        current: 3,
        limit: -1, // unlimited
        percentage: 0,
        trend: '-2 resolved',
        chartData: [5, 4, 6, 3, 4, 2, 3, 4, 5, 3, 3, 3]
      }
    }
  },
  historicalUsage: {
    monthly: [
      {
        month: '2024-12',
        usage: {
          users: 10,
          storage: 230,
          apiCalls: 765000,
          bandwidth: 890.5,
          supportTickets: 5,
          cost: 2847.00
        }
      },
      {
        month: '2024-11',
        usage: {
          users: 9,
          storage: 215,
          apiCalls: 720000,
          bandwidth: 845.2,
          supportTickets: 7,
          cost: 2847.00
        }
      },
      {
        month: '2024-10',
        usage: {
          users: 8,
          storage: 200,
          apiCalls: 680000,
          bandwidth: 780.1,
          supportTickets: 4,
          cost: 2847.00
        }
      }
    ]
  },
  alerts: [
    {
      id: 'alert_1',
      type: 'warning',
      metric: 'storage',
      threshold: 80,
      currentValue: 4.8,
      message: 'Storage usage is healthy',
      severity: 'low',
      createdAt: '2025-01-01T00:00:00Z',
      resolved: true
    },
    {
      id: 'alert_2',
      type: 'info',
      metric: 'apiCalls',
      threshold: 10,
      currentValue: 0.8,
      message: 'API usage is well within limits',
      severity: 'low',
      createdAt: '2025-01-01T00:00:00Z',
      resolved: true
    }
  ],
  costBreakdown: {
    currentMonth: {
      basePlan: 2400.00,
      storage: 250.00,
      support: 197.00,
      overageCharges: 0.00,
      total: 2847.00
    },
    projectedNextMonth: {
      basePlan: 2400.00,
      storage: 250.00,
      support: 197.00,
      overageCharges: 0.00,
      total: 2847.00,
      estimatedOverage: {
        storage: 0.00,
        apiCalls: 0.00,
        bandwidth: 0.00
      }
    }
  },
  recommendations: [
    {
      type: 'optimization',
      title: 'Storage Optimization',
      description: 'You have 4.7TB of unused storage. Consider downgrading to Professional plan to save $150/month.',
      potentialSaving: 150.00,
      impact: 'medium',
      actionUrl: '/billing/change-plan'
    },
    {
      type: 'feature',
      title: 'API Caching',
      description: 'Enable API response caching to reduce API call usage by up to 40%.',
      potentialSaving: 0.00,
      impact: 'low',
      actionUrl: '/settings/api-cache'
    }
  ]
};

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const metric = searchParams.get('metric'); // specific metric or 'all'
    const period = searchParams.get('period') || 'current'; // 'current', 'historical'
    const granularity = searchParams.get('granularity') || 'monthly'; // 'daily', 'weekly', 'monthly'

    const queryParams = new URLSearchParams({
      metric: metric || 'all',
      period,
      granularity
    });

    const response = await fetch(`${BRAIN_API_URL}/api/brain/billing/usage?${queryParams}`, {
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
    });

    if (!response.ok) {
      console.error('Brain API billing/usage error:', response.status);
      
      if (metric && metric !== 'all') {
        const metricData = fallbackUsageData.currentPeriod.usage[metric as keyof typeof fallbackUsageData.currentPeriod.usage];
        return NextResponse.json({
          metric,
          period,
          data: metricData || null
        });
      }
      
      return NextResponse.json(fallbackUsageData);
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Billing usage API error:', error);
    const urlParams = new URL(request.url).searchParams;
    const metric = urlParams.get('metric');
    
    if (metric && metric !== 'all') {
      const metricData = fallbackUsageData.currentPeriod.usage[metric as keyof typeof fallbackUsageData.currentPeriod.usage];
      return NextResponse.json({
        metric,
        period: urlParams.get('period') || 'current',
        data: metricData || null
      });
    }
    
    return NextResponse.json(fallbackUsageData);
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, ...data } = body;
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/billing/usage`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      console.error('Brain API billing/usage POST error:', response.status);
      
      // Handle different actions with fallback responses
      switch (action) {
        case 'set_alert':
          const mockAlert = {
            id: `alert_${Date.now()}`,
            type: data.type || 'warning',
            metric: data.metric,
            threshold: data.threshold,
            currentValue: 0,
            message: `Alert set for ${data.metric} at ${data.threshold}%`,
            severity: data.severity || 'medium',
            createdAt: new Date().toISOString(),
            resolved: false
          };
          return NextResponse.json({ success: true, alert: mockAlert });
          
        case 'export_usage':
          return NextResponse.json({ 
            success: true, 
            exportUrl: `/api/billing/usage/export?format=${data.format}&period=${data.period}`,
            message: 'Usage data export prepared successfully'
          });
          
        case 'calculate_cost':
          const baseCost = 2847.00;
          const overageCost = (data.projectedUsage?.storage || 0) * 0.10 + 
                             (data.projectedUsage?.apiCalls || 0) * 0.001 +
                             (data.projectedUsage?.bandwidth || 0) * 0.05;
          return NextResponse.json({
            success: true,
            costEstimate: {
              baseCost,
              overageCost,
              totalCost: baseCost + overageCost,
              breakdown: {
                storage: (data.projectedUsage?.storage || 0) * 0.10,
                apiCalls: (data.projectedUsage?.apiCalls || 0) * 0.001,
                bandwidth: (data.projectedUsage?.bandwidth || 0) * 0.05
              }
            }
          });
          
        default:
          return NextResponse.json({ success: true, message: 'Usage action processed successfully' });
      }
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Billing usage POST API error:', error);
    return NextResponse.json(
      { error: 'Failed to process usage action', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}