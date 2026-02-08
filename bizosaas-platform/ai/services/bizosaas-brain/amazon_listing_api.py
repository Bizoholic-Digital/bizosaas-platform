"""
Amazon Listing API Integration Layer

This module provides the FastAPI endpoints and integration layer for the complete
Amazon listing workflow, exposing all functionality through a RESTful API that
integrates with the BizOSaaS Platform's central brain gateway.

Key Features:
- Complete Amazon listing workflow API endpoints
- Real-time progress tracking with WebSocket support
- Tenant-aware authentication and authorization
- Bulk processing with async job management
- Comprehensive validation and compliance checking
- Performance monitoring and analytics
- Error handling with detailed responses
- Integration with BizOSaaS AI Coordinator

API Endpoints:
- POST /api/brain/amazon/listings/create - Create single listing
- POST /api/brain/amazon/listings/bulk - Start bulk processing
- GET /api/brain/amazon/listings/batch/{batch_id} - Get batch status
- GET /api/brain/amazon/listings/validate - Validate listing content
- WebSocket /api/brain/amazon/listings/progress - Real-time progress updates

Integration with BizOSaaS Platform:
- Routes through FastAPI AI Central Hub (Port 8001)
- Tenant-aware processing with proper isolation
- Integration with 93+ AI agents ecosystem
- Comprehensive audit trail and logging
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
import logging

# FastAPI imports
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, WebSocket, WebSocketDisconnect, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
from typing_extensions import Annotated

# BizOSaaS Platform imports
from .ai_coordinator import EnhancedAICoordinator, EnhancedTenantContext
from .amazon_listing_workflow_orchestrator import (
    AmazonListingWorkflowOrchestrator, ProductInput, WorkflowConfiguration, WorkflowResult
)
from .amazon_compliance_validator import (
    AmazonComplianceValidator, ValidationResult, ComplianceRules, ComplianceLevel
)
from .amazon_content_generator import (
    AmazonContentGenerator, AmazonListingContent, ContentGenerationConfig
)
from .amazon_bulk_processor import (
    AmazonBulkProcessor, BatchConfiguration, BatchProcessingResult, ProcessingPriority, BatchMode
)
from .research_to_listing_bridge import ResearchToListingBridge

# Setup logging
logger = logging.getLogger(__name__)

# Authentication setup
security = HTTPBearer()

# Pydantic models for API requests/responses
class ProductInputModel(BaseModel):
    """Product input model for API"""
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    category: Optional[str] = Field(None, description="Product category")
    price: Optional[float] = Field(None, gt=0, description="Product price")
    brand: Optional[str] = Field(None, description="Product brand")
    sku: Optional[str] = Field(None, description="Product SKU")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Additional product attributes")
    images: List[str] = Field(default_factory=list, description="Product image URLs")
    target_keywords: List[str] = Field(default_factory=list, description="Target keywords for SEO")

    def to_product_input(self) -> ProductInput:
        """Convert to internal ProductInput format"""
        return ProductInput(
            name=self.name,
            description=self.description,
            category=self.category,
            price=self.price,
            brand=self.brand,
            sku=self.sku,
            attributes=self.attributes,
            images=self.images,
            target_keywords=self.target_keywords
        )

class WorkflowConfigurationModel(BaseModel):
    """Workflow configuration model for API"""
    enable_research: bool = Field(True, description="Enable product research phase")
    enable_content_generation: bool = Field(True, description="Enable AI content generation")
    enable_seo_optimization: bool = Field(True, description="Enable SEO optimization")
    enable_compliance_validation: bool = Field(True, description="Enable compliance validation")
    auto_submit: bool = Field(False, description="Auto-submit to Amazon after validation")
    research_depth: str = Field("standard", description="Research depth: basic, standard, comprehensive")
    content_tone: str = Field("professional", description="Content tone: professional, casual, technical")
    target_audience: str = Field("general", description="Target audience: general, professional, technical")
    compliance_level: str = Field("standard", description="Compliance level: basic, standard, strict")

    @validator('research_depth')
    def validate_research_depth(cls, v):
        if v not in ['basic', 'standard', 'comprehensive']:
            raise ValueError('research_depth must be: basic, standard, or comprehensive')
        return v

    @validator('content_tone')
    def validate_content_tone(cls, v):
        if v not in ['professional', 'casual', 'technical', 'marketing']:
            raise ValueError('content_tone must be: professional, casual, technical, or marketing')
        return v

    @validator('compliance_level')
    def validate_compliance_level(cls, v):
        if v not in ['basic', 'standard', 'strict']:
            raise ValueError('compliance_level must be: basic, standard, or strict')
        return v

class BatchConfigurationModel(BaseModel):
    """Batch configuration model for API"""
    batch_size: int = Field(10, ge=1, le=100, description="Items per batch")
    max_concurrent: int = Field(5, ge=1, le=20, description="Max concurrent workers")
    timeout_minutes: int = Field(30, ge=5, le=120, description="Timeout per item in minutes")
    mode: str = Field("hybrid", description="Processing mode: concurrent, sequential, hybrid, adaptive")
    retry_enabled: bool = Field(True, description="Enable automatic retries")
    validation_required: bool = Field(True, description="Require compliance validation")
    priority: str = Field("normal", description="Processing priority: urgent, high, normal, low, background")

    @validator('mode')
    def validate_mode(cls, v):
        valid_modes = ['concurrent', 'sequential', 'hybrid', 'adaptive']
        if v not in valid_modes:
            raise ValueError(f'mode must be one of: {", ".join(valid_modes)}')
        return v

    @validator('priority')
    def validate_priority(cls, v):
        valid_priorities = ['urgent', 'high', 'normal', 'low', 'background']
        if v not in valid_priorities:
            raise ValueError(f'priority must be one of: {", ".join(valid_priorities)}')
        return v

    def to_batch_configuration(self) -> BatchConfiguration:
        """Convert to internal BatchConfiguration format"""
        mode_mapping = {
            'concurrent': BatchMode.CONCURRENT,
            'sequential': BatchMode.SEQUENTIAL,
            'hybrid': BatchMode.HYBRID,
            'adaptive': BatchMode.ADAPTIVE
        }

        return BatchConfiguration(
            batch_size=self.batch_size,
            max_concurrent=self.max_concurrent,
            timeout_per_item=timedelta(minutes=self.timeout_minutes),
            mode=mode_mapping[self.mode],
            retry_enabled=self.retry_enabled,
            validation_required=self.validation_required
        )

class CreateListingRequest(BaseModel):
    """Request model for creating a single listing"""
    product: ProductInputModel
    workflow_config: Optional[WorkflowConfigurationModel] = None
    tenant_id: Optional[str] = None

class BulkListingRequest(BaseModel):
    """Request model for bulk listing creation"""
    products: List[ProductInputModel] = Field(..., min_items=1, max_items=1000)
    workflow_config: Optional[WorkflowConfigurationModel] = None
    batch_config: Optional[BatchConfigurationModel] = None
    tenant_id: Optional[str] = None

class ValidationRequest(BaseModel):
    """Request model for listing validation"""
    listing_content: Dict[str, Any]
    compliance_level: Optional[str] = Field("standard", description="Compliance level")
    tenant_id: Optional[str] = None

class ListingResponse(BaseModel):
    """Response model for listing operations"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None
    workflow_id: Optional[str] = None
    processing_time: Optional[float] = None

