# BizOSaaS Event Bus Service

A comprehensive Domain Event Bus service for the BizOSaaS platform, enabling event-driven architecture and autonomous AI agent coordination across microservices.

## 🚀 Features

### Core Event Bus Capabilities
- **Event Publishing & Subscription**: Publish and subscribe to domain events across services
- **Multi-tenant Isolation**: Secure tenant-based event isolation and routing
- **Event Persistence**: Persistent event storage with PostgreSQL for audit trails and replay
- **Message Broker Support**: Multiple broker support (Redis, RabbitMQ, Kafka)
- **Real-time Processing**: Both synchronous and asynchronous event processing
- **Event Replay**: Replay events for debugging, testing, and recovery scenarios

### AI Agent Coordination
- **Autonomous Agent Tasks**: Coordinate AI agent tasks through events
- **Analysis Workflows**: Manage AI analysis requests and results
- **Task Assignment**: Automatic task assignment to appropriate AI agents
- **Result Aggregation**: Collect and distribute AI analysis results

### Advanced Features
- **Event Sourcing**: Support for event sourcing patterns
- **Event Versioning**: Schema evolution and backward compatibility
- **Dead Letter Queue**: Failed event handling and retry mechanisms
- **Health Monitoring**: Comprehensive health checks and metrics
- **Rate Limiting**: Per-tenant rate limiting and resource controls
- **Data Encryption**: Tenant-specific data encryption for sensitive events

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Agents     │    │   CRM Service   │    │ Campaign Mgmt   │
│   Service       │    │                 │    │   Service       │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │                         │
                    │    Event Bus Service    │
                    │      (Port 8003)        │
                    │                         │
                    └────────────┬────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
    ┌─────▼─────┐      ┌─────────▼─────────┐   ┌───────▼────────┐
    │   Redis   │      │   PostgreSQL      │   │  Message       │
    │ (Pub/Sub) │      │ (Event Store)     │   │  Broker        │
    └───────────┘      └───────────────────┘   └────────────────┘
```

## 🎯 Event Types

### User & Tenant Events
- `user.created` - User account created
- `user.updated` - User account updated  
- `user.deactivated` - User account deactivated
- `tenant.created` - New tenant organization created
- `tenant.subscription_changed` - Tenant subscription plan changed

### Lead & Campaign Events
- `lead.created` - New lead captured
- `lead.qualified` - Lead qualified by AI or human
- `lead.converted` - Lead converted to customer
- `campaign.created` - Marketing campaign created
- `campaign.launched` - Campaign launched and active
- `campaign.optimized` - Campaign optimized by AI

### AI Agent Events
- `ai.analysis_requested` - AI analysis requested
- `ai.analysis_started` - AI analysis started processing
- `ai.analysis_completed` - AI analysis completed
- `ai.analysis_failed` - AI analysis failed
- `agent.task_assigned` - Task assigned to AI agent
- `agent.task_completed` - Task completed by AI agent
- `agent.task_failed` - Task failed by AI agent

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Redis (for pub/sub and caching)
- PostgreSQL (for event persistence)
- Docker (optional, for containerized deployment)

### Installation

1. **Clone and Navigate to Event Bus Service**
```bash
cd /home/alagiri/projects/bizoholic/bizosaas/services/event-bus
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Set Environment Variables**
```bash
export EVENTBUS_REDIS_HOST=localhost
export EVENTBUS_REDIS_PORT=6379
export EVENTBUS_POSTGRES_HOST=localhost
export EVENTBUS_POSTGRES_PORT=5432
export EVENTBUS_POSTGRES_USER=admin
export EVENTBUS_POSTGRES_PASSWORD=securepassword
export EVENTBUS_POSTGRES_DB=bizosaas
```

### Running the Service

#### Option 1: Standalone Version (Recommended for Testing)
```bash
python standalone_main.py
```

#### Option 2: Full Version (Production)
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```

#### Option 3: Docker
```bash
docker build -t bizosaas-event-bus .
docker run -p 8003:8003 -e EVENTBUS_REDIS_HOST=host.docker.internal bizosaas-event-bus
```

### Verify Installation
```bash
curl http://localhost:8003/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-10T12:00:00Z",
  "version": "1.0.0",
  "components": {
    "redis": {"status": "healthy"},
    "event_store": {"status": "healthy"}
  }
}
```

## 📖 API Documentation

Once the service is running, visit:
- **Swagger UI**: http://localhost:8003/docs
- **ReDoc**: http://localhost:8003/redoc

### Key Endpoints

#### Event Publishing
```bash
POST /events/publish
```

Example:
```bash
curl -X POST "http://localhost:8003/events/publish" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "lead.created",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
    "source_service": "crm-service",
    "data": {
      "lead_id": "123e4567-e89b-12d3-a456-426614174000",
      "email": "john.doe@example.com",
      "company": "Acme Corp"
    },
    "priority": "high"
  }'
```

#### Event Subscription
```bash
POST /events/subscribe
```

Example:
```bash
curl -X POST "http://localhost:8003/events/subscribe" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "lead.created",
    "service_name": "ai-agents",
    "webhook_url": "http://ai-agents:8001/events/webhook"
  }'
```

#### Event History
```bash
POST /events/history
```

Example:
```bash
curl -X POST "http://localhost:8003/events/history" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
    "event_types": ["lead.created", "lead.qualified"],
    "limit": 50
  }'
```

## 🤖 AI Agent Integration Examples

### AI Agents Service Integration

```python
from event_bus.client_sdk import EventBusClient, EventBusClientConfig

# Initialize client
config = EventBusClientConfig(
    base_url="http://localhost:8003",
    service_name="ai-agents"
)
client = EventBusClient(config)
await client.connect()

# Subscribe to analysis requests
await client.subscribe_to_events(
    event_type="ai.analysis_requested",
    handler=handle_analysis_request
)

# Publish analysis results
await client.publish_event(
    event_type="ai.analysis_completed",
    tenant_id=tenant_id,
    data={
        "analysis_type": "lead_scoring",
        "results": {"score": 87, "confidence": 92}
    }
)
```

### CRM Service Integration

```python
async def create_lead(tenant_id, contact_info):
    """Create lead and trigger AI analysis"""
    lead_id = uuid4()
    
    # Store lead in database
    # ... CRM logic ...
    
    # Publish lead created event
    await event_client.publish_event(
        event_type="lead.created",
        tenant_id=tenant_id,
        data={
            "lead_id": str(lead_id),
            "contact_info": contact_info,
            "source": "web_form"
        },
        target_services=["ai-agents", "marketing-automation"]
    )
```

## 🔄 Event-Driven Workflows

### Lead Processing Workflow
```
1. Lead Created (CRM) 
   → 2. AI Analysis Requested (Auto)
   → 3. Lead Scoring (AI Agents)
   → 4. Analysis Completed (AI Agents)
   → 5. Lead Qualified/Nurture (CRM)
   → 6. Campaign Optimization (Campaign Mgmt)
```

### Campaign Optimization Workflow
```
1. Campaign Launched (Campaign Mgmt)
   → 2. Monitoring Started (AI Agents) 
   → 3. Performance Analysis (AI Agents)
   → 4. Optimization Suggestions (AI Agents)
   → 5. Auto-Apply Changes (Campaign Mgmt)
   → 6. Results Tracking (Analytics)
```

## 🧪 Testing & Demos

### Demo Endpoints (Available in Standalone Mode)

1. **Create Demo Lead**
```bash
curl -X POST "http://localhost:8003/demo/create-lead" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
    "contact_info": {
      "email": "demo@example.com", 
      "company": "Demo Corp"
    }
  }'
```

2. **Request AI Analysis**
```bash
curl -X POST "http://localhost:8003/demo/ai-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
    "analysis_type": "lead_scoring"
  }'
```

### Integration Testing

Run the integration demo:
```python
from integration_examples import run_integration_demo
await run_integration_demo()
```

This will simulate a complete workflow:
1. Create new lead
2. Trigger AI analysis 
3. Launch marketing campaign
4. Apply AI optimizations
5. Track results

## 📊 Monitoring & Metrics

### Metrics Endpoint
```bash
GET /metrics
```

Key metrics tracked:
- `events_published` - Total events published
- `events_processed` - Total events processed  
- `events_failed` - Total failed events
- `active_subscriptions` - Current active subscriptions
- `processing_time_ms` - Average processing time

### Health Monitoring
```bash
GET /health
```

Monitors:
- Redis connectivity
- PostgreSQL connectivity
- Message broker health
- Event processing status
- Subscription health

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `EVENTBUS_SERVICE_PORT` | `8003` | Service port |
| `EVENTBUS_REDIS_HOST` | `localhost` | Redis host |
| `EVENTBUS_REDIS_PORT` | `6379` | Redis port |
| `EVENTBUS_POSTGRES_HOST` | `localhost` | PostgreSQL host |
| `EVENTBUS_POSTGRES_PORT` | `5432` | PostgreSQL port |
| `EVENTBUS_POSTGRES_USER` | `admin` | PostgreSQL user |
| `EVENTBUS_POSTGRES_PASSWORD` | `securepassword` | PostgreSQL password |
| `EVENTBUS_POSTGRES_DB` | `bizosaas` | PostgreSQL database |
| `EVENTBUS_BROKER_TYPE` | `redis` | Message broker (redis/rabbitmq/kafka) |
| `EVENTBUS_MAX_RETRY_ATTEMPTS` | `3` | Maximum retry attempts |
| `EVENTBUS_EVENT_TTL_DAYS` | `30` | Event retention period |
| `EVENTBUS_ENABLE_TENANT_ISOLATION` | `true` | Enable tenant isolation |

### Message Broker Configuration

#### Redis (Default)
```bash
EVENTBUS_BROKER_TYPE=redis
EVENTBUS_REDIS_HOST=localhost
EVENTBUS_REDIS_PORT=6379
```

#### RabbitMQ
```bash
EVENTBUS_BROKER_TYPE=rabbitmq
EVENTBUS_RABBITMQ_URL=amqp://user:pass@localhost:5672/
```

#### Kafka
```bash
EVENTBUS_BROKER_TYPE=kafka
EVENTBUS_KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

