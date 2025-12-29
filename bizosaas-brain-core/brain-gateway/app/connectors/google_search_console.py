import httpx
import os
from typing import Dict, Any, List, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry
from .oauth_mixin import OAuthMixin

@ConnectorRegistry.register
class GoogleSearchConsoleConnector(BaseConnector, OAuthMixin):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="google-search-console",
            name="Google Search Console",
            type=ConnectorType.ANALYTICS,
            description="Monitor your organic search performance, indexing status, and site health.",
            icon="search",
            version="1.0.0",
            auth_schema={
                "access_token": {"type": "string", "label": "Access Token", "format": "password"},
                "refresh_token": {"type": "string", "label": "Refresh Token", "format": "password"},
                "site_url": {"type": "string", "label": "Site URL", "placeholder": "https://example.com"}
            }
        )

    def _get_base_url(self) -> str:
        return "https://www.googleapis.com/webmasters/v3"

    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
        scopes = [
            "https://www.googleapis.com/auth/webmasters.readonly",
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

    async def validate_credentials(self) -> bool:
        token = self.credentials.get("access_token")
        if not token:
            return False
            
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            # Test by listing sites
            response = await client.get(f"{self._get_base_url()}/sites", headers=headers)
            return response.status_code == 200

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from Google Search Console API.
        Supported resource_types: 'performance', 'sites', 'sitemaps'
        """
        token = self.credentials.get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            if resource_type == "sites":
                response = await client.get(f"{self._get_base_url()}/sites", headers=headers)
                response.raise_for_status()
                return response.json()
            
            elif resource_type == "performance":
                site_url = self.credentials.get("site_url")
                if not site_url:
                     return {"error": "site_url is required for performance data"}
                
                # Performance query requires POST
                url = f"{self._get_base_url()}/sites/{site_url.replace('/', '%2F')}/searchAnalytics/query"
                response = await client.post(
                    url, 
                    headers=headers,
                    json={
                        "startDate": params.get("startDate", "30daysAgo") if params else "30daysAgo",
                        "endDate": params.get("endDate", "yesterday") if params else "yesterday",
                        "dimensions": params.get("dimensions", ["query", "page"]) if params else ["query", "page"]
                    }
                )
                response.raise_for_status()
                return response.json()
            
            elif resource_type == "sitemaps":
                site_url = self.credentials.get("site_url")
                if not site_url:
                     return {"error": "site_url is required for sitemaps"}
                     
                url = f"{self._get_base_url()}/sites/{site_url.replace('/', '%2F')}/sitemaps"
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()

        return {"error": "Unsupported resource type"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute actions on Google Search Console.
        action: 'link_site', 'auto_link'
        """
        if action == "link_site":
            site_url = payload.get("site_url")
            if not site_url:
                raise ValueError("site_url is required for link_site action")
            
            # Update credentials
            self.credentials["site_url"] = site_url
            return {
                "status": "success",
                "message": f"Successfully linked site {site_url}",
                "site_url": site_url
            }

        if action == "auto_link":
            # 1. Discover sites
            data = await self.sync_data("sites")
            sites = data.get("siteEntry", [])
            
            if not sites:
                return {"status": "error", "message": "No sites found in Google Search Console."}
                
            if len(sites) == 1:
                site_url = sites[0]["siteUrl"]
                self.credentials["site_url"] = site_url
                return {
                    "status": "success",
                    "auto": True,
                    "message": f"Automatically linked site: {site_url}",
                    "site_url": site_url
                }
            
            # Filter for site_url if provided in payload (e.g. from onboarding website profile)
            target_url = payload.get("target_url")
            if target_url:
                for site in sites:
                    if target_url in site["siteUrl"]:
                        self.credentials["site_url"] = site["siteUrl"]
                        return {
                            "status": "success",
                            "auto": True,
                            "message": f"Linked matching site: {site['siteUrl']}",
                            "site_url": site["siteUrl"]
                        }

            return {
                "status": "multiple_found",
                "message": "Multiple sites found. Please select one manually.",
                "sites": sites
            }
            
        raise NotImplementedError(f"Action {action} not implemented for Google Search Console")
