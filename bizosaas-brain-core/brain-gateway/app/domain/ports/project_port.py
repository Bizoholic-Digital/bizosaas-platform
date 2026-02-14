from abc import abstractmethod
from typing import List, Optional
from ..entities.project_task import Project, Task
from .base_connector import BaseConnectorPort

class ProjectPort(BaseConnectorPort):
    """
    Standard interface for Project Management systems (Notion, Trello, Jira).
    """
    
    @abstractmethod
    async def get_projects(self, tenant_id: str) -> List[Project]:
        """Fetch all active projects/boards."""
        pass
    
    @abstractmethod
    async def get_tasks(self, tenant_id: str, project_id: str) -> List[Task]:
        """Fetch tasks for a specific project."""
        pass
    
    @abstractmethod
    async def create_task(self, tenant_id: str, task: Task) -> Task:
        """Create a new task in the external system."""
        pass
    
    @abstractmethod
    async def update_task_status(self, tenant_id: str, task_id: str, status: str) -> Task:
        """Move a task to a new status (e.g. TODO -> DONE)."""
        pass
