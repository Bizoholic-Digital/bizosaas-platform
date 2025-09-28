"""
Client SDK for BizOSaaS Event Bus

Provides easy-to-use clients for services to interact with the event bus,
including publishing events, subscribing to events, and managing subscriptions.
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Union
from uuid import UUID, uuid4

import aiohttp
import websockets
from pydantic import BaseModel, ValidationError
import structlog

from domain_events import BaseEvent, EventPriority, create_event

logger = structlog.get_logger(__name__)


class EventBusClientConfig(BaseModel):
    """Configuration for Event Bus Client"""
    base_url: str = "http://localhost:8003"
    service_name: str
    api_key: Optional[str] = None
    timeout_seconds: int = 30
    max_retries: int = 3
    enable_websocket: bool = True
    websocket_url: Optional[str] = None


class EventBusClient:
    """
    Client SDK for BizOSaaS Event Bus
    
    Provides methods to:
    - Publish events
    - Subscribe to events
    - Query event history
    - Manage subscriptions
    """
    
    def __init__(self, config: EventBusClientConfig):
        self.config = config
        self.logger = logger.bind(
            component="eventbus_client",
            service_name=config.service_name
        )
        
        # HTTP session
        self.session: Optional[aiohttp.ClientSession] = None
        
        # WebSocket connection for real-time subscriptions
        self.websocket: Optional[websockets.WebSocketServerProtocol] = None
        self.subscription_handlers: Dict[str, Callable] = {}
        
        # Connection state
        self.is_connected = False
    
    async def connect(self) -> None:
        """Initialize client connection"""
        try:
            # Create HTTP session
            timeout = aiohttp.ClientTimeout(total=self.config.timeout_seconds)
            headers = {"Content-Type": "application/json"}
            
            if self.config.api_key:
                headers["Authorization"] = f"Bearer {self.config.api_key}"
            
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                headers=headers
            )
            
            # Test connection
            await self._health_check()
            
            self.is_connected = True
            self.logger.info("Event Bus client connected")
            
        except Exception as e:
            self.logger.error("Failed to connect to Event Bus", error=str(e))
            raise
    
    async def disconnect(self) -> None:
        """Close client connections"""
        try:
            if self.websocket:
                await self.websocket.close()
                self.websocket = None
            
            if self.session:
                await self.session.close()
                self.session = None
            
            self.is_connected = False
            self.logger.info("Event Bus client disconnected")
            
        except Exception as e:
            self.logger.error("Error disconnecting from Event Bus", error=str(e))
    
    async def publish_event(
        self,
        event_type: str,
        tenant_id: UUID,
        data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
        priority: EventPriority = EventPriority.NORMAL,
        target_services: Optional[List[str]] = None,
        correlation_id: Optional[UUID] = None,
        aggregate_id: Optional[UUID] = None,
        aggregate_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Publish an event to the event bus
        
        Args:
            event_type: Type of event (e.g., 'lead.created')
            tenant_id: Tenant UUID for multi-tenancy
            data: Event payload data
            metadata: Optional event metadata
            priority: Event priority level
            target_services: List of target services
            correlation_id: Optional correlation ID
            aggregate_id: Optional aggregate ID
            aggregate_type: Optional aggregate type
            
        Returns:
            Response from event bus with event ID and status
        """
        if not self.is_connected:
            await self.connect()
        
        try:
            payload = {
                "event_type": event_type,
                "tenant_id": str(tenant_id),
                "source_service": self.config.service_name,
                "data": data,
                "metadata": metadata or {},
                "priority": priority.value,
                "target_services": target_services or [],
                "correlation_id": str(correlation_id) if correlation_id else None,
                "aggregate_id": str(aggregate_id) if aggregate_id else None,
                "aggregate_type": aggregate_type
            }
            
            async with self.session.post(
                f"{self.config.base_url}/events/publish",
                json=payload
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    self.logger.info(
                        "Event published",
                        event_type=event_type,
                        event_id=result.get("event_id"),
                        tenant_id=str(tenant_id)
                    )
                    return result
                else:
                    error_text = await response.text()
                    self.logger.error(
                        "Failed to publish event",
                        status_code=response.status,
                        error=error_text
                    )
                    raise Exception(f"HTTP {response.status}: {error_text}")
        
        except Exception as e:
            self.logger.error("Error publishing event", error=str(e))
            raise
    
    async def subscribe_to_events(
        self,
        event_type: str,
        handler: Callable[[BaseEvent], None],
        tenant_id: Optional[UUID] = None,
        filters: Optional[Dict[str, Any]] = None,
        webhook_url: Optional[str] = None
    ) -> str:
        """
        Subscribe to events
        
        Args:
            event_type: Event type to subscribe to (supports wildcards)
            handler: Function to handle received events
            tenant_id: Optional tenant ID for tenant-specific subscriptions
            filters: Optional event filters
            webhook_url: Optional webhook URL for HTTP notifications
            
        Returns:
            Subscription ID
        """
        if not self.is_connected:
            await self.connect()
        
        try:
            payload = {
                "event_type": event_type,
                "service_name": self.config.service_name,
                "tenant_id": str(tenant_id) if tenant_id else None,
                "filters": filters or {},
                "webhook_url": webhook_url
            }
            
            async with self.session.post(
                f"{self.config.base_url}/events/subscribe",
                json=payload
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    subscription_id = result["subscription_id"]
                    
                    # Store handler for WebSocket notifications
                    self.subscription_handlers[subscription_id] = handler
                    
                    self.logger.info(
                        "Subscription created",
                        event_type=event_type,
                        subscription_id=subscription_id
                    )
                    
                    return subscription_id
                else:
                    error_text = await response.text()
                    raise Exception(f"HTTP {response.status}: {error_text}")
        
        except Exception as e:
            self.logger.error("Error subscribing to events", error=str(e))
            raise
    
    async def unsubscribe(self, subscription_id: str) -> bool:
        """
        Unsubscribe from events
        
        Args:
            subscription_id: ID of subscription to cancel
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected:
            await self.connect()
        
        try:
            async with self.session.delete(
                f"{self.config.base_url}/events/subscribe/{subscription_id}"
            ) as response:
                success = response.status == 200
                
                if success:
                    # Remove local handler
                    self.subscription_handlers.pop(subscription_id, None)
                    
                    self.logger.info("Unsubscribed", subscription_id=subscription_id)
                else:
                    error_text = await response.text()
                    self.logger.error(
                        "Failed to unsubscribe",
                        subscription_id=subscription_id,
                        error=error_text
                    )
                
                return success
        
        except Exception as e:
            self.logger.error("Error unsubscribing", error=str(e))
            return False
    
    async def get_event_history(
        self,
        tenant_id: UUID,
        event_types: Optional[List[str]] = None,
        aggregate_id: Optional[UUID] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get event history
        
        Args:
            tenant_id: Tenant ID to query
            event_types: Optional list of event types to filter
            aggregate_id: Optional aggregate ID to filter
            start_time: Optional start time for range query
            end_time: Optional end time for range query
            limit: Maximum number of events to return
            
        Returns:
            List of events
        """
        if not self.is_connected:
            await self.connect()
        
        try:
            payload = {
                "tenant_id": str(tenant_id),
                "event_types": event_types,
                "aggregate_id": str(aggregate_id) if aggregate_id else None,
                "start_time": start_time.isoformat() if start_time else None,
                "end_time": end_time.isoformat() if end_time else None,
                "limit": limit
            }
            
            async with self.session.post(
                f"{self.config.base_url}/events/history",
                json=payload
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("events", [])
                else:
                    error_text = await response.text()
                    raise Exception(f"HTTP {response.status}: {error_text}")
        
        except Exception as e:
            self.logger.error("Error getting event history", error=str(e))
            raise
    
    async def replay_events(
        self,
        tenant_id: UUID,
        event_types: List[str],
        start_time: datetime,
        end_time: Optional[datetime] = None,
        target_service: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Replay events
        
        Args:
            tenant_id: Tenant ID to replay events for
            event_types: List of event types to replay
            start_time: Start time for replay
            end_time: Optional end time for replay
            target_service: Optional specific service to replay to
            
        Returns:
            Replay status information
        """
        if not self.is_connected:
            await self.connect()
        
        try:
            payload = {
                "tenant_id": str(tenant_id),
                "event_types": event_types,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat() if end_time else None,
                "target_service": target_service
            }
            
            async with self.session.post(
                f"{self.config.base_url}/events/replay",
                json=payload
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    self.logger.info(
                        "Event replay started",
                        tenant_id=str(tenant_id),
                        event_types=event_types
                    )
                    return result
                else:
                    error_text = await response.text()
                    raise Exception(f"HTTP {response.status}: {error_text}")
        
        except Exception as e:
            self.logger.error("Error starting event replay", error=str(e))
            raise
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get event bus metrics"""
        if not self.is_connected:
            await self.connect()
        
        try:
            async with self.session.get(
                f"{self.config.base_url}/metrics"
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"HTTP {response.status}: {error_text}")
        
        except Exception as e:
            self.logger.error("Error getting metrics", error=str(e))
            raise
    
    async def get_subscription_stats(self) -> Dict[str, Any]:
        """Get subscription statistics"""
        if not self.is_connected:
            await self.connect()
        
        try:
            async with self.session.get(
                f"{self.config.base_url}/subscriptions/stats"
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"HTTP {response.status}: {error_text}")
        
        except Exception as e:
            self.logger.error("Error getting subscription stats", error=str(e))
            raise
    
    async def _health_check(self) -> bool:
        """Check if event bus is healthy"""
        try:
            async with self.session.get(
                f"{self.config.base_url}/health"
            ) as response:
                if response.status == 200:
                    health_data = await response.json()
                    is_healthy = health_data.get("status") == "healthy"
                    
                    if is_healthy:
                        self.logger.debug("Event bus health check passed")
                    else:
                        self.logger.warning("Event bus health check failed", health_data=health_data)
                    
                    return is_healthy
                else:
                    self.logger.warning("Event bus health check returned non-200", status=response.status)
                    return False
        
        except Exception as e:
            self.logger.error("Event bus health check error", error=str(e))
            return False
    
    # Context manager support
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()


class EventBusServiceMixin:
    """
    Mixin class for services to easily integrate with Event Bus
    
    Provides common patterns for event publishing and subscription
    """
    
    def __init__(self, service_name: str, event_bus_config: EventBusClientConfig):
        self.service_name = service_name
        self.event_bus_client = EventBusClient(event_bus_config)
        self.logger = logger.bind(service_name=service_name)
    
    async def initialize_event_bus(self) -> None:
        """Initialize event bus connection"""
        await self.event_bus_client.connect()
        
        # Subscribe to service-specific events
        await self._setup_event_subscriptions()
        
        self.logger.info("Event bus integration initialized")
    
    async def cleanup_event_bus(self) -> None:
        """Cleanup event bus connection"""
        await self.event_bus_client.disconnect()
        self.logger.info("Event bus integration cleaned up")
    
    async def _setup_event_subscriptions(self) -> None:
        """Override this method to set up service-specific subscriptions"""
        pass
    
    async def publish_domain_event(
        self,
        event_type: str,
        tenant_id: UUID,
        data: Dict[str, Any],
        **kwargs
    ) -> str:
        """Helper method to publish domain events"""
        try:
            result = await self.event_bus_client.publish_event(
                event_type=event_type,
                tenant_id=tenant_id,
                data=data,
                **kwargs
            )
            return result["event_id"]
        
        except Exception as e:
            self.logger.error(
                "Failed to publish domain event",
                event_type=event_type,
                error=str(e)
            )
            raise
    
    async def handle_domain_event(self, event: BaseEvent) -> None:
        """Override this method to handle incoming domain events"""
        self.logger.info(
            "Received domain event",
            event_type=event.event_type,
            event_id=str(event.event_id)
        )


# Helper functions for common event patterns

async def create_event_bus_client(
    service_name: str,
    base_url: str = "http://localhost:8003",
    api_key: Optional[str] = None
) -> EventBusClient:
    """Create and connect an event bus client"""
    config = EventBusClientConfig(
        base_url=base_url,
        service_name=service_name,
        api_key=api_key
    )
    
    client = EventBusClient(config)
    await client.connect()
    return client


def create_typed_event_publisher(event_type: str, client: EventBusClient):
    """Create a typed event publisher function"""
    
    async def publish(tenant_id: UUID, data: Dict[str, Any], **kwargs):
        return await client.publish_event(
            event_type=event_type,
            tenant_id=tenant_id,
            data=data,
            **kwargs
        )
    
    return publish


def create_event_handler(event_type: str):
    """Decorator to create event handlers"""
    
    def decorator(func: Callable[[BaseEvent], None]):
        func._event_type = event_type
        return func
    
    return decorator


# Example usage and helper classes

class AIAgentEventClient(EventBusServiceMixin):
    """Example AI Agent service integration"""
    
    async def _setup_event_subscriptions(self) -> None:
        """Set up AI agent specific subscriptions"""
        
        # Subscribe to analysis requests
        await self.event_bus_client.subscribe_to_events(
            event_type="ai.analysis_requested",
            handler=self._handle_analysis_request
        )
        
        # Subscribe to lead creation for automatic analysis
        await self.event_bus_client.subscribe_to_events(
            event_type="lead.created",
            handler=self._handle_new_lead
        )
    
    async def _handle_analysis_request(self, event: BaseEvent) -> None:
        """Handle AI analysis requests"""
        try:
            analysis_type = event.data.get("analysis_type")
            target_id = event.data.get("target_id")
            
            # Perform analysis (mock)
            results = {"score": 85, "recommendations": ["Optimize keywords", "Increase budget"]}
            
            # Publish analysis completed event
            await self.publish_domain_event(
                event_type="ai.analysis_completed",
                tenant_id=event.tenant_id,
                data={
                    "analysis_id": str(uuid4()),
                    "analysis_type": analysis_type,
                    "target_id": target_id,
                    "results": results
                },
                correlation_id=event.correlation_id
            )
            
        except Exception as e:
            self.logger.error("Failed to handle analysis request", error=str(e))
    
    async def _handle_new_lead(self, event: BaseEvent) -> None:
        """Handle new lead events for automatic analysis"""
        try:
            lead_id = event.data.get("lead_id")
            
            # Trigger automatic lead scoring
            await self.publish_domain_event(
                event_type="ai.analysis_requested",
                tenant_id=event.tenant_id,
                data={
                    "analysis_type": "lead_scoring",
                    "target_id": lead_id,
                    "parameters": {"auto_triggered": True}
                },
                correlation_id=event.event_id
            )
            
        except Exception as e:
            self.logger.error("Failed to handle new lead", error=str(e))


class CRMEventClient(EventBusServiceMixin):
    """Example CRM service integration"""
    
    async def _setup_event_subscriptions(self) -> None:
        """Set up CRM specific subscriptions"""
        
        # Subscribe to lead qualification events
        await self.event_bus_client.subscribe_to_events(
            event_type="lead.qualified",
            handler=self._handle_qualified_lead
        )
        
        # Subscribe to AI analysis completion
        await self.event_bus_client.subscribe_to_events(
            event_type="ai.analysis_completed",
            handler=self._handle_analysis_results
        )
    
    async def _handle_qualified_lead(self, event: BaseEvent) -> None:
        """Handle qualified lead events"""
        lead_id = event.data.get("lead_id")
        qualification_score = event.data.get("qualification_score", 0)
        
        if qualification_score > 80:
            # Create opportunity
            await self.publish_domain_event(
                event_type="opportunity.created",
                tenant_id=event.tenant_id,
                data={
                    "opportunity_id": str(uuid4()),
                    "lead_id": lead_id,
                    "score": qualification_score,
                    "source": "ai_qualification"
                }
            )
    
    async def _handle_analysis_results(self, event: BaseEvent) -> None:
        """Handle AI analysis results"""
        analysis_type = event.data.get("analysis_type")
        results = event.data.get("results", {})
        
        if analysis_type == "lead_scoring":
            # Update lead with AI score
            lead_id = event.data.get("target_id")
            score = results.get("score", 0)
            
            # In real implementation, update database
            self.logger.info(
                "Updating lead with AI score",
                lead_id=lead_id,
                score=score
            )