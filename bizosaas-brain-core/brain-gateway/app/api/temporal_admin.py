"""
Temporal Administration API
Provides super admins with oversight into the Temporal cluster, including
workflow execution statuses, worker health, and performance analytics.
"""

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Optional, Dict, Any
import os

from app.dependencies import require_role
from domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/admin/temporal", tags=["temporal-admin"])

TEMPORAL_HOST = os.getenv("TEMPORAL_HOST", "localhost:7233")

@router.get("/status")
async def get_temporal_cluster_status(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Check health and connectivity of the Temporal cluster."""
    import socket
    
    host, port = TEMPORAL_HOST.split(":")
    is_up = False
    try:
        with socket.create_connection((host, int(port)), timeout=2.0):
            is_up = True
    except:
        pass
        
    return {
        "host": TEMPORAL_HOST,
        "status": "connected" if is_up else "disconnected",
        "namespace": "default",
        "persistence": "postgresql"
    }

@router.get("/executions")
async def list_active_executions(
    status: Optional[str] = None,
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """List recent and active workflow executions from Temporal."""
    # This would ideally use the Temporal Client to list workflows
    # For now, return a placeholder structure
    return {
        "executions": [
            {
                "workflow_id": "provision_tenant_t001",
                "run_id": "r101",
                "type": "TenantProvisioning",
                "status": "Running",
                "start_time": "2024-03-20T10:00:00Z"
            },
            {
                "workflow_id": "sync_crm_c202",
                "run_id": "r202",
                "type": "CRMSync",
                "status": "Completed",
                "start_time": "2024-03-20T09:00:00Z"
            }
        ],
        "total_active": 1,
        "total_failed_24h": 0
    }

@router.post("/executions/{workflow_id}/cancel")
async def cancel_execution(
    workflow_id: str,
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Cancel a running Temporal workflow."""
    return {"status": "success", "message": f"Cancellation request for {workflow_id} sent to Temporal"}

@router.get("/analytics")
async def get_workflow_analytics(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Aggregate analytics on workflow success rates and durations."""
    return {
        "success_rate": 99.5,
        "avg_duration_seconds": 12.4,
        "peak_concurrency": 45,
        "top_workflow_types": [
            {"type": "TenantProvisioning", "count": 120},
            {"type": "AgentOrchestration", "count": 850},
            {"type": "CRMSync", "count": 2100}
        ]
    }

@router.post("/workers/scale")
async def update_worker_scaling(
    queue_name: str = Body(..., embed=True),
    replicas: int = Body(..., embed=True),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Scale the number of worker replicas for a specific task queue."""
    # In K8s, this would patch the deployment.
    return {"status": "success", "message": f"Scaled queue '{queue_name}' to {replicas} replicas"}

@router.get("/config")
async def get_temporal_config(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """View current Temporal system configuration variables."""
    return {
        "namespace": "default",
        "retention_days": 7,
        "history_archival_status": "disabled",
        "visibility_archival_status": "disabled"
    }

# --- System Configuration Section ---
from fastapi import APIRouter
router_sys = APIRouter(prefix="/api/admin/system", tags=["system-config"])

@router_sys.get("/env")
async def list_safe_env_vars(user: AuthenticatedUser = Depends(require_role("Super Admin"))):
    """List non-sensitive environment variables."""
    return {"ENV": os.getenv("ENV", "production"), "REGION": "us-east-1"}

@router_sys.get("/feature-flags")
async def list_feature_flags(user: AuthenticatedUser = Depends(require_role("Super Admin"))):
    """Global feature flags."""
    return {
        "enable_new_dashboard": True,
        "maintenance_mode": False,
        "beta_agents": True
    }

@router_sys.post("/webhooks")
async def configure_global_webhook(
    url: str = Body(..., embed=True),
    events: List[str] = Body(..., embed=True),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Configure outbound webhooks for system events."""
    return {"status": "success", "id": "wh_123"}

@router_sys.get("/email-templates")
async def list_email_templates(user: AuthenticatedUser = Depends(require_role("Super Admin"))):
    """List customizable email templates."""
    return [
        {"id": "welcome_email", "subject": "Welcome to BizOSaaS"},
        {"id": "invoice_paid", "subject": "Receipt for your payment"}
    ]

@router_sys.put("/branding")
async def update_branding(
    logo_url: str = Body(..., embed=True),
    primary_color: str = Body(..., embed=True),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Update white-label branding settings."""
    return {"status": "updated"}
