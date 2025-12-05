"""
Base Domain Models and Aggregates for DDD Implementation

This module provides the foundation for Domain-Driven Design patterns including:
- Base Aggregate Root
- Base Entity and Value Object
- Domain Events
- Repository interfaces
"""

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol, Type, TypeVar, Generic
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import structlog

logger = structlog.get_logger(__name__)

# SQLAlchemy Base
Base = declarative_base()

# Type variables for generics
T = TypeVar('T')
AggregateType = TypeVar('AggregateType', bound='AggregateRoot')


class DomainEvent(BaseModel):
    """Base class for all domain events"""
    
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    aggregate_id: UUID
    aggregate_type: str
    tenant_id: UUID
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class ValueObject(BaseModel, ABC):
    """Base class for value objects - immutable objects with no identity"""
    
    class Config:
        frozen = True  # Make immutable
        validate_assignment = True


class Entity(BaseModel, ABC):
    """Base class for entities - objects with identity"""
    
    id: UUID = Field(default_factory=uuid4)
    tenant_id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    version: int = Field(default=1)
    
    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)


class AggregateRoot(Entity, ABC):
    """
    Base class for aggregate roots - entities that serve as the consistency boundary
    and the only entry point for modifying the aggregate
    """
    
    def __init__(self, **data):
        super().__init__(**data)
        self._domain_events: List[DomainEvent] = []
        self._is_dirty = False
    
    @property
    def domain_events(self) -> List[DomainEvent]:
        """Get uncommitted domain events"""
        return self._domain_events.copy()
    
    def clear_events(self) -> None:
        """Clear domain events (called after successful persistence)"""
        self._domain_events.clear()
        self._is_dirty = False
    
    def add_domain_event(self, event: DomainEvent) -> None:
        """Add a domain event to be published"""
        self._domain_events.append(event)
        self._is_dirty = True
        logger.debug(
            "Domain event added",
            event_type=event.event_type,
            aggregate_id=str(self.id),
            aggregate_type=event.aggregate_type
        )
    
    def mark_events_as_committed(self) -> None:
        """Mark events as committed (called after successful publication)"""
        self.clear_events()
    
    @property
    def is_dirty(self) -> bool:
        """Check if aggregate has uncommitted changes"""
        return self._is_dirty or len(self._domain_events) > 0
    
    def increment_version(self) -> None:
        """Increment version for optimistic concurrency control"""
        self.version += 1
        self.updated_at = datetime.utcnow()
        self._is_dirty = True


class Repository(Protocol, Generic[AggregateType]):
    """Generic repository interface following the Repository pattern"""
    
    @abstractmethod
    async def get_by_id(self, aggregate_id: UUID, tenant_id: UUID) -> Optional[AggregateType]:
        """Get aggregate by ID within tenant context"""
        pass
    
    @abstractmethod
    async def save(self, aggregate: AggregateType) -> AggregateType:
        """Save aggregate and publish domain events"""
        pass
    
    @abstractmethod
    async def delete(self, aggregate_id: UUID, tenant_id: UUID) -> bool:
        """Delete aggregate by ID within tenant context"""
        pass
    
    @abstractmethod
    async def exists(self, aggregate_id: UUID, tenant_id: UUID) -> bool:
        """Check if aggregate exists within tenant context"""
        pass


class Specification(ABC):
    """Base class for specifications (business rules)"""
    
    @abstractmethod
    async def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if the candidate satisfies this specification"""
        pass
    
    def and_(self, other: 'Specification') -> 'AndSpecification':
        """Combine with another specification using AND logic"""
        return AndSpecification(self, other)
    
    def or_(self, other: 'Specification') -> 'OrSpecification':
        """Combine with another specification using OR logic"""
        return OrSpecification(self, other)
    
    def not_(self) -> 'NotSpecification':
        """Negate this specification"""
        return NotSpecification(self)


class AndSpecification(Specification):
    """Combines two specifications with AND logic"""
    
    def __init__(self, left: Specification, right: Specification):
        self.left = left
        self.right = right
    
    async def is_satisfied_by(self, candidate: Any) -> bool:
        left_result = await self.left.is_satisfied_by(candidate)
        if not left_result:
            return False
        return await self.right.is_satisfied_by(candidate)


class OrSpecification(Specification):
    """Combines two specifications with OR logic"""
    
    def __init__(self, left: Specification, right: Specification):
        self.left = left
        self.right = right
    
    async def is_satisfied_by(self, candidate: Any) -> bool:
        left_result = await self.left.is_satisfied_by(candidate)
        if left_result:
            return True
        return await self.right.is_satisfied_by(candidate)


class NotSpecification(Specification):
    """Negates a specification"""
    
    def __init__(self, spec: Specification):
        self.spec = spec
    
    async def is_satisfied_by(self, candidate: Any) -> bool:
        result = await self.spec.is_satisfied_by(candidate)
        return not result


class DomainException(Exception):
    """Base class for domain-specific exceptions"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class BusinessRuleViolation(DomainException):
    """Raised when a business rule is violated"""
    pass


class ConcurrencyException(DomainException):
    """Raised when optimistic concurrency control fails"""
    pass


class TenantIsolationViolation(DomainException):
    """Raised when tenant isolation is violated"""
    pass


# Base SQLAlchemy model for database entities
class BaseEntity(Base):
    """Base SQLAlchemy model with common fields"""
    
    __abstract__ = True
    
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(PGUUID(as_uuid=True), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    version = Column("version", Integer, default=1, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Audit fields
    created_by = Column(PGUUID(as_uuid=True))
    updated_by = Column(PGUUID(as_uuid=True))
    
    def to_domain(self) -> Entity:
        """Convert SQLAlchemy model to domain entity"""
        raise NotImplementedError("Subclasses must implement to_domain method")
    
    @classmethod
    def from_domain(cls, domain_entity: Entity) -> 'BaseEntity':
        """Create SQLAlchemy model from domain entity"""
        raise NotImplementedError("Subclasses must implement from_domain method")


class UnitOfWork(ABC):
    """Unit of Work pattern for managing transactions"""
    
    def __init__(self):
        self._repositories: Dict[str, Repository] = {}
        self._committed = False
    
    async def __aenter__(self):
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
    
    @abstractmethod
    async def start(self) -> None:
        """Start the unit of work"""
        pass
    
    @abstractmethod
    async def commit(self) -> None:
        """Commit all changes"""
        pass
    
    @abstractmethod
    async def rollback(self) -> None:
        """Rollback all changes"""
        pass
    
    def register_repository(self, name: str, repository: Repository) -> None:
        """Register a repository with the unit of work"""
        self._repositories[name] = repository
    
    def get_repository(self, name: str) -> Repository:
        """Get a registered repository"""
        return self._repositories.get(name)


class EventPublisher(ABC):
    """Interface for publishing domain events"""
    
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        """Publish a single domain event"""
        pass
    
    @abstractmethod
    async def publish_many(self, events: List[DomainEvent]) -> None:
        """Publish multiple domain events"""
        pass