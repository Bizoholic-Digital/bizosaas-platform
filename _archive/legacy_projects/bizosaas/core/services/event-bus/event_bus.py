"""
Domain Event Bus Core Implementation

This module provides the core event bus functionality for the BizOSaaS platform,
enabling event-driven architecture and AI agent coordination.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Set
from uuid import UUID, uuid4

import redis.asyncio as redis
from pydantic import BaseModel
from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
import structlog

from domain_events import BaseEvent, EventStatus, EventPriority, create_event
from event_storage import EventStore, EventStorageModel
from message_brokers import MessageBrokerInterface, RedisMessageBroker, RabbitMQBroker
from subscription_manager import SubscriptionManager, EventSubscription
from tenant_isolation import TenantContext, ensure_tenant_isolation


logger = structlog.get_logger(__name__)


class EventProcessingResult(BaseModel):
    """Result of event processing"""
    success: bool
    event_id: UUID
    processed_by: List[str] = []
    errors: List[str] = []
    processing_time_ms: int = 0


class EventBusConfig(BaseModel):
    """Event Bus Configuration"""
    # Redis configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    
    # Message broker configuration
    broker_type: str = "redis"  # redis, rabbitmq, kafka
    rabbitmq_url: Optional[str] = None
    kafka_bootstrap_servers: Optional[str] = None
    
    # PostgreSQL configuration for event store
    database_url: str
    
    # Processing configuration
    max_retry_attempts: int = 3
    retry_delay_seconds: int = 5
    event_ttl_days: int = 30
    batch_size: int = 100
    worker_concurrency: int = 10
    
    # Tenant isolation
    enable_tenant_isolation: bool = True
    
    # Monitoring
    metrics_enabled: bool = True
    health_check_interval: int = 30


class EventBus:
    """
    Core Event Bus implementation for BizOSaaS platform
    
    Provides:
    - Event publishing and subscription
    - Multi-tenant event isolation
    - Reliable event delivery
    - Event replay and audit trail
    - AI agent coordination
    - Real-time and batch processing
    """
    
    def __init__(self, config: EventBusConfig):
        self.config = config
        self.logger = logger.bind(component="event_bus")
        
        # Core components
        self.event_store: Optional[EventStore] = None
        self.message_broker: Optional[MessageBrokerInterface] = None
        self.subscription_manager: Optional[SubscriptionManager] = None
        self.redis_client: Optional[redis.Redis] = None
        
        # Processing state
        self.is_running = False
        self.worker_tasks: List[asyncio.Task] = []
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.middleware: List[Callable] = []
        
        # Metrics and monitoring
        self.metrics = {
            "events_published": 0,
            "events_processed": 0,
            "events_failed": 0,
            "processing_time_total_ms": 0,
            "active_subscriptions": 0
        }
    
    async def initialize(self) -> None:
        """Initialize the event bus"""
        try:
            self.logger.info("Initializing Event Bus")
            
            # Initialize Redis client
            self.redis_client = redis.Redis(
                host=self.config.redis_host,
                port=self.config.redis_port,
                db=self.config.redis_db,
                password=self.config.redis_password,
                decode_responses=True
            )
            
            # Test Redis connection
            await self.redis_client.ping()
            self.logger.info("Redis connection established")
            
            # Initialize event store
            self.event_store = EventStore(self.config.database_url)
            await self.event_store.initialize()
            self.logger.info("Event store initialized")
            
            # Initialize message broker
            if self.config.broker_type == "redis":
                self.message_broker = RedisMessageBroker(self.redis_client)
            elif self.config.broker_type == "rabbitmq":
                self.message_broker = RabbitMQBroker(self.config.rabbitmq_url)
            else:
                raise ValueError(f"Unsupported broker type: {self.config.broker_type}")
            
            await self.message_broker.initialize()
            self.logger.info("Message broker initialized", broker_type=self.config.broker_type)
            
            # Initialize subscription manager
            self.subscription_manager = SubscriptionManager(self.redis_client)
            await self.subscription_manager.initialize()
            self.logger.info("Subscription manager initialized")
            
            # Register built-in middleware
            self._register_builtin_middleware()
            
            self.logger.info("Event Bus initialization complete")
            
        except Exception as e:
            self.logger.error("Failed to initialize Event Bus", error=str(e))
            raise
    
    async def start(self) -> None:
        """Start the event bus processing"""
        if self.is_running:
            return
        
        self.logger.info("Starting Event Bus")
        self.is_running = True
        
        # Start worker tasks
        for i in range(self.config.worker_concurrency):
            task = asyncio.create_task(
                self._event_processing_worker(f"worker-{i}")
            )
            self.worker_tasks.append(task)
        
        # Start health check task
        health_task = asyncio.create_task(self._health_check_worker())
        self.worker_tasks.append(health_task)
        
        # Start metrics collection
        if self.config.metrics_enabled:
            metrics_task = asyncio.create_task(self._metrics_collection_worker())
            self.worker_tasks.append(metrics_task)
        
        self.logger.info("Event Bus started", workers=self.config.worker_concurrency)
    
    async def stop(self) -> None:
        """Stop the event bus processing"""
        if not self.is_running:
            return
        
        self.logger.info("Stopping Event Bus")
        self.is_running = False
        
        # Cancel all worker tasks
        for task in self.worker_tasks:
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self.worker_tasks, return_exceptions=True)
        self.worker_tasks.clear()
        
        # Cleanup resources
        if self.message_broker:
            await self.message_broker.close()
        
        if self.redis_client:
            await self.redis_client.aclose()
        
        self.logger.info("Event Bus stopped")
    
    async def publish_event(
        self, 
        event: BaseEvent,
        tenant_context: Optional[TenantContext] = None
    ) -> EventProcessingResult:
        """
        Publish an event to the bus
        
        Args:
            event: The event to publish
            tenant_context: Tenant context for isolation
            
        Returns:
            EventProcessingResult indicating success/failure
        """
        start_time = datetime.utcnow()
        
        try:
            # Apply tenant isolation if enabled
            if self.config.enable_tenant_isolation and tenant_context:
                event = ensure_tenant_isolation(event, tenant_context)
            
            # Apply middleware
            for middleware in self.middleware:
                event = await middleware(event)
            
            # Store event in event store
            await self.event_store.store_event(event)
            
            # Publish to message broker
            routing_key = self._build_routing_key(event)
            await self.message_broker.publish(
                routing_key=routing_key,
                message=event.model_dump_json(),
                priority=self._map_priority(event.priority)
            )
            
            # Update metrics
            self.metrics["events_published"] += 1
            processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            self.logger.info(
                "Event published",
                event_id=str(event.event_id),
                event_type=event.event_type,
                tenant_id=str(event.tenant_id),
                processing_time_ms=int(processing_time)
            )
            
            return EventProcessingResult(
                success=True,
                event_id=event.event_id,
                processing_time_ms=int(processing_time)
            )
            
        except Exception as e:
            self.metrics["events_failed"] += 1
            self.logger.error(
                "Failed to publish event",
                event_id=str(event.event_id),
                error=str(e)
            )
            
            return EventProcessingResult(
                success=False,
                event_id=event.event_id,
                errors=[str(e)]
            )
    
    async def subscribe(
        self,
        event_type: str,
        handler: Callable[[BaseEvent], Any],
        service_name: str,
        tenant_id: Optional[UUID] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Subscribe to events
        
        Args:
            event_type: Type of event to subscribe to (e.g., "lead.created")
            handler: Function to handle the event
            service_name: Name of the subscribing service
            tenant_id: Optional tenant ID for tenant-specific subscriptions
            filters: Optional filters for event matching
            
        Returns:
            Subscription ID
        """
        subscription = EventSubscription(
            subscription_id=str(uuid4()),
            event_type=event_type,
            service_name=service_name,
            tenant_id=tenant_id,
            filters=filters or {},
            created_at=datetime.utcnow()
        )
        
        # Register with subscription manager
        await self.subscription_manager.add_subscription(subscription)
        
        # Register handler locally
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        
        self.event_handlers[event_type].append(handler)
        
        # Subscribe to message broker
        routing_key = self._build_subscription_routing_key(event_type, tenant_id)
        await self.message_broker.subscribe(
            routing_key=routing_key,
            callback=self._create_message_handler(handler, subscription)
        )
        
        self.metrics["active_subscriptions"] += 1
        
        self.logger.info(
            "Subscription created",
            subscription_id=subscription.subscription_id,
            event_type=event_type,
            service_name=service_name
        )
        
        return subscription.subscription_id
    
    async def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from events"""
        try:
            subscription = await self.subscription_manager.get_subscription(subscription_id)
            if not subscription:
                return False
            
            # Remove from subscription manager
            await self.subscription_manager.remove_subscription(subscription_id)
            
            # Remove from message broker
            routing_key = self._build_subscription_routing_key(
                subscription.event_type, 
                subscription.tenant_id
            )
            await self.message_broker.unsubscribe(routing_key)
            
            self.metrics["active_subscriptions"] -= 1
            
            self.logger.info("Subscription removed", subscription_id=subscription_id)
            return True
            
        except Exception as e:
            self.logger.error("Failed to unsubscribe", subscription_id=subscription_id, error=str(e))
            return False
    
    async def replay_events(
        self,
        tenant_id: UUID,
        event_types: List[str],
        start_time: datetime,
        end_time: Optional[datetime] = None,
        target_service: Optional[str] = None
    ) -> int:
        """
        Replay events for a tenant within a time range
        
        Args:
            tenant_id: Tenant to replay events for
            event_types: List of event types to replay
            start_time: Start time for replay
            end_time: End time for replay (defaults to now)
            target_service: Optional specific service to replay to
            
        Returns:
            Number of events replayed
        """
        if not end_time:
            end_time = datetime.utcnow()
        
        events = await self.event_store.get_events(
            tenant_id=tenant_id,
            event_types=event_types,
            start_time=start_time,
            end_time=end_time
        )
        
        replayed_count = 0
        for event_data in events:
            try:
                # Reconstruct event
                event = create_event(event_data["event_type"], **event_data)
                
                # Mark as replay
                event.metadata["is_replay"] = True
                event.metadata["replayed_at"] = datetime.utcnow().isoformat()
                
                # Filter by target service if specified
                if target_service:
                    event.target_services = [target_service]
                
                # Republish event
                await self.publish_event(event)
                replayed_count += 1
                
            except Exception as e:
                self.logger.error(
                    "Failed to replay event",
                    event_id=event_data.get("event_id"),
                    error=str(e)
                )
        
        self.logger.info(
            "Event replay completed",
            tenant_id=str(tenant_id),
            events_replayed=replayed_count,
            time_range=(start_time.isoformat(), end_time.isoformat())
        )
        
        return replayed_count
    
    async def get_event_history(
        self,
        tenant_id: UUID,
        aggregate_id: Optional[UUID] = None,
        event_types: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get event history for debugging and analysis"""
        return await self.event_store.get_events(
            tenant_id=tenant_id,
            aggregate_id=aggregate_id,
            event_types=event_types,
            limit=limit
        )
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        active_subs = await self.subscription_manager.get_subscription_count()
        
        return {
            **self.metrics,
            "active_subscriptions": active_subs,
            "is_running": self.is_running,
            "worker_count": len(self.worker_tasks),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def add_middleware(self, middleware: Callable[[BaseEvent], BaseEvent]) -> None:
        """Add middleware for event processing"""
        self.middleware.append(middleware)
    
    # Private methods
    
    def _register_builtin_middleware(self) -> None:
        """Register built-in middleware"""
        
        async def correlation_middleware(event: BaseEvent) -> BaseEvent:
            """Ensure correlation ID is set"""
            if not event.correlation_id:
                event.correlation_id = uuid4()
            return event
        
        async def timestamp_middleware(event: BaseEvent) -> BaseEvent:
            """Ensure timestamp is current"""
            if not event.timestamp:
                event.timestamp = datetime.utcnow()
            return event
        
        self.add_middleware(correlation_middleware)
        self.add_middleware(timestamp_middleware)
    
    def _build_routing_key(self, event: BaseEvent) -> str:
        """Build routing key for event"""
        base_key = f"events.{event.category.value}.{event.event_type}"
        
        if self.config.enable_tenant_isolation:
            return f"tenant.{event.tenant_id}.{base_key}"
        
        return base_key
    
    def _build_subscription_routing_key(self, event_type: str, tenant_id: Optional[UUID] = None) -> str:
        """Build routing key for subscription"""
        if self.config.enable_tenant_isolation and tenant_id:
            return f"tenant.{tenant_id}.events.*.{event_type}"
        
        return f"events.*.{event_type}"
    
    def _map_priority(self, priority: EventPriority) -> int:
        """Map event priority to broker priority"""
        mapping = {
            EventPriority.LOW: 1,
            EventPriority.NORMAL: 5,
            EventPriority.HIGH: 8,
            EventPriority.CRITICAL: 10
        }
        return mapping.get(priority, 5)
    
    def _create_message_handler(
        self, 
        handler: Callable, 
        subscription: EventSubscription
    ) -> Callable:
        """Create message handler for broker callback"""
        
        async def message_handler(message: str) -> None:
            try:
                # Parse event from message
                event_data = json.loads(message)
                event = create_event(event_data["event_type"], **event_data)
                
                # Apply subscription filters
                if not self._matches_filters(event, subscription.filters):
                    return
                
                # Apply tenant isolation
                if (self.config.enable_tenant_isolation and 
                    subscription.tenant_id and 
                    event.tenant_id != subscription.tenant_id):
                    return
                
                # Call handler
                await handler(event)
                
                # Update event status
                await self.event_store.update_event_status(
                    event.event_id, 
                    EventStatus.COMPLETED
                )
                
                self.metrics["events_processed"] += 1
                
            except Exception as e:
                self.logger.error(
                    "Event handler failed",
                    subscription_id=subscription.subscription_id,
                    error=str(e)
                )
                
                # Update event status
                if 'event' in locals():
                    await self.event_store.update_event_status(
                        event.event_id, 
                        EventStatus.FAILED
                    )
                
                self.metrics["events_failed"] += 1
        
        return message_handler
    
    def _matches_filters(self, event: BaseEvent, filters: Dict[str, Any]) -> bool:
        """Check if event matches subscription filters"""
        for key, expected_value in filters.items():
            if hasattr(event, key):
                actual_value = getattr(event, key)
                if actual_value != expected_value:
                    return False
            elif key in event.data:
                actual_value = event.data[key]
                if actual_value != expected_value:
                    return False
            else:
                return False
        
        return True
    
    async def _event_processing_worker(self, worker_name: str) -> None:
        """Background worker for event processing"""
        self.logger.info("Event processing worker started", worker=worker_name)
        
        try:
            while self.is_running:
                # Process failed events for retry
                await self._process_failed_events()
                
                # Cleanup old events
                await self._cleanup_old_events()
                
                # Wait before next iteration
                await asyncio.sleep(30)
                
        except asyncio.CancelledError:
            self.logger.info("Event processing worker stopped", worker=worker_name)
        except Exception as e:
            self.logger.error("Event processing worker error", worker=worker_name, error=str(e))
    
    async def _process_failed_events(self) -> None:
        """Process failed events for retry"""
        try:
            failed_events = await self.event_store.get_failed_events(
                max_retries=self.config.max_retry_attempts,
                batch_size=self.config.batch_size
            )
            
            for event_data in failed_events:
                try:
                    event = create_event(event_data["event_type"], **event_data)
                    
                    # Check if retry limit exceeded
                    if event.retry_count >= event.max_retries:
                        await self.event_store.update_event_status(
                            event.event_id,
                            EventStatus.FAILED
                        )
                        continue
                    
                    # Increment retry count
                    event.retry_count += 1
                    event.status = EventStatus.RETRYING
                    
                    # Wait for retry delay
                    await asyncio.sleep(self.config.retry_delay_seconds)
                    
                    # Republish event
                    await self.publish_event(event)
                    
                except Exception as e:
                    self.logger.error(
                        "Failed to retry event",
                        event_id=event_data.get("event_id"),
                        error=str(e)
                    )
        
        except Exception as e:
            self.logger.error("Failed to process failed events", error=str(e))
    
    async def _cleanup_old_events(self) -> None:
        """Cleanup old events past TTL"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=self.config.event_ttl_days)
            deleted_count = await self.event_store.cleanup_old_events(cutoff_date)
            
            if deleted_count > 0:
                self.logger.info("Cleaned up old events", deleted_count=deleted_count)
        
        except Exception as e:
            self.logger.error("Failed to cleanup old events", error=str(e))
    
    async def _health_check_worker(self) -> None:
        """Background health check worker"""
        while self.is_running:
            try:
                # Check Redis connection
                await self.redis_client.ping()
                
                # Check event store connection
                await self.event_store.health_check()
                
                # Check message broker
                await self.message_broker.health_check()
                
                await asyncio.sleep(self.config.health_check_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error("Health check failed", error=str(e))
                await asyncio.sleep(self.config.health_check_interval)
    
    async def _metrics_collection_worker(self) -> None:
        """Background metrics collection worker"""
        while self.is_running:
            try:
                # Update subscription count
                self.metrics["active_subscriptions"] = \
                    await self.subscription_manager.get_subscription_count()
                
                # Store metrics in Redis for monitoring
                metrics_key = f"eventbus:metrics:{datetime.utcnow().strftime('%Y%m%d%H%M')}"
                await self.redis_client.hset(
                    metrics_key,
                    mapping=self.metrics
                )
                
                # Set TTL for metrics
                await self.redis_client.expire(metrics_key, 86400)  # 24 hours
                
                await asyncio.sleep(60)  # Collect every minute
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error("Metrics collection failed", error=str(e))
                await asyncio.sleep(60)