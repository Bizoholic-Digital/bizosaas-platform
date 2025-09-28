#!/usr/bin/env python3
"""
BizOSaaS Event Bus Service - Standalone Version

Main FastAPI service providing REST API for event publishing,
subscription management, and event bus administration.

This standalone version can be run directly without module imports.
"""

import asyncio
import json
import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union
from uuid import UUID, uuid4

import redis.asyncio as redis
import structlog
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

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


# Domain Event Definitions (Simplified)

class EventStatus(str, Enum):
    """Event processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class EventPriority(str, Enum):
    """Event priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class EventCategory(str, Enum):
    """Event categories for organization"""
    USER = "user"
    TENANT = "tenant"
    CAMPAIGN = "campaign"
    LEAD = "lead"
    AI_ANALYSIS = "ai_analysis"
    SYSTEM = "system"
    INTEGRATION = "integration"
    BILLING = "billing"
    SECURITY = "security"


class BaseEvent(BaseModel):
    """Base domain event with common fields"""
    
    # Event identification
    event_id: UUID = Field(default_factory=uuid4, description="Unique event identifier")
    event_type: str = Field(..., description="Type of event")
    event_version: str = Field(default="1.0", description="Event schema version")
    
    # Event metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the event occurred")
    tenant_id: UUID = Field(..., description="Tenant context for multi-tenancy")
    source_service: str = Field(..., description="Service that emitted the event")
    correlation_id: Optional[UUID] = Field(None, description="Request correlation ID")
    causation_id: Optional[UUID] = Field(None, description="ID of the event that caused this event")
    
    # Event properties
    category: EventCategory = Field(..., description="Event category")
    priority: EventPriority = Field(default=EventPriority.NORMAL, description="Event priority")
    aggregate_id: Optional[UUID] = Field(None, description="ID of the aggregate root")
    aggregate_type: Optional[str] = Field(None, description="Type of aggregate root")
    
    # Event data
    data: Dict[str, Any] = Field(default_factory=dict, description="Event payload")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    # Processing info
    status: EventStatus = Field(default=EventStatus.PENDING, description="Processing status")
    retry_count: int = Field(default=0, description="Number of processing retries")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    
    # Routing and targeting
    target_services: List[str] = Field(default_factory=list, description="Services that should receive this event")
    routing_key: Optional[str] = Field(None, description="Message broker routing key")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


# Application Settings

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
    
    # Event bus configuration
    max_retry_attempts: int = 3
    event_ttl_days: int = 30
    enable_tenant_isolation: bool = True
    
    # Security
    jwt_secret: str = "your-super-secret-jwt-key-here"
    allowed_origins: List[str] = ["*"]
    
    class Config:
        env_prefix = "EVENTBUS_"
        case_sensitive = False


# Global variables
settings = Settings()
redis_client: Optional[redis.Redis] = None
event_store: Dict[str, Any] = {}  # In-memory storage for demo
subscriptions: Dict[str, Any] = {}  # In-memory subscriptions
metrics = {
    "events_published": 0,
    "events_processed": 0,
    "events_failed": 0,
    "active_subscriptions": 0
}


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


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str = "1.0.0"
    components: Dict[str, Dict[str, Any]]


# Core Event Bus Logic (Simplified)

async def initialize_redis():
    """Initialize Redis connection"""
    global redis_client
    try:
        redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password,
            decode_responses=True
        )
        await redis_client.ping()
        logger.info("Redis connection established")
        return True
    except Exception as e:
        logger.error("Failed to connect to Redis", error=str(e))
        return False


async def store_event(event: BaseEvent) -> bool:
    """Store event (simplified in-memory storage)"""
    try:
        event_data = event.model_dump()
        event_store[str(event.event_id)] = event_data
        
        # Also store in Redis if available
        if redis_client:
            await redis_client.hset(
                f"events:{event.tenant_id}",
                str(event.event_id),
                json.dumps(event_data, default=str)
            )
        
        logger.info("Event stored", event_id=str(event.event_id), event_type=event.event_type)
        return True
    except Exception as e:
        logger.error("Failed to store event", error=str(e))
        return False


