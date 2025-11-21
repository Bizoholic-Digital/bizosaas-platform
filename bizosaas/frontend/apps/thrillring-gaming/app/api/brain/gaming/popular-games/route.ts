import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const limit = parseInt(searchParams.get('limit') || '20')
    const platform = searchParams.get('platform') || 'all'

    console.log('[THRILLRING-GAMING] Fetching popular games:', { limit, platform })

    // Try FastAPI Brain Gateway first with 3 second timeout
    try {
      console.log('[THRILLRING-GAMING] Trying FastAPI Brain Gateway')

      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 3000) // 3 second timeout

      const response = await fetch(`${BRAIN_API_URL}/api/brain/gaming/popular-games?limit=${limit}&platform=${platform}`, {
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
          data: brainData.games || brainData.data || [],
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

    // Enhanced fallback data
    console.log('[THRILLRING-GAMING] Using enhanced fallback data')
    const fallbackGames = [
      {
        id: 1,
        name: "Apex Legends",
        description: "A free-to-play battle royale game with unique character abilities and fast-paced combat.",
        image_url: "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=400",
        rating: 95,
        platforms: ["PC", "PlayStation", "Xbox", "Nintendo Switch"],
        genre: ["Battle Royale", "FPS"],
        release_date: "2019-02-04",
        developer: "Respawn Entertainment",
        publisher: "Electronic Arts",
        price: 0,
        status: "live",
        tournament_prize_pool: 100000,
        active_players: 2048000,
        twitch_viewers: 85000
      },
      {
        id: 2,
        name: "Valorant",
        description: "A tactical 5v5 character-based shooter with unique agent abilities and strategic gameplay.",
        image_url: "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=400",
        rating: 92,
        platforms: ["PC"],
        genre: ["Tactical Shooter", "FPS"],
        release_date: "2020-06-02",
        developer: "Riot Games",
        publisher: "Riot Games",
        price: 0,
        status: "registration_open",
        tournament_prize_pool: 75000,
        active_players: 1024000,
        twitch_viewers: 120000
      },
      {
        id: 3,
        name: "League of Legends",
        description: "The world's most popular MOBA game with intense strategic team-based gameplay.",
        image_url: "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=400",
        rating: 97,
        platforms: ["PC", "Mobile"],
        genre: ["MOBA", "Strategy"],
        release_date: "2009-10-27",
        developer: "Riot Games",
        publisher: "Riot Games",
        price: 0,
        status: "coming_soon",
        tournament_prize_pool: 150000,
        active_players: 4096000,
        twitch_viewers: 200000
      },
      {
        id: 4,
        name: "Counter-Strike 2",
        description: "The legendary tactical FPS returns with enhanced graphics and refined gameplay mechanics.",
        image_url: "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=400",
        rating: 94,
        platforms: ["PC"],
        genre: ["Tactical Shooter", "FPS"],
        release_date: "2023-09-27",
        developer: "Valve Corporation",
        publisher: "Valve Corporation",
        price: 0,
        status: "live",
        tournament_prize_pool: 200000,
        active_players: 1500000,
        twitch_viewers: 95000
      },
      {
        id: 5,
        name: "Dota 2",
        description: "The ultimate MOBA experience with complex strategies and massive competitive scene.",
        image_url: "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=400",
        rating: 96,
        platforms: ["PC"],
        genre: ["MOBA", "Strategy"],
        release_date: "2013-07-09",
        developer: "Valve Corporation",
        publisher: "Valve Corporation",
        price: 0,
        status: "live",
        tournament_prize_pool: 500000,
        active_players: 800000,
        twitch_viewers: 180000
      },
      {
        id: 6,
        name: "Overwatch 2",
        description: "Hero-based team shooter with dynamic gameplay and evolving meta strategies.",
        image_url: "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=400",
        rating: 89,
        platforms: ["PC", "PlayStation", "Xbox", "Nintendo Switch"],
        genre: ["Hero Shooter", "FPS"],
        release_date: "2022-10-04",
        developer: "Blizzard Entertainment",
        publisher: "Blizzard Entertainment",
        price: 0,
        status: "registration_open",
        tournament_prize_pool: 120000,
        active_players: 950000,
        twitch_viewers: 75000
      }
    ]

    return NextResponse.json({
      success: true,
      source: 'enhanced_fallback',
      data: fallbackGames.slice(0, limit),
      meta: {
        total: fallbackGames.length,
        limit,
        platform,
        note: 'Enhanced fallback data with gaming tournament details'
      }
    })

  } catch (error) {
    console.error('[THRILLRING-GAMING] Popular games API error:', error)
    return NextResponse.json(
      {
        success: false,
        error: 'Failed to fetch popular games',
        source: 'error_fallback',
        data: []
      },
      { status: 500 }
    )
  }
}
