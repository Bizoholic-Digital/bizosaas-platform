from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class DomainAvailability(BaseModel):
    domain: str
    available: bool
    price: Optional[float] = None
    currency: str = "USD"
    premium: bool = False
    registrar: str

class DomainInfo(BaseModel):
    domain: str
    registrar: str
    expiry_date: Optional[str] = None
    status: str
    auto_renew: bool = True
    dns_records: List[Dict[str, Any]] = []

class DomainPort(ABC):
    @abstractmethod
    async def search_domains(self, query: str, tlds: List[str]) -> List[DomainAvailability]:
        """Search for domain availability across multiple TLDs."""
        pass

    @abstractmethod
    async def register_domain(self, domain: str, years: int = 1, contact_info: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Register a new domain name."""
        pass

    @abstractmethod
    async def get_domain_info(self, domain: str) -> Optional[DomainInfo]:
        """Get detailed information about a registered domain."""
        pass

    @abstractmethod
    async def renew_domain(self, domain: str, years: int = 1) -> bool:
        """Renew an existing domain registration."""
        pass
