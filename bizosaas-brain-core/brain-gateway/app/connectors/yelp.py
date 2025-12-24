import httpx
from typing import Dict, Any, List, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class YelpConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="yelp",
            name="Yelp Fusion",
            type=ConnectorType.MARKETING,
            description="Monitor your local business reputation and reviews on Yelp.",
            icon="star",
            version="1.0.0",
            auth_schema={
                "api_key": {"type": "string", "label": "Yelp API Key", "format": "password"},
                "business_id": {"type": "string", "label": "Business ID", "placeholder": "your-business-alias-or-id"}
            }
        )

    def _get_base_url(self) -> str:
        return "https://api.yelp.com/v3"

    async def validate_credentials(self) -> bool:
        api_key = self.credentials.get("api_key")
        business_id = self.credentials.get("business_id")
        if not (api_key and business_id):
            return False
        
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {api_key}"}
            # Test by fetching business details
            response = await client.get(f"{self._get_base_url()}/businesses/{business_id}", headers=headers)
            return response.status_code == 200

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from Yelp Fusion API.
        Supported resource_types: 'business_info', 'reviews'
        """
        api_key = self.credentials.get("api_key")
        business_id = self.credentials.get("business_id")
        headers = {"Authorization": f"Bearer {api_key}"}
        
        async with httpx.AsyncClient() as client:
            if resource_type == "business_info":
                response = await client.get(f"{self._get_base_url()}/businesses/{business_id}", headers=headers)
                response.raise_for_status()
                return response.json()
            
            elif resource_type == "reviews":
                response = await client.get(f"{self._get_base_url()}/businesses/{business_id}/reviews", headers=headers)
                response.raise_for_status()
                return response.json()

        return {"error": "Unsupported resource type"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions on Yelp.
        Currently primarily used for retrieval.
        """
        raise ValueError(f"Unsupported action: {action}")
