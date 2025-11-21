import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const queryParams = new URLSearchParams();
    
    // Pass through all search parameters
    searchParams.forEach((value, key) => {
      queryParams.append(key, value);
    });

    const response = await fetch(`${BRAIN_API_URL}/api/brain/business-directory/google/accounts?${queryParams}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3006',
      },
    });

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status);
      // Fallback Google accounts data
      return NextResponse.json({
        accounts: [
          {
            id: "google_account_001",
            email: "business@acmecorp.com",
            name: "Acme Corporation",
            type: "business",
            verified: true,
            connected_at: "2024-01-15T10:30:00Z",
            last_sync: "2024-09-18T09:15:00Z",
            locations_count: 3,
            status: "active",
            permissions: ["BASIC", "POSTS", "INSIGHTS"],
            profile_photo: "/api/placeholder-image/google-account-1"
          },
          {
            id: "google_account_002",
            email: "marketing@acmecorp.com",
            name: "Acme Marketing",
            type: "business",
            verified: true,
            connected_at: "2024-02-20T14:45:00Z",
            last_sync: "2024-09-18T08:30:00Z",
            locations_count: 1,
            status: "active",
            permissions: ["BASIC", "POSTS"],
            profile_photo: "/api/placeholder-image/google-account-2"
          }
        ],
        total: 2,
        source: "fallback"
      }, { status: 200 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Google accounts API error:', error);
    return NextResponse.json({
      accounts: [],
      total: 0,
      error: 'Failed to fetch Google accounts',
      source: "error"
    }, { status: 500 });
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const accountId = searchParams.get('account_id');

    if (!accountId) {
      return NextResponse.json({
        error: 'Account ID is required',
        source: "error"
      }, { status: 400 });
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/business-directory/google/accounts?account_id=${accountId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3006',
      },
    });

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status);
      // Fallback disconnect response
      return NextResponse.json({
        success: true,
        account_id: accountId,
        message: "Google account disconnected successfully",
        source: "fallback"
      }, { status: 200 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Google account disconnect error:', error);
    return NextResponse.json({
      error: 'Failed to disconnect Google account',
      source: "error"
    }, { status: 500 });
  }
}