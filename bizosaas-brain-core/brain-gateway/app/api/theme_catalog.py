from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional, Dict, Any
from app.dependencies import get_db, get_current_user, require_role
from app.domain.ports.identity_port import AuthenticatedUser
from app.models.marketplace import ThemeTemplate, AffiliatePartner
from pydantic import BaseModel

router = APIRouter()

# Schema
class ThemeResponse(BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str]
    category: Optional[str]
    price: float
    currency: str
    preview_url: Optional[str]
    thumbnail_url: Optional[str]
    affiliate_link: Optional[str]
    tags: List[str]
    partner_name: Optional[str]

    class Config:
        from_attributes = True

# Routes
@router.get("/", response_model=List[ThemeResponse])
async def list_themes(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Browse the theme catalog with filters."""
    query = db.query(ThemeTemplate).filter(ThemeTemplate.is_active == True)
    
    if category:
        query = query.filter(ThemeTemplate.category == category)
    
    if min_price is not None:
        query = query.filter(ThemeTemplate.price >= min_price)
    
    if max_price is not None:
        query = query.filter(ThemeTemplate.price <= max_price)
        
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                ThemeTemplate.name.ilike(search_filter),
                ThemeTemplate.description.ilike(search_filter),
                ThemeTemplate.category.ilike(search_filter)
            )
        )
        
    themes = query.all()
    return themes

@router.get("/{slug}", response_model=ThemeResponse)
async def get_theme(slug: str, db: Session = Depends(get_db)):
    """Get detailed information about a specific theme."""
    theme = db.query(ThemeTemplate).filter(ThemeTemplate.slug == slug).first()
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")
    return theme

@router.post("/sync", status_code=202)
async def sync_themes(
    partner_slug: str = "envato",
    current_user: AuthenticatedUser = Depends(require_role("Super Admin")),
    db: Session = Depends(get_db)
):
    """Admin only: Trigger a sync of themes from affiliate partners."""
    from app.services.envato_service import EnvatoService
    
    service = EnvatoService(db)
    result = await service.sync_themes(partner_slug)
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error"))
        
    return result
