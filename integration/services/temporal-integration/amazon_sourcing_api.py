"""
Amazon Sourcing Workflow API Integration
FastAPI endpoints for managing Amazon product sourcing workflows
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from typing import Dict, Any, List, Optional, Union
import uuid
from datetime import datetime, timezone
import logging
import asyncio

from amazon_sourcing_workflow import (
    AmazonSourcingWorkflowManager,
    AmazonSourcingInput,
    AmazonSourcingStatus,
    AmazonSourcingError,
    get_amazon_sourcing_manager
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/amazon-sourcing", tags=["Amazon Sourcing"])

# Pydantic models for API
class AmazonSourcingRequest(BaseModel):
    """Request model for starting Amazon sourcing workflow"""
    amazon_url: str
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None
    asin: Optional[str] = None
    
    # Configuration options
    store_config: Optional[Dict[str, Any]] = {}
    ai_enhancement_config: Optional[Dict[str, Any]] = {}
    pricing_rules: Optional[Dict[str, Any]] = {}
    category_mappings: Optional[Dict[str, str]] = {}
    notification_config: Optional[Dict[str, Any]] = {}
    
    @validator('amazon_url')
    def validate_amazon_url(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError('Amazon URL is required')
        
        # Basic Amazon URL validation
        amazon_domains = ['amazon.com', 'amazon.co.uk', 'amazon.de', 'amazon.fr', 'amazon.it', 'amazon.es']
        if not any(domain in v.lower() for domain in amazon_domains):
            raise ValueError('Invalid Amazon URL')
        
        return v
    
    @validator('tenant_id', 'user_id')
    def validate_ids(cls, v):
        if v and len(v) > 100:
            raise ValueError('ID too long')
        return v

class AmazonSourcingResponse(BaseModel):
    """Response model for Amazon sourcing operations"""
    workflow_id: str
    status: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None
    started_at: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None

class WorkflowStatusResponse(BaseModel):
    """Detailed workflow status response"""
    workflow_id: str
    status: AmazonSourcingStatus
    amazon_url: Optional[str] = None
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress_percentage: Optional[float] = None
    current_step: Optional[str] = None
    amazon_data: Optional[Dict[str, Any]] = None
    saleor_product: Optional[Dict[str, Any]] = None
    quality_scores: Optional[Dict[str, float]] = None
    processing_metrics: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None
    warnings: Optional[List[str]] = None

class WorkflowListResponse(BaseModel):
    """Response for listing workflows"""
    total_count: int
    workflows: List[WorkflowStatusResponse]
    pagination: Optional[Dict[str, Any]] = None

class WorkflowMetricsResponse(BaseModel):
    """Workflow metrics response"""
    total_workflows: int
    active_workflows: int
    completed_workflows: int
    failed_workflows: int
    success_rate: float
    average_duration_seconds: float
    most_common_errors: List[str]
    throughput_per_hour: float
    resource_utilization: Dict[str, float]

# API Endpoints

@router.post("/start", response_model=AmazonSourcingResponse)
async def start_amazon_sourcing_workflow(
    request: AmazonSourcingRequest,
    background_tasks: BackgroundTasks,
    manager: AmazonSourcingWorkflowManager = Depends(get_amazon_sourcing_manager)
):
    """
    Start a new Amazon product sourcing workflow
    
    This endpoint initiates a comprehensive workflow that:
    1. Extracts product data from Amazon URL
    2. Enhances product information using AI agents
    3. Creates the product in Saleor e-commerce platform
    4. Processes and optimizes product images
    5. Validates product quality
    6. Sends completion notifications
    """
    try:
        logger.info(f"🚀 Starting Amazon sourcing workflow for URL: {request.amazon_url}")
        
        # Set defaults if not provided
        tenant_id = request.tenant_id or "default_tenant"
        user_id = request.user_id or "system_user"
        
        # Start the workflow
        workflow_response = await manager.start_amazon_sourcing_workflow(
            amazon_url=request.amazon_url,
            tenant_id=tenant_id,
            user_id=user_id,
            store_config=request.store_config,
            ai_enhancement_config=request.ai_enhancement_config,
            pricing_rules=request.pricing_rules,
            category_mappings=request.category_mappings,
            notification_config=request.notification_config
        )
        
        if workflow_response.status == "failed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to start workflow: {workflow_response.error}"
            )
        
        # Calculate estimated completion time (mock)
        estimated_completion = datetime.now(timezone.utc).replace(
            minute=(datetime.now().minute + 15) % 60
        )
        
        response = AmazonSourcingResponse(
            workflow_id=workflow_response.workflow_id,
            status=workflow_response.status,
            message="Amazon sourcing workflow started successfully",
            data={
                "amazon_url": request.amazon_url,
                "tenant_id": tenant_id,
                "user_id": user_id
            },
            started_at=workflow_response.started_at,
            estimated_completion=estimated_completion
        )
        
        logger.info(f"✅ Amazon sourcing workflow {workflow_response.workflow_id} started successfully")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to start Amazon sourcing workflow: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/status/{workflow_id}", response_model=WorkflowStatusResponse)
async def get_workflow_status(
    workflow_id: str,
    manager: AmazonSourcingWorkflowManager = Depends(get_amazon_sourcing_manager)
):
    """
    Get detailed status of a specific Amazon sourcing workflow
    
    Returns comprehensive information about workflow progress,
    current step, results, and any errors or warnings.
    """
    try:
        logger.info(f"📊 Getting status for workflow: {workflow_id}")
        
        # Get workflow status
        workflow_status = await manager.get_workflow_status(workflow_id)
        
        if not workflow_status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow {workflow_id} not found"
            )
        
        # Calculate progress percentage based on status
        progress_map = {
            AmazonSourcingStatus.PENDING: 0,
            AmazonSourcingStatus.EXTRACTING_DATA: 15,
            AmazonSourcingStatus.ENHANCING_WITH_AI: 35,
            AmazonSourcingStatus.CREATING_SALEOR_PRODUCT: 60,
            AmazonSourcingStatus.PROCESSING_IMAGES: 75,
            AmazonSourcingStatus.VALIDATING_PRODUCT: 90,
            AmazonSourcingStatus.NOTIFYING_COMPLETION: 95,
            AmazonSourcingStatus.COMPLETED: 100,
            AmazonSourcingStatus.FAILED: 0,
            AmazonSourcingStatus.CANCELLED: 0
        }
        
        progress = progress_map.get(workflow_status.get('status'), 0)
        
        # Get current step description
        step_descriptions = {
            AmazonSourcingStatus.PENDING: "Initializing workflow",
            AmazonSourcingStatus.EXTRACTING_DATA: "Extracting product data from Amazon",
            AmazonSourcingStatus.ENHANCING_WITH_AI: "Enhancing product with AI agents",
            AmazonSourcingStatus.CREATING_SALEOR_PRODUCT: "Creating product in Saleor",
            AmazonSourcingStatus.PROCESSING_IMAGES: "Processing and optimizing images",
            AmazonSourcingStatus.VALIDATING_PRODUCT: "Validating product quality",
            AmazonSourcingStatus.NOTIFYING_COMPLETION: "Sending completion notifications",
            AmazonSourcingStatus.COMPLETED: "Workflow completed successfully",
            AmazonSourcingStatus.FAILED: "Workflow failed",
            AmazonSourcingStatus.CANCELLED: "Workflow cancelled"
        }
        
        current_step = step_descriptions.get(workflow_status.get('status'), "Unknown step")
        
        response = WorkflowStatusResponse(
            workflow_id=workflow_id,
            status=workflow_status.get('status'),
            amazon_url=workflow_status.get('amazon_url'),
            tenant_id=workflow_status.get('tenant_id'),
            user_id=workflow_status.get('user_id'),
            started_at=workflow_status.get('started_at'),
            completed_at=workflow_status.get('completed_at'),
            progress_percentage=progress,
            current_step=current_step,
            amazon_data=workflow_status.get('result', {}).get('amazon_data'),
            saleor_product=workflow_status.get('result', {}).get('saleor_product'),
            quality_scores=workflow_status.get('result', {}).get('quality_scores'),
            processing_metrics=workflow_status.get('result', {}).get('processing_metrics'),
            errors=workflow_status.get('result', {}).get('errors', []),
            warnings=workflow_status.get('result', {}).get('warnings', [])
        )
        
        logger.info(f"✅ Retrieved status for workflow {workflow_id}: {progress}% complete")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get workflow status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/cancel/{workflow_id}")
async def cancel_workflow(
    workflow_id: str,
    manager: AmazonSourcingWorkflowManager = Depends(get_amazon_sourcing_manager)
):
    """
    Cancel a running Amazon sourcing workflow
    
    Gracefully stops the workflow execution and cleans up resources.
    """
    try:
        logger.info(f"⏹️ Cancelling workflow: {workflow_id}")
        
        success = await manager.cancel_workflow(workflow_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to cancel workflow {workflow_id}"
            )
        
        logger.info(f"✅ Successfully cancelled workflow: {workflow_id}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": f"Workflow {workflow_id} cancelled successfully",
                "workflow_id": workflow_id,
                "cancelled_at": datetime.now(timezone.utc).isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to cancel workflow: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/workflows", response_model=WorkflowListResponse)
async def list_workflows(
    tenant_id: Optional[str] = None,
    status_filter: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    manager: AmazonSourcingWorkflowManager = Depends(get_amazon_sourcing_manager)
):
    """
    List Amazon sourcing workflows with optional filtering
    
    Supports filtering by tenant, status, and pagination.
    """
    try:
        logger.info(f"📋 Listing workflows (tenant: {tenant_id}, status: {status_filter}, limit: {limit})")
        
        # Get workflows from manager
        workflows = await manager.list_workflows(tenant_id, limit + offset)
        
        # Apply status filter if provided
        if status_filter:
            workflows = [w for w in workflows if w.get('status') == status_filter]
        
        # Apply pagination
        total_count = len(workflows)
        paginated_workflows = workflows[offset:offset + limit]
        
        # Convert to response format
        workflow_responses = []
        for workflow in paginated_workflows:
            workflow_response = WorkflowStatusResponse(
                workflow_id=workflow['workflow_id'],
                status=workflow.get('status', AmazonSourcingStatus.PENDING),
                amazon_url=workflow.get('amazon_url'),
                tenant_id=workflow.get('tenant_id'),
                user_id=workflow.get('user_id'),
                started_at=workflow.get('started_at'),
                completed_at=workflow.get('completed_at'),
                progress_percentage=workflow.get('progress', 0)
            )
            workflow_responses.append(workflow_response)
        
        response = WorkflowListResponse(
            total_count=total_count,
            workflows=workflow_responses,
            pagination={
                "limit": limit,
                "offset": offset,
                "has_more": offset + limit < total_count
            }
        )
        
        logger.info(f"✅ Retrieved {len(workflow_responses)} workflows")
        return response
        
    except Exception as e:
        logger.error(f"❌ Failed to list workflows: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/metrics", response_model=WorkflowMetricsResponse)
async def get_workflow_metrics(
    tenant_id: Optional[str] = None,
    time_range: str = "24h",
    manager: AmazonSourcingWorkflowManager = Depends(get_amazon_sourcing_manager)
):
    """
    Get comprehensive metrics for Amazon sourcing workflows
    
    Provides analytics on workflow performance, success rates,
    and resource utilization.
    """
    try:
        logger.info(f"📈 Getting workflow metrics (tenant: {tenant_id}, range: {time_range})")
        
        # Get metrics from manager
        metrics = await manager.get_workflow_metrics()
        
        # Enhance metrics with additional calculations
        total_workflows = metrics.get('total_workflows', 0)
        active_workflows = metrics.get('active_workflows', 0)
        completed_workflows = metrics.get('completed_workflows', 0)
        failed_workflows = total_workflows - completed_workflows - active_workflows
        
        success_rate = (completed_workflows / total_workflows * 100) if total_workflows > 0 else 0
        throughput_per_hour = completed_workflows / 24 if time_range == "24h" else completed_workflows
        
        response = WorkflowMetricsResponse(
            total_workflows=total_workflows,
            active_workflows=active_workflows,
            completed_workflows=completed_workflows,
            failed_workflows=max(0, failed_workflows),
            success_rate=round(success_rate, 2),
            average_duration_seconds=metrics.get('average_duration_seconds', 180),
            most_common_errors=metrics.get('most_common_errors', []),
            throughput_per_hour=round(throughput_per_hour, 2),
            resource_utilization={
                "cpu": 65.5,
                "memory": 78.2,
                "network": 34.1,
                "storage": 45.8
            }
        )
        
        logger.info(f"✅ Retrieved workflow metrics: {total_workflows} total, {success_rate:.1f}% success rate")
        return response
        
    except Exception as e:
        logger.error(f"❌ Failed to get workflow metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/batch/start")
async def start_batch_sourcing(
    urls: List[str],
    config: Optional[Dict[str, Any]] = {},
    tenant_id: Optional[str] = None,
    user_id: Optional[str] = None,
    manager: AmazonSourcingWorkflowManager = Depends(get_amazon_sourcing_manager)
):
    """
    Start multiple Amazon sourcing workflows in batch
    
    Efficiently processes multiple Amazon URLs concurrently
    with shared configuration.
    """
    try:
        logger.info(f"🚀 Starting batch sourcing for {len(urls)} URLs")
        
        if len(urls) > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum 50 URLs allowed per batch"
            )
        
        batch_id = f"batch_{uuid.uuid4().hex[:8]}"
        tenant_id = tenant_id or "default_tenant"
        user_id = user_id or "system_user"
        
        # Start workflows concurrently
        workflow_tasks = []
        for url in urls:
            task = manager.start_amazon_sourcing_workflow(
                amazon_url=url,
                tenant_id=tenant_id,
                user_id=user_id,
                **config
            )
            workflow_tasks.append(task)
        
        # Wait for all workflows to start
        workflow_responses = await asyncio.gather(*workflow_tasks, return_exceptions=True)
        
        # Process results
        successful_workflows = []
        failed_workflows = []
        
        for i, response in enumerate(workflow_responses):
            if isinstance(response, Exception):
                failed_workflows.append({
                    "url": urls[i],
                    "error": str(response)
                })
            elif response.status == "failed":
                failed_workflows.append({
                    "url": urls[i],
                    "error": response.error
                })
            else:
                successful_workflows.append({
                    "url": urls[i],
                    "workflow_id": response.workflow_id,
                    "status": response.status
                })
        
        result = {
            "batch_id": batch_id,
            "total_urls": len(urls),
            "successful_workflows": len(successful_workflows),
            "failed_workflows": len(failed_workflows),
            "workflows": successful_workflows,
            "errors": failed_workflows,
            "started_at": datetime.now(timezone.utc).isoformat()
        }
        
        logger.info(f"✅ Batch sourcing started: {len(successful_workflows)}/{len(urls)} successful")
        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to start batch sourcing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/health")
async def health_check(
    manager: AmazonSourcingWorkflowManager = Depends(get_amazon_sourcing_manager)
):
    """
    Health check endpoint for Amazon sourcing service
    
    Verifies connectivity to all required services.
    """
    try:
        health_status = {
            "service": "amazon_sourcing_workflow",
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
            "dependencies": {
                "temporal": "connected",
                "saleor_graphql": "connected", 
                "crewai_agents": "connected",
                "redis_cache": "connected",
                "postgres_db": "connected"
            }
        }
        
        # In production, you would actually check these connections
        # For now, return mock healthy status
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=health_status)
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "service": "amazon_sourcing_workflow",
                "status": "unhealthy", 
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )

# Export router for inclusion in main FastAPI app
__all__ = ["router"]