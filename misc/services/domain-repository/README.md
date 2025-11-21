# BizOSaaS Domain Repository Service

A comprehensive Domain-Driven Design (DDD) implementation for managing business domain aggregates with event sourcing, multi-tenant isolation, and seamless Event Bus integration.

## Overview

The Domain Repository Service serves as the central authority for business entities and rules across the BizOSaaS platform. It implements Domain-Driven Design patterns to ensure consistent business logic enforcement and provides a clean API for other services to interact with core business entities.

## Key Features

### 🏗️ Domain-Driven Design
- **Rich Domain Models**: Fully featured aggregate roots with encapsulated business logic
- **Repository Pattern**: Clean abstractions for data access with automatic event publishing
- **Value Objects**: Immutable objects representing domain concepts
- **Specification Pattern**: Composable business rules and validation
- **Business Rule Enforcement**: Automatic validation of domain invariants

### 🔄 Event-Driven Architecture
- **Event Bus Integration**: Seamless integration with BizOSaaS Event Bus (port 8009)
- **Domain Events**: Automatic publishing of domain events on aggregate changes
- **Event Sourcing Ready**: Built with event sourcing patterns in mind
- **Asynchronous Processing**: Non-blocking event publishing with retry logic

### 🏢 Multi-Tenant Support
- **Tenant Isolation**: Complete isolation of data and operations by tenant
- **Row-Level Security**: Database-level tenant isolation
- **Tenant Context**: Automatic tenant validation in all operations
- **UUID-Based**: Globally unique identifiers for all entities

### ⚡ High Performance
- **Async/Await**: Fully asynchronous operations using SQLAlchemy async
- **Connection Pooling**: Optimized database connection management
- **Optimistic Concurrency**: Version-based concurrency control
- **Caching Ready**: Built-in support for Redis caching

### 🛡️ Production Ready
- **Error Handling**: Comprehensive error handling with structured logging
- **Health Checks**: Built-in health monitoring endpoints
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Type Safety**: Full type annotations with Pydantic models

## Core Domain Aggregates

### 1. Lead Aggregate
Manages the complete lead lifecycle from capture to conversion:

```python
# Create a lead
lead = await lead_service.create_lead(
    tenant_id=tenant_id,
    contact_info=ContactInfo(
        email="prospect@example.com",
        first_name="John",
        last_name="Doe",
        company="Example Corp"
    ),
    source=LeadSource.WEBSITE_FORM,
    utm_parameters={"utm_campaign": "spring_promotion"}
)

# Qualify the lead
qualified_lead = await lead_service.qualify_lead(
    lead_id=lead.id,
    tenant_id=tenant_id,
    user_id=sales_rep_id,
    score=LeadScore(total_score=85, behavioral_score=90)
)

# Convert to customer
customer = await lead_service.convert_lead_to_customer(
    lead_id=lead.id,
    tenant_id=tenant_id,
    user_id=sales_rep_id,
    conversion_value=Decimal("5000.00")
)
```

**Features:**
- Lead scoring with multiple dimensions
- Status transition validation
- Lead-to-customer conversion
- Interaction tracking
- Attribution management

### 2. Customer Aggregate
Manages customer lifecycle and relationship data:

```python
# Update customer profile
customer = await customer_service.update_customer_profile(
    customer_id=customer_id,
    tenant_id=tenant_id,
    new_profile=CustomerProfile(
        email="updated@example.com",
        company_name="Updated Corp",
        annual_revenue=Decimal("1000000")
    )
)

# Record a purchase
customer = await customer_service.record_customer_purchase(
    customer_id=customer_id,
    tenant_id=tenant_id,
    order_value=Decimal("2500.00")
)

# Upgrade tier automatically based on value
if customer.metrics.total_revenue >= 10000:
    await customer_service.upgrade_customer_tier(
        customer_id=customer_id,
        tenant_id=tenant_id,
        new_tier=CustomerTier.GOLD
    )
```

**Features:**
- Customer segmentation and tiering
- Churn risk calculation
- Purchase history tracking
- Automatic tier upgrades
- Communication preferences

### 3. Campaign Aggregate
Manages marketing campaigns with AI optimization:

```python
# Create a campaign
campaign = await campaign_service.create_campaign(
    tenant_id=tenant_id,
    name="Spring Product Launch",
    campaign_type=CampaignType.MULTI_CHANNEL,
    objective=CampaignObjective.LEAD_GENERATION,
    budget=CampaignBudget(
        total_budget=Decimal("10000.00"),
        daily_budget=Decimal("500.00")
    ),
    schedule=CampaignSchedule(
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=30)
    )
)

# Launch the campaign
launched_campaign = await campaign_service.launch_campaign(
    campaign_id=campaign.id,
    tenant_id=tenant_id,
    user_id=marketing_manager_id
)

# Enable AI optimization
optimized_campaign = await campaign_service.enable_ai_optimization(
    campaign_id=campaign.id,
    tenant_id=tenant_id,
    optimization_goal=OptimizationGoal.MINIMIZE_CPA,
    user_id=marketing_manager_id
)
```

**Features:**
- Multi-channel campaign coordination
- Budget management and allocation
- AI-driven optimization
- Performance tracking
- Real-time metrics

## API Endpoints

### Lead Management
- `POST /api/v1/leads` - Create a new lead
- `GET /api/v1/leads/{lead_id}` - Get lead details
- `POST /api/v1/leads/{lead_id}/qualify` - Qualify a lead
- `POST /api/v1/leads/{lead_id}/convert` - Convert lead to customer
- `GET /api/v1/leads` - List qualified leads

### Customer Management
- `GET /api/v1/customers/{customer_id}` - Get customer details
- `PUT /api/v1/customers/{customer_id}/profile` - Update customer profile
- `GET /api/v1/customers/at-risk` - List customers at churn risk

### Campaign Management
- `POST /api/v1/campaigns` - Create a new campaign
- `POST /api/v1/campaigns/{campaign_id}/launch` - Launch campaign
- `GET /api/v1/campaigns/active` - List active campaigns

### Health & Monitoring
- `GET /health` - Simple health check
- `GET /health/` - Detailed health check with statistics

## Architecture

### Layer Structure
```
├── api/                    # FastAPI routes and models
│   ├── models.py          # Pydantic request/response models
│   ├── routers.py         # API route definitions
│   └── dependencies.py    # Dependency injection
├── application/           # Application services
│   └── services.py        # Use case orchestration
├── domain/               # Core domain logic
│   ├── base.py           # Base DDD patterns
│   └── aggregates/       # Domain aggregates
│       ├── lead.py       # Lead aggregate and events
│       ├── customer.py   # Customer aggregate and events
│       └── campaign.py   # Campaign aggregate and events
├── infrastructure/       # External concerns
│   ├── repositories.py   # Data persistence
│   └── event_bus_integration.py  # Event publishing
├── database.py           # Database setup and management
├── config.py            # Configuration management
└── main.py              # FastAPI application
```

### Event Flow
1. **Domain Operation** → Business logic executed in aggregate
2. **Domain Events** → Events generated by aggregate
3. **Repository Save** → Data persisted with optimistic locking
4. **Event Publishing** → Events sent to Event Bus
5. **Event Distribution** → Other services receive events
6. **Business Reactions** → AI agents, analytics, etc. react

## Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql+asyncpg://admin:securepassword@localhost:5432/bizosaas

# Event Bus
EVENT_BUS_URL=http://localhost:8009
ENABLE_EVENT_PUBLISHING=true

# Application
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-super-secret-key-here

# Redis (optional)
REDIS_URL=redis://localhost:6379/0
```

### Docker Deployment
```dockerfile
# Build and run with Docker
docker build -t bizosaas/domain-repository .
docker run -p 8011:8011 \
  -e DATABASE_URL=postgresql+asyncpg://admin:securepassword@db:5432/bizosaas \
  -e EVENT_BUS_URL=http://event-bus:8009 \
  bizosaas/domain-repository
```

## Integration Examples

### With AI Agents Service
```python
# AI Agents can listen for domain events
@event_handler("lead.qualified")
async def analyze_qualified_lead(event: LeadQualified):
    lead_id = event.data["lead_id"]
    tenant_id = event.tenant_id
    
    # Perform AI analysis
    analysis = await ai_service.analyze_lead(lead_id, tenant_id)
    
    # Update lead score based on AI insights
    await domain_repository.update_lead_score(
        lead_id=lead_id,
        tenant_id=tenant_id,
        new_score=analysis.suggested_score
    )
```

### With CRM Service
```python
# CRM can react to customer events
@event_handler("customer.churn_risk_updated")
async def handle_churn_risk(event: CustomerChurnRiskUpdated):
    if event.data["new_churn_risk"] >= 80:
        # Create high-priority task in CRM
        await crm_service.create_retention_task(
            customer_id=event.aggregate_id,
            tenant_id=event.tenant_id,
            priority="high"
        )
```

### With Analytics Service
```python
# Analytics can track all domain events
@event_handler("*")  # Listen to all events
async def track_domain_event(event: BaseEvent):
    await analytics_service.record_event(
        event_type=event.event_type,
        tenant_id=event.tenant_id,
        data=event.data,
        timestamp=event.occurred_at
    )
```

## Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env

# Initialize database
python -c "from database import init_database; import asyncio; asyncio.run(init_database())"

# Run the service
python main.py
```

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=domain-repository

# Test specific aggregate
pytest tests/test_lead_aggregate.py
```

### API Documentation
When running in development mode, API documentation is available at:
- Swagger UI: http://localhost:8011/docs
- ReDoc: http://localhost:8011/redoc
- OpenAPI JSON: http://localhost:8011/openapi.json

## Monitoring & Observability

### Health Checks
- **Simple**: `GET /health` - Basic connectivity check
- **Detailed**: `GET /health/` - Service statistics and component health

### Structured Logging
All operations are logged with structured JSON logs including:
- Request correlation IDs
- Tenant context
- Performance metrics
- Error details

### Metrics
Integration with Prometheus-compatible metrics:
- Request duration
- Event publishing rates
- Database query performance
- Error rates by type

## Security

### Multi-Tenant Isolation
- All operations require valid tenant context
- Row-level security in database
- Tenant validation in all API endpoints

### Authentication
- Header-based tenant identification (`X-Tenant-ID`)
- Optional user context (`X-User-ID`)
- JWT token support (when available)

### Data Protection
- Sensitive data encryption
- Audit logging
- GDPR compliance ready

## Performance

### Optimizations
- Async/await throughout
- Connection pooling
- Optimistic concurrency control
- Efficient queries with proper indexing

### Scalability
- Stateless design
- Horizontal scaling ready
- Event-driven architecture
- Caching support

## Error Handling

### Business Rule Violations
```json
{
  "error": "BUSINESS_RULE_VIOLATION",
  "message": "Cannot convert unqualified lead to customer",
  "details": {
    "lead_id": "123e4567-e89b-12d3-a456-426614174000",
    "current_status": "new"
  }
}
```

### Concurrency Conflicts
```json
{
  "error": "CONCURRENCY_EXCEPTION",
  "message": "Entity was modified by another process",
  "details": {
    "expected_version": 5,
    "actual_version": 7
  }
}
```

### Tenant Isolation Violations
```json
{
  "error": "TENANT_ISOLATION_VIOLATION",
  "message": "Entity not found or access denied",
  "details": {
    "tenant_id": "00000000-0000-4000-8000-000000000001"
  }
}
```

## Contributing

1. Follow Domain-Driven Design principles
2. Add comprehensive tests for new aggregates
3. Update API documentation
4. Ensure event publishing works correctly
5. Maintain backward compatibility

## License

Part of the BizOSaaS platform - Internal use only.