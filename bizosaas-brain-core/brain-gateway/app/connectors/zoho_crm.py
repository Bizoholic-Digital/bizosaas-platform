import httpx
from typing import Dict, Any, Optional, List
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class ZohoCRMConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="zoho-crm",
            name="Zoho CRM",
            type=ConnectorType.CRM,
            description="Sync leads, contacts, and deals. Automate sales workflows.",
            icon="zoho",
            version="1.0.0",
            auth_schema={
                "client_id": {"type": "string", "label": "Client ID"},
                "client_secret": {"type": "string", "label": "Client Secret", "format": "password"},
                "refresh_token": {"type": "string", "label": "Refresh Token", "help": "Generate via Zoho Developer Console"},
                "data_center": {"type": "select", "label": "Data Center", "options": ["com", "eu", "in", "cn", "au"], "default": "com"}
            }
        )

    def _get_base_url(self) -> str:
        dc = self.credentials.get("data_center", "com")
        return f"https://www.zohoapis.{dc}/crm/v2"

    async def _get_access_token(self) -> str:
        # In a real implementation, we would manage token refresh and caching here.
        # For this prototype, we'll assume the user provides a valid access token 
        # OR we implement a simple refresh flow if client_id/secret/refresh_token are present.
        
        # Simplified for MVP: If 'access_token' is directly provided (for testing)
        if self.credentials.get("access_token"):
            return self.credentials.get("access_token")

        # Refresh token flow
        client_id = self.credentials.get("client_id")
        client_secret = self.credentials.get("client_secret")
        refresh_token = self.credentials.get("refresh_token")
        dc = self.credentials.get("data_center", "com")
        
        if not (client_id and client_secret and refresh_token):
            raise ValueError("Missing OAuth credentials")

        token_url = f"https://accounts.zoho.{dc}/oauth/v2/token"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, params={
                "refresh_token": refresh_token,
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "refresh_token"
            })
            
            if response.status_code != 200:
                raise ValueError(f"Failed to refresh token: {response.text}")
                
            return response.json().get("access_token")

    async def validate_credentials(self) -> bool:
        try:
            token = await self._get_access_token()
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_base_url()}/orgs",
                    headers={"Authorization": f"Zoho-oauthtoken {token}"},
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
        Sync data from Zoho CRM.
        Supported resource_types: 'Leads', 'Contacts', 'Deals', 'Accounts'
        """
        # Map friendly names to API module names if needed
        module_map = {
            "leads": "Leads",
            "contacts": "Contacts",
            "deals": "Deals",
            "accounts": "Accounts"
        }
        module = module_map.get(resource_type.lower(), resource_type)
        
        try:
            token = await self._get_access_token()
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_base_url()}/{module}",
                    headers={"Authorization": f"Zoho-oauthtoken {token}"},
                    params=params,
                    timeout=30.0
                )
                
                if response.status_code == 204: # No Content
                    return {"data": [], "meta": {"count": 0}}
                    
                response.raise_for_status()
                data = response.json()
                
                return {
                    "data": data.get("data", []),
                    "meta": data.get("info", {})
                }
        except Exception as e:
            self.logger.error(f"Sync failed for {resource_type}: {e}")
            raise

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions on Zoho CRM.
        Supported actions: 'create_lead', 'update_lead', 'create_contact'
        """
        if action == "create_lead":
            return await self._create_record("Leads", payload)
        elif action == "create_contact":
            return await self._create_record("Contacts", payload)
        elif action == "create_deal":
            return await self._create_record("Deals", payload)
        
        raise ValueError(f"Unsupported action: {action}")

    async def _create_record(self, module: str, record_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            token = await self._get_access_token()
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._get_base_url()}/{module}",
                    headers={"Authorization": f"Zoho-oauthtoken {token}"},
                    json={"data": [record_data]}, # Zoho expects a list under 'data'
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            self.logger.error(f"Create record failed for {module}: {e}")
            raise
