from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
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
    use_google: bool = True,
    db: Session = Depends(get_db)
):
    service = DirectoryService(db)
    return await service.search(query, location, category, page, limit, use_google)

@router.get("/autocomplete")
async def autocomplete_directory(
    query: str,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = DirectoryService(db)
    return await service.autocomplete(query, location)

@router.get("/businesses/featured")
async def get_featured(db: Session = Depends(get_db)):
    # Simple implementation: just newest for now
    service = DirectoryService(db)
    return await service.search(limit=6)

@router.get("/businesses/my")
async def get_my_listings(
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user)
):
    service = DirectoryService(db)
    return await service.get_user_listings(user.id)

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

@router.get("/businesses/{id}/events")
async def get_business_events(id: uuid.UUID, db: Session = Depends(get_db)):
    service = DirectoryService(db)
    return await service.get_events(id)

@router.get("/businesses/{id}/products")
async def get_business_products(id: uuid.UUID, db: Session = Depends(get_db)):
    from app.models.directory import DirectoryListing
    business = db.query(DirectoryListing).filter(DirectoryListing.id == id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business.products or []

@router.get("/businesses/{id}/coupons")
async def get_business_coupons(id: uuid.UUID, db: Session = Depends(get_db)):
    service = DirectoryService(db)
    return await service.get_coupons(id)

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    external_link: Optional[str] = None

class CouponCreate(BaseModel):
    title: str
    description: Optional[str] = None
    code: Optional[str] = None
    discount_value: Optional[str] = None
    expiry_date: Optional[datetime] = None
    terms_link: Optional[str] = None

@router.post("/businesses/{id}/events")
async def create_event(
    id: uuid.UUID,
    event: EventCreate,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user)
):
    service = DirectoryService(db)
    return await service.create_event(id, user.id, event.model_dump())

@router.post("/businesses/{id}/coupons")
async def create_coupon(
    id: uuid.UUID,
    coupon: CouponCreate,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user)
):
    service = DirectoryService(db)
    return await service.create_coupon(id, user.id, coupon.model_dump())

@router.get("/businesses/{id}/reviews")
async def get_business_reviews(id: uuid.UUID, db: Session = Depends(get_db)):
    # Simple placeholder returning empty list for now until we have a review model
    # Wait, let's check if we have a Review model
    return []

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

class EnquirySubmit(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    subject: Optional[str] = None
    message: str

@router.post("/businesses/{id}/claim")
async def claim_business(
    id: uuid.UUID,
    claim: ClaimRequest,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user)
):
    service = DirectoryService(db)
    return await service.create_claim_request(id, user.id, claim.method, claim.data or {})

class VerifyRequest(BaseModel):
    code: str

@router.post("/claims/{claim_id}/verify")
async def verify_claim(
    claim_id: uuid.UUID,
    data: VerifyRequest,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user)
):
    service = DirectoryService(db)
    return await service.verify_claim_code(claim_id, user.id, data.code)

@router.post("/claims/{claim_id}/resend")
async def resend_claim_code(
    claim_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user)
):
    service = DirectoryService(db)
    return await service.resend_claim_code(claim_id, user.id)

@router.post("/businesses/{id}/enquire")
async def submit_enquiry(
    id: uuid.UUID,
    enquiry: EnquirySubmit,
    db: Session = Depends(get_db)
):
    service = DirectoryService(db)
    return await service.create_enquiry(id, enquiry.model_dump())

@router.get("/businesses/{id}/enquiries")
async def get_enquiries(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user)
):
    service = DirectoryService(db)
    # Service will check if user owns the listing
    return await service.get_enquiries(id, user.id)

@router.put("/enquiries/{enquiry_id}/status")
async def update_enquiry_status(
    enquiry_id: uuid.UUID,
    status: str = Query(..., regex="^(read|replied|spam)$"),
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user)
):
    service = DirectoryService(db)
    return await service.update_enquiry_status(enquiry_id, user.id, status)

@router.post("/businesses/{id}/analyze")
async def analyze_business_website(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user)
):
    service = DirectoryService(db)
    
    # Check ownership
    from app.models.directory import DirectoryListing
    listing = db.query(DirectoryListing).filter(DirectoryListing.id == id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
        
    if listing.claimed_by != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to analyze this listing")
        
    return await service.analyze_website(id)

@router.post("/businesses/{id}/optimize-seo")
async def optimize_business_seo(
    id: uuid.UUID,
    db: Session = Depends(get_db),
    user: Any = Depends(get_current_user)
):
    service = DirectoryService(db)
    
    # Check ownership
    from app.models.directory import DirectoryListing
    listing = db.query(DirectoryListing).filter(DirectoryListing.id == id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
        
    if listing.claimed_by != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to optimize this listing")
        
    return await service.optimize_listing_seo(id)
