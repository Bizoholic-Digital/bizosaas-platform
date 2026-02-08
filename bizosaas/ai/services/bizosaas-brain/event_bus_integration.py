"""
Event Bus Integration for BizOSaaS Brain API

Integrates the advanced Event Bus tenant isolation system with the Brain API
for unified tenant-aware event publishing and subscription management.
"""

import asyncio
import os
import httpx
from typing import Dict, Any, List, Optional, Union
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field
import structlog

# Import unified tenant system
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from unified_tenant_middleware import UnifiedTenant, TenantNotFoundError

logger = structlog.get_logger(__name__)


class EventBusMessage(BaseModel):
    """Event Bus message model for Brain API integration"""
    event_type: str = Field(..., description="Type of event to publish")
    tenant_id: Union[str, UUID] = Field(..., description="Tenant ID for multi-tenancy")
    data: Dict[str, Any] = Field(default_factory=dict, description="Event payload")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Event metadata")
    priority: str = Field(default="normal", description="Event priority: low, normal, high, critical")
    target_services: List[str] = Field(default_factory=list, description="Target services")
    source_service: str = Field(default="brain-api", description="Source service name")
    correlation_id: Optional[UUID] = Field(None, description="Correlation ID")
    aggregate_id: Optional[UUID] = Field(None, description="Aggregate ID")
    aggregate_type: Optional[str] = Field(None, description="Aggregate type")


class EventBusSubscription(BaseModel):
    """Event Bus subscription model"""
    event_type: str = Field(..., description="Event type to subscribe to")
    service_name: str = Field(..., description="Name of subscribing service")
    tenant_id: Optional[Union[str, UUID]] = Field(None, description="Tenant ID for tenant-specific subscriptions")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Event filters")
    webhook_url: Optional[str] = Field(None, description="Webhook URL for notifications")