async def publish_event_internal(event: BaseEvent) -> bool:
    """Publish event to subscribers (simplified)"""
    try:
        # Store the event
        await store_event(event)
        
        # Notify subscribers (simplified)
        event_key = event.event_type
        tenant_key = f"tenant.{event.tenant_id}.{event_key}"
        
        # Check for subscriptions
        matching_subscriptions = []
        for sub_id, sub_data in subscriptions.items():
            if (sub_data.get("event_type") == event_key or 
                sub_data.get("event_type") == tenant_key):
                matching_subscriptions.append(sub_data)
        
        # Simulate notification to subscribers
        for sub in matching_subscriptions:
            logger.info(
                "Notifying subscriber",
                service_name=sub.get("service_name"),
                event_type=event.event_type
            )
        
        metrics["events_published"] += 1
        return True
    
    except Exception as e:
        logger.error("Failed to publish event", error=str(e))
        metrics["events_failed"] += 1
        return False


async def create_subscription(
    event_type: str,
    service_name: str,
    tenant_id: Optional[UUID] = None,
    filters: Optional[Dict[str, Any]] = None,
    webhook_url: Optional[str] = None
) -> str:
    """Create a new subscription"""
    subscription_id = str(uuid4())
    
    subscription_data = {
        "subscription_id": subscription_id,
        "event_type": event_type,
        "service_name": service_name,
        "tenant_id": str(tenant_id) if tenant_id else None,
        "filters": filters or {},
        "webhook_url": webhook_url,
        "created_at": datetime.utcnow().isoformat()
    }
    
    subscriptions[subscription_id] = subscription_data
    metrics["active_subscriptions"] = len(subscriptions)
    
    logger.info(
        "Subscription created",
        subscription_id=subscription_id,
        event_type=event_type,
        service_name=service_name
    )
    
    return subscription_id


# Application lifespan management

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting BizOSaaS Event Bus Service")
    
    try:
        # Initialize Redis
        await initialize_redis()
        logger.info("Event Bus Service started successfully")
        
        yield
        
    except Exception as e:
        logger.error("Failed to start Event Bus Service", error=str(e))
        raise
    
    finally:
        # Cleanup
        if redis_client:
            await redis_client.aclose()
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
            "subscriptions": "/subscriptions",
            "metrics": "/metrics",
            "health": "/health"
        }
    }


