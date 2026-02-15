import httpx
from typing import Dict, Any, Optional, List
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class SlackConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="slack",
            name="Slack",
            type=ConnectorType.COMMUNICATION,
            description="Sync channels and messages. Post notifications and automate Slack workflows.",
            icon="slack",
            version="1.0.0",
            auth_schema={
                "bot_token": {"type": "string", "label": "Bot User OAuth Token", "format": "password", "help": "Starts with xoxb-"},
                "app_token": {"type": "string", "label": "App-Level Token", "format": "password", "help": "Starts with xapp- (optional)"}
            }
        )

    def _get_headers(self) -> Dict[str, str]:
        token = self.credentials.get("bot_token")
        if not token:
            raise ValueError("Missing Slack Bot Token")
        return {"Authorization": f"Bearer {token}"}

    async def validate_credentials(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://slack.com/api/auth.test",
                    headers=self._get_headers(),
                    timeout=10.0
                )
                data = response.json()
                return data.get("ok", False)
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from Slack.
        Supported resource_types: 'channels', 'messages', 'users'
        """
        params = params or {}
        
        if resource_type.lower() == 'channels':
            url = "https://slack.com/api/conversations.list"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self._get_headers(), params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                if not data.get("ok"):
                    raise ValueError(f"Slack API error: {data.get('error')}")
                return {"data": data.get("channels", []), "meta": data.get("response_metadata", {})}

        if resource_type.lower() == 'messages':
            channel_id = params.get("channel_id")
            if not channel_id:
                raise ValueError("channel_id is required to sync messages")
            url = "https://slack.com/api/conversations.history"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self._get_headers(), params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                if not data.get("ok"):
                    raise ValueError(f"Slack API error: {data.get('error')}")
                return {"data": data.get("messages", []), "meta": data.get("response_metadata", {})}

        if resource_type.lower() == 'users':
            url = "https://slack.com/api/users.list"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self._get_headers(), params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                if not data.get("ok"):
                    raise ValueError(f"Slack API error: {data.get('error')}")
                return {"data": data.get("members", []), "meta": data.get("response_metadata", {})}

        raise NotImplementedError(f"Resource type {resource_type} not supported for Slack")

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions on Slack.
        Supported actions: 'post_message', 'create_channel'
        """
        if action == "post_message":
            url = "https://slack.com/api/chat.postMessage"
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=self._get_headers(), json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                if not data.get("ok"):
                    raise ValueError(f"Slack API error: {data.get('error')}")
                return {"status": "success", "data": data}

        if action == "create_channel":
            url = "https://slack.com/api/conversations.create"
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=self._get_headers(), json={"name": payload.get("name")}, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                if not data.get("ok"):
                    raise ValueError(f"Slack API error: {data.get('error')}")
                return {"status": "success", "data": data}

        raise NotImplementedError(f"Action {action} not supported for Slack")
