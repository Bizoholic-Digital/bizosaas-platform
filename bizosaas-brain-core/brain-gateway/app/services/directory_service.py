from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.models.directory import DirectoryListing, DirectoryAnalytics, DirectoryClaimRequest
from typing import List, Optional, Dict, Any
from datetime import datetime, date

class DirectoryService:
    def __init__(self, db: Session):
        self.db = db

    async def search(
        self,
        query: Optional[str] = None,
        location: Optional[str] = None,
        category: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> Dict[str, Any]:
        """Search directory listings with filters"""
        q = self.db.query(DirectoryListing).filter(DirectoryListing.status == 'active')

        if query:
            search_filter = or_(
                DirectoryListing.business_name.ilike(f"%{query}%"),
                DirectoryListing.description.ilike(f"%{query}%"),
                DirectoryListing.category.ilike(f"%{query}%")
            )
            q = q.filter(search_filter)

        if location:
            q = q.filter(DirectoryListing.city.ilike(f"%{location}%"))

        if category:
            q = q.filter(DirectoryListing.category == category)

        total = q.count()
        listings = q.order_by(desc(DirectoryListing.created_at)).offset((page - 1) * limit).limit(limit).all()

        return {
            "businesses": listings,
            "total": total,
            "page": page,
            "limit": limit
        }

    async def get_by_slug(self, slug: str) -> Optional[DirectoryListing]:
        """Get listing by business slug"""
        return self.db.query(DirectoryListing).filter(DirectoryListing.business_slug == slug).first()

    async def get_user_listings(self, user_id: UUID) -> List[DirectoryListing]:
        """Get all listings claimed by a user"""
        return self.db.query(DirectoryListing).filter(
            DirectoryListing.claimed == True,
            DirectoryListing.claimed_by == user_id
        ).order_by(desc(DirectoryListing.created_at)).all()

    async def create_from_places_data(self, data: Dict[str, Any], user_id: Optional[UUID] = None) -> DirectoryListing:
        """Create a listing from Google Places data"""
        slug = data.get("slug")
        if not slug:
            # Simple fallback slug generation
            name = data.get("name", "unknown")
            location = data.get("location", "")
            import re
            slug = re.sub(r'[^a-zA-Z0-9]', '-', f"{name} {location}".lower())
            slug = re.sub(r'-+', '-', slug).strip('-')

        # Check for existing
        existing = await self.get_by_slug(slug)
        if existing:
            return existing

        listing = DirectoryListing(
            business_slug=slug,
            business_name=data.get("name"),
            google_place_id=data.get("google_place_id"),
            address=data.get("location"),
            city=data.get("city"),
            state=data.get("state"),
            country=data.get("country"),
            postal_code=data.get("postal_code"),
            phone=data.get("phone"),
            website=data.get("website"),
            category=data.get("category"),
            google_data=data.get("google_data"),
            google_rating=data.get("google_rating"),
            google_reviews_count=data.get("google_reviews_count"),
            status='active',
            visibility='public'
        )

        if user_id:
            listing.claimed_by = user_id
            listing.claimed = True
            listing.claimed_at = datetime.utcnow()
            listing.verification_status = 'verified'

        self.db.add(listing)
        self.db.commit()
        self.db.refresh(listing)
        return listing

    async def log_view(self, listing_id: UUID):
        """Log a page view for a listing"""
        today = date.today()
        analytics = self.db.query(DirectoryAnalytics).filter(
            DirectoryAnalytics.listing_id == listing_id,
            DirectoryAnalytics.date == today
        ).first()

        if not analytics:
            analytics = DirectoryAnalytics(
                listing_id=listing_id,
                date=today,
                page_views=1,
                unique_visitors=1
            )
            self.db.add(analytics)
        else:
            analytics.page_views += 1
            # In a real app, unique visitors would check sessions/IP
            analytics.unique_visitors += 1 

        self.db.commit()

    async def log_click(self, listing_id: UUID, click_type: str):
        """Log engagement clicks (phone, website, directions)"""
        today = date.today()
        analytics = self.db.query(DirectoryAnalytics).filter(
            DirectoryAnalytics.listing_id == listing_id,
            DirectoryAnalytics.date == today
        ).first()

        if not analytics:
            analytics = DirectoryAnalytics(listing_id=listing_id, date=today)
            self.db.add(analytics)

        if click_type == 'phone':
            analytics.phone_clicks += 1
        elif click_type == 'website':
            analytics.website_clicks += 1
        elif click_type == 'directions':
            analytics.direction_clicks += 1

        self.db.commit()

    async def create_claim_request(self, listing_id: UUID, user_id: UUID, method: str, data: Dict[str, Any]) -> DirectoryClaimRequest:
        """Create a new claim request for a listing"""
        request = DirectoryClaimRequest(
            listing_id=listing_id,
            user_id=user_id,
            verification_method=method,
            verification_data=data,
            status='pending'
        )
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        return request

    async def get_directory_stats(self) -> Dict[str, Any]:
        """Get high-level stats for directory management"""
        from sqlalchemy import func
        total_listings = self.db.query(DirectoryListing).count()
        claimed_listings = self.db.query(DirectoryListing).filter(DirectoryListing.claimed == True).count()
        pending_claims = self.db.query(DirectoryClaimRequest).filter(DirectoryClaimRequest.status == 'pending').count()
        
        # Total views across all time
        total_views = self.db.query(func.sum(DirectoryAnalytics.page_views)).scalar() or 0
        
        return {
            "total_listings": total_listings,
            "claimed_listings": claimed_listings,
            "pending_claims": pending_claims,
            "total_views": int(total_views)
        }

    async def update_listing(self, listing_id: UUID, data: Dict[str, Any]) -> DirectoryListing:
        """Update an existing listing"""
        listing = self.db.query(DirectoryListing).filter(DirectoryListing.id == listing_id).first()
        if not listing:
            raise ValueError("Listing not found")
        
        for key, value in data.items():
            if hasattr(listing, key):
                setattr(listing, key, value)
        
        listing.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(listing)
        return listing

    async def create_enquiry(self, listing_id: UUID, data: dict):
        from app.models.directory import DirectoryEnquiry
        from fastapi import HTTPException
        
        enquiry = DirectoryEnquiry(
            listing_id=listing_id,
            name=data["name"],
            email=data["email"],
            phone=data.get("phone"),
            subject=data.get("subject"),
            message=data["message"]
        )
        self.db.add(enquiry)
        self.db.commit()
        self.db.refresh(enquiry)
        
        # TODO: Trigger automation workflow (email notification, AI enrichment)
        
        return enquiry

    async def get_enquiries(self, listing_id: UUID, user_id: UUID):
        from app.models.directory import DirectoryListing, DirectoryEnquiry
        from fastapi import HTTPException
        
        # Verify ownership
        listing = self.db.query(DirectoryListing).filter(
            DirectoryListing.id == listing_id,
            DirectoryListing.claimed == True,
            DirectoryListing.claimed_by == user_id
        ).first()
        
        if not listing:
            raise HTTPException(status_code=403, detail="Not authorized to view enquiries for this listing")
            
        return self.db.query(DirectoryEnquiry).filter(
            DirectoryEnquiry.listing_id == listing_id
        ).order_by(desc(DirectoryEnquiry.created_at)).all()

    async def update_enquiry_status(self, enquiry_id: UUID, user_id: UUID, status: str):
        from app.models.directory import DirectoryListing, DirectoryEnquiry
        from fastapi import HTTPException
        
        enquiry = self.db.query(DirectoryEnquiry).filter(DirectoryEnquiry.id == enquiry_id).first()
        if not enquiry:
            raise HTTPException(status_code=404, detail="Enquiry not found")
            
        # Verify ownership of the listing
        listing = self.db.query(DirectoryListing).filter(
            DirectoryListing.id == enquiry.listing_id,
            DirectoryListing.claimed == True,
            DirectoryListing.claimed_by == user_id
        ).first()
        
        if not listing:
            raise HTTPException(status_code=403, detail="Not authorized to update this enquiry")
            
        enquiry.status = status
        self.db.commit()
        self.db.refresh(enquiry)
        return enquiry

    async def get_events(self, listing_id: uuid.UUID):
        from app.models.directory import DirectoryEvent
        return self.db.query(DirectoryEvent).filter(
            DirectoryEvent.listing_id == listing_id,
            DirectoryEvent.status != 'cancelled'
        ).order_by(DirectoryEvent.start_date.asc()).all()

    async def create_event(self, listing_id: uuid.UUID, user_id: uuid.UUID, data: dict):
        from app.models.directory import DirectoryListing, DirectoryEvent
        from fastapi import HTTPException
        
        # Verify ownership
        listing = self.db.query(DirectoryListing).filter(
            DirectoryListing.id == listing_id,
            DirectoryListing.claimed == True,
            DirectoryListing.claimed_by == user_id
        ).first()
        
        if not listing:
            raise HTTPException(status_code=403, detail="Not authorized to add events to this listing")
            
        event = DirectoryEvent(
            listing_id=listing_id,
            **data
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    async def get_coupons(self, listing_id: uuid.UUID):
        from app.models.directory import DirectoryCoupon
        return self.db.query(DirectoryCoupon).filter(
            DirectoryCoupon.listing_id == listing_id,
            DirectoryCoupon.status == 'active'
        ).order_by(DirectoryCoupon.created_at.desc()).all()

    async def create_coupon(self, listing_id: uuid.UUID, user_id: uuid.UUID, data: dict):
        from app.models.directory import DirectoryListing, DirectoryCoupon
        from fastapi import HTTPException
        
        # Verify ownership
        listing = self.db.query(DirectoryListing).filter(
            DirectoryListing.id == listing_id,
            DirectoryListing.claimed == True,
            DirectoryListing.claimed_by == user_id
        ).first()
        
        if not listing:
            raise HTTPException(status_code=403, detail="Not authorized to add coupons to this listing")
            
        coupon = DirectoryCoupon(
            listing_id=listing_id,
            **data
        )
        self.db.add(coupon)
        self.db.commit()
        self.db.refresh(coupon)
        return coupon
