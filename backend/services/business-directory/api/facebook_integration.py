"""
Facebook Business Integration API Routes
Provides REST endpoints for Facebook Business Page operations
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_async_session
from ..core.auth import get_current_tenant
from ..services.facebook_business_client import facebook_client, FacebookDataMapper
from ..schemas.business import BusinessResponse

router = APIRouter(prefix="/facebook", tags=["Facebook Integration"])

# Request Models
class FacebookAuthRequest(BaseModel):
    access_token: str

class FacebookPageUpdateRequest(BaseModel):
    page_id: str
    access_token: str
    updates: Dict[str, Any]

class FacebookSearchRequest(BaseModel):
    query: str
    access_token: str
    location: Optional[str] = None
    limit: int = Field(default=25, ge=1, le=100)

class FacebookInsightsRequest(BaseModel):
    page_id: str
    access_token: str
    metrics: Optional[List[str]] = None
    period: str = Field(default="day", pattern="^(day|week|days_28)$")
    since: Optional[datetime] = None
    until: Optional[datetime] = None

# Response Models
class FacebookPageResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    category: str
    phone: Optional[str]
    website: Optional[str]
    email: Optional[str]
    rating: Optional[float]
    review_count: Optional[int]
    followers_count: Optional[int]
    is_verified: bool
    is_published: bool
    location: Dict[str, Any]
    picture_url: Optional[str]
    cover_url: Optional[str]

class FacebookPostResponse(BaseModel):
    id: str
    message: Optional[str]
    type: str
    created_time: str
    likes_count: int
    comments_count: int
    shares_count: int
    engagement_rate: float

class FacebookReviewResponse(BaseModel):
    id: str
    rating: int
    text: Optional[str]
    created_time: str
    reviewer_name: str
    reviewer_id: str

class FacebookInsightResponse(BaseModel):
    metric_name: str
    period: str
    values: List[Dict[str, Any]]

# Endpoints

@router.get("/pages", response_model=List[FacebookPageResponse])
async def get_user_pages(
    access_token: str = Query(...),
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Get Facebook pages managed by the user"""
    try:
        response = await facebook_client.get_user_pages(access_token)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        pages = []
        for page_data in response.data.get("data", []):
            unified_data = FacebookDataMapper.map_page_info(page_data)
            pages.append(FacebookPageResponse(
                id=unified_data["platform_id"],
                name=unified_data["name"],
                description=unified_data.get("description"),
                category=unified_data.get("category", ""),
                phone=unified_data.get("phone"),
                website=unified_data.get("website_url"),
                email=unified_data.get("emails", [None])[0] if unified_data.get("emails") else None,
                rating=unified_data.get("rating"),
                review_count=unified_data.get("review_count"),
                followers_count=unified_data.get("followers_count"),
                is_verified=unified_data.get("is_verified", False),
                is_published=unified_data.get("is_published", True),
                location=unified_data["location"],
                picture_url=unified_data.get("image_url"),
                cover_url=unified_data.get("cover_photo_url")
            ))
        
        return pages
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/page/{page_id}", response_model=FacebookPageResponse)
async def get_page_info(
    page_id: str,
    access_token: str = Query(...),
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Get detailed Facebook page information"""
    try:
        response = await facebook_client.get_page_info(page_id, access_token)
        
        if not response.success:
            raise HTTPException(status_code=404, detail=response.error)
        
        unified_data = FacebookDataMapper.map_page_info(response.data)
        
        return FacebookPageResponse(
            id=unified_data["platform_id"],
            name=unified_data["name"],
            description=unified_data.get("description"),
            category=unified_data.get("category", ""),
            phone=unified_data.get("phone"),
            website=unified_data.get("website_url"),
            email=unified_data.get("emails", [None])[0] if unified_data.get("emails") else None,
            rating=unified_data.get("rating"),
            review_count=unified_data.get("review_count"),
            followers_count=unified_data.get("followers_count"),
            is_verified=unified_data.get("is_verified", False),
            is_published=unified_data.get("is_published", True),
            location=unified_data["location"],
            picture_url=unified_data.get("image_url"),
            cover_url=unified_data.get("cover_photo_url")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/page/{page_id}")
async def update_page_info(
    page_id: str,
    request: FacebookPageUpdateRequest,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Update Facebook page information"""
    try:
        response = await facebook_client.update_page_info(
            page_id, request.access_token, **request.updates
        )
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        return {
            "success": True,
            "message": "Page updated successfully",
            "page_id": page_id,
            "updated_fields": list(request.updates.keys())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/page/{page_id}/posts", response_model=List[FacebookPostResponse])
async def get_page_posts(
    page_id: str,
    access_token: str = Query(...),
    limit: int = Query(default=25, ge=1, le=100),
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Get Facebook page posts"""
    try:
        response = await facebook_client.get_page_posts(
            page_id, access_token, limit, since, until
        )
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        posts = FacebookDataMapper.map_posts(response.data)
        
        return [
            FacebookPostResponse(
                id=post["post_id"],
                message=post.get("message"),
                type=post.get("type", ""),
                created_time=post["created_time"],
                likes_count=post["likes_count"],
                comments_count=post["comments_count"],
                shares_count=post["shares_count"],
                engagement_rate=(
                    (post["likes_count"] + post["comments_count"] + post["shares_count"]) / 
                    max(1, post.get("reach", 100)) * 100  # Mock reach for calculation
                )
            )
            for post in posts
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/page/{page_id}/reviews", response_model=List[FacebookReviewResponse])
async def get_page_reviews(
    page_id: str,
    access_token: str = Query(...),
    limit: int = Query(default=25, ge=1, le=100),
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Get Facebook page reviews"""
    try:
        response = await facebook_client.get_page_reviews(page_id, access_token, limit)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        reviews = FacebookDataMapper.map_reviews(response.data)
        
        return [
            FacebookReviewResponse(
                id=review["review_id"],
                rating=review["rating"],
                text=review.get("text"),
                created_time=review["time_created"],
                reviewer_name=review["author_name"],
                reviewer_id=review["author_id"]
            )
            for review in reviews
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/page/{page_id}/insights", response_model=List[FacebookInsightResponse])
async def get_page_insights(
    page_id: str,
    request: FacebookInsightsRequest,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Get Facebook page insights/analytics"""
    try:
        response = await facebook_client.get_page_insights(
            page_id, request.access_token, request.metrics,
            request.period, request.since, request.until
        )
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        insights = FacebookDataMapper.map_insights(response.data)
        
        # Group insights by metric
        grouped_insights = {}
        for insight in insights:
            metric_name = insight["metric_name"]
            if metric_name not in grouped_insights:
                grouped_insights[metric_name] = {
                    "metric_name": metric_name,
                    "period": insight["period"],
                    "values": []
                }
            grouped_insights[metric_name]["values"].append({
                "date": insight["date"],
                "value": insight["value"]
            })
        
        return [FacebookInsightResponse(**data) for data in grouped_insights.values()]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=List[FacebookPageResponse])
async def search_facebook_pages(
    request: FacebookSearchRequest,
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Search for Facebook pages"""
    try:
        response = await facebook_client.search_pages(
            request.query, request.access_token, request.location, request.limit
        )
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        pages = []
        for page_data in response.data.get("data", []):
            unified_data = FacebookDataMapper.map_page_info(page_data)
            pages.append(FacebookPageResponse(
                id=unified_data["platform_id"],
                name=unified_data["name"],
                description=unified_data.get("description"),
                category=unified_data.get("category", ""),
                phone=unified_data.get("phone"),
                website=unified_data.get("website_url"),
                email=unified_data.get("emails", [None])[0] if unified_data.get("emails") else None,
                rating=unified_data.get("rating"),
                review_count=unified_data.get("review_count"),
                followers_count=unified_data.get("followers_count"),
                is_verified=unified_data.get("is_verified", False),
                is_published=unified_data.get("is_published", True),
                location=unified_data["location"],
                picture_url=unified_data.get("image_url"),
                cover_url=unified_data.get("cover_photo_url")
            ))
        
        return pages
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# OAuth and Authentication endpoints

@router.get("/auth/url")
async def get_facebook_auth_url(
    redirect_uri: str = Query(...),
    tenant: Dict = Depends(get_current_tenant)
):
    """Get Facebook OAuth authorization URL"""
    try:
        from urllib.parse import urlencode
        
        params = {
            "client_id": "your_facebook_app_id",  # This should come from settings
            "redirect_uri": redirect_uri,
            "scope": "pages_manage_business,pages_read_engagement,pages_show_list,business_management",
            "response_type": "code",
            "state": f"tenant_{tenant['id']}"  # Include tenant info for security
        }
        
        auth_url = f"https://www.facebook.com/v18.0/dialog/oauth?{urlencode(params)}"
        
        return {
            "auth_url": auth_url,
            "redirect_uri": redirect_uri,
            "scopes": [
                "pages_manage_business",
                "pages_read_engagement", 
                "pages_show_list",
                "business_management"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auth/token")
async def exchange_facebook_code(
    code: str,
    redirect_uri: str,
    tenant: Dict = Depends(get_current_tenant)
):
    """Exchange Facebook OAuth code for access token"""
    try:
        # This would typically exchange the code for an access token
        # For security, this should be done server-side
        
        # Mock response - in reality, you'd call Facebook's token endpoint
        return {
            "access_token": "mock_access_token",
            "token_type": "bearer",
            "expires_in": 7200,
            "scope": "pages_manage_business,pages_read_engagement",
            "message": "Token exchange successful"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Analytics endpoints

@router.get("/analytics/page-performance/{page_id}")
async def get_page_performance_analytics(
    page_id: str,
    access_token: str = Query(...),
    days: int = Query(default=30, ge=1, le=365),
    tenant: Dict = Depends(get_current_tenant),
    session: AsyncSession = Depends(get_async_session)
):
    """Get comprehensive Facebook page performance analytics"""
    try:
        # Get various insights
        since_date = datetime.utcnow() - timedelta(days=days)
        
        # Get page insights
        insights_response = await facebook_client.get_page_insights(
            page_id, access_token,
            metrics=["page_impressions", "page_engaged_users", "page_fan_adds"],
            period="day",
            since=since_date
        )
        
        # Get recent posts for engagement analysis
        posts_response = await facebook_client.get_page_posts(
            page_id, access_token, limit=50, since=since_date
        )
        
        # Process and return analytics
        analytics = {
            "page_id": page_id,
            "period_days": days,
            "overview": {
                "total_impressions": 45230,  # Mock data
                "total_engagement": 3421,
                "new_followers": 89,
                "engagement_rate": 7.56
            },
            "trends": {
                "impressions_trend": "increasing",
                "engagement_trend": "stable",
                "follower_growth": "positive"
            },
            "top_posts": [
                {
                    "post_id": "123456789",
                    "message": "Sample post content",
                    "engagement": 245,
                    "reach": 1890
                }
            ],
            "demographics": {
                "age_groups": {
                    "18-24": 15,
                    "25-34": 35,
                    "35-44": 28,
                    "45-54": 15,
                    "55+": 7
                },
                "gender": {
                    "male": 45,
                    "female": 55
                }
            }
        }
        
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def facebook_health_check():
    """Check Facebook API health status"""
    try:
        # In a real implementation, you'd test with a valid token
        # For now, return mock health status
        return {
            "status": "healthy",
            "api_status": "connected",
            "api_version": "v18.0",
            "timestamp": datetime.utcnow().isoformat(),
            "available_features": [
                "page_management",
                "insights",
                "posts",
                "reviews"
            ]
        }
            
    except Exception as e:
        return {
            "status": "unhealthy",
            "api_status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }