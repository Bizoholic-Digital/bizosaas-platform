import os
import httpx
import logging
import psutil
from typing import Dict, Any
from sqlalchemy import text
from app.dependencies import engine

logger = logging.getLogger(__name__)

async def get_dependency_health() -> Dict[str, Any]:
    """
    Returns a structured health status of all system dependencies.
    """
    dependencies = {}
    overall_status = "healthy"

    # 1. Database
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        dependencies["database"] = {"status": "up", "latency": "ok"}
    except Exception as e:
        dependencies["database"] = {"status": "down", "error": str(e)}
        overall_status = "unhealthy"

    # 2. Vault
    vault_addr = os.getenv('VAULT_ADDR')
    if vault_addr:
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(f"{vault_addr}/v1/sys/health", timeout=2.0)
                if res.status_code == 200:
                    dependencies["vault"] = {"status": "up"}
                else:
                    dependencies["vault"] = {"status": "degraded", "code": res.status_code}
        except Exception:
            dependencies["vault"] = {"status": "ignored (optional)"}
            # Vault is optional, do not downgrade overall status
            pass

    # 3. Temporal
    temporal_host = os.getenv("TEMPORAL_HOST", "temporal:7233")
    # Basic check if port is open (simplified)
    import socket
    try:
        host, port = temporal_host.split(":")
        with socket.create_connection((host, int(port)), timeout=1.0):
            dependencies["temporal"] = {"status": "up"}
    except Exception:
        dependencies["temporal"] = {"status": "down"}
        if overall_status == "healthy":
             overall_status = "degraded"

    # 4. Redis (Used for Caching / Rate Limiting)
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        try:
            import redis.asyncio as redis
            r = redis.from_url(redis_url)
            await r.ping()
            dependencies["redis"] = {"status": "up"}
            await r.aclose()
        except Exception as e:
            dependencies["redis"] = {"status": "down", "error": str(e)}
            # Redis is currently optional for core flow

    # 5. Internal Microservices (Optional Check)
    # Only check if env vars are actively set, otherwise ignore
    services = {}
    if os.getenv("CMS_URL"):
        services["cms"] = os.getenv("CMS_URL")
    if os.getenv("CRM_URL"):
        services["crm"] = os.getenv("CRM_URL")
    if os.getenv("AI_AGENTS_URL"):
        services["ai-agents"] = os.getenv("AI_AGENTS_URL")

    service_results = {}
    if services:
        for name, url in services.items():
            try:
                async with httpx.AsyncClient() as client:
                    health_url = f"{url}/health" if name == "ai-agents" else url
                    res = await client.get(health_url, timeout=1.0)
                    service_results[name] = "up" if res.status_code < 500 else f"error:{res.status_code}"
            except Exception:
                # Optional services shouldn't degrade health
                service_results[name] = "unreachable (optional)"
    else:
         service_results = {"message": "No external services configured"}
    
    dependencies["services"] = service_results

    return {
        "status": overall_status,
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        },
        "dependencies": dependencies
    }
