import httpx
from typing import Dict, Any, List, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class TwilioConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="twilio",
            name="Twilio",
            type=ConnectorType.OTHER,
            description="Send SMS and WhatsApp messages to your leads and customers.",
            icon="message-square",
            version="1.0.0",
            auth_schema={
                "account_sid": {"type": "string", "label": "Account SID", "placeholder": "AC..."},
                "auth_token": {"type": "string", "label": "Auth Token", "format": "password"},
                "from_number": {"type": "string", "label": "Twilio Phone Number", "placeholder": "+1234567890"}
            }
        )

    def _get_base_url(self) -> str:
        account_sid = self.credentials.get("account_sid")
        return f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}"

    async def validate_credentials(self) -> bool:
        account_sid = self.credentials.get("account_sid")
        auth_token = self.credentials.get("auth_token")
        if not (account_sid and auth_token):
            return False
        
        async with httpx.AsyncClient() as client:
            # Test by fetching account details
            response = await client.get(
                f"{self._get_base_url()}.json",
                auth=(account_sid, auth_token)
            )
            return response.status_code == 200

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from Twilio API.
        Supported resource_types: 'messages', 'usage'
        """
        account_sid = self.credentials.get("account_sid")
        auth_token = self.credentials.get("auth_token")
        
        async with httpx.AsyncClient() as client:
            if resource_type == "messages":
                response = await client.get(
                    f"{self._get_base_url()}/Messages.json", 
                    auth=(account_sid, auth_token),
                    params={"PageSize": 20}
                )
                response.raise_for_status()
                return response.json()
            
            elif resource_type == "usage":
                response = await client.get(
                    f"{self._get_base_url()}/Usage/Records.json", 
                    auth=(account_sid, auth_token)
                )
                response.raise_for_status()
                return response.json()

        return {"error": "Unsupported resource type"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions on Twilio.
        Supported actions: 'send_sms'
        """
        account_sid = self.credentials.get("account_sid")
        auth_token = self.credentials.get("auth_token")
        from_number = self.credentials.get("from_number")

        if action == "send_sms":
            to_number = payload.get("to")
            body = payload.get("body")
            if not (to_number and body):
                 return {"status": "error", "message": "to and body are required"}
                 
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._get_base_url()}/Messages.json",
                    auth=(account_sid, auth_token),
                    data={
                        "To": to_number,
                        "From": from_number,
                        "Body": body
                    }
                )
                response.raise_for_status()
                return response.json()

        raise ValueError(f"Unsupported action: {action}")
