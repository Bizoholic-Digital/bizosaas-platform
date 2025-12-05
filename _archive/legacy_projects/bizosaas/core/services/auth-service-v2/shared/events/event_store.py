"""
Event Store Implementation using Redis Streams
Provides reliable event persistence and publishing with outbox pattern
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Callable, AsyncGenerator
from contextlib import asynccontextmanager

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update
from sqlalchemy.orm import declarative_base

from .domain_events import DomainEvent, deserialize_event

logger = logging.getLogger(__name__)

Base = declarative_base()


class OutboxEvent(Base):
    """Outbox pattern implementation for reliable event publishing"""
    __tablename__ = "outbox_events"
    
    id: str
    tenant_id: str
    event_type: str
    aggregate_id: str
    aggregate_type: str
    event_data: str  # JSON serialized event
    created_at: datetime
    published_at: Optional[datetime]
    is_published: bool = False
    retry_count: int = 0
    max_retries: int = 3


class EventStore:
    """Redis Streams-based event store with outbox pattern"""
    
    def __init__(self, redis_client: redis.Redis, db_session: AsyncSession):
        self.redis = redis_client
        self.db_session = db_session
        self.stream_name = "bizosaas:events"
        self.consumer_group = "event-processors"
        self.consumer_name = "event-store-consumer"
        
    async def initialize(self):
        """Initialize Redis streams and consumer group"""
        try:
            # Create consumer group if it doesn't exist
            await self.redis.xgroup_create(
                self.stream_name,
                self.consumer_group,
                id='0',
                mkstream=True
            )
            logger.info(f"Created consumer group {self.consumer_group}")
        except redis.ResponseError as e:
            if "BUSYGROUP" in str(e):
                logger.info(f"Consumer group {self.consumer_group} already exists")
            else:
                raise
    
    async def store_events(self, events: List[DomainEvent]) -> None:
        """Store events in outbox table for reliable delivery"""
        if not events:
            return
            
        try:
            # Store in outbox table first (transactional)
            for event in events:
                outbox_data = {
                    'id': event.event_id,
                    'tenant_id': event.tenant_id,
                    'event_type': event.event_type,
                    'aggregate_id': event.aggregate_id,
                    'aggregate_type': event.aggregate_type,
                    'event_data': event.to_json(),
                    'created_at': event.occurred_at,
                    'is_published': False,
                    'retry_count': 0
                }
                
                stmt = insert(OutboxEvent).values(**outbox_data)
                await self.db_session.execute(stmt)
            
            await self.db_session.commit()
            logger.info(f"Stored {len(events)} events in outbox")
            
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Failed to store events in outbox: {e}")
            raise
    
    async def publish_pending_events(self) -> int:
        """Publish events from outbox to Redis streams"""
        published_count = 0
        
        try:
            # Get unpublished events
            stmt = select(OutboxEvent).where(
                OutboxEvent.is_published == False,
                OutboxEvent.retry_count < OutboxEvent.max_retries
            ).order_by(OutboxEvent.created_at).limit(100)
            
            result = await self.db_session.execute(stmt)
            outbox_events = result.scalars().all()
            
            for outbox_event in outbox_events:
                try:
                    # Publish to Redis stream
                    stream_data = {
                        'event_id': outbox_event.id,
                        'tenant_id': outbox_event.tenant_id,
                        'event_type': outbox_event.event_type,
                        'aggregate_id': outbox_event.aggregate_id,
                        'aggregate_type': outbox_event.aggregate_type,
                        'event_data': outbox_event.event_data,
                        'occurred_at': outbox_event.created_at.isoformat()
                    }
                    
                    message_id = await self.redis.xadd(
                        self.stream_name,
                        stream_data,
                        maxlen=10000  # Keep last 10k events
                    )
                    
                    # Mark as published
                    stmt = update(OutboxEvent).where(
                        OutboxEvent.id == outbox_event.id
                    ).values(
                        is_published=True,
                        published_at=datetime.utcnow()
                    )
                    await self.db_session.execute(stmt)
                    
                    published_count += 1
                    logger.debug(f"Published event {outbox_event.id} to stream {message_id}")
                    
                except Exception as e:
                    # Increment retry count on failure
                    stmt = update(OutboxEvent).where(
                        OutboxEvent.id == outbox_event.id
                    ).values(
                        retry_count=OutboxEvent.retry_count + 1
                    )
                    await self.db_session.execute(stmt)
                    
                    logger.error(f"Failed to publish event {outbox_event.id}: {e}")
            
            await self.db_session.commit()
            
            if published_count > 0:
                logger.info(f"Published {published_count} events to Redis stream")
                
            return published_count
            
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f"Failed to publish events: {e}")
            raise
    
    async def read_events(self, count: int = 10, block_ms: int = 1000) -> List[Dict[str, Any]]:
        """Read events from Redis stream"""
        try:
            # Read from stream
            messages = await self.redis.xreadgroup(
                self.consumer_group,
                self.consumer_name,
                {self.stream_name: '>'},
                count=count,
                block=block_ms
            )
            
            events = []
            for stream, stream_messages in messages:
                for message_id, fields in stream_messages:
                    # Decode Redis response
                    event_data = {k.decode(): v.decode() for k, v in fields.items()}
                    event_data['message_id'] = message_id.decode()
                    events.append(event_data)
            
            return events
            
        except Exception as e:
            logger.error(f"Failed to read events from stream: {e}")
            return []
    
    async def acknowledge_event(self, message_id: str) -> None:
        """Acknowledge event processing"""
        try:
            await self.redis.xack(
                self.stream_name,
                self.consumer_group,
                message_id
            )
            logger.debug(f"Acknowledged event {message_id}")
        except Exception as e:
            logger.error(f"Failed to acknowledge event {message_id}: {e}")
    
    async def get_pending_events(self) -> List[Dict[str, Any]]:
        """Get events that were consumed but not acknowledged"""
        try:
            pending = await self.redis.xpending(
                self.stream_name,
                self.consumer_group
            )
            
            if pending['pending'] > 0:
                # Get detailed pending info
                pending_msgs = await self.redis.xpending_range(
                    self.stream_name,
                    self.consumer_group,
                    min="-",
                    max="+",
                    count=100
                )
                
                events = []
                for msg in pending_msgs:
                    message_id, consumer, idle_time, delivery_count = msg
                    
                    # Get the actual message
                    messages = await self.redis.xrange(
                        self.stream_name,
                        min=message_id,
                        max=message_id
                    )
                    
                    if messages:
                        _, fields = messages[0]
                        event_data = {k.decode(): v.decode() for k, v in fields.items()}
                        event_data['message_id'] = message_id.decode()
                        event_data['idle_time'] = idle_time
                        event_data['delivery_count'] = delivery_count
                        events.append(event_data)
                
                return events
            
            return []
            
        except Exception as e:
            logger.error(f"Failed to get pending events: {e}")
            return []


class EventPublisher:
    """High-level event publisher with batching and retry logic"""
    
    def __init__(self, event_store: EventStore):
        self.event_store = event_store
        self._batch: List[DomainEvent] = []
        self._batch_size = 50
        self._publish_task: Optional[asyncio.Task] = None
        
    async def publish(self, event: DomainEvent) -> None:
        """Publish single event"""
        await self.publish_batch([event])
    
    async def publish_batch(self, events: List[DomainEvent]) -> None:
        """Publish multiple events as batch"""
        await self.event_store.store_events(events)
        
        # Trigger immediate publishing for critical events
        critical_events = {'tenant.created', 'subscription.upgraded', 'lead.converted'}
        if any(event.event_type in critical_events for event in events):
            await self.event_store.publish_pending_events()
    
    async def start_background_publisher(self, interval_seconds: int = 5) -> None:
        """Start background task to publish events from outbox"""
        if self._publish_task and not self._publish_task.done():
            return
            
        self._publish_task = asyncio.create_task(
            self._background_publisher(interval_seconds)
        )
    
    async def stop_background_publisher(self) -> None:
        """Stop background publisher task"""
        if self._publish_task and not self._publish_task.done():
            self._publish_task.cancel()
            try:
                await self._publish_task
            except asyncio.CancelledError:
                pass
    
    async def _background_publisher(self, interval_seconds: int) -> None:
        """Background task to continuously publish pending events"""
        logger.info("Started background event publisher")
        
        try:
            while True:
                try:
                    published_count = await self.event_store.publish_pending_events()
                    
                    # Clean up old published events (keep for 30 days)
                    cutoff_date = datetime.utcnow() - timedelta(days=30)
                    stmt = text("""
                        DELETE FROM outbox_events 
                        WHERE is_published = true 
                        AND published_at < :cutoff_date
                        LIMIT 1000
                    """)
                    await self.event_store.db_session.execute(stmt, {'cutoff_date': cutoff_date})
                    await self.event_store.db_session.commit()
                    
                except Exception as e:
                    logger.error(f"Error in background publisher: {e}")
                
                await asyncio.sleep(interval_seconds)
                
        except asyncio.CancelledError:
            logger.info("Background event publisher stopped")
            raise


class EventHandler:
    """Base class for event handlers"""
    
    def __init__(self, event_types: List[str]):
        self.event_types = event_types
    
    async def handle(self, event: DomainEvent) -> None:
        """Handle domain event - override in subclasses"""
        raise NotImplementedError
    
    def can_handle(self, event_type: str) -> bool:
        """Check if handler can process event type"""
        return event_type in self.event_types


class EventProcessor:
    """Event processor that routes events to appropriate handlers"""
    
    def __init__(self, event_store: EventStore):
        self.event_store = event_store
        self.handlers: List[EventHandler] = []
        self._processor_task: Optional[asyncio.Task] = None
        
    def register_handler(self, handler: EventHandler) -> None:
        """Register event handler"""
        self.handlers.append(handler)
        logger.info(f"Registered handler for events: {handler.event_types}")
    
    async def start_processing(self) -> None:
        """Start event processing loop"""
        if self._processor_task and not self._processor_task.done():
            return
            
        self._processor_task = asyncio.create_task(self._process_events())
    
    async def stop_processing(self) -> None:
        """Stop event processing"""
        if self._processor_task and not self._processor_task.done():
            self._processor_task.cancel()
            try:
                await self._processor_task
            except asyncio.CancelledError:
                pass
    
    async def _process_events(self) -> None:
        """Main event processing loop"""
        logger.info("Started event processor")
        
        try:
            while True:
                try:
                    # Read events from stream
                    events_data = await self.event_store.read_events(count=20, block_ms=5000)
                    
                    for event_data in events_data:
                        try:
                            # Parse event
                            event_json = json.loads(event_data['event_data'])
                            event = deserialize_event(event_json)
                            
                            # Route to appropriate handlers
                            handled = False
                            for handler in self.handlers:
                                if handler.can_handle(event.event_type):
                                    await handler.handle(event)
                                    handled = True
                            
                            if not handled:
                                logger.warning(f"No handler for event type: {event.event_type}")
                            
                            # Acknowledge event
                            await self.event_store.acknowledge_event(event_data['message_id'])
                            
                        except Exception as e:
                            logger.error(f"Error processing event {event_data.get('event_id', 'unknown')}: {e}")
                            # TODO: Implement dead letter queue for failed events
                            
                except Exception as e:
                    logger.error(f"Error in event processing loop: {e}")
                    await asyncio.sleep(5)  # Back off on errors
                
        except asyncio.CancelledError:
            logger.info("Event processor stopped")
            raise


@asynccontextmanager
async def event_system(redis_client: redis.Redis, db_session: AsyncSession):
    """Context manager for event system lifecycle"""
    event_store = EventStore(redis_client, db_session)
    await event_store.initialize()
    
    publisher = EventPublisher(event_store)
    processor = EventProcessor(event_store)
    
    # Start background tasks
    await publisher.start_background_publisher()
    await processor.start_processing()
    
    try:
        yield {
            'event_store': event_store,
            'publisher': publisher,
            'processor': processor
        }
    finally:
        # Clean shutdown
        await publisher.stop_background_publisher()
        await processor.stop_processing()