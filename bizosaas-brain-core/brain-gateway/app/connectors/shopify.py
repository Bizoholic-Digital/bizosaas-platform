import httpx
from typing import Dict, Any, Optional, List
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class ShopifyConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="shopify",
            name="Shopify",
            type=ConnectorType.ECOMMERCE,
            description="Sync products, orders, and customers. Automate e-commerce workflows.",
            icon="shopify",
            version="1.0.0",
            auth_schema={
                "shop_url": {"type": "string", "label": "Shop URL", "placeholder": "your-shop.myshopify.com"},
                "access_token": {"type": "string", "label": "Admin API Access Token", "format": "password", "help": "From Shopify Admin > Apps > Develop apps"}
            }
        )

    def _get_base_url(self) -> str:
        shop_url = self.credentials.get("shop_url", "").replace("https://", "").replace("http://", "").rstrip("/")
        return f"https://{shop_url}/admin/api/2024-01"

    def _get_headers(self) -> Dict[str, str]:
        token = self.credentials.get("access_token")
        return {
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json"
        }

    async def validate_credentials(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_base_url()}/shop.json",
                    headers=self._get_headers(),
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from Shopify.
        Supported resource_types: 'products', 'orders', 'customers'
        """
        endpoint = resource_type.lower()
        # Map friendly names if needed, but Shopify uses plural lowercase mostly
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_base_url()}/{endpoint}.json",
                    headers=self._get_headers(),
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                # Shopify returns data wrapped in the resource name key, e.g. {'products': [...]}
                # We try to extract the list dynamically
                result_list = data.get(endpoint, [])
                if not result_list and len(data.keys()) == 1:
                    # Fallback: grab the first key's value if it matches expectation
                    key = list(data.keys())[0]
                    result_list = data[key]

                return {
                    "data": result_list,
                    "meta": {
                        "count": len(result_list)
                    }
                }
        except Exception as e:
            self.logger.error(f"Sync failed for {resource_type}: {e}")
            raise

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions on Shopify.
        Supported actions: 'create_product', 'update_product'
        """
        if action == "create_product":
            return await self._create_product(payload)
        
        raise ValueError(f"Unsupported action: {action}")

    async def _create_product(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Ensure payload is wrapped in 'product' key if not already
            if "product" not in payload:
                payload = {"product": payload}

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._get_base_url()}/products.json",
                    headers=self._get_headers(),
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            self.logger.error(f"Create product failed: {e}")
            raise
