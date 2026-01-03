import httpx
import os
import time
from typing import Dict, Any, List, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .oauth_mixin import OAuthMixin
from .registry import ConnectorRegistry

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
            version="1.1.0",
            auth_schema={
                "access_token": {"type": "string", "label": "Access Token", "format": "password", "hidden": True},
                "refresh_token": {"type": "string", "label": "Refresh Token", "format": "password", "hidden": True},
                "expires_at": {"type": "number", "label": "Expires At", "hidden": True},
                "location_id": {"type": "string", "label": "Location ID", "placeholder": "locations/123456"},
                "account_id": {"type": "string", "label": "Account ID", "placeholder": "accounts/123456"}
            }
        )

    def _get_base_url(self) -> str:
        return "https://mybusinessbusinessinformation.googleapis.com/v1"

    def _get_account_url(self) -> str:
         return "https://mybusinessaccountmanagement.googleapis.com/v1"

    async def _get_access_token(self) -> str:
        """
        Retrieves a valid access token, refreshing if necessary.
        """
        access_token = self.credentials.get("access_token")
        refresh_token = self.credentials.get("refresh_token")
        expires_at = self.credentials.get("expires_at", 0)

        # Refresh if expired or about to expire
        if refresh_token and (not access_token or time.time() > (expires_at - 60)):
            try:
                token_data = await self.refresh_token(refresh_token)
                self.credentials["access_token"] = token_data.get("access_token")
                if "expires_in" in token_data:
                    self.credentials["expires_at"] = int(time.time()) + token_data["expires_in"]
                return self.credentials["access_token"]
            except Exception as e:
                self.logger.error(f"Failed to refresh GBP token: {e}")
        
        if not access_token:
            raise ValueError("No valid OAuth session. Please reconnect Google Business Profile.")
            
        return access_token

    async def validate_credentials(self) -> bool:
        try:
            token = await self._get_access_token()
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {token}"}
                # Test by listing accounts
                response = await client.get(f"{self._get_account_url()}/accounts", headers=headers)
                return response.status_code == 200
        except Exception:
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            if not self.credentials.get("location_id"):
                return ConnectorStatus.DEGRADED
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
                    # Discover accounts
                    accounts_data = await self.sync_data("accounts")
                    accounts = accounts_data.get("accounts", [])
                    if not accounts:
                         return {"error": "No accounts found"}
                    account_id = accounts[0]["name"]

                response = await client.get(
                    f"{self._get_base_url()}/{account_id}/locations", 
                    headers=headers,
                    params={"readMask": "name,title,storefrontAddress,categories,regularHours"}
                )
                response.raise_for_status()
                return response.json()

            elif resource_type == "reviews":
                location_id = self.credentials.get("location_id")
                if not location_id:
                    raise ValueError("location_id is required to fetch reviews")
                
                # Use My Business API v4 for reviews (legacy but still common for reviews)
                url = f"https://mybusiness.googleapis.com/v4/{location_id}/reviews"
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()

        return {"error": f"Unsupported resource type: {resource_type}"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if action == "auto_link":
            token = await self._get_access_token()
            headers = {"Authorization": f"Bearer {token}"}
            
            # 1. Get Accounts
            acc_resp = await self.sync_data("accounts")
            accounts = acc_resp.get("accounts", [])
            if not accounts:
                return {"status": "error", "message": "No Google Business accounts found."}
            
            # 2. Find Locations across all accounts
            all_locations = []
            for acc in accounts:
                async with httpx.AsyncClient() as client:
                    loc_resp = await client.get(
                        f"{self._get_base_url()}/{acc['name']}/locations",
                        headers=headers,
                        params={"readMask": "name,title,storefrontAddress"}
                    )
                    if loc_resp.status_code == 200:
                        locs = loc_resp.json().get("locations", [])
                        for l in locs:
                            all_locations.append({
                                "account_id": acc["name"],
                                "location_id": l["name"],
                                "title": l["title"],
                                "address": l.get("storefrontAddress")
                            })

            if not all_locations:
                return {"status": "error", "message": "No locations discovered."}

            # 3. Auto-link if exactly one, or search by name
            target_name = payload.get("target_name")
            if target_name:
                for loc in all_locations:
                    if target_name.lower() in loc["title"].lower():
                        self.credentials["account_id"] = loc["account_id"]
                        self.credentials["location_id"] = loc["location_id"]
                        return {"status": "success", "message": f"Linked: {loc['title']}", "location": loc}

            if len(all_locations) == 1:
                loc = all_locations[0]
                self.credentials["account_id"] = loc["account_id"]
                self.credentials["location_id"] = loc["location_id"]
                return {"status": "success", "message": f"Automatically linked: {loc['title']}", "location": loc}

            return {
                "status": "multiple_found",
                "locations": all_locations
            }

        raise NotImplementedError(f"Action {action} not implemented for GBP")

    # OAuthMixin Implementation
    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        scopes = [
            "https://www.googleapis.com/auth/business.manage",
            "openid", "email", "profile"
        ]
        return (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope={' '.join(scopes)}&"
            f"state={state}&"
            f"access_type=offline&"
            f"prompt=consent"
        )
    
    async def exchange_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, data=data)
            resp.raise_for_status()
            token_data = resp.json()
            if "expires_in" in token_data:
                token_data["expires_at"] = int(time.time()) + token_data["expires_in"]
            return token_data
    
    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        url = "https://oauth2.googleapis.com/token"
        data = {
            "refresh_token": refresh_token,
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "grant_type": "refresh_token"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, data=data)
            resp.raise_for_status()
            return resp.json()
