import httpx
from typing import Dict, Any, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

from .oauth_mixin import OAuthMixin
import os

@ConnectorRegistry.register
class GoogleTagManagerConnector(BaseConnector, OAuthMixin):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="google-tag-manager",
            name="Google Tag Manager",
            type=ConnectorType.MARKETING,
            description="Manage marketing tags (GA4, Ads, FB Pixel) via a single container.",
            icon="tag",
            version="1.1.0",
            auth_schema={
                "container_id": {"type": "string", "label": "Container ID", "placeholder": "GTM-XXXXXX"},
                "account_id": {"type": "string", "label": "Account ID"},
                "access_token": {"type": "string", "label": "Access Token", "format": "password"}
            }
        )

    async def _get_access_token(self) -> str:
        # Simplistic token retrieval for now
        return self.credentials.get("access_token")

    async def validate_credentials(self) -> bool:
        container_id = self.credentials.get("container_id", "")
        if not container_id.startswith("GTM-"):
            return False
        return True

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from GTM.
        Supported resource_types: 'accounts', 'containers', 'tags'
        """
        token = await self._get_access_token()
        if not token:
             return {"status": "error", "message": "No access token"}

        async with httpx.AsyncClient() as client:
            if resource_type == 'accounts':
                url = "https://www.googleapis.com/tagmanager/v2/accounts"
                resp = await client.get(url, headers={"Authorization": f"Bearer {token}"})
                return resp.json()
            
            if resource_type == 'containers':
                account_id = self.credentials.get("account_id")
                if not account_id:
                     # Attempt to find first account if not set
                     accounts_data = await self.sync_data("accounts")
                     accounts = accounts_data.get("account", [])
                     if not accounts: return {"containers": []}
                     account_id = accounts[0]["accountId"]
                
                url = f"https://www.googleapis.com/tagmanager/v2/accounts/{account_id}/containers"
                resp = await client.get(url, headers={"Authorization": f"Bearer {token}"})
                return resp.json()

            if resource_type == 'tags':
                account_id = self.credentials.get("account_id")
                container_id = self.credentials.get("container_id") # This usually needs path format or specific ID
                # GTM API often uses paths like accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/tags
                # For simplicity, we'll assume latest workspace if not specified, but the path is needed.
                path = params.get("path") if params else None
                if not path:
                     return {"error": "Workspace path is required for tags"}

                url = f"https://www.googleapis.com/tagmanager/v2/{path}/tags"
                resp = await client.get(url, headers={"Authorization": f"Bearer {token}"})
                return resp.json()

        return {"status": "unsupported_resource", "resource": resource_type}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions.
        Supported actions: 'get_snippet', 'auto_link'
        """
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
            # Discover first container
            data = await self.sync_data("containers")
            containers = data.get("container", [])
            if not containers:
                return {"status": "error", "message": "No GTM containers found"}
            
            if len(containers) == 1:
                container = containers[0]
                self.credentials["container_id"] = container["publicId"]
                self.credentials["account_id"] = container["accountId"]
                
                return {
                    "status": "success",
                    "message": f"Successfully linked container: {container['name']}",
                    "container_id": container["publicId"]
                }
            
            return {
                "status": "multiple_found",
                "message": "Multiple GTM containers found. Please select one manually.",
                "containers": containers
            }
        
        raise ValueError(f"Unsupported action: {action}")

    # OAuth Methods
    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        # Added .edit.containers scope to allow provisioning of tags as required by the GTM-first strategy
        scopes = [
            "https://www.googleapis.com/auth/tagmanager.readonly",
            "https://www.googleapis.com/auth/tagmanager.edit.containers"
        ]
        scope_str = "%20".join(scopes)
        return f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope_str}&state={state}&access_type=offline&prompt=consent"

    async def exchange_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        url = "https://oauth2.googleapis.com/token"
        data = {"code": code, "client_id": os.getenv("GOOGLE_CLIENT_ID"), "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"), "redirect_uri": redirect_uri, "grant_type": "authorization_code"}
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, data=data)
            resp.raise_for_status()
            return resp.json()
