import strawberry
from typing import Optional, List, Dict, Any

@strawberry.type
class CRMContactType:
    id: Optional[str]
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    tags: List[str]
    source: Optional[str] = None

@strawberry.type
class CRMDealType:
    id: Optional[str]
    title: str
    value: float
    currency: str
    stage: str
    pipeline: Optional[str] = None
    contact_ids: List[str]
    close_date: Optional[str] = None

@strawberry.type
class CRMStatsType:
    contacts: int
    leads: int
    campaigns: int
    last_sync: Optional[str] = None

@strawberry.input
class CRMContactInput:
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    tags: Optional[List[str]] = None

@strawberry.input
class CRMDealInput:
    title: str
    value: float
    currency: str = "USD"
    stage: str
    pipeline: Optional[str] = None
    contact_ids: Optional[List[str]] = None
    close_date: Optional[str] = None
