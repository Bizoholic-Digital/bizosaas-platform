import httpx
from typing import Dict, Any, List, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class MailchimpConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="mailchimp",
            name="Mailchimp",
            type=ConnectorType.MARKETING,
            description="Manage your email subscribers, audiences, and campaign performance.",
            icon="mail",
            version="1.0.0",
            auth_schema={
                "api_key": {"type": "string", "label": "API Key", "format": "password"},
                "server_prefix": {"type": "string", "label": "Server Prefix", "placeholder": "e.g., us20"},
                "list_id": {"type": "string", "label": "Audience ID", "placeholder": "Optional (for default list)"}
            }
        )

    def _get_base_url(self) -> str:
        server = self.credentials.get("server_prefix", "us1")
        return f"https://{server}.api.mailchimp.com/3.0"

    async def validate_credentials(self) -> bool:
        api_key = self.credentials.get("api_key")
        if not api_key:
            return False
        
        async with httpx.AsyncClient() as client:
            # Test by fetching account info
            response = await client.get(
                f"{self._get_base_url()}/", 
                auth=("user", api_key)
            )
            return response.status_code == 200

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from Mailchimp API v3.0.
        Supported resource_types: 'lists', 'members', 'campaigns'
        """
        api_key = self.credentials.get("api_key")
        
        async with httpx.AsyncClient() as client:
            if resource_type == "lists":
                response = await client.get(f"{self._get_base_url()}/lists", auth=("user", api_key))
                response.raise_for_status()
                return response.json()
            
            elif resource_type == "members":
                list_id = params.get("list_id") or self.credentials.get("list_id")
                if not list_id:
                     return {"error": "list_id is required for members"}
                
                response = await client.get(
                    f"{self._get_base_url()}/lists/{list_id}/members", 
                    auth=("user", api_key)
                )
                response.raise_for_status()
                return response.json()
            
            elif resource_type == "campaigns":
                response = await client.get(f"{self._get_base_url()}/campaigns", auth=("user", api_key))
                response.raise_for_status()
                return response.json()

        return {"error": "Unsupported resource type"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions on Mailchimp.
        Supported actions: 'add_member'
        """
        api_key = self.credentials.get("api_key")
        
        if action == "add_member":
            list_id = payload.get("list_id") or self.credentials.get("list_id")
            email = payload.get("email")
            if not (list_id and email):
                 return {"status": "error", "message": "list_id and email are required"}
                 
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._get_base_url()}/lists/{list_id}/members",
                    auth=("user", api_key),
                    json={
                        "email_address": email,
                        "status": payload.get("status", "subscribed"),
                        "merge_fields": payload.get("merge_fields", {})
                    }
                )
                response.raise_for_status()
                return response.json()

        raise ValueError(f"Unsupported action: {action}")
