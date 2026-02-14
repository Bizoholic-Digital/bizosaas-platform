from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.dependencies import get_db, require_role
from app.models.mcp import McpRegistry, UserMcpInstallation, McpCategory
from app.domain.ports.identity_port import AuthenticatedUser
import random

router = APIRouter(prefix="/api/admin/mcp", tags=["admin-mcp"])

@router.get("/stats")
async def get_mcp_stats(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Overall MCP ecosystem health stats."""
    total_registry = db.query(McpRegistry).count()
    total_installed = db.query(UserMcpInstallation).count()
    active_instances = db.query(UserMcpInstallation).filter(UserMcpInstallation.status == 'active').count()
    pending_instances = db.query(UserMcpInstallation).filter(UserMcpInstallation.status == 'pending').count()
    failed_instances = db.query(UserMcpInstallation).filter(UserMcpInstallation.status == 'failed').count()
    
    # Mock some performance metrics
    latency_avg = random.uniform(45, 120)
    uptime = 99.98
    
    return {
        "registry_count": total_registry,
        "total_installations": total_installed,
        "active_nodes": active_instances,
        "health_score": (active_instances / total_installed * 100) if total_installed > 0 else 100,
        "alerts": pending_instances + failed_instances,
        "average_latency_ms": latency_avg,
        "uptime_percentage": uptime,
        "active_category_distribution": {
            "CRM": 12,
            "Search": 8,
            "Productivity": 15,
            "Utilities": 5
        }
    }

@router.get("/registry")
async def get_full_registry(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Detailed registry view for administration."""
    registry = db.query(McpRegistry).all()
    
    results = []
    for m in registry:
        inst_count = db.query(UserMcpInstallation).filter(UserMcpInstallation.mcp_id == m.id).count()
        results.append({
            "id": str(m.id),
            "name": m.name,
            "slug": m.slug,
            "is_official": m.is_official,
            "install_count": inst_count,
            "capabilities": m.capabilities,
            "vendor": m.vendor_name or "Official",
            "quality_score": m.quality_score,
            "is_recommended": m.is_recommended,
            "tags": m.tags or [],
            "source_type": m.source_type,
            "status": "active" # Registry items are always active in registry
        })
    return results

@router.get("/instances")
async def get_all_instances(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Monitor all running MCP instances across all tenants/users."""
    instances = db.query(UserMcpInstallation).all()
    return [{
        "id": str(i.id),
        "user_id": str(i.user_id),
        "mcp_name": i.mcp.name,
        "mcp_slug": i.mcp.slug,
        "status": i.status,
        "created_at": i.created_at,
        "updated_at": i.updated_at
    } for i in instances]

@router.get("/registry/{mcp_id}/versions")
async def get_mcp_versions(
    mcp_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """List version history of an MCP."""
    from uuid import UUID
    mcp = db.query(McpRegistry).filter(McpRegistry.id == UUID(mcp_id)).first()
    if not mcp:
        raise HTTPException(status_code=404, detail="MCP not found")
        
    # Assuming versions are stored in config metadata or a separate store
    # For MVP without schema change, we look at mcp_config.get("versions", [])
    config = mcp.mcp_config or {}
    versions = config.get("versions", [])
    
    # If no versions list, treat current as v1.0.0
    if not versions:
        versions = [{
            "version": "1.0.0",
            "created_at": str(mcp.created_at),
            "changelog": "Initial release",
            "active": True
        }]
        
    return versions

@router.post("/registry/{mcp_id}/versions")
async def create_mcp_version(
    mcp_id: str,
    version_data: Dict[str, Any], # {version: "1.1.0", changelog: "Fixes"}
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Publish a new version of an MCP."""
    from uuid import UUID
    import datetime
    
    mcp = db.query(McpRegistry).filter(McpRegistry.id == UUID(mcp_id)).first()
    if not mcp:
        raise HTTPException(status_code=404, detail="MCP not found")
    
    config = dict(mcp.mcp_config) if mcp.mcp_config else {}
    versions = config.get("versions", [])
    
    new_version = {
        "version": version_data.get("version"),
        "changelog": version_data.get("changelog"),
        "created_at": datetime.datetime.utcnow().isoformat(),
        "active": True,
        "author": user.email
    }
    
    # Mark old versions as inactive? Or allow multiple active? Usually one "latest"
    # We just append for history
    versions.insert(0, new_version)
    config["versions"] = versions
    
    mcp.mcp_config = config
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(mcp, "mcp_config")
    
    db.commit()
    return {"status": "success", "platform_version": new_version["version"]}
