from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any
from app.connectors.registry import ConnectorRegistry
from app.connectors.base import ConnectorConfig, ConnectorStatus
from app.middleware.auth import get_current_user
from domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/connectors", tags=["connectors"])

# Mock database for MVP
active_connectors = {}

@router.get("/types", response_model=List[ConnectorConfig])
async def list_connector_types(
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List all available connector types"""
    return ConnectorRegistry.get_all_configs()

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
        is_valid = await connector.validate_credentials()
        
        if not is_valid:
            raise HTTPException(status_code=400, detail="Invalid credentials")
            
        # Save to mock DB (keyed by tenant)
        active_connectors[f"{tenant_id}:{connector_id}"] = {
            "connector_id": connector_id,
            "credentials": credentials, # In prod, encrypt this!
            "status": ConnectorStatus.CONNECTED
        }
        
        return {"status": "connected", "message": f"Successfully connected to {connector.config.name}"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{connector_id}/status")
async def get_connector_status(
    connector_id: str,
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Get connection status"""
    tenant_id = user.tenant_id or "default_tenant"
    key = f"{tenant_id}:{connector_id}"
    
    if key not in active_connectors:
        return {"status": ConnectorStatus.DISCONNECTED}
        
    data = active_connectors[key]
    connector = ConnectorRegistry.create_connector(connector_id, tenant_id, data["credentials"])
    status = await connector.get_status()
    return {"status": status}

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

@router.post("/{connector_id}/action/{action}")
async def perform_action(
    connector_id: str,
    action: str,
    payload: Dict[str, Any] = Body(...),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Perform action on connector"""
    tenant_id = user.tenant_id or "default_tenant"
    key = f"{tenant_id}:{connector_id}"
    
    if key not in active_connectors:
        raise HTTPException(status_code=404, detail="Connector not connected")
        
    data = active_connectors[key]
    connector = ConnectorRegistry.create_connector(connector_id, tenant_id, data["credentials"])
    
    try:
        result = await connector.perform_action(action, payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
