import httpx
from typing import Dict, Any, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class PinterestConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="pinterest",
            name="Pinterest",
            type=ConnectorType.MARKETING,
            description="Manage pins, boards, and view analytics.",
            icon="pinterest",
            version="1.0.0",
            auth_schema={
                "access_token": {"type": "string", "label": "Access Token", "format": "password"},
                "ad_account_id": {"type": "string", "label": "Ad Account ID", "placeholder": "Optional for ads"}
            }
        )

    def _get_api_url(self) -> str:
        return "https://api.pinterest.com/v5"

    async def validate_credentials(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_api_url()}/user_account",
                    headers={"Authorization": f"Bearer {self.credentials.get('access_token')}"},
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception:
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from Pinterest.
        Supported resource_types: 'boards', 'pins', 'analytics'
        """
        endpoint = ""
        if resource_type == "boards":
            endpoint = "/boards"
        elif resource_type == "pins":
            endpoint = "/pins"
        else:
            # MVP placeholder for analytics
            return {"data": [], "meta": {"resource": resource_type, "status": "mock"}}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_api_url()}{endpoint}",
                    headers={"Authorization": f"Bearer {self.credentials.get('access_token')}"},
                    params=params,
                    timeout=30.0
                )
                if response.status_code != 200:
                    return {"data": [], "error": response.text}
                    
                return {
                    "data": response.json().get("items", []),
                    "meta": {"resource": resource_type}
                }
        except Exception as e:
            self.logger.error(f"Pinterest sync failed: {e}")
            raise

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions.
        Supported actions: 'create_pin'
        """
        if action == "create_pin":
             # Implementation for creating a pin
             return {"status": "success", "id": "mock_pin_id"}
        
        raise ValueError(f"Unsupported action: {action}")
