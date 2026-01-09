# Testing & Monitoring Architecture

**Date:** January 9, 2026  
**Version:** 1.0

---

## Overview

This document outlines the technical architecture for implementing comprehensive testing and monitoring across the BizOSaaS platform.

---

## 1. Backend Testing Architecture

### 1.1 Testing Stack

```
pytest (Unit & Integration Tests)
├── pytest-asyncio (Async test support)
├── pytest-cov (Coverage reporting)
├── httpx (Async HTTP client for API tests)
├── pytest-mock (Mocking support)
└── faker (Test data generation)

Locust (Load Testing)
├── Custom load scenarios
├── Performance benchmarking
└── Concurrent user simulation

Contract Testing
├── Pact (Consumer-driven contracts)
└── API schema validation
```

### 1.2 Test Structure

```
testing/
├── backend/
│   ├── unit/
│   │   ├── test_agents.py
│   │   ├── test_connectors.py
│   │   ├── test_rag.py
│   │   ├── test_workflows.py
│   │   └── test_mcp.py
│   ├── integration/
│   │   ├── test_database.py
│   │   ├── test_redis.py
│   │   ├── test_vault.py
│   │   ├── test_temporal.py
│   │   └── test_external_services.py
│   ├── e2e/
│   │   ├── test_onboarding_flow.py
│   │   ├── test_campaign_flow.py
│   │   └── test_data_sync_flow.py
│   ├── performance/
│   │   ├── locustfile.py
│   │   └── scenarios/
│   ├── conftest.py (Fixtures)
│   └── pytest.ini (Config)
├── fixtures/
│   ├── test_data.json
│   ├── mock_responses/
│   └── sample_documents/
└── reports/
    ├── coverage/
    ├── performance/
    └── integration/
```

### 1.3 Test Database Strategy

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def test_db():
    """Create test database for entire test session"""
    engine = create_engine("postgresql://test:test@localhost:5432/test_db")
    TestSessionLocal = sessionmaker(bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    yield TestSessionLocal
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_db):
    """Provide clean database session per test"""
    session = test_db()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
```

### 1.4 API Testing Pattern

```python
# test_brain_gateway.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_agent_execution():
    async with AsyncClient(base_url="http://localhost:8001") as client:
        # Arrange
        payload = {
            "agent_id": "google_ads_specialist",
            "task": "Create campaign",
            "context": {...}
        }
        
        # Act
        response = await client.post("/api/agents/execute", json=payload)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "result" in data
```

### 1.5 Mocking External Services

```python
# test_connectors.py
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_wordpress_connector():
    with patch('app.connectors.wordpress.WordPressConnector._make_request') as mock:
        # Mock WordPress API response
        mock.return_value = {
            "id": 1,
            "title": {"rendered": "Test Post"},
            "status": "publish"
        }
        
        # Test connector
        connector = WordPressConnector(...)
        result = await connector.get_posts()
        
        assert len(result) > 0
        assert result[0]["title"] == "Test Post"
```

---

## 2. OpenTelemetry Integration

### 2.1 Architecture

```
Brain Gateway (FastAPI)
├── OpenTelemetry SDK
│   ├── Tracer Provider
│   ├── Meter Provider
│   └── Logger Provider
├── Instrumentation
│   ├── FastAPI (automatic)
│   ├── SQLAlchemy (automatic)
│   ├── Redis (automatic)
│   └── Custom spans
└── Exporters
    ├── Prometheus (metrics)
    ├── OTLP (traces & logs)
    └── Console (debugging)

Observability Backend
├── Prometheus (metrics storage)
├── Loki (log aggregation)
├── Tempo/Jaeger (trace storage)
└── Grafana (visualization)
```

### 2.2 Implementation

```python
# main.py
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server

# Set up tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Set up metrics
start_http_server(port=8000, addr="0.0.0.0")
reader = PrometheusMetricReader()
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

# Instrument FastAPI
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

# Custom metrics
agent_execution_counter = meter.create_counter(
    name="agent_executions_total",
    description="Total number of agent executions",
    unit="1"
)

agent_duration_histogram = meter.create_histogram(
    name="agent_execution_duration_seconds",
    description="Agent execution duration",
    unit="s"
)
```

### 2.3 Custom Instrumentation

```python
# app/services/agent_service.py
from opentelemetry import trace
import time

tracer = trace.get_tracer(__name__)

async def execute_agent(agent_id: str, task: dict):
    with tracer.start_as_current_span("agent_execution") as span:
        # Add attributes
        span.set_attribute("agent.id", agent_id)
        span.set_attribute("task.type", task["type"])
        
        start_time = time.time()
        
        try:
            # Execute agent
            result = await _execute(agent_id, task)
            span.set_attribute("execution.status", "success")
            
        except Exception as e:
            span.set_attribute("execution.status", "error")
            span.record_exception(e)
            raise
        
        finally:
            duration = time.time() - start_time
            agent_duration_histogram.record(duration, {"agent_id": agent_id})
            agent_execution_counter.add(1, {"agent_id": agent_id})
        
        return result
