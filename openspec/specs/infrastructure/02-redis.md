# Redis Cache Service - Infrastructure

## Service Identity
- **Name**: Redis Cache
- **Type**: Infrastructure - In-Memory Data Store
- **Container**: `bizosaas-redis-staging`
- **Image**: `redis:7-alpine`
- **Port**: `6380:6379` (external:internal)
- **Network**: `dokploy-network`
- **Status**: ✅ Running (2+ days uptime)

## Purpose
High-performance in-memory data store for caching, session management, message queuing, and real-time event streaming across the BizOSaaS platform.

## Architecture

### Redis Use Cases
```
Redis Service
├── Cache Layer
│   ├── API Response Caching
│   ├── Database Query Caching
│   ├── Vector Operation Caching
│   └── Static Content Caching
├── Session Management
│   ├── User Sessions (JWT tokens)
│   ├── OAuth State
│   └── CSRF Tokens
├── Message Queue
│   ├── Background Jobs (Celery)
│   ├── Task Queues
│   └── Job Results
└── Event Streaming
    ├── Redis Streams (Event-Driven)
    ├── Pub/Sub Messaging
    └── Real-time Notifications
```

### Data Structures Used
- **Strings**: Simple key-value caching
- **Hashes**: User sessions, object caching
- **Lists**: Job queues, activity feeds
- **Sets**: Unique items, tags, relationships
- **Sorted Sets**: Leaderboards, time-series data
- **Streams**: Event sourcing, audit logs
- **HyperLogLog**: Unique visitor counts
- **Bitmaps**: User activity tracking

## Dependencies

### Required By (Consumers)
- Brain API Gateway (caching, sessions)
- AI Agents Service (vector caching, job queue)
- Auth Service (sessions, tokens)
- All Backend Services (caching)
- All Frontend Services (session store)

### External Dependencies
- None (base infrastructure)

## Configuration

### Environment Variables
```bash
# Redis Connection
REDIS_HOST=bizosaas-redis-staging
REDIS_PORT=6379
REDIS_PASSWORD=  # No password in development (set in production)
REDIS_DB=0

# Cache Configuration
REDIS_CACHE_TTL=3600  # 1 hour default
REDIS_SESSION_TTL=86400  # 24 hours
REDIS_MAX_MEMORY=2gb
REDIS_EVICTION_POLICY=allkeys-lru

# Performance
REDIS_MAX_CONNECTIONS=1000
REDIS_TIMEOUT=5
```

### Docker Compose Configuration
```yaml
services:
  redis:
    image: redis:7-alpine
    container_name: bizosaas-redis-staging
    command: redis-server --maxmemory 2gb --maxmemory-policy allkeys-lru
    ports:
      - "6380:6379"
    volumes:
      - redis_data:/data
    networks:
      - dokploy-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
```

## Cache Strategies

### API Response Caching
```python
import redis
from functools import wraps
import json

redis_client = redis.Redis(
    host="bizosaas-redis-staging",
    port=6379,
    db=0,
    decode_responses=True
)

def cache_api_response(ttl=3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"api:{func.__name__}:{hash(str(args) + str(kwargs))}"

            # Check cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            # Execute function
            result = await func(*args, **kwargs)

            # Store in cache
            redis_client.setex(
                cache_key,
                ttl,
                json.dumps(result)
            )
            return result
        return wrapper
    return decorator

# Usage
@cache_api_response(ttl=1800)
async def get_campaign_analytics(campaign_id: str):
    # Expensive database query
    return analytics_data
```

### Database Query Caching
```python
def cache_database_query(model_name: str, ttl=3600):
    def get_cached_or_query(query_key: str, query_func):
        cache_key = f"db:{model_name}:{query_key}"

        # Try cache first
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        # Query database
        result = query_func()

        # Cache result
        redis_client.setex(cache_key, ttl, json.dumps(result))
        return result

    return get_cached_or_query
```

### Vector Operation Caching
```python
import numpy as np

def cache_vector_embedding(text: str, embedding: np.ndarray, ttl=86400):
    """Cache text embeddings to avoid recomputation"""
    cache_key = f"vector:embedding:{hash(text)}"
    redis_client.setex(
        cache_key,
        ttl,
        embedding.tobytes()
    )

def get_cached_embedding(text: str) -> np.ndarray:
    cache_key = f"vector:embedding:{hash(text)}"
    cached = redis_client.get(cache_key)
    if cached:
        return np.frombuffer(cached, dtype=np.float32)
    return None
```

## Session Management

### User Session Storage
```python
from datetime import timedelta
import uuid

class SessionStore:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.prefix = "session:"

    def create_session(self, user_id: str, data: dict) -> str:
        """Create new session"""
        session_id = str(uuid.uuid4())
        session_key = f"{self.prefix}{session_id}"

        session_data = {
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            **data
        }

        self.redis.setex(
            session_key,
            timedelta(days=1),
            json.dumps(session_data)
        )
        return session_id

    def get_session(self, session_id: str) -> dict:
        """Retrieve session data"""
        session_key = f"{self.prefix}{session_id}"
        data = self.redis.get(session_key)
        return json.loads(data) if data else None

    def delete_session(self, session_id: str):
        """Delete session"""
        session_key = f"{self.prefix}{session_id}"
        self.redis.delete(session_key)

    def refresh_session(self, session_id: str):
        """Extend session TTL"""
        session_key = f"{self.prefix}{session_id}"
        self.redis.expire(session_key, timedelta(days=1))
```

