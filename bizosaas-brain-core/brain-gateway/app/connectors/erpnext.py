import httpx
import logging
from typing import Dict, Any, List, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class ERPNextConnector(BaseConnector):
    """
    ERPNext Connector for BizOSaaS.
    Enables AI Agents to interact with ERPNext for inventory, sales, and accounting data.
    """

    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="erpnext",
            name="ERPNext",
            type=ConnectorType.OTHER, # ERP falls under OTHER or we could add ERP type
            description="Manage your business with ERPNext inventory, sales, and accounting.",
            icon="database",
            auth_schema={
                "type": "object",
                "properties": {
                    "base_url": {"type": "string", "title": "ERPNext Site URL", "placeholder": "https://erp.example.com"},
                    "api_key": {"type": "string", "title": "API Key"},
                    "api_secret": {"type": "string", "title": "API Secret", "format": "password"}
                },
                "required": ["base_url", "api_key", "api_secret"]
            }
        )

    async def validate_credentials(self) -> bool:
        """Verify credentials by checking the `/api/method/frappe.auth.get_logged_user` endpoint."""
        try:
            base_url = self.credentials.get("base_url").rstrip('/')
            api_key = self.credentials.get("api_key")
            api_secret = self.credentials.get("api_secret")
            
            headers = {
                "Authorization": f"token {api_key}:{api_secret}",
                "Accept": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{base_url}/api/method/frappe.auth.get_logged_user", headers=headers)
                return response.status_code == 200
        except Exception as e:
            logger.error(f"ERPNext validation failed: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        is_valid = await self.validate_credentials()
        return ConnectorStatus.CONNECTED if is_valid else ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Fetch data from ERPNext.
        Example resource_types: 'Item', 'Sales Order', 'Purchase Order', 'Customer'
        """
        try:
            base_url = self.credentials.get("base_url").rstrip('/')
            api_key = self.credentials.get("api_key")
            api_secret = self.credentials.get("api_secret")
            
            headers = {
                "Authorization": f"token {api_key}:{api_secret}",
                "Accept": "application/json"
            }
            
            # ERPNext REST API for DocTypes: /api/resource/{DocType}
            url = f"{base_url}/api/resource/{resource_type}"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "status": "success",
                        "data": data.get("data", []),
                        "resource": resource_type
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"ERPNext returned {response.status_code}: {response.text}"
                    }
        except Exception as e:
            logger.error(f"ERPNext sync failed for {resource_type}: {e}")
            return {"status": "error", "message": str(e)}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform a write action in ERPNext.
        action format: 'create_{DocType}' or 'update_{DocType}'
        """
        try:
            base_url = self.credentials.get("base_url").rstrip('/')
            api_key = self.credentials.get("api_key")
            api_secret = self.credentials.get("api_secret")
            
            headers = {
                "Authorization": f"token {api_key}:{api_secret}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            if action.startswith("create_"):
                doctype = action.replace("create_", "")
                url = f"{base_url}/api/resource/{doctype}"
                method = "POST"
            elif action.startswith("update_"):
                # Expecting payload to have 'name' (ID) of the document
                doc_name = payload.pop("name", None)
                if not doc_name:
                    return {"status": "error", "message": "Missing 'name' in update payload"}
                doctype = action.replace("update_", "")
                url = f"{base_url}/api/resource/{doctype}/{doc_name}"
                method = "PUT"
            else:
                return {"status": "error", "message": f"Unsupported action: {action}"}
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                if method == "POST":
                    response = await client.post(url, headers=headers, json=payload)
                else:
                    response = await client.put(url, headers=headers, json=payload)
                
                if response.status_code in [200, 201]:
                    return {
                        "status": "success",
                        "data": response.json().get("data"),
                        "action": action
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"ERPNext action failed: {response.status_code} - {response.text}"
                    }
        except Exception as e:
            logger.error(f"ERPNext action failed: {e}")
            return {"status": "error", "message": str(e)}
