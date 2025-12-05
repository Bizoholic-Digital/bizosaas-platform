"""
CoreLDove E-commerce Order Processing Workflow System
Main entry point for the comprehensive order processing automation
"""

import os
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

from .services.order_orchestrator import OrderProcessingOrchestrator
from .services.inventory_manager import InventoryManager
from .services.payment_processor import PaymentProcessor
from .services.fulfillment_manager import FulfillmentManager
from .services.notification_service import NotificationService
from .integrations.saleor_integration import SaleorIntegration
from .integrations.ai_crew_integration import AICrewIntegration
from .models.order_models import (
    OrderCreateRequest, OrderUpdateRequest, OrderResponse,
    OrderStatus, FulfillmentRequest, RefundRequest, TrackingResponse
)
from .utils.security import get_current_user, verify_api_key
from .utils.monitoring import PerformanceMonitor, MetricsCollector
from .utils.error_handler import ErrorHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global services
order_orchestrator: Optional[OrderProcessingOrchestrator] = None
performance_monitor: Optional[PerformanceMonitor] = None
metrics_collector: Optional[MetricsCollector] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup application lifecycle"""
    global order_orchestrator, performance_monitor, metrics_collector
    
    logger.info("Starting CoreLDove Order Processing Workflow System...")
    
    try:
        # Initialize services
        performance_monitor = PerformanceMonitor()
        metrics_collector = MetricsCollector()
        
        # Initialize order orchestrator with all dependencies
        order_orchestrator = OrderProcessingOrchestrator(
            inventory_manager=InventoryManager(),
            payment_processor=PaymentProcessor(),
            fulfillment_manager=FulfillmentManager(),
            notification_service=NotificationService(),
            saleor_integration=SaleorIntegration(),
            ai_crew_integration=AICrewIntegration(),
            performance_monitor=performance_monitor,
            metrics_collector=metrics_collector
        )
        
        await order_orchestrator.initialize()
        
        logger.info("Order Processing Workflow System initialized successfully")
        yield
        
    except Exception as e:
        logger.error(f"Failed to initialize Order Processing System: {e}")
        raise
    
    finally:
        # Cleanup
        if order_orchestrator:
            await order_orchestrator.shutdown()
        logger.info("Order Processing Workflow System shutdown complete")


# Initialize FastAPI app
app = FastAPI(
    title="CoreLDove Order Processing Workflow API",
    description="Comprehensive E-commerce Order Processing with AI Automation",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handler
error_handler = ErrorHandler()

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return await error_handler.handle_error(exc)


# Health check endpoint
@app.get("/health", response_model=Dict[str, Any])
async def health_check():
    """System health check"""
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "services": {}
        }
        
        if order_orchestrator:
            health_status["services"] = await order_orchestrator.get_health_status()
        
        return health_status
    
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "error": str(e)}
        )


# Order Processing Endpoints
@app.post("/api/order-workflow/orders", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreateRequest,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create and process new order with full automation"""
    try:
        logger.info(f"Creating new order for user {current_user.get('user_id')}")
        
        # Start performance monitoring
        start_time = datetime.utcnow()
        
        # Process order through orchestrator
        order_result = await order_orchestrator.process_order(
            order_data=order_data.dict(),
            user_context=current_user
        )
        
        # Schedule background tasks
        background_tasks.add_task(
            _track_order_metrics,
            order_result["order_id"],
            start_time
        )
        
        background_tasks.add_task(
            _send_order_notifications,
            order_result
        )
        
        return OrderResponse(**order_result)
    
    except Exception as e:
        logger.error(f"Order creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order processing failed: {str(e)}"
        )


