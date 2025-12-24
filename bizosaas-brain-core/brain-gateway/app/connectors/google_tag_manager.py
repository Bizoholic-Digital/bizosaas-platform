import httpx
from typing import Dict, Any, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class GoogleTagManagerConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="google-tag-manager",
            name="Google Tag Manager",
            type=ConnectorType.MARKETING,
            description="Manage marketing tags (GA4, Ads, FB Pixel) via a single container.",
            icon="tag",
            version="1.0.0",
            auth_schema={
                "container_id": {"type": "string", "label": "Container ID", "placeholder": "GTM-XXXXXX"},
                "account_id": {"type": "string", "label": "Account ID", "placeholder": "Optional (for API access)"},
                "api_key": {"type": "string", "label": "API Key", "format": "password", "placeholder": "Optional (for API access)"}
            }
        )

    async def validate_credentials(self) -> bool:
        # Basic validation: Check if Container ID format is correct
        container_id = self.credentials.get("container_id", "")
        if not container_id.startswith("GTM-"):
            return False
        return True

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from GTM.
        Supported resource_types: 'container'
        """
        return {
            "container_id": self.credentials.get("container_id"),
            "status": "active",
            "meta": {
                "resource": resource_type,
                "source": "gtm_config"
            }
        }

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions.
        Supported actions: 'get_snippet'
        """
        if action == "get_snippet":
            container_id = self.credentials.get("container_id")
            if not container_id:
                return {"status": "error", "message": "container_id is required"}
                
            return {
                "status": "success",
                "snippets": {
                    "head": f"<!-- Google Tag Manager --><script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{container_id}');</script><!-- End Google Tag Manager -->",
                    "body": f"<!-- Google Tag Manager (noscript) --><noscript><iframe src=\"https://www.googletagmanager.com/ns.html?id={container_id}\" height=\"0\" width=\"0\" style=\"display:none;visibility:hidden\"></iframe></noscript><!-- End Google Tag Manager (noscript) -->"
                }
            }
        
        raise ValueError(f"Unsupported action: {action}")