class BatchResponse(BaseModel):
    """Response model for batch operations"""
    success: bool
    message: str
    batch_id: str
    total_items: int
    estimated_completion: Optional[str] = None
    progress_url: Optional[str] = None

class BatchStatusResponse(BaseModel):
    """Response model for batch status"""
    batch_id: str
    status: str
    progress: Dict[str, Any]
    items: List[Dict[str, Any]]
    statistics: Dict[str, Any]
    estimated_completion: Optional[str] = None

class ValidationResponse(BaseModel):
    """Response model for validation operations"""
    success: bool
    overall_score: float
    compliance_level: str
    issues: List[Dict[str, Any]]
    recommendations: List[str]
    auto_fix_available: bool

# Global instances (would be injected via dependency injection in production)
_orchestrator: Optional[AmazonListingWorkflowOrchestrator] = None
_validator: Optional[AmazonComplianceValidator] = None
_bulk_processor: Optional[AmazonBulkProcessor] = None
_ai_coordinator: Optional[EnhancedAICoordinator] = None

# WebSocket connection manager
class ConnectionManager:
    """Manage WebSocket connections for real-time updates"""

    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, batch_id: str):
        """Accept WebSocket connection"""
        await websocket.accept()
        if batch_id not in self.active_connections:
            self.active_connections[batch_id] = []
        self.active_connections[batch_id].append(websocket)

    def disconnect(self, websocket: WebSocket, batch_id: str):
        """Remove WebSocket connection"""
        if batch_id in self.active_connections:
            if websocket in self.active_connections[batch_id]:
                self.active_connections[batch_id].remove(websocket)
            if not self.active_connections[batch_id]:
                del self.active_connections[batch_id]

    async def send_update(self, batch_id: str, message: dict):
        """Send update to all connections for a batch"""
        if batch_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[batch_id]:
                try:
                    await connection.send_json(message)
                except:
                    disconnected.append(connection)

            # Remove disconnected connections
            for connection in disconnected:
                self.disconnect(connection, batch_id)

