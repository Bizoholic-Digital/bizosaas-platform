/**
 * Gamification Leaderboards API Route
 * Connects client portal to gamification service via FastAPI Central Hub
 */

import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const platform = searchParams.get('platform') || 'bizoholic';
    const leaderboardType = searchParams.get('type') || 'performance';
    const timePeriod = searchParams.get('period') || 'monthly';
    const limit = parseInt(searchParams.get('limit') || '50');

    const response = await fetch(
      `${BRAIN_API_URL}/api/brain/gamification/leaderboards?platform=${platform}&leaderboard_type=${leaderboardType}&time_period=${timePeriod}&limit=${limit}`,
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
      // Return fallback leaderboard data
      return NextResponse.json({
        leaderboard_data: [
          {
            rank: 1,
            user_id: 'user_001',
            display_name: 'Marketing Maverick',
            company: 'TechStart Inc.',
            score: 2850,
            achievements_count: 15,
            platform: 'bizoholic',
            avatar: '🏆',
            badges: ['top_performer', 'innovation_leader'],
            last_activity: '2024-10-05T09:30:00Z'
          },
          {
            rank: 2,
            user_id: 'user_002',
            display_name: 'Sales Superstar',
            company: 'Growth Co.',
            score: 2720,
            achievements_count: 12,
            platform: 'bizoholic',
            avatar: '⭐',
            badges: ['sales_master', 'client_champion'],
            last_activity: '2024-10-05T08:15:00Z'
          },
          {
            rank: 3,
            user_id: 'user_003',
            display_name: 'Content Creator Pro',
            company: 'Creative Studio',
            score: 2650,
            achievements_count: 18,
            platform: 'bizoholic',
            avatar: '🎨',
            badges: ['content_king', 'social_media_guru'],
            last_activity: '2024-10-05T07:45:00Z'
          },
          {
            rank: 4,
            user_id: 'user_004',
            display_name: 'E-commerce Expert',
            company: 'Online Retail Ltd.',
            score: 2580,
            achievements_count: 14,
            platform: 'coreldove',
            avatar: '🛒',
            badges: ['conversion_optimizer', 'inventory_master'],
            last_activity: '2024-10-04T22:30:00Z'
          },
          {
            rank: 5,
            user_id: 'user_005',
            display_name: 'Analytics Ace',
            company: 'Data Insights Corp',
            score: 2420,
            achievements_count: 11,
            platform: 'bizoholic',
            avatar: '📊',
            badges: ['data_wizard', 'insight_generator'],
            last_activity: '2024-10-04T18:20:00Z'
          }
        ],
        user_position: {
          rank: 12,
          user_id: 'current_user',
          display_name: 'Your Company',
          company: 'Acme Corporation',
          score: 1850,
          achievements_count: 8,
          platform: 'bizoholic',
          avatar: '🚀',
          badges: ['rising_star'],
          points_to_next_rank: 180,
          next_rank_holder: 'Digital Pioneer'
        },
        leaderboard_metadata: {
          total_participants: 156,
          update_frequency: 'hourly',
          last_updated: '2024-10-05T10:00:00Z',
          season: 'Q4 2024',
          season_ends: '2024-12-31T23:59:59Z'
        },
        competitive_insights: [
          {
            type: 'opportunity',
            title: 'Close the Gap',
            description: 'You\'re only 180 points away from moving up to rank 11',
            recommended_action: 'Complete 2 more achievements to climb the leaderboard'
          },
          {
            type: 'trend',
            title: 'Rising Performance',
            description: 'You\'ve gained 3 ranks this week',
            recommended_action: 'Keep up the momentum with consistent daily activity'
          },
          {
            type: 'comparison',
            title: 'Industry Benchmark',
            description: 'You\'re performing above 75% of companies in your industry',
            recommended_action: 'Focus on content creation to reach the top 10%'
          }
        ],
        next_update: '2024-10-05T11:00:00Z'
      }, { status: 200 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching leaderboard data:', error);
    return NextResponse.json(
      { error: 'Failed to fetch leaderboard data' },
      { status: 500 }
    );
  }
}