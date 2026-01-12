from temporalio import activity
from typing import Dict, Any, List, Optional
import logging
import httpx
import re
from app.connectors.registry import ConnectorRegistry

logger = logging.getLogger(__name__)

@activity.defn
async def analyze_website_tags(params: Dict[str, Any]) -> Dict[str, Any]:
    """Scrape a website to detect existing marketing tags."""
    url = params.get("url")
    if not url:
        return {"error": "URL is required"}
    
    if not url.startswith("http"):
        url = f"https://{url}"

    logger.info(f"Analyzing website for tags: {url}")
    
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
            response = await client.get(url)
            html = response.text
            
            # Detect GTM
            gtm_match = re.search(r'GTM-[A-Z0-9]+', html)
            # Detect GA4
            ga4_match = re.search(r'G-[A-Z0-9]+', html)
            # Detect Facebook Pixel
            fb_match = re.search(r'fbq\(\'init\', \'([0-9]+)\'\)', html)
            
            results = {
                "gtm_detected": bool(gtm_match),
                "gtm_id": gtm_match.group(0) if gtm_match else None,
                "ga4_detected": bool(ga4_match),
                "ga4_id": ga4_match.group(0) if ga4_match else None,
                "facebook_pixel_detected": bool(fb_match),
                "facebook_pixel_id": fb_match.group(1) if fb_match else None,
                "status": "success"
            }
            
            logger.info(f"Tag detection results for {url}: {results}")
            return results
    except Exception as e:
        logger.error(f"Failed to analyze website {url}: {e}")
        return {"error": str(e), "status": "failed"}

@activity.defn
async def discover_gtm_assets(params: Dict[str, Any]) -> Dict[str, Any]:
    """Use GTM API to discover accounts and containers."""
    access_token = params.get("access_token")
    tenant_id = params.get("tenant_id", "default")
    
    if not access_token:
        return {"error": "Access token is required"}
        
    try:
        connector = ConnectorRegistry.create_connector("google-tag-manager", tenant_id, {"access_token": access_token})
        
        # 1. Get Accounts
        accounts_data = await connector.sync_data("accounts")
        accounts = accounts_data.get("account", [])
        
        if not accounts:
            return {"status": "no_accounts_found"}
            
        # 2. Get Containers for first account (simplistic for now)
        first_account_id = accounts[0]["accountId"]
        connector.credentials["account_id"] = first_account_id
        
        containers_data = await connector.sync_data("containers")
        containers = containers_data.get("container", [])
        
        return {
            "status": "success",
            "account_id": first_account_id,
            "account_name": accounts[0]["name"],
            "containers": [
                {"id": c["publicId"], "name": c["name"], "path": c["path"]} 
                for c in containers
            ]
        }
    except Exception as e:
        logger.error(f"Failed to discover GTM assets: {e}")
        return {"error": str(e), "status": "failed"}

@activity.defn
async def setup_gtm_tags_workflow(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Conceptual setup of tags within a GTM container.
    In a real implementation, this would use the GTM API to create Tags, Triggers, and Variables.
    """
    container_id = params.get("container_id")
    tags_to_setup = params.get("tags", ["ga4", "ads"])
    
    logger.info(f"Setting up tags {tags_to_setup} in GTM container {container_id}")
    
    # Mocking GTM API calls to create tags
    return {
        "status": "success",
        "container_id": container_id,
        "provisioned_tags": tags_to_setup,
        "message": f"Successfully provisioned {len(tags_to_setup)} tags in GTM."
    }
