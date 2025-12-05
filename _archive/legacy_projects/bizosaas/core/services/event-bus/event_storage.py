"""
Event Storage Layer for BizOSaaS Event Bus

Provides persistent storage for domain events with PostgreSQL backend,
supporting event replay, audit trails, and event sourcing patterns.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import (
    Column, String, DateTime, Text, Integer, Boolean, Index,
    create_engine, select, update, delete, and_, or_, desc
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import structlog

from domain_events import BaseEvent, EventStatus, EventPriority, EventCategory

logger = structlog.get_logger(__name__)

Base = declarative_base()


class EventStorageModel(Base):
    """SQLAlchemy model for event storage"""
    __tablename__ = "domain_events"
    
    # Primary identification
    event_id = Column(PG_UUID(as_uuid=True), primary_key=True)
    event_type = Column(String(100), nullable=False, index=True)
    event_version = Column(String(10), nullable=False, default="1.0")
    
    # Timestamp and ordering
    timestamp = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Multi-tenancy
    tenant_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    
    # Event metadata
    source_service = Column(String(100), nullable=False, index=True)
    correlation_id = Column(PG_UUID(as_uuid=True), index=True)
    causation_id = Column(PG_UUID(as_uuid=True), index=True)
    
    # Event categorization
    category = Column(String(50), nullable=False, index=True)
    priority = Column(String(20), nullable=False, default="normal", index=True)
    
    # Aggregate information
    aggregate_id = Column(PG_UUID(as_uuid=True), index=True)
    aggregate_type = Column(String(100), index=True)
    
    # Event payload
    data = Column(JSONB, nullable=False, default=dict)
    event_metadata = Column(JSONB, nullable=False, default=dict)
    
    # Processing status
    status = Column(String(20), nullable=False, default="pending", index=True)
    retry_count = Column(Integer, nullable=False, default=0)
    max_retries = Column(Integer, nullable=False, default=3)
    last_error = Column(Text)
    
    # Routing information
    target_services = Column(JSONB, nullable=False, default=list)
    routing_key = Column(String(200), index=True)
    
    # Audit fields
    processed_at = Column(DateTime, index=True)
    processed_by = Column(String(100))
    processing_time_ms = Column(Integer)
    
    # Create composite indexes for common queries
    __table_args__ = (
        Index('ix_events_tenant_type', 'tenant_id', 'event_type'),
        Index('ix_events_tenant_timestamp', 'tenant_id', 'timestamp'),
        Index('ix_events_aggregate', 'tenant_id', 'aggregate_id', 'timestamp'),
        Index('ix_events_status_priority', 'status', 'priority'),
        Index('ix_events_correlation', 'tenant_id', 'correlation_id'),
        Index('ix_events_category_timestamp', 'category', 'timestamp'),
    )


class EventStore:
    """
    Event Store for persistent event storage
    
    Features:
    - Multi-tenant event isolation
    - Event replay and audit trails
    - Efficient querying and indexing
    - Event sourcing support
    - Cleanup and maintenance
    """
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = None
        self.async_session = None
        self.logger = logger.bind(component="event_store")
    
    async def initialize(self) -> None:
        """Initialize the event store"""
        try:
            # Create async engine
            self.engine = create_async_engine(
                self.database_url,
                echo=False,  # Set to True for SQL debugging
                pool_size=20,
                max_overflow=30,
                pool_pre_ping=True,
            )
            
            # Create session factory
            self.async_session = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            # Create tables
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            
            self.logger.info("Event store initialized")
            
        except Exception as e:
            self.logger.error("Failed to initialize event store", error=str(e))
            raise
    
    async def store_event(self, event: BaseEvent) -> None:
        """Store an event in the database"""
        try:
            async with self.async_session() as session:
                # Convert event to storage model
                storage_event = EventStorageModel(
                    event_id=event.event_id,
                    event_type=event.event_type,
                    event_version=event.event_version,
                    timestamp=event.timestamp,
                    tenant_id=event.tenant_id,
                    source_service=event.source_service,
                    correlation_id=event.correlation_id,
                    causation_id=event.causation_id,
                    category=event.category.value,
                    priority=event.priority.value,
                    aggregate_id=event.aggregate_id,
                    aggregate_type=event.aggregate_type,
                    data=event.data,
                    event_metadata=event.metadata,
                    status=event.status.value,
                    retry_count=event.retry_count,
                    max_retries=event.max_retries,
                    target_services=event.target_services,
                    routing_key=event.routing_key,
                )
                
                session.add(storage_event)
                await session.commit()
                
                self.logger.debug(
                    "Event stored",
                    event_id=str(event.event_id),
                    event_type=event.event_type,
                    tenant_id=str(event.tenant_id)
                )
        
        except Exception as e:
            self.logger.error(
                "Failed to store event",
                event_id=str(event.event_id),
                error=str(e)
            )
            raise
    
    async def get_event(self, event_id: UUID) -> Optional[Dict[str, Any]]:
        """Get a single event by ID"""
        try:
            async with self.async_session() as session:
                result = await session.execute(
                    select(EventStorageModel).where(EventStorageModel.event_id == event_id)
                )
                event = result.scalar_one_or_none()
                
                if event:
                    return self._event_to_dict(event)
                return None
        
        except Exception as e:
            self.logger.error("Failed to get event", event_id=str(event_id), error=str(e))
            return None
    
    async def get_events(
        self,
        tenant_id: UUID,
        event_types: Optional[List[str]] = None,
        aggregate_id: Optional[UUID] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        correlation_id: Optional[UUID] = None,
        status: Optional[EventStatus] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get events with filtering options"""
        try:
            async with self.async_session() as session:
                query = select(EventStorageModel).where(
                    EventStorageModel.tenant_id == tenant_id
                )
                
                # Apply filters
                if event_types:
                    query = query.where(EventStorageModel.event_type.in_(event_types))
                
                if aggregate_id:
                    query = query.where(EventStorageModel.aggregate_id == aggregate_id)
                
                if start_time:
                    query = query.where(EventStorageModel.timestamp >= start_time)
                
                if end_time:
                    query = query.where(EventStorageModel.timestamp <= end_time)
                
                if correlation_id:
                    query = query.where(EventStorageModel.correlation_id == correlation_id)
                
                if status:
                    query = query.where(EventStorageModel.status == status.value)
                
                # Order by timestamp (newest first)
                query = query.order_by(desc(EventStorageModel.timestamp))
                
                # Apply pagination
                query = query.offset(offset).limit(limit)
                
                result = await session.execute(query)
                events = result.scalars().all()
                
                return [self._event_to_dict(event) for event in events]
        
        except Exception as e:
            self.logger.error(
                "Failed to get events",
                tenant_id=str(tenant_id),
                error=str(e)
            )
            return []
    
    async def get_events_by_aggregate(
        self,
        tenant_id: UUID,
        aggregate_id: UUID,
        aggregate_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get all events for a specific aggregate (event sourcing)"""
        try:
            async with self.async_session() as session:
                query = select(EventStorageModel).where(
                    and_(
                        EventStorageModel.tenant_id == tenant_id,
                        EventStorageModel.aggregate_id == aggregate_id
                    )
                )
                
                if aggregate_type:
                    query = query.where(EventStorageModel.aggregate_type == aggregate_type)
                
                # Order by timestamp (oldest first for event sourcing)
                query = query.order_by(EventStorageModel.timestamp).limit(limit)
                
                result = await session.execute(query)
                events = result.scalars().all()
                
                return [self._event_to_dict(event) for event in events]
        
        except Exception as e:
            self.logger.error(
                "Failed to get events by aggregate",
                tenant_id=str(tenant_id),
                aggregate_id=str(aggregate_id),
                error=str(e)
            )
            return []
    
    async def get_failed_events(
        self, 
        max_retries: int = 3, 
        batch_size: int = 100
    ) -> List[Dict[str, Any]]:
        """Get failed events that can be retried"""
        try:
            async with self.async_session() as session:
                query = select(EventStorageModel).where(
                    and_(
                        EventStorageModel.status == EventStatus.FAILED.value,
                        EventStorageModel.retry_count < max_retries
                    )
                ).order_by(EventStorageModel.timestamp).limit(batch_size)
                
                result = await session.execute(query)
                events = result.scalars().all()
                
                return [self._event_to_dict(event) for event in events]
        
        except Exception as e:
            self.logger.error("Failed to get failed events", error=str(e))
            return []
    
    async def update_event_status(
        self,
        event_id: UUID,
        status: EventStatus,
        error_message: Optional[str] = None,
        processed_by: Optional[str] = None,
        processing_time_ms: Optional[int] = None
    ) -> bool:
        """Update event processing status"""
        try:
            async with self.async_session() as session:
                update_data = {
                    "status": status.value,
                    "updated_at": datetime.utcnow()
                }
                
                if status == EventStatus.COMPLETED:
                    update_data["processed_at"] = datetime.utcnow()
                
                if error_message:
                    update_data["last_error"] = error_message
                
                if processed_by:
                    update_data["processed_by"] = processed_by
                
                if processing_time_ms is not None:
                    update_data["processing_time_ms"] = processing_time_ms
                
                # Increment retry count if retrying
                if status == EventStatus.RETRYING:
                    update_data["retry_count"] = EventStorageModel.retry_count + 1
                
                await session.execute(
                    update(EventStorageModel)
                    .where(EventStorageModel.event_id == event_id)
                    .values(**update_data)
                )
                
                await session.commit()
                return True
        
        except Exception as e:
            self.logger.error(
                "Failed to update event status",
                event_id=str(event_id),
                error=str(e)
            )
            return False
    
    async def cleanup_old_events(self, cutoff_date: datetime) -> int:
        """Delete events older than cutoff date"""
        try:
            async with self.async_session() as session:
                result = await session.execute(
                    delete(EventStorageModel).where(
                        and_(
                            EventStorageModel.timestamp < cutoff_date,
                            EventStorageModel.status == EventStatus.COMPLETED.value
                        )
                    )
                )
                
                deleted_count = result.rowcount
                await session.commit()
                
                self.logger.info("Cleaned up old events", deleted_count=deleted_count)
                return deleted_count
        
        except Exception as e:
            self.logger.error("Failed to cleanup old events", error=str(e))
            return 0
    
    async def get_event_statistics(
        self, 
        tenant_id: Optional[UUID] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get event statistics for monitoring"""
        try:
            async with self.async_session() as session:
                # Build base query
                base_query = select(EventStorageModel)
                
                if tenant_id:
                    base_query = base_query.where(EventStorageModel.tenant_id == tenant_id)
                
                if start_time:
                    base_query = base_query.where(EventStorageModel.timestamp >= start_time)
                
                if end_time:
                    base_query = base_query.where(EventStorageModel.timestamp <= end_time)
                
                # Count by status
                status_counts = {}
                for status in EventStatus:
                    count_query = base_query.where(EventStorageModel.status == status.value)
                    result = await session.execute(count_query)
                    status_counts[status.value] = len(result.scalars().all())
                
                # Count by event type (top 10)
                type_query = base_query.with_only_columns(EventStorageModel.event_type)
                result = await session.execute(type_query)
                event_types = [row[0] for row in result.fetchall()]
                
                from collections import Counter
                top_event_types = dict(Counter(event_types).most_common(10))
                
                return {
                    "status_counts": status_counts,
                    "top_event_types": top_event_types,
                    "total_events": sum(status_counts.values()),
                    "query_time_range": {
                        "start_time": start_time.isoformat() if start_time else None,
                        "end_time": end_time.isoformat() if end_time else None
                    }
                }
        
        except Exception as e:
            self.logger.error("Failed to get event statistics", error=str(e))
            return {}
    
    async def get_correlation_chain(
        self,
        tenant_id: UUID,
        correlation_id: UUID
    ) -> List[Dict[str, Any]]:
        """Get all events in a correlation chain"""
        try:
            async with self.async_session() as session:
                query = select(EventStorageModel).where(
                    and_(
                        EventStorageModel.tenant_id == tenant_id,
                        or_(
                            EventStorageModel.correlation_id == correlation_id,
                            EventStorageModel.causation_id == correlation_id
                        )
                    )
                ).order_by(EventStorageModel.timestamp)
                
                result = await session.execute(query)
                events = result.scalars().all()
                
                return [self._event_to_dict(event) for event in events]
        
        except Exception as e:
            self.logger.error(
                "Failed to get correlation chain",
                correlation_id=str(correlation_id),
                error=str(e)
            )
            return []
    
    async def health_check(self) -> bool:
        """Check if event store is healthy"""
        try:
            async with self.async_session() as session:
                # Simple query to test connection
                await session.execute(select(1))
                return True
        
        except Exception as e:
            self.logger.error("Event store health check failed", error=str(e))
            return False
    
    def _event_to_dict(self, event: EventStorageModel) -> Dict[str, Any]:
        """Convert storage model to dictionary"""
        return {
            "event_id": str(event.event_id),
            "event_type": event.event_type,
            "event_version": event.event_version,
            "timestamp": event.timestamp.isoformat(),
            "created_at": event.created_at.isoformat(),
            "updated_at": event.updated_at.isoformat() if event.updated_at else None,
            "tenant_id": str(event.tenant_id),
            "source_service": event.source_service,
            "correlation_id": str(event.correlation_id) if event.correlation_id else None,
            "causation_id": str(event.causation_id) if event.causation_id else None,
            "category": event.category,
            "priority": event.priority,
            "aggregate_id": str(event.aggregate_id) if event.aggregate_id else None,
            "aggregate_type": event.aggregate_type,
            "data": event.data,
            "metadata": event.metadata,
            "status": event.status,
            "retry_count": event.retry_count,
            "max_retries": event.max_retries,
            "last_error": event.last_error,
            "target_services": event.target_services,
            "routing_key": event.routing_key,
            "processed_at": event.processed_at.isoformat() if event.processed_at else None,
            "processed_by": event.processed_by,
            "processing_time_ms": event.processing_time_ms,
        }
    
    async def close(self) -> None:
        """Close the event store"""
        if self.engine:
            await self.engine.dispose()