class BrainEventBusClient:
    """
    Brain API Event Bus client with unified tenant integration
    
    Provides a high-level interface for the Brain API to interact with
    the Event Bus while ensuring proper tenant isolation and context.
    """
    
    def __init__(
        self,
        event_bus_url: str = None,
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.event_bus_url = event_bus_url or os.getenv(
            'EVENT_BUS_URL', 
            'http://localhost:8009'
        )
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = logger.bind(component="brain_event_bus_client")
        
        # HTTP client for Event Bus communication
        self.http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            headers={
                "User-Agent": "BizOSaaS-Brain-API/2.0.0",
                "Content-Type": "application/json"
            }
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.http_client.aclose()
    
    async def publish_tenant_event(
        self,
        tenant: UnifiedTenant,
        event_type: str,
        data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
        priority: str = "normal",
        target_services: Optional[List[str]] = None,
        correlation_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """
        Publish an event with unified tenant context
        
        Args:
            tenant: Unified tenant object
            event_type: Type of event to publish
            data: Event payload data
            metadata: Additional event metadata
            priority: Event priority (low, normal, high, critical)
            target_services: Specific services to target
            correlation_id: Optional correlation ID for tracking
            
        Returns:
            Event publishing response from Event Bus
        """
        try:
            # Prepare event message with tenant context
            event_message = EventBusMessage(
                event_type=event_type,
                tenant_id=tenant.tenant_uuid,
                data=data,
                metadata={
                    **(metadata or {}),
                    "tenant_context": {
                        "tenant_id": tenant.tenant_id,
                        "tenant_uuid": str(tenant.tenant_uuid),
                        "tenant_slug": tenant.slug,
                        "tenant_name": tenant.name,
                        "subscription_tier": tenant.subscription_tier.value,
                        "status": tenant.status.value,
                        "primary_domain": tenant.primary_domain
                    },
                    "published_by": "brain-api",
                    "published_at": datetime.now().isoformat()
                },
                priority=priority,
                target_services=target_services or [],
                correlation_id=correlation_id or uuid4()
            )
            
            # Convert UUID to string for JSON serialization
            event_data = event_message.model_dump()
            if isinstance(event_data['tenant_id'], UUID):
                event_data['tenant_id'] = str(event_data['tenant_id'])
            if event_data.get('correlation_id') and isinstance(event_data['correlation_id'], UUID):
                event_data['correlation_id'] = str(event_data['correlation_id'])
            
            # Publish to Event Bus
            response = await self.http_client.post(
                f"{self.event_bus_url}/api/events/publish",
                json=event_data
            )
            
            if response.status_code == 200:
                result = response.json()
                self.logger.info(
                    "Event published successfully",
                    event_type=event_type,
                    tenant_slug=tenant.slug,
                    event_id=result.get('event_id'),
                    correlation_id=str(correlation_id) if correlation_id else None
                )
                return result
            else:
                error_msg = f"Event Bus publish failed: {response.status_code} - {response.text}"
                self.logger.error(error_msg, tenant_slug=tenant.slug, event_type=event_type)
                raise Exception(error_msg)
                
        except Exception as e:
            self.logger.error(
                "Failed to publish tenant event",
                error=str(e),
                tenant_slug=tenant.slug,
                event_type=event_type
            )
            raise
    
    async def create_tenant_subscription(
        self,
        tenant: UnifiedTenant,
        event_type: str,
        service_name: str,
        filters: Optional[Dict[str, Any]] = None,
        webhook_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a tenant-specific event subscription
        
        Args:
            tenant: Unified tenant object
            event_type: Event type to subscribe to
            service_name: Name of the subscribing service
            filters: Optional filters for events
            webhook_url: Optional webhook URL for notifications
            
        Returns:
            Subscription creation response
        """
        try:
            subscription = EventBusSubscription(
                event_type=event_type,
                service_name=service_name,
                tenant_id=tenant.tenant_uuid,
                filters={
                    **(filters or {}),
                    "tenant_context.tenant_slug": tenant.slug,
                    "tenant_context.tenant_uuid": str(tenant.tenant_uuid)
                },
                webhook_url=webhook_url
            )
            
            subscription_data = subscription.model_dump()
            if isinstance(subscription_data['tenant_id'], UUID):
                subscription_data['tenant_id'] = str(subscription_data['tenant_id'])
            
            response = await self.http_client.post(
                f"{self.event_bus_url}/api/subscriptions",
                json=subscription_data
            )
            
            if response.status_code == 200:
                result = response.json()
                self.logger.info(
                    "Tenant subscription created",
                    event_type=event_type,
                    tenant_slug=tenant.slug,
                    service_name=service_name,
                    subscription_id=result.get('subscription_id')
                )
                return result
            else:
                error_msg = f"Subscription creation failed: {response.status_code} - {response.text}"
                self.logger.error(error_msg, tenant_slug=tenant.slug, event_type=event_type)
                raise Exception(error_msg)
                
        except Exception as e:
            self.logger.error(
                "Failed to create tenant subscription",
                error=str(e),
                tenant_slug=tenant.slug,
                event_type=event_type
            )
            raise
    
    async def get_tenant_events(
        self,
        tenant: UnifiedTenant,
        event_types: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get event history for a specific tenant
        
        Args:
            tenant: Unified tenant object
            event_types: Optional list of event types to filter
            limit: Maximum number of events to return
            offset: Offset for pagination
            start_time: Optional start time filter
            end_time: Optional end time filter
            
        Returns:
            Event history response
        """
        try:
            params = {
                "tenant_id": str(tenant.tenant_uuid),
                "limit": limit,
                "offset": offset
            }
            
            if event_types:
                params["event_types"] = ",".join(event_types)
            if start_time:
                params["start_time"] = start_time.isoformat()
            if end_time:
                params["end_time"] = end_time.isoformat()
            
            response = await self.http_client.get(
                f"{self.event_bus_url}/api/events/history",
                params=params
            )
            
            if response.status_code == 200:
                result = response.json()
                self.logger.info(
                    "Retrieved tenant event history",
                    tenant_slug=tenant.slug,
                    event_count=len(result.get('events', [])),
                    total_count=result.get('total_count', 0)
                )
                return result
            else:
                error_msg = f"Event history retrieval failed: {response.status_code} - {response.text}"
                self.logger.error(error_msg, tenant_slug=tenant.slug)
                raise Exception(error_msg)
                
        except Exception as e:
            self.logger.error(
                "Failed to get tenant events",
                error=str(e),
                tenant_slug=tenant.slug
            )
            raise
    
    async def get_tenant_metrics(
        self,
        tenant: UnifiedTenant,
        time_range: str = "24h"
    ) -> Dict[str, Any]:
        """
        Get event metrics for a specific tenant
        
        Args:
            tenant: Unified tenant object
            time_range: Time range for metrics (1h, 24h, 7d, 30d)
            
        Returns:
            Tenant event metrics
        """
        try:
            params = {
                "tenant_id": str(tenant.tenant_uuid),
                "time_range": time_range
            }
            
            response = await self.http_client.get(
                f"{self.event_bus_url}/api/metrics/tenant",
                params=params
            )
            
            if response.status_code == 200:
                result = response.json()
                self.logger.info(
                    "Retrieved tenant event metrics",
                    tenant_slug=tenant.slug,
                    time_range=time_range
                )
                return result
            else:
                error_msg = f"Metrics retrieval failed: {response.status_code} - {response.text}"
                self.logger.error(error_msg, tenant_slug=tenant.slug)
                raise Exception(error_msg)
                
        except Exception as e:
            self.logger.error(
                "Failed to get tenant metrics",
                error=str(e),
                tenant_slug=tenant.slug
            )
            raise
    
    async def health_check(self) -> Dict[str, Any]:
        """Check Event Bus health status"""
        try:
            response = await self.http_client.get(
                f"{self.event_bus_url}/health"
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "status": "unhealthy",
                    "error": f"Status code: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


# Global Event Bus client instance
_event_bus_client: Optional[BrainEventBusClient] = None


async def get_event_bus_client() -> BrainEventBusClient:
    """Get or create the global Event Bus client"""
    global _event_bus_client
    
    if _event_bus_client is None:
        _event_bus_client = BrainEventBusClient()
    
    return _event_bus_client


async def publish_brain_event(
    tenant: UnifiedTenant,
    event_type: str,
    data: Dict[str, Any],
    **kwargs
) -> Dict[str, Any]:
    """
    Convenience function for publishing events from Brain API
    
    Args:
        tenant: Unified tenant object
        event_type: Type of event to publish
        data: Event data payload
        **kwargs: Additional arguments passed to publish_tenant_event
        
    Returns:
        Event publishing response
    """
    client = await get_event_bus_client()
    return await client.publish_tenant_event(
        tenant=tenant,
        event_type=event_type,
        data=data,
        **kwargs
    )


# Common event types for Brain API operations
class BrainEventTypes:
    """Standard event types used by the Brain API"""
    
    # Tenant events
    TENANT_CREATED = "brain.tenant.created"
    TENANT_UPDATED = "brain.tenant.updated"
    TENANT_ACTIVATED = "brain.tenant.activated"
    TENANT_DEACTIVATED = "brain.tenant.deactivated"
    
    # Service events
    SERVICE_HEALTH_CHECK = "brain.service.health_check"
    SERVICE_ROUTE_ACCESSED = "brain.service.route_accessed"
    SERVICE_ERROR = "brain.service.error"
    
    # Business events
    LEAD_CREATED = "brain.business.lead_created"
    CAMPAIGN_STARTED = "brain.business.campaign_started"
    REPORT_GENERATED = "brain.business.report_generated"
    
    # AI Agent events
    AI_AGENT_TRIGGERED = "brain.ai.agent_triggered"
    AI_AGENT_COMPLETED = "brain.ai.agent_completed"
    AI_AGENT_FAILED = "brain.ai.agent_failed"
    
    # Integration events
    EXTERNAL_API_CALLED = "brain.integration.api_called"
    WEBHOOK_RECEIVED = "brain.integration.webhook_received"
    SYNC_COMPLETED = "brain.integration.sync_completed"
    
    # Security events
    AUTHENTICATION_SUCCESS = "brain.security.auth_success"
    AUTHENTICATION_FAILED = "brain.security.auth_failed"
    PERMISSION_DENIED = "brain.security.permission_denied"
    
    # Personal AI Assistant events
    ASSISTANT_TASK_CREATED = "brain.assistant.task_created"
    ASSISTANT_TASK_UPDATED = "brain.assistant.task_updated"
    ASSISTANT_TASK_COMPLETED = "brain.assistant.task_completed"
    MOBILE_COMMAND_PROCESSED = "brain.assistant.mobile_command"
    WORKFLOW_EXECUTED = "brain.assistant.workflow_executed"
    CLIENT_INQUIRY_RECEIVED = "brain.assistant.client_inquiry"
    CODE_REVIEW_COMPLETED = "brain.assistant.code_review"
    DAILY_REPORT_GENERATED = "brain.assistant.daily_report"
    STRATEGIC_INSIGHTS_GENERATED = "brain.assistant.strategic_insights"


# Event publishing helpers for common Brain API operations
async def publish_tenant_activity(
    tenant: UnifiedTenant,
    activity_type: str,
    activity_data: Dict[str, Any],
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """Publish tenant activity event"""
    return await publish_brain_event(
        tenant=tenant,
        event_type=f"brain.tenant.activity.{activity_type}",
        data={
            "activity_type": activity_type,
            "user_id": user_id,
            **activity_data
        },
        metadata={
            "category": "tenant_activity",
            "source": "brain_api"
        }
    )


async def publish_service_metrics(
    tenant: UnifiedTenant,
    service_name: str,
    metrics: Dict[str, Any]
) -> Dict[str, Any]:
    """Publish service performance metrics"""
    return await publish_brain_event(
        tenant=tenant,
        event_type=BrainEventTypes.SERVICE_HEALTH_CHECK,
        data={
            "service_name": service_name,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        },
        metadata={
            "category": "service_metrics",
            "service": service_name
        }
    )


async def publish_ai_agent_result(
    tenant: UnifiedTenant,
    agent_name: str,
    result: Dict[str, Any],
    execution_time_ms: int,
    success: bool = True
) -> Dict[str, Any]:
    """Publish AI agent execution result"""
    event_type = BrainEventTypes.AI_AGENT_COMPLETED if success else BrainEventTypes.AI_AGENT_FAILED
    
    return await publish_brain_event(
        tenant=tenant,
        event_type=event_type,
        data={
            "agent_name": agent_name,
            "result": result,
            "execution_time_ms": execution_time_ms,
            "success": success
        },
        metadata={
            "category": "ai_agent",
            "agent": agent_name
        },
        priority="high" if not success else "normal"
    )