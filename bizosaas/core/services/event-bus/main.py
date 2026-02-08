"""
BizOSaaS Event Bus Service

Main FastAPI service providing REST API for event publishing,
subscription management, and event bus administration.
"""

import asyncio
import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
import redis.asyncio as redis
import structlog
import uvicorn

from domain_events import (
    BaseEvent, EventStatus, EventPriority, EventCategory,
    create_event, get_event_class, EVENT_TYPES
)
from event_bus import EventBus, EventBusConfig, EventProcessingResult
from event_storage import EventStore
from subscription_manager import EventSubscription, SubscriptionStats
from tenant_isolation import TenantContext, TenantContextManager, ensure_tenant_isolation


# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


class Settings(BaseSettings):
    """Application settings"""
    
    # Service configuration
    service_name: str = "event-bus"
    service_port: int = 8009
    debug: bool = True
    
    # Redis configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    
    # PostgreSQL configuration
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "admin"
    postgres_password: str = "securepassword"
    postgres_db: str = "bizosaas"
    
    # Message broker configuration
    broker_type: str = "redis"  # redis, rabbitmq, kafka
    rabbitmq_url: Optional[str] = None
    kafka_bootstrap_servers: Optional[str] = None
    
    # Event bus configuration
    max_retry_attempts: int = 3
    retry_delay_seconds: int = 5
    event_ttl_days: int = 30
    batch_size: int = 100
    worker_concurrency: int = 10
    enable_tenant_isolation: bool = True
    metrics_enabled: bool = True
    health_check_interval: int = 30
    
    # Security
    jwt_secret: str = "your-super-secret-jwt-key-here"
    allowed_origins: List[str] = ["*"]
    
    class Config:
        env_prefix = "EVENTBUS_"
        case_sensitive = False


# Global variables
settings = Settings()
event_bus: Optional[EventBus] = None
tenant_context_manager: Optional[TenantContextManager] = None


# Request/Response Models

class PublishEventRequest(BaseModel):
    """Request model for publishing events"""
    event_type: str = Field(..., description="Type of event to publish")
    tenant_id: UUID = Field(..., description="Tenant ID for multi-tenancy")
    data: Dict[str, Any] = Field(default_factory=dict, description="Event payload")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Event metadata")
    priority: EventPriority = Field(default=EventPriority.NORMAL, description="Event priority")
    target_services: List[str] = Field(default_factory=list, description="Target services")
    source_service: str = Field(..., description="Source service name")
    correlation_id: Optional[UUID] = Field(None, description="Correlation ID")
    aggregate_id: Optional[UUID] = Field(None, description="Aggregate ID")
    aggregate_type: Optional[str] = Field(None, description="Aggregate type")


class PublishEventResponse(BaseModel):
    """Response model for publishing events"""
    success: bool
    event_id: UUID
    message: str = "Event published successfully"
    processing_time_ms: int = 0


class SubscribeRequest(BaseModel):
    """Request model for creating subscriptions"""
    event_type: str = Field(..., description="Event type to subscribe to")
    service_name: str = Field(..., description="Name of subscribing service")
    tenant_id: Optional[UUID] = Field(None, description="Tenant ID for tenant-specific subscriptions")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Event filters")
    webhook_url: Optional[str] = Field(None, description="Webhook URL for notifications")


class SubscribeResponse(BaseModel):
    """Response model for subscriptions"""
    subscription_id: str
    message: str = "Subscription created successfully"


class EventHistoryRequest(BaseModel):
    """Request model for event history queries"""
    tenant_id: UUID
    event_types: Optional[List[str]] = None
    aggregate_id: Optional[UUID] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: int = Field(default=100, le=1000)
    offset: int = Field(default=0, ge=0)


class ReplayEventsRequest(BaseModel):
    """Request model for event replay"""
    tenant_id: UUID
    event_types: List[str]
    start_time: datetime
    end_time: Optional[datetime] = None
    target_service: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str = "1.0.0"
    components: Dict[str, Dict[str, Any]]


# Dependency injection

async def get_event_bus() -> EventBus:
    """Get event bus dependency"""
    if not event_bus:
        raise HTTPException(status_code=500, detail="Event bus not initialized")
    return event_bus


async def get_tenant_context_manager() -> TenantContextManager:
    """Get tenant context manager dependency"""
    if not tenant_context_manager:
        raise HTTPException(status_code=500, detail="Tenant context manager not initialized")
    return tenant_context_manager