```

### 2.4 Trace Propagation

```python
# Propagate trace context to external services
from opentelemetry.propagate import inject

async def call_external_api(url: str, data: dict):
    headers = {}
    inject(headers)  # Inject trace context
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
    
    return response
```

---

## 3. Service Health Monitoring

### 3.1 Health Check API

```python
# app/api/health.py
from fastapi import APIRouter, Response
from sqlalchemy import text
import redis
import hvac

router = APIRouter()

@router.get("/health")
async def health_check():
    """Comprehensive health check"""
    health = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {}
    }
    
    # Check PostgreSQL
    try:
        db.execute(text("SELECT 1"))
        health["services"]["postgresql"] = {"status": "up"}
    except Exception as e:
        health["services"]["postgresql"] = {"status": "down", "error": str(e)}
        health["status"] = "unhealthy"
    
    # Check Redis
    try:
        redis_client.ping()
        health["services"]["redis"] = {"status": "up"}
    except Exception as e:
        health["services"]["redis"] = {"status": "down", "error": str(e)}
        health["status"] = "unhealthy"
    
    # Check Vault
    try:
        vault_client.sys.is_initialized()
        health["services"]["vault"] = {"status": "up"}
    except Exception as e:
        health["services"]["vault"] = {"status": "down", "error": str(e)}
        health["status"] = "unhealthy"
    
    # Check Temporal
    try:
        await temporal_client.get_workflow_service().describe_namespace(...)
        health["services"]["temporal"] = {"status": "up"}
    except Exception as e:
        health["services"]["temporal"] = {"status": "down", "error": str(e)}
        health["status"] = "unhealthy"
    
    status_code = 200 if health["status"] == "healthy" else 503
    return Response(content=json.dumps(health), status_code=status_code)

@router.get("/health/ready")
async def readiness_check():
    """Kubernetes readiness probe"""
    # Check if service is ready to accept traffic
    return {"status": "ready"}

@router.get("/health/live")
async def liveness_check():
    """Kubernetes liveness probe"""
    # Check if service is alive
    return {"status": "alive"}
```

### 3.2 Metrics Aggregation

```python
# app/api/metrics.py
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

