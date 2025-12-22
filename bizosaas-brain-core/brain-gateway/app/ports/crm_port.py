from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Contact(BaseModel):
    id: Optional[str] = None
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    tags: List[str] = []
    custom_fields: Dict[str, Any] = {}
    source: Optional[str] = None

class Deal(BaseModel):
    id: Optional[str] = None
    title: str
    value: float
    currency: str = "USD"
    stage: str
    pipeline: Optional[str] = None
    contact_ids: List[str] = []
    close_date: Optional[str] = None

class CRMStats(BaseModel):
    contacts: int
    leads: int
    campaigns: int
    last_sync: Optional[str] = None

class CRMPort(ABC):
    """
    Abstract Port for Customer Relationship Management systems.
    Adapters (Connectors) must implement these methods.
    """

    @abstractmethod
    async def get_stats(self) -> CRMStats:
        """Retrieve CRM statistics."""
        pass

    @abstractmethod
    async def get_contacts(self, limit: int = 100, cursor: Optional[str] = None) -> List[Contact]:
        """Retrieve a list of contacts."""
        pass

    @abstractmethod
    async def get_contact(self, contact_id: str) -> Optional[Contact]:
        """Retrieve a single contact by ID."""
        pass
    
    @abstractmethod
    async def get_contact_by_email(self, email: str) -> Optional[Contact]:
        """Retrieve a single contact by Email."""
        pass

    @abstractmethod
    async def create_contact(self, contact: Contact) -> Contact:
        """Create a new contact."""
        pass

    @abstractmethod
    async def update_contact(self, contact_id: str, updates: Dict[str, Any]) -> Contact:
        """Update an existing contact."""
        pass
        
    @abstractmethod
    async def get_deals(self, limit: int = 100) -> List[Deal]:
        """Retrieve a list of deals/opportunities."""
        pass
        
    @abstractmethod
    async def create_deal(self, deal: Deal) -> Deal:
        """Create a new deal."""
        pass
