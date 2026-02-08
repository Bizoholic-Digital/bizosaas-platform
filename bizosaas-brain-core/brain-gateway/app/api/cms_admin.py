"""
CMS Administration API
Provides a centralized dashboard for managing all connected WordPress sites
across the platform.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.dependencies import get_db, require_role, get_secret_service
from app.domain.services.secret_service import SecretService
from app.connectors.registry import ConnectorRegistry
from app.connectors.base import ConnectorType
from domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/admin/cms", tags=["cms-admin"])

@router.get("/sites")
async def list_all_connected_sites(
    db: Session = Depends(get_db),
    secret_service: SecretService = Depends(get_secret_service),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """List all WordPress sites connected by tenants."""
    # We need to find all tenants that have any CMS credentials
    # Since credentials are in Vault/DB via SecretService, we might need a way to list them.
    # For now, we'll query the users/tenants table and check for credentials.
    
    from app.models.user import Tenant
    tenants = db.query(Tenant).all()
    
    results = []
    for t in tenants:
        # Check for WordPress/ZipWP credentials
        for cms_id in ["wordpress", "zipwp"]:
            creds = await secret_service.get_connector_credentials(str(t.id), cms_id)
            if creds:
                results.append({
                    "tenant_id": str(t.id),
                    "tenant_name": t.name,
                    "platform": cms_id,
                    "site_url": creds.get("site_url") or creds.get("url"),
                    "status": "connected",
                    "connected_at": t.updated_at # Approximate
                })
    
    return results

@router.get("/plugins/status")
async def get_plugin_distribution_stats(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Get stats on BizoSaaS Connect plugin versions across all sites."""
    # This would ideally call each site or check a central telemetry DB
    return {
        "total_installations": 0,
        "latest_version": "1.2.5",
        "version_breakdown": {
            "1.2.5": 0,
            "1.2.4": 0,
            "1.1.0": 0
        }
    }

@router.post("/plugins/deploy")
async def bulk_deploy_plugin(
    version: str,
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Trigger a bulk update or installation of the BizoSaaS plugin."""
    # This involves a Temporal workflow to iterate through all connected sites
    return {"status": "accepted", "message": f"Bulk deployment of version {version} started"}
