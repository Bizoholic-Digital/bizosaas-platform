/**
 * Gamification Achievements API Route
 * Connects client portal to gamification service via FastAPI Central Hub
 */

import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const tenantId = searchParams.get('tenant_id');
    const platform = searchParams.get('platform') || 'bizoholic';
    const forceRefresh = searchParams.get('force_refresh') === 'true';

    if (!tenantId) {
      return NextResponse.json({ error: 'Tenant ID is required' }, { status: 400 });
    }

    const response = await fetch(
      `${BRAIN_API_URL}/api/brain/gamification/achievements/progress/${tenantId}?platform=${platform}&force_refresh=${forceRefresh}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Host': 'localhost:3001',
          'Authorization': request.headers.get('Authorization') || 'Bearer mock-token',
        },
      }
    );

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status);
      // Return fallback achievement data
      return NextResponse.json({
        unlocked_achievements: [
          {
            id: 'first_lead',
            name: 'First Lead Generated',
            description: 'Generated your first lead through the platform',
            icon: '🎯',
            points: 100,
            category: 'milestone',
            unlocked_at: '2024-10-01T10:00:00Z',
            platform: 'bizoholic'
          },
          {
            id: 'content_creator',
            name: 'Content Creator',
            description: 'Published 10 blog posts via Wagtail CMS',
            icon: '✍️',
            points: 250,
            category: 'content',
            unlocked_at: '2024-10-03T14:30:00Z',
            platform: 'bizoholic'
          }
        ],
        updated_progress: [
          {
            achievement_id: 'sales_master',
            name: 'Sales Master',
            description: 'Close $10,000 in sales',
            current_value: 7500,
            target_value: 10000,
            progress_percentage: 75,
            icon: '💰',
            category: 'performance'
          },
          {
            achievement_id: 'social_influencer',
            name: 'Social Influencer',
            description: 'Gain 1000 social media followers',
            current_value: 850,
            target_value: 1000,
            progress_percentage: 85,
            icon: '📱',
            category: 'social'
          }
        ],
        recommendations: [
          {
            type: 'quick_win',
            title: 'Close 1 more deal',
            description: 'You need $2,500 more in sales to unlock the Sales Master achievement',
            estimated_effort: 'Medium',
            potential_points: 500
          },
          {
            type: 'engagement',
            title: 'Create a case study',
            description: 'Showcase your successful campaigns to unlock the Case Study Expert badge',
            estimated_effort: 'High',
            potential_points: 300
          }
        ],
        engagement_score: 85.5,
        cross_client_insights_count: 12
      }, { status: 200 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching achievement data:', error);
    return NextResponse.json(
      { error: 'Failed to fetch achievement data' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const response = await fetch(`${BRAIN_API_URL}/api/brain/gamification/achievements/custom`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3001',
        'Authorization': request.headers.get('Authorization') || 'Bearer mock-token',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      console.error('Failed to create custom achievement:', response.status);
      return NextResponse.json(
        { error: 'Failed to create custom achievement' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error creating custom achievement:', error);
    return NextResponse.json(
      { error: 'Failed to create custom achievement' },
      { status: 500 }
    );
  }
}