connection_manager = ConnectionManager()

# Initialize API router
router = APIRouter(prefix="/api/brain/amazon/listings", tags=["Amazon Listings"])

async def get_tenant_context(credentials: HTTPAuthorizationCredentials = Depends(security)) -> EnhancedTenantContext:
    """Extract tenant context from authentication token"""
    # In production, this would validate JWT token and extract tenant info
    # For now, we'll use a placeholder implementation
    try:
        # Mock token validation - replace with actual JWT validation
        token = credentials.credentials

        # Extract tenant ID from token (mock implementation)
        tenant_id = "default_tenant"  # Would be extracted from validated JWT

        return EnhancedTenantContext(
            tenant_id=tenant_id,
            user_id="default_user",
            subscription_tier="premium",
            feature_flags={"amazon_listing": True, "bulk_processing": True},
            api_limits={"requests_per_hour": 1000, "batch_size_limit": 100},
            custom_config={}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

def init_services(
    orchestrator: AmazonListingWorkflowOrchestrator,
    validator: AmazonComplianceValidator,
    bulk_processor: AmazonBulkProcessor,
    ai_coordinator: EnhancedAICoordinator
):
    """Initialize service dependencies"""
    global _orchestrator, _validator, _bulk_processor, _ai_coordinator
    _orchestrator = orchestrator
    _validator = validator
    _bulk_processor = bulk_processor
    _ai_coordinator = ai_coordinator

    # Register progress callback for WebSocket updates
    _bulk_processor.register_progress_callback(send_batch_progress_update)

async def send_batch_progress_update(batch_id: str, batch_result: BatchProcessingResult):
    """Send batch progress update via WebSocket"""
    message = {
        "type": "progress_update",
        "batch_id": batch_id,
        "status": batch_result.status.value,
        "progress": {
            "total_items": batch_result.total_items,
            "processed_items": batch_result.processed_items,
            "successful_items": batch_result.successful_items,
            "failed_items": batch_result.failed_items,
            "error_rate": batch_result.error_rate,
            "percentage": (batch_result.processed_items / batch_result.total_items) * 100 if batch_result.total_items > 0 else 0
        },
        "timestamp": datetime.utcnow().isoformat()
    }

    await connection_manager.send_update(batch_id, message)

@router.post("/create", response_model=ListingResponse)
async def create_listing(
    request: CreateListingRequest,
    background_tasks: BackgroundTasks,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
):
    """
    Create a single Amazon listing using the complete workflow

    This endpoint processes a single product through the entire Amazon listing
    workflow including research, content generation, validation, and submission.
    """
    try:
        if not _orchestrator:
            raise HTTPException(status_code=500, detail="Service not initialized")

        start_time = datetime.utcnow()
        workflow_id = str(uuid.uuid4())

        logger.info(f"Starting listing creation for tenant {tenant_context.tenant_id}")

        # Convert request models to internal formats
        product_input = request.product.to_product_input()

        # Set up workflow configuration
        workflow_config = WorkflowConfiguration()
        if request.workflow_config:
            workflow_config.enable_research = request.workflow_config.enable_research
            workflow_config.enable_content_generation = request.workflow_config.enable_content_generation
            workflow_config.enable_seo_optimization = request.workflow_config.enable_seo_optimization
            workflow_config.auto_submit = request.workflow_config.auto_submit

        # Execute workflow
        workflow_result = await _orchestrator.start_listing_workflow(
            tenant_context=tenant_context,
            products=[product_input],
            configuration=workflow_config
        )

        # Calculate processing time
        processing_time = (datetime.utcnow() - start_time).total_seconds()

        # Prepare response
        response_data = {
            "workflow_result": asdict(workflow_result),
            "product_processed": product_input.name,
            "listings_created": len(workflow_result.listings) if workflow_result.listings else 0
        }

        if workflow_result.success:
            return ListingResponse(
                success=True,
                message="Listing created successfully",
                data=response_data,
                workflow_id=workflow_id,
                processing_time=processing_time
            )
        else:
            return ListingResponse(
                success=False,
                message="Listing creation failed",
                data=response_data,
                errors=workflow_result.errors,
                workflow_id=workflow_id,
                processing_time=processing_time
            )

    except Exception as e:
        logger.error(f"Listing creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Listing creation failed: {str(e)}"
        )

@router.post("/bulk", response_model=BatchResponse)
async def create_bulk_listings(
    request: BulkListingRequest,
    background_tasks: BackgroundTasks,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
):
    """
    Start bulk processing of Amazon listings

    This endpoint initiates bulk processing of multiple products, returning
    a batch ID for tracking progress through the WebSocket endpoint.
    """
    try:
        if not _bulk_processor:
            raise HTTPException(status_code=500, detail="Bulk processor not initialized")

        logger.info(f"Starting bulk processing for {len(request.products)} products")

        # Convert request models to internal formats
        products = [product.to_product_input() for product in request.products]

        # Set up configurations
        workflow_config = WorkflowConfiguration()
        if request.workflow_config:
            workflow_config.enable_research = request.workflow_config.enable_research
            workflow_config.enable_content_generation = request.workflow_config.enable_content_generation
            workflow_config.enable_seo_optimization = request.workflow_config.enable_seo_optimization
            workflow_config.auto_submit = request.workflow_config.auto_submit

        batch_config = None
        priority = ProcessingPriority.NORMAL

        if request.batch_config:
            batch_config = request.batch_config.to_batch_configuration()

            # Map priority
            priority_mapping = {
                'urgent': ProcessingPriority.URGENT,
                'high': ProcessingPriority.HIGH,
                'normal': ProcessingPriority.NORMAL,
                'low': ProcessingPriority.LOW,
                'background': ProcessingPriority.BACKGROUND
            }
            priority = priority_mapping.get(request.batch_config.priority, ProcessingPriority.NORMAL)

        # Start bulk processing
        batch_id = await _bulk_processor.process_bulk_listings(
            products=products,
            tenant_context=tenant_context,
            workflow_config=workflow_config,
            batch_config=batch_config,
            priority=priority
        )

        # Calculate estimated completion time
        estimated_minutes = len(products) * 2  # Rough estimate: 2 minutes per product
        estimated_completion = (datetime.utcnow() + timedelta(minutes=estimated_minutes)).isoformat()

        return BatchResponse(
            success=True,
            message=f"Bulk processing started for {len(products)} products",
            batch_id=batch_id,
            total_items=len(products),
            estimated_completion=estimated_completion,
            progress_url=f"/api/brain/amazon/listings/progress/{batch_id}"
        )

    except Exception as e:
        logger.error(f"Bulk processing failed to start: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Bulk processing failed to start: {str(e)}"
        )

@router.get("/batch/{batch_id}", response_model=BatchStatusResponse)
async def get_batch_status(
    batch_id: str,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
):
    """
    Get the current status of a bulk processing batch

    Returns detailed information about batch progress, item status,
    and performance statistics.
    """
    try:
        if not _bulk_processor:
            raise HTTPException(status_code=500, detail="Bulk processor not initialized")

        batch_result = _bulk_processor.get_batch_status(batch_id)

        if not batch_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Batch {batch_id} not found"
            )

        # Security check - ensure tenant can access this batch
        batch_items_for_tenant = [
            item for item in batch_result.items
            if item.tenant_id == tenant_context.tenant_id
        ]

        if not batch_items_for_tenant:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this batch"
            )

        # Prepare response data
        progress_data = {
            "total_items": batch_result.total_items,
            "processed_items": batch_result.processed_items,
            "successful_items": batch_result.successful_items,
            "failed_items": batch_result.failed_items,
            "error_rate": batch_result.error_rate,
            "percentage": (batch_result.processed_items / batch_result.total_items) * 100 if batch_result.total_items > 0 else 0,
            "started_at": batch_result.started_at.isoformat(),
            "completed_at": batch_result.completed_at.isoformat() if batch_result.completed_at else None,
            "processing_time": str(batch_result.processing_time) if batch_result.processing_time else None
        }

        # Convert items to serializable format
        items_data = []
        for item in batch_items_for_tenant[:50]:  # Limit to first 50 items for performance
            item_data = {
                "id": item.id,
                "product_name": item.product_input.name,
                "status": item.status.value,
                "progress_percentage": item.progress_percentage,
                "current_phase": item.current_phase,
                "error_message": item.error_message,
                "retry_count": item.retry_count,
                "processing_time": str(item.processing_time) if item.processing_time else None
            }
            items_data.append(item_data)

        # Estimate completion time
        estimated_completion = None
        if batch_result.status.value == "processing" and batch_result.processed_items > 0:
            avg_time_per_item = batch_result.processing_time.total_seconds() / batch_result.processed_items
            remaining_items = batch_result.total_items - batch_result.processed_items
            estimated_seconds = remaining_items * avg_time_per_item
            estimated_completion = (datetime.utcnow() + timedelta(seconds=estimated_seconds)).isoformat()

        return BatchStatusResponse(
            batch_id=batch_id,
            status=batch_result.status.value,
            progress=progress_data,
            items=items_data,
            statistics=batch_result.summary_statistics,
            estimated_completion=estimated_completion
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get batch status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get batch status: {str(e)}"
        )

