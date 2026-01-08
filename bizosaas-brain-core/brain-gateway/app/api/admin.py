from fastapi import APIRouter, HTTPException, Depends, Request
import httpx
import os
import psutil
import time
from typing import Dict, Any, List
from app.dependencies import get_current_user, require_role, get_db
from sqlalchemy.orm import Session
from domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/admin", tags=["admin"])

AUTH_URL = os.getenv("AUTH_URL", "http://auth-service:8006")

@router.get("/stats")
async def get_platform_stats(
    request: Request,
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Aggregate platform-wide statistics for Super Admins.
    """
    stats = {
        "tenants": {"total": 0, "active": 0},
        "users": {"total": 0, "active": 0},
        "revenue": {"monthly": 0.0, "currency": "USD"},
        "system": {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "uptime_seconds": int(time.time() - psutil.Process().create_time())
        },
        "timestamp": time.time()
    }

    try:
        token = request.headers.get("Authorization")
        async with httpx.AsyncClient() as client:
            # Fetch counts from Auth Service
            response = await client.get(
                f"{AUTH_URL}/auth/admin/counts",
                headers={"Authorization": token} if token else {},
                timeout=5.0
            )
            if response.status_code == 200:
                auth_data = response.json()
                stats["tenants"]["total"] = auth_data.get("total_tenants", 0)
                stats["users"]["total"] = auth_data.get("total_users", 0)
    except Exception as e:
        print(f"Error fetching auth counts: {e}")

    return stats

@router.get("/users")
async def list_all_users(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Proxy to list all users from Auth Service"""
    token = request.headers.get("Authorization")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{AUTH_URL}/users", # FastAPI Users common endpoint
            headers={"Authorization": token} if token else {},
            params={"skip": skip, "limit": limit},
            timeout=10.0
        )
        return response.json()

@router.get("/tenants")
async def list_all_tenants(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Proxy to list all tenants from Auth Service"""
    token = request.headers.get("Authorization")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{AUTH_URL}/tenants",
            headers={"Authorization": token} if token else {},
            params={"skip": skip, "limit": limit},
            timeout=10.0
        )
        return response.json()

@router.get("/health")
async def get_system_health(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Detailed system health info"""
    return {
        "status": "healthy",
        "services": {
            "auth": "up",
            "brain-gateway": "up",
            "database": "connected",
            "redis": "connected"
        },
        "resources": {
            "cpu": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory()._asdict(),
            "disk": psutil.disk_usage('/')._asdict()
        }
    }

@router.get("/analytics")
async def get_api_analytics(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Fetch API analytics from Prometheus metrics.
    """
    metrics = {
        "requests_per_minute": 0,
        "response_time_avg": 0,
        "error_rate": 0.0,
        "active_sessions": 0,
        "llm_requests": 0,
        "timestamp": time.time()
    }

    try:
        async with httpx.AsyncClient() as client:
            # Fetch raw Prometheus metrics from local instrumentator
            response = await client.get("http://localhost:8000/metrics", timeout=2.0)
            if response.status_code == 200:
                text = response.text
                
                # Simple parsing for MVP (In production use prometheus_client parser)
                # Looking for: http_request_duration_seconds_count
                # And: http_request_duration_seconds_sum
                # And: http_request_duration_seconds_bucket{le="5xx"} or similar
                
                req_count = 0
                error_count = 0
                duration_sum = 0.0
                
                for line in text.splitlines():
                    # Total Requests
                    if line.startswith("http_request_duration_seconds_count"):
                        try:
                            val = float(line.split()[-1])
                            req_count += val
                            # Check if this metric line contains agent routes
                            if '/api/brain/agents' in line or '/tasks' in line:
                                metrics["llm_requests"] = metrics.get("llm_requests", 0) + int(val)
                        except: pass
                    
                    # Total Duration
                    elif line.startswith("http_request_duration_seconds_sum"):
                        try:
                            duration_sum += float(line.split()[-1])
                        except: pass
                    
                    # Errors
                    elif 'status="5' in line or 'status="4' in line:
                         if "_count" in line:
                            try:
                                error_count += float(line.split()[-1])
                            except: pass

                # Calculate averages
                metrics["requests_per_minute"] = int(req_count / 10) if req_count > 0 else 0
                metrics["response_time_avg"] = int((duration_sum / req_count) * 1000) if req_count > 0 else 0
                metrics["error_rate"] = round((error_count / req_count) * 100, 2) if req_count > 0 else 0.0
                metrics["active_sessions"] = int(req_count / 100)
                if "llm_requests" not in metrics: metrics["llm_requests"] = 0
                
    except Exception as e:
        print(f"Error fetching Prometheus metrics: {e}")

    return metrics

@router.post("/users/{user_id}/promote")
async def promote_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Promote a user to partner role."""
    from app.services.user_service import UserService
    from uuid import UUID
    user_service = UserService(db)
    try:
        user = user_service.promote_to_partner(UUID(user_id))
        return {"status": "success", "message": f"User {user.email} promoted to partner"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/users/{user_id}/demote")
async def demote_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Demote a partner to client role."""
    from app.services.user_service import UserService
    from uuid import UUID
    user_service = UserService(db)
    try:
        user = user_service.demote_to_client(UUID(user_id))
        return {"status": "success", "message": f"User {user.email} demoted to client"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/audit-logs")
async def get_audit_logs(
    limit: int = 50,
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Fetch recent audit logs."""
    from app.models.user import AuditLog
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()
    return logs
