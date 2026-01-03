import httpx
import os
from typing import Dict, Any, Optional, List
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry
from .oauth_mixin import OAuthMixin

@ConnectorRegistry.register
class GoogleTagManagerConnector(BaseConnector, OAuthMixin):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="google-tag-manager",
            name="Google Tag Manager",
            type=ConnectorType.MARKETING,
            description="Manage marketing tags via a single container with automatic discovery.",
            icon="tag",
            version="1.1.0",
            auth_schema={
                "access_token": {"type": "string", "label": "Access Token", "format": "password"},
                "refresh_token": {"type": "string", "label": "Refresh Token", "format": "password"},
                "container_id": {"type": "string", "label": "Container ID", "placeholder": "GTM-XXXXXX", "help": "Automatically detected if using Google Login"},
                "account_id": {"type": "string", "label": "Account ID", "placeholder": "accounts/123456"}
            }
        )

    async def _get_access_token(self) -> str:
        return self.credentials.get("access_token", "")

    async def validate_credentials(self) -> bool:
        # If we have a container_id and it looks like GTM-XXXX, return True for basic config
        # But if we want to check API, we need token
        token = await self._get_access_token()
        if not token:
            container_id = self.credentials.get("container_id", "")
            return container_id.startswith("GTM-")
            
        async with httpx.AsyncClient() as client:
            try:
                # Test by listing accounts
                response = await client.get(
                    "https://tagmanager.googleapis.com/tagmanager/v2/accounts",
                    headers={"Authorization": f"Bearer {token}"}
                )
                return response.status_code == 200
            except Exception:
                return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from GTM.
        resource_type: 'accounts', 'containers', 'snippets'
        """
        token = await self._get_access_token()
        if not token:
             if resource_type == "snippets":
                 return await self.perform_action("get_snippet", {})
             return {"error": "Authentication required for advanced sync"}

        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            if resource_type == "accounts":
                resp = await client.get("https://tagmanager.googleapis.com/tagmanager/v2/accounts", headers=headers)
                resp.raise_for_status()
                return resp.json()
            
            elif resource_type == "containers":
                account_id = params.get("account_id") or self.credentials.get("account_id")
                if not account_id:
                     # Get first account
                     acc_data = await self.sync_data("accounts")
                     accounts = acc_data.get("account", [])
                     if not accounts: return {"error": "No accounts found"}
                     account_id = accounts[0]["path"]
                
                url = f"https://tagmanager.googleapis.com/tagmanager/v2/{account_id}/containers"
                resp = await client.get(url, headers=headers)
                resp.raise_for_status()
                return resp.json()

        return {"error": f"Unsupported resource: {resource_type}"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if action == "get_snippet":
            container_id = self.credentials.get("container_id")
            if not container_id:
                return {"status": "error", "message": "container_id is required"}
                
            return {
                "status": "success",
                "snippets": {
                    "head": f"<!-- Google Tag Manager --><script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{container_id}');</script><!-- End Google Tag Manager -->",
                    "body": f"<!-- Google Tag Manager (noscript) --><noscript><iframe src=\"https://www.googletagmanager.com/ns.html?id={container_id}\" height=\"0\" width=\"0\" style=\"display:none;visibility:hidden\"></iframe></noscript><!-- End Google Tag Manager (noscript) -->"
                }
            }
        
        if action == "auto_link":
            # 1. Get Accounts
            acc_data = await self.sync_data("accounts")
            accounts = acc_data.get("account", [])
            if not accounts:
                return {"status": "error", "message": "No GTM accounts found."}
            
            # 2. Get Containers for first account (or search)
            account_path = accounts[0]["path"] # e.g. "accounts/123"
            self.credentials["account_id"] = account_path
            
            cont_data = await self.sync_data("containers", {"account_id": account_path})
            containers = cont_data.get("container", [])
            
            if not containers:
                return {"status": "partial_success", "message": "Linked account but no containers found.", "account_id": account_path}
            
            if len(containers) == 1:
                self.credentials["container_id"] = containers[0]["publicId"]
                return {
                    "status": "success",
                    "auto": True,
                    "container_id": containers[0]["publicId"],
                    "message": f"Successfully linked container: {containers[0].get('name')}"
                }
            
            return {
                "status": "multiple_found",
                "message": "Multiple containers found. Please select one.",
                "containers": containers
            }
        
        raise ValueError(f"Unsupported action: {action}")

    # OAuth Management
    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        scope = "https://www.googleapis.com/auth/tagmanager.readonly"
        return (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope={scope}&"
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
            return resp.json()

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