@router.post("/validate", response_model=ValidationResponse)
async def validate_listing(
    request: ValidationRequest,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
):
    """
    Validate Amazon listing content for compliance

    Performs comprehensive validation of listing content against Amazon's
    policies and requirements, returning detailed feedback and recommendations.
    """
    try:
        if not _validator:
            raise HTTPException(status_code=500, detail="Validator not initialized")

        logger.info(f"Starting listing validation for tenant {tenant_context.tenant_id}")

        # Convert compliance level
        compliance_mapping = {
            'basic': ComplianceLevel.BASIC,
            'standard': ComplianceLevel.STANDARD,
            'strict': ComplianceLevel.STRICT
        }
        compliance_level = compliance_mapping.get(request.compliance_level, ComplianceLevel.STANDARD)

        # Create compliance rules
        compliance_rules = ComplianceRules(level=compliance_level)

        # Convert listing content (this would be more sophisticated in production)
        listing_content = AmazonListingContent(
            title=request.listing_content.get('title', ''),
            description=request.listing_content.get('description', ''),
            bullet_points=request.listing_content.get('bullet_points', []),
            keywords=request.listing_content.get('keywords', []),
            category=request.listing_content.get('category', ''),
            price=request.listing_content.get('price'),
            images=request.listing_content.get('images', []),
            attributes=request.listing_content.get('attributes', {}),
            msrp=request.listing_content.get('msrp')
        )

        # Perform validation
        validation_result = await _validator.validate_listing(
            listing_content=listing_content,
            tenant_context=tenant_context,
            compliance_rules=compliance_rules
        )

        # Convert issues to serializable format
        issues_data = []
        for issue in validation_result.issues:
            issue_data = {
                "category": issue.category.value,
                "severity": issue.severity.value,
                "title": issue.title,
                "description": issue.description,
                "field_affected": issue.field_affected,
                "recommended_action": issue.recommended_action,
                "auto_fixable": issue.auto_fixable
            }
            issues_data.append(issue_data)

        return ValidationResponse(
            success=validation_result.overall_score > 70,  # Consider 70+ as passing
            overall_score=validation_result.overall_score,
            compliance_level=validation_result.compliance_level.value,
            issues=issues_data,
            recommendations=validation_result.recommendations,
            auto_fix_available=validation_result.auto_fix_available
        )

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation failed: {str(e)}"
        )

