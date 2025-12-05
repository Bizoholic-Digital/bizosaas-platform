"""
Business Listings API Routes
FastAPI routes for managing business directory listings
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
import logging

from ..core import get_db, get_current_active_user, require_business_read, require_business_write
from ..models import BusinessListing
from ..schemas import (
    BusinessCreateSchema,
    BusinessUpdateSchema,
    BusinessResponseSchema,
    BusinessSearchSchema,
    BusinessClaimSchema,
    BusinessAnalyticsSchema,
    BusinessAnalyticsResponseSchema,
    PaginatedResponseSchema,
    SuccessSchema,
    ErrorSchema
)
from ..services import BusinessService, search_service
from ..core.security import get_tenant_from_request, rate_limit_middleware

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/businesses",
    tags=["Business Listings"],
    dependencies=[Depends(rate_limit_middleware)]
)

# Initialize business service
business_service = BusinessService()


@router.post(
    "/",
    response_model=BusinessResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create Business Listing",
    description="Create a new business listing in the directory"
)
async def create_business(
    business_data: BusinessCreateSchema,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_write)
):
    """Create a new business listing"""
    try:
        tenant_id = await get_tenant_from_request(request)
        
        # Create business
        business = await business_service.create_business(
            tenant_id=tenant_id,
            user_id=current_user.user_id,
            business_data=business_data,
            db=db
        )
        
        # Generate vector embedding in background
        background_tasks.add_task(
            search_service.generate_embedding,
            business
        )
        
        logger.info(f"Created business listing {business.id} for tenant {tenant_id}")
        return BusinessResponseSchema.from_orm(business)
        
    except Exception as e:
        logger.error(f"Error creating business: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create business listing"
        )


@router.get(
    "/",
    response_model=PaginatedResponseSchema,
    summary="Search Business Listings",
    description="Search and filter business listings with pagination"
)
async def search_businesses(
    request: Request,
    query: Optional[str] = Query(None, description="Search query"),
    category_id: Optional[UUID] = Query(None, description="Filter by category"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state"),
    is_verified: Optional[bool] = Query(None, description="Filter by verification status"),
    is_featured: Optional[bool] = Query(None, description="Filter by featured status"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating"),
    latitude: Optional[float] = Query(None, ge=-90, le=90, description="Search center latitude"),
    longitude: Optional[float] = Query(None, ge=-180, le=180, description="Search center longitude"),
    radius: Optional[float] = Query(None, ge=0, le=100, description="Search radius in km"),
    search_type: str = Query("hybrid", regex="^(semantic|keyword|hybrid)$", description="Search type"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_read)
):
    """Search business listings with filters"""
    try:
        tenant_id = await get_tenant_from_request(request)
        
        # Build search parameters
        search_params = BusinessSearchSchema(
            query=query,
            category_id=category_id,
            city=city,
            state=state,
            is_verified=is_verified,
            is_featured=is_featured,
            min_rating=min_rating,
            latitude=latitude,
            longitude=longitude,
            radius=radius,
            search_type=search_type,
            page=page,
            size=size,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # Track search query
        if query:
            await search_service.track_search_query(
                query=query,
                tenant_id=tenant_id,
                user_id=current_user.user_id
            )
        
        # Perform search
        results = await business_service.search_businesses(
            tenant_id=tenant_id,
            search_params=search_params,
            db=db
        )
        
        return results
        
    except Exception as e:
        logger.error(f"Error searching businesses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search business listings"
        )


@router.get(
    "/{business_id}",
    response_model=BusinessResponseSchema,
    summary="Get Business Listing",
    description="Get a specific business listing by ID"
)
async def get_business(
    business_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_read)
):
    """Get a business listing by ID"""
    try:
        tenant_id = await get_tenant_from_request(request)
        
        business = await business_service.get_business(
            business_id=str(business_id),
            tenant_id=tenant_id,
            db=db,
            include_relations=True
        )
        
        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business listing not found"
            )
        
        return BusinessResponseSchema.from_orm(business)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching business {business_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch business listing"
        )


@router.put(
    "/{business_id}",
    response_model=BusinessResponseSchema,
    summary="Update Business Listing",
    description="Update an existing business listing"
)
async def update_business(
    business_id: UUID,
    update_data: BusinessUpdateSchema,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_write)
):
    """Update a business listing"""
    try:
        tenant_id = await get_tenant_from_request(request)
        
        business = await business_service.update_business(
            business_id=str(business_id),
            tenant_id=tenant_id,
            user_id=current_user.user_id,
            update_data=update_data,
            db=db
        )
        
        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business listing not found"
            )
        
        # Update vector embedding in background if content changed
        search_fields = ['name', 'description', 'short_description', 'city', 'state']
        if any(getattr(update_data, field, None) for field in search_fields):
            background_tasks.add_task(
                search_service.generate_embedding,
                business
            )
        
        logger.info(f"Updated business listing {business_id}")
        return BusinessResponseSchema.from_orm(business)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating business {business_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update business listing"
        )


@router.delete(
    "/{business_id}",
    response_model=SuccessSchema,
    summary="Delete Business Listing",
    description="Delete a business listing (soft delete by default)"
)
async def delete_business(
    business_id: UUID,
    request: Request,
    soft_delete: bool = Query(True, description="Perform soft delete"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_write)
):
    """Delete a business listing"""
    try:
        tenant_id = await get_tenant_from_request(request)
        
        success = await business_service.delete_business(
            business_id=str(business_id),
            tenant_id=tenant_id,
            user_id=current_user.user_id,
            db=db,
            soft_delete=soft_delete
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business listing not found"
            )
        
        logger.info(f"Deleted business listing {business_id}")
        return SuccessSchema(
            message="Business listing deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting business {business_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete business listing"
        )


@router.post(
    "/{business_id}/claim",
    response_model=SuccessSchema,
    summary="Claim Business Listing",
    description="Claim ownership of a business listing"
)
async def claim_business(
    business_id: UUID,
    claim_data: BusinessClaimSchema,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_write)
):
    """Claim a business listing"""
    try:
        tenant_id = await get_tenant_from_request(request)
        
        success = await business_service.claim_business(
            business_id=str(business_id),
            tenant_id=tenant_id,
            user_id=current_user.user_id,
            db=db
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Business not found or already claimed"
            )
        
        logger.info(f"Business {business_id} claimed by user {current_user.user_id}")
        return SuccessSchema(
            message="Business listing claimed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error claiming business {business_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to claim business listing"
        )


@router.get(
    "/{business_id}/analytics",
    response_model=BusinessAnalyticsResponseSchema,
    summary="Get Business Analytics",
    description="Get analytics data for a business listing"
)
async def get_business_analytics(
    business_id: UUID,
    analytics_params: BusinessAnalyticsSchema = Depends(),
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_read)
):
    """Get business analytics data"""
    try:
        tenant_id = await get_tenant_from_request(request)
        
        analytics_data = await business_service.get_business_analytics(
            business_id=str(business_id),
            tenant_id=tenant_id,
            date_from=analytics_params.date_from,
            date_to=analytics_params.date_to,
            db=db
        )
        
        return BusinessAnalyticsResponseSchema(**analytics_data)
        
    except Exception as e:
        logger.error(f"Error fetching analytics for business {business_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch business analytics"
        )


@router.get(
    "/suggestions/autocomplete",
    response_model=List[dict],
    summary="Business Suggestions",
    description="Get business suggestions for autocomplete"
)
async def get_business_suggestions(
    request: Request,
    query: str = Query(min_length=2, description="Search query for suggestions"),
    limit: int = Query(5, ge=1, le=20, description="Number of suggestions"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_read)
):
    """Get business suggestions for autocomplete"""
    try:
        tenant_id = await get_tenant_from_request(request)
        
        suggestions = await search_service.suggest_businesses(
            query=query,
            tenant_id=tenant_id,
            limit=limit,
            db=db
        )
        
        return suggestions
        
    except Exception as e:
        logger.error(f"Error getting business suggestions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get business suggestions"
        )


@router.get(
    "/trending/searches",
    response_model=List[str],
    summary="Trending Searches",
    description="Get trending search queries"
)
async def get_trending_searches(
    request: Request,
    limit: int = Query(10, ge=1, le=50, description="Number of trending searches"),
    current_user = Depends(require_business_read)
):
    """Get trending search queries"""
    try:
        tenant_id = await get_tenant_from_request(request)
        
        trending = await search_service.get_trending_searches(
            tenant_id=tenant_id,
            limit=limit
        )
        
        return trending
        
    except Exception as e:
        logger.error(f"Error getting trending searches: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get trending searches"
        )


# Error handlers
@router.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle validation errors"""
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(exc)
    )


@router.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception in businesses API: {exc}")
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="An unexpected error occurred"
    )