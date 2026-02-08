import strawberry
from typing import List, Optional
from datetime import datetime

@strawberry.type
class GameType:
    id: int
    name: str
    description: str = ""
    image_url: str = ""
    rating: float = 0.0
    release_date: str = ""
    developer: str = ""
    publisher: str = ""
    price: float = 0.0
    active_players: int = 0
    twitch_viewers: int = 0
    # Arrays need to be typed carefully in strawberry
    platforms: List[str]
    genre: List[str]

@strawberry.type
class TournamentType:
    id: int
    title: str
    description: str = ""
    game: str
    prize_pool: float
    currency: str = "USD"
    participants: int = 0
    max_participants: int = 0
    status: str
    registration_status: str
    start_date: str
    end_date: str
    registration_deadline: str = ""
    format: str = ""
    region: str = ""
    organizer: str = ""
    stream_url: str = ""
    image_url: str = ""
    featured: bool = False
    entry_fee: float = 0.0
    # Lists
    platform: List[str]

@strawberry.type
class LeaderboardEntryType:
    rank: int
    name: str
    wins: int
    points: int
    earnings: float
    avatar: str = ""

@strawberry.type
class GamingStatsType:
    total_players: int
    active_tournaments: int
    total_prize_pool: float
    live_matches: int