### JWT Token Blacklist
```python
def blacklist_token(jti: str, exp: int):
    """Add revoked JWT to blacklist"""
    ttl = exp - int(datetime.utcnow().timestamp())
    if ttl > 0:
        redis_client.setex(f"blacklist:{jti}", ttl, "1")

def is_token_blacklisted(jti: str) -> bool:
    """Check if JWT is blacklisted"""
    return redis_client.exists(f"blacklist:{jti}") > 0
```

## Message Queue (Celery Integration)

### Celery Configuration
```python
from celery import Celery

celery_app = Celery(
    'bizosaas',
    broker='redis://bizosaas-redis-staging:6379/1',
    backend='redis://bizosaas-redis-staging:6379/2'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    task_soft_time_limit=3000,  # 50 minutes
)
```

### Background Tasks
```python
@celery_app.task(name='process_campaign')
def process_campaign_task(campaign_id: str):
    """Process marketing campaign asynchronously"""
    # Long-running campaign processing
    return {"status": "completed", "campaign_id": campaign_id}

# Trigger task
result = process_campaign_task.delay("campaign-123")

# Check result
if result.ready():
    print(result.get())
```

## Event Streaming (Redis Streams)

### Event Producer
```python
def publish_event(stream_name: str, event_type: str, data: dict):
    """Publish event to Redis Stream"""
    event = {
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "data": json.dumps(data)
    }

    redis_client.xadd(
        f"stream:{stream_name}",
        event,
        maxlen=10000  # Keep last 10k events
    )
```

### Event Consumer
```python
def consume_events(stream_name: str, consumer_group: str, consumer_name: str):
    """Consume events from Redis Stream"""
    stream_key = f"stream:{stream_name}"

    # Create consumer group if not exists
    try:
        redis_client.xgroup_create(stream_key, consumer_group, id='0', mkstream=True)
    except redis.ResponseError:
        pass  # Group already exists

    # Read events
    while True:
        events = redis_client.xreadgroup(
            consumer_group,
            consumer_name,
            {stream_key: '>'},
            count=10,
            block=5000
        )

        for stream, messages in events:
            for message_id, data in messages:
                try:
                    process_event(data)
                    # Acknowledge message
                    redis_client.xack(stream_key, consumer_group, message_id)
                except Exception as e:
                    # Handle error (dead letter queue)
                    pass
```

## Pub/Sub Messaging

### Publisher
```python
def publish_notification(channel: str, message: dict):
    """Publish real-time notification"""
    redis_client.publish(
        f"notifications:{channel}",
        json.dumps(message)
    )
```

### Subscriber
```python
def subscribe_notifications(channels: list):
    """Subscribe to notification channels"""
    pubsub = redis_client.pubsub()
    pubsub.subscribe(*[f"notifications:{ch}" for ch in channels])

    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            handle_notification(data)
```

## Performance Optimization

### Connection Pooling
```python
from redis import ConnectionPool

# Create connection pool
pool = ConnectionPool(
    host='bizosaas-redis-staging',
    port=6379,
    db=0,
    max_connections=50,
    socket_connect_timeout=5,
    socket_timeout=5
)

redis_client = redis.Redis(connection_pool=pool)
```

### Pipeline Operations
```python
def batch_cache_set(items: dict):
    """Batch set multiple cache items"""
    pipe = redis_client.pipeline()
    for key, value in items.items():
        pipe.setex(key, 3600, json.dumps(value))
    pipe.execute()
```

### Lua Scripts (Atomic Operations)
```python
# Rate limiting with Lua script
rate_limit_script = """
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local ttl = tonumber(ARGV[2])

local current = redis.call('GET', key)
if current then
    if tonumber(current) >= limit then
        return 0
    else
        redis.call('INCR', key)
        return 1
    end
else
    redis.call('SETEX', key, ttl, 1)
    return 1
end
"""

def check_rate_limit(user_id: str, limit=100, window=60):
    key = f"ratelimit:{user_id}"
    result = redis_client.eval(rate_limit_script, 1, key, limit, window)
    return bool(result)
```

## Health Checks

### Container Health Check
```bash
# Check Redis is responding
docker exec bizosaas-redis-staging redis-cli ping

# Expected output: PONG
```

### Application Health Check
```python
def check_redis_health():
    try:
        # Test connection
        redis_client.ping()

        # Test write
        redis_client.setex("health_check", 10, "ok")

        # Test read
        value = redis_client.get("health_check")

        return value == b"ok"
    except Exception as e:
        return False
```

