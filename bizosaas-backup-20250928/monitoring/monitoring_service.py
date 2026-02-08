from fastapi import FastAPI
import psutil
import redis
import requests
import asyncio
from datetime import datetime
import json

app = FastAPI(title="BizOSaaS Monitoring Service")

# Service endpoints to monitor
SERVICES = {
    "api-gateway": "http://api-gateway:8080/health",
    "ai-agents": "http://ai-agents:8001/health", 
    "business-directory": "http://business-directory:8003/health",
    "django-crm": "http://django-crm:8007/health",
    "wagtail-cms": "http://wagtail-cms:8010/health"
}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/metrics")
async def get_metrics():
    """Get system and service metrics"""
    # System metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    # Service health checks
    service_health = {}
    for service_name, endpoint in SERVICES.items():
        try:
            response = requests.get(endpoint, timeout=5)
            service_health[service_name] = {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": response.elapsed.total_seconds(),
                "status_code": response.status_code
            }
        except Exception as e:
            service_health[service_name] = {
                "status": "unreachable",
                "error": str(e)
            }
    
    return {
        "timestamp": datetime.now().isoformat(),
        "system": {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available": memory.available,
            "memory_total": memory.total
        },
        "services": service_health
    }

@app.get("/status")
async def get_status():
    """Get overall platform status"""
    metrics = await get_metrics()
    
    # Determine overall status
    unhealthy_services = [
        name for name, health in metrics["services"].items() 
        if health["status"] != "healthy"
    ]
    
    if not unhealthy_services:
        overall_status = "all_healthy"
    elif len(unhealthy_services) < len(SERVICES) // 2:
        overall_status = "degraded"
    else:
        overall_status = "critical"
    
    return {
        "overall_status": overall_status,
        "healthy_services": len(SERVICES) - len(unhealthy_services),
        "total_services": len(SERVICES),
        "unhealthy_services": unhealthy_services,
        "metrics": metrics
    }