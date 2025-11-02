import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const response = await fetch(`${BRAIN_API_URL}/api/brain/business-directory/google/auth/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3006',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status);
      // Fallback OAuth start response
      return NextResponse.json({
        auth_url: "https://accounts.google.com/oauth/authorize?client_id=example&redirect_uri=http://localhost:3006/api/brain/business-directory/google/auth/callback&scope=https://www.googleapis.com/auth/business.manage&response_type=code&state=fallback_state",
        state: "fallback_state",
        expires_at: new Date(Date.now() + 3600000).toISOString(),
        source: "fallback"
      }, { status: 200 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Google OAuth start error:', error);
    return NextResponse.json({
      error: 'Failed to initiate Google OAuth',
      source: "error"
    }, { status: 500 });
  }
}