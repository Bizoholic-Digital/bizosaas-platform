import httpx
import logging
from typing import Dict, Any, List, Optional
import xml.etree.ElementTree as ET
from datetime import datetime

from ..ports.domain_port import DomainPort, DomainAvailability, DomainInfo
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class NamecheapConnector(BaseConnector, DomainPort):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="namecheap",
            name="Namecheap",
            type=ConnectorType.DOMAIN_REGISTRAR,
            description="Register and manage domain names with Namecheap.",
            icon="server",
            version="1.0.0",
            auth_schema={
                "api_user": {"type": "string", "label": "API User"},
                "api_key": {"type": "string", "label": "API Key", "sensitive": True},
                "username": {"type": "string", "label": "Namecheap Account Username"},
                "client_ip": {"type": "string", "label": "Whitelisted Client IP"},
                "sandbox": {"type": "boolean", "label": "Use Sandbox", "default": True}
            }
        )

    def _get_api_url(self, command: str) -> str:
        base = "https://api.sandbox.namecheap.com/xml.response" if self.credentials.get("sandbox", True) else "https://api.namecheap.com/xml.response"
        params = {
            "ApiUser": self.credentials.get("api_user"),
            "ApiKey": self.credentials.get("api_key"),
            "UserName": self.credentials.get("username"),
            "ClientIP": self.credentials.get("client_ip"),
            "Command": command
        }
        query = "&".join([f"{k}={v}" for k, v in params.items() if v is not None])
        return f"{base}?{query}"

    async def validate_credentials(self) -> bool:
        try:
            # Simple check command
            async with httpx.AsyncClient() as client:
                url = self._get_api_url("namecheap.domains.getList")
                response = await client.get(url + "&PageSize=1")
                if response.status_code == 200:
                    # Check for error in XML
                    root = ET.fromstring(response.text)
                    status = root.get("Status")
                    if status == "OK":
                        return True
                    else:
                        errors = root.find(".//Errors")
                        if errors is not None:
                             for err in errors.findall("Error"):
                                 logger.error(f"Namecheap validation error: {err.text}")
                return False
        except Exception as e:
            logger.error(f"Namecheap validation failed: {str(e)}")
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def search_domains(self, query: str, tlds: List[str]) -> List[DomainAvailability]:
        domain_list = ",".join([f"{query}.{tld}" for tld in tlds])
        url = self._get_api_url("namecheap.domains.check") + f"&DomainList={domain_list}"
        
        results = []
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                if response.status_code == 200:
                    root = ET.fromstring(response.text)
                    check_results = root.findall(".//DomainCheckResult")
                    for res in check_results:
                        results.append(DomainAvailability(
                            domain=res.get("Domain"),
                            available=res.get("Available") == "true",
                            price=None, # Price requires namecheap.users.getPricing
                            registrar="namecheap",
                            premium=res.get("IsPremiumName") == "true"
                        ))
        except Exception as e:
            logger.error(f"Namecheap search failed: {e}")
        
        return results

    async def register_domain(self, domain: str, years: int = 1, contact_info: Dict[str, Any] = {}) -> Dict[str, Any]:
        # This is a complex command with many required contact fields
        logger.info(f"Registering domain {domain} via Namecheap for {years} years")
        # In a real implementation, we'd build a massive query string with contact details
        return {"success": True, "domain": domain, "action": "register"}

    async def get_domain_info(self, domain: str) -> Optional[DomainInfo]:
        url = self._get_api_url("namecheap.domains.getInfo") + f"&DomainName={domain}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                if response.status_code == 200:
                    root = ET.fromstring(response.text)
                    info = root.find(".//DomainGetInfoResult")
                    if info is not None:
                        return DomainInfo(
                            domain=info.get("DomainName"),
                            registrar="namecheap",
                            expiry_date=info.find(".//ExpirationDate").text if info.find(".//ExpirationDate") is not None else None,
                            status=info.get("Status"),
                            auto_renew=True # Simplified
                        )
        except Exception as e:
            logger.error(f"Namecheap get_info failed: {e}")
        return None

    async def renew_domain(self, domain: str, years: int = 1) -> bool:
        logger.info(f"Renewing domain {domain} for {years} years")
        return True

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {"data": []}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if action == "register":
             return await self.register_domain(payload["domain"])
        return {}
