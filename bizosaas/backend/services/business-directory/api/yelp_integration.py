"""
Yelp Business Integration API Routes
Provides REST endpoints for Yelp business directory operations
"""

from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_async_session
from ..core.auth import get_current_tenant
from ..services.yelp_business_client import yelp_client, YelpDataMapper
from ..schemas.business import BusinessResponse, BusinessSearchResponse

router = APIRouter(prefix="/yelp", tags=["Yelp Integration"])

# Request Models
class YelpSearchRequest(BaseModel):
    term: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius: Optional[int] = Field(None, ge=1, le=40000)
    categories: Optional[str] = None
    limit: int = Field(default=20, ge=1, le=50)
    offset: int = Field(default=0, ge=0)

class YelpClaimRequest(BaseModel):
    business_id: str
    yelp_business_id: str

# Response Models
class YelpBusinessResponse(BaseModel):
    id: str
    name: str
    alias: Optional[str]
    image_url: Optional[str]
    url: str
    phone: Optional[str]
    rating: Optional[float]
    review_count: int
    price: Optional[str]
    categories: List[str]
    is_closed: bool
    location: Dict[str, Any]
    coordinates: Dict[str, float]
    transactions: List[str]
    distance: Optional[float]

class YelpReviewResponse(BaseModel):
    id: str
    rating: int
    text: str
    time_created: str
    url: str
    user: Dict[str, Any]

class YelpSearchResponse(BaseModel):
    businesses: List[YelpBusinessResponse]
    total: int
    region: Optional[Dict[str, Any]]

# Endpoints

