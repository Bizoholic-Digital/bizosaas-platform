# BizOSaaS Platform Analytics Integration Guide

## Overview

This guide provides comprehensive instructions for integrating the unified analytics system across all BizOSaaS platforms. The analytics system provides cross-platform insights, AI-powered recommendations, and predictive analytics while maintaining complete tenant data isolation.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    BizOSaaS Analytics Platform                   │
├─────────────────────────────────────────────────────────────────┤
│  Frontend Dashboards (React/Next.js)                           │
│  ├── Unified Analytics Dashboard                               │
│  ├── Platform-Specific Views                                   │
│  └── Real-time Monitoring                                      │
├─────────────────────────────────────────────────────────────────┤
│  API Layer (FastAPI)                                           │
│  ├── Analytics Routes (/api/analytics/*)                       │
│  ├── Data Collection Endpoints                                 │
│  ├── AI Insights API                                           │
│  └── Export & Reporting                                        │
├─────────────────────────────────────────────────────────────────┤
│  Analytics Service Layer                                        │
│  ├── Unified Analytics Service                                 │
│  ├── Platform Data Collectors                                  │
│  ├── AI Insights Generator                                     │
│  └── Predictive Analytics Engine                               │
├─────────────────────────────────────────────────────────────────┤
│  Data Storage Layer                                             │
│  ├── PostgreSQL (Analytics Schema)                             │
│  ├── Time-series Data (Analytics Data Points)                  │
│  ├── Aggregated Metrics (Daily/Weekly/Monthly)                 │
│  └── AI Insights & Predictions Storage                         │
└─────────────────────────────────────────────────────────────────┘
```

## Integration Steps

### 1. Database Setup

First, apply the analytics schema to your PostgreSQL database:

```bash
# Connect to your PostgreSQL database
psql -h localhost -U bizosaas_user -d bizosaas_platform

# Apply the analytics schema
\i /home/alagiri/projects/bizoholic/bizosaas-platform/analytics/database/analytics_schema.sql
```

**Verification:**
```sql
-- Verify schema creation
\dt analytics.*

-- Check RLS policies
SELECT schemaname, tablename, policyname
FROM pg_policies
WHERE schemaname = 'analytics';

-- Test tenant isolation
SET app.current_tenant_id = 'test-tenant-123';
SELECT * FROM analytics.analytics_data_points LIMIT 5;
```

### 2. Backend Integration

#### A. Install Dependencies

Add to your `requirements.txt`:
```
pandas>=1.5.0
numpy>=1.24.0
scikit-learn>=1.3.0
asyncpg>=0.28.0
sqlalchemy[asyncio]>=2.0.0
```

#### B. Initialize Analytics Service

Add to your FastAPI application startup:

```python
from analytics.api.analytics_routes import router as analytics_router, initialize_analytics_service

# Add to your FastAPI app
app.include_router(analytics_router)

# Add startup event
@app.on_event("startup")
async def startup_event():
    await initialize_analytics_service(app)
    logger.info("Analytics service initialized")
```

#### C. Configure Tenant Context Middleware

Ensure your application has tenant context middleware:

```python
from shared.enhanced_tenant_context import EnhancedTenantContext

@app.middleware("http")
async def tenant_context_middleware(request: Request, call_next):
    # Extract tenant information from JWT token or headers
    tenant_id = extract_tenant_from_request(request)

    # Set tenant context for RLS
    request.state.tenant_context = await get_tenant_context(tenant_id)

    response = await call_next(request)
    return response
```

### 3. Platform Data Collection

#### A. Bizoholic Marketing Data

Add analytics tracking to your marketing campaigns:

```python
from analytics.services.unified_analytics_service import AnalyticsDataPoint, MetricType

async def track_campaign_metrics(tenant_id: str, campaign_data: dict):
    """Track marketing campaign metrics"""

    # Revenue tracking
    if campaign_data.get('revenue'):
        await record_analytics_point(
            tenant_id=tenant_id,
            platform=PlatformType.BIZOHOLIC,
            metric_type=MetricType.REVENUE,
            metric_name="campaign_revenue",
            value=campaign_data['revenue'],
            dimensions={
                "campaign_id": campaign_data['id'],
                "campaign_type": campaign_data['type']
            }
        )

    # Conversion tracking
    if campaign_data.get('conversion_rate'):
        await record_analytics_point(
            tenant_id=tenant_id,
            platform=PlatformType.BIZOHOLIC,
            metric_type=MetricType.CONVERSIONS,
            metric_name="campaign_conversion",
            value=campaign_data['conversion_rate'],
            dimensions={
                "leads_generated": campaign_data.get('leads', 0),
                "clicks": campaign_data.get('clicks', 0)
            }
        )
```

#### B. CoreLDove Ecommerce Data

Track ecommerce metrics:

```python
async def track_ecommerce_metrics(tenant_id: str, order_data: dict):
    """Track ecommerce order metrics"""

    # Sales tracking
    await record_analytics_point(
        tenant_id=tenant_id,
        platform=PlatformType.CORELDOVE,
        metric_type=MetricType.REVENUE,
        metric_name="order_revenue",
        value=order_data['total_amount'],
        dimensions={
            "order_id": order_data['id'],
            "customer_id": order_data['customer_id'],
            "product_count": len(order_data['items'])
        }
    )

    # Customer engagement
    await record_analytics_point(
        tenant_id=tenant_id,
        platform=PlatformType.CORELDOVE,
        metric_type=MetricType.ENGAGEMENT,
        metric_name="customer_activity",
        value=1,  # Active customer
        dimensions={
            "session_duration": order_data.get('session_duration'),
            "pages_viewed": order_data.get('pages_viewed')
        }
    )
```

#### C. Business Directory Data

Track directory engagement:

```python
async def track_directory_metrics(tenant_id: str, listing_data: dict):
    """Track business directory metrics"""

    # Listing views
    await record_analytics_point(
        tenant_id=tenant_id,
        platform=PlatformType.BUSINESS_DIRECTORY,
        metric_type=MetricType.ENGAGEMENT,
        metric_name="listing_views",
        value=listing_data['view_count'],
        dimensions={
            "listing_id": listing_data['id'],
            "category": listing_data['category'],
            "location": listing_data['location']
        }
    )
```

#### D. ThrillRing Gaming Data

Track gaming activity:

```python
async def track_gaming_metrics(tenant_id: str, session_data: dict):
    """Track gaming session metrics"""

    # Player engagement
    await record_analytics_point(
        tenant_id=tenant_id,
        platform=PlatformType.THRILLRING,
        metric_type=MetricType.ENGAGEMENT,
        metric_name="gaming_session",
        value=session_data['duration_minutes'],
        dimensions={
            "player_id": session_data['player_id'],
            "game_type": session_data['game_type'],
            "score": session_data['final_score']
        }
    )
```

#### E. QuantTrade Financial Data

Track trading performance:

```python
async def track_trading_metrics(tenant_id: str, trade_data: dict):
    """Track trading performance metrics"""

    # Trading performance
    await record_analytics_point(
        tenant_id=tenant_id,
        platform=PlatformType.QUANTTRADE,
        metric_type=MetricType.PERFORMANCE,
        metric_name="trade_pnl",
        value=trade_data['profit_loss'],
        dimensions={
            "trade_id": trade_data['id'],
            "instrument": trade_data['instrument'],
            "strategy": trade_data['strategy']
        }
    )
```

### 4. Frontend Integration

#### A. Install Required Components

Add to your `package.json`:
```json
{
  "dependencies": {
    "recharts": "^2.8.0",
    "lucide-react": "^0.263.1",
    "@radix-ui/react-tabs": "^1.0.4",
    "@radix-ui/react-select": "^1.2.2"
  }
}
```

#### B. Add Analytics Dashboard to Your App

```typescript
// pages/analytics.tsx or app/analytics/page.tsx
import UnifiedAnalyticsDashboard from '@/components/analytics/unified_analytics_dashboard';

export default function AnalyticsPage() {
  return (
    <div className="container mx-auto">
      <UnifiedAnalyticsDashboard />
    </div>
  );
}
```

#### C. Add Navigation Menu Item

```typescript
// components/navigation.tsx
const navigationItems = [
  // ... other items
  {
    name: 'Analytics',
    href: '/analytics',
    icon: BarChart3Icon,
    current: pathname === '/analytics',
  }
];
```

### 5. Real-time Data Collection

#### A. Set up Data Collection Triggers

Add triggers to your existing data models:

```python
# In your existing service files
from analytics.services.data_collection import collect_platform_metrics

# After creating/updating records
async def create_campaign(campaign_data: dict):
    # Your existing logic
    campaign = await create_campaign_record(campaign_data)

    # Analytics collection
    await collect_platform_metrics(
        tenant_id=campaign.tenant_id,
        platform="bizoholic",
        action="campaign_created",
        data=campaign_data
    )

    return campaign
```

#### B. Implement WebSocket Updates (Optional)

For real-time dashboard updates:

```python
from fastapi import WebSocket
import json

@app.websocket("/ws/analytics/{tenant_id}")
async def analytics_websocket(websocket: WebSocket, tenant_id: str):
    await websocket.accept()

    try:
        while True:
            # Send real-time updates
            latest_metrics = await get_latest_metrics(tenant_id)
            await websocket.send_text(json.dumps(latest_metrics))
            await asyncio.sleep(30)  # Update every 30 seconds

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for tenant {tenant_id}")
```

### 6. AI Integration

#### A. Configure AI Coordinator

Ensure your AI coordinator is properly configured:

```python
# ai/services/bizosaas_brain/main.py
from ai.services.bizosaas_brain.tenant_aware_ai_coordinator import TenantAwareAICoordinator

ai_coordinator = TenantAwareAICoordinator(rls_manager)

# Register analytics-specific agents
await ai_coordinator.register_agent({
    "specialization": "data_analyst",
    "supported_platforms": ["all"],
    "capabilities": ["trend_analysis", "insight_generation", "anomaly_detection"]
})
```

#### B. Enable Automated Insights

Set up automated insight generation:

```python
# Schedule daily insight generation
from celery import Celery

@celery.task
async def generate_daily_insights():
    """Generate AI insights for all tenants"""
    tenants = await get_all_tenants()

    for tenant in tenants:
        try:
            await analytics_service.generate_ai_insights(
                platform_data=await collect_tenant_data(tenant.id),
                platform_metrics=await get_platform_metrics(tenant.id),
                tenant_context=tenant.context
            )
        except Exception as e:
            logger.error(f"Failed to generate insights for {tenant.id}: {e}")

# Schedule to run daily at 2 AM
celery.conf.beat_schedule = {
    'generate-insights': {
        'task': 'generate_daily_insights',
        'schedule': crontab(hour=2, minute=0),
    },
}
```

### 7. Security & Compliance

#### A. Enable Row-Level Security

Ensure RLS is enabled and working:

```sql
-- Test RLS functionality
SET app.current_tenant_id = 'tenant-a';
INSERT INTO analytics.analytics_data_points (tenant_id, platform, metric_type, metric_name, metric_value)
VALUES ('tenant-a', 'bizoholic', 'revenue', 'test_metric', 100.00);

SET app.current_tenant_id = 'tenant-b';
SELECT * FROM analytics.analytics_data_points; -- Should not see tenant-a data
```

#### B. Configure Data Retention

Set up automatic data cleanup:

```python
# Schedule weekly cleanup
@celery.task
async def cleanup_old_analytics():
    """Clean up old analytics data"""
    deleted_count = await analytics_service.cleanup_old_data(
        retention_days=365  # Keep 1 year of data
    )
    logger.info(f"Cleaned up {deleted_count} old analytics records")

# Schedule weekly cleanup
celery.conf.beat_schedule['cleanup-analytics'] = {
    'task': 'cleanup_old_analytics',
    'schedule': crontab(day_of_week=0, hour=3, minute=0),  # Sunday 3 AM
}
```

### 8. Performance Optimization

#### A. Database Indexing

Ensure proper indexes are created:

```sql
-- Additional performance indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_analytics_tenant_platform_time_value
ON analytics.analytics_data_points(tenant_id, platform, recorded_at DESC, metric_value);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_daily_metrics_tenant_platform_date
ON analytics.daily_metrics(tenant_id, platform, metric_date DESC);
```

#### B. Caching Strategy

Implement Redis caching for frequent queries:

```python
import redis
import json
from datetime import timedelta

redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def get_cached_dashboard(tenant_id: str, time_range: str) -> Optional[dict]:
    """Get cached dashboard data"""
    cache_key = f"dashboard:{tenant_id}:{time_range}"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        return json.loads(cached_data)
    return None

async def cache_dashboard(tenant_id: str, time_range: str, dashboard_data: dict):
    """Cache dashboard data for 15 minutes"""
    cache_key = f"dashboard:{tenant_id}:{time_range}"
    redis_client.setex(
        cache_key,
        timedelta(minutes=15),
        json.dumps(dashboard_data, default=str)
    )
```

### 9. Testing

#### A. Unit Tests

Create tests for analytics functionality:

```python
# tests/test_analytics.py
import pytest
from analytics.services.unified_analytics_service import UnifiedAnalyticsService

@pytest.mark.asyncio
async def test_analytics_data_collection():
    """Test analytics data collection"""
    service = UnifiedAnalyticsService(rls_manager, ai_coordinator)

    # Test data point creation
    result = await service.record_analytics_point(
        tenant_id="test-tenant",
        platform=PlatformType.BIZOHOLIC,
        metric_type=MetricType.REVENUE,
        metric_name="test_revenue",
        value=100.00
    )

    assert result is not None
    assert result.tenant_id == "test-tenant"

@pytest.mark.asyncio
async def test_tenant_isolation():
    """Test that tenant data is properly isolated"""
    # Set tenant context
    await rls_manager.set_tenant_context(session, "tenant-a")

    # Query should only return tenant-a data
    data = await analytics_service.collect_platform_data(
        session, tenant_context, query
    )

    # Verify all data belongs to tenant-a
    for platform_data in data.values():
        for point in platform_data:
            assert point.tenant_id == "tenant-a"
```

#### B. Integration Tests

Test end-to-end analytics flow:

```python
@pytest.mark.asyncio
async def test_dashboard_generation():
    """Test complete dashboard generation"""

    # Create test data
    await create_test_analytics_data()

    # Generate dashboard
    dashboard = await analytics_service.build_unified_dashboard(
        session=session,
        tenant_context=test_tenant_context,
        query=test_query
    )

    # Verify dashboard structure
    assert dashboard.tenant_id == test_tenant_context.tenant_id
    assert len(dashboard.platform_metrics) > 0
    assert len(dashboard.cross_platform_insights) >= 0
```

### 10. Monitoring & Maintenance

#### A. Health Checks

Add health check endpoints:

```python
@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check for analytics system"""
    checks = {}

    # Database connectivity
    try:
        await session.execute("SELECT 1 FROM analytics.analytics_data_points LIMIT 1")
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"

    # AI coordinator
    try:
        await ai_coordinator.health_check()
        checks["ai_coordinator"] = "healthy"
    except Exception as e:
        checks["ai_coordinator"] = f"error: {str(e)}"

    # Redis cache
    try:
        redis_client.ping()
        checks["cache"] = "healthy"
    except Exception as e:
        checks["cache"] = f"error: {str(e)}"

    overall_status = "healthy" if all(
        status == "healthy" for status in checks.values()
    ) else "degraded"

    return {
        "status": overall_status,
        "checks": checks,
        "timestamp": datetime.utcnow()
    }
```

#### B. Metrics Monitoring

Set up Prometheus metrics:

```python
from prometheus_client import Counter, Histogram, Gauge

# Analytics metrics
analytics_requests = Counter('analytics_requests_total', 'Total analytics requests', ['endpoint', 'tenant'])
analytics_query_duration = Histogram('analytics_query_duration_seconds', 'Analytics query duration')
active_tenants = Gauge('analytics_active_tenants', 'Number of active tenants')

# Middleware to track metrics
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    if request.url.path.startswith("/api/analytics"):
        tenant_id = request.headers.get("X-Tenant-ID", "unknown")
        analytics_requests.labels(endpoint=request.url.path, tenant=tenant_id).inc()

    response = await call_next(request)
    return response
```

## Troubleshooting

### Common Issues

1. **RLS Not Working**
   ```sql
   -- Check if RLS is enabled
   SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'analytics';

   -- Verify tenant context is set
   SHOW app.current_tenant_id;
   ```

2. **Slow Dashboard Loading**
   ```python
   # Check if aggregated metrics are up to date
   SELECT MAX(updated_at) FROM analytics.daily_metrics;

   # Run manual aggregation
   SELECT analytics.aggregate_daily_metrics('tenant-id', 'platform', CURRENT_DATE);
   ```

3. **AI Insights Not Generating**
   ```python
   # Check AI coordinator status
   await ai_coordinator.health_check()

   # Verify agent registration
   agents = await ai_coordinator.list_agents()
   print(f"Available agents: {[a.specialization for a in agents]}")
   ```

### Performance Tuning

1. **Database Optimization**
   ```sql
   -- Update table statistics
   ANALYZE analytics.analytics_data_points;
   ANALYZE analytics.daily_metrics;

   -- Check slow queries
   SELECT query, mean_time, calls
   FROM pg_stat_statements
   WHERE query LIKE '%analytics%'
   ORDER BY mean_time DESC;
   ```

2. **Memory Usage**
   ```python
   # Monitor memory usage during large queries
   import psutil

   def log_memory_usage():
       process = psutil.Process()
       memory_mb = process.memory_info().rss / 1024 / 1024
       logger.info(f"Memory usage: {memory_mb:.2f} MB")
   ```

## Deployment Checklist

- [ ] Analytics schema applied to database
- [ ] RLS policies verified and working
- [ ] Analytics service integrated into FastAPI app
- [ ] Frontend dashboard deployed and accessible
- [ ] Data collection triggers added to all platforms
- [ ] AI coordinator configured with analytics agents
- [ ] Caching layer configured (Redis)
- [ ] Monitoring and health checks implemented
- [ ] Security audit completed
- [ ] Performance testing completed
- [ ] Backup strategy implemented for analytics data
- [ ] Data retention policies configured
- [ ] User access controls configured per subscription tier

## Support

For technical support or questions about the analytics integration:

1. Check the troubleshooting section above
2. Review the API documentation at `/docs#/Analytics`
3. Monitor health check endpoints for system status
4. Check application logs for detailed error messages

---

**Note**: This integration guide assumes you have already completed the setup of the core BizOSaaS platform components including the enhanced tenant context system, RLS manager, and AI coordinator. If you haven't completed these prerequisites, please refer to their respective implementation guides first.