export interface Game {
  id: number
  name: string
  description: string
  image_url: string
  rating: number
  platforms: string[]
  genre: string[]
  release_date: string
  developer: string
  publisher: string
  price: number
  status?: string
  tournament_prize_pool?: number
  active_players?: number
  twitch_viewers?: number
}

export interface Tournament {
  id: number
  title: string
  description: string
  game: string
  prize_pool: number
  currency: string
  participants: number
  max_participants: number
  status: string
  registration_status: string
  start_date: string
  end_date: string
  registration_deadline: string
  format: string
  platform: string[]
  region: string
  organizer: string
  stream_url?: string
  rules_url?: string
  image_url?: string
  featured?: boolean
  skill_level?: string
  entry_fee?: number
  min_team_size?: number
  max_team_size?: number
}

export interface GamingAPIResponse<T> {
  success: boolean
  source: string
  data: T[]
  meta?: any
  error?: string
}

export interface GamingStats {
  totalPlayers: number
  activeTournaments: number
  totalPrizePool: number
  liveMatches: number
}
