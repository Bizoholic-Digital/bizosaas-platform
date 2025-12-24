import httpx
import os
from typing import Dict, Any, List, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry
from .oauth_mixin import OAuthMixin

@ConnectorRegistry.register
class HubSpotConnector(BaseConnector, OAuthMixin):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="hubspot",
            name="HubSpot",
            type=ConnectorType.OTHER,
            description="Sync your CRM deals, companies, and contacts with HubSpot.",
            icon="activity",
            version="1.0.0",
            auth_schema={
                "access_token": {"type": "string", "label": "Access Token", "format": "password"},
                "refresh_token": {"type": "string", "label": "Refresh Token", "format": "password"}
            }
        )

    def _get_base_url(self) -> str:
        return "https://api.hubapi.com"

    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        client_id = os.environ.get("HUBSPOT_CLIENT_ID", "")
        scopes = [
            "crm.objects.contacts.read", "crm.objects.contacts.write",
            "crm.objects.deals.read", "crm.objects.companies.read"
        ]
        scope_str = "%20".join(scopes)
        return (
            f"https://app.hubspot.com/oauth/authorize?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"scope={scope_str}&"
            f"state={state}"
        )

    async def exchange_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._get_base_url()}/oauth/v1/token",
                data={
                    "client_id": os.environ.get("HUBSPOT_CLIENT_ID", ""),
                    "client_secret": os.environ.get("HUBSPOT_CLIENT_SECRET", ""),
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_uri
                },
            )
            response.raise_for_status()
            return response.json()

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._get_base_url()}/oauth/v1/token",
                data={
                    "client_id": os.environ.get("HUBSPOT_CLIENT_ID", ""),
                    "client_secret": os.environ.get("HUBSPOT_CLIENT_SECRET", ""),
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token
                },
            )
            response.raise_for_status()
            return response.json()

    async def validate_credentials(self) -> bool:
        token = self.credentials.get("access_token")
        if not token:
            return False
        
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            # Test by fetching contact schema
            response = await client.get(f"{self._get_base_url()}/crm/v3/objects/contacts", headers=headers, params={"limit": 1})
            return response.status_code == 200

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from HubSpot CRM API v3.
        Supported resource_types: 'contacts', 'deals', 'companies'
        """
        token = self.credentials.get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            if resource_type == "contacts":
                response = await client.get(f"{self._get_base_url()}/crm/v3/objects/contacts", headers=headers)
                response.raise_for_status()
                return response.json()
            
            elif resource_type == "deals":
                response = await client.get(f"{self._get_base_url()}/crm/v3/objects/deals", headers=headers)
                response.raise_for_status()
                return response.json()

        return {"error": "Unsupported resource type"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise ValueError(f"Unsupported action: {action}")
