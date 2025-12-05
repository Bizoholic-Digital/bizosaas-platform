import httpx
from typing import Dict, Any, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class TelegramConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="telegram",
            name="Telegram Bot",
            type=ConnectorType.COMMUNICATION,
            description="Send notifications and interact via Telegram bots.",
            icon="send",
            version="1.0.0",
            auth_schema={
                "bot_token": {"type": "string", "label": "Bot Token", "format": "password", "help": "From @BotFather"}
            }
        )

    def _get_api_url(self) -> str:
        return f"https://api.telegram.org/bot{self.credentials.get('bot_token')}"

    async def validate_credentials(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self._get_api_url()}/getMe", timeout=10.0)
                return response.status_code == 200
        except Exception:
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data (limited for polling bots, mostly used for Webhook info).
        """
        if resource_type == "webhook_info":
             async with httpx.AsyncClient() as client:
                response = await client.get(f"{self._get_api_url()}/getWebhookInfo")
                return {"data": response.json()}
        return {"data": [], "meta": {"resource": resource_type, "status": "not_supported"}}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Supported actions: 'send_message'
        """
        if action == "send_message":
            chat_id = payload.get("chat_id")
            text = payload.get("text")
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self._get_api_url()}/sendMessage",
                        json={"chat_id": chat_id, "text": text},
                        timeout=30.0
                    )
                    return response.json()
            except Exception as e:
                self.logger.error(f"Telegram send failed: {e}")
                raise
        
        raise ValueError(f"Unsupported action: {action}")
