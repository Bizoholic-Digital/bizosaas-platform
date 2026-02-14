from abc import abstractmethod
from typing import List, Optional
from ..entities.crm import Contact, Deal
from .base_connector import BaseConnectorPort

class CRMPort(BaseConnectorPort):
    """
    Standard interface for interacting with ANY CRM (Zoho, HubSpot, etc.)
    """
    
    @abstractmethod
    async def get_contacts(self, tenant_id: str, limit: int = 20, cursor: Optional[str] = None) -> List[Contact]:
        """Fetch list of contacts."""
        pass
    
    @abstractmethod
    async def get_contact_by_email(self, tenant_id: str, email: str) -> Optional[Contact]:
        """Find a single contact by email."""
        pass
    
    @abstractmethod
    async def create_contact(self, tenant_id: str, contact: Contact) -> Contact:
        """Create a new contact in the external CRM."""
        pass
    
    @abstractmethod
    async def update_contact(self, tenant_id: str, contact_id: str, data: dict) -> Contact:
        """Update an existing contact."""
        pass

    @abstractmethod
    async def get_deals(self, tenant_id: str) -> List[Deal]:
        """Fetch deals/opportunities."""
        pass
