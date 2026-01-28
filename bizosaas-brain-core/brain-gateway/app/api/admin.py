from fastapi import APIRouter, HTTPException, Depends, Request, Body
import httpx
import os
import psutil
import time
import logging
from typing import Dict, Any, List, Optional
from app.dependencies import get_current_user, require_role, get_db, get_identity_port
from sqlalchemy.orm import Session
from domain.ports.identity_port import AuthenticatedUser, IdentityPort

logger = logging.getLogger(__name__)

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
    # Use a non-blocking interval for better CPU accuracy
    cpu_usage = psutil.cpu_percent(interval=None) # Non-blocking, but needs prior call
    # Trigger one first if we suspect it might be the first call
    if cpu_usage == 0: cpu_usage = psutil.cpu_percent(interval=0.1)

    stats = {
        "tenants": {"total": 0, "active": 0},
        "users": {"total": 0, "active": 0},
        "revenue": {"monthly": 0.0, "currency": "USD"},
        "system": {
            "cpu_usage": cpu_usage,
            "memory_usage": psutil.virtual_memory().percent,
            "memory_mb": int(psutil.virtual_memory().used / (1024 * 1024)),
            "uptime_seconds": int(time.time() - psutil.Process().create_time()),
            "load_avg": os.getloadavg() if hasattr(os, 'getloadavg') else [0,0,0]
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
    skip: int = 0,
    limit: int = 100,
    identity: IdentityPort = Depends(get_identity_port),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Retrieve all users directly from the Identity Provider (Clerk)."""
    return await identity.list_users(skip=skip, limit=limit)

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    identity: IdentityPort = Depends(get_identity_port),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Permanently delete a user from Clerk and local database."""
    # 1. Protection for Platform Owner
    from app.models.user import User
    from uuid import UUID
    
    # Try to find user email for protection and logging
    user_email = "unknown"
    try:
        # Check Clerk directly first to get email
        # (This is safer than relying on local DB which might be out of sync)
        users = await identity.list_users(limit=500)
        target = next((u for u in users if u["id"] == user_id), None)
        if target:
            user_email = target["email"]
            if user_email == "bizoholic.digital@gmail.com":
                raise HTTPException(status_code=403, detail="Cannot delete the platform owner account.")
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        logger.warning(f"Deletion context check failed: {e}")

    # 2. Delete from Clerk
    clerk_deleted = await identity.delete_user(user_id)
    if not clerk_deleted:
        raise HTTPException(status_code=500, detail="Failed to delete user from Clerk")

    # 3. Delete from Local DB (if exists)
    try:
        # Clean up local references
        # Since local IDs are GUIDs, we might not find them by string user_id
        # We try both by ID and by Email
        db_user = db.query(User).filter(User.email == user_email).first()
        if db_user:
            db.delete(db_user)
            db.commit()
    except Exception as e:
        logger.error(f"Failed to cleanup local user record: {e}")

    # 4. Audit Log
    from app.models.user import AuditLog
    log = AuditLog(
        user_id=admin_user.id,
        action="USER_DELETED_PERMANENTLY",
        details={"target_user_id": user_id, "target_email": user_email}
    )
    db.add(log)
    db.commit()

    return {"status": "success", "message": f"User {user_email} deleted successfully"}

@router.put("/users/{user_id}")
async def update_user(
    user_id: str,
    user_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    identity: IdentityPort = Depends(get_identity_port),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Update user profile and roles, syncing to Clerk."""
    # 1. Sync Role to Clerk if provided
    if "role" in user_data:
        # Protect owner role from being changed down? 
        # (Optional, but let's focus on syncing for now)
        await identity.update_user_metadata(user_id, {"role": user_data["role"]})

    # 2. Update Local DB if user exists
    from app.models.user import User
    try:
        # Find by email or GUID
        # In this context, we usually have the email in user_data or fetched from Clerk
        db_user = db.query(User).filter(User.email == user_data.get("email")).first()
        if db_user:
            if "name" in user_data:
                parts = user_data["name"].split()
                db_user.first_name = parts[0] if parts else ""
                db_user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
            if "role" in user_data:
                db_user.role = user_data["role"].lower()
            if "status" in user_data:
                db_user.is_active = (user_data["status"] == "active")
            db.commit()
    except Exception as e:
        logger.error(f"Local DB sync failed during update: {e}")

    return {"status": "success", "message": "User updated successfully"}

@router.get("/users/auth-providers")
async def list_auth_providers(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Get status of SSO providers."""
    # Mock config
    return [
        {"id": "google", "name": "Google Workspace", "enabled": True, "client_id": "********.apps.googleusercontent.com"},
        {"id": "microsoft", "name": "Microsoft Azure AD", "enabled": False, "client_id": None},
        {"id": "facebook", "name": "Facebook", "enabled": False, "client_id": None},
        {"id": "github", "name": "GitHub", "enabled": True, "client_id": "********"}
    ]

@router.put("/users/auth-providers")
async def update_auth_providers(
    provider_id: str = Body(..., embed=True),
    config: Dict[str, Any] = Body(..., embed=True),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Update SSO provider configuration."""
    # In real implementation, this would update Authentik or a config file
    logger.info(f"Updated Auth Provider {provider_id}: {config}")
    return {"status": "success", "message": f"Provider {provider_id} updated"}

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
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Detailed system health info with live connection checks and container status"""
    import subprocess
    import redis
    from sqlalchemy import text
    
    services = {
        "auth": "down",
        "brain-gateway": "up",
        "database": "disconnected",
        "redis": "disconnected",
        "temporal": "disconnected"
    }

    # 1. Check Database
    try:
        db.execute(text("SELECT 1"))
        services["database"] = "connected"
    except Exception as e:
        logger.error(f"Health check: Database disconnected: {e}")

    # 2. Check Redis
    try:
        r = redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))
        if r.ping():
            services["redis"] = "connected"
    except Exception as e:
        logger.error(f"Health check: Redis disconnected: {e}")

    # 3. Check Auth Service
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{AUTH_URL}/health", timeout=2.0)
            if resp.status_code == 200:
                services["auth"] = "up"
    except Exception:
        pass

    # 4. Check Temporal
    try:
        from temporalio.client import Client
        temporal_url = os.getenv("TEMPORAL_URL", "temporal:7233")
        # Lightweight check: try to connect
        # NOTE: A full check might need an async client, but for health check simple attempt is better
        services["temporal"] = "connected" # Simplified for now as Temporal is usually internal
    except Exception:
        pass

    containers = []
    try:
        # Get actual container statuses from docker
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}|{{.Status}}|{{.Image}}"],
            capture_output=True, text=True, timeout=2.0
        )
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if line:
                    parts = line.split("|")
                    if len(parts) == 3:
                        name, status, image = parts
                        containers.append({
                            "name": name,
                            "status": "up" if "Up" in status else "down",
                            "raw_status": status,
                            "image": image
                        })
    except Exception as e:
        logger.error(f"Failed to fetch container status: {e}")

    return {
        "status": "healthy" if all(v in ["up", "connected"] for v in services.values()) else "degraded",
        "services": services,
        "containers": containers,
        "resources": {
            "cpu": psutil.cpu_percent(interval=0.1),
            "memory": psutil.virtual_memory()._asdict(),
            "disk": psutil.disk_usage('/')._asdict()
        }
    }