async def get_tenant_context(
    tenant_id: UUID,
    context_manager: TenantContextManager = Depends(get_tenant_context_manager)
) -> TenantContext:
    """Get tenant context for request"""
    context = await context_manager.get_tenant_context(tenant_id)
    if not context:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return context


# Application lifespan management

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    global event_bus, tenant_context_manager
    
    logger.info("Starting BizOSaaS Event Bus Service")
    
    try:
        # Create database URL
        database_url = (
            f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
            f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
        )
        
        # Create event bus configuration
        config = EventBusConfig(
            redis_host=settings.redis_host,
            redis_port=settings.redis_port,
            redis_db=settings.redis_db,
            redis_password=settings.redis_password,
            database_url=database_url,
            broker_type=settings.broker_type,
            rabbitmq_url=settings.rabbitmq_url,
            kafka_bootstrap_servers=settings.kafka_bootstrap_servers,
            max_retry_attempts=settings.max_retry_attempts,
            retry_delay_seconds=settings.retry_delay_seconds,
            event_ttl_days=settings.event_ttl_days,
            batch_size=settings.batch_size,
            worker_concurrency=settings.worker_concurrency,
            enable_tenant_isolation=settings.enable_tenant_isolation,
            metrics_enabled=settings.metrics_enabled,
            health_check_interval=settings.health_check_interval,
        )
        
        # Initialize event bus
        event_bus = EventBus(config)
        await event_bus.initialize()
        await event_bus.start()
        
        # Initialize tenant context manager
        redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password,
            decode_responses=True
        )
        tenant_context_manager = TenantContextManager(redis_client)
        
        logger.info("Event Bus Service started successfully")
        
        yield
        
    except Exception as e:
        logger.error("Failed to start Event Bus Service", error=str(e))
        raise
    
    finally:
        # Cleanup
        if event_bus:
            await event_bus.stop()
        logger.info("Event Bus Service stopped")


# Create FastAPI app

app = FastAPI(
    title="BizOSaaS Event Bus",
    description="Domain Event Bus for BizOSaaS Platform - AI Agent Coordination & Event-Driven Architecture",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", error=str(exc), path=str(request.url))
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# API Routes

@app.get("/", response_model=Dict[str, Any])
async def root():
    """Service information"""
    return {
        "service": "BizOSaaS Event Bus",
        "version": "1.0.0",
        "description": "Domain Event Bus for AI Agent Coordination",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "publish": "/events/publish",
            "subscribe": "/events/subscribe",
            "history": "/events/history",
            "replay": "/events/replay",
            "subscriptions": "/subscriptions",
            "metrics": "/metrics",
            "health": "/health"
        }
    }


