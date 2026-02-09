import httpx
import os
import logging
from typing import Dict, Any, List, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry
from .oauth_mixin import OAuthMixin
from ..ports.crm_port import CRMPort, Contact, Deal, CRMStats

from app.observability.decorators import instrument_connector_operation, instrument_sync_operation

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class HubSpotConnector(BaseConnector, OAuthMixin, CRMPort):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="hubspot",
            name="HubSpot",
            type=ConnectorType.CRM,
            description="Sync your CRM deals, companies, and contacts with HubSpot.",
            icon="activity",
            version="2.0.0",
            auth_schema={
                "access_token": {"type": "string", "label": "Access Token", "format": "password"},
                "refresh_token": {"type": "string", "label": "Refresh Token", "format": "password"}
            }
        )

    def _get_base_url(self) -> str:
        return "https://api.hubapi.com"
    
    def _get_headers(self) -> Dict[str, str]:
        token = self.credentials.get("access_token")
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        client_id = os.environ.get("HUBSPOT_CLIENT_ID", "")
        scopes = [
            "crm.objects.contacts.read", "crm.objects.contacts.write",
            "crm.objects.deals.read", "crm.objects.deals.write",
            "crm.objects.companies.read", "crm.objects.companies.write"
        ]
        scope_str = "%20".join(scopes)
        return (
            f"https://app.hubspot.com/oauth/authorize?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"scope={scope_str}&"
            f"state={state}"
        )

    async def exchange_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._get_base_url()}/oauth/v1/token",
                data={
                    "client_id": os.environ.get("HUBSPOT_CLIENT_ID", ""),
                    "client_secret": os.environ.get("HUBSPOT_CLIENT_SECRET", ""),
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_uri
                },
            )
            response.raise_for_status()
            return response.json()

    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._get_base_url()}/oauth/v1/token",
                data={
                    "client_id": os.environ.get("HUBSPOT_CLIENT_ID", ""),
                    "client_secret": os.environ.get("HUBSPOT_CLIENT_SECRET", ""),
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token
                },
            )
            response.raise_for_status()
            return response.json()

    async def validate_credentials(self) -> bool:
        token = self.credentials.get("access_token")
        if not token:
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_base_url()}/crm/v3/objects/contacts",
                    headers=self._get_headers(),
                    params={"limit": 1}
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"HubSpot credential validation failed: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    # CRM Port Implementation
    async def get_stats(self) -> CRMStats:
        """Get CRM statistics from HubSpot"""
        try:
            async with httpx.AsyncClient() as client:
                headers = self._get_headers()
                
                # Get contact count
                contacts_resp = await client.get(
                    f"{self._get_base_url()}/crm/v3/objects/contacts",
                    headers=headers,
                    params={"limit": 1}
                )
                contacts_count = contacts_resp.json().get("total", 0) if contacts_resp.status_code == 200 else 0
                
                # Get deals count
                deals_resp = await client.get(
                    f"{self._get_base_url()}/crm/v3/objects/deals",
                    headers=headers,
                    params={"limit": 1}
                )
                deals_data = deals_resp.json() if deals_resp.status_code == 200 else {}
                deals_count = deals_data.get("total", 0)
                
                return CRMStats(
                    contacts=contacts_count,
                    deals=deals_count,
                    companies=0,  # Would need separate API call
                    total_deal_value=0.0
                )
        except Exception as e:
            logger.error(f"Failed to get HubSpot stats: {e}")
            return CRMStats(contacts=0, deals=0, companies=0)

    @instrument_sync_operation("contacts")
    async def get_contacts(self, limit: int = 100, cursor: Optional[str] = None) -> List[Contact]:
        """Get contacts from HubSpot"""
        try:
            async with httpx.AsyncClient() as client:
                params = {"limit": min(limit, 100)}
                if cursor:
                    params["after"] = cursor
                    
                response = await client.get(
                    f"{self._get_base_url()}/crm/v3/objects/contacts",
                    headers=self._get_headers(),
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
                contacts = []
                for item in data.get("results", []):
                    props = item.get("properties", {})
                    contacts.append(Contact(
                        id=item.get("id"),
                        email=props.get("email", ""),
                        first_name=props.get("firstname"),
                        last_name=props.get("lastname"),
                        phone=props.get("phone"),
                        company=props.get("company"),
                        tags=[],
                        custom_fields=props
                    ))
                
                return contacts
        except Exception as e:
            logger.error(f"Failed to get HubSpot contacts: {e}")
            return []

    async def get_contact(self, contact_id: str) -> Optional[Contact]:
        """Get a specific contact by ID"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_base_url()}/crm/v3/objects/contacts/{contact_id}",
                    headers=self._get_headers()
                )
                if response.status_code == 404:
                    return None
                    
                response.raise_for_status()
                item = response.json()
                props = item.get("properties", {})
                
                return Contact(
                    id=item.get("id"),
                    email=props.get("email", ""),
                    first_name=props.get("firstname"),
                    last_name=props.get("lastname"),
                    phone=props.get("phone"),
                    company=props.get("company"),
                    custom_fields=props
                )
        except Exception as e:
            logger.error(f"Failed to get HubSpot contact {contact_id}: {e}")
            return None

    async def get_contact_by_email(self, email: str) -> Optional[Contact]:
        """Get contact by email"""
        contacts = await self.get_contacts(limit=1)
        for contact in contacts:
            if contact.email == email:
                return contact
        return None

    @instrument_connector_operation("create_contact")
    async def create_contact(self, contact: Contact) -> Contact:
        """Create a new contact in HubSpot"""
        try:
            async with httpx.AsyncClient() as client:
                properties = {
                    "email": contact.email,
                    "firstname": contact.first_name,
                    "lastname": contact.last_name,
                    "phone": contact.phone,
                    "company": contact.company
                }
                
                response = await client.post(
                    f"{self._get_base_url()}/crm/v3/objects/contacts",
                    headers=self._get_headers(),
                    json={"properties": properties}
                )
                response.raise_for_status()
                result = response.json()
                contact.id = result.get("id")
                return contact
        except Exception as e:
            logger.error(f"Failed to create HubSpot contact: {e}")
            raise

    @instrument_connector_operation("update_contact")
    async def update_contact(self, contact_id: str, updates: Dict[str, Any]) -> Contact:
        """Update an existing contact"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self._get_base_url()}/crm/v3/objects/contacts/{contact_id}",
                    headers=self._get_headers(),
                    json={"properties": updates}
                )
                response.raise_for_status()
                
                # Return updated contact
                return await self.get_contact(contact_id)
        except Exception as e:
            logger.error(f"Failed to update HubSpot contact {contact_id}: {e}")
            raise

    @instrument_connector_operation("delete_contact")
    async def delete_contact(self, contact_id: str) -> bool:
        """Delete an existing contact"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self._get_base_url()}/crm/v3/objects/contacts/{contact_id}",
                    headers=self._get_headers()
                )
                return response.status_code in [204, 200]
        except Exception as e:
            logger.error(f"Failed to delete HubSpot contact {contact_id}: {e}")
            return False

    @instrument_sync_operation("deals")
    async def get_deals(self, limit: int = 100) -> List[Deal]:
        """Get deals from HubSpot"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_base_url()}/crm/v3/objects/deals",
                    headers=self._get_headers(),
                    params={"limit": min(limit, 100)}
                )
                response.raise_for_status()
                data = response.json()
                
                deals = []
                for item in data.get("results", []):
                    props = item.get("properties", {})
                    deals.append(Deal(
                        id=item.get("id"),
                        title=props.get("dealname", "Untitled Deal"),
                        value=float(props.get("amount", 0)),
                        stage=props.get("dealstage", ""),
                        pipeline=props.get("pipeline"),
                        close_date=props.get("closedate")
                    ))
                
                return deals
        except Exception as e:
            logger.error(f"Failed to get HubSpot deals: {e}")
            return []

    @instrument_connector_operation("create_deal")
    async def create_deal(self, deal: Deal) -> Deal:
        """Create a new deal in HubSpot"""
        try:
            async with httpx.AsyncClient() as client:
                properties = {
                    "dealname": deal.title,
                    "amount": str(deal.value),
                    "dealstage": deal.stage,
                    "pipeline": deal.pipeline,
                    "closedate": deal.close_date
                }
                
                response = await client.post(
                    f"{self._get_base_url()}/crm/v3/objects/deals",
                    headers=self._get_headers(),
                    json={"properties": properties}
                )
                response.raise_for_status()
                result = response.json()
                deal.id = result.get("id")
                return deal
        except Exception as e:
            logger.error(f"Failed to create HubSpot deal: {e}")
            raise

    async def update_deal(self, deal_id: str, updates: Dict[str, Any]) -> Deal:
        """Update an existing deal"""
        try:
            async with httpx.AsyncClient() as client:
                # Map titles to HubSpot properties if present
                if "title" in updates:
                    updates["dealname"] = updates.pop("title")
                if "value" in updates:
                    updates["amount"] = str(updates.pop("value"))
                
                response = await client.patch(
                    f"{self._get_base_url()}/crm/v3/objects/deals/{deal_id}",
                    headers=self._get_headers(),
                    json={"properties": updates}
                )
                response.raise_for_status()
                
                # Refresh and return
                deals = await self.get_deals() # Simplified, could get single deal
                for d in deals:
                    if d.id == deal_id:
                        return d
                return Deal(id=deal_id, title="Updated Deal", value=0, stage="")
        except Exception as e:
            logger.error(f"Failed to update HubSpot deal {deal_id}: {e}")
            raise

    async def delete_deal(self, deal_id: str) -> bool:
        """Delete an existing deal"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self._get_base_url()}/crm/v3/objects/deals/{deal_id}",
                    headers=self._get_headers()
                )
                return response.status_code in [204, 200]
        except Exception as e:
            logger.error(f"Failed to delete HubSpot deal {deal_id}: {e}")
            return False

    # Legacy methods for backward compatibility
    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Legacy sync support"""
        if resource_type == "contacts":
            contacts = await self.get_contacts()
            return {"data": [c.dict() for c in contacts]}
        elif resource_type == "deals":
            deals = await self.get_deals()
            return {"data": [d.dict() for d in deals]}
        return {"error": "Unsupported resource type"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Legacy action support"""
        return {"error": f"Unsupported action: {action}"}