@router.get("/metrics")
async def metrics_endpoint():
    """Prometheus metrics endpoint"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@router.get("/metrics/summary")
async def metrics_summary():
    """Aggregated metrics summary for Admin Dashboard"""
    return {
        "agents": {
            "total_executions": agent_execution_counter._value.get(),
            "success_rate": calculate_success_rate(),
            "avg_duration": get_avg_duration()
        },
        "connectors": {
            "total_calls": connector_call_counter._value.get(),
            "error_rate": calculate_error_rate()
        },
        "api": {
            "requests_per_minute": get_rpm(),
            "p95_latency": get_p95_latency()
        }
    }
```

### 3.3 Service Dependency Graph

```python
# app/api/admin.py
@router.get("/admin/service-graph")
async def get_service_dependency_graph():
    """Return hierarchical service dependency graph"""
    return {
        "brain_gateway": {
            "status": "up",
            "dependencies": {
                "postgresql": {
                    "status": "up",
                    "latency_ms": 5
                },
                "redis": {
                    "status": "up",
                    "latency_ms": 2
                },
                "vault": {
                    "status": "up",
                    "latency_ms": 10
                },
                "temporal": {
                    "status": "up",
                    "latency_ms": 15
                }
            }
        }
    }
```

---

## 4. Admin Dashboard Integration

### 4.1 Real-time Monitoring Component

```typescript
// app/dashboard/system-status/page.tsx
'use client'

import { useEffect, useState } from 'react'
import { Card } from '@/components/ui/card'

export default function SystemStatusPage() {
  const [health, setHealth] = useState(null)
  const [metrics, setMetrics] = useState(null)

  useEffect(() => {
    // Fetch health status
    const fetchHealth = async () => {
      const res = await fetch('/api/brain/health')
      const data = await res.json()
      setHealth(data)
    }

    // Fetch metrics
    const fetchMetrics = async () => {
      const res = await fetch('/api/brain/metrics/summary')
      const data = await res.json()
      setMetrics(data)
    }

    // Initial fetch
    fetchHealth()
    fetchMetrics()

    // Auto-refresh every 30 seconds
    const interval = setInterval(() => {
      fetchHealth()
      fetchMetrics()
    }, 30000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="space-y-6">
      <h1>System Status</h1>
      
      {/* Service Health Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {health?.services && Object.entries(health.services).map(([name, service]) => (
          <ServiceHealthCard key={name} name={name} service={service} />
        ))}
      </div>

      {/* Metrics Dashboard */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <MetricsCard title="Agent Performance" data={metrics?.agents} />
        <MetricsCard title="Connector Health" data={metrics?.connectors} />
        <MetricsCard title="API Performance" data={metrics?.api} />
      </div>

      {/* OpenTelemetry Traces */}
      <Card>
        <h2>Recent Traces</h2>
        <TracesTable />
      </Card>
    </div>
  )
}
```

### 4.2 WebSocket Live Updates

```typescript
// lib/hooks/useSystemHealth.ts
import { useEffect, useState } from 'react'

export function useSystemHealth() {
  const [health, setHealth] = useState(null)
  const [ws, setWs] = useState<WebSocket | null>(null)

  useEffect(() => {
    // Establish WebSocket connection
    const websocket = new WebSocket('ws://localhost:8001/ws/health')

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setHealth(data)
    }

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    setWs(websocket)

    return () => {
      websocket.close()
    }
  }, [])

  return { health, connected: ws?.readyState === WebSocket.OPEN }
}
```

### 4.3 Grafana Embedding

```typescript
// components/GrafanaDashboard.tsx
export function GrafanaDashboard({ dashboardUid }: { dashboardUid: string }) {
  const grafanaUrl = process.env.NEXT_PUBLIC_GRAFANA_URL
  const iframeUrl = `${grafanaUrl}/d/${dashboardUid}?orgId=1&kiosk=tv`

  return (
    <div className="w-full h-[600px]">
      <iframe
        src={iframeUrl}
        width="100%"
        height="100%"
        frameBorder="0"
      />
    </div>
  )
}
```

---

## 5. Grafana Dashboards

### 5.1 Brain Gateway Dashboard

```json
{
  "dashboard": {
    "title": "Brain Gateway Performance",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Response Time (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, http_request_duration_seconds_bucket)"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])"
          }
        ]
      },
      {
        "title": "Active Connections",
        "targets": [
          {
            "expr": "http_connections_active"
          }
        ]
      }
    ]
  }
}
```

### 5.2 Agent Performance Dashboard

```json
{
  "dashboard": {
    "title": "AI Agent Performance",
    "panels": [
      {
        "title": "Agent Executions",
        "targets": [
          {
            "expr": "sum(agent_executions_total) by (agent_id)"
          }
        ]
      },
      {
        "title": "Execution Duration",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, agent_execution_duration_seconds_bucket)"
          }
        ]
      },
      {
        "title": "Success Rate",
        "targets": [
          {
            "expr": "sum(rate(agent_executions_total{status=\"success\"}[5m])) / sum(rate(agent_executions_total[5m]))"
          }
        ]
      }
    ]
  }
}
```

---

## 6. CI/CD Integration

### 6.1 GitHub Actions Workflow

```yaml
# .github/workflows/backend-tests.yml
name: Backend Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_PASSWORD: test
      redis:
        image: redis:7-alpine

    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd bizosaas-brain-core/brain-gateway
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379/0
        run: |
          cd testing/backend
          pytest -v --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./testing/backend/coverage.xml
```

---

## 7. Performance Benchmarks

### 7.1 Load Testing Scenario

```python
# testing/performance/locustfile.py
from locust import HttpUser, task, between

class BrainGatewayUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def execute_agent(self):
        self.client.post("/api/agents/execute", json={
            "agent_id": "campaign_manager",
            "task": {"type": "analyze_performance"}
        })
    
    @task(2)
    def list_connectors(self):
        self.client.get("/api/connectors")
    
    @task(1)
    def get_metrics(self):
        self.client.get("/api/metrics/summary")
```

### 7.2 Performance Targets

```yaml
# Performance SLAs
api_endpoints:
  p50_latency: < 100ms
  p95_latency: < 500ms
  p99_latency: < 1000ms
  error_rate: < 0.1%
  availability: > 99.9%

agent_execution:
  avg_duration: < 5s
  p95_duration: < 10s
  success_rate: > 95%

database:
  query_latency: < 100ms
  connection_pool: 95% efficiency
```

---

## 8. Security Testing

### 8.1 OWASP ZAP Configuration

```bash
# Run ZAP baseline scan
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t http://localhost:8001 \
  -r zap-report.html

# Run full scan
docker run -t owasp/zap2docker-stable zap-full-scan.py \
  -t http://localhost:8001 \
  -r zap-full-report.html
```

### 8.2 Authentication Tests

```python
# test_auth.py
@pytest.mark.asyncio
async def test_jwt_validation():
    """Test JWT token validation"""
    # Test with invalid token
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.get("/api/agents", headers=headers)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_rbac():
    """Test role-based access control"""
    # Regular user shouldn't access admin endpoints
    user_token = get_user_token()
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await client.get("/api/admin/users", headers=headers)
    assert response.status_code == 403
```

---

## Summary

This architecture provides:

✅ **Comprehensive Testing**
- Unit tests for all components
- Integration tests for all services
- E2E tests for critical flows
- Performance and load testing
- Security testing

✅ **Full Observability**
- OpenTelemetry tracing
- Prometheus metrics
- Centralized logging
- Real-time monitoring

✅ **Service Health Monitoring**
- Health check endpoints
- Service dependency tracking
- Admin dashboard integration
- Alert system

✅ **Production Readiness**
- CI/CD integration
- Performance benchmarks
- Security hardening
- Documentation