@router.post("/search", response_model=YelpSearchResponse)
async def search_yelp_businesses(
    request: YelpSearchRequest,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Search for businesses on Yelp"""
    try:
        response = await yelp_client.search_businesses(
            term=request.term,
            location=request.location,
            latitude=request.latitude,
            longitude=request.longitude,
            radius=request.radius,
            categories=request.categories,
            limit=request.limit,
            offset=request.offset
        )
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        businesses = []
        for business_data in response.data.get("businesses", []):
            unified_data = YelpDataMapper.map_business_from_search(business_data)
            businesses.append(YelpBusinessResponse(
                id=unified_data["platform_id"],
                name=unified_data["name"],
                alias=unified_data.get("alias"),
                image_url=unified_data.get("image_url"),
                url=unified_data["website_url"],
                phone=unified_data.get("phone"),
                rating=unified_data.get("rating"),
                review_count=unified_data.get("review_count", 0),
                price=unified_data.get("price"),
                categories=unified_data.get("categories", []),
                is_closed=unified_data.get("is_closed", False),
                location=unified_data["location"],
                coordinates=unified_data["coordinates"],
                transactions=unified_data["platform_data"].get("transactions", []),
                distance=unified_data["platform_data"].get("distance")
            ))
        
        return YelpSearchResponse(
            businesses=businesses,
            total=response.data.get("total", len(businesses)),
            region=response.data.get("region")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/business/{yelp_business_id}", response_model=YelpBusinessResponse)
async def get_yelp_business_details(
    yelp_business_id: str,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Get detailed information about a Yelp business"""
    try:
        response = await yelp_client.get_business_details(yelp_business_id)
        
        if not response.success:
            raise HTTPException(status_code=404, detail=response.error)
        
        unified_data = YelpDataMapper.map_business_details(response.data)
        
        return YelpBusinessResponse(
            id=unified_data["platform_id"],
            name=unified_data["name"],
            alias=unified_data.get("alias"),
            image_url=unified_data.get("image_url"),
            url=unified_data["website_url"],
            phone=unified_data.get("phone"),
            rating=unified_data.get("rating"),
            review_count=unified_data.get("review_count", 0),
            price=unified_data.get("price"),
            categories=unified_data.get("categories", []),
            is_closed=unified_data.get("is_closed", False),
            location=unified_data["location"],
            coordinates=unified_data["coordinates"],
            transactions=unified_data["platform_data"].get("transactions", []),
            distance=unified_data["platform_data"].get("distance")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/business/{yelp_business_id}/reviews", response_model=List[YelpReviewResponse])
async def get_yelp_business_reviews(
    yelp_business_id: str,
    locale: str = "en_US",
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Get reviews for a Yelp business"""
    try:
        response = await yelp_client.get_business_reviews(yelp_business_id, locale)
        
        if not response.success:
            raise HTTPException(status_code=404, detail=response.error)
        
        reviews = YelpDataMapper.map_reviews(response.data)
        
        return [
            YelpReviewResponse(
                id=review["review_id"],
                rating=review["rating"],
                text=review["text"],
                time_created=review["time_created"],
                url=review["url"],
                user={
                    "id": review["platform_data"]["user_id"],
                    "name": review["author_name"],
                    "image_url": review["author_profile_photo"],
                    "profile_url": review["platform_data"]["user_profile_url"]
                }
            )
            for review in reviews
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/autocomplete")
async def yelp_autocomplete(
    text: str = Query(..., min_length=2),
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    tenant: Dict = Depends(get_current_tenant)
):
    """Get Yelp autocomplete suggestions"""
    try:
        response = await yelp_client.autocomplete(text, latitude, longitude)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        return response.data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_yelp_categories(
    locale: str = "en_US",
    tenant: Dict = Depends(get_current_tenant)
):
    """Get list of Yelp business categories"""
    try:
        response = await yelp_client.get_categories(locale)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        return response.data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/claim-business")
async def claim_yelp_business(
    request: YelpClaimRequest,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Claim a Yelp business listing (associate with existing business)"""
    try:
        # Get Yelp business details
        response = await yelp_client.get_business_details(request.yelp_business_id)
        
        if not response.success:
            raise HTTPException(status_code=404, detail="Yelp business not found")
        
        # Map Yelp data to unified format
        unified_data = YelpDataMapper.map_business_details(response.data)
        
        # Here you would typically:
        # 1. Validate that the user has permission to claim this business
        # 2. Create or update BusinessPlatform record
        # 3. Store the platform-specific data
        
        # For now, return success with the mapped data
        return {
            "success": True,
            "message": "Yelp business claimed successfully",
            "business_id": request.business_id,
            "yelp_business_id": request.yelp_business_id,
            "yelp_data": unified_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/match-business/{business_id}")
async def find_yelp_matches(
    business_id: str,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Find potential Yelp matches for an existing business"""
    try:
        # This would typically:
        # 1. Get business data from database
        # 2. Search Yelp using business name and location
        # 3. Score potential matches
        # 4. Return ranked list of candidates
        
        # Mock implementation
        return {
            "business_id": business_id,
            "potential_matches": [
                {
                    "yelp_id": "example-business-1",
                    "name": "Example Business",
                    "match_score": 0.95,
                    "confidence": "high",
                    "reasons": ["name_match", "location_match", "phone_match"]
                },
                {
                    "yelp_id": "similar-business-1",
                    "name": "Similar Business",
                    "match_score": 0.72,
                    "confidence": "medium",
                    "reasons": ["location_match", "category_match"]
                }
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Analytics endpoints

@router.get("/analytics/performance")
async def get_yelp_performance_analytics(
    business_id: Optional[str] = None,
    days: int = Query(default=30, ge=1, le=365),
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Get Yelp performance analytics"""
    try:
        # This would typically query actual data from database
        # For now, return mock analytics
        return {
            "business_id": business_id,
            "period_days": days,
            "metrics": {
                "total_reviews": 127,
                "average_rating": 4.3,
                "rating_distribution": {
                    "5_star": 65,
                    "4_star": 34,
                    "3_star": 18,
                    "2_star": 7,
                    "1_star": 3
                },
                "review_velocity": {
                    "reviews_per_month": 8.5,
                    "trend": "increasing"
                },
                "engagement": {
                    "views": 2840,
                    "photos_added": 12,
                    "check_ins": 89
                }
            },
            "comparison": {
                "category_average_rating": 4.1,
                "local_competitor_average": 3.9
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def yelp_health_check():
    """Check Yelp API health status"""
    try:
        # Perform a simple API call to check connectivity
        response = await yelp_client.get_categories()
        
        if response.success:
            return {
                "status": "healthy",
                "api_status": "connected",
                "rate_limit_remaining": response.rate_limit_remaining,
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            return {
                "status": "unhealthy",
                "api_status": "error",
                "error": response.error,
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        return {
            "status": "unhealthy",
            "api_status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }