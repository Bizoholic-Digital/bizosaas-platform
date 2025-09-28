# BizOSaaS Cross-Platform Data Synchronization Service

A comprehensive real-time data synchronization service that ensures seamless data flow between Bizoholic (AI Marketing), CoreLDove (E-commerce), and BizOSaaS (Unified Backend) platforms.

## 🚀 Features

### Core Synchronization
- **Real-time Data Flow**: Event-driven synchronization with WebSocket support
- **Multi-Platform Support**: Seamless integration across Bizoholic, CoreLDove, and BizOSaaS
- **Conflict Resolution**: Intelligent handling of data conflicts with multiple resolution strategies
- **Event Bus**: Centralized message routing and transformation
- **Rate Limiting**: Intelligent API rate limiting to prevent service overload

### Data Types Synchronized
- **Customer Data**: User profiles, preferences, authentication tokens
- **Business Data**: Leads, campaigns, orders, products, analytics
- **Operational Data**: System health, performance metrics, configuration changes

### Performance & Reliability
- **Scalable Architecture**: Horizontal scaling with load balancing
- **Fault Tolerance**: Retry logic, dead letter queues, circuit breakers
- **Monitoring**: Real-time metrics, alerting, and health dashboards
- **High Availability**: 99.9% uptime with automated failover

## 📋 Requirements

- Python 3.11+
- PostgreSQL 12+ with pgvector extension
- Redis 6+
- FastAPI
- Docker & Docker Compose

## 🛠 Installation

### Using Docker (Recommended)

1. **Build the service**:
   ```bash
   docker build -t bizosaas/data-sync:latest .
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the service**:
   ```bash
   docker-compose up -d bizosaas-data-sync
   ```

### Manual Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the service**:
   ```bash
   python main.py
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://admin:securepassword@localhost:5432/bizosaas` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/6` |
| `JWT_SECRET` | JWT secret key | `dev-secret-key` |
| `SYNC_BATCH_SIZE` | Batch size for bulk operations | `100` |
| `SYNC_INTERVAL_SECONDS` | Sync processing interval | `5` |
| `MAX_CONCURRENT_SYNCS` | Max concurrent sync operations | `10` |
| `EVENT_RETENTION_DAYS` | Event retention period | `30` |

### Platform URLs

Configure the service URLs for each platform:

```env
BIZOSAAS_BRAIN_URL=http://bizosaas-brain:8001
BIZOHOLIC_FRONTEND_URL=http://bizosaas-bizoholic-frontend:3008
CORELDOVE_FRONTEND_URL=http://bizosaas-coreldove-frontend:3012
```

## 📊 API Documentation

### Core Endpoints

#### Health Check
```bash
GET /health
```

#### Create Sync Event
```bash
POST /sync/events
Content-Type: application/json

{
  "event_type": "user_created",
  "source_platform": "bizoholic",
  "target_platforms": ["coreldove", "bizosaas"],
  "data": {
    "user_id": "user123",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "tenant_id": "tenant123"
}
```

#### Get Sync Status
```bash
GET /sync/events/{event_id}
```

#### WebSocket Real-time Updates
```javascript
const ws = new WebSocket('ws://localhost:8025/ws/sync');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Sync update:', data);
};
```

### Monitoring Endpoints

#### Get Metrics
```bash
GET /sync/metrics?hours=24&tenant_id=tenant123
```

#### Get Dashboard Data
```bash
GET /sync/status
```

## 🔄 Synchronization Flow

### 1. Event Creation
```python
# Create a sync event
event = SyncEvent(
    event_type=SyncEventType.USER_CREATED,
    source_platform=PlatformType.BIZOHOLIC,
    target_platforms=[PlatformType.CORELDOVE, PlatformType.BIZOSAAS],
    data=user_data,
    tenant_id="tenant123"
)
```

### 2. Event Processing
- Event is queued in Redis based on priority
- Background worker processes events
- Data is transformed for each target platform
- API calls are made to target platforms
- Results are stored and monitored

### 3. Conflict Resolution
- Conflicts are detected during synchronization
- Resolution strategy is determined based on rules
- Conflicts are resolved automatically or flagged for manual review

## 🧩 Architecture Components

### Data Sync Engine (`main.py`)
- Core synchronization logic
- Event publishing and processing
- Database and Redis integration
- WebSocket real-time updates

### Conflict Resolution (`conflict_resolution.py`)
- Conflict detection algorithms
- Multiple resolution strategies
- Business rule validation
- Audit trail for all resolutions

### Event Bus (`event_bus.py`)
- Message routing between platforms
- Data transformation
- Priority-based queuing
- Platform-specific formatting

### Monitoring (`monitoring.py`)
- Real-time metrics collection
- Alerting and notifications
- Performance monitoring
- Health checks

### API Integration (`api_integration.py`)
- Cross-platform API clients
- Rate limiting
- Request/response transformation
- Bulk operations support

## 📈 Monitoring & Alerting

### Metrics Collected
- Sync success/failure rates
- Processing times and latencies
- Queue depths and throughput
- Platform health scores
- Error rates and types

### Alert Conditions
- Sync failure rate > 5%
- Processing latency > 5 seconds
- Queue depth > 1000 events
- Platform health score < 95%
- Error rate > 10%

### Dashboard Access
Access the monitoring dashboard at:
```
http://localhost:8025/docs
```

## 🔧 Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Quality
```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

### Database Migrations
The service automatically creates required tables on startup:
- `sync_events` - Event tracking
- `sync_results` - Sync results
- `cross_platform_users` - User data
- `sync_conflicts` - Conflict tracking
- `sync_metrics` - Performance metrics

## 🚀 Deployment

### Production Deployment

1. **Configure environment for production**:
   ```env
   ENVIRONMENT=production
   DATABASE_URL=postgresql://user:pass@prod-db:5432/bizosaas
   REDIS_URL=redis://prod-redis:6379/6
   ```

2. **Deploy with Docker Compose**:
   ```bash
   docker-compose -f docker-compose.production.yml up -d
   ```

3. **Verify deployment**:
   ```bash
   curl http://localhost:8025/health
   ```

### Scaling

The service supports horizontal scaling:

```yaml
services:
  bizosaas-data-sync:
    image: bizosaas/data-sync:latest
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
```

## 🔒 Security

### Authentication
- JWT-based authentication
- Service-to-service authentication
- API key management

### Data Protection
- Encryption at rest and in transit
- Data anonymization options
- GDPR compliance features

### Access Control
- Role-based access control
- Tenant isolation
- Audit logging

## 🐛 Troubleshooting

### Common Issues

#### High Queue Depth
```bash
# Check queue status
redis-cli llen events:critical
redis-cli llen events:normal

# Scale up workers or optimize processing
```

#### Sync Failures
```bash
# Check logs
docker logs bizosaas-data-sync-8025

# Check failed events
curl http://localhost:8025/sync/events?status=failed
```

#### Performance Issues
```bash
# Check metrics
curl http://localhost:8025/sync/metrics

# Monitor database connections
# Optimize batch sizes and intervals
```

### Debug Mode
Enable debug logging:
```env
LOG_LEVEL=DEBUG
```

## 📞 Support

For issues and questions:

1. Check the [troubleshooting guide](#🐛-troubleshooting)
2. Review the logs and metrics
3. Contact the development team

## 📄 License

This service is part of the BizOSaaS platform and is proprietary software.