import httpx
from typing import Dict, Any, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class FacebookAdsConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="facebook-ads",
            name="Meta Ads & Social",
            type=ConnectorType.MARKETING,
            description="Manage Facebook and Instagram ads, posts, and insights.",
            icon="facebook",
            version="1.0.0",
            auth_schema={
                "access_token": {"type": "string", "label": "Access Token", "format": "password"},
                "ad_account_id": {"type": "string", "label": "Ad Account ID", "placeholder": "act_123456789"},
                "page_id": {"type": "string", "label": "Page ID", "placeholder": "For organic posts"},
                "pixel_id": {"type": "string", "label": "Meta Pixel ID", "placeholder": "123456789"}
            }
        )

    def _get_base_url(self) -> str:
        return "https://graph.facebook.com/v17.0"

    async def validate_credentials(self) -> bool:
        token = self.credentials.get("access_token")
        if not token:
            return False
        # In real impl, call /me endpoint
        return True

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from Meta Graph API.
        Supported resource_types: 'campaigns', 'insights', 'posts'
        """
        token = self.credentials.get("access_token")
        endpoint = ""
        
        if resource_type == "campaigns":
            account_id = self.credentials.get("ad_account_id")
            endpoint = f"/{account_id}/campaigns"
        elif resource_type == "posts":
            page_id = self.credentials.get("page_id")
            endpoint = f"/{page_id}/posts"
        elif resource_type == "insights":
             account_id = self.credentials.get("ad_account_id")
             endpoint = f"/{account_id}/insights"
        else:
            raise ValueError(f"Unsupported resource type: {resource_type}")

        # Mock response for MVP structure
        return {
            "data": [],
            "meta": {
                "resource": resource_type,
                "source": "meta_graph_api"
            }
        }

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions.
        Supported actions: 'create_post', 'send_capi_event'
        """
        token = self.credentials.get("access_token")
        pixel_id = self.credentials.get("pixel_id")

        if action == "create_post":
            # Logic to post to FB Page
            return {"status": "success", "id": "mock_post_id"}
        
        elif action == "send_capi_event":
            if not pixel_id:
                return {"status": "error", "message": "pixel_id is required for CAPI"}
            
            # Simple CAPI implementation
            # In production, we must hash user data (email, phone, etc.) using SHA-256
            import hashlib
            
            def hash_data(data: Optional[str]) -> Optional[str]:
                if not data: return None
                return hashlib.sha256(data.strip().lower().encode()).hexdigest()

            user_data = payload.get("user_data", {})
            hashed_user_data = {
                "em": [hash_data(user_data.get("email"))] if user_data.get("email") else [],
                "ph": [hash_data(user_data.get("phone"))] if user_data.get("phone") else [],
                "client_ip_address": user_data.get("client_ip_address"),
                "client_user_agent": user_data.get("client_user_agent")
            }

            event_data = {
                "event_name": payload.get("event_name", "PageView"),
                "event_time": int(time.time()),
                "action_source": "website",
                "user_data": hashed_user_data,
                "custom_data": payload.get("custom_data", {})
            }

            url = f"{self._get_base_url()}/{pixel_id}/events"
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, 
                    params={"access_token": token},
                    json={"data": [event_data]}
                )
                response.raise_for_status()
                return response.json()
        
        raise ValueError(f"Unsupported action: {action}")