@router.websocket("/progress/{batch_id}")
async def batch_progress_websocket(websocket: WebSocket, batch_id: str):
    """
    WebSocket endpoint for real-time batch progress updates

    Provides real-time updates on batch processing progress, including
    item status changes, error notifications, and completion events.
    """
    try:
        await connection_manager.connect(websocket, batch_id)

        # Send initial status
        if _bulk_processor:
            batch_result = _bulk_processor.get_batch_status(batch_id)
            if batch_result:
                initial_message = {
                    "type": "initial_status",
                    "batch_id": batch_id,
                    "status": batch_result.status.value,
                    "total_items": batch_result.total_items,
                    "processed_items": batch_result.processed_items
                }
                await websocket.send_json(initial_message)

        # Keep connection alive and handle messages
        while True:
            try:
                # Wait for client messages (ping/pong, etc.)
                message = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)

                # Handle client messages
                if message == "ping":
                    await websocket.send_text("pong")

            except asyncio.TimeoutError:
                # Send keepalive ping
                await websocket.send_json({"type": "ping"})
            except WebSocketDisconnect:
                break

    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        connection_manager.disconnect(websocket, batch_id)

@router.post("/batch/{batch_id}/pause")
async def pause_batch(
    batch_id: str,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
):
    """Pause a running batch"""
    try:
        if not _bulk_processor:
            raise HTTPException(status_code=500, detail="Bulk processor not initialized")

        success = await _bulk_processor.pause_batch(batch_id)

        if success:
            return {"success": True, "message": f"Batch {batch_id} paused"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Batch cannot be paused"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to pause batch: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to pause batch: {str(e)}"
        )

