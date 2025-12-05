import httpx
import base64
from typing import Dict, Any, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class WordPressConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="wordpress",
            name="WordPress",
            type=ConnectorType.CMS,
            description="Connect your WordPress site to sync content and media.",
            icon="wordpress",
            version="1.0.0",
            auth_schema={
                "url": {"type": "string", "label": "WordPress Site URL", "placeholder": "https://your-site.com"},
                "username": {"type": "string", "label": "Username"},
                "application_password": {"type": "string", "label": "Application Password", "help": "Generate in Users > Profile"}
            }
        )

    def _get_auth_header(self) -> Dict[str, str]:
        username = self.credentials.get("username")
        password = self.credentials.get("application_password")
        if not username or not password:
            return {}
        credentials = f"{username}:{password}"
        token = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {token}"}

    def _get_base_url(self) -> str:
        url = self.credentials.get("url", "").rstrip("/")
        # Ensure we don't double-append wp-json if user already included it
        if "wp-json" in url:
            return f"{url}/wp/v2"
        return f"{url}/wp-json/wp/v2"

    async def validate_credentials(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_base_url()}/users/me",
                    headers=self._get_auth_header(),
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
        Sync data from WordPress, WooCommerce, or FluentCRM.
        Supported resource_types: 
        - WP: 'posts', 'pages', 'media'
        - Woo: 'products', 'orders', 'customers'
        - FluentCRM: 'contacts', 'campaigns'
        """
        base_url = self._get_base_url()
        
        # Determine endpoint based on resource type
        if resource_type in ['posts', 'pages', 'media']:
            endpoint = f"{base_url}/wp-json/wp/v2/{resource_type}"
        
        # WooCommerce Endpoints
        elif resource_type in ['products', 'orders', 'customers']:
            endpoint = f"{base_url}/wp-json/wc/v3/{resource_type}"
            
        # FluentCRM Endpoints (assuming REST API enabled)
        elif resource_type in ['contacts', 'campaigns']:
            endpoint = f"{base_url}/wp-json/fluentcrm/v2/{resource_type}"
            
        else:
            raise ValueError(f"Unsupported resource type: {resource_type}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    endpoint,
                    auth=self._get_auth(),
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                return {
                    "data": data,
                    "meta": {
                        "count": len(data) if isinstance(data, list) else 1,
                        "resource": resource_type
                    }
                }
        except Exception as e:
            self.logger.error(f"Sync failed for {resource_type}: {e}")
            raise

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions on WordPress/WooCommerce.
        Supported actions: 'create_post', 'update_post', 'create_product', 'create_contact'
        """
        base_url = self._get_base_url()
        
        if action == "create_post":
            endpoint = f"{base_url}/posts"
            method = "POST"
        elif action == "update_post":
            post_id = payload.get("id")
            endpoint = f"{base_url}/posts/{post_id}"
            method = "PUT"
        elif action == "create_product":
            endpoint = f"{base_url.replace('/wp/v2', '/wc/v3')}/products"
            method = "POST"
        else:
            raise ValueError(f"Unsupported action: {action}")
            
        try:
            async with httpx.AsyncClient() as client:
                if method == "POST":
                    response = await client.post(
                        endpoint,
                        headers=self._get_auth_header(),
                        json=payload,
                        timeout=30.0
                    )
                else:  # PUT
                    response = await client.put(
                        endpoint,
                        headers=self._get_auth_header(),
                        json=payload,
                        timeout=30.0
                    )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            self.logger.error(f"Action {action} failed: {e}")
            raise

