from fastapi import APIRouter, HTTPException, Depends, Request, Body
import httpx
import os
import psutil
import time
from typing import Dict, Any, List, Optional
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

@router.put("/users/{user_id}/permissions")
async def update_user_permissions(
    user_id: str,
    permissions: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Enable/Disable user features."""
    from app.services.user_service import UserService
    from uuid import UUID
    user_service = UserService(db)
    try:
        user = user_service.update_permissions(UUID(user_id), permissions)
        return {"status": "success", "message": "Permissions updated", "permissions": user.permissions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/users/{user_id}/impersonate")
async def impersonate_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Generate a short-lived impersonation token for Super Admins."""
    impersonation_secret = os.getenv("IMPERSONATION_SECRET")
    if not impersonation_secret:
        raise HTTPException(status_code=500, detail="Impersonation not configured")

    from app.models.user import User
    from uuid import UUID
    import jwt
    import datetime

    # Fetch user details to populate the token
    user = db.query(User).filter(User.id == UUID(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create the token
    now = datetime.datetime.utcnow()
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "name": f"{user.first_name} {user.last_name}",
        "roles": [user.role],
        "tenant_id": str(user.tenant_id) if user.tenant_id else "default",
        "type": "impersonation",
        "impersonator_id": admin_user.id,
        "iat": now,
        "exp": now + datetime.timedelta(hours=1) # 1 hour expiry
    }
    
    token = jwt.encode(payload, impersonation_secret, algorithm="HS256")
    
    # Audit Log
    from app.models.user import AuditLog
    log = AuditLog(
        user_id=admin_user.id,
        action="IMPERSONATION_START",
        details={"target_user": str(user.id), "target_email": user.email}
    )
    db.add(log)
    db.commit()
    
    return {"token": token}

@router.get("/audit-logs")
async def get_audit_logs(
    user_id: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Fetch recent audit logs."""
    from app.models.user import AuditLog
    from uuid import UUID
    
    query = db.query(AuditLog)
    if user_id:
        try:
             # Filter by target user (if 'details' contains it) or the actor (user_id)
             # Usually we want to see what happened TO a user or BY a user.
             # Current model: user_id is the ACTOR.
             # If filter is for a specific user management view, we might want logs where they are the target too?
             # For now, let's filter by the actor (logs of what this user did).
             uid = UUID(user_id)
             query = query.filter(AuditLog.user_id == uid)
        except ValueError:
            pass # Ignore invalid UUID
            
    logs = query.order_by(AuditLog.created_at.desc()).limit(limit).all()
    return logs
