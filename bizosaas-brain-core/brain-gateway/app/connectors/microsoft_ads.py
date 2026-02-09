import httpx
import time
from typing import Dict, Any, List, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry
from .oauth_mixin import OAuthMixin
import os

@ConnectorRegistry.register
class MicrosoftAdsConnector(BaseConnector, OAuthMixin):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="microsoft-ads",
            name="Microsoft Advertising",
            type=ConnectorType.MARKETING,
            description="Manage your Bing search ads and monitor campaign performance.",
            icon="bing",
            version="1.0.0",
            auth_schema={
                "access_token": {"type": "string", "label": "Access Token", "format": "password"},
                "refresh_token": {"type": "string", "label": "Refresh Token", "format": "password"},
                "customer_id": {"type": "string", "label": "Customer ID", "placeholder": "1234567"},
                "developer_token": {"type": "string", "label": "Developer Token", "format": "password"}
            }
        )

    def _get_base_url(self) -> str:
        return "https://ads.microsoft.com/Api/Advertiser/CampaignManagement/v13"

    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        client_id = os.environ.get("MICROSOFT_CLIENT_ID", "")
        scope = "https://ads.microsoft.com/ads.manage offline_access openid profile email"
        scope_enc = scope.replace(" ", "%20")
        return (
            f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?"
            f"client_id={client_id}&"
            f"response_type=code&"
            f"redirect_uri={redirect_uri}&"
            f"response_mode=query&"
            f"scope={scope_enc}&"
            f"state={state}"
        )

    async def exchange_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://login.microsoftonline.com/common/oauth2/v2.0/token",
                data={
                    "client_id": os.environ.get("MICROSOFT_CLIENT_ID", ""),
                    "client_secret": os.environ.get("MICROSOFT_CLIENT_SECRET", ""),
                    "code": code,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                },
            )
            response.raise_for_status()
            return response.json()

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://login.microsoftonline.com/common/oauth2/v2.0/token",
                data={
                    "client_id": os.environ.get("MICROSOFT_CLIENT_ID", ""),
                    "client_secret": os.environ.get("MICROSOFT_CLIENT_SECRET", ""),
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token",
                },
            )
            response.raise_for_status()
            return response.json()

    async def _get_access_token(self) -> str:
        return self.credentials.get("access_token", "")

    async def validate_credentials(self) -> bool:
        token = await self._get_access_token()
        dev_token = self.credentials.get("developer_token")
        if not (token and dev_token):
            return False
            
        # Simplified validation for MVP structure
        return True

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from Microsoft Ads API.
        Supported resource_types: 'campaigns', 'performance'
        """
        # Note: Microsoft Ads uses SOAP or a specialized REST wrapper. 
        # This is a structural implementation for the Brain Gateway.
        return {
            "data": [],
            "meta": {
                "resource": resource_type,
                "source": "microsoft_ads_v13"
            }
        }

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise ValueError(f"Unsupported action: {action}")