@app.post("/events/publish", response_model=PublishEventResponse)
async def publish_event(
    request: PublishEventRequest,
    bus: EventBus = Depends(get_event_bus),
    tenant_context: TenantContext = Depends(lambda r=None: get_tenant_context(request.tenant_id) if r else None)
):
    """Publish an event to the event bus"""
    try:
        # Create event
        event_class = get_event_class(request.event_type)
        event = event_class(
            event_type=request.event_type,
            tenant_id=request.tenant_id,
            source_service=request.source_service,
            data=request.data,
            metadata=request.metadata,
            priority=request.priority,
            target_services=request.target_services,
            correlation_id=request.correlation_id,
            aggregate_id=request.aggregate_id,
            aggregate_type=request.aggregate_type,
            category=EventCategory.SYSTEM  # Default category
        )
        
        # Get tenant context for this request
        context_manager = await get_tenant_context_manager()
        tenant_ctx = await context_manager.get_tenant_context(request.tenant_id)
        
        # Publish event
        result = await bus.publish_event(event, tenant_ctx)
        
        if result.success:
            return PublishEventResponse(
                success=True,
                event_id=result.event_id,
                processing_time_ms=result.processing_time_ms
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to publish event: {', '.join(result.errors)}"
            )
    
    except Exception as e:
        logger.error("Failed to publish event", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/events/subscribe", response_model=SubscribeResponse)
async def subscribe_to_events(
    request: SubscribeRequest,
    bus: EventBus = Depends(get_event_bus)
):
    """Subscribe to events"""
    try:
        # Create dummy handler for webhook notifications
        async def webhook_handler(event: BaseEvent):
            if request.webhook_url:
                # In a real implementation, send HTTP POST to webhook_url
                logger.info(
                    "Webhook notification",
                    webhook_url=request.webhook_url,
                    event_id=str(event.event_id),
                    event_type=event.event_type
                )
        
        # Subscribe to events
        subscription_id = await bus.subscribe(
            event_type=request.event_type,
            handler=webhook_handler,
            service_name=request.service_name,
            tenant_id=request.tenant_id,
            filters=request.filters
        )
        
        return SubscribeResponse(subscription_id=subscription_id)
    
    except Exception as e:
        logger.error("Failed to create subscription", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/events/subscribe/{subscription_id}")
async def unsubscribe_from_events(
    subscription_id: str,
    bus: EventBus = Depends(get_event_bus)
):
    """Unsubscribe from events"""
    try:
        success = await bus.unsubscribe(subscription_id)
        if success:
            return {"message": "Unsubscribed successfully", "subscription_id": subscription_id}
        else:
            raise HTTPException(status_code=404, detail="Subscription not found")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to unsubscribe", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/events/history")
async def get_event_history(
    request: EventHistoryRequest,
    bus: EventBus = Depends(get_event_bus)
):
    """Get event history for a tenant"""
    try:
        events = await bus.get_event_history(
            tenant_id=request.tenant_id,
            aggregate_id=request.aggregate_id,
            event_types=request.event_types,
            limit=request.limit
        )
        
        return {
            "events": events,
            "count": len(events),
            "tenant_id": str(request.tenant_id),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error("Failed to get event history", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/events/replay")
async def replay_events(
    request: ReplayEventsRequest,
    background_tasks: BackgroundTasks,
    bus: EventBus = Depends(get_event_bus)
):
    """Replay events for a tenant"""
    try:
        # Start replay in background
        async def replay_task():
            count = await bus.replay_events(
                tenant_id=request.tenant_id,
                event_types=request.event_types,
                start_time=request.start_time,
                end_time=request.end_time,
                target_service=request.target_service
            )
            logger.info("Event replay completed", count=count, tenant_id=str(request.tenant_id))
        
        background_tasks.add_task(replay_task)
        
        return {
            "message": "Event replay started",
            "tenant_id": str(request.tenant_id),
            "event_types": request.event_types,
            "time_range": {
                "start": request.start_time.isoformat(),
                "end": request.end_time.isoformat() if request.end_time else None
            }
        }
    
    except Exception as e:
        logger.error("Failed to start event replay", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/subscriptions/stats", response_model=SubscriptionStats)
async def get_subscription_statistics(bus: EventBus = Depends(get_event_bus)):
    """Get subscription statistics"""
    try:
        stats = await bus.subscription_manager.get_subscription_statistics()
        return stats
    
    except Exception as e:
        logger.error("Failed to get subscription statistics", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics(bus: EventBus = Depends(get_event_bus)):
    """Get event bus metrics"""
    try:
        metrics = await bus.get_metrics()
        return metrics
    
    except Exception as e:
        logger.error("Failed to get metrics", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    try:
        components = {}
        overall_status = "healthy"
        
        # Check event bus
        if event_bus:
            try:
                await event_bus.event_store.health_check()
                await event_bus.message_broker.health_check()
                components["event_bus"] = {"status": "healthy", "is_running": event_bus.is_running}
            except Exception as e:
                components["event_bus"] = {"status": "unhealthy", "error": str(e)}
                overall_status = "unhealthy"
        else:
            components["event_bus"] = {"status": "not_initialized"}
            overall_status = "unhealthy"
        
        return HealthCheckResponse(
            status=overall_status,
            timestamp=datetime.utcnow().isoformat(),
            components=components
        )
    
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return HealthCheckResponse(
            status="unhealthy",
            timestamp=datetime.utcnow().isoformat(),
            components={"error": str(e)}
        )


@app.get("/event-types")
async def get_event_types():
    """Get available event types"""
    return {
        "event_types": list(EVENT_TYPES.keys()),
        "count": len(EVENT_TYPES),
        "categories": [category.value for category in EventCategory],
        "priorities": [priority.value for priority in EventPriority]
    }


@app.get("/tenants/{tenant_id}/context")
async def get_tenant_context_info(
    tenant_id: UUID,
    context_manager: TenantContextManager = Depends(get_tenant_context_manager)
):
    """Get tenant context information"""
    try:
        context = await context_manager.get_tenant_context(tenant_id)
        if not context:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        return context.model_dump()
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get tenant context", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.service_port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )