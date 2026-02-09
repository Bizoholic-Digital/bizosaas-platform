import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://brain-gateway:8000';

export async function POST(request: NextRequest) {
  try {
    const campaignData = await request.json();

    // Validate required fields (basic validation, backend should do full validation)
    if (!campaignData.objective || !campaignData.targeting || !campaignData.creative || !campaignData.budget) {
      return NextResponse.json(
        {
          success: false,
          error: 'Missing required campaign data',
          errors: ['Objective, targeting, creative, and budget are required']
        },
        { status: 400 }
      );
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/campaign-wizards/google-ads`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
        'X-Tenant-ID': request.headers.get('X-Tenant-ID') || 'default'
      },
      body: JSON.stringify(campaignData)
    });

    if (!response.ok) {
      console.error('Brain API campaign-wizards/google-ads POST error:', response.status);
      const errorData = await response.json().catch(() => ({}));
      return NextResponse.json(
        {
          success: false,
          error: 'Failed to create Google Ads campaign',
          details: errorData
        },
        { status: response.status }
      );
    }

    return NextResponse.json(await response.json());

  } catch (error) {
    console.error('Error creating Google Ads campaign:', error);
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to create campaign due to internal error',
        details: error instanceof Error ? error.message : 'Unknown error'
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

    const response = await fetch(`${BRAIN_API_URL}/api/brain/campaign-wizards/google-ads?campaignId=${campaignId}`, {
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
        'X-Tenant-ID': request.headers.get('X-Tenant-ID') || 'default'
      },
    });

    if (!response.ok) {
      console.error('Brain API campaign-wizards/google-ads GET error:', response.status);
      return NextResponse.json(
        { error: 'Failed to retrieve campaign status' },
        { status: response.status }
      );
    }

    return NextResponse.json(await response.json());

  } catch (error) {
    console.error('Error retrieving campaign status:', error);
    return NextResponse.json(
      { error: 'Failed to retrieve campaign status', details: error instanceof Error ? error.message : 'Unknown error' },
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

    const response = await fetch(`${BRAIN_API_URL}/api/brain/campaign-wizards/google-ads?campaignId=${campaignId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
        'X-Tenant-ID': request.headers.get('X-Tenant-ID') || 'default'
      },
      body: JSON.stringify(updateData)
    });

    if (!response.ok) {
      console.error('Brain API campaign-wizards/google-ads PUT error:', response.status);
      return NextResponse.json(
        { error: 'Failed to update campaign' },
        { status: response.status }
      );
    }

    return NextResponse.json(await response.json());

  } catch (error) {
    console.error('Error updating Google Ads campaign:', error);
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
    const action = searchParams.get('action') || 'pause'; // 'pause' or 'delete'

    if (!campaignId) {
      return NextResponse.json(
        { error: 'Campaign ID is required' },
        { status: 400 }
      );
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/campaign-wizards/google-ads?campaignId=${campaignId}&action=${action}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
        'X-Tenant-ID': request.headers.get('X-Tenant-ID') || 'default'
      }
    });

    if (!response.ok) {
      console.error('Brain API campaign-wizards/google-ads DELETE error:', response.status);
      return NextResponse.json(
        { error: `Failed to ${action} campaign` },
        { status: response.status }
      );
    }

    return NextResponse.json(await response.json());

  } catch (error) {
    console.error(`Error ${searchParams.get('action') || 'pausing'} Google Ads campaign:`, error);
    return NextResponse.json(
      {
        success: false,
        error: `Failed to ${searchParams.get('action') || 'pause'} campaign`
      },
      { status: 500 }
    );
  }
}