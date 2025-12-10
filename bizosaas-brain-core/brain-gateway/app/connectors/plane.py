import httpx
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from ..ports.project_port import ProjectPort, Project, Issue, Cycle, IssueState
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class PlaneConnector(BaseConnector, ProjectPort):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="plane",
            name="Plane.so",
            type=ConnectorType.PROJECT_MANAGEMENT,
            description="Open Source Project Management tool.",
            icon="plane",
            version="1.0.0",
            auth_schema={
                "url": {"type": "string", "label": "Instance URL", "placeholder": "https://app.plane.so"},
                "api_key": {"type": "string", "label": "API Key"},
                "workspace_slug": {"type": "string", "label": "Workspace Slug"}
            }
        )

    def _get_headers(self) -> Dict[str, str]:
        return {
            "X-API-Key": self.credentials.get("api_key"),
            "Content-Type": "application/json"
        }

    def _get_api_url(self, path: str) -> str:
        base_url = self.credentials.get("url", "https://app.plane.so").rstrip("/")
        slug = self.credentials.get("workspace_slug")
        # Most Plane APIs are /api/v1/workspaces/:slug/...
        return f"{base_url}/api/v1/workspaces/{slug}/{path.lstrip('/')}"

    async def validate_credentials(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self._get_api_url("projects"),
                    headers=self._get_headers(),
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Plane validation failed: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR
        
    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {"data": []}
    
    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {}

    # --- ProjectPort Implementation ---

    async def get_projects(self) -> List[Project]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._get_api_url("projects"),
                headers=self._get_headers(),
                timeout=15.0
            )
            response.raise_for_status()
            data = response.json().get("results", [])
            return [
                Project(
                    id=str(p["id"]),
                    name=p["name"],
                    identifier=p.get("identifier"),
                    description=p.get("description"),
                    start_date=p.get("start_date"), # Parse if needed
                    target_date=p.get("target_date")
                ) for p in data
            ]

    async def get_project(self, project_id: str) -> Optional[Project]:
        # Usually get from list if endpoint not available or implement specific
        return None

    async def create_project(self, project: Project) -> Project:
        payload = {
            "name": project.name,
            "identifier": project.identifier,
            "description": project.description
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._get_api_url("projects"),
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            p = response.json()
            project.id = str(p["id"])
            return project

    async def get_cycles(self, project_id: str) -> List[Cycle]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._get_api_url(f"projects/{project_id}/cycles"),
                headers=self._get_headers()
            )
            data = response.json().get("results", [])
            return [
                Cycle(
                    id=str(c["id"]),
                    project_id=str(c["project_detail"]["id"]),
                    name=c["name"],
                    start_date=c.get("start_date"),
                    end_date=c.get("end_date")
                ) for c in data
            ]

    async def get_states(self, project_id: str) -> List[IssueState]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._get_api_url(f"projects/{project_id}/states"),
                headers=self._get_headers()
            )
            data = response.json().get("results", [])
            return [
                IssueState(
                    id=str(s["id"]),
                    name=s["name"],
                    group=s["group"],
                    color=s["color"]
                ) for s in data
            ]

    async def get_issues(self, project_id: str, cycle_id: Optional[str] = None) -> List[Issue]:
        endpoint = f"projects/{project_id}/issues"
        params = {}
        if cycle_id:
             params["cycle"] = cycle_id
             
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._get_api_url(endpoint),
                headers=self._get_headers(),
                params=params
            )
            response.raise_for_status()
            data = response.json().get("results", [])
            return [
                Issue(
                    id=str(i["id"]),
                    title=i["name"],
                    description=i.get("description_html"), # or description_stripped
                    project_id=project_id,
                    state_id=str(i.get("state")),
                    priority=i.get("priority"),
                    due_date=i.get("target_date")
                ) for i in data
            ]

    async def get_issue(self, issue_id: str) -> Optional[Issue]:
        return None

    async def create_issue(self, issue: Issue) -> Issue:
        payload = {
            "name": issue.title,
            "description_html": issue.description,
            "priority": issue.priority,
            "state": issue.state_id
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._get_api_url(f"projects/{issue.project_id}/issues"),
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            i = response.json()
            issue.id = str(i["id"])
            return issue

    async def update_issue(self, issue_id: str, updates: Dict[str, Any]) -> Issue:
        # Complex to find project_id for issue_id if not provided, assuming caller knows
        return Issue(title="Updated", project_id="")
