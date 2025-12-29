from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any
import logging

from app.connectors.registry import ConnectorRegistry
from app.connectors.base import ConnectorConfig, ConnectorStatus
from app.middleware.auth import get_current_user
from domain.ports.identity_port import AuthenticatedUser
from app.dependencies import get_secret_service
from app.domain.services.secret_service import SecretService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/connectors", tags=["connectors"])

@router.get("/types", response_model=List[ConnectorConfig])
async def list_connector_types(
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List all available connector types"""
    return ConnectorRegistry.get_all_configs()

@router.get("", response_model=List[Dict[str, Any]])
async def list_connectors_with_status(
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """List all connectors with their status"""
    tenant_id = user.tenant_id or "default_tenant"
    configs = ConnectorRegistry.get_all_configs()
    
    # Get list of connected connectors from Vault
    connected_ids = await secret_service.list_tenant_connectors(tenant_id)
    
    results = []
    for config in configs:
        status = ConnectorStatus.CONNECTED if config.id in connected_ids else ConnectorStatus.DISCONNECTED
        last_sync = None  # TODO: Store sync metadata in Vault
        
        # Merge status into config
        data = config.dict()
        data["status"] = status.value
        data["lastSync"] = last_sync
        results.append(data)
        
    return results

@router.post("/{connector_id}/connect")
async def connect_connector(
    connector_id: str, 
    credentials: Dict[str, Any] = Body(...),
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
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
            
        # Store credentials in Vault
        success = await secret_service.store_connector_credentials(
            tenant_id=tenant_id,
            connector_id=connector_id,
            credentials=credentials,
            metadata={
                "created_by": user.email,
                "connector_name": connector.config.name
            }
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to store credentials securely")
        
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
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """Disconnect an integration"""
    tenant_id = user.tenant_id or "default_tenant"
    
    success = await secret_service.delete_connector_credentials(tenant_id, connector_id)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete credentials")
        
    return {"status": "disconnected"}

@router.post("/{connector_id}/validate")
async def validate_connector(
    connector_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """Validate existing connection"""
    tenant_id = user.tenant_id or "default_tenant"
    
    credentials = await secret_service.get_connector_credentials(tenant_id, connector_id)
    if not credentials:
        raise HTTPException(status_code=404, detail="Connector not connected")
        
    connector = ConnectorRegistry.create_connector(connector_id, tenant_id, credentials)
    is_valid = await connector.validate_credentials()
    
    return {"valid": is_valid}

@router.post("/{connector_id}/action/{action}")
async def perform_connector_action(
    connector_id: str,
    action: str,
    payload: Dict[str, Any] = Body(...),
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """Execute an action on a connector"""
    tenant_id = user.tenant_id or "default_tenant"
    
    credentials = await secret_service.get_connector_credentials(tenant_id, connector_id)
    if not credentials:
        raise HTTPException(status_code=404, detail="Connector not connected")
        
    connector = ConnectorRegistry.create_connector(connector_id, tenant_id, credentials)
    
    try:
        result = await connector.perform_action(action, payload)
        
        # If the action updated the credentials, save them back to Vault
        if result.get("status") == "success":
            await secret_service.store_connector_credentials(
                tenant_id=tenant_id,
                connector_id=connector_id,
                credentials=connector.credentials
            )
             
        return result
    except Exception as e:
        logger.error(f"Action {action} failed for {connector_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{connector_id}/sync/{resource}")
async def sync_resource(
    connector_id: str,
    resource: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """Sync data from connector"""
    tenant_id = user.tenant_id or "default_tenant"
    
    credentials = await secret_service.get_connector_credentials(tenant_id, connector_id)
    if not credentials:
        raise HTTPException(status_code=404, detail="Connector not connected")
        
    connector = ConnectorRegistry.create_connector(connector_id, tenant_id, credentials)
    
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
