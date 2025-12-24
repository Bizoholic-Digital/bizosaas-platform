import httpx
import os
from typing import Dict, Any, List, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry
from .oauth_mixin import OAuthMixin

@ConnectorRegistry.register
class GoHighLevelConnector(BaseConnector, OAuthMixin):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="gohighlevel",
            name="GoHighLevel (GHL)",
            type=ConnectorType.OTHER,
            description="Manage your CRM contacts, pipelines, and opportunities in GHL.",
            icon="zap",
            version="1.0.0",
            auth_schema={
                "access_token": {"type": "string", "label": "Access Token", "format": "password"},
                "refresh_token": {"type": "string", "label": "Refresh Token", "format": "password"},
                "location_id": {"type": "string", "label": "Location ID", "placeholder": "your_ghl_location_id"}
            }
        )

    def _get_base_url(self) -> str:
        return "https://services.leadconnectorhq.com"

    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        client_id = os.environ.get("GHL_CLIENT_ID", "")
        scopes = [
            "contacts.readonly", "contacts.write", "pipelines.readonly", "opportunities.readonly"
        ]
        scope_str = "%20".join(scopes)
        return (
            f"https://marketplace.gohighlevel.com/oauth/chooselocation?"
            f"response_type=code&"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"scope={scope_str}&"
            f"state={state}"
        )

    async def exchange_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._get_base_url()}/oauth/token",
                data={
                    "client_id": os.environ.get("GHL_CLIENT_ID", ""),
                    "client_secret": os.environ.get("GHL_CLIENT_SECRET", ""),
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
                f"{self._get_base_url()}/oauth/token",
                data={
                    "client_id": os.environ.get("GHL_CLIENT_ID", ""),
                    "client_secret": os.environ.get("GHL_CLIENT_SECRET", ""),
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token
                },
            )
            response.raise_for_status()
            return response.json()

    async def validate_credentials(self) -> bool:
        token = self.credentials.get("access_token")
        location_id = self.credentials.get("location_id")
        if not (token and location_id):
            return False
        
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {token}",
                "Version": "2021-07-28"
            }
            # Test by fetching pipelines
            response = await client.get(
                f"{self._get_base_url()}/pipelines/", 
                headers=headers,
                params={"locationId": location_id}
            )
            return response.status_code == 200

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from GHL API V2.
        Supported resource_types: 'contacts', 'pipelines', 'opportunities'
        """
        token = self.credentials.get("access_token")
        location_id = self.credentials.get("location_id")
        headers = {
            "Authorization": f"Bearer {token}",
            "Version": "2021-07-28"
        }
        
        async with httpx.AsyncClient() as client:
            if resource_type == "contacts":
                response = await client.get(
                    f"{self._get_base_url()}/contacts/", 
                    headers=headers,
                    params={"locationId": location_id}
                )
                response.raise_for_status()
                return response.json()
            
            elif resource_type == "pipelines":
                response = await client.get(
                    f"{self._get_base_url()}/pipelines/", 
                    headers=headers,
                    params={"locationId": location_id}
                )
                response.raise_for_status()
                return response.json()

        return {"error": "Unsupported resource type"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise ValueError(f"Unsupported action: {action}")
