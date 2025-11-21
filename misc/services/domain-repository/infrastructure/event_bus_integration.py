"""
Event Bus Integration for Domain Repository Service

This module provides integration with the BizOSaaS Event Bus for publishing
domain events when aggregates change.
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from uuid import UUID

import httpx
import structlog
from pydantic import BaseModel

from .domain.base import DomainEvent, EventPublisher

logger = structlog.get_logger(__name__)


class EventBusConfig(BaseModel):
    """Configuration for Event Bus integration"""
    
    base_url: str = "http://localhost:8009"  # Event Bus service URL
    service_name: str = "domain-repository"
    timeout_seconds: int = 30
    max_retries: int = 3
    enable_publishing: bool = True


class EventBusClient:
    """Client for interacting with the BizOSaaS Event Bus"""
    
    def __init__(self, config: EventBusConfig):
        self.config = config
        self.logger = logger.bind(
            component="eventbus_client",
            service_name=config.service_name
        )
        
        # HTTP client for REST API calls
        self.http_client: Optional[httpx.AsyncClient] = None
    
    async def start(self) -> None:
        """Initialize the event bus client"""
        
        if not self.config.enable_publishing:
            self.logger.info("Event publishing disabled")
            return
        
        try:
            timeout = httpx.Timeout(self.config.timeout_seconds)
            self.http_client = httpx.AsyncClient(
                base_url=self.config.base_url,
                timeout=timeout,
                headers={
                    "Content-Type": "application/json",
                    "X-Service-Name": self.config.service_name
                }
            )
            
            # Test connection
            await self._health_check()
            
            self.logger.info("Event Bus client initialized successfully")
            
        except Exception as e:
            self.logger.error("Failed to initialize Event Bus client", error=str(e))
            raise
    
    async def stop(self) -> None:
        """Cleanup the event bus client"""
        
        if self.http_client:
            await self.http_client.aclose()
            self.http_client = None
        
        self.logger.info("Event Bus client stopped")
    
    async def publish_event(self, event: DomainEvent) -> bool:
        """Publish a single domain event"""
        
        if not self.config.enable_publishing or not self.http_client:
            self.logger.debug("Event publishing disabled, skipping event", event_type=event.event_type)
            return True
        
        try:
            # Convert domain event to Event Bus format
            event_data = self._convert_to_event_bus_format(event)
            
            # Publish to Event Bus
            response = await self.http_client.post(
                "/api/v1/events/publish",
                json=event_data
            )
            
            if response.status_code == 200:
                self.logger.info(
                    "Event published successfully",
                    event_id=str(event.event_id),
                    event_type=event.event_type,
                    aggregate_id=str(event.aggregate_id)
                )
                return True
            else:
                self.logger.error(
                    "Failed to publish event",
                    event_id=str(event.event_id),
                    event_type=event.event_type,
                    status_code=response.status_code,
                    response_text=response.text
                )
                return False
                
        except Exception as e:
            self.logger.error(
                "Exception while publishing event",
                event_id=str(event.event_id),
                event_type=event.event_type,
                error=str(e)
            )
            return False
    
    async def publish_events(self, events: List[DomainEvent]) -> int:
        """Publish multiple domain events"""
        
        if not events:
            return 0
        
        if not self.config.enable_publishing or not self.http_client:
            self.logger.debug("Event publishing disabled, skipping events", event_count=len(events))
            return len(events)  # Pretend success when disabled
        
        try:
            # Convert all events to Event Bus format
            events_data = [self._convert_to_event_bus_format(event) for event in events]
            
            # Publish batch to Event Bus
            response = await self.http_client.post(
                "/api/v1/events/publish-batch",
                json={"events": events_data}
            )
            
            if response.status_code == 200:
                response_data = response.json()
                published_count = response_data.get("published_count", 0)
                
                self.logger.info(
                    "Events published successfully",
                    total_events=len(events),
                    published_count=published_count
                )
                
                return published_count
            else:
                self.logger.error(
                    "Failed to publish events batch",
                    event_count=len(events),
                    status_code=response.status_code,
                    response_text=response.text
                )
                return 0
                
        except Exception as e:
            self.logger.error(
                "Exception while publishing events batch",
                event_count=len(events),
                error=str(e)
            )
            return 0
    
    async def _health_check(self) -> None:
        """Check if Event Bus is healthy"""
        
        if not self.http_client:
            raise RuntimeError("HTTP client not initialized")
        
        try:
            response = await self.http_client.get("/health")
            
            if response.status_code != 200:
                raise RuntimeError(f"Event Bus health check failed: {response.status_code}")
            
            self.logger.debug("Event Bus health check passed")
            
        except httpx.RequestError as e:
            raise RuntimeError(f"Failed to connect to Event Bus: {e}")
    
    def _convert_to_event_bus_format(self, domain_event: DomainEvent) -> Dict[str, Any]:
        """Convert domain event to Event Bus expected format"""
        
        # Map domain event fields to Event Bus fields
        event_data = {
            "event_id": str(domain_event.event_id),
            "event_type": domain_event.event_type,
            "event_version": "1.0",
            "timestamp": domain_event.occurred_at.isoformat(),
            "tenant_id": str(domain_event.tenant_id),
            "source_service": self.config.service_name,
            "aggregate_id": str(domain_event.aggregate_id),
            "aggregate_type": domain_event.aggregate_type,
            "data": domain_event.data,
            "metadata": domain_event.metadata,
            "category": self._get_event_category(domain_event.event_type),
            "priority": self._get_event_priority(domain_event.event_type),
            "target_services": self._get_target_services(domain_event.event_type)
        }
        
        return event_data
    
    def _get_event_category(self, event_type: str) -> str:
        """Get event category based on event type"""
        
        if event_type.startswith("lead."):
            return "lead"
        elif event_type.startswith("customer."):
            return "user"  # Customer events map to user category
        elif event_type.startswith("campaign."):
            return "campaign"
        elif event_type.startswith("product."):
            return "system"
        elif event_type.startswith("order."):
            return "billing"
        else:
            return "system"
    
    def _get_event_priority(self, event_type: str) -> str:
        """Get event priority based on event type"""
        
        # High priority events
        high_priority_events = [
            "lead.created",
            "lead.converted",
            "customer.created",
            "customer.churned",
            "campaign.launched",
            "order.completed",
            "order.refunded"
        ]
        
        # Critical priority events
        critical_priority_events = [
            "customer.churn_risk_updated",
            "campaign.budget_exceeded",
            "order.payment_failed"
        ]
        
        if event_type in critical_priority_events:
            return "critical"
        elif event_type in high_priority_events:
            return "high"
        else:
            return "normal"
    
    def _get_target_services(self, event_type: str) -> List[str]:
        """Get target services that should receive this event"""
        
        target_services = []
        
        # Lead events
        if event_type.startswith("lead."):
            target_services.extend(["ai-agents", "crm-service", "analytics-service"])
        
        # Customer events
        elif event_type.startswith("customer."):
            target_services.extend(["ai-agents", "crm-service", "analytics-service", "marketing-automation"])
        
        # Campaign events
        elif event_type.startswith("campaign."):
            target_services.extend(["ai-agents", "analytics-service", "marketing-automation"])
            
            # Budget exceeded events should also go to billing
            if "budget" in event_type:
                target_services.append("billing-service")
        
        # Product events
        elif event_type.startswith("product."):
            target_services.extend(["analytics-service", "inventory-service"])
        
        # Order events
        elif event_type.startswith("order."):
            target_services.extend(["billing-service", "analytics-service", "fulfillment-service"])
        
        return target_services


class DomainEventPublisher(EventPublisher):
    """Implementation of EventPublisher using Event Bus"""
    
    def __init__(self, event_bus_client: EventBusClient):
        self.event_bus_client = event_bus_client
        self.logger = logger.bind(component="domain_event_publisher")
    
    async def publish(self, event: DomainEvent) -> None:
        """Publish a single domain event"""
        
        success = await self.event_bus_client.publish_event(event)
        
        if not success:
            self.logger.error(
                "Failed to publish domain event",
                event_id=str(event.event_id),
                event_type=event.event_type
            )
            # In a production system, you might want to:
            # 1. Store failed events for retry
            # 2. Send to dead letter queue
            # 3. Raise an exception
    
    async def publish_many(self, events: List[DomainEvent]) -> None:
        """Publish multiple domain events"""
        
        if not events:
            return
        
        published_count = await self.event_bus_client.publish_events(events)
        
        if published_count < len(events):
            failed_count = len(events) - published_count
            self.logger.error(
                "Some domain events failed to publish",
                total_events=len(events),
                published_count=published_count,
                failed_count=failed_count
            )


class EventBusIntegration:
    """Main integration class for Event Bus functionality"""
    
    def __init__(self, config: EventBusConfig):
        self.config = config
        self.client = EventBusClient(config)
        self.publisher = DomainEventPublisher(self.client)
        self.logger = logger.bind(component="eventbus_integration")
    
    async def start(self) -> None:
        """Start the Event Bus integration"""
        
        await self.client.start()
        self.logger.info("Event Bus integration started")
    
    async def stop(self) -> None:
        """Stop the Event Bus integration"""
        
        await self.client.stop()
        self.logger.info("Event Bus integration stopped")
    
    def get_publisher(self) -> EventPublisher:
        """Get the event publisher instance"""
        return self.publisher
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.stop()


# Utility functions for testing and development
async def test_event_bus_connection(config: EventBusConfig) -> bool:
    """Test connection to Event Bus"""
    
    try:
        async with EventBusIntegration(config) as integration:
            logger.info("Event Bus connection test successful")
            return True
    except Exception as e:
        logger.error("Event Bus connection test failed", error=str(e))
        return False


async def publish_test_event(config: EventBusConfig, tenant_id: UUID) -> bool:
    """Publish a test event to verify integration"""
    
    try:
        test_event = DomainEvent(
            event_type="test.domain_repository_health",
            aggregate_id=UUID("00000000-0000-4000-8000-000000000001"),
            aggregate_type="Test",
            tenant_id=tenant_id,
            data={"message": "Domain Repository service is healthy"},
            metadata={"test": True}
        )
        
        async with EventBusIntegration(config) as integration:
            await integration.get_publisher().publish(test_event)
            logger.info("Test event published successfully")
            return True
            
    except Exception as e:
        logger.error("Failed to publish test event", error=str(e))
        return False