import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://brain-gateway:8000';

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
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
        'X-Tenant-ID': request.headers.get('X-Tenant-ID') || 'default'
      },
    });

    if (!response.ok) {
      console.error('Brain API billing/usage error:', response.status);
      return NextResponse.json(
        { error: 'Failed to fetch usage data' },
        { status: response.status }
      );
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Billing usage API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const response = await fetch(`${BRAIN_API_URL}/api/brain/billing/usage`, {
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
      console.error('Brain API billing/usage POST error:', response.status);
      return NextResponse.json(
        { error: 'Failed to process usage action' },
        { status: response.status }
      );
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