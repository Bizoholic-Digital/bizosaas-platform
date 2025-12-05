#!/usr/bin/env python3
"""
WordPress Integration API for CoreLDove Manager Plugin
Connects WordPress plugin (KVM2) to KVM4 backend services via Brain Gateway
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Header, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import uuid4
import httpx
import os
import logging

# Setup logging
logger = logging.getLogger(__name__)

# Create WordPress Integration Router
wordpress_router = APIRouter(
    prefix="/api/v1/wordpress",
    tags=["wordpress-integration"]
)

# ============================================================================
# Pydantic Models for Request/Response Validation
# ============================================================================

class ProductDiscoveryRequest(BaseModel):
    """Request to discover products from Amazon marketplace"""
    keywords: str = Field(..., description="Search keywords for product discovery")
    max_results: int = Field(10, ge=1, le=50, description="Maximum number of results")
    marketplace: str = Field("IN", description="Amazon marketplace (IN, US, UK, etc.)")
    category: Optional[str] = Field(None, description="Product category filter")
    min_price: Optional[float] = Field(None, description="Minimum price filter")
    max_price: Optional[float] = Field(None, description="Maximum price filter")

class ProductApprovalRequest(BaseModel):
    """Request to approve a product for publishing"""
    product_id: str = Field(..., description="Internal product candidate ID")
    asin: str = Field(..., description="Amazon ASIN")
    marketplace: str = Field("IN", description="Source marketplace")
    platforms: List[str] = Field(["google_shopping"], description="Target platforms")
    auto_publish: bool = Field(True, description="Auto-publish after content generation")

class ProductRejectionRequest(BaseModel):
    """Request to reject a product"""
    product_id: str = Field(..., description="Internal product candidate ID")
    reason: Optional[str] = Field(None, description="Rejection reason")

class KeywordResearchRequest(BaseModel):
    """Request for AI-powered keyword research"""
    seed_keywords: List[str] = Field(..., description="Initial seed keywords")
    marketplace: str = Field("IN", description="Target marketplace")
    niche: Optional[str] = Field(None, description="Product niche/category")

class ContentGenerationRequest(BaseModel):
    """Request to generate SEO content for a product"""
    product_id: str = Field(..., description="Product ID")
    asin: str = Field(..., description="Amazon ASIN")
    content_types: List[str] = Field(
        ["title", "description", "features"],
        description="Types of content to generate"
    )
    target_keywords: Optional[List[str]] = Field(None, description="Target SEO keywords")

class MultiPlatformPublishRequest(BaseModel):
    """Request to publish product to multiple platforms"""
    product_id: str = Field(..., description="Product ID")
    platforms: List[str] = Field(
        ...,
        description="Platforms: google_shopping, pinterest, facebook, amazon, flipkart"
    )
    schedule_time: Optional[datetime] = Field(None, description="Schedule for later")

class InventorySyncRequest(BaseModel):
    """Request to sync inventory across platforms"""
    product_ids: Optional[List[str]] = Field(None, description="Specific products (null for all)")
    platforms: List[str] = Field(
        ["google_shopping", "pinterest", "facebook"],
        description="Platforms to sync"
    )

class WorkflowResponse(BaseModel):
    """Standard workflow response"""
    success: bool = Field(..., description="Operation success status")
    workflow_id: str = Field(..., description="Workflow tracking ID")
    status: str = Field(..., description="Current workflow status")
    message: str = Field(..., description="Human-readable message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional response data")

# ============================================================================
# Authentication
# ============================================================================

async def verify_api_key(x_api_key: str = Header(...)):
    """Verify WordPress plugin API key"""
    valid_api_key = os.getenv("WORDPRESS_API_KEY", "coreldove_wp_api_key_2025")
    if x_api_key != valid_api_key:
        logger.warning(f"Invalid API key attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return True

# ============================================================================
# Service Clients for Internal Communication
# ============================================================================

class ServiceClients:
    """HTTP clients for communicating with KVM4 backend services"""

    @staticmethod
    def get_amazon_sourcing_client():
        """Client for Amazon Sourcing Service (port 8080)"""
        return httpx.AsyncClient(
            base_url="http://backend-amazon-sourcing:8080",
            timeout=30.0
        )

    @staticmethod
    def get_ai_agents_client():
        """Client for AI Agents Service (port 8002)"""
        return httpx.AsyncClient(
            base_url="http://backend-ai-agents:8002",
            timeout=60.0
        )

    @staticmethod
    def get_coreldove_backend_client():
        """Client for CoreLDove Backend Service (port 9000)"""
        return httpx.AsyncClient(
            base_url="http://backend-coreldove-backend:9000",
            timeout=30.0
        )

# ============================================================================
# API Endpoints
# ============================================================================

@wordpress_router.get("/health")
async def health_check():
    """
    Health check endpoint for WordPress plugin monitoring
    """
    return {
        "status": "healthy",
        "service": "WordPress Integration API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@wordpress_router.post("/discover-products", response_model=WorkflowResponse)
async def discover_products(
    request: ProductDiscoveryRequest,
    background_tasks: BackgroundTasks,
    authenticated: bool = Depends(verify_api_key)
):
    """
    Discover products from Amazon marketplace using SP-API

    This endpoint:
    1. Searches Amazon marketplace using provided keywords
    2. Returns product candidates with pricing, ratings, images
    3. Stores candidates in database for WordPress review
    """
    workflow_id = f"discover-{uuid4()}"

    try:
        logger.info(f"Product discovery request: {request.keywords} in {request.marketplace}")

        # Call Amazon Sourcing Service
        async with ServiceClients.get_amazon_sourcing_client() as client:
            response = await client.post("/api/v1/search", json={
                "keywords": request.keywords,
                "max_results": request.max_results,
                "marketplace": request.marketplace,
                "filters": {
                    "category": request.category,
                    "min_price": request.min_price,
                    "max_price": request.max_price
                }
            })

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Amazon sourcing failed: {response.text}"
                )

            products_data = response.json()

        return WorkflowResponse(
            success=True,
            workflow_id=workflow_id,
            status="completed",
            message=f"Found {len(products_data.get('products', []))} products",
            data=products_data
        )

    except httpx.RequestError as e:
        logger.error(f"Product discovery failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Amazon sourcing service unavailable: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Product discovery error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Product discovery failed: {str(e)}"
        )

@wordpress_router.post("/approve-product", response_model=WorkflowResponse)
async def approve_product(
    request: ProductApprovalRequest,
    background_tasks: BackgroundTasks,
    authenticated: bool = Depends(verify_api_key)
):
    """
    Approve a product and trigger publishing workflows

    This endpoint:
    1. Updates product status to 'approved' in database
    2. Triggers AI content generation workflow
    3. Publishes to selected platforms if auto_publish=True
    """
    workflow_id = f"approve-{uuid4()}"

    try:
        logger.info(f"Product approval: {request.product_id} (ASIN: {request.asin})")

        # Update product status in CoreLDove backend
        async with ServiceClients.get_coreldove_backend_client() as client:
            response = await client.post(f"/api/products/{request.product_id}/approve", json={
                "asin": request.asin,
                "marketplace": request.marketplace,
                "auto_publish": request.auto_publish,
                "target_platforms": request.platforms
            })

            if response.status_code not in [200, 201]:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Product approval failed: {response.text}"
                )

            approval_data = response.json()

        # If auto-publish enabled, trigger publishing workflow
        if request.auto_publish:
            # This would trigger Temporal workflow in production
            logger.info(f"Auto-publishing product {request.product_id} to platforms: {request.platforms}")
            # TODO: Trigger Temporal workflow here

        return WorkflowResponse(
            success=True,
            workflow_id=workflow_id,
            status="approved" if not request.auto_publish else "publishing",
            message=f"Product approved{'and publishing' if request.auto_publish else ''}",
            data=approval_data
        )

    except Exception as e:
        logger.error(f"Product approval error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Product approval failed: {str(e)}"
        )

@wordpress_router.post("/reject-product", response_model=WorkflowResponse)
async def reject_product(
    request: ProductRejectionRequest,
    authenticated: bool = Depends(verify_api_key)
):
    """
    Reject a product candidate with optional reason
    """
    workflow_id = f"reject-{uuid4()}"

    try:
        logger.info(f"Product rejection: {request.product_id}")

        async with ServiceClients.get_coreldove_backend_client() as client:
            response = await client.post(f"/api/products/{request.product_id}/reject", json={
                "reason": request.reason
            })

            if response.status_code not in [200, 201]:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Product rejection failed: {response.text}"
                )

            rejection_data = response.json()

        return WorkflowResponse(
            success=True,
            workflow_id=workflow_id,
            status="rejected",
            message="Product rejected successfully",
            data=rejection_data
        )

    except Exception as e:
        logger.error(f"Product rejection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Product rejection failed: {str(e)}"
        )

@wordpress_router.post("/keyword-research", response_model=WorkflowResponse)
async def perform_keyword_research(
    request: KeywordResearchRequest,
    background_tasks: BackgroundTasks,
    authenticated: bool = Depends(verify_api_key)
):
    """
    AI-powered keyword research for product discovery

    Uses AI agents to:
    1. Expand seed keywords
    2. Analyze search volume and competition
    3. Suggest high-opportunity keywords
    """
    workflow_id = f"keyword-{uuid4()}"

    try:
        logger.info(f"Keyword research: {request.seed_keywords}")

        async with ServiceClients.get_ai_agents_client() as client:
            response = await client.post("/api/v1/keyword-research", json={
                "seed_keywords": request.seed_keywords,
                "marketplace": request.marketplace,
                "niche": request.niche
            })

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Keyword research failed: {response.text}"
                )

            keyword_data = response.json()

        return WorkflowResponse(
            success=True,
            workflow_id=workflow_id,
            status="completed",
            message=f"Generated {len(keyword_data.get('keywords', []))} keyword suggestions",
            data=keyword_data
        )

    except Exception as e:
        logger.error(f"Keyword research error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Keyword research failed: {str(e)}"
        )

@wordpress_router.post("/generate-content", response_model=WorkflowResponse)
async def generate_content(
    request: ContentGenerationRequest,
    background_tasks: BackgroundTasks,
    authenticated: bool = Depends(verify_api_key)
):
    """
    Generate SEO-optimized content for products using AI agents

    Generates:
    - Product titles (SEO-optimized)
    - Product descriptions
    - Feature bullet points
    - Meta descriptions
    """
    workflow_id = f"content-{uuid4()}"

    try:
        logger.info(f"Content generation for product: {request.product_id}")

        async with ServiceClients.get_ai_agents_client() as client:
            response = await client.post("/api/v1/generate-content", json={
                "product_id": request.product_id,
                "asin": request.asin,
                "content_types": request.content_types,
                "target_keywords": request.target_keywords
            })

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Content generation failed: {response.text}"
                )

            content_data = response.json()

        return WorkflowResponse(
            success=True,
            workflow_id=workflow_id,
            status="completed",
            message=f"Generated {len(request.content_types)} content types",
            data=content_data
        )

    except Exception as e:
        logger.error(f"Content generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content generation failed: {str(e)}"
        )

@wordpress_router.post("/publish-multi-platform", response_model=WorkflowResponse)
async def publish_to_platforms(
    request: MultiPlatformPublishRequest,
    background_tasks: BackgroundTasks,
    authenticated: bool = Depends(verify_api_key)
):
    """
    Publish product to multiple platforms

    Supported platforms:
    - google_shopping: Google Merchant Center
    - pinterest: Pinterest Product Pins
    - facebook: Facebook Catalog
    - amazon: Amazon Seller Central
    - flipkart: Flipkart Seller Hub
    """
    workflow_id = f"publish-{uuid4()}"

    try:
        logger.info(f"Multi-platform publish: {request.product_id} to {request.platforms}")

        # Trigger publishing via CoreLDove backend
        async with ServiceClients.get_coreldove_backend_client() as client:
            response = await client.post("/api/products/publish", json={
                "product_id": request.product_id,
                "platforms": request.platforms,
                "schedule_time": request.schedule_time.isoformat() if request.schedule_time else None
            })

            if response.status_code not in [200, 201, 202]:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Publishing failed: {response.text}"
                )

            publish_data = response.json()

        return WorkflowResponse(
            success=True,
            workflow_id=workflow_id,
            status="publishing" if not request.schedule_time else "scheduled",
            message=f"Publishing to {len(request.platforms)} platforms",
            data=publish_data
        )

    except Exception as e:
        logger.error(f"Multi-platform publish error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Publishing failed: {str(e)}"
        )

@wordpress_router.post("/sync-inventory", response_model=WorkflowResponse)
async def sync_inventory(
    request: InventorySyncRequest,
    background_tasks: BackgroundTasks,
    authenticated: bool = Depends(verify_api_key)
):
    """
    Sync inventory levels across all publishing platforms

    Ensures consistent stock levels on:
    - Google Shopping
    - Pinterest
    - Facebook Catalog
    - Amazon
    - Flipkart
    """
    workflow_id = f"sync-{uuid4()}"

    try:
        logger.info(f"Inventory sync request for platforms: {request.platforms}")

        async with ServiceClients.get_coreldove_backend_client() as client:
            response = await client.post("/api/inventory/sync", json={
                "product_ids": request.product_ids,
                "platforms": request.platforms
            })

            if response.status_code not in [200, 202]:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Inventory sync failed: {response.text}"
                )

            sync_data = response.json()

        return WorkflowResponse(
            success=True,
            workflow_id=workflow_id,
            status="syncing",
            message=f"Syncing inventory across {len(request.platforms)} platforms",
            data=sync_data
        )

    except Exception as e:
        logger.error(f"Inventory sync error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inventory sync failed: {str(e)}"
        )

@wordpress_router.get("/workflow-status/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow_status(
    workflow_id: str,
    authenticated: bool = Depends(verify_api_key)
):
    """
    Query the status of a Temporal workflow

    Returns current state, progress, and any error messages
    """
    try:
        logger.info(f"Workflow status query: {workflow_id}")

        # In production, this would query Temporal
        # For MVP, return mock status
        return WorkflowResponse(
            success=True,
            workflow_id=workflow_id,
            status="running",
            message="Workflow is in progress",
            data={
                "started_at": datetime.utcnow().isoformat(),
                "progress": 50,
                "steps_completed": 3,
                "steps_total": 6
            }
        )

    except Exception as e:
        logger.error(f"Workflow status error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get workflow status: {str(e)}"
        )

# ============================================================================
# Router Export
# ============================================================================

logger.info("✅ WordPress Integration API initialized")