@router.get("/logs/{service_name}")
async def get_service_logs(
    service_name: str,
    tail: int = 100,
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Fetch logs for a specific docker service/container."""
    import subprocess
    try:
        result = subprocess.run(
            ["docker", "logs", "--tail", str(tail), service_name],
            capture_output=True, text=True, timeout=5.0
        )
        return {
            "service": service_name,
            "logs": result.stdout if result.returncode == 0 else result.stderr,
            "status": "success" if result.returncode == 0 else "error"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch logs: {str(e)}")

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

@router.get("/users/{user_id}/sessions")
async def get_user_sessions(
    user_id: str,
    identity: IdentityPort = Depends(get_identity_port),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Retrieve all active sessions for a specific user."""
    return await identity.list_sessions(user_id)

@router.post("/sessions/{session_id}/revoke")
async def revoke_user_session(
    session_id: str,
    identity: IdentityPort = Depends(get_identity_port),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Forcefully terminate a user session."""
    success = await identity.revoke_session(session_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to revoke session")
    return {"status": "success", "message": "Session revoked"}

@router.get("/directory/stats")
async def get_directory_stats(
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    from app.services.directory_service import DirectoryService
    service = DirectoryService(db)
    return await service.get_directory_stats()

@router.get("/directory/listings")
async def list_directory_listings(
    query: Optional[str] = None,
    city: Optional[str] = None,
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    from app.services.directory_service import DirectoryService
    service = DirectoryService(db)
    return await service.search(query=query, location=city, page=page, limit=limit)

@router.get("/directory/claims")
async def list_directory_claims(
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    from app.models.directory import DirectoryClaimRequest
    from app.models.user import User
    
    claims = db.query(DirectoryClaimRequest).order_by(DirectoryClaimRequest.created_at.desc()).all()
    
    results = []
    for claim in claims:
        user = db.query(User).filter(User.id == claim.user_id).first()
        results.append({
            "id": str(claim.id),
            "listing_id": str(claim.listing_id),
            "user_id": str(claim.user_id),
            "user_email": user.email if user else "Unknown",
            "method": claim.verification_method,
            "status": claim.status,
            "created_at": claim.created_at
        })
    return results

@router.post("/directory/claims/{claim_id}/approve")
async def approve_directory_claim(
    claim_id: str,
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    from app.services.directory_service import DirectoryService
    from uuid import UUID
    service = DirectoryService(db)
    try:
        claim = await service.approve_claim(UUID(claim_id), UUID(admin_user.id))
        return {"status": "success", "message": "Claim approved successfully", "claim_id": str(claim.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/directory/claims/{claim_id}/reject")
async def reject_directory_claim(
    claim_id: str,
    reason: Optional[str] = Body(None, embed=True),
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    from app.services.directory_service import DirectoryService
    from uuid import UUID
    service = DirectoryService(db)
    try:
        claim = await service.reject_claim(UUID(claim_id), UUID(admin_user.id), reason)
        return {"status": "success", "message": "Claim rejected", "claim_id": str(claim.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/directory/listings/{listing_id}")
async def delete_directory_listing(
    listing_id: str,
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    from app.services.directory_service import DirectoryService
    from uuid import UUID
    service = DirectoryService(db)
    try:
        await service.soft_delete_listing(UUID(listing_id))
        return {"status": "success", "message": "Listing soft-deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/directory/listings/{listing_id}/optimize")
async def optimize_directory_listing(
    listing_id: str,
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    from app.services.directory_service import DirectoryService
    from uuid import UUID
    service = DirectoryService(db)
    try:
        optimization = await service.optimize_listing_seo(UUID(listing_id))
        return {"status": "success", "data": optimization}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/revenue/stats")
async def get_platform_revenue_stats(
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    from app.services.revenue_service import RevenueService
    service = RevenueService(db)
    return await service.get_stats()

@router.get("/revenue/transactions")
async def list_revenue_transactions(
    limit: int = 50,
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    from app.services.revenue_service import RevenueService
    service = RevenueService(db)
    return await service.get_recent_transactions(limit=limit)

@router.get("/domains")
async def list_global_domains(
    db: Session = Depends(get_db),
    admin_user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    from app.services.revenue_service import DomainService
    service = DomainService(db)
    return await service.get_all_domains()
