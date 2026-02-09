import httpx
import base64
import logging
from typing import Dict, Any, List, Optional
from ..ports.crm_port import CRMPort, Contact, Deal, CRMStats
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry
from app.observability.decorators import instrument_connector_operation, instrument_sync_operation

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class FluentCRMConnector(BaseConnector, CRMPort):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="fluentcrm",
            name="FluentCRM (WordPress)",
            type=ConnectorType.CRM,
            description="Marketing automation and CRM inside WordPress.",
            icon="fluentcrm",
            version="1.0.0",
            auth_schema={
                "url": {"type": "string", "label": "WordPress Site URL", "placeholder": "https://your-site.com"},
                "username": {"type": "string", "label": "Username"},
                "application_password": {"type": "string", "label": "Application Password", "help": "Generate in Users > Profile"}
            }
        )

    def _get_auth_header(self) -> Dict[str, str]:
        username = self.credentials.get("username")
        password = self.credentials.get("application_password")
        if not username or not password:
            return {}
        credentials = f"{username}:{password}"
        token = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {token}"}

    def _get_api_url(self, path: str) -> str:
        base_url = self.credentials.get("url", "").rstrip("/")
        # Remove wp-json if present in base url to avoid duplication
        if base_url.endswith("/wp-json"):
            base_url = base_url[:-8]
            
        return f"{base_url}/wp-json/fluent-crm/v2/{path.lstrip('/')}"

    async def validate_credentials(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self._get_api_url("contacts"),
                    headers=self._get_auth_header(),
                    params={"per_page": 1},
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"FluentCRM validation failed: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Implementation for BaseConnector.sync_data generic method
        if resource_type == "contacts":
            contacts = await self.get_contacts()
            return {"data": [c.dict() for c in contacts]}
        return {"data": []}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation for BaseConnector.perform_action generic method
        if action == "create_contact":
            contact = Contact(**payload)
            result = await self.create_contact(contact)
            return result.dict()
        return {}

    async def get_stats(self) -> CRMStats:
        async with httpx.AsyncClient() as client:
            try:
                # Fetch one contact to get meta total
                response = await client.get(
                    self._get_api_url("contacts"),
                    headers=self._get_auth_header(),
                    params={"per_page": 1},
                    timeout=10.0
                )
                if response.status_code == 200:
                   data = response.json()
                   # FluentCRM V2 often returns 'meta' with 'total'
                   total = 0
                   if "meta" in data and "total" in data["meta"]:
                       total = data["meta"]["total"]
                   elif "total" in data:
                       total = data["total"]
                   
                   return CRMStats(contacts=total, leads=0, campaigns=0)
            except Exception as e:
                logger.error(f"Stats fetch failed: {e}")
            
            return CRMStats(contacts=0, leads=0, campaigns=0)

    # --- CRMPort Implementation ---

    @instrument_sync_operation("contacts")
    async def get_contacts(self, limit: int = 100, cursor: Optional[str] = None) -> List[Contact]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._get_api_url("contacts"),
                headers=self._get_auth_header(),
                params={"per_page": limit, "page": cursor if cursor else 1},
                timeout=15.0
            )
            response.raise_for_status()
            data = response.json().get("data", [])
            
            contacts = []
            for item in data:
                contacts.append(Contact(
                    id=str(item.get("id")),
                    email=item.get("email"),
                    first_name=item.get("first_name"),
                    last_name=item.get("last_name"),
                    phone=item.get("phone"),
                    source="fluentcrm",
                    tags=[str(t) for t in item.get("tags", [])]
                ))
            return contacts

    async def get_contact(self, contact_id: str) -> Optional[Contact]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self._get_api_url(f"contacts/{contact_id}"),
                    headers=self._get_auth_header()
                )
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                item = response.json().get("contact", {})
                return Contact(
                    id=str(item.get("id")),
                    email=item.get("email"),
                    first_name=item.get("first_name"),
                    last_name=item.get("last_name"),
                    phone=item.get("phone"),
                    source="fluentcrm"
                )
            except Exception as e:
                logger.error(f"Error getting contact {contact_id}: {e}")
                return None

    async def get_contact_by_email(self, email: str) -> Optional[Contact]:
        # FluentCRM might filter by email
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._get_api_url("contacts"),
                headers=self._get_auth_header(),
                params={"search": email}
            )
            data = response.json().get("data", [])
            for item in data:
                if item.get("email") == email:
                     return Contact(
                        id=str(item.get("id")),
                        email=item.get("email"),
                        first_name=item.get("first_name"),
                        last_name=item.get("last_name"),
                        source="fluentcrm"
                    )
            return None

    @instrument_connector_operation("create_contact")
    async def create_contact(self, contact: Contact) -> Contact:
        payload = {
            "email": contact.email,
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "phone": contact.phone,
            "tags": contact.tags,
            "status": "subscribed"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._get_api_url("contacts"),
                headers=self._get_auth_header(),
                json=payload
            )
            response.raise_for_status()
            item = response.json().get("contact", {})
            contact.id = str(item.get("id"))
            return contact

    @instrument_connector_operation("update_contact")
    async def update_contact(self, contact_id: str, updates: Dict[str, Any]) -> Contact:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                self._get_api_url(f"contacts/{contact_id}"),
                headers=self._get_auth_header(),
                json=updates
            )
            response.raise_for_status()
            # Ideally fetch updated contact properly
            return await self.get_contact(contact_id)

    @instrument_connector_operation("delete_contact")
    async def delete_contact(self, contact_id: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                self._get_api_url(f"contacts/{contact_id}"),
                headers=self._get_auth_header()
            )
            return response.status_code in [200, 204]

    async def get_deals(self, limit: int = 100) -> List[Deal]:
        # FluentCRM core doesn't have deals. Return empty list.
        return []

    async def create_deal(self, deal: Deal) -> Deal:
        raise NotImplementedError("Deals are not supported in FluentCRM Connector currently.")

    async def update_deal(self, deal_id: str, updates: Dict[str, Any]) -> Deal:
        raise NotImplementedError("Deals are not supported in FluentCRM Connector currently.")

    async def delete_deal(self, deal_id: str) -> bool:
        raise NotImplementedError("Deals are not supported in FluentCRM Connector currently.")
