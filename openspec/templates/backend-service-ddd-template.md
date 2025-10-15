# [Service Name] - Backend Service (DDD)

## Service Identity
- **Name**: [Service Name]
- **Type**: Backend - [Service Type]
- **Container**: `[container-name]`
- **Image**: `[image-name]`
- **Port**: `[external:internal]`
- **Domain**: `[domain or N/A]`
- **Status**: [✅ Running | ❌ Not Running | ⚠️ Unhealthy]

## Purpose
[Brief description of what this service does and why it exists]

## Domain-Driven Design Architecture

### Bounded Context
```
[Service Name] Bounded Context
├── Domain Layer
│   ├── Entities (Business Objects)
│   ├── Value Objects (Immutable Objects)
│   ├── Aggregates (Consistency Boundaries)
│   ├── Domain Events (State Changes)
│   ├── Domain Services (Business Logic)
│   └── Repository Interfaces (Data Access Contracts)
├── Application Layer
│   ├── Use Cases / Commands
│   ├── Query Handlers
│   ├── Application Services
│   └── DTOs (Data Transfer Objects)
├── Infrastructure Layer
│   ├── Repository Implementations
│   ├── External Service Adapters
│   ├── Database Migrations
│   └── Message Queue Adapters
└── API Layer (Interface)
    ├── REST Endpoints
    ├── GraphQL Resolvers (if applicable)
    ├── Request/Response Models
    └── API Documentation
```

### Core Domain Model

#### Aggregates
```python
# [Aggregate Name] - Main aggregate root
class [AggregateName]:
    """
    [Description of aggregate and its responsibility]

    Invariants:
    - [Business rule 1]
    - [Business rule 2]
    """
    def __init__(self, id: UUID, ...):
        self.id = id
        self._domain_events: List[DomainEvent] = []

    def [business_method](self, ...):
        """[Business operation description]"""
        # Business logic
        # Emit domain event
        self._add_domain_event([EventName](...))

    def _add_domain_event(self, event: DomainEvent):
        self._domain_events.append(event)

    @property
    def domain_events(self) -> List[DomainEvent]:
        return self._domain_events
```

#### Entities
```python
class [EntityName]:
    """[Entity description]"""
    def __init__(self, id: UUID, ...):
        self.id = id
        # Entity attributes
```

#### Value Objects
```python
@dataclass(frozen=True)
class [ValueObjectName]:
    """Immutable value object for [description]"""
    value: str

    def __post_init__(self):
        # Validation logic
        if not self._is_valid():
            raise ValueError(f"Invalid {self.__class__.__name__}")

    def _is_valid(self) -> bool:
        # Validation rules
        return True
```

#### Domain Events
```python
@dataclass
class [EventName]:
    """Emitted when [condition]"""
    aggregate_id: UUID
    tenant_id: UUID
    timestamp: datetime
    # Event data
```

### Domain Services
```python
class [DomainServiceName]:
    """
    Domain service for [complex business logic that doesn't belong to a single entity]
    """
    def [operation](self, ...):
        # Complex business logic
        pass
```

### Repository Interfaces
```python
from abc import ABC, abstractmethod

class [RepositoryName](ABC):
    """Repository interface for [Aggregate]"""

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[[Aggregate]]:
        pass

    @abstractmethod
    async def save(self, aggregate: [Aggregate]) -> None:
        pass

    @abstractmethod
    async def list_by_tenant(self, tenant_id: UUID) -> List[[Aggregate]]:
        pass
```

## Application Layer

### Use Cases / Commands
```python
@dataclass
class [CommandName]:
    """Command to [action]"""
    tenant_id: UUID
    # Command parameters

class [CommandHandler]:
    """Handles [CommandName]"""
    def __init__(self, repository: [RepositoryName], event_bus: EventBus):
        self.repository = repository
        self.event_bus = event_bus

    async def handle(self, command: [CommandName]) -> [Result]:
        # Load aggregate
        aggregate = await self.repository.get_by_id(command.id)

        # Execute business logic
        aggregate.[business_method](...)

        # Save aggregate
        await self.repository.save(aggregate)

        # Publish domain events
        for event in aggregate.domain_events:
            await self.event_bus.publish(event)

        return result
```

