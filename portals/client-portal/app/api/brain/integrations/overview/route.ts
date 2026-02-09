import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://brain-gateway:8000';

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
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
        'X-Tenant-ID': request.headers.get('X-Tenant-ID') || 'default'
      },
    });

    if (!response.ok) {
      console.error('Brain API integrations/overview error:', response.status);
      return NextResponse.json(
        { error: 'Failed to fetch integrations overview' },
        { status: response.status }
      );
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Integrations overview API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const response = await fetch(`${BRAIN_API_URL}/api/brain/integrations/overview`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
        'X-Tenant-ID': request.headers.get('X-Tenant-ID') || 'default'
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      console.error('Brain API integrations/overview POST error:', response.status);
      return NextResponse.json(
        { error: 'Failed to process overview action' },
        { status: response.status }
      );
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