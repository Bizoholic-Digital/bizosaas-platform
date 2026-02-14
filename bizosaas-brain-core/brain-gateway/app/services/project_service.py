from typing import List
from app.domain.entities.project_task import Project, Task
from app.domain.ports.project_port import ProjectPort
from app.adapters.project_mgmt.mock_trello import MockTrelloAdapter

class ProjectService:
    """
    Application service for Project Management.
    Orchestrates data flow between API and Adapters.
    """
    
    def __init__(self):
        # In a real scenario, this would be injected or resolved via factory
        # based on tenant configuration.
        self.adapter: ProjectPort = MockTrelloAdapter()

    async def get_all_projects(self, tenant_id: str) -> List[Project]:
        """Fetch credentials from Vault (mocked) and get projects."""
        # TODO: Get tenant-specific credentials
        return await self.adapter.get_projects(tenant_id)

    async def get_project_tasks(self, tenant_id: str, project_id: str) -> List[Task]:
        """Fetch tasks for a specific project."""
        return await self.adapter.get_tasks(tenant_id, project_id)

    async def create_task(self, tenant_id: str, task: Task) -> Task:
        """Create a new task via the adapter."""
        return await self.adapter.create_task(tenant_id, task)