### Query Handlers (CQRS)
```python
class [QueryName]:
    """Query for [data]"""
    tenant_id: UUID
    # Query parameters

class [QueryHandler]:
    """Handles [QueryName]"""
    async def handle(self, query: [QueryName]) -> [Result]:
        # Direct database query (bypassing domain model for reads)
        return result
```

## Infrastructure Layer

### Repository Implementation
```python
from sqlalchemy.ext.asyncio import AsyncSession

class [RepositoryImplementation]([RepositoryName]):
    """PostgreSQL implementation of [RepositoryName]"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> Optional[[Aggregate]]:
        result = await self.session.execute(
            select([Model]).where([Model].id == id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def save(self, aggregate: [Aggregate]) -> None:
        model = self._to_model(aggregate)
        self.session.add(model)
        await self.session.commit()

    def _to_domain(self, model) -> [Aggregate]:
        """Map database model to domain aggregate"""
        return [Aggregate](...)

    def _to_model(self, aggregate: [Aggregate]):
        """Map domain aggregate to database model"""
        return [Model](...)
```

### External Service Adapter
```python
class [ExternalServiceName]:
    """Adapter for [external service]"""

    async def [operation](self, ...):
        # Call external API
        # Transform response to domain objects
        pass
```

## API Layer

### FastAPI Endpoints
```python
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/[resource]", tags=["[Tag]"])

@router.post("/")
async def create_[resource](
    request: [RequestModel],
    tenant_id: UUID = Depends(get_current_tenant)
):
    """Create new [resource]"""
    command = [CommandName](
        tenant_id=tenant_id,
        ...
    )
    result = await command_bus.handle(command)
    return result

@router.get("/{id}")
async def get_[resource](
    id: UUID,
    tenant_id: UUID = Depends(get_current_tenant)
):
    """Get [resource] by ID"""
    query = [QueryName](tenant_id=tenant_id, id=id)
    result = await query_bus.handle(query)

    if not result:
        raise HTTPException(status_code=404, detail="Not found")

    return result

@router.put("/{id}")
async def update_[resource](
    id: UUID,
    request: [UpdateRequestModel],
    tenant_id: UUID = Depends(get_current_tenant)
):
    """Update [resource]"""
    command = [UpdateCommandName](...)
    result = await command_bus.handle(command)
    return result

@router.delete("/{id}")
async def delete_[resource](
    id: UUID,
    tenant_id: UUID = Depends(get_current_tenant)
):
    """Delete [resource]"""
    command = [DeleteCommandName](...)
    await command_bus.handle(command)
    return {"status": "deleted"}
```

### Request/Response Models (Pydantic)
```python
from pydantic import BaseModel, Field

class [RequestModel](BaseModel):
    """Request model for creating [resource]"""
    field1: str = Field(..., description="...")
    field2: int = Field(..., gt=0, description="...")

class [ResponseModel](BaseModel):
    """Response model for [resource]"""
    id: UUID
    field1: str
    field2: int
    created_at: datetime

    class Config:
        from_attributes = True
```

## Configuration

### Environment Variables
```bash
# Service Configuration
[SERVICE]_HOST=0.0.0.0
[SERVICE]_PORT=[port]
[SERVICE]_LOG_LEVEL=info

# Database
DATABASE_URL=postgresql://postgres:password@bizosaas-postgres-staging:5432/bizosaas_platform

# Redis
REDIS_URL=redis://bizosaas-redis-staging:6379/0

# External Services
[EXTERNAL_SERVICE]_API_KEY=${VAULT:[path]}
```

