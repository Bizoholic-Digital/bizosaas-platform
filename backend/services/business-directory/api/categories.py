"""
Business Categories API Routes
FastAPI routes for managing business directory categories
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
import logging

from ..core import get_db, require_business_read, require_business_write, require_business_admin
from ..schemas import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
    SuccessSchema
)
from ..services import BusinessService
from ..core.security import get_tenant_from_request, rate_limit_middleware

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/categories",
    tags=["Business Categories"],
    dependencies=[Depends(rate_limit_middleware)]
)

# Initialize business service
business_service = BusinessService()


@router.get(
    "/",
    response_model=List[CategoryResponseSchema],
    summary="List Business Categories",
    description="Get business categories with optional parent filtering"
)
async def list_categories(
    request: Request,
    parent_id: Optional[UUID] = Query(None, description="Parent category ID (null for root categories)"),
    include_inactive: bool = Query(False, description="Include inactive categories"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_business_read)
):
    """List business categories"""
    try:
        tenant_id = await get_tenant_from_request(request)
        
        categories = await business_service.get_categories(
            tenant_id=tenant_id,
            parent_id=str(parent_id) if parent_id else None,
            include_inactive=include_inactive,
            db=db
        )
        
        return [CategoryResponseSchema.from_orm(category) for category in categories]
        
    except Exception as e:
        logger.error(f"Error listing categories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch categories"
        )