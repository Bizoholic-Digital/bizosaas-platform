import httpx
import logging
from typing import Dict, Any, List, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry
from app.ports.crm_port import CRMPort, Contact, Deal, CRMStats

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class DjangoCRMConnector(BaseConnector, CRMPort):
    """
    Django CRM Connector for BizOSaaS.
    Integrates with the Django-based CRM service.
    """

    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="django_crm",
            name="Django CRM",
            type=ConnectorType.CRM,
            description="Enterprise CRM built with Django. Manages leads, contacts, and deals.",
            icon="users",
            auth_schema={
                "type": "object",
                "properties": {
                    "base_url": {"type": "string", "title": "CRM URL", "placeholder": "https://crm.bizoholic.net"},
                    "api_key": {"type": "string", "title": "API Key", "format": "password"}
                },
                "required": ["base_url", "api_key"]
            }
        )

    async def validate_credentials(self) -> bool:
        try:
            base_url = self.credentials.get("base_url").rstrip('/')
            api_key = self.credentials.get("api_key")
            headers = {"Authorization": f"Token {api_key}"}
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{base_url}/api/auth/status/", headers=headers)
                return response.status_code == 200
        except Exception:
            return False

    async def get_status(self) -> ConnectorStatus:
        is_valid = await self.validate_credentials()
        return ConnectorStatus.CONNECTED if is_valid else ConnectorStatus.ERROR

    async def get_stats(self) -> CRMStats:
        # Mocking for now, in reality call /api/stats/
        return CRMStats(contacts=150, leads=45, campaigns=12, last_sync="2024-02-03T10:00:00Z")

    async def get_contacts(self, limit: int = 100, cursor: Optional[str] = None) -> List[Contact]:
        base_url = self.credentials.get("base_url").rstrip('/')
        api_key = self.credentials.get("api_key")
        headers = {"Authorization": f"Token {api_key}"}
        
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(f"{base_url}/api/contacts/", headers=headers, params={"limit": limit})
            if response.status_code == 200:
                data = response.json()
                return [Contact(**c) for c in data.get("results", [])]
            return []

    async def create_contact(self, contact: Contact) -> Contact:
        base_url = self.credentials.get("base_url").rstrip('/')
        api_key = self.credentials.get("api_key")
        headers = {"Authorization": f"Token {api_key}"}
        
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                f"{base_url}/api/contacts/", 
                headers=headers, 
                json=contact.dict(exclude={"id"})
            )
            response.raise_for_status()
            return Contact(**response.json())

    async def update_contact(self, contact_id: str, updates: Dict[str, Any]) -> Contact:
        base_url = self.credentials.get("base_url").rstrip('/')
        api_key = self.credentials.get("api_key")
        headers = {"Authorization": f"Token {api_key}"}
        
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.patch(
                f"{base_url}/api/contacts/{contact_id}/", 
                headers=headers, 
                json=updates
            )
            response.raise_for_status()
            return Contact(**response.json())

    async def delete_contact(self, contact_id: str) -> bool:
        base_url = self.credentials.get("base_url").rstrip('/')
        api_key = self.credentials.get("api_key")
        headers = {"Authorization": f"Token {api_key}"}
        
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.delete(f"{base_url}/api/contacts/{contact_id}/", headers=headers)
            return response.status_code == 204

    # Other methods (get_deals, etc.) would follow similar patterns
    async def get_deals(self, limit: int = 100) -> List[Deal]: return []
    async def create_deal(self, deal: Deal) -> Deal: return deal
    async def update_deal(self, deal_id: str, updates: Dict[str, Any]) -> Deal: return Deal(id=deal_id, **updates)
    async def delete_deal(self, deal_id: str) -> bool: return True
    async def get_contact(self, contact_id: str) -> Optional[Contact]: return None
    async def get_contact_by_email(self, email: str) -> Optional[Contact]: return None
