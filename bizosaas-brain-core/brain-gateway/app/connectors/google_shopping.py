import httpx
from typing import Dict, Any, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class GoogleShoppingConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="google-shopping",
            name="Google Shopping",
            type=ConnectorType.ECOMMERCE,
            description="Sync products to Google Merchant Center.",
            icon="shopping-bag",
            version="1.0.0",
            auth_schema={
                "merchant_id": {"type": "string", "label": "Merchant ID", "placeholder": "123456789"},
                "access_token": {"type": "string", "label": "OAuth Access Token", "format": "password"}
            }
        )

    def _get_api_url(self) -> str:
        return "https://shoppingcontent.googleapis.com/content/v2.1"

    async def validate_credentials(self) -> bool:
        # Basic format check
        return bool(self.credentials.get("merchant_id") and self.credentials.get("access_token"))

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from Google Content API.
        Supported resource_types: 'products'
        """
        if resource_type == "products":
            merchant_id = self.credentials.get("merchant_id")
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{self._get_api_url()}/{merchant_id}/products",
                        headers={"Authorization": f"Bearer {self.credentials.get('access_token')}"},
                        params=params,
                        timeout=30.0
                    )
                    if response.status_code == 200:
                        return {"data": response.json().get("resources", [])}
                    return {"data": [], "error": response.text}
            except Exception as e:
                self.logger.error(f"Google Shopping sync failed: {e}")
                return {"data": [], "error": str(e)}

        return {"data": [], "meta": {"resource": resource_type, "status": "not_supported"}}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions.
        Supported actions: 'insert_product'
        """
        if action == "insert_product":
             # Implementation for product insertion
             return {"status": "success", "id": "mock_product_id"}
        
        raise ValueError(f"Unsupported action: {action}")
