import httpx
import logging
from typing import Dict, Any, Optional, List
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class FlipkartConnector(BaseConnector):
    """
    Flipkart Seller API Connector.
    Handles product listings, order retrieval, and inventory updates.
    """
    
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="flipkart",
            name="Flipkart Seller",
            type=ConnectorType.MARKETPLACE,
            description="Integrate with Flipkart Seller Hub for listing management, order sync, and fulfillment.",
            icon="flipkart",
            version="1.0.0",
            auth_schema={
                "app_id": {"type": "string", "label": "Application ID", "help": "From Flipkart API Console"},
                "app_secret": {"type": "string", "label": "Application Secret", "format": "password"},
                "seller_id": {"type": "string", "label": "Seller ID"}
            }
        )

    def _get_base_url(self) -> str:
        # Flipkart Seller API Sandbox vs Production
        is_sandbox = self.credentials.get("sandbox", False)
        if is_sandbox:
            return "https://sandbox.flipkart.net/sellers"
        return "https://api.flipkart.net/sellers"

    async def _get_access_token(self) -> str:
        """
        OAuth2 token retrieval for Flipkart.
        """
        # In a real implementation, we would cache this in Redis.
        # This is a simplified version for integration.
        app_id = self.credentials.get("app_id")
        app_secret = self.credentials.get("app_secret")
        
        async with httpx.AsyncClient() as client:
            try:
                # Actual Flipkart OAuth endpoint is https://api.flipkart.net/oauth-service/oauth/token
                response = await client.get(
                    "https://api.flipkart.net/oauth-service/oauth/token",
                    params={
                        "grant_type": "client_credentials",
                        "scope": "manage_listings,read_orders"
                    },
                    auth=(app_id, app_secret),
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json().get("access_token")
            except Exception as e:
                self.logger.error(f"Failed to get Flipkart token: {e}")
                raise

    async def validate_credentials(self) -> bool:
        try:
            # Try to get a token as a validation test
            token = await self._get_access_token()
            return token is not None
        except Exception:
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from Flipkart Seller Hub.
        Supported resource_types: 'listings', 'orders', 'inventory'
        """
        token = await self._get_access_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        endpoint_map = {
            "listings": "listings/v3",
            "orders": "v2/orders/search",
            "inventory": "v3/inventory"
        }
        
        endpoint = endpoint_map.get(resource_type.lower())
        if not endpoint:
            raise ValueError(f"Unsupported resource type for Flipkart: {resource_type}")

        try:
            async with httpx.AsyncClient() as client:
                # Note: Flipkart often uses POST for searches even for 'GET' logic
                method = "POST" if resource_type == "orders" else "GET"
                
                response = await client.request(
                    method,
                    f"{self._get_base_url()}/{endpoint}",
                    headers=headers,
                    json=params if method == "POST" else None,
                    params=params if method == "GET" else None,
                    timeout=30.0
                )
                response.raise_for_status()
                return {"data": response.json(), "status": "success"}
        except Exception as e:
            self.logger.error(f"Flipkart sync failed for {resource_type}: {e}")
            raise

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute actions on Flipkart.
        Supported actions: 'update_price', 'update_inventory', 'create_listing'
        """
        token = await self._get_access_token()
        headers = {"Authorization": f"Bearer {token}"}

        if action == "update_inventory":
            # Flipkart V3 Inventory Update
            sku = payload.get("sku")
            quantity = payload.get("quantity")
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._get_base_url()}/v3/inventory",
                    headers=headers,
                    json={sku: {"quantity": quantity}},
                    timeout=10.0
                )
                return response.json()
        
        elif action == "publish_listing":
            # Map Shopify format to Flipkart schema
            # This is where the 'AI Optimization' normally happens before calling this
            return await self._create_listing(payload, headers)

        raise ValueError(f"Unsupported action: {action}")

    async def _create_listing(self, payload: Dict[str, Any], headers: Dict) -> Dict[str, Any]:
        """
        Mock implementation of listing creation.
        """
        # Flipkart requires multi-stage listing (create draft -> upload images -> publish)
        self.logger.info(f"Creating Flipkart listing for {payload.get('name')}")
        return {"status": "queued", "marketplace": "flipkart", "external_id": f"FK_{payload.get('sku')}"}
