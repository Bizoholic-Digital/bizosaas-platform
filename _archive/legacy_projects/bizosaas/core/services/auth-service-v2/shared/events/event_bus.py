"""
Event-driven communication system for BizoholicSaaS microservices
Provides pub/sub messaging between services using Redis Streams
"""

import asyncio
import json
import uuid
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import redis.asyncio as redis
import logging

logger = logging.getLogger(__name__)

class EventType(Enum):
    """Standard event types across all services"""
    
    # User Management Events
    USER_CREATED = "user.created"
    USER_UPDATED = "user.updated"
    USER_DELETED = "user.deleted"
    USER_LOGIN = "user.login"
    USER_LOGOUT = "user.logout"
    
    # Campaign Management Events
    CAMPAIGN_CREATED = "campaign.created"
    CAMPAIGN_UPDATED = "campaign.updated"
    CAMPAIGN_STARTED = "campaign.started"
    CAMPAIGN_PAUSED = "campaign.paused"
    CAMPAIGN_COMPLETED = "campaign.completed"
    CAMPAIGN_FAILED = "campaign.failed"
    
    # AI Agent Events
    AGENT_TASK_STARTED = "agent.task.started"
    AGENT_TASK_COMPLETED = "agent.task.completed"
    AGENT_TASK_FAILED = "agent.task.failed"
    AGENT_OPTIMIZATION_COMPLETE = "agent.optimization.complete"
    
    # Analytics Events
    METRIC_RECORDED = "metric.recorded"
    REPORT_GENERATED = "report.generated"
    DASHBOARD_UPDATED = "dashboard.updated"
    
    # Integration Events
    INTEGRATION_CONNECTED = "integration.connected"
    INTEGRATION_DISCONNECTED = "integration.disconnected"
    INTEGRATION_SYNC_STARTED = "integration.sync.started"
    INTEGRATION_SYNC_COMPLETED = "integration.sync.completed"
    INTEGRATION_SYNC_FAILED = "integration.sync.failed"
    
    # Notification Events
    NOTIFICATION_SENT = "notification.sent"
    NOTIFICATION_DELIVERED = "notification.delivered"
    NOTIFICATION_FAILED = "notification.failed"
    
    # Sales Funnel Events
    FUNNEL_STAGE_ENTERED = "funnel.stage.entered"
    FUNNEL_STAGE_COMPLETED = "funnel.stage.completed"
    FUNNEL_CONVERSION = "funnel.conversion"
    
    # System Events
    HEALTH_CHECK = "system.health_check"
    ERROR_OCCURRED = "system.error"

@dataclass
class Event:
    """Standard event structure"""
    id: str
    type: EventType
    source_service: str
    tenant_id: str
    user_id: Optional[str] = None
    timestamp: str = None
    data: Dict[str, Any] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
        if self.data is None:
            self.data = {}
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> dict:
        """Convert event to dictionary"""
        event_dict = asdict(self)
        event_dict['type'] = self.type.value
        return event_dict
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        """Create event from dictionary"""
        data['type'] = EventType(data['type'])
        return cls(**data)

class EventHandler:
    """Base class for event handlers"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.handlers: Dict[EventType, List[Callable]] = {}
    
    def subscribe(self, event_type: EventType, handler: Callable):
        """Subscribe to an event type"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        logger.info(f"Handler subscribed to {event_type.value} in {self.service_name}")
    
    async def handle_event(self, event: Event):
        """Handle incoming event"""
        if event.type in self.handlers:
            for handler in self.handlers[event.type]:
                try:
                    await handler(event)
                    logger.debug(f"Event {event.id} handled by {handler.__name__}")
                except Exception as e:
                    logger.error(f"Error handling event {event.id}: {e}")

