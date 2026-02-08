import { useState, useEffect } from 'react'
import type { Game, Tournament, GamingAPIResponse, GamingStats } from '../types/gaming'

export const usePopularGames = (limit = 20, platform = 'all') => {
  const [games, setGames] = useState<Game[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [source, setSource] = useState<string>('unknown')

  useEffect(() => {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 5000) // 5 second timeout

    const fetchGames = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch(
          `/api/brain/gaming/popular-games?limit=${limit}&platform=${platform}`,
          { signal: controller.signal }
        )

        clearTimeout(timeoutId)

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`)
        }

        const result: GamingAPIResponse<Game> = await response.json()

        if (result.success) {
          setGames(result.data)
          setSource(result.source)
        } else {
          setError(result.error || 'Failed to fetch games')
        }

      } catch (err: any) {
        clearTimeout(timeoutId)
        if (err.name === 'AbortError') {
          console.warn('[THRILLRING] Request timeout - using fallback empty data')
          setError('Backend unavailable - showing offline mode')
        } else {
          console.error('[THRILLRING] Error fetching popular games:', err)
          setError('Network error fetching games')
        }
        setGames([]) // Fallback to empty array
      } finally {
        setLoading(false)
      }
    }

    fetchGames()

    return () => {
      clearTimeout(timeoutId)
      controller.abort()
    }
  }, [limit, platform])

  return { games, loading, error, source }
}

export const useTournaments = (status = 'all', game = 'all', limit = 20) => {
  const [tournaments, setTournaments] = useState<Tournament[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [source, setSource] = useState<string>('unknown')

  useEffect(() => {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 5000) // 5 second timeout

    const fetchTournaments = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch(
          `/api/brain/gaming/tournaments?status=${status}&game=${game}&limit=${limit}`,
          { signal: controller.signal }
        )

        clearTimeout(timeoutId)

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`)
        }

        const result: GamingAPIResponse<Tournament> = await response.json()

        if (result.success) {
          setTournaments(result.data)
          setSource(result.source)
        } else {
          setError(result.error || 'Failed to fetch tournaments')
        }

      } catch (err: any) {
        clearTimeout(timeoutId)
        if (err.name === 'AbortError') {
          console.warn('[THRILLRING] Request timeout - using fallback empty data')
          setError('Backend unavailable - showing offline mode')
        } else {
          console.error('[THRILLRING] Error fetching tournaments:', err)
          setError('Network error fetching tournaments')
        }
        setTournaments([]) // Fallback to empty array
      } finally {
        setLoading(false)
      }
    }

    fetchTournaments()

    return () => {
      clearTimeout(timeoutId)
      controller.abort()
    }
  }, [status, game, limit])

  return { tournaments, loading, error, source }
}

export const useGamingStats = (): { stats: GamingStats; loading: boolean } => {
  const [stats, setStats] = useState<GamingStats>({
    totalPlayers: 0,
    activeTournaments: 0,
    totalPrizePool: 0,
    liveMatches: 0
  })
  const [loading, setLoading] = useState(true)
  const { games, loading: gamesLoading } = usePopularGames(6)
  const { tournaments, loading: tournamentsLoading } = useTournaments('all', 'all', 10)

  useEffect(() => {
    // Wait for both hooks to finish loading
    if (!gamesLoading && !tournamentsLoading) {
      if (games.length > 0 || tournaments.length > 0) {
        const totalPlayers = games.reduce((sum, game) => sum + (game.active_players || 0), 0)
        const activeTournaments = tournaments.filter(t => t.status === 'live' || t.status === 'registration_open').length
        const totalPrizePool = tournaments.reduce((sum, tournament) => sum + tournament.prize_pool, 0)
        const liveMatches = tournaments.filter(t => t.status === 'live').length * 10 // Estimate

        setStats({
          totalPlayers,
          activeTournaments,
          totalPrizePool,
          liveMatches
        })
      }
      setLoading(false)
    }
  }, [games, tournaments, gamesLoading, tournamentsLoading])

  return { stats, loading }
}

export const useLeaderboard = (gameSlug: string) => {
  const [leaderboard, setLeaderboard] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        setLoading(true)
        const response = await fetch(`/api/brain/gaming/leaderboard/${gameSlug}`)
        if (!response.ok) throw new Error('Failed to fetch leaderboard')
        const data = await response.json()
        setLeaderboard(data)
      } catch (err: any) {
        console.error('Leaderboard fetch error:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    if (gameSlug) fetchLeaderboard()
  }, [gameSlug])

  return { leaderboard, loading, error }
}
