import { useState, useEffect } from 'react'
import type { Game, Tournament, GamingAPIResponse, GamingStats } from '../types/gaming'

export const usePopularGames = (limit = 20, platform = 'all') => {
  const [games, setGames] = useState<Game[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [source, setSource] = useState<string>('unknown')

  useEffect(() => {
    const fetchGames = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch(`/api/brain/gaming/popular-games?limit=${limit}&platform=${platform}`)
        const result: GamingAPIResponse<Game> = await response.json()

        if (result.success) {
          setGames(result.data)
          setSource(result.source)
        } else {
          setError(result.error || 'Failed to fetch games')
        }

      } catch (err) {
        console.error('[THRILLRING] Error fetching popular games:', err)
        setError('Network error fetching games')
      } finally {
        setLoading(false)
      }
    }

    fetchGames()
  }, [limit, platform])

  return { games, loading, error, source }
}

export const useTournaments = (status = 'all', game = 'all', limit = 20) => {
  const [tournaments, setTournaments] = useState<Tournament[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [source, setSource] = useState<string>('unknown')

  useEffect(() => {
    const fetchTournaments = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch(`/api/brain/gaming/tournaments?status=${status}&game=${game}&limit=${limit}`)
        const result: GamingAPIResponse<Tournament> = await response.json()

        if (result.success) {
          setTournaments(result.data)
          setSource(result.source)
        } else {
          setError(result.error || 'Failed to fetch tournaments')
        }

      } catch (err) {
        console.error('[THRILLRING] Error fetching tournaments:', err)
        setError('Network error fetching tournaments')
      } finally {
        setLoading(false)
      }
    }

    fetchTournaments()
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
  const { games } = usePopularGames(6)
  const { tournaments } = useTournaments('all', 'all', 10)

  useEffect(() => {
    if (games.length > 0 && tournaments.length > 0) {
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
      setLoading(false)
    }
  }, [games, tournaments])

  return { stats, loading }
}
