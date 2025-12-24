import httpx
import os
from typing import Dict, Any, List, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry
from .oauth_mixin import OAuthMixin

@ConnectorRegistry.register
class TikTokAdsConnector(BaseConnector, OAuthMixin):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="tiktok-ads",
            name="TikTok Ads",
            type=ConnectorType.MARKETING,
            description="Manage your short-form video campaigns and track performance on TikTok.",
            icon="video",
            version="1.0.0",
            auth_schema={
                "access_token": {"type": "string", "label": "Access Token", "format": "password"},
                "advertiser_id": {"type": "string", "label": "Advertiser ID", "placeholder": "700..."},
            }
        )

    def _get_base_url(self) -> str:
        return "https://business-api.tiktok.com/open_api/v1.3"

    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        app_id = os.environ.get("TIKTOK_APP_ID", "")
        # TikTok uses a specific auth URL
        return (
            f"https://www.tiktok.com/v2/auth/authorize/?"
            f"client_key={app_id}&"
            f"scope=ads.manage&"
            f"response_type=code&"
            f"redirect_uri={redirect_uri}&"
            f"state={state}"
        )

    async def exchange_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._get_base_url()}/oauth2/access_token/",
                json={
                    "app_id": os.environ.get("TIKTOK_APP_ID", ""),
                    "secret": os.environ.get("TIKTOK_APP_SECRET", ""),
                    "auth_code": code,
                    "grant_type": "auth_code"
                },
            )
            response.raise_for_status()
            data = response.json()
            if data.get("code") != 0:
                 raise ValueError(f"TikTok error: {data.get('message')}")
            return data["data"]

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._get_base_url()}/oauth2/refresh_token/",
                json={
                    "app_id": os.environ.get("TIKTOK_APP_ID", ""),
                    "secret": os.environ.get("TIKTOK_APP_SECRET", ""),
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token"
                },
            )
            response.raise_for_status()
            data = response.json()
            if data.get("code") != 0:
                 raise ValueError(f"TikTok error: {data.get('message')}")
            return data["data"]

    async def validate_credentials(self) -> bool:
        token = self.credentials.get("access_token")
        advertiser_id = self.credentials.get("advertiser_id")
        if not (token and advertiser_id):
            return False
        
        async with httpx.AsyncClient() as client:
            headers = {"Access-Token": token}
            # Test by fetching advertiser info
            response = await client.get(
                f"{self._get_base_url()}/advertiser/info/", 
                headers=headers,
                params={"advertiser_ids": [advertiser_id]}
            )
            return response.status_code == 200

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from TikTok Marketing API.
        Supported resource_types: 'campaigns', 'ad_groups', 'insights'
        """
        token = self.credentials.get("access_token")
        advertiser_id = self.credentials.get("advertiser_id")
        headers = {"Access-Token": token}
        
        async with httpx.AsyncClient() as client:
            if resource_type == "campaigns":
                response = await client.get(
                    f"{self._get_base_url()}/campaign/get/", 
                    headers=headers,
                    params={"advertiser_id": advertiser_id}
                )
                response.raise_for_status()
                return response.json()
            
            elif resource_type == "insights":
                response = await client.get(
                    f"{self._get_base_url()}/report/integrated/get/", 
                    headers=headers,
                    params={
                        "advertiser_id": advertiser_id,
                        "report_type": "BASIC",
                        "data_level": "AUCTION_CAMPAIGN",
                        "dimensions": ["campaign_id"],
                        "start_date": params.get("start_date", "2024-01-01") if params else "2024-01-01",
                        "end_date": params.get("end_date", "2024-12-31") if params else "2024-12-31"
                    }
                )
                response.raise_for_status()
                return response.json()

        return {"error": "Unsupported resource type"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise ValueError(f"Unsupported action: {action}")
