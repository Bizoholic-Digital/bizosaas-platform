import { NextRequest, NextResponse } from 'next/server';

// Backend API configuration
const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://brain-gateway:8000';
const ANALYTICS_DASHBOARD_URL = 'http://localhost:3009';

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
      }

      console.warn(`[CLIENT-PORTAL] Analytics dashboard error: ${response.status} - Falling back to Brain Gateway`);
    } catch (analyticsError) {
      console.warn('[CLIENT-PORTAL] Analytics dashboard connection failed, trying Brain Gateway:', analyticsError);
    }

    // Fallback to Brain Gateway
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
      console.error(`Brain Gateway analytics error: ${brainResponse.status}`);
      return NextResponse.json(
        { error: 'Failed to fetch analytics data from upstream services' },
        { status: brainResponse.status }
      );
    }

  } catch (error) {
    console.error('[CLIENT-PORTAL] Analytics dashboard API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}