### Docker Compose Configuration
```yaml
services:
  [service-name]:
    build:
      context: ./path/to/service
      dockerfile: Dockerfile
    container_name: [container-name]
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - VAULT_ADDR=http://bizosaas-vault-staging:8200
    ports:
      - "[external]:[internal]"
    networks:
      - dokploy-network
    depends_on:
      - postgres
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:[port]/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
```

## Multi-Tenancy

### Tenant Context Middleware
```python
from fastapi import Request, Depends
from sqlalchemy import text

async def set_tenant_context(
    request: Request,
    tenant_id: UUID = Depends(get_current_tenant)
):
    """Set PostgreSQL tenant context for RLS"""
    async with get_db_session() as session:
        await session.execute(
            text(f"SET app.current_tenant_id = '{tenant_id}'")
        )
```

### Row-Level Security
```sql
-- Enable RLS on tables
ALTER TABLE [table_name] ENABLE ROW LEVEL SECURITY;

-- Create tenant isolation policy
CREATE POLICY tenant_isolation_policy ON [table_name]
    USING (tenant_id = current_setting('app.current_tenant_id')::UUID);
```

## Event-Driven Architecture

### Event Publishing
```python
class EventBus:
    """Event bus for publishing domain events"""

    def __init__(self, redis_client):
        self.redis = redis_client

    async def publish(self, event: DomainEvent):
        """Publish event to Redis Stream"""
        stream_name = f"events:{event.__class__.__name__}"
        await self.redis.xadd(
            stream_name,
            {
                "event_type": event.__class__.__name__,
                "tenant_id": str(event.tenant_id),
                "data": event.json()
            }
        )
```

### Event Consumers
```python
async def consume_events():
    """Consume domain events"""
    while True:
        events = await redis_client.xread({
            "events:*": "$"
        })

        for stream, messages in events:
            for message_id, data in messages:
                event = deserialize_event(data)
                await handle_event(event)
```

## Testing Strategy

### Domain Tests (Unit)
```python
def test_[aggregate]_[business_operation]():
    # Arrange
    aggregate = [Aggregate](...)

    # Act
    aggregate.[business_method](...)

    # Assert
    assert aggregate.[property] == expected_value
    assert len(aggregate.domain_events) == 1
    assert isinstance(aggregate.domain_events[0], [EventName])
```

### Application Tests (Integration)
```python
@pytest.mark.asyncio
async def test_[command_handler]():
    # Arrange
    repository = Mock([RepositoryName])
    handler = [CommandHandler](repository, event_bus)
    command = [CommandName](...)

    # Act
    result = await handler.handle(command)

    # Assert
    assert result is not None
    repository.save.assert_called_once()
```

### API Tests (End-to-End)
```python
from fastapi.testclient import TestClient

def test_create_[resource]():
    client = TestClient(app)
    response = client.post(
        "/[resource]",
        json={...},
        headers={"Authorization": "Bearer token"}
    )
    assert response.status_code == 200
    assert response.json()["id"] is not None
```

## Health Checks

```python
@router.get("/health")
async def health_check():
    """Service health check"""
    return {
        "status": "healthy",
        "service": "[service-name]",
        "version": "1.0.0",
        "database": await check_database(),
        "redis": await check_redis()
    }
```

## Dependencies
- PostgreSQL (database)
- Redis (caching, events)
- Vault (secrets)
- [Other services]

## Integration Points
- Brain API Gateway (routing)
- [Other services]

## Monitoring
- Request latency
- Error rate
- Database query performance
- Domain event throughput

## Common Issues
[Common problems and solutions]

## Deployment Checklist
- [ ] Database schema created
- [ ] RLS policies applied
- [ ] Environment variables configured
- [ ] Health checks passing
- [ ] Integration tests passing
- [ ] API documentation generated
- [ ] Monitoring configured

## References
- DDD Blue Book (Eric Evans)
- Implementing Domain-Driven Design (Vaughn Vernon)
- BizOSaaS PRD: `/home/alagiri/projects/bizoholic/comprehensive_prd_06092025.md`

---
**Status**: [Status]
**Last Updated**: October 15, 2025
**Owner**: Backend Team