class EventBus:
    """Redis-based event bus for microservices communication"""
    
    def __init__(self, redis_client: redis.Redis, service_name: str):
        self.redis_client = redis_client
        self.service_name = service_name
        self.handlers = EventHandler(service_name)
        self.consumer_tasks: Dict[str, asyncio.Task] = {}
        self.is_running = False
        
        # Stream configuration
        self.stream_prefix = "bizosaas:events"
        self.consumer_group = f"service:{service_name}"
        self.consumer_name = f"{service_name}:{uuid.uuid4().hex[:8]}"
    
    async def initialize(self):
        """Initialize event bus and create consumer groups"""
        try:
            # Create consumer groups for each event type
            for event_type in EventType:
                stream_name = f"{self.stream_prefix}:{event_type.value}"
                try:
                    await self.redis_client.xgroup_create(
                        stream_name, self.consumer_group, id='0', mkstream=True
                    )
                    logger.debug(f"Consumer group created for {stream_name}")
                except redis.exceptions.ResponseError as e:
                    if "BUSYGROUP" not in str(e):
                        logger.error(f"Error creating consumer group: {e}")
            
            logger.info(f"Event bus initialized for service {self.service_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize event bus: {e}")
            raise
    
    async def publish(self, event: Event) -> str:
        """Publish an event to the event bus"""
        try:
            stream_name = f"{self.stream_prefix}:{event.type.value}"
            event_data = event.to_dict()
            
            # Add event to Redis stream
            event_id = await self.redis_client.xadd(
                stream_name, 
                event_data,
                maxlen=10000,  # Keep last 10k events
                approximate=True
            )
            
            logger.debug(f"Event published: {event.id} to {stream_name}")
            return event_id
            
        except Exception as e:
            logger.error(f"Failed to publish event {event.id}: {e}")
            raise
    
    def subscribe(self, event_type: EventType, handler: Callable):
        """Subscribe to an event type"""
        self.handlers.subscribe(event_type, handler)
        
        # Start consumer for this event type if not already running
        stream_name = f"{self.stream_prefix}:{event_type.value}"
        if stream_name not in self.consumer_tasks:
            task = asyncio.create_task(self._consume_events(event_type))
            self.consumer_tasks[stream_name] = task
    
    async def _consume_events(self, event_type: EventType):
        """Consume events from a specific stream"""
        stream_name = f"{self.stream_prefix}:{event_type.value}"
        
        while self.is_running:
            try:
                # Read from stream using consumer group
                messages = await self.redis_client.xreadgroup(
                    self.consumer_group,
                    self.consumer_name,
                    {stream_name: '>'},
                    count=10,
                    block=1000  # 1 second timeout
                )
                
                for stream, msgs in messages:
                    for msg_id, fields in msgs:
                        try:
                            # Parse event
                            event = Event.from_dict(fields)
                            
                            # Handle event
                            await self.handlers.handle_event(event)
                            
                            # Acknowledge message
                            await self.redis_client.xack(
                                stream_name, self.consumer_group, msg_id
                            )
                            
                        except Exception as e:
                            logger.error(f"Error processing message {msg_id}: {e}")
                            
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error consuming from {stream_name}: {e}")
                await asyncio.sleep(1)  # Brief pause before retrying
    
    async def start(self):
        """Start the event bus consumers"""
        self.is_running = True
        logger.info(f"Event bus started for service {self.service_name}")
    
    async def stop(self):
        """Stop the event bus consumers"""
        self.is_running = False
        
        # Cancel all consumer tasks
        for task in self.consumer_tasks.values():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        
        self.consumer_tasks.clear()
        logger.info(f"Event bus stopped for service {self.service_name}")
    
    async def get_stream_info(self, event_type: EventType) -> dict:
        """Get information about an event stream"""
        stream_name = f"{self.stream_prefix}:{event_type.value}"
        try:
            return await self.redis_client.xinfo_stream(stream_name)
        except redis.exceptions.ResponseError:
            return {"length": 0, "groups": 0}
    
    async def get_pending_messages(self, event_type: EventType) -> list:
        """Get pending messages for this consumer"""
        stream_name = f"{self.stream_prefix}:{event_type.value}"
        try:
            return await self.redis_client.xpending(
                stream_name, self.consumer_group
            )
        except redis.exceptions.ResponseError:
            return []

# Event factory functions for common events
class EventFactory:
    """Factory for creating standard events"""
    
    @staticmethod
    def user_created(tenant_id: str, user_id: str, user_data: dict) -> Event:
        return Event(
            id=str(uuid.uuid4()),
            type=EventType.USER_CREATED,
            source_service="user-management",
            tenant_id=tenant_id,
            user_id=user_id,
            data=user_data
        )
    
    @staticmethod
    def campaign_started(tenant_id: str, user_id: str, campaign_id: str, campaign_data: dict) -> Event:
        return Event(
            id=str(uuid.uuid4()),
            type=EventType.CAMPAIGN_STARTED,
            source_service="campaign-management",
            tenant_id=tenant_id,
            user_id=user_id,
            data={
                "campaign_id": campaign_id,
                **campaign_data
            }
        )
    
    @staticmethod
    def agent_task_completed(tenant_id: str, task_id: str, agent_name: str, result_data: dict) -> Event:
        return Event(
            id=str(uuid.uuid4()),
            type=EventType.AGENT_TASK_COMPLETED,
            source_service="ai-agents",
            tenant_id=tenant_id,
            data={
                "task_id": task_id,
                "agent_name": agent_name,
                **result_data
            }
        )
    
    @staticmethod
    def metric_recorded(tenant_id: str, entity_id: str, metric_name: str, value: float) -> Event:
        return Event(
            id=str(uuid.uuid4()),
            type=EventType.METRIC_RECORDED,
            source_service="analytics",
            tenant_id=tenant_id,
            data={
                "entity_id": entity_id,
                "metric_name": metric_name,
                "value": value,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    @staticmethod
    def integration_sync_completed(tenant_id: str, integration_id: str, sync_data: dict) -> Event:
        return Event(
            id=str(uuid.uuid4()),
            type=EventType.INTEGRATION_SYNC_COMPLETED,
            source_service="integration",
            tenant_id=tenant_id,
            data={
                "integration_id": integration_id,
                **sync_data
            }
        )

# Decorator for event handlers
def event_handler(event_type: EventType):
    """Decorator to mark functions as event handlers"""
    def decorator(func):
        func._event_type = event_type
        func._is_event_handler = True
        return func
    return decorator

# Service base class with event support
class EventAwareService:
    """Base class for services with event bus integration"""
    
    def __init__(self, service_name: str, redis_client: redis.Redis):
        self.service_name = service_name
        self.event_bus = EventBus(redis_client, service_name)
        self._register_handlers()
    
    def _register_handlers(self):
        """Automatically register methods marked with @event_handler"""
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, '_is_event_handler') and hasattr(attr, '_event_type'):
                self.event_bus.subscribe(attr._event_type, attr)
    
    async def start_event_processing(self):
        """Start processing events"""
        await self.event_bus.initialize()
        await self.event_bus.start()
    
    async def stop_event_processing(self):
        """Stop processing events"""
        await self.event_bus.stop()
    
    async def publish_event(self, event: Event):
        """Publish an event"""
        return await self.event_bus.publish(event)