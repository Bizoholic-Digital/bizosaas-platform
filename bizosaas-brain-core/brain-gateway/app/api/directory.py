from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.dependencies import get_db, get_current_user
from app.services.directory_service import DirectoryService
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/api/brain/business-directory", tags=["business-directory"])

class ListingCreate(BaseModel):
    name: str
    slug: Optional[str] = None
    google_place_id: Optional[str] = None
    location: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    category: Optional[str] = None
    google_data: Optional[Dict[str, Any]] = None
    google_rating: Optional[float] = None
    google_reviews_count: Optional[int] = None

@router.get("/search")
async def search_directory(
    query: Optional[str] = None,
    location: Optional[str] = None,
    category: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = DirectoryService(db)
    return await service.search(query, location, category, page, limit)

@router.get("/businesses/featured")
async def get_featured(db: Session = Depends(get_db)):
    # Simple implementation: just newest for now
    service = DirectoryService(db)
    return await service.search(limit=6)

@router.get("/businesses/{slug}")
async def get_business(slug: str, db: Session = Depends(get_db)):
    service = DirectoryService(db)
    business = await service.get_by_slug(slug)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    # Log view (don't wait for it)
    import asyncio
    asyncio.create_task(service.log_view(business.id))
    
    return business

@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    # Get unique categories from listing table
    from app.models.directory import DirectoryListing
    categories = db.query(DirectoryListing.category).filter(DirectoryListing.category != None).distinct().all()
    # Flatten list
    cat_list = [c[0] for c in categories]
    return cat_list

@router.post("/businesses")
async def create_listing(
    data: ListingCreate,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user)
):
    service = DirectoryService(db)
    return await service.create_from_places_data(data.model_dump(), user_id=user.id)

@router.post("/businesses/{id}/click")
async def log_click(
    id: uuid.UUID,
    click_type: str = Query(..., regex="^(phone|website|directions)$"),
    db: Session = Depends(get_db)
):
    service = DirectoryService(db)
    await service.log_click(id, click_type)
    return {"status": "success"}

class ClaimRequest(BaseModel):
    method: str
    data: Optional[Dict[str, Any]] = None

@router.post("/businesses/{id}/claim")
async def claim_business(
    id: uuid.UUID,
    claim: ClaimRequest,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user)
):
    service = DirectoryService(db)
    return await service.create_claim_request(id, user.id, claim.method, claim.data or {})
