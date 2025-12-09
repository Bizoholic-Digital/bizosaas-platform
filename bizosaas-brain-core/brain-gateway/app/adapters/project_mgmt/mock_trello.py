from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from domain.ports.project_port import ProjectPort
from domain.entities.project_task import Project, Task, TaskStatus

class MockTrelloAdapter(ProjectPort):
    """
    Mock implementation of Trello connector for testing and development.
    Uses in-memory storage to simulate an external API.
    """
    
    def __init__(self):
        self._projects = {}
        self._tasks = {}
        # Pre-seed some data
        self._seed_data()

    def _seed_data(self):
        p_id = str(uuid.uuid4())
        self._projects[p_id] = {
            "id": p_id,
            "name": "Website Redesign",
            "url": "https://trello.com/b/example"
        }
        
        t_id_1 = str(uuid.uuid4())
        self._tasks[t_id_1] = {
            "id": t_id_1,
            "project_id": p_id,
            "title": "Design Homepage",
            "status": "in_progress"
        }
        
    async def validate_credentials(self, credentials: Dict[str, Any]) -> bool:
        return credentials.get("api_key") == "valid_key"

    async def get_health(self) -> Dict[str, Any]:
        return {"status": "ok", "latency_ms": 15}

    async def get_authorize_url(self, state: str) -> str:
        return f"https://trello.com/1/authorize?key=mock&return_url=callback&state={state}"

    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        return {"access_token": "mock_token", "expires_in": 3600}

    async def get_projects(self, tenant_id: str) -> List[Project]:
        return [
            Project(
                tenant_id=tenant_id,
                name=p["name"],
                source_system="trello",
                external_id=p_id,
                external_url=p["url"]
            )
            for p_id, p in self._projects.items()
        ]

    async def get_tasks(self, tenant_id: str, project_id: str) -> List[Task]:
        return [
            Task(
                tenant_id=tenant_id,
                project_id=project_id,
                title=t["title"],
                status=TaskStatus(t["status"]),
                source_system="trello",
                external_id=t_id,
                priority="medium"
            )
            for t_id, t in self._tasks.items()
            if t["project_id"] == project_id
        ]

    async def create_task(self, tenant_id: str, task: Task) -> Task:
        t_id = str(uuid.uuid4())
        self._tasks[t_id] = {
            "id": t_id,
            "project_id": task.project_id,
            "title": task.title,
            "status": task.status.value
        }
        task.external_id = t_id
        task.source_system = "trello"
        return task

    async def update_task_status(self, tenant_id: str, task_id: str, status: str) -> Task:
        # detailed implementation skipped for brevity
        pass
