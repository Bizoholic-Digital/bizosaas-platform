from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Dict, Any, Optional
import httpx
from pydantic import BaseModel
import logging
from app.connectors.registry import ConnectorRegistry
from app.connectors.oauth_mixin import OAuthMixin
from app.dependencies import get_secret_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/oauth", tags=["oauth"])

class OAuthCallbackParams(BaseModel):
    code: str
    state: str
    connector_id: str
    tenant_id: str
    redirect_uri: str = "http://localhost:3003/dashboard/integrations/callback"

@router.get("/authorize/{connector_id}")
async def authorize_connector(connector_id: str, tenant_id: str, redirect_uri: str):
    """
    Start OAuth flow for a connector.
    Returns the authorization URL to redirect the user to.
    """
    connector_cls = ConnectorRegistry.get_connector_class(connector_id)
    if not connector_cls:
        raise HTTPException(status_code=404, detail=f"Connector {connector_id} not found")
    
    # Check if connector supports OAuth
    if not issubclass(connector_cls, OAuthMixin):
        raise HTTPException(status_code=400, detail=f"Connector {connector_id} does not support OAuth")
    
    try:
        # Instantiate with minimal context. Credentials aren't needed for generating auth URL usually.
        connector = connector_cls(tenant_id=tenant_id, credentials={})
        
        # State usually encodes tenant_id and connector_id to verify on callback
        # We can implement a secure state generation helper later.
        state = f"{tenant_id}:{connector_id}" 
        
        auth_url = await connector.get_auth_url(redirect_uri=redirect_uri, state=state)
        return {"url": auth_url}
        
    except Exception as e:
        logger.error(f"Failed to generate auth URL for {connector_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/callback")
async def oauth_callback(
    params: OAuthCallbackParams,
    secret_service = Depends(get_secret_service)
):
    """
    Handle OAuth callback code exchange.
    1. Verify state (simple check for now)
    2. Exchange code for tokens
    3. Save tokens to secure storage (Vault/DB)
    """
    logger.info(f"OAuth callback for {params.connector_id} tenant {params.tenant_id}")
    
    # Verify state matches expected format
    expected_state_prefix = f"{params.tenant_id}:{params.connector_id}"
    if not params.state.startswith(expected_state_prefix):
         raise HTTPException(status_code=400, detail="Invalid state parameter")

    connector_cls = ConnectorRegistry.get_connector_class(params.connector_id)
    if not connector_cls:
        raise HTTPException(status_code=404, detail=f"Connector {params.connector_id} not found")
        
    if not issubclass(connector_cls, OAuthMixin):
        raise HTTPException(status_code=400, detail=f"Connector {params.connector_id} does not support OAuth")

    try:
        connector = connector_cls(tenant_id=params.tenant_id, credentials={})
        token_data = await connector.exchange_code(code=params.code, redirect_uri=params.redirect_uri)
        
        # Save credentials to DB/Vault
        success = await secret_service.store_connector_credentials(
            tenant_id=params.tenant_id,
            connector_id=params.connector_id,
            credentials=token_data,
            metadata={"oauth_connected": True, "provider": params.connector_id}
        )
        
        if not success:
            logger.error(f"Failed to store credentials for {params.connector_id}")
            raise HTTPException(status_code=500, detail="Failed to store credentials securely")
        
        logger.info(f"Successfully connected {params.connector_id} for {params.tenant_id}")
        
        # Check if this is an onboarding discovery request
        if params.state.endswith(":onboarding"):
             logger.info("Triggering automatic discovery for onboarding...")
             # Future: trigger discovery tasks
        
        return {
            "status": "success", 
            "message": "Connected successfully"
            # Removed raw credentials return for security
        }
        
    except Exception as e:
        logger.error(f"OAuth exchange failed for {params.connector_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Connection failed: {str(e)}")
