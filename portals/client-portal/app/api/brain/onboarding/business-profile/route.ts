import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://brain-gateway:8000';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validate required fields
    const { business_type, industry, company_size, goals } = body;

    if (!body) {
      return NextResponse.json(
        { error: 'Missing request body' },
        { status: 400 }
      );
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/onboarding/business-profile`, {
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
      console.error('Brain API onboarding/business-profile POST error:', response.status);
      return NextResponse.json(
        { error: 'Failed to create business profile' },
        { status: response.status }
      );
    }

    return NextResponse.json(await response.json());

  } catch (error) {
    console.error('Business profile creation error:', error);
    return NextResponse.json(
      { error: 'Failed to create business profile', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    const response = await fetch(`${BRAIN_API_URL}/api/brain/onboarding/business-profile`, {
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
        'X-Tenant-ID': request.headers.get('X-Tenant-ID') || 'default'
      },
    });

    if (!response.ok) {
      console.error('Brain API onboarding/business-profile GET error:', response.status);
      return NextResponse.json(
        { error: 'Failed to fetch business profile' },
        { status: response.status }
      );
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Business profile GET error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch business profile', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}
