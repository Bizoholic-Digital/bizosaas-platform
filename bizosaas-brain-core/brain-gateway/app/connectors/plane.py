from typing import Dict, Any, List, Optional
import httpx
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus

from .registry import ConnectorRegistry

from ..ports.project_port import ProjectPort, Project, Issue, IssueState, Cycle

@ConnectorRegistry.register
class PlaneConnector(BaseConnector, ProjectPort):
    def __init__(self, tenant_id: str, credentials: Dict[str, Any]):
        super().__init__(tenant_id, credentials)
        self.api_url = credentials.get("api_url", "https://api.plane.so/api/v1")
        self.api_key = credentials.get("api_key")
        
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="plane",
            name="Plane",
            type=ConnectorType.PROJECT_MANAGEMENT,
            description="Open Source Project Management Tool (Project & Task creation)",
            icon="plane",
            version="1.0.0",
            auth_schema={
                "api_url": {
                    "type": "string",
                    "label": "API URL",
                    "placeholder": "https://api.plane.so/api/v1",
                    "default": "https://api.plane.so/api/v1"
                },
                "api_key": {
                    "type": "string",
                    "label": "API Key",
                    "format": "password",
                    "placeholder": "Your Plane API Key"
                }
            }
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
            
    async def get_projects(self) -> List[Project]:
        workspace_slug = self.credentials.get("workspace_slug")
        data = await self.sync_data("projects", {"workspace_slug": workspace_slug})
        
        projects_data = data.get("results", []) if isinstance(data, dict) else data
        return [
            Project(
                id=p["id"],
                name=p["name"],
                identifier=p.get("identifier"),
                description=p.get("description")
            ) for p in projects_data
        ]

    async def get_project(self, project_id: str) -> Optional[Project]:
        workspace_slug = self.credentials.get("workspace_slug")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/workspaces/{workspace_slug}/projects/{project_id}/",
                headers={"X-API-Key": self.api_key}
            )
            if response.status_code == 200:
                p = response.json()
                return Project(
                    id=p["id"],
                    name=p["name"],
                    identifier=p.get("identifier"),
                    description=p.get("description")
                )
            return None

    async def create_project(self, project: Project) -> Project:
        payload = {
            "name": project.name,
            "identifier": project.identifier,
            "description": project.description
        }
        workspace_slug = self.credentials.get("workspace_slug")
        res = await self._create_project({**payload, "workspace_slug": workspace_slug})
        project.id = res["id"]
        return project

    async def get_cycles(self, project_id: str) -> List[Cycle]:
        workspace_slug = self.credentials.get("workspace_slug")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/workspaces/{workspace_slug}/projects/{project_id}/cycles/",
                headers={"X-API-Key": self.api_key}
            )
            data = response.json() if response.status_code == 200 else []
            return [
                Cycle(
                    id=c["id"],
                    project_id=project_id,
                    name=c["name"],
                    start_date=None, # Should parse if available
                    end_date=None
                ) for c in (data.get("results", []) if isinstance(data, dict) else data)
            ]

    async def get_states(self, project_id: str) -> List[IssueState]:
        return [] # Simplified

    async def get_issues(self, project_id: str, cycle_id: Optional[str] = None) -> List[Issue]:
        workspace_slug = self.credentials.get("workspace_slug")
        params = {"workspace_slug": workspace_slug, "project_id": project_id}
        data = await self.sync_data("issues", params)
        return [
            Issue(
                id=i["id"],
                title=i["name"],
                description=i.get("description"),
                project_id=project_id,
                priority=i.get("priority")
            ) for i in (data.get("results", []) if isinstance(data, dict) else data)
        ]

    async def get_issue(self, issue_id: str) -> Optional[Issue]:
        return None

    async def create_issue(self, issue: Issue) -> Issue:
        workspace_slug = self.credentials.get("workspace_slug")
        payload = {
            "name": issue.title,
            "description": issue.description,
            "project_id": issue.project_id,
            "priority": issue.priority
        }
        res = await self._create_issue({**payload, "workspace_slug": workspace_slug, "project_id": issue.project_id})
        issue.id = res["id"]
        return issue

    async def update_issue(self, issue_id: str, updates: Dict[str, Any]) -> Issue:
        raise NotImplementedError()

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
            elif resource == "members":
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
                    f"{self.api_url}/workspaces/{slug}/members/",
                    headers=headers
                )
            else:
                raise ValueError(f"Unknown resource: {resource}")
                
            response.raise_for_status()
            return response.json()

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute actions on Plane.
        Actions: create_project, create_issue
        """
        if action == "create_project":
            return await self._create_project(payload)
        elif action == "create_issue":
            return await self._create_issue(payload)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def _create_project(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        workspace_slug = payload.get("workspace_slug")
        if not workspace_slug:
             # Try to get first workspace if not provided
             ws = await self.sync_data("workspaces")
             if ws:
                 workspace_slug = ws[0]["slug"]
             else:
                 raise ValueError("workspace_slug required")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/workspaces/{workspace_slug}/projects/",
                headers={"X-API-Key": self.api_key},
                json=payload
            )
            response.raise_for_status()
            return response.json()

    async def _create_issue(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        workspace_slug = payload.get("workspace_slug")
        project_id = payload.get("project_id")
        
        if not workspace_slug or not project_id:
            raise ValueError("workspace_slug and project_id required")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/workspaces/{workspace_slug}/projects/{project_id}/issues/",
                headers={"X-API-Key": self.api_key},
                json=payload
            )
            response.raise_for_status()
            return response.json()
