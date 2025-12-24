from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any
import logging

from app.connectors.registry import ConnectorRegistry
from app.connectors.base import ConnectorConfig, ConnectorStatus
from app.middleware.auth import get_current_user
from domain.ports.identity_port import AuthenticatedUser
from app.store import active_connectors

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/connectors", tags=["connectors"])

@router.get("/types", response_model=List[ConnectorConfig])
async def list_connector_types(
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List all available connector types"""
    return ConnectorRegistry.get_all_configs()

@router.get("/", response_model=List[Dict[str, Any]])
async def list_connectors_with_status(
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List all connectors with their status"""
    tenant_id = user.tenant_id or "default_tenant"
    configs = ConnectorRegistry.get_all_configs()
    
    results = []
    for config in configs:
        key = f"{tenant_id}:{config.id}"
        status = ConnectorStatus.DISCONNECTED
        last_sync = None
        
        if key in active_connectors:
             status = active_connectors[key].get("status", ConnectorStatus.DISCONNECTED)
             last_sync = active_connectors[key].get("last_sync")
        
        # Merge status into config
        data = config.dict()
        data["status"] = status
        data["lastSync"] = last_sync
        results.append(data)
        
    return results

@router.post("/{connector_id}/connect")
async def connect_connector(
    connector_id: str, 
    credentials: Dict[str, Any] = Body(...),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Connect a new integration"""
    tenant_id = user.tenant_id or "default_tenant"
    
    try:
        connector = ConnectorRegistry.create_connector(connector_id, tenant_id, credentials)
        if credentials.get("force_connect"):
            is_valid = True
        else:
            is_valid = await connector.validate_credentials()
        
        if not is_valid:
            raise HTTPException(status_code=400, detail="Invalid credentials")
            
        # Save to mock DB
        active_connectors[f"{tenant_id}:{connector_id}"] = {
            "connector_id": connector_id,
            "credentials": credentials, 
            "status": ConnectorStatus.CONNECTED
        }
        
        return {"status": "connected", "message": f"Successfully connected to {connector.config.name}"}
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to connect connector {connector_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{connector_id}/disconnect")
async def disconnect_connector(
    connector_id: str,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Disconnect an integration"""
    tenant_id = user.tenant_id or "default_tenant"
    key = f"{tenant_id}:{connector_id}"
    
    if key in active_connectors:
        del active_connectors[key]
        
    return {"status": "disconnected"}

@router.post("/{connector_id}/validate")
async def validate_connector(
    connector_id: str,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Validate existing connection"""
    tenant_id = user.tenant_id or "default_tenant"
    key = f"{tenant_id}:{connector_id}"
    
    if key not in active_connectors:
        raise HTTPException(status_code=404, detail="Connector not connected")
        
    data = active_connectors[key]
    connector = ConnectorRegistry.create_connector(connector_id, tenant_id, data["credentials"])
    is_valid = await connector.validate_credentials()
    
    return {"valid": is_valid}

@router.post("/{connector_id}/action/{action}")
async def perform_connector_action(
    connector_id: str,
    action: str,
    payload: Dict[str, Any] = Body(...),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Execute an action on a connector"""
    tenant_id = user.tenant_id or "default_tenant"
    key = f"{tenant_id}:{connector_id}"
    
    if key not in active_connectors:
        raise HTTPException(status_code=404, detail="Connector not connected")
        
    data = active_connectors[key]
    connector = ConnectorRegistry.create_connector(connector_id, tenant_id, data["credentials"])
    
    try:
        result = await connector.perform_action(action, payload)
        
        # If the action updated the credentials (like link_property), save them
        # (Note: In a real DB, connector.credentials would be persisted)
        if result.get("status") == "success":
             active_connectors[key]["credentials"] = connector.credentials
             
        return result
    except Exception as e:
        logger.error(f"Action {action} failed for {connector_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{connector_id}/sync/{resource}")
async def sync_resource(
    connector_id: str,
    resource: str,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Sync data from connector"""
    tenant_id = user.tenant_id or "default_tenant"
    key = f"{tenant_id}:{connector_id}"
    
    if key not in active_connectors:
        raise HTTPException(status_code=404, detail="Connector not connected")
        
    data = active_connectors[key]
    connector = ConnectorRegistry.create_connector(connector_id, tenant_id, data["credentials"])
    
    try:
        result = await connector.sync_data(resource)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{connector_id}/discover/{resource}")
async def discover_resources(
    connector_id: str,
    resource: str,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Alias for sync_data to discover resources like properties or accounts"""
    return await sync_resource(connector_id, resource, user)
