from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from domain.ports.identity_port import AuthenticatedUser
from app.models.gaming import Tournament, Match, Game, PlayerGamingStats, GameCompany, HumanPlayerProfile
from pydantic import BaseModel
from typing import List, Optional
import uuid

router = APIRouter()

class TournamentCreate(BaseModel):
    name: str
    game_slug: str
    type: str = "single_elimination"
    max_participants: int = 16

@router.post("/tournaments")
async def create_tournament(
    req: TournamentCreate,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    game = db.query(Game).filter(Game.slug == req.game_slug).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    tournament = Tournament(
        name=req.name,
        tenant_id=current_user.tenant_id,
        game_id=game.id,
        type=req.type,
        max_participants=req.max_participants,
        status="draft"
    )
    db.add(tournament)
    db.commit()
    db.refresh(tournament)
    return tournament

@router.get("/tournaments", response_model=List[dict])
async def list_tournaments(
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tournaments = db.query(Tournament).filter(Tournament.tenant_id == current_user.tenant_id).all()
    return tournaments

@router.get("/leaderboard/{game_slug}")
async def get_leaderboard(
    game_slug: str,
    db: Session = Depends(get_db)
):
    game = db.query(Game).filter(Game.slug == game_slug).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    stats = db.query(PlayerGamingStats).filter(
        PlayerGamingStats.game_id == game.id
    ).order_by(PlayerGamingStats.mmr.desc()).limit(100).all()
    
    return stats

@router.get("/companies/{slug}")
async def get_company_wiki(
    slug: str,
    db: Session = Depends(get_db)
):
    company = db.query(GameCompany).filter(GameCompany.slug == slug).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.get("/wiki/game/{slug}")
async def get_game_wiki(
    slug: str,
    db: Session = Depends(get_db)
):
    game = db.query(Game).filter(Game.slug == slug).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.get("/profiles/{nickname}")
async def get_player_profile(
    nickname: str,
    db: Session = Depends(get_db)
):
    profile = db.query(HumanPlayerProfile).filter(HumanPlayerProfile.nickname == nickname).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Player profile not found")
    return profile
