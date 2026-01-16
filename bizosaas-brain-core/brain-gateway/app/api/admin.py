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
            "method": claim.method,
            "status": claim.status,
            "created_at": claim.created_at
        })
    return results

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
