from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Dict, Any, List
import time
from app.dependencies import get_current_user, require_role
from domain.ports.identity_port import AuthenticatedUser
from app.store import active_connectors
from app.connectors.registry import ConnectorRegistry
import psutil

router = APIRouter(prefix="/api/brain/metrics", tags=["metrics"])

@router.get("/summary")
async def get_metrics_summary(
    user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Get a summary of application metrics for the current tenant or platform.
    """
    tenant_id = user.tenant_id
    
    # Platform-wide for admins, single tenant for users
    is_admin = "admin" in user.roles or "super_admin" in user.roles
    
    # 1. Connector Stats
    configs = ConnectorRegistry.get_all_configs()
    total_available_connectors = len(configs)
    
    # Count active connectors in memory for this tenant
    # (In a real app, query DB for all connectors)
    tenant_active_count = sum(1 for key in active_connectors if key.startswith(f"{tenant_id}:"))
    
    # 2. System Load (Mocking some values that would come from Prometheus)
    summary = {
        "connectors": {
            "total_available": total_available_connectors,
            "active_for_tenant": tenant_active_count,
        },
        "system": {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "status": "healthy"
        },
        "performance": {
            "p95_latency_ms": 450, # Mock
            "uptime_percent": 99.98 # Mock
        }
    }
    
    if is_admin:
        summary["platform"] = {
            "total_active_connectors": len(active_connectors),
            "total_tenants_active": len(set(key.split(':')[0] for key in active_connectors))
        }
        
    return summary

@router.get("/aggregation")
async def get_aggregated_metrics(
    user: AuthenticatedUser = Depends(require_role("admin"))
):
    """
    Aggregate metrics across all components for dashboard visualizations.
    """
    # This would ideally query Prometheus/Loki
    # For now, return mock structured data for the UI
    import random
    
    # Generate some time-series data
    history = []
    now = int(time.time())
    for i in range(10):
        history.append({
            "timestamp": now - (i * 3600),
            "requests": random.randint(100, 1000),
            "errors": random.randint(0, 20)
        })
        
    return {
        "api_traffic": history,
        "connector_health": [
            {"id": "hubspot", "status": "stable", "success_rate": 99.5},
            {"id": "shopify", "status": "stable", "success_rate": 98.2},
            {"id": "wordpress", "status": "stable", "success_rate": 99.9},
        ],
        "top_connectors": [
            {"id": "google-ads", "calls": 5420},
            {"id": "mailchimp", "calls": 3120},
            {"id": "slack", "calls": 1200}
        ]
    }

@router.get("/logs")
async def get_service_logs(
    service: str = "brain-gateway",
    limit: int = 100,
    user: AuthenticatedUser = Depends(require_role("admin"))
):
    """
    Fetch logs from Loki for a specific service.
    """
    import httpx
    import os
    
    loki_url = os.getenv("LOKI_URL", "http://loki:3100")
    
    try:
        async with httpx.AsyncClient() as client:
            # Query Loki for logs from this service
            # We assume logs are labeled with 'container_name' or 'service'
            query = f'{{container_name=~".*{service}.*"}}'
            params = {
                "query": query,
                "limit": limit
            }
            
            response = await client.get(f"{loki_url}/loki/api/v1/query_range", params=params, timeout=5.0)
            
            if response.status_code != 200:
                # Fallback to mock logs if Loki is not reachable or configured
                return {
                    "source": "mock",
                    "logs": [
                        {"timestamp": time.time(), "level": "INFO", "message": f"Starting {service}..."},
                        {"timestamp": time.time() + 1, "level": "DEBUG", "message": "Initialized registry"},
                        {"timestamp": time.time() + 2, "level": "INFO", "message": "API Ready"}
                    ]
                }
            
            return response.json()
            
    except Exception as e:
        return {
            "source": "error",
            "message": str(e),
            "logs": []
        }

@router.post("/alert")
async def receive_alert(
    alert_data: Dict[str, Any] = Body(...)
):
    """
    Webhook endpoint to receive alerts from Prometheus Alertmanager.
    Alerts can be used to trigger in-app notifications or automated recovery.
    """
    import json
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"RECEIVED_ALERT: {json.dumps(alert_data)}")
    
    status = alert_data.get("status")
    alerts = alert_data.get("alerts", [])
    
    for alert in alerts:
        summary = alert.get("annotations", {}).get("summary", "No summary")
        severity = alert.get("labels", {}).get("severity", "info")
        logger.warning(f"ALERT_PROCESSED: [{status.upper()}] {severity} - {summary}")
    
    return {"status": "received"}

@router.get("/endpoints")
async def get_endpoint_analytics(
    user: AuthenticatedUser = Depends(require_role("admin"))
):
    """
    Fetch detailed performance and status analytics for all API endpoints.
    """
    import random
    
    # In production, this would perform a complex Prometheus query:
    # sum(rate(http_request_duration_seconds_count[1h])) by (handler, status)
    
    endpoints = [
        {"path": "/api/brain/agents", "method": "GET", "avg_latency": 150, "success_rate": 99.8, "requests_1h": 1200},
        {"path": "/api/brain/agents/{id}/chat", "method": "POST", "avg_latency": 850, "success_rate": 95.5, "requests_1h": 4500},
        {"path": "/api/connectors", "method": "GET", "avg_latency": 210, "success_rate": 99.9, "requests_1h": 850},
        {"path": "/api/cms/sync", "method": "POST", "avg_latency": 1200, "success_rate": 92.0, "requests_1h": 300},
        {"path": "/health", "method": "GET", "avg_latency": 45, "success_rate": 100.0, "requests_1h": 12000},
    ]
    
    return {
        "summary": {
            "total_requests_1h": sum(e["requests_1h"] for e in endpoints),
            "avg_latency": sum(e["avg_latency"] for e in endpoints) / len(endpoints),
            "error_rate": 100.0 - (sum(e["success_rate"] for e in endpoints) / len(endpoints))
        },
        "endpoints": endpoints
    }