@router.post("/batch/{batch_id}/resume")
async def resume_batch(
    batch_id: str,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
):
    """Resume a paused batch"""
    try:
        if not _bulk_processor:
            raise HTTPException(status_code=500, detail="Bulk processor not initialized")

        success = await _bulk_processor.resume_batch(batch_id)

        if success:
            return {"success": True, "message": f"Batch {batch_id} resumed"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Batch cannot be resumed"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to resume batch: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to resume batch: {str(e)}"
        )

@router.post("/batch/{batch_id}/cancel")
async def cancel_batch(
    batch_id: str,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
):
    """Cancel a batch"""
    try:
        if not _bulk_processor:
            raise HTTPException(status_code=500, detail="Bulk processor not initialized")

        success = await _bulk_processor.cancel_batch(batch_id)

        if success:
            return {"success": True, "message": f"Batch {batch_id} cancelled"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Batch cannot be cancelled"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to cancel batch: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel batch: {str(e)}"
        )

@router.get("/stats/performance")
async def get_performance_stats(
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
):
    """Get performance statistics"""
    try:
        if not _bulk_processor:
            raise HTTPException(status_code=500, detail="Bulk processor not initialized")

        stats = await _bulk_processor.get_performance_statistics()

        return {
            "success": True,
            "data": stats,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Failed to get performance stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get performance stats: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if all services are initialized
        services_status = {
            "orchestrator": _orchestrator is not None,
            "validator": _validator is not None,
            "bulk_processor": _bulk_processor is not None,
            "ai_coordinator": _ai_coordinator is not None
        }

        all_healthy = all(services_status.values())

        return {
            "healthy": all_healthy,
            "services": services_status,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "healthy": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

# Export the router
__all__ = ['router', 'init_services']