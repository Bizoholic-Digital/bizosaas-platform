from typing import Dict, Any, List, Optional
import httpx
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus

class PlaneConnector(BaseConnector):
    def __init__(self, tenant_id: str, credentials: Dict[str, Any]):
        super().__init__(tenant_id, credentials)
        self.api_url = credentials.get("api_url", "https://api.plane.so/api/v1")
        self.api_key = credentials.get("api_key")
        
    @property
    def config(self) -> ConnectorConfig:
        return ConnectorConfig(
            id="plane",
            name="Plane",
            type=ConnectorType.PROJECT_MANAGEMENT,
            description="Open Source Project Management Tool",
            logo_url="https://github.com/makeplane.png",
            version="1.0.0",
            auth_fields=[
                {
                    "key": "api_url",
                    "label": "API URL",
                    "type": "text",
                    "placeholder": "https://plane.your-domain.com/api/v1",
                    "required": True,
                    "default": "https://api.plane.so/api/v1"
                },
                {
                    "key": "api_key",
                    "label": "API Key",
                    "type": "password",
                    "placeholder": "Your Plane API Key",
                    "required": True
                }
            ]
        )

    async def validate_credentials(self) -> bool:
        """Validate credentials by fetching current user"""
        if not self.api_key:
            return False
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/users/me/",
                    headers={"X-API-Key": self.api_key},
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception:
            return False
            
    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Sync data for a specific resource.
        Resources: workspaces, projects, issues
        """
        if not self.api_key:
            raise ValueError("API Key not found")
            
        headers = {"X-API-Key": self.api_key}
        
        async with httpx.AsyncClient() as client:
            if resource == "workspaces":
                response = await client.get(
                    f"{self.api_url}/workspaces/",
                    headers=headers
                )
            elif resource == "projects":
                # Requires workspace_slug in params
                slug = params.get("workspace_slug") if params else None
                if not slug:
                    # Fallback: get first workspace
                    ws_resp = await client.get(f"{self.api_url}/workspaces/", headers=headers)
                    if ws_resp.status_code == 200 and ws_resp.json():
                        slug = ws_resp.json()[0]["slug"]
                    else:
                        return []
                response = await client.get(
                    f"{self.api_url}/workspaces/{slug}/projects/",
                    headers=headers
                )
            elif resource == "issues":
                 # Requires workspace_slug and project_id in params
                slug = params.get("workspace_slug")
                project_id = params.get("project_id")
                if not slug or not project_id:
                     raise ValueError("workspace_slug and project_id required for issues")
                response = await client.get(
                    f"{self.api_url}/workspaces/{slug}/projects/{project_id}/issues/",
                    headers=headers
                )
            else:
                raise ValueError(f"Unknown resource: {resource}")
                
            response.raise_for_status()
            return response.json()