### Performance Monitoring
```bash
# Check Redis stats
redis-cli INFO stats

# Monitor commands in real-time
redis-cli MONITOR

# Check memory usage
redis-cli INFO memory
```

## Integration Points

### Brain API Gateway Integration
```python
from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = redis.from_url("redis://bizosaas-redis-staging:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.get("/campaigns/{campaign_id}")
@cache(expire=3600)
async def get_campaign(campaign_id: str):
    # Response automatically cached
    return campaign_data
```

### AI Agents Integration
```python
# Cache LLM responses
def cache_llm_response(prompt: str, response: str, ttl=86400):
    cache_key = f"llm:response:{hash(prompt)}"
    redis_client.setex(cache_key, ttl, response)

def get_cached_llm_response(prompt: str):
    cache_key = f"llm:response:{hash(prompt)}"
    return redis_client.get(cache_key)
```

## Monitoring

### Key Metrics
```bash
# Connected clients
redis-cli INFO clients | grep connected_clients

# Memory usage
redis-cli INFO memory | grep used_memory_human

# Hit rate
redis-cli INFO stats | grep keyspace_hits

# Evicted keys
redis-cli INFO stats | grep evicted_keys
```

### Alerting Thresholds
- Memory usage > 80% of max_memory
- Connected clients > 900 (90% of max)
- Cache hit rate < 80%
- Eviction rate > 1000 keys/sec

## Common Issues

### Issue 1: Out of Memory
**Symptom**: Redis stops accepting writes
**Diagnosis**: `redis-cli INFO memory`
**Solution**:
- Increase maxmemory limit
- Verify eviction policy is set
- Review cache TTLs
- Remove unused keys

### Issue 2: Connection Timeout
**Symptom**: Clients timeout connecting to Redis
**Diagnosis**: `redis-cli INFO clients`
**Solution**:
- Increase timeout settings
- Implement connection pooling
- Check network latency
- Review firewall rules

### Issue 3: Slow Commands
**Symptom**: Commands taking > 1 second
**Diagnosis**: `redis-cli --latency`
**Solution**:
- Avoid KEYS command (use SCAN instead)
- Use pipelining for bulk operations
- Optimize data structures
- Enable persistence options carefully

### Issue 4: High Eviction Rate
**Symptom**: Keys being evicted frequently
**Diagnosis**: `redis-cli INFO stats | grep evicted_keys`
**Solution**:
- Increase maxmemory
- Review TTL settings
- Use more efficient data structures
- Implement cache warming

## Security Considerations

### Access Control
```bash
# Enable password protection (production)
redis-cli CONFIG SET requirepass "secure_password_here"

# Restrict commands
redis-cli CONFIG SET rename-command FLUSHDB ""
redis-cli CONFIG SET rename-command FLUSHALL ""
```

### Encryption
- **In Transit**: Use Redis TLS/SSL in production
- **At Rest**: Enable RDB/AOF encryption
- **Credentials**: Store password in HashiCorp Vault

### Network Security
```bash
# Bind to specific interfaces
bind 127.0.0.1 ::1  # Localhost only

# Disable protected mode for Docker
protected-mode no  # Only in Docker networks
```

## Persistence Options

### RDB Snapshots
```bash
# redis.conf
save 900 1      # Save after 900 sec if 1 key changed
save 300 10     # Save after 300 sec if 10 keys changed
save 60 10000   # Save after 60 sec if 10000 keys changed
```

### AOF (Append-Only File)
```bash
# redis.conf
appendonly yes
appendfsync everysec  # Balance between performance and safety
```

## Testing

### Unit Tests
```python
import pytest
from redis import Redis

@pytest.fixture
def redis_client():
    client = Redis(host='localhost', port=6379, db=15)  # Test DB
    yield client
    client.flushdb()  # Clean up after tests

def test_cache_set_get(redis_client):
    redis_client.setex("test_key", 60, "test_value")
    assert redis_client.get("test_key") == b"test_value"

def test_session_management(redis_client):
    store = SessionStore(redis_client)
    session_id = store.create_session("user-123", {"role": "admin"})
    session = store.get_session(session_id)
    assert session["user_id"] == "user-123"
```

## Deployment Checklist

- [ ] Redis 7 container deployed
- [ ] Memory limit configured (maxmemory)
- [ ] Eviction policy set (allkeys-lru)
- [ ] Health checks passing
- [ ] Connection pooling configured
- [ ] Monitoring dashboards created
- [ ] Backup strategy defined (RDB/AOF)
- [ ] All services connected successfully
- [ ] Cache hit rate > 80%

## References
- [Redis 7 Documentation](https://redis.io/docs/)
- [Redis Best Practices](https://redis.io/topics/optimization)
- [Celery with Redis](https://docs.celeryproject.org/en/stable/getting-started/brokers/redis.html)
- BizOSaaS PRD: `/home/alagiri/projects/bizoholic/comprehensive_prd_06092025.md`

---
**Status**: ✅ Production-Ready
**Last Updated**: October 15, 2025
**Owner**: Infrastructure Team
