import httpx
import logging
from typing import Dict, Any, List, Optional

from ..ports.domain_port import DomainPort, DomainAvailability, DomainInfo
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class CloudflareConnector(BaseConnector, DomainPort):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="cloudflare",
            name="Cloudflare",
            type=ConnectorType.DOMAIN_REGISTRAR,
            description="Register and manage domain names with Cloudflare (Wholesale pricing).",
            icon="shield",
            version="1.0.0",
            auth_schema={
                "api_token": {"type": "string", "label": "Cloudflare API Token", "sensitive": True},
                "account_id": {"type": "string", "label": "Cloudflare Account ID"},
                "affiliate_link": {"type": "string", "label": "Affiliate Link", "default": ""}
            }
        )

    async def validate_credentials(self) -> bool:
        # Placeholder for Cloudflare API verification
        return True

    async def get_status(self) -> ConnectorStatus:
        return ConnectorStatus.CONNECTED

    async def search_domains(self, query: str, tlds: List[str]) -> List[DomainAvailability]:
        # Cloudflare Registrar is unique: it mostly supports transfers and renewals at cost.
        # Registration of new domains might vary by TLD.
        return [
            DomainAvailability(
                domain=f"{query}.{tld}",
                available=True,
                price=8.50 if tld == "com" else 12.00,
                registrar="cloudflare"
            ) for tld in tlds
        ]

    async def register_domain(self, domain: str, years: int = 1, contact_info: Dict[str, Any] = {}) -> Dict[str, Any]:
        logger.info(f"Cloudflare: Registering {domain}")
        return {"success": True, "domain": domain}

    async def get_domain_info(self, domain: str) -> Optional[DomainInfo]:
        return DomainInfo(domain=domain, registrar="cloudflare", status="active")

    async def renew_domain(self, domain: str, years: int = 1) -> bool:
        return True

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {"data": []}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {}
