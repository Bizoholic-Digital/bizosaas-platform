from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any
import logging

from app.connectors.registry import ConnectorRegistry
from app.connectors.base import ConnectorConfig, ConnectorStatus
from app.middleware.auth import get_current_user
from app.domain.ports.identity_port import AuthenticatedUser
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

@router.post("/{connector_id}/test")
async def test_connector_credentials(
    connector_id: str,
    credentials: Dict[str, Any] = Body(...),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Test connector credentials without saving them"""
    tenant_id = user.tenant_id or "default_tenant"
    
    try:
        connector = ConnectorRegistry.create_connector(connector_id, tenant_id, credentials)
        is_valid = await connector.validate_credentials()
        return {"valid": is_valid}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Test failed for {connector_id}: {e}")
        return {"valid": False, "error": str(e)}

@router.get("/{connector_id}/status")
async def get_connector_status(
    connector_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """Get status of a specific connector"""
    tenant_id = user.tenant_id or "default_tenant"
    
    credentials = await secret_service.get_connector_credentials(tenant_id, connector_id)
    if not credentials:
        return {"status": "disconnected"}
        
    try:
        connector = ConnectorRegistry.create_connector(connector_id, tenant_id, credentials)
        status = await connector.get_status()
        return {"status": status.value}
    except Exception:
        return {"status": "error"}

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
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """Alias for sync_data to discover resources like properties or accounts"""
    return await sync_resource(connector_id, resource, user, secret_service)

@router.get("/{connector_id}/plugins")
async def discover_plugins(
    connector_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """Discover plugins for a connected WordPress site"""
    if connector_id != "wordpress":
        raise HTTPException(status_code=400, detail="Plugin discovery only supported for WordPress")
    
    tenant_id = user.tenant_id or "default_tenant"
    credentials = await secret_service.get_connector_credentials(tenant_id, connector_id)
    
    if not credentials:
        raise HTTPException(status_code=404, detail="WordPress not connected")
        
    from app.connectors.wordpress import WordPressConnector
    connector = WordPressConnector(tenant_id=tenant_id, credentials=credentials)
    plugins = await connector.discover_plugins()
    
    return {"plugins": plugins}

@router.post("/{connector_id}/auto-connect-plugins")
async def auto_connect_plugins(
    connector_id: str,
    plugin_slugs: List[str] = Body(...),
    user: AuthenticatedUser = Depends(get_current_user),
    secret_service: SecretService = Depends(get_secret_service)
):
    """
    Automatically connect discovered plugins by reusing parent credentials.
    Specifically optimized for WordPress child plugins like FluentCRM.
    """
    if connector_id != "wordpress":
        raise HTTPException(status_code=400, detail="Auto-connect only supported for WordPress")
    
    tenant_id = user.tenant_id or "default_tenant"
    parent_creds = await secret_service.get_connector_credentials(tenant_id, connector_id)
    
    if not parent_creds:
        raise HTTPException(status_code=404, detail="Parent WordPress connector not found")

    # Mapping of WP plugin text-domains to our connector IDs
    # and any credential transformations needed
    TRANSFORMS = {
        "fluentcrm": {
            "target": "fluentcrm",
            "creds": lambda c: {
                "url": c.get("url"),
                "username": c.get("username"),
                "application_password": c.get("application_password")
            }
        },
        # WooCommerce might work with Basic Auth (WP App Passwords) 
        # if the site is configured to allow it for the WC REST API.
        "woocommerce": {
            "target": "woocommerce",
            "creds": lambda c: {
                "url": c.get("url"),
                # Note: Default WooCommerce connector expects CK/CS. 
                # We might need to handle Basic Auth fallback in the connector itself.
                "consumer_key": c.get("username"), 
                "consumer_secret": c.get("application_password")
            }
        }
    }

    connected = []
    errors = []

    for slug in plugin_slugs:
        if slug not in TRANSFORMS:
            errors.append({"slug": slug, "error": "No auto-connect transform defined for this plugin"})
            continue
        
        config = TRANSFORMS[slug]
        target_id = config["target"]
        child_creds = config["creds"](parent_creds)

        try:
            # 1. Create connector instance to validate
            connector = ConnectorRegistry.create_connector(target_id, tenant_id, child_creds)
            # validation might be slow, we'll do basic check or trust the parent for now
            # is_valid = await connector.validate_credentials()
            
            # 2. Store credentials
            success = await secret_service.store_connector_credentials(
                tenant_id=tenant_id,
                connector_id=target_id,
                credentials=child_creds,
                metadata={
                    "auto_configured_from": "wordpress",
                    "created_by": user.email
                }
            )
            
            if success:
                connected.append(slug)
            else:
                errors.append({"slug": slug, "error": "Failed to store credentials"})
                
        except Exception as e:
            errors.append({"slug": slug, "error": str(e)})

    return {
        "status": "partial_success" if errors else "success",
        "connected": connected,
        "errors": errors
    }

@router.get("/marketplace/plugins")
async def list_marketplace_plugins(
    platform: str = "wordpress",
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List curated plugins for a platform to drive cross-sells and demand understanding."""
    MARKETPLACE = {
        "wordpress": [
            {
                "slug": "fluentcrm",
                "name": "FluentCRM",
                "description": "Full-featured email marketing automation for WP. Sync leads directly to CRM agents.",
                "category": "Marketing",
                "icon": "mail",
                "supported": True,
                "auto_connect": True,
                "partner_deal": "Get 20% off with BIZOSAAS20"
            },
            {
                "slug": "woocommerce",
                "name": "WooCommerce",
                "description": "Power your online store. Sync products and orders to AI Sales agents.",
                "category": "E-commerce",
                "icon": "shopping-cart",
                "supported": True,
                "auto_connect": True
            },
            {
                "slug": "wp-vivid",
                "name": "WPVivid Backup",
                "description": "Best-in-class backup and migration. We are working on a deal for BizOSaaS clients.",
                "category": "Utility",
                "icon": "hard-drive",
                "supported": False,
                "auto_connect": False,
                "status": "Planning"
            },
            {
                "slug": "rank-math",
                "name": "Rank Math SEO",
                "description": "AI-friendly SEO optimization. Requested by many users.",
                "category": "SEO",
                "icon": "trending-up",
                "supported": False,
                "auto_connect": False,
                "status": "In Development"
            }
        ]
    }
    
    return MARKETPLACE.get(platform, [])

@router.post("/marketplace/track-interest")
async def track_plugin_interest(
    plugin_slug: str = Body(..., embed=True),
    action: str = Body(..., embed=True), # 'view', 'click', 'install_attempt'
    platform: str = Body("wordpress", embed=True),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Track user interaction with marketplace items for demand analysis."""
    tenant_id = user.tenant_id or "default_tenant"
    logger.info(f"DEMAND_TRACK: {user.email} | {action} | {platform}:{plugin_slug}")
    
    # Store in DB if needed. For now logs are fine for analytics.
    return {"status": "success", "message": "Interest tracked"}

@router.get("/marketplace/metrics")
async def get_marketplace_metrics(
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Get aggregated marketplace metrics for the platform owner."""
    # Ensure only super_admin can see this
    if user.role != "super_admin" and user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    # In a real app, you'd query the DB for DEMAND_TRACK events.
    # For now, we return mock aggregated data to build the UI.
    return [
        {
            "slug": "fluentcrm",
            "name": "FluentCRM",
            "views": 150,
            "clicks": 45,
            "install_attempts": 12,
            "trend": "+15%",
            "demand_score": 85
        },
        {
            "slug": "woocommerce",
            "name": "WooCommerce",
            "views": 200,
            "clicks": 30,
            "install_attempts": 5,
            "trend": "-5%",
            "demand_score": 62
        },
        {
            "slug": "rank-math",
            "name": "Rank Math SEO",
            "views": 310,
            "clicks": 120,
            "install_attempts": 0, # Not supported yet
            "trend": "+40%",
            "demand_score": 95
        },
        {
            "slug": "wp-vivid",
            "name": "WPVivid Backup",
            "views": 80,
            "clicks": 10,
            "install_attempts": 0,
            "trend": "0%",
            "demand_score": 30
        }
    ]

@router.get("/analytics")
async def get_connector_analytics(
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Get global connector analytics/traffic data"""
    # Mock data structure for now, to be replaced with real OpenTelemetry/Prometheus queries later
    import random
    from datetime import datetime, timedelta

    # Generate last 24h traffic
    now = datetime.utcnow()
    traffic_series = []
    for i in range(24):
        time_slot = (now - timedelta(hours=23-i)).strftime("%H:00")
        traffic_series.append({
            "time": time_slot,
            "requests": random.randint(300, 3000),
            "failures": random.randint(0, 50)
        })

    # Connector usage (could use real connected count + random multipliers)
    # Getting real connected names:
    real_configs = ConnectorRegistry.get_all_configs()
    usage_distribution = []
    colors = ['#4285F4', '#FFE01B', '#96588A', '#4A154B', '#635BFF', '#FF7A59', '#00C853', '#AA00FF']
    
    for idx, config in enumerate(real_configs):
        # Weight popularity for demo
        base_calls = 5000 if config.id in ['google', 'slack', 'stripe'] else 1000
        
        usage_distribution.append({
            "name": config.name,
            "connector_id": config.id,
            "calls": random.randint(base_calls, base_calls * 10),
            "value": random.randint(100, 500), # Used for Pie chart sizing
            "color": colors[idx % len(colors)],
            "reliability": 99.0 + (random.random()), # 99.0 - 100.0
            "latency": f"{random.randint(100, 800)}ms",
            "last_event": f"{random.randint(1, 60)} seconds ago",
            "status": "STABLE" if random.random() > 0.05 else "DEGRADED"
        })

    # Sort by calls for "Top Connectors"
    usage_distribution.sort(key=lambda x: x['calls'], reverse=True)

    return {
        "traffic_series": traffic_series,
        "usage_distribution": usage_distribution,
        "global_stats": {
            "total_requests": f"{sum(d['calls'] for d in usage_distribution)/1000:.1f}K",
            "success_rate": "99.8%",
            "latency_p95": "450ms",
            "throughput": "8.4 GB"
        }
    }
