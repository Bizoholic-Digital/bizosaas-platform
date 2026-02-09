from temporalio import activity
from typing import Dict, Any
import logging
import asyncio
from uuid import UUID
from datetime import datetime
from app.dependencies import SessionLocal
from app.models.mcp import UserMcpInstallation, McpRegistry

logger = logging.getLogger(__name__)

@activity.defn
async def provision_mcp_resources(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates the provisioning of an MCP server (e.g., Docker container on Dokploy).
    Uses the configuration from the McpRegistry.
    """
    installation_id = params.get("installation_id")
    mcp_slug = params.get("mcp_slug")
    
    logger.info(f"Activity: Provisioning resources for installation {installation_id} ({mcp_slug})")
    
    db = SessionLocal()
    try:
        # Fetch registry config
        mcp = db.query(McpRegistry).filter(McpRegistry.slug == mcp_slug).first()
        if not mcp:
            raise Exception(f"MCP Registry entry not found for slug: {mcp_slug}")
            
        config = mcp.mcp_config or {}
        logger.info(f"Using registry config: {config}")
        
        # Simulate container startup delay
        await asyncio.sleep(2)
        
        return {
            "status": "provisioned",
            "resource_id": f"container-{mcp_slug}-{str(installation_id)[:8]}",
            "endpoint": config.get("url") or f"http://{mcp_slug}:8000",
            "config_applied": config
        }
    finally:
        db.close()

@activity.defn
async def configure_mcp_application(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Performs application-specific configuration (e.g., setting up WP plugins or API keys).
    """
    installation_id = params.get("installation_id")
    mcp_slug = params.get("mcp_slug")
    resource_data = params.get("resource_data", {})
    
    logger.info(f"Activity: Configuring MCP application {mcp_slug}")
    
    # Simulate configuration delay
    await asyncio.sleep(1)
    
    # Logic for specific MCPs could go here
    # Example: If mcp_slug == 'wordpress', trigger plugin installs
    
    return {
        "status": "configured",
        "settings": {
            "managed": True,
            "version": "1.0.0",
            "api_endpoint": resource_data.get("endpoint")
        }
    }

@activity.defn
async def finalize_mcp_installation(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Finalizes the installation in the database.
    """
    installation_id = params.get("installation_id")
    status = params.get("status", "active")
    config = params.get("config", {})
    
    logger.info(f"Activity: Finalizing installation {installation_id}")
    
    db = SessionLocal()
    try:
        installation = db.query(UserMcpInstallation).filter(UserMcpInstallation.id == installation_id).first()
        if installation:
            installation.status = status
            installation.config = {**(installation.config or {}), **config}
            installation.updated_at = datetime.utcnow()
            db.commit()
            logger.info(f"Installation {installation_id} set to {status}")
            return {"status": "success", "installation_id": str(installation_id)}
        else:
            return {"status": "error", "message": "Installation not found"}
    finally:
        db.close()

@activity.defn
async def register_managed_service_as_mcp_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Links a newly provisioned managed service (like WordPress) to the tenant's MCP installations.
    This allows agents to immediately 'see' and 'use' the new site via MCP.
    """
    tenant_id = params.get("tenant_id")
    mcp_slug = params.get("mcp_slug", "wordpress") # Default to wordpress for now
    infra_data = params.get("infra_metadata", {})
    setup_data = params.get("setup_data", {})
    
    logger.info(f"Activity: Registering managed {mcp_slug} for tenant {tenant_id}")
    
    db = SessionLocal()
    try:
        # 1. Find the MCP Registry entry
        mcp = db.query(McpRegistry).filter(McpRegistry.slug == mcp_slug).first()
        if not mcp:
            return {"status": "error", "message": f"MCP Registry entry not found for {mcp_slug}"}
            
        # 2. Create UserMcpInstallation
        # In a real system, tenant_id would be checked against user_id or a tenant owner
        # For simplicity, we assume tenant_id maps to a valid user or use a system placeholder
        installation = UserMcpInstallation(
            id=UUID(params.get("installation_id")) if params.get("installation_id") else None,
            user_id=UUID(tenant_id) if tenant_id and tenant_id != "platform_admin" else None,
            mcp_id=mcp.id,
            status="active",
            config={
                "url": infra_data.get("wp_url"),
                "api_key": setup_data.get("api_key"),
                "source": "managed_automation"
            }
        )
        
        db.add(installation)
        db.commit()
        db.refresh(installation)
        
        return {
            "status": "success",
            "installation_id": str(installation.id),
            "mcp_slug": mcp_slug
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to register managed MCP: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
