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
    """Use GTM API to discover accounts, containers, and workspaces."""
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
            return {"status": "no_accounts_found", "containers": []}
            
        # 2. Get Containers for first account
        first_account_id = accounts[0]["accountId"]
        connector.credentials["account_id"] = first_account_id
        
        containers_data = await connector.sync_data("containers")
        containers = containers_data.get("container", [])

        # 3. Enhance with Workspace info for each container
        enriched_containers = []
        for c in containers:
            # Typically a container has at least one workspace. 
            # We'll fetch workspaces for the container to find the default (usually named "Default Workspace")
            # GTM API path: accounts/{accountId}/containers/{containerId}/workspaces
            async with httpx.AsyncClient() as client:
                url = f"https://www.googleapis.com/tagmanager/v2/accounts/{first_account_id}/containers/{c['containerId']}/workspaces"
                resp = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
                workspaces = resp.json().get("workspace", [])
                
                # Find default or latest
                default_workspace = workspaces[0] if workspaces else None
                
                enriched_containers.append({
                    "id": c["publicId"],
                    "containerId": c["containerId"],
                    "name": c["name"],
                    "path": c["path"],
                    "workspacePath": default_workspace["path"] if default_workspace else None,
                    "workspaceId": default_workspace["workspaceId"] if default_workspace else None
                })
        
        return {
            "status": "success",
            "account_id": first_account_id,
            "account_name": accounts[0]["name"],
            "containers": enriched_containers
        }
    except Exception as e:
        logger.error(f"Failed to discover GTM assets: {e}")
        return {"error": str(e), "status": "failed"}

@activity.defn
async def provision_ga4_in_gtm(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Programmatically create a GA4 Configuration tag in a GTM workspace.
    """
    access_token = params.get("access_token")
    workspace_path = params.get("workspace_path")
    measurement_id = params.get("measurement_id")
    
    if not all([access_token, workspace_path, measurement_id]):
        return {"error": "Missing required parameters for GTM provisioning"}

    logger.info(f"Provisioning GA4 ({measurement_id}) in GTM workspace: {workspace_path}")
    
    try:
        url = f"https://www.googleapis.com/tagmanager/v2/{workspace_path}/tags"
        
        # Tag Definition for GA4 Configuration
        tag_config = {
            "name": "GA4 Configuration - BizOSaaS Managed",
            "type": "gaawe", # GA4 Configuration Type
            "parameter": [
                {"type": "template", "key": "measurementId", "value": measurement_id},
                {"type": "boolean", "key": "sendPageView", "value": "true"}
            ],
            "firingTriggerId": ["2147483647"] # Built-in 'All Pages' trigger ID in GTM
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url, 
                headers={"Authorization": f"Bearer {access_token}"},
                json=tag_config
            )
            
            if resp.status_code == 200:
                return {"status": "success", "tag": resp.json()}
            else:
                return {"status": "error", "message": resp.text, "code": resp.status_code}

    except Exception as e:
        logger.error(f"Failed to provision GA4 in GTM: {e}")
        return {"error": str(e), "status": "failed"}

@activity.defn
async def audit_gtm_container_tags(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes all tags in a GTM workspace and categorizes them.
    Identify: GA4, Google Ads, Facebook Pixel, LinkedIn, etc.
    """
    access_token = params.get("access_token")
    workspace_path = params.get("workspace_path")
    
    if not access_token or not workspace_path:
        return {"error": "Missing access_token or workspace_path"}

    logger.info(f"Auditing GTM tags for workspace: {workspace_path}")
    
    try:
        url = f"https://www.googleapis.com/tagmanager/v2/{workspace_path}/tags"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
            resp.raise_for_status()
            tags = resp.json().get("tag", [])
            
            essential_services = []
            good_to_have_services = []
            
            # Simplified mapping logic
            for tag in tags:
                tag_type = tag.get("type")
                tag_name = tag.get("name")
                
                service_info = {
                    "id": tag.get("tagId"),
                    "name": tag_name,
                    "type": tag_type,
                    "status": "active"
                }

                # Categorization logic
                if tag_type in ["gaawe", "ua"]: # GA4 or Universal Analytics
                    service_info["service"] = "Google Analytics"
                    essential_services.append(service_info)
                elif tag_type in ["awct", "spkt"]: # Google Ads Conversion or Remarketing
                    service_info["service"] = "Google Ads"
                    essential_services.append(service_info)
                elif "facebook" in tag_name.lower() or "pixel" in tag_name.lower():
                    service_info["service"] = "Facebook Pixel"
                    good_to_have_services.append(service_info)
                elif "linkedin" in tag_name.lower():
                    service_info["service"] = "LinkedIn Insight"
                    good_to_have_services.append(service_info)
                else:
                    # General scripts or custom tags
                    service_info["service"] = "Custom Service"
                    good_to_have_services.append(service_info)

            return {
                "status": "success",
                "essential": essential_services,
                "optional": good_to_have_services,
                "raw_count": len(tags)
            }

    except Exception as e:
        logger.error(f"Failed to audit GTM container: {e}")
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
