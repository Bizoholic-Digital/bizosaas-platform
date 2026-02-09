import httpx
from typing import Dict, Any, List, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class CalendlyConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="calendly",
            name="Calendly",
            type=ConnectorType.OTHER,
            description="Automate your appointment scheduling and manage event types.",
            icon="calendar",
            version="1.0.0",
            auth_schema={
                "access_token": {"type": "string", "label": "Personal Access Token", "format": "password", "help": "Generate in Calendly > Integrations & Apps"},
                "organization_uri": {"type": "string", "label": "Organization URI", "placeholder": "https://api.calendly.com/organizations/..."}
            }
        )

    def _get_base_url(self) -> str:
        return "https://api.calendly.com"

    async def validate_credentials(self) -> bool:
        token = self.credentials.get("access_token")
        if not token:
            return False
        
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            # Test by fetching the current user
            response = await client.get(f"{self._get_base_url()}/users/me", headers=headers)
            return response.status_code == 200

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sync data from Calendly API V2.
        Supported resource_types: 'event_types', 'scheduled_events'
        """
        token = self.credentials.get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            if resource_type == "event_types":
                user_uri = params.get("user") if params else None
                if not user_uri:
                     # Fetch user URI if not provided
                     user_res = await client.get(f"{self._get_base_url()}/users/me", headers=headers)
                     user_res.raise_for_status()
                     user_uri = user_res.json()["resource"]["uri"]
                
                response = await client.get(
                    f"{self._get_base_url()}/event_types", 
                    headers=headers,
                    params={"user": user_uri}
                )
                response.raise_for_status()
                return response.json()
            
            elif resource_type == "scheduled_events":
                org_uri = self.credentials.get("organization_uri")
                if not org_uri:
                     return {"error": "organization_uri is required for events"}
                     
                response = await client.get(
                    f"{self._get_base_url()}/scheduled_events", 
                    headers=headers,
                    params={"organization": org_uri}
                )
                response.raise_for_status()
                return response.json()

        return {"error": "Unsupported resource type"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform actions on Calendly.
        """
        raise ValueError(f"Unsupported action: {action}")
