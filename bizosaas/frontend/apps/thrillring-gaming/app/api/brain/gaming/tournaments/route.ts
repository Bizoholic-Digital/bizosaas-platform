import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const limit = parseInt(searchParams.get('limit') || '20')
    const status = searchParams.get('status') || 'all'
    const game = searchParams.get('game') || 'all'

    console.log('[THRILLRING-GAMING] Fetching tournaments:', { limit, status, game })

    // Try FastAPI Brain Gateway first with 3 second timeout
    try {
      console.log('[THRILLRING-GAMING] Trying FastAPI Brain Gateway')

      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 3000) // 3 second timeout

      const response = await fetch(`${BRAIN_API_URL}/api/brain/gaming/tournaments?limit=${limit}&status=${status}&game=${game}`, {
        headers: {
          'Content-Type': 'application/json',
          'Host': 'localhost:3005',
        },
        signal: controller.signal,
        next: { revalidate: 300 } // Cache for 5 minutes
      })

      clearTimeout(timeoutId)

      if (response.ok) {
        const brainData = await response.json()
        console.log('[THRILLRING-GAMING] Brain Gateway success')
        return NextResponse.json({
          success: true,
          source: 'brain_gateway',
          data: brainData.tournaments || brainData.data || [],
          meta: brainData.meta || {}
        })
      }
    } catch (brainError: any) {
      if (brainError.name === 'AbortError') {
        console.log('[THRILLRING-GAMING] Brain Gateway timeout - using fallback')
      } else {
        console.error('[THRILLRING-GAMING] Brain Gateway failed:', brainError)
      }
    }

    // Enhanced fallback tournament data
    console.log('[THRILLRING-GAMING] Using enhanced fallback data')
    const fallbackTournaments = [
      {
        id: 1,
        title: "Apex Legends Championship Series",
        description: "The ultimate battle royale tournament with $100,000 prize pool",
        game: "Apex Legends",
        prize_pool: 100000,
        currency: "USD",
        participants: 156,
        max_participants: 200,
        status: "live",
        registration_status: "closed",
        start_date: "2025-11-05T10:00:00Z",
        end_date: "2025-11-07T20:00:00Z",
        registration_deadline: "2025-11-03T23:59:59Z",
        format: "Battle Royale - Squad (3 players)",
        platform: ["PC", "PlayStation", "Xbox"],
        region: "North America",
        organizer: "ThrillRing Esports",
        stream_url: "https://twitch.tv/thrillring",
        rules_url: "https://thrillring.com/tournaments/apex-rules",
        image_url: "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800",
        featured: true,
        skill_level: "Professional",
        entry_fee: 0,
        min_team_size: 3,
        max_team_size: 3
      },
      {
        id: 2,
        title: "Valorant Masters Tournament",
        description: "Tactical FPS showdown with $75,000 on the line",
        game: "Valorant",
        prize_pool: 75000,
        currency: "USD",
        participants: 89,
        max_participants: 128,
        status: "registration_open",
        registration_status: "open",
        start_date: "2025-11-10T10:00:00Z",
        end_date: "2025-11-12T20:00:00Z",
        registration_deadline: "2025-11-08T23:59:59Z",
        format: "5v5 - Team Tournament",
        platform: ["PC"],
        region: "Europe",
        organizer: "ThrillRing Esports",
        stream_url: "https://twitch.tv/thrillring",
        rules_url: "https://thrillring.com/tournaments/valorant-rules",
        image_url: "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800",
        featured: true,
        skill_level: "Semi-Professional",
        entry_fee: 0,
        min_team_size: 5,
        max_team_size: 7
      },
      {
        id: 3,
        title: "League of Legends Regional Cup",
        description: "The ultimate MOBA showdown with $150,000 prize pool",
        game: "League of Legends",
        prize_pool: 150000,
        currency: "USD",
        participants: 64,
        max_participants: 64,
        status: "coming_soon",
        registration_status: "coming_soon",
        start_date: "2025-11-20T10:00:00Z",
        end_date: "2025-11-22T20:00:00Z",
        registration_deadline: "2025-11-15T23:59:59Z",
        format: "5v5 - Double Elimination",
        platform: ["PC"],
        region: "Asia-Pacific",
        organizer: "ThrillRing Esports",
        stream_url: "https://twitch.tv/thrillring",
        rules_url: "https://thrillring.com/tournaments/lol-rules",
        image_url: "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800",
        featured: true,
        skill_level: "Professional",
        entry_fee: 50,
        min_team_size: 5,
        max_team_size: 7
      }
    ]

    return NextResponse.json({
      success: true,
      source: 'enhanced_fallback',
      data: fallbackTournaments.slice(0, limit),
      meta: {
        total: fallbackTournaments.length,
        limit,
        status,
        game,
        note: 'Enhanced fallback tournament data'
      }
    })

  } catch (error) {
    console.error('[THRILLRING-GAMING] Tournaments API error:', error)
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to fetch tournaments',
        source: 'error_fallback',
        data: []
      },
      { status: 500 }
    )
  }
}