## 🚀 Production Deployment

### Docker Compose Integration

Add to your `docker-compose.yml`:

```yaml
services:
  event-bus:
    build: ./services/event-bus
    ports:
      - "8003:8003"
    environment:
      - EVENTBUS_REDIS_HOST=redis
      - EVENTBUS_POSTGRES_HOST=postgres
      - EVENTBUS_POSTGRES_PASSWORD=securepassword
    depends_on:
      - redis
      - postgres
    networks:
      - bizosaas-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8003/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: event-bus
spec:
  replicas: 3
  selector:
    matchLabels:
      app: event-bus
  template:
    metadata:
      labels:
        app: event-bus
    spec:
      containers:
      - name: event-bus
        image: bizosaas/event-bus:latest
        ports:
        - containerPort: 8003
        env:
        - name: EVENTBUS_REDIS_HOST
          value: "redis-service"
        - name: EVENTBUS_POSTGRES_HOST
          value: "postgres-service"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8003
          initialDelaySeconds: 30
          periodSeconds: 10
```

## 🔐 Security Considerations

### Multi-tenancy
- Events are automatically isolated by tenant ID
- Tenant context validation on all operations
- Row-level security for database operations

### Data Protection
- Optional encryption for sensitive event data
- Configurable data retention policies
- Audit logging for compliance

### Network Security
- CORS configuration for browser clients
- Optional API key authentication
- Rate limiting per tenant

## 🛠️ Development

### Adding New Event Types

1. Add event class to `domain_events.py`:
```python
class CustomEventCreated(BaseEvent):
    event_type: str = "custom.event_created"
    category: EventCategory = EventCategory.CUSTOM
```

2. Register in `EVENT_TYPES` dictionary
3. Add to integration examples
4. Update documentation

### Adding New Message Brokers

1. Implement `MessageBrokerInterface` in `message_brokers.py`
2. Add to broker factory function
3. Add configuration options
4. Test integration

### Testing

Run unit tests:
```bash
pytest tests/
```

Run integration tests:
```bash
python -m pytest tests/integration/
```

## 📝 Troubleshooting

### Common Issues

1. **Redis Connection Failed**
   - Verify Redis is running: `redis-cli ping`
   - Check host/port configuration
   - Ensure firewall allows connections

2. **PostgreSQL Connection Failed**  
   - Check database exists: `psql -h localhost -U admin -d bizosaas`
   - Verify credentials and permissions
   - Check connection limits

3. **Event Publishing Fails**
   - Verify tenant ID format (valid UUID)
   - Check event data structure
   - Review error logs for details

4. **No Events Received**
   - Verify subscription is active: `GET /subscriptions`
   - Check event type matching (case-sensitive)
   - Review tenant isolation settings

### Logs and Debugging

Enable debug logging:
```bash
export EVENTBUS_DEBUG=true
```

View structured logs:
```bash
docker logs -f event-bus-container | jq
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit pull request

## 📄 License

This project is part of the BizOSaaS platform and is proprietary software.

## 🆘 Support

For support and questions:
- Check the troubleshooting section above
- Review API documentation at `/docs`
- Check service health at `/health`
- Review metrics at `/metrics`

---

## 🎯 Next Steps

1. **Deploy Event Bus Service**: Use Docker or direct Python execution
2. **Integrate with AI Agents**: Use the client SDK to connect AI agents
3. **Connect CRM Service**: Publish lead events from CRM
4. **Set up Monitoring**: Configure metrics collection and alerting
5. **Test Workflows**: Run integration demos to verify functionality

The Event Bus is the backbone of the BizOSaaS event-driven architecture, enabling autonomous AI agent coordination and seamless cross-service communication.