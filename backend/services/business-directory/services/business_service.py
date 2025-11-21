"""
Business Service Layer
Core business logic for managing business directory operations
"""

from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, text
from sqlalchemy.orm import selectinload, joinedload
from uuid import UUID
import logging
import json
from datetime import datetime, timedelta

from ..models import (
    BusinessListing,
    BusinessCategory, 
    BusinessReview,
    BusinessEvent,
    BusinessProduct,
    BusinessCoupon,
    BusinessAnalytics
)
from ..schemas import (
    BusinessCreateSchema,
    BusinessUpdateSchema,
    BusinessSearchSchema,
    BusinessResponseSchema,
    PaginatedResponseSchema
)
from ..core.database import get_tenant_db
from .search_service import SearchService

# Configure logging
logger = logging.getLogger(__name__)


class BusinessService:
    """
    Service class for business directory operations
    """
    
    def __init__(self):
        self.search_service = SearchService()
    
    # ============================================================================
    # Business Listing Operations
    # ============================================================================
    
    async def create_business(
        self,
        tenant_id: str,
        user_id: str,
        business_data: BusinessCreateSchema,
        db: AsyncSession
    ) -> BusinessListing:
        """Create a new business listing"""
        try:
            # Set tenant context
            await db.execute(
                text("SELECT set_config('app.current_tenant_id', :tenant_id, false)"),
                {"tenant_id": tenant_id}
            )
            
            # Create business instance
            business = BusinessListing(
                tenant_id=UUID(tenant_id),
                created_by=UUID(user_id),
                **business_data.dict(exclude_unset=True)
            )
            
            # Generate slug if not provided
            if not business.slug:
                business.slug = await self._generate_unique_slug(business.name, db)
            
            # Update search content for vector embedding
            business.update_search_content()
            
            # Add to database
            db.add(business)
            await db.flush()
            
            # Generate vector embedding asynchronously
            await self.search_service.generate_embedding(business)
            
            await db.commit()
            await db.refresh(business)
            
            logger.info(f"Created business listing: {business.id} for tenant: {tenant_id}")
            return business
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating business: {e}")
            raise
    
    async def get_business(
        self,
        business_id: str,
        tenant_id: str,
        db: AsyncSession,
        include_relations: bool = True
    ) -> Optional[BusinessListing]:
        """Get a business listing by ID"""
        try:
            # Set tenant context
            await db.execute(
                text("SELECT set_config('app.current_tenant_id', :tenant_id, false)"),
                {"tenant_id": tenant_id}
            )
            
            # Build query with optional relations
            query = select(BusinessListing).where(
                and_(
                    BusinessListing.id == UUID(business_id),
                    BusinessListing.tenant_id == UUID(tenant_id),
                    BusinessListing.is_deleted == False
                )
            )
            
            if include_relations:
                query = query.options(
                    selectinload(BusinessListing.category),
                    selectinload(BusinessListing.reviews),
                    selectinload(BusinessListing.events),
                    selectinload(BusinessListing.products),
                    selectinload(BusinessListing.coupons)
                )
            
            result = await db.execute(query)
            business = result.scalar_one_or_none()
            
            if business:
                # Increment view count
                business.increment_view_count()
                await db.commit()
            
            return business
            
        except Exception as e:
            logger.error(f"Error fetching business {business_id}: {e}")
            raise
    
    async def update_business(
        self,
        business_id: str,
        tenant_id: str,
        user_id: str,
        update_data: BusinessUpdateSchema,
        db: AsyncSession
    ) -> Optional[BusinessListing]:
        """Update a business listing"""
        try:
            # Get existing business
            business = await self.get_business(business_id, tenant_id, db, include_relations=False)
            if not business:
                return None
            
            # Update fields
            update_dict = update_data.dict(exclude_unset=True, exclude_none=True)
            for field, value in update_dict.items():
                setattr(business, field, value)
            
            # Update audit fields
            business.updated_by = UUID(user_id)
            
            # Update search content if relevant fields changed
            search_fields = ['name', 'description', 'short_description', 'city', 'state']
            if any(field in update_dict for field in search_fields):
                business.update_search_content()
                # Regenerate vector embedding
                await self.search_service.generate_embedding(business)
            
            await db.commit()
            await db.refresh(business)
            
            logger.info(f"Updated business listing: {business.id}")
            return business
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating business {business_id}: {e}")
            raise
    
    async def delete_business(
        self,
        business_id: str,
        tenant_id: str,
        user_id: str,
        db: AsyncSession,
        soft_delete: bool = True
    ) -> bool:
        """Delete a business listing"""
        try:
            business = await self.get_business(business_id, tenant_id, db, include_relations=False)
            if not business:
                return False
            
            if soft_delete:
                # Soft delete
                business.soft_delete()
                business.updated_by = UUID(user_id)
            else:
                # Hard delete
                await db.delete(business)
            
            await db.commit()
            
            logger.info(f"Deleted business listing: {business_id}")
            return True
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error deleting business {business_id}: {e}")
            raise
    
    async def search_businesses(
        self,
        tenant_id: str,
        search_params: BusinessSearchSchema,
        db: AsyncSession
    ) -> PaginatedResponseSchema:
        """Search and filter business listings"""
        try:
            # Set tenant context
            await db.execute(
                text("SELECT set_config('app.current_tenant_id', :tenant_id, false)"),
                {"tenant_id": tenant_id}
            )
            
            # Start with base query
            query = select(BusinessListing).where(
                and_(
                    BusinessListing.tenant_id == UUID(tenant_id),
                    BusinessListing.is_deleted == False,
                    BusinessListing.status == "active"
                )
            )
            
            # Apply filters
            query = await self._apply_business_filters(query, search_params)
            
            # Apply text/semantic search
            if search_params.query:
                if search_params.search_type in ["semantic", "hybrid"]:
                    # Use vector search
                    businesses = await self.search_service.semantic_search(\n                        search_params.query,\n                        tenant_id,\n                        limit=search_params.size,\n                        filters=search_params.dict(),\n                        db=db\n                    )\n                    # Convert to response format\n                    total = len(businesses)\n                    items = businesses[search_params.offset:search_params.offset + search_params.size]\n                else:\n                    # Use text search\n                    query = self._apply_text_search(query, search_params.query)\n                    \n                    # Get total count\n                    count_query = select(func.count()).select_from(query.subquery())\n                    total_result = await db.execute(count_query)\n                    total = total_result.scalar()\n                    \n                    # Apply pagination and sorting\n                    query = self._apply_sorting(query, search_params.sort_by, search_params.sort_order)\n                    query = query.offset(search_params.offset).limit(search_params.size)\n                    \n                    # Execute query\n                    result = await db.execute(query)\n                    items = result.scalars().all()\n            else:\n                # No search query, just filtering\n                # Get total count\n                count_query = select(func.count()).select_from(query.subquery())\n                total_result = await db.execute(count_query)\n                total = total_result.scalar()\n                \n                # Apply pagination and sorting\n                query = self._apply_sorting(query, search_params.sort_by, search_params.sort_order)\n                query = query.offset(search_params.offset).limit(search_params.size)\n                \n                # Execute query\n                result = await db.execute(query)\n                items = result.scalars().all()\n            \n            # Calculate pagination info\n            pages = (total + search_params.size - 1) // search_params.size\n            has_next = search_params.page < pages\n            has_prev = search_params.page > 1\n            \n            return PaginatedResponseSchema(\n                items=[BusinessResponseSchema.from_orm(item) for item in items],\n                total=total,\n                page=search_params.page,\n                size=search_params.size,\n                pages=pages,\n                has_next=has_next,\n                has_prev=has_prev\n            )\n            \n        except Exception as e:\n            logger.error(f\"Error searching businesses: {e}\")\n            raise\n    \n    async def claim_business(\n        self,\n        business_id: str,\n        tenant_id: str,\n        user_id: str,\n        db: AsyncSession\n    ) -> bool:\n        \"\"\"Claim a business listing\"\"\"\n        try:\n            business = await self.get_business(business_id, tenant_id, db, include_relations=False)\n            if not business or business.is_claimed:\n                return False\n            \n            business.claim_business(user_id)\n            await db.commit()\n            \n            logger.info(f\"Business {business_id} claimed by user {user_id}\")\n            return True\n            \n        except Exception as e:\n            await db.rollback()\n            logger.error(f\"Error claiming business {business_id}: {e}\")\n            raise\n    \n    # ============================================================================\n    # Business Categories\n    # ============================================================================\n    \n    async def get_categories(\n        self,\n        tenant_id: str,\n        parent_id: Optional[str] = None,\n        include_inactive: bool = False,\n        db: AsyncSession\n    ) -> List[BusinessCategory]:\n        \"\"\"Get business categories\"\"\"\n        try:\n            # Set tenant context\n            await db.execute(\n                text(\"SELECT set_config('app.current_tenant_id', :tenant_id, false)\"),\n                {\"tenant_id\": tenant_id}\n            )\n            \n            query = select(BusinessCategory).where(\n                and_(\n                    BusinessCategory.tenant_id == UUID(tenant_id),\n                    BusinessCategory.is_deleted == False\n                )\n            )\n            \n            if parent_id:\n                query = query.where(BusinessCategory.parent_id == UUID(parent_id))\n            else:\n                query = query.where(BusinessCategory.parent_id.is_(None))\n            \n            if not include_inactive:\n                query = query.where(BusinessCategory.is_active == True)\n            \n            query = query.order_by(BusinessCategory.sort_order, BusinessCategory.name)\n            \n            result = await db.execute(query)\n            return result.scalars().all()\n            \n        except Exception as e:\n            logger.error(f\"Error fetching categories: {e}\")\n            raise\n    \n    # ============================================================================\n    # Business Analytics\n    # ============================================================================\n    \n    async def get_business_analytics(\n        self,\n        business_id: str,\n        tenant_id: str,\n        date_from: datetime,\n        date_to: datetime,\n        db: AsyncSession\n    ) -> Dict[str, Any]:\n        \"\"\"Get business analytics data\"\"\"\n        try:\n            # Set tenant context\n            await db.execute(\n                text(\"SELECT set_config('app.current_tenant_id', :tenant_id, false)\"),\n                {\"tenant_id\": tenant_id}\n            )\n            \n            # Get analytics data\n            query = select(BusinessAnalytics).where(\n                and_(\n                    BusinessAnalytics.business_id == UUID(business_id),\n                    BusinessAnalytics.tenant_id == UUID(tenant_id),\n                    BusinessAnalytics.date >= date_from,\n                    BusinessAnalytics.date <= date_to\n                )\n            ).order_by(BusinessAnalytics.date)\n            \n            result = await db.execute(query)\n            analytics_data = result.scalars().all()\n            \n            # Aggregate metrics\n            metrics = {\n                \"total_views\": sum(a.views for a in analytics_data),\n                \"total_clicks\": sum(a.clicks for a in analytics_data),\n                \"total_calls\": sum(a.phone_calls for a in analytics_data),\n                \"total_website_visits\": sum(a.website_visits for a in analytics_data),\n                \"total_directions\": sum(a.direction_requests for a in analytics_data),\n                \"new_reviews\": sum(a.new_reviews for a in analytics_data)\n            }\n            \n            # Calculate trends (compare with previous period)\n            period_days = (date_to - date_from).days\n            previous_from = date_from - timedelta(days=period_days)\n            previous_to = date_from\n            \n            prev_query = select(BusinessAnalytics).where(\n                and_(\n                    BusinessAnalytics.business_id == UUID(business_id),\n                    BusinessAnalytics.tenant_id == UUID(tenant_id),\n                    BusinessAnalytics.date >= previous_from,\n                    BusinessAnalytics.date < previous_to\n                )\n            )\n            \n            prev_result = await db.execute(prev_query)\n            prev_data = prev_result.scalars().all()\n            \n            prev_metrics = {\n                \"total_views\": sum(a.views for a in prev_data),\n                \"total_clicks\": sum(a.clicks for a in prev_data),\n                \"total_calls\": sum(a.phone_calls for a in prev_data)\n            }\n            \n            # Calculate percentage changes\n            trends = {}\n            for metric, current_value in metrics.items():\n                if metric.startswith('total_'):\n                    prev_value = prev_metrics.get(metric, 0)\n                    if prev_value > 0:\n                        change = ((current_value - prev_value) / prev_value) * 100\n                        trends[metric] = round(change, 2)\n                    else:\n                        trends[metric] = 100.0 if current_value > 0 else 0.0\n            \n            return {\n                \"business_id\": business_id,\n                \"period\": {\n                    \"from\": date_from,\n                    \"to\": date_to\n                },\n                \"metrics\": metrics,\n                \"trends\": trends,\n                \"daily_data\": [\n                    {\n                        \"date\": a.date,\n                        \"views\": a.views,\n                        \"clicks\": a.clicks,\n                        \"calls\": a.phone_calls,\n                        \"website_visits\": a.website_visits,\n                        \"directions\": a.direction_requests,\n                        \"new_reviews\": a.new_reviews\n                    }\n                    for a in analytics_data\n                ]\n            }\n            \n        except Exception as e:\n            logger.error(f\"Error fetching analytics for business {business_id}: {e}\")\n            raise\n    \n    # ============================================================================\n    # Helper Methods\n    # ============================================================================\n    \n    async def _generate_unique_slug(self, name: str, db: AsyncSession) -> str:\n        \"\"\"Generate a unique slug for business name\"\"\"\n        import re\n        \n        # Create base slug\n        base_slug = re.sub(r'[^a-zA-Z0-9\\s]', '', name.lower())\n        base_slug = re.sub(r'\\s+', '-', base_slug).strip('-')\n        \n        # Check for uniqueness\n        counter = 0\n        slug = base_slug\n        \n        while True:\n            query = select(BusinessListing).where(BusinessListing.slug == slug)\n            result = await db.execute(query)\n            if not result.scalar_one_or_none():\n                break\n            \n            counter += 1\n            slug = f\"{base_slug}-{counter}\"\n        \n        return slug\n    \n    async def _apply_business_filters(self, query, search_params: BusinessSearchSchema):\n        \"\"\"Apply filters to business query\"\"\"\n        filters = []\n        \n        # Category filter\n        if search_params.category_id:\n            filters.append(BusinessListing.category_id == search_params.category_id)\n        \n        # Location filters\n        if search_params.city:\n            filters.append(BusinessListing.city.ilike(f\"%{search_params.city}%\"))\n        \n        if search_params.state:\n            filters.append(BusinessListing.state.ilike(f\"%{search_params.state}%\"))\n        \n        if search_params.country:\n            filters.append(BusinessListing.country.ilike(f\"%{search_params.country}%\"))\n        \n        # Status filters\n        if search_params.is_verified is not None:\n            filters.append(BusinessListing.is_verified == search_params.is_verified)\n        \n        if search_params.is_featured is not None:\n            filters.append(BusinessListing.is_featured == search_params.is_featured)\n        \n        # Rating filter\n        if search_params.min_rating is not None:\n            filters.append(BusinessListing.rating_average >= str(search_params.min_rating))\n        \n        # Price range filter\n        if search_params.price_range:\n            filters.append(BusinessListing.price_range.in_(search_params.price_range))\n        \n        # Tags filter\n        if search_params.tags:\n            tag_filters = []\n            for tag in search_params.tags:\n                tag_filters.append(BusinessListing.tags.contains([tag]))\n            filters.append(or_(*tag_filters))\n        \n        # Amenities filter\n        if search_params.amenities:\n            amenity_filters = []\n            for amenity in search_params.amenities:\n                amenity_filters.append(BusinessListing.amenities.contains([amenity]))\n            filters.append(or_(*amenity_filters))\n        \n        # Location-based search (radius)\n        if (search_params.latitude is not None and \n            search_params.longitude is not None and \n            search_params.radius is not None):\n            \n            # Using simple distance calculation\n            # In production, consider using PostGIS for accurate distance\n            lat_diff = func.abs(func.cast(BusinessListing.latitude, func.FLOAT) - search_params.latitude)\n            lng_diff = func.abs(func.cast(BusinessListing.longitude, func.FLOAT) - search_params.longitude)\n            \n            # Approximate distance filter (not accurate for large distances)\n            distance_filter = and_(\n                lat_diff < (search_params.radius / 111.0),  # Rough lat degree to km\n                lng_diff < (search_params.radius / (111.0 * func.cos(func.radians(search_params.latitude))))\n            )\n            filters.append(distance_filter)\n        \n        if filters:\n            query = query.where(and_(*filters))\n        \n        return query\n    \n    def _apply_text_search(self, query, search_query: str):\n        \"\"\"Apply text-based search to query\"\"\"\n        search_terms = search_query.lower().split()\n        \n        search_conditions = []\n        for term in search_terms:\n            term_conditions = [\n                BusinessListing.name.ilike(f\"%{term}%\"),\n                BusinessListing.description.ilike(f\"%{term}%\"),\n                BusinessListing.short_description.ilike(f\"%{term}%\"),\n                BusinessListing.city.ilike(f\"%{term}%\"),\n                BusinessListing.state.ilike(f\"%{term}%\")\n            ]\n            search_conditions.append(or_(*term_conditions))\n        \n        if search_conditions:\n            query = query.where(and_(*search_conditions))\n        \n        return query\n    \n    def _apply_sorting(self, query, sort_by: str, sort_order: str):\n        \"\"\"Apply sorting to query\"\"\"\n        sort_column = getattr(BusinessListing, sort_by, BusinessListing.created_at)\n        \n        if sort_order.lower() == \"desc\":\n            query = query.order_by(sort_column.desc())\n        else:\n            query = query.order_by(sort_column.asc())\n        \n        return query"