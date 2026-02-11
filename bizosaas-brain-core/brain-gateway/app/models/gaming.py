from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, JSON, Float, Text
from sqlalchemy.orm import relationship
from .utils import GUID
from .base import Base
import uuid
from datetime import datetime

class GameCompany(Base):
    __tablename__ = "game_companies"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    slug = Column(String(150), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    website = Column(String(255), nullable=True)
    headquarters = Column(String(255), nullable=True)
    founded_at = Column(DateTime(timezone=True), nullable=True)
    type = Column(String(50), default="developer") # developer, publisher, service_provider
    
    # Wiki Data
    wiki_content = Column(JSON, default={}) # News, milestones, major releases
    meta_data = Column(JSON, default={}) 
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Game(Base):
    __tablename__ = "games"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    genre = Column(String(100), nullable=True)
    release_date = Column(DateTime(timezone=True), nullable=True)
    engine = Column(String(100), nullable=True)
    
    # Relationships
    developer_id = Column(GUID, ForeignKey("game_companies.id"), nullable=True)
    publisher_id = Column(GUID, ForeignKey("game_companies.id"), nullable=True)
    
    # Wiki Data
    wiki_data = Column(JSON, default={}) # History, Gameplay mechanics, Platform availability
    media_assets = Column(JSON, default={}) # Banners, trailers, screenshots
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(GUID, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    game_id = Column(GUID, ForeignKey("games.id"), nullable=False)
    name = Column(String(150), nullable=False)
    type = Column(String(50), nullable=False, default="single_elimination")
    status = Column(String(20), default="draft", nullable=False)
    max_participants = Column(Integer, default=16)
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)
    settings = Column(JSON, default={})
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Match(Base):
    __tablename__ = "matches"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    tournament_id = Column(GUID, ForeignKey("tournaments.id", ondelete="CASCADE"), nullable=False)
    round = Column(Integer, default=1)
    position = Column(Integer, nullable=True)
    
    player1_id = Column(GUID, ForeignKey("users.id"), nullable=True)
    player2_id = Column(GUID, ForeignKey("users.id"), nullable=True)
    
    score1 = Column(Integer, default=0)
    score2 = Column(Integer, default=0)
    
    winner_id = Column(GUID, ForeignKey("users.id"), nullable=True)
    status = Column(String(20), default="scheduled", nullable=False)
    
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

class HumanPlayerProfile(Base):
    __tablename__ = "human_player_profiles"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Gaming Identity
    nickname = Column(String(100), unique=True, nullable=False, index=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(255), nullable=True)
    
    # Wiki / Personal Data
    full_name = Column(String(150), nullable=True)
    spouse_name = Column(String(150), nullable=True)
    kids_names = Column(JSON, default=[]) # List of names
    birth_date = Column(DateTime(timezone=True), nullable=True)
    location = Column(String(255), nullable=True)
    
    # Career & News
    news_mentions = Column(JSON, default=[]) # Links and snippets
    milestones = Column(JSON, default={}) # Career highlights
    social_links = Column(JSON, default={})
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class PlayerGamingStats(Base):
    __tablename__ = "player_gaming_stats"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    game_id = Column(GUID, ForeignKey("games.id"), nullable=False)
    tenant_id = Column(GUID, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    
    mmr = Column(Float, default=1000.0)
    rank = Column(String(50), nullable=True)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    total_matches = Column(Integer, default=0)
    
    meta_data = Column(JSON, default={}) 
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
