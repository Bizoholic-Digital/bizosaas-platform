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
    secret_service: SecretService = Depends(get_secret_service),
    db: Session = Depends(get_db)
):
    """List all connectors with status and auto-detected suggestions (gated by consent)"""
    tenant_id = user.tenant_id or "default"
    configs = ConnectorRegistry.get_all_configs()
    
    # Check for Discovery Consent (GDPR/SOC2)
    consent = db.query(ConsentRecord).filter(
        ConsentRecord.user_id == user.id,
        ConsentRecord.consent_type == "third_party_sync",
        ConsentRecord.granted == True,
        ConsentRecord.revoked_at == None
    ).first()
    
    # Get connected connectors from Vault
    connected_ids = await secret_service.list_tenant_connectors(tenant_id)
    results = []
    
    for config in configs:
        is_connected = config.id in connected_ids
        status = ConnectorStatus.DISCONNECTED
        features = []
        suggestions = []
        
        if is_connected:
            try:
                credentials = await secret_service.get_connector_credentials(tenant_id, config.id)
                if credentials:
                    connector = ConnectorRegistry.create_connector(config.id, tenant_id, credentials)
                    status = await connector.get_status()
                    
                    # Discovery logic (only if consent granted)
                    if consent and hasattr(connector, '_discover_plugins'):
                        discovery = await connector.perform_action("discover_plugins", {})
                        if discovery.get("status") == "success":
                            plugins = discovery.get("plugins", {})
                            
                            # Map plugins to platform features
                            mapping = {
                                "woocommerce": {"slug": "woocommerce", "label": "WooCommerce", "type": "ecommerce"},
                                "fluent-crm": {"slug": "fluent-crm", "label": "FluentCRM", "type": "crm"}
                            }
                            
                            for p_slug, p_info in plugins.items():
                                if p_info.get("detected") and p_slug in mapping:
                                    feat_type = mapping[p_slug]["type"]
                                    if p_slug in connected_ids:
                                        features.append(feat_type)
                                    else:
                                        suggestions.append(mapping[p_slug])
            except Exception as e:
                logger.warning(f"Status check failed for {config.id}: {e}")
                status = ConnectorStatus.ERROR

        data = config.dict()
        data["status"] = status.value
        data["features"] = features
        data["suggestions"] = suggestions
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
    tenant_id = user.tenant_id or "default"
    
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
    tenant_id = user.tenant_id or "default"
    
    # Remove from Vault
    success = await secret_service.delete_connector_credentials(tenant_id, connector_id)
    
    # Also remove from in-memory seeded store if present
    from app.store import active_connectors
    in_memory_key = f"{tenant_id}:{connector_id}"
    if in_memory_key in active_connectors:
        del active_connectors[in_memory_key]
        success = True # Consider it a success if we removed it from memory
        
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
    tenant_id = user.tenant_id or "default"
    
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
    tenant_id = user.tenant_id or "default"
    
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
    tenant_id = user.tenant_id or "default"
    
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
