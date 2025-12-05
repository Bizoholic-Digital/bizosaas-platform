"""
Health Router
Health check endpoints for the monitoring service
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
import asyncio
import time

router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": "integration-monitor",
        "version": "1.0.0",
        "timestamp": time.time()
    }


@router.get("/detailed")
async def detailed_health_check():
    """Detailed health check with system information"""
    try:
        # Check database connectivity
        db_healthy = True  # Would check actual DB connection
        
        # Check Redis connectivity
        redis_healthy = True  # Would check actual Redis connection
        
        # Check memory usage
        import psutil
        memory_usage = psutil.virtual_memory().percent
        
        # Check CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # Overall health determination
        overall_healthy = db_healthy and redis_healthy and memory_usage < 90 and cpu_usage < 90
        
        return {
            "status": "healthy" if overall_healthy else "degraded",
            "service": "integration-monitor",
            "version": "1.0.0",
            "timestamp": time.time(),
            "components": {
                "database": "healthy" if db_healthy else "unhealthy",
                "redis": "healthy" if redis_healthy else "unhealthy",
                "memory_usage": f"{memory_usage:.1f}%",
                "cpu_usage": f"{cpu_usage:.1f}%"
            },
            "uptime": time.time() - 1703980800,  # Would track actual start time
            "checks_performed": 0,  # Would get from monitor engine
            "active_integrations": 0  # Would get from registry
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "integration-monitor",
            "version": "1.0.0",
            "timestamp": time.time(),
            "error": str(e)
        }


@router.get("/readiness")
async def readiness_check():
    """Kubernetes readiness probe endpoint"""
    try:
        # Check if service is ready to handle requests
        # This would check if all required components are initialized
        
        ready = True  # Would check actual readiness
        
        if ready:
            return {"status": "ready"}
        else:
            raise HTTPException(status_code=503, detail="Service not ready")
            
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Readiness check failed: {str(e)}")


@router.get("/liveness")
async def liveness_check():
    """Kubernetes liveness probe endpoint"""
    try:
        # Check if service is alive and functioning
        # This would check for deadlocks, infinite loops, etc.
        
        alive = True  # Would check actual liveness
        
        if alive:
            return {"status": "alive"}
        else:
            raise HTTPException(status_code=503, detail="Service not alive")
            
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Liveness check failed: {str(e)}")


@router.get("/startup")
async def startup_check():
    """Kubernetes startup probe endpoint"""
    try:
        # Check if service has completed startup
        # This would check if initial loading is complete
        
        started = True  # Would check actual startup status
        
        if started:
            return {"status": "started"}
        else:
            raise HTTPException(status_code=503, detail="Service still starting")
            
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Startup check failed: {str(e)}")


@router.get("/dependencies")
async def dependencies_check():
    """Check health of external dependencies"""
    try:
        dependencies = {
            "bizosaas_brain": {
                "url": "http://localhost:8001/health",
                "status": "unknown",
                "response_time": 0.0
            },
            "vault": {
                "url": "http://localhost:8200/v1/sys/health",
                "status": "unknown", 
                "response_time": 0.0
            },
            "database": {
                "status": "unknown",
                "response_time": 0.0
            },
            "redis": {
                "status": "unknown",
                "response_time": 0.0
            }
        }
        
        # Check each dependency
        import aiohttp
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
            
            # Check BizOSaaS Brain API
            try:
                start_time = time.time()
                async with session.get("http://localhost:8001/health") as response:
                    dependencies["bizosaas_brain"]["status"] = "healthy" if response.status == 200 else "unhealthy"
                    dependencies["bizosaas_brain"]["response_time"] = time.time() - start_time
            except:
                dependencies["bizosaas_brain"]["status"] = "unhealthy"
            
            # Check Vault
            try:
                start_time = time.time()
                async with session.get("http://localhost:8200/v1/sys/health") as response:
                    dependencies["vault"]["status"] = "healthy" if response.status == 200 else "unhealthy"
                    dependencies["vault"]["response_time"] = time.time() - start_time
            except:
                dependencies["vault"]["status"] = "unhealthy"
        
        # Check database (mock for now)
        dependencies["database"]["status"] = "healthy"
        dependencies["database"]["response_time"] = 0.001
        
        # Check Redis (mock for now)
        dependencies["redis"]["status"] = "healthy"
        dependencies["redis"]["response_time"] = 0.001
        
        # Calculate overall health
        healthy_count = sum(1 for dep in dependencies.values() if dep["status"] == "healthy")
        total_count = len(dependencies)
        overall_health = "healthy" if healthy_count == total_count else "degraded" if healthy_count > 0 else "unhealthy"
        
        return {
            "status": overall_health,
            "dependencies": dependencies,
            "summary": {
                "total": total_count,
                "healthy": healthy_count,
                "unhealthy": total_count - healthy_count
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "dependencies": {}
        }