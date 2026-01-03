import httpx
import os
import time
from typing import Dict, Any, Optional, List
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .oauth_mixin import OAuthMixin
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class GoogleAnalyticsConnector(BaseConnector, OAuthMixin):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="google-analytics",
            name="Google Analytics 4",
            type=ConnectorType.ANALYTICS,
            description="Track website traffic, user behavior, and conversion metrics.",
            icon="google-analytics",
            version="1.1.0",
            auth_schema={
                "access_token": {"type": "string", "label": "Access Token", "format": "password", "hidden": True},
                "refresh_token": {"type": "string", "label": "Refresh Token", "format": "password", "hidden": True},
                "expires_at": {"type": "number", "label": "Expires At", "hidden": True},
                "property_id": {"type": "string", "label": "GA4 Property ID", "placeholder": "properties/123456789"}
            }
        )

    async def _get_access_token(self) -> str:
        """
        Retrieves a valid access token, refreshing if necessary.
        """
        access_token = self.credentials.get("access_token")
        refresh_token = self.credentials.get("refresh_token")
        expires_at = self.credentials.get("expires_at", 0)

        # Refresh if expired or about to expire (within 60 seconds)
        if refresh_token and (not access_token or time.time() > (expires_at - 60)):
            try:
                token_data = await self.refresh_token(refresh_token)
                self.credentials["access_token"] = token_data.get("access_token")
                # Update expires_at if provided by Google (typically 3600s)
                if "expires_in" in token_data:
                    self.credentials["expires_at"] = int(time.time()) + token_data["expires_in"]
                
                # Note: In a real production system, we would trigger a callback here 
                # to persist the updated credentials to the database.
                return self.credentials["access_token"]
            except Exception as e:
                self.logger.error(f"Failed to refresh Google Analytics token: {e}")
        
        if not access_token:
            raise ValueError("No valid OAuth session found. Please reconnect.")
            
        return access_token

    async def validate_credentials(self) -> bool:
        try:
            token = await self._get_access_token()
            # Try to list accounts as a validation check
            url = "https://analyticsadmin.googleapis.com/v1beta/accountSummaries"
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            self.logger.error(f"GA4 Validation failed: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            if not self.credentials.get("property_id"):
                return ConnectorStatus.DEGRADED # Connected but needs configuration
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Fetch reports or metadata from GA4.
        resource_type: 'basic_report', 'properties', 'accounts'
        """
        token = await self._get_access_token()
        
        if resource_type == 'properties' or resource_type == 'list_properties':
            url = "https://analyticsadmin.googleapis.com/v1beta/properties"
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, headers={"Authorization": f"Bearer {token}"})
                resp.raise_for_status()
                return resp.json()

        if resource_type == 'accounts':
            url = "https://analyticsadmin.googleapis.com/v1beta/accountSummaries"
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, headers={"Authorization": f"Bearer {token}"})
                resp.raise_for_status()
                return resp.json()

        # GA4 Report
        property_id = self.credentials.get("property_id")
        if not property_id:
             raise ValueError("property_id is required for reports. Run 'auto_link' first.")
             
        # Standardize property_id (ensure it has properties/ prefix if needed)
        full_property_id = property_id if property_id.startswith("properties/") else f"properties/{property_id}"
        
        url = f"https://analyticsdata.googleapis.com/v1beta/{full_property_id}:runReport"
        
        # Default report request
        report_request = {
            "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
            "dimensions": [{"name": "date"}],
            "metrics": [{"name": "activeUsers"}, {"name": "sessions"}, {"name": "screenPageViews"}]
        }
        
        if params and "request_body" in params:
            report_request = params["request_body"]

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers={"Authorization": f"Bearer {token}"},
                json=report_request,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute actions on Google Analytics.
        action: 'auto_link', 'set_property'
        """
        if action == "set_property":
            property_id = payload.get("property_id")
            if not property_id:
                raise ValueError("property_id is required")
            self.credentials["property_id"] = property_id
            return {"status": "success", "property_id": property_id}

        if action == "auto_link":
            # Discover first available property
            # First, check accountSummaries to find properties more easily
            token = await self._get_access_token()
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    "https://analyticsadmin.googleapis.com/v1beta/accountSummaries",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if resp.status_code != 200:
                    return {"status": "error", "message": "Failed to fetch account summaries"}
                
                summaries = resp.json().get("accountSummaries", [])
                discovered_properties = []
                
                for account in summaries:
                    for prop in account.get("propertySummaries", []):
                        discovered_properties.append({
                            "id": prop["property"],
                            "name": prop["displayName"]
                        })
                
                if not discovered_properties:
                    return {"status": "error", "message": "No GA4 properties found in this account."}
                
                # Auto-select the first one if only one, or return list
                if len(discovered_properties) == 1 or payload.get("force_first"):
                    prop = discovered_properties[0]
                    self.credentials["property_id"] = prop["id"]
                    return {
                        "status": "success",
                        "message": f"Successfully linked property: {prop['name']}",
                        "property_id": prop["id"]
                    }
                
                return {
                    "status": "multiple_found",
                    "properties": discovered_properties
                }
            
        raise NotImplementedError(f"Action {action} not implemented for GA4")

    # OAuthMixin Implementation
    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        scopes = [
            "https://www.googleapis.com/auth/analytics.readonly",
            "https://www.googleapis.com/auth/analytics.edit" # Needed for some management tasks
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
            # Calculate expiry
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
