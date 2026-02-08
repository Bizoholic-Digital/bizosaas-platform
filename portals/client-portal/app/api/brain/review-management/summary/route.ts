import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const days = searchParams.get('days') || '30';

    // Forward request to BizOSaaS Brain API
    const brainApiUrl = `${process.env.BIZOSAAS_BRAIN_API_URL || 'http://brain-gateway:8000'}/api/brain/review-management/summary?days=${days}`;

    const response = await fetch(brainApiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        // Forward authorization header if present
        ...(request.headers.get('authorization') && {
          authorization: request.headers.get('authorization')!
        }),
        'X-Tenant-ID': request.headers.get('X-Tenant-ID') || 'default'
      },
    });

    if (!response.ok) {
      console.error(`Brain API responded with status: ${response.status}`);
      return NextResponse.json(
        { error: 'Failed to fetch review summary data' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Review summary API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}