@app.put("/api/order-workflow/orders/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: str,
    status_update: OrderUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update order status with automated workflow triggers"""
    try:
        logger.info(f"Updating order {order_id} status to {status_update.status}")
        
        order_result = await order_orchestrator.update_order_status(
            order_id=order_id,
            new_status=status_update.status,
            update_data=status_update.dict(exclude_unset=True),
            user_context=current_user
        )
        
        return OrderResponse(**order_result)
    
    except Exception as e:
        logger.error(f"Order status update failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status update failed: {str(e)}"
        )


@app.post("/api/order-workflow/orders/{order_id}/fulfill", response_model=OrderResponse)
async def process_fulfillment(
    order_id: str,
    fulfillment_data: FulfillmentRequest,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Process order fulfillment with automated shipping and tracking"""
    try:
        logger.info(f"Processing fulfillment for order {order_id}")
        
        fulfillment_result = await order_orchestrator.process_fulfillment(
            order_id=order_id,
            fulfillment_data=fulfillment_data.dict(),
            user_context=current_user
        )
        
        # Schedule background notification tasks
        background_tasks.add_task(
            _send_fulfillment_notifications,
            fulfillment_result
        )
        
        return OrderResponse(**fulfillment_result)
    
    except Exception as e:
        logger.error(f"Fulfillment processing failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Fulfillment failed: {str(e)}"
        )


@app.post("/api/order-workflow/orders/{order_id}/refund", response_model=OrderResponse)
async def process_refund(
    order_id: str,
    refund_data: RefundRequest,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Process order refund with automated payment processing"""
    try:
        logger.info(f"Processing refund for order {order_id}")
        
        refund_result = await order_orchestrator.process_refund(
            order_id=order_id,
            refund_data=refund_data.dict(),
            user_context=current_user
        )
        
        # Schedule background notification tasks
        background_tasks.add_task(
            _send_refund_notifications,
            refund_result
        )
        
        return OrderResponse(**refund_result)
    
    except Exception as e:
        logger.error(f"Refund processing failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Refund failed: {str(e)}"
        )


@app.get("/api/order-workflow/orders/{order_id}/tracking", response_model=TrackingResponse)
async def get_order_tracking(
    order_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get real-time order tracking information"""
    try:
        tracking_info = await order_orchestrator.get_order_tracking(
            order_id=order_id,
            user_context=current_user
        )
        
        return TrackingResponse(**tracking_info)
    
    except Exception as e:
        logger.error(f"Tracking retrieval failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tracking information not found: {str(e)}"
        )


@app.get("/api/order-workflow/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get complete order information"""
    try:
        order_info = await order_orchestrator.get_order(
            order_id=order_id,
            user_context=current_user
        )
        
        return OrderResponse(**order_info)
    
    except Exception as e:
        logger.error(f"Order retrieval failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order not found: {str(e)}"
        )


@app.get("/api/order-workflow/orders", response_model=List[OrderResponse])
async def list_orders(
    status: Optional[OrderStatus] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """List orders with filtering and pagination"""
    try:
        orders = await order_orchestrator.list_orders(
            user_context=current_user,
            status_filter=status,
            limit=limit,
            offset=offset
        )
        
        return [OrderResponse(**order) for order in orders]
    
    except Exception as e:
        logger.error(f"Order listing failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order listing failed: {str(e)}"
        )


# Analytics and Monitoring Endpoints
@app.get("/api/order-workflow/analytics/performance")
async def get_performance_metrics(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get order processing performance metrics"""
    try:
        if not performance_monitor:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Performance monitoring not available"
            )
        
        metrics = await performance_monitor.get_metrics()
        return metrics
    
    except Exception as e:
        logger.error(f"Performance metrics retrieval failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Metrics retrieval failed: {str(e)}"
        )


@app.get("/api/order-workflow/analytics/inventory")
async def get_inventory_analytics(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get inventory analytics and insights"""
    try:
        analytics = await order_orchestrator.get_inventory_analytics()
        return analytics
    
    except Exception as e:
        logger.error(f"Inventory analytics retrieval failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analytics retrieval failed: {str(e)}"
        )


# Background task functions
async def _track_order_metrics(order_id: str, start_time: datetime):
    """Track order processing metrics"""
    try:
        if metrics_collector:
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            await metrics_collector.record_order_metric(
                order_id=order_id,
                metric_type="processing_time",
                value=processing_time
            )
    except Exception as e:
        logger.error(f"Metrics tracking failed: {e}")


async def _send_order_notifications(order_result: Dict[str, Any]):
    """Send order confirmation notifications"""
    try:
        if order_orchestrator:
            await order_orchestrator.send_order_notifications(order_result)
    except Exception as e:
        logger.error(f"Order notification failed: {e}")


async def _send_fulfillment_notifications(fulfillment_result: Dict[str, Any]):
    """Send fulfillment notifications"""
    try:
        if order_orchestrator:
            await order_orchestrator.send_fulfillment_notifications(fulfillment_result)
    except Exception as e:
        logger.error(f"Fulfillment notification failed: {e}")


async def _send_refund_notifications(refund_result: Dict[str, Any]):
    """Send refund notifications"""
    try:
        if order_orchestrator:
            await order_orchestrator.send_refund_notifications(refund_result)
    except Exception as e:
        logger.error(f"Refund notification failed: {e}")


if __name__ == "__main__":
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8001"))
    reload = os.getenv("ENVIRONMENT", "development") == "development"
    
    logger.info(f"Starting CoreLDove Order Processing API on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )