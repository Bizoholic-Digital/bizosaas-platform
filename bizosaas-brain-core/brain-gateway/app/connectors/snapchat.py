import httpx
from typing import Dict, Any, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class SnapchatAdsConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="snapchat-ads",
            name="Snapchat Ads",
            type=ConnectorType.MARKETING,
            description="Reach the Snapchat generation with vertical video ads.",
            icon="ghost",  # Assuming a 'ghost' or 'snapchat' icon exists in frontend
            version="1.0.0",
            auth_schema={
                "access_token": {"type": "string", "label": "OAuth Access Token", "format": "password"},
                "ad_account_id": {"type": "string", "label": "Ad Account ID"}
            }
        )

    def _get_api_url(self) -> str:
        return "https://adsapi.snapchat.com/v1"

    async def validate_credentials(self) -> bool:
        return bool(self.credentials.get("access_token"))

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from Snapchat Marketing API.
        Supported resource_types: 'campaigns', 'ads'
        """
        account_id = self.credentials.get("ad_account_id")
        endpoint = ""
        
        if resource_type == "campaigns":
            endpoint = f"/adaccounts/{account_id}/campaigns"
        elif resource_type == "ads":
            endpoint = f"/adaccounts/{account_id}/ads"
        
        if not endpoint:
             return {"data": [], "meta": {"resource": resource_type, "status": "not_supported"}}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_api_url()}{endpoint}",
                    headers={"Authorization": f"Bearer {self.credentials.get('access_token')}"},
                    params=params,
                    timeout=30.0
                )
                if response.status_code == 200:
                    return {"data": response.json().get("campaigns", [])} # Simplified
                return {"data": [], "error": response.text}
        except Exception as e:
            self.logger.error(f"Snapchat sync failed: {e}")
            raise

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise ValueError(f"Unsupported action: {action}")
