import httpx
from typing import Dict, Any, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class WhatsAppConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="whatsapp",
            name="WhatsApp Business",
            type=ConnectorType.COMMUNICATION,
            description="Send messages and notifications to customers.",
            icon="message-circle",
            version="1.0.0",
            auth_schema={
                "access_token": {"type": "string", "label": "System User Access Token", "format": "password"},
                "phone_number_id": {"type": "string", "label": "Phone Number ID", "placeholder": "1234567890"},
                "waba_id": {"type": "string", "label": "WhatsApp Business Account ID", "placeholder": "Optional"}
            }
        )

    def _get_api_url(self) -> str:
        return "https://graph.facebook.com/v17.0"

    async def validate_credentials(self) -> bool:
        # Basic check
        return bool(self.credentials.get("access_token") and self.credentials.get("phone_number_id"))

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data.
        Supported resource_types: 'templates'
        """
        if resource_type == "templates":
            waba_id = self.credentials.get("waba_id")
            if not waba_id:
                return {"data": [], "error": "WABA ID required for templates"}
                
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{self._get_api_url()}/{waba_id}/message_templates",
                        headers={"Authorization": f"Bearer {self.credentials.get('access_token')}"},
                        timeout=30.0
                    )
                    return {"data": response.json().get("data", [])}
            except Exception as e:
                self.logger.error(f"WhatsApp sync failed: {e}")
                return {"data": [], "error": str(e)}

        return {"data": [], "meta": {"resource": resource_type, "status": "not_supported"}}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions.
        Supported actions: 'send_message'
        """
        if action == "send_message":
            phone_id = self.credentials.get("phone_number_id")
            to = payload.get("to")
            template = payload.get("template_name")
            language = payload.get("language_code", "en_US")
            
            # Simple template message structure
            message_payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "template",
                "template": {
                    "name": template,
                    "language": {
                        "code": language
                    }
                }
            }
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self._get_api_url()}/{phone_id}/messages",
                        headers={
                            "Authorization": f"Bearer {self.credentials.get('access_token')}",
                            "Content-Type": "application/json"
                        },
                        json=message_payload,
                        timeout=30.0
                    )
                    return response.json()
            except Exception as e:
                self.logger.error(f"Send message failed: {e}")
                raise
        
        raise ValueError(f"Unsupported action: {action}")
