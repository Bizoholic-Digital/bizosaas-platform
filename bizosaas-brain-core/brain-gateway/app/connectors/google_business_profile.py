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

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions.
        Supported actions: 'link_location', 'reply_review'
        """
        if action == "link_location":
            location_id = payload.get("location_id")
            if not location_id:
                return {"status": "error", "message": "location_id is required"}
            self.credentials["location_id"] = location_id
            return {"status": "success", "location_id": location_id}
            
        elif action == "reply_review":
             review_id = payload.get("review_id")
             comment = payload.get("comment")
             location_id = self.credentials.get("location_id")
             
             if not (review_id and comment and location_id):
                  return {"status": "error", "message": "review_id, comment, and location_id are required"}
             
             token = await self._get_access_token()
             headers = {"Authorization": f"Bearer {token}"}
             url = f"https://mybusiness.googleapis.com/v4/{location_id}/reviews/{review_id}/reply"
             
             async with httpx.AsyncClient() as client:
                  response = await client.put(url, headers=headers, json={"comment": comment})
                  response.raise_for_status()
                  return response.json()

        raise ValueError(f"Unsupported action: {action}")
