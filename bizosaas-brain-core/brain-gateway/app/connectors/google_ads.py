import httpx
from typing import Dict, Any, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

from .oauth_mixin import OAuthMixin
import os
import time

@ConnectorRegistry.register
class GoogleAdsConnector(BaseConnector, OAuthMixin):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="google-ads",
            name="Google Ads",
            type=ConnectorType.MARKETING,
            description="Manage ad campaigns, track conversions, and optimize spend.",
            icon="monitor",
            version="2.0.0",
            auth_schema={
                "access_token": {"type": "string", "label": "Access Token", "format": "password"},
                "refresh_token": {"type": "string", "label": "Refresh Token", "format": "password"},
                "customer_id": {"type": "string", "label": "Customer ID (Manager)", "placeholder": "123-456-7890"},
                "client_customer_id": {"type": "string", "label": "Client Customer ID", "placeholder": "123-456-7890"},
                "developer_token": {"type": "string", "label": "Developer Token", "format": "password"}
            }
        )

    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
        scopes = ["https://www.googleapis.com/auth/adwords", "openid", "email", "profile"]
        scope_str = "%20".join(scopes)
        return (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope={scope_str}&"
            f"state={state}&"
            f"access_type=offline&"
            f"prompt=consent"
        )

    async def exchange_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": os.environ.get("GOOGLE_CLIENT_ID", ""),
                    "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET", ""),
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                },
            )
            response.raise_for_status()
            return response.json()

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "refresh_token": refresh_token,
                    "client_id": os.environ.get("GOOGLE_CLIENT_ID", ""),
                    "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET", ""),
                    "grant_type": "refresh_token",
                },
            )
            response.raise_for_status()
            return response.json()

    def _get_api_url(self) -> str:
        return "https://googleads.googleapis.com/v14/customers"

    async def validate_credentials(self) -> bool:
        token = self.credentials.get("access_token")
        dev_token = self.credentials.get("developer_token")
        customer_id = self.credentials.get("customer_id")
        
        if not (token and dev_token and customer_id):
            return False
            
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {token}",
                "developer-token": dev_token,
                "login-customer-id": customer_id.replace("-", "")
            }
            # Simple ping to list accessible customers
            response = await client.get("https://googleads.googleapis.com/v14/customers:listAccessibleCustomers", headers=headers)
            return response.status_code == 200

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from Google Ads API.
        Supported resource_types: 'campaigns', 'performance'
        """
        token = self.credentials.get("access_token")
        dev_token = self.credentials.get("developer_token")
        customer_id = self.credentials.get("client_customer_id") or self.credentials.get("customer_id")
        customer_id = customer_id.replace("-", "")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "developer-token": dev_token,
            "login-customer-id": self.credentials.get("customer_id", "").replace("-", "")
        }
        
        async with httpx.AsyncClient() as client:
            if resource_type == "campaigns":
                query = "SELECT campaign.id, campaign.name, campaign.status FROM campaign"
                url = f"{self._get_api_url()}/{customer_id}/googleAds:search"
                response = await client.post(url, headers=headers, json={"query": query})
                response.raise_for_status()
                return response.json()
            
            elif resource_type == "performance":
                query = "SELECT metrics.clicks, metrics.impressions, metrics.cost_micros FROM campaign"
                url = f"{self._get_api_url()}/{customer_id}/googleAds:search"
                response = await client.post(url, headers=headers, json={"query": query})
                response.raise_for_status()
                return response.json()

        return {"error": "Unsupported resource type"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute actions on Google Ads.
        action: 'auto_link'
        """
        if action == "auto_link":
            token = self.credentials.get("access_token")
            dev_token = self.credentials.get("developer_token")
            
            if not token or not dev_token:
                return {"status": "error", "message": "Missing access_token or developer_token"}
            
            headers = {
                "Authorization": f"Bearer {token}",
                "developer-token": dev_token,
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get("https://googleads.googleapis.com/v14/customers:listAccessibleCustomers", headers=headers)
                response.raise_for_status()
                data = response.json()
                
                customers = data.get("resourceNames", [])
                if not customers:
                    return {"status": "error", "message": "No Google Ads accounts found."}
                
                if len(customers) == 1:
                    customer_resource = customers[0]
                    customer_id = customer_resource.split("/")[-1]
                    self.credentials["customer_id"] = customer_id
                    self.credentials["client_customer_id"] = customer_id
                    return {
                        "status": "success",
                        "auto": True,
                        "message": f"Automatically linked Ads account: {customer_id}",
                        "customer_id": customer_id
                    }
                
                return {
                    "status": "multiple_found",
                    "message": "Multiple Google Ads accounts found.",
                    "accounts": customers
                }

        raise ValueError(f"Unsupported action: {action}")