@app.post("/events/publish", response_model=PublishEventResponse)
async def publish_event(request: PublishEventRequest):
    """Publish an event to the event bus"""
    try:
        # Create event
        event = BaseEvent(
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
        
        # Publish event
        success = await publish_event_internal(event)
        
        if success:
            return PublishEventResponse(
                success=True,
                event_id=event.event_id
            )
        else:
            raise HTTPException(status_code=400, detail="Failed to publish event")
    
    except Exception as e:
        logger.error("Failed to publish event", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/events/subscribe", response_model=SubscribeResponse)
async def subscribe_to_events(request: SubscribeRequest):
    """Subscribe to events"""
    try:
        subscription_id = await create_subscription(
            event_type=request.event_type,
            service_name=request.service_name,
            tenant_id=request.tenant_id,
            filters=request.filters,
            webhook_url=request.webhook_url
        )
        
        return SubscribeResponse(subscription_id=subscription_id)
    
    except Exception as e:
        logger.error("Failed to create subscription", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/events/subscribe/{subscription_id}")
async def unsubscribe_from_events(subscription_id: str):
    """Unsubscribe from events"""
    try:
        if subscription_id in subscriptions:
            del subscriptions[subscription_id]
            metrics["active_subscriptions"] = len(subscriptions)
            return {"message": "Unsubscribed successfully", "subscription_id": subscription_id}
        else:
            raise HTTPException(status_code=404, detail="Subscription not found")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to unsubscribe", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/events/history")
async def get_event_history(request: EventHistoryRequest):
    """Get event history for a tenant"""
    try:
        # Filter events by tenant
        tenant_events = []
        for event_id, event_data in event_store.items():
            if event_data.get("tenant_id") == str(request.tenant_id):
                # Apply additional filters
                include_event = True
                
                if request.event_types:
                    if event_data.get("event_type") not in request.event_types:
                        include_event = False
                
                if request.aggregate_id:
                    if event_data.get("aggregate_id") != str(request.aggregate_id):
                        include_event = False
                
                if include_event:
                    tenant_events.append(event_data)
        
        # Sort by timestamp and apply limit
        tenant_events.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        tenant_events = tenant_events[:request.limit]
        
        return {
            "events": tenant_events,
            "count": len(tenant_events),
            "tenant_id": str(request.tenant_id),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error("Failed to get event history", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/subscriptions")
async def get_subscriptions():
    """Get all subscriptions"""
    return {
        "subscriptions": list(subscriptions.values()),
        "count": len(subscriptions),
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/subscriptions/stats")
async def get_subscription_statistics():
    """Get subscription statistics"""
    # Calculate stats
    subscriptions_by_service = {}
    subscriptions_by_event_type = {}
    
    for sub_data in subscriptions.values():
        service = sub_data.get("service_name", "unknown")
        event_type = sub_data.get("event_type", "unknown")
        
        subscriptions_by_service[service] = subscriptions_by_service.get(service, 0) + 1
        subscriptions_by_event_type[event_type] = subscriptions_by_event_type.get(event_type, 0) + 1
    
    return {
        "total_subscriptions": len(subscriptions),
        "active_subscriptions": len(subscriptions),
        "subscriptions_by_service": subscriptions_by_service,
        "subscriptions_by_event_type": subscriptions_by_event_type,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/metrics")
async def get_metrics():
    """Get event bus metrics"""
    return {
        **metrics,
        "event_store_size": len(event_store),
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    try:
        components = {}
        overall_status = "healthy"
        
        # Check Redis
        if redis_client:
            try:
                await redis_client.ping()
                components["redis"] = {"status": "healthy"}
            except Exception as e:
                components["redis"] = {"status": "unhealthy", "error": str(e)}
                overall_status = "unhealthy"
        else:
            components["redis"] = {"status": "not_connected"}
        
        # Check event store
        components["event_store"] = {
            "status": "healthy",
            "size": len(event_store)
        }
        
        # Check subscriptions
        components["subscriptions"] = {
            "status": "healthy", 
            "count": len(subscriptions)
        }
        
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
        "event_categories": [category.value for category in EventCategory],
        "event_priorities": [priority.value for priority in EventPriority],
        "event_statuses": [status.value for status in EventStatus],
        "example_event_types": [
            "lead.created",
            "lead.qualified", 
            "campaign.launched",
            "ai.analysis_requested",
            "ai.analysis_completed",
            "agent.task_assigned",
            "agent.task_completed"
        ]
    }


# Demo endpoints for testing

@app.post("/demo/create-lead")
async def demo_create_lead(
    tenant_id: UUID,
    contact_info: Dict[str, Any] = {"email": "demo@example.com", "company": "Demo Corp"}
):
    """Demo endpoint to create a lead and trigger events"""
    lead_id = uuid4()
    
    # Publish lead created event
    event = BaseEvent(
        event_type="lead.created",
        tenant_id=tenant_id,
        source_service="demo-service",
        data={
            "lead_id": str(lead_id),
            "contact_info": contact_info,
            "source": "demo_api"
        },
        category=EventCategory.LEAD,
        priority=EventPriority.HIGH
    )
    
    success = await publish_event_internal(event)
    
    return {
        "lead_id": str(lead_id),
        "event_published": success,
        "event_id": str(event.event_id)
    }


@app.post("/demo/ai-analysis")
async def demo_ai_analysis(
    tenant_id: UUID,
    analysis_type: str = "lead_scoring",
    target_id: Optional[UUID] = None
):
    """Demo endpoint to request AI analysis"""
    if not target_id:
        target_id = uuid4()
    
    # Publish analysis request
    event = BaseEvent(
        event_type="ai.analysis_requested",
        tenant_id=tenant_id,
        source_service="demo-service",
        data={
            "analysis_type": analysis_type,
            "target_id": str(target_id),
            "parameters": {"demo": True}
        },
        category=EventCategory.AI_ANALYSIS,
        priority=EventPriority.HIGH
    )
    
    success = await publish_event_internal(event)
    
    # Simulate AI completion (in real system, this would be handled by AI service)
    if success:
        await asyncio.sleep(1)  # Simulate processing time
        
        completion_event = BaseEvent(
            event_type="ai.analysis_completed", 
            tenant_id=tenant_id,
            source_service="ai-agents",
            data={
                "analysis_id": str(uuid4()),
                "analysis_type": analysis_type,
                "target_id": str(target_id),
                "results": {
                    "score": 85,
                    "confidence": 92,
                    "recommendations": ["High priority lead", "Follow up within 24 hours"]
                }
            },
            category=EventCategory.AI_ANALYSIS,
            correlation_id=event.event_id
        )
        
        await publish_event_internal(completion_event)
        
        return {
            "analysis_requested": True,
            "request_event_id": str(event.event_id),
            "completion_event_id": str(completion_event.event_id),
            "target_id": str(target_id)
        }
    
    return {
        "analysis_requested": False,
        "error": "Failed to publish event"
    }


if __name__ == "__main__":
    uvicorn.run(
        "standalone_main:app",
        host="0.0.0.0",
        port=settings.service_port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )