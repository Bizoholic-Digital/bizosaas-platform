# Brain API Gateway - Backend Service (DDD)

## Service Identity
- **Name**: Brain API Gateway
- **Type**: Backend - Central API Gateway & Routing Hub
- **Container**: `bizosaas-brain-staging`
- **Image**: `bizosaas/brain-gateway:latest`
- **Port**: `8001:8001` (external:internal)
- **Status**: ✅ Running (20+ hours uptime)

## Purpose
FastAPI centralized brain and API gateway where 93 CrewAI + LangChain AI agents make autonomous decisions, orchestrating specialized data stores (Wagtail CMS, Saleor, Django CRM) through unified internal APIs.

## Domain-Driven Design Architecture

### Bounded Context
**Brain Gateway Context** - Central coordination and routing for all platform operations

```
Brain Gateway Bounded Context
├── Domain Layer
│   ├── Entities: Request, Route, Integration
│   ├── Aggregates: ServiceRoute, IntegrationConfig
│   ├── Value Objects: HttpMethod, RoutePattern, ApiKey
│   ├── Domain Events: RouteRegistered, ServiceHealthChanged, IntegrationActivated
│   ├── Domain Services: RoutingStrategy, LoadBalancer, CircuitBreaker
│   └── Repository Interfaces: IRouteRepository, IIntegrationRepository
├── Application Layer
│   ├── Commands: RegisterServiceCommand, UpdateRouteCommand
│   ├── Queries: GetHealthStatusQuery, ListServicesQuery
│   ├── Handlers: RequestRouter, HealthMonitor, MetricsCollector
│   └── DTOs: ServiceRegistrationDTO, RouteConfigDTO
├── Infrastructure Layer
│   ├── HTTP Client Adapter (httpx)
│   ├── Redis Caching Layer
│   ├── PostgreSQL Route Storage
│   └── Vault Integration (API keys)
└── API Layer
    ├── REST Endpoints (FastAPI)
    ├── WebSocket Gateway
    ├── GraphQL Endpoint
    └── OpenAPI Documentation
```

### Core Aggregates

#### ServiceRoute Aggregate
```python
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from uuid import UUID, uuid4

class ServiceStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DOWN = "down"

class ServiceRoute:
    """
    Aggregate root for service routing configuration
    
    Invariants:
    - Service name must be unique per tenant
    - At least one route must be healthy
    - Circuit breaker thresholds must be valid
    """
    def __init__(
        self,
        id: UUID,
        service_name: str,
        base_url: str,
        tenant_id: Optional[UUID] = None
    ):
        self.id = id
        self.service_name = service_name
        self.base_url = base_url
        self.tenant_id = tenant_id
        self.routes: List[Route] = []
        self.health_status = ServiceStatus.HEALTHY
        self.circuit_breaker_threshold = 5
        self.failure_count = 0
        self._domain_events: List[DomainEvent] = []

    def register_route(self, path: str, method: HttpMethod, target_service: str):
        """Register new route to target service"""
        route = Route(
            id=uuid4(),
            path=path,
            method=method,
            target_service=target_service,
            service_route_id=self.id
        )
        self.routes.append(route)
        self._add_domain_event(RouteRegisteredEvent(
            service_id=self.id,
            route_path=path,
            tenant_id=self.tenant_id
        ))

    def update_health_status(self, is_healthy: bool):
        """Update service health status"""
        if is_healthy:
            self.failure_count = 0
            old_status = self.health_status
            self.health_status = ServiceStatus.HEALTHY
        else:
            self.failure_count += 1
            old_status = self.health_status
            
            if self.failure_count >= self.circuit_breaker_threshold:
                self.health_status = ServiceStatus.DOWN
            else:
                self.health_status = ServiceStatus.DEGRADED

        if old_status != self.health_status:
            self._add_domain_event(ServiceHealthChangedEvent(
                service_id=self.id,
                old_status=old_status,
                new_status=self.health_status,
                tenant_id=self.tenant_id
            ))

    def can_route_request(self) -> bool:
        """Check if service can handle requests"""
        return self.health_status != ServiceStatus.DOWN

    def _add_domain_event(self, event: DomainEvent):
        self._domain_events.append(event)
```

#### Integration Aggregate
```python
class IntegrationConfig:
    """
    Aggregate for external API integrations (40+ integrations)
    
    Manages:
    - API credentials (from Vault)
    - Rate limiting
    - Retry policies
    - Integration health
    """
    def __init__(
        self,
        id: UUID,
        integration_name: str,
        category: IntegrationCategory,
        tenant_id: UUID
    ):
        self.id = id
        self.integration_name = integration_name
        self.category = category
        self.tenant_id = tenant_id
        self.is_active = False
        self.rate_limit_per_minute = 60
        self.retry_count = 3
        self._domain_events: List[DomainEvent] = []

    def activate(self, credentials: dict):
        """Activate integration with credentials"""
        if not self._validate_credentials(credentials):
            raise ValueError("Invalid credentials")
        
        self.is_active = True
        self._add_domain_event(IntegrationActivatedEvent(
            integration_id=self.id,
            integration_name=self.integration_name,
            tenant_id=self.tenant_id
        ))

    def _validate_credentials(self, credentials: dict) -> bool:
        required_fields = self._get_required_fields()
        return all(field in credentials for field in required_fields)
```

### Value Objects
```python
@dataclass(frozen=True)
class HttpMethod:
    value: str

    def __post_init__(self):
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        if self.value.upper() not in valid_methods:
            raise ValueError(f"Invalid HTTP method: {self.value}")

@dataclass(frozen=True)
class RoutePattern:
    pattern: str

    def matches(self, path: str) -> bool:
        import re
        regex = self.pattern.replace("{", "(?P<").replace("}", ">[^/]+)")
        return bool(re.match(f"^{regex}$", path))
```

### Domain Events
```python
@dataclass
class RouteRegisteredEvent:
    service_id: UUID
    route_path: str
    tenant_id: Optional[UUID]
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class ServiceHealthChangedEvent:
    service_id: UUID
    old_status: ServiceStatus
    new_status: ServiceStatus
    tenant_id: Optional[UUID]
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class IntegrationActivatedEvent:
    integration_id: UUID
    integration_name: str
    tenant_id: UUID
    timestamp: datetime = field(default_factory=datetime.utcnow)
```

## Registered Services

### Current Service Registry (13 services)
```python
REGISTERED_SERVICES = {
    # AI & ML
    "ai-agents": {"port": 8008, "path": "/api/v1/agents"},
    
    # Backend Services
    "auth-service": {"port": 8007, "path": "/api/v1/auth"},
    "wagtail-cms": {"port": 8002, "path": "/api/v1/cms"},
    "saleor-backend": {"port": 8000, "path": "/graphql"},
    "django-crm": {"port": 8003, "path": "/api/v1/crm"},
    "coreldove-backend": {"port": 8005, "path": "/api/v1/coreldove"},
    "amazon-sourcing": {"port": 8009, "path": "/api/v1/amazon"},
    "business-directory": {"port": 8004, "path": "/api/v1/directory"},
    "quanttrade-backend": {"port": 8012, "path": "/api/v1/trading"},
    
    # Infrastructure
    "vault": {"port": 8200, "path": "/v1"},
    "temporal": {"port": 7233, "path": "/"},
    "superset": {"port": 8088, "path": "/api/v1"},
    "redis": {"port": 6379, "internal": True}
}
```

## API Layer - Routing Strategy

### Dynamic Request Routing
```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
import httpx

app = FastAPI(title="BizOSaaS Brain Gateway")

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def route_request(
    service: str,
    path: str,
    request: Request,
    tenant_id: UUID = Depends(get_current_tenant)
):
    """
    Dynamic routing to backend services
    
    Example: GET /brain-gateway/ai-agents/campaigns/123
    Routes to: http://bizosaas-ai-agents-staging:8008/api/v1/agents/campaigns/123
    """
    # Get service configuration
    service_config = await route_repository.get_service_config(service)
    
    if not service_config or not service_config.can_route_request():
        raise HTTPException(status_code=503, detail=f"Service {service} unavailable")

    # Build target URL
    target_url = f"{service_config.base_url}/{path}"

    # Forward request
    async with httpx.AsyncClient() as client:
        try:
            # Copy headers (add tenant context)
            headers = dict(request.headers)
            headers["X-Tenant-ID"] = str(tenant_id)

            # Make request
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=await request.body(),
                params=request.query_params
            )

            # Update service health
            await update_service_health(service_config.id, is_healthy=True)

            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )

        except Exception as e:
            # Update service health (circuit breaker)
            await update_service_health(service_config.id, is_healthy=False)
            raise HTTPException(status_code=502, detail=str(e))
```

### Health Check Aggregation
```python
@app.get("/health")
async def health_check():
    """Aggregate health status of all services"""
    service_statuses = {}

    for service_name, config in REGISTERED_SERVICES.items():
        if config.get("internal"):
            continue

        try:
            health_url = f"http://{service_name}:{config['port']}/health"
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.get(health_url)
                service_statuses[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "degraded",
                    "response_time_ms": response.elapsed.total_seconds() * 1000
                }
        except:
            service_statuses[service_name] = {"status": "down"}

    overall_health = "healthy" if all(
        s.get("status") == "healthy" for s in service_statuses.values()
    ) else "degraded"

    return {
        "status": overall_health,
        "services": service_statuses,
        "timestamp": datetime.utcnow().isoformat()
    }
```

## 93 AI Agents Integration

### Agent Pattern Routing
```python
class AIAgentRouter:
    """Route requests to appropriate AI agent patterns"""

    # 4-Agent Pattern (6 complex integrations)
    FOUR_AGENT_APIS = ["facebook", "amazon-sp", "amazon-ads", "stripe", "paypal", "payu"]

    # 3-Agent Pattern (8 medium integrations)
    THREE_AGENT_APIS = ["instagram", "linkedin", "youtube", "google-search", 
                         "google-ads", "google-analytics", "openai", "anthropic"]

    # 2-Agent Pattern (12 standard integrations)
    TWO_AGENT_APIS = ["twitter", "tiktok", "pinterest", "google-business", 
                       "bing", "facebook-ads", "razorpay", "amazon-ses", 
                       "sendgrid", "twilio", "hubspot", "calendly"]

    async def route_to_agent(self, integration: str, action: str, data: dict):
        """Determine agent pattern and route request"""
        if integration in self.FOUR_AGENT_APIS:
            return await self._route_four_agent(integration, action, data)
        elif integration in self.THREE_AGENT_APIS:
            return await self._route_three_agent(integration, action, data)
        elif integration in self.TWO_AGENT_APIS:
            return await self._route_two_agent(integration, action, data)
        else:
            return await self._route_single_agent(integration, action, data)
```

## Configuration

### Environment Variables
```bash
# Brain Gateway
BRAIN_GATEWAY_HOST=0.0.0.0
BRAIN_GATEWAY_PORT=8001
LOG_LEVEL=info

# Database
DATABASE_URL=postgresql://postgres:SharedInfra2024!SuperSecure@bizosaas-postgres-staging:5432/bizosaas_platform

# Redis (caching, circuit breaker state)
REDIS_URL=redis://bizosaas-redis-staging:6379/0

# Vault (API keys for 40+ integrations)
VAULT_ADDR=http://bizosaas-vault-staging:8200
VAULT_TOKEN=${VAULT_TOKEN}

# Services Discovery
SERVICE_REGISTRY_ENABLED=true
AUTO_DISCOVERY=true
HEALTH_CHECK_INTERVAL=30
```

## Multi-Tenancy

### Tenant Context Middleware
```python
from fastapi import Header, HTTPException

async def get_current_tenant(
    authorization: str = Header(None),
    x_tenant_id: str = Header(None)
) -> UUID:
    """Extract tenant ID from JWT or header"""
    if x_tenant_id:
        return UUID(x_tenant_id)
    
    # Extract from JWT
    token = authorization.replace("Bearer ", "")
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return UUID(payload["tenant_id"])

@app.middleware("http")
async def add_tenant_context(request: Request, call_next):
    """Add tenant context to all downstream requests"""
    try:
        tenant_id = await get_current_tenant(
            authorization=request.headers.get("authorization"),
            x_tenant_id=request.headers.get("x-tenant-id")
        )
        
        # Set in database context
        async with get_db_session() as session:
            await session.execute(
                text(f"SET app.current_tenant_id = '{tenant_id}'")
            )
        
        response = await call_next(request)
        return response
    except Exception as e:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid tenant context"}
        )
```

## Rate Limiting & Circuit Breaker

### Rate Limiter
```python
from redis import Redis
from datetime import timedelta

class RateLimiter:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    async def is_allowed(self, tenant_id: UUID, service: str) -> bool:
        """Check if request is within rate limit"""
        key = f"ratelimit:{tenant_id}:{service}"
        
        # Sliding window: 100 requests per minute
        current = await self.redis.incr(key)
        if current == 1:
            await self.redis.expire(key, 60)
        
        return current <= 100
```

### Circuit Breaker
```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = {}

    async def call(self, service_id: UUID, func):
        """Execute with circuit breaker protection"""
        failure_count = self.failures.get(service_id, 0)
        
        if failure_count >= self.failure_threshold:
            raise HTTPException(status_code=503, detail="Circuit breaker open")

        try:
            result = await func()
            self.failures[service_id] = 0  # Reset on success
            return result
        except Exception as e:
            self.failures[service_id] = failure_count + 1
            raise
```

## Monitoring & Observability

### Metrics Collection
```python
from prometheus_client import Counter, Histogram

request_count = Counter('brain_gateway_requests_total', 'Total requests', ['service', 'method', 'status'])
request_duration = Histogram('brain_gateway_request_duration_seconds', 'Request duration', ['service'])

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    service = request.path_params.get("service", "unknown")
    request_count.labels(service=service, method=request.method, status=response.status_code).inc()
    request_duration.labels(service=service).observe(duration)
    
    return response
```

## Testing

### Integration Test
```python
@pytest.mark.asyncio
async def test_route_to_ai_agents():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/ai-agents/campaigns",
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 200
```

## Deployment Checklist
- [x] Brain Gateway container deployed
- [x] PostgreSQL route storage configured
- [x] Redis caching enabled
- [x] Vault integration active
- [x] Health checks passing
- [x] All 13 services registered
- [x] Circuit breaker configured
- [x] Rate limiting active
- [x] Monitoring dashboards created

---
**Status**: ✅ Production-Ready
**Last Updated**: October 15, 2025
**Owner**: Backend Team
