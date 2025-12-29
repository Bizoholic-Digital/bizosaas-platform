import httpx
import time
from typing import Dict, Any, List, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry
from .oauth_mixin import OAuthMixin
import os

@ConnectorRegistry.register
class GoogleBusinessProfileConnector(BaseConnector, OAuthMixin):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="google-business-profile",
            name="Google Business Profile",
            type=ConnectorType.OTHER,
            description="Manage your local business presence, reviews, and posts on Google.",
            icon="map-pin",
            version="1.0.0",
            auth_schema={
                "access_token": {"type": "string", "label": "Access Token", "format": "password"},
                "refresh_token": {"type": "string", "label": "Refresh Token", "format": "password"},
                "location_id": {"type": "string", "label": "Location ID", "placeholder": "locations/123456"},
                "account_id": {"type": "string", "label": "Account ID", "placeholder": "accounts/123456"}
            }
        )

    def _get_base_url(self) -> str:
        return "https://mybusinessbusinessinformation.googleapis.com/v1"

    def _get_account_url(self) -> str:
         return "https://mybusinessaccountmanagement.googleapis.com/v1"

    def _get_reviews_url(self) -> str:
        return "https://mybusinessnotifications.googleapis.com/v1"

    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
        scopes = [
            "https://www.googleapis.com/auth/business.manage",
            "openid",
            "email",
            "profile"
        ]
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

    async def _get_access_token(self) -> str:
        # Check if current token is valid (this is a simplified logic)
        # In a real app we'd check expiry
        return self.credentials.get("access_token", "")

    async def validate_credentials(self) -> bool:
        token = await self._get_access_token()
        if not token:
            return False
        
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            # Test by listing accounts
            response = await client.get(f"{self._get_account_url()}/accounts", headers=headers)
            return response.status_code == 200

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from GBP API.
        Supported resource_types: 'locations', 'reviews', 'accounts'
        """
        token = await self._get_access_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            if resource_type == "accounts":
                response = await client.get(f"{self._get_account_url()}/accounts", headers=headers)
                response.raise_for_status()
                return response.json()
            
            elif resource_type == "locations":
                account_id = self.credentials.get("account_id")
                if not account_id:
                    # Fallback: find first account
                    accounts = await self.sync_data("accounts")
                    if not accounts.get("accounts"):
                         return {"error": "No accounts found"}
                    account_id = accounts["accounts"][0]["name"]

                response = await client.get(
                    f"{self._get_base_url()}/{account_id}/locations", 
                    headers=headers,
                    params={"readMask": "name,title,storeCode"}
                )
                response.raise_for_status()
                return response.json()

            elif resource_type == "reviews":
                location_id = self.credentials.get("location_id")
                if not location_id:
                    return {"error": "location_id is required to fetch reviews"}
                
                # Reviews are under a different base URL
                url = f"https://mybusiness.googleapis.com/v4/{location_id}/reviews"
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()

        return {"error": "Unsupported resource type"}

        elif action == "auto_link":
            # 1. Discover accounts
            data = await self.sync_data("accounts")
            accounts = data.get("accounts", [])
            
            if not accounts:
                return {"status": "error", "message": "No Google Business accounts found."}
                
            # If multiple accounts, we might need to iterate. For auto-link, we try the first one or target name.
            account_id = accounts[0]["name"]
            self.credentials["account_id"] = account_id
            
            # 2. Discover locations for this account
            loc_data = await self.sync_data("locations")
            locations = loc_data.get("locations", [])
            
            if not locations:
                 return {"status": "partial_success", "message": f"Linked account {account_id} but no locations found.", "account_id": account_id}
            
            if len(locations) == 1:
                location_id = locations[0]["name"]
                self.credentials["location_id"] = location_id
                return {
                    "status": "success",
                    "auto": True,
                    "message": f"Automatically linked location: {locations[0].get('title')}",
                    "account_id": account_id,
                    "location_id": location_id
                }
            
            # Match by title if provided
            target_name = payload.get("target_name")
            if target_name:
                for loc in locations:
                    if target_name.lower() in loc.get("title", "").lower():
                        self.credentials["location_id"] = loc["name"]
                        return {
                            "status": "success",
                            "auto": True,
                            "message": f"Linked matching location: {loc.get('title')}",
                            "account_id": account_id,
                            "location_id": loc["name"]
                        }

            return {
                "status": "multiple_found",
                "message": "Multiple locations found. Please select one manually.",
                "account_id": account_id,
                "locations": locations
            }

        raise ValueError(f"Unsupported action: {action}")
