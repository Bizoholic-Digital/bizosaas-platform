from typing import Optional, List, Dict
from pydantic import Field, EmailStr
from .base import BaseEntity

class Contact(BaseEntity):
    """
    Canonical representation of a CRM Contact.
    Maps to: Zoho Contact, HubSpot Contact, Salesforce Contact.
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    
    # Standard CRM lifecycle stage
    lifecycle_stage: str = Field(default="lead", description="lead, subscriber, customer, evangelist")
    status: str = "new"
    
    # Generic fields for mapping varying CRM schemas
    custom_fields: Dict[str, str] = Field(default_factory=dict)
    
    # Connector details
    source_system: str = Field(..., description="e.g., 'zoho', 'hubspot', 'salesforce'")
    external_id: str = Field(..., description="ID in the external system")
    external_url: Optional[str] = None
    
    last_contacted_at: Optional[str] = None
    owner_id: Optional[str] = None

class Deal(BaseEntity):
    """
    Canonical representation of a CRM Deal/Opportunity.
    """
    title: str
    amount: Optional[float] = 0.0
    currency: str = "USD"
    stage: str = Field(..., description="Deal stage (e.g., 'qualification', 'proposal')")
    probability: Optional[int] = None
    
    contact_ids: List[str] = []
    company_id: Optional[str] = None
    
    source_system: str
    external_id: str
    
    expected_close_date: Optional[str] = None
