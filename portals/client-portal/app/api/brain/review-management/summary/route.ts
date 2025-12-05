import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const days = searchParams.get('days') || '30';
    
    // Forward request to BizOSaaS Brain API
    const brainApiUrl = `${process.env.BIZOSAAS_BRAIN_API_URL || 'http://localhost:3006'}/api/brain/review-management/summary?days=${days}`;
    
    const response = await fetch(brainApiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        // Forward authorization header if present
        ...(request.headers.get('authorization') && {
          authorization: request.headers.get('authorization')!
        }),
      },
    });

    if (!response.ok) {
      throw new Error(`Brain API responded with status: ${response.status}`);
    }

    const data = await response.json();
    
    return NextResponse.json(data);
  } catch (error) {
    console.error('Review summary API error:', error);
    
    // Return mock data for development
    return NextResponse.json({
      totalReviews: 145,
      platformBreakdown: {
        google_business: 85,
        yelp: 35,
        facebook: 25
      },
      sentimentDistribution: {
        positive: 98,
        neutral: 32,
        negative: 15
      },
      averageRating: 4.3,
      responseRate: 0.87,
      recentActivity: [
        {
          id: '1',
          platform: 'google_business',
          rating: 5,
          sentiment: 'positive',
          timestamp: new Date().toISOString()
        },
        {
          id: '2',
          platform: 'yelp',
          rating: 2,
          sentiment: 'negative',
          timestamp: new Date(Date.now() - 86400000).toISOString()
        }
      ]
    });
  }
}