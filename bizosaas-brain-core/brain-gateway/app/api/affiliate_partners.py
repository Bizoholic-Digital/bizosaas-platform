from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.dependencies import get_db, require_role
from app.domain.ports.identity_port import AuthenticatedUser
from app.models.marketplace import AffiliatePartner
from pydantic import BaseModel, HttpUrl

router = APIRouter()

# Schema
class AffiliatePartnerBase(BaseModel):
    name: str
    slug: str
    website_url: Optional[HttpUrl] = None
    is_active: bool = True

class AffiliatePartnerCreate(AffiliatePartnerBase):
    api_config: Dict[str, Any] = {}

class AffiliatePartnerResponse(AffiliatePartnerBase):
    id: str
    
    class Config:
        from_attributes = True

# Routes
@router.get("/", response_model=List[AffiliatePartnerResponse])
async def list_partners(
    current_user: AuthenticatedUser = Depends(require_role("Super Admin")),
    db: Session = Depends(get_db)
):
    """Admin only: List all affiliate partners."""
    partners = db.query(AffiliatePartner).all()
    return partners

@router.post("/", response_model=AffiliatePartnerResponse, status_code=201)
async def create_partner(
    request: AffiliatePartnerCreate,
    current_user: AuthenticatedUser = Depends(require_role("Super Admin")),
    db: Session = Depends(get_db)
):
    """Admin only: Create a new affiliate partner."""
    if db.query(AffiliatePartner).filter(AffiliatePartner.slug == request.slug).first():
        raise HTTPException(status_code=400, detail="Partner with this slug already exists")
    
    partner = AffiliatePartner(**request.model_dump())
    db.add(partner)
    db.commit()
    db.refresh(partner)
    return partner

@router.patch("/{partner_id}", response_model=AffiliatePartnerResponse)
async def update_partner(
    partner_id: str,
    request: AffiliatePartnerCreate,
    current_user: AuthenticatedUser = Depends(require_role("Super Admin")),
    db: Session = Depends(get_db)
):
    """Admin only: Update an existing affiliate partner."""
    partner = db.query(AffiliatePartner).filter(AffiliatePartner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    
    for key, value in request.model_dump(exclude_unset=True).items():
        setattr(partner, key, value)
    
    db.commit()
    db.refresh(partner)
    return partner
