import httpx
import logging
from typing import Dict, Any, List, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class AutomationConnector(BaseConnector):
    """
    A generic connector for Automation platforms (n8n, Zapier, Make, Pabbly).
    Instead of hardcoding APIs, it focuses on standard Webhook and Workflow triggers.
    """
    
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="automation-hub",
            name="Automation Hub",
            type=ConnectorType.OTHER,
            description="Generic connector for n8n, Zapier, Make, and Pabbly instances.",
            icon="settings",
            version="1.0.0",
            capabilities=["workflows", "webhooks", "data-sync"],
            auth_schema={
                "platform": {
                    "type": "select", 
                    "label": "Platform", 
                    "options": ["n8n", "Zapier", "Make", "Pabbly", "Other"]
                },
                "api_url": {
                    "type": "string", 
                    "label": "API / Host URL", 
                    "placeholder": "https://n8n.yourdomain.com"
                },
                "api_key": {
                    "type": "password", 
                    "label": "API Key / Token"
                },
                "webhook_base_url": {
                    "type": "string", 
                    "label": "Webhook Base URL (Optional)", 
                    "placeholder": "https://n8n.domains.com/webhook"
                }
            }
        )

    async def validate_credentials(self) -> bool:
        platform = self.credentials.get("platform", "").lower()
        api_url = self.credentials.get("api_url", "").rstrip("/")
        api_key = self.credentials.get("api_key")
        
        if not api_url or not api_key:
            return False
            
        try:
            async with httpx.AsyncClient() as client:
                if platform == "n8n":
                    # n8n health check / info
                    response = await client.get(
                        f"{api_url}/api/v1/owner", # Requires API Key
                        headers={"X-N8N-API-KEY": api_key},
                        timeout=10.0
                    )
                    return response.status_code == 200
                elif platform == "make":
                    # Make (Integromat) connection check
                    response = await client.get(
                        f"{api_url}/api/v2/connections",
                        headers={"Authorization": f"Token {api_key}"},
                        timeout=10.0
                    )
                    return response.status_code == 200
                
                # Default success for others if URL is reachable
                response = await client.get(api_url, timeout=5.0)
                return response.status_code < 500
        except Exception as e:
            logger.error(f"Automation validation failed: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Fetch list of workflows or connections"""
        platform = self.credentials.get("platform", "").lower()
        api_url = self.credentials.get("api_url", "").rstrip("/")
        api_key = self.credentials.get("api_key")
        
        async with httpx.AsyncClient() as client:
            if platform == "n8n" and resource_type == "workflows":
                response = await client.get(
                    f"{api_url}/api/v1/workflows",
                    headers={"X-N8N-API-KEY": api_key}
                )
                return response.json()
                
        return {"data": [], "message": f"Sync for {resource_type} not implemented for {platform}"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger a workflow or webhook"""
        if action == "trigger_webhook":
            webhook_url = payload.get("url")
            if not webhook_url and self.credentials.get("webhook_base_url"):
                webhook_url = f"{self.credentials['webhook_base_url']}/{payload.get('slug')}"
                
            if not webhook_url:
                return {"status": "error", "message": "Missing Webhook URL"}
                
            async with httpx.AsyncClient() as client:
                response = await client.post(webhook_url, json=payload.get("data", {}))
                return {
                    "status": "success" if response.status_code < 300 else "error",
                    "http_code": response.status_code,
                    "response": response.text[:500]
                }
                
        return {"status": "error", "message": f"Unknown action: {action}"}
