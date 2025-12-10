from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class Project(BaseModel):
    id: Optional[str] = None
    name: str
    identifier: Optional[str] = None # e.g. "PROJ"
    description: Optional[str] = None
    lead_id: Optional[str] = None
    start_date: Optional[datetime] = None
    target_date: Optional[datetime] = None

class Cycle(BaseModel):
    id: str
    project_id: str
    name: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class IssueState(BaseModel):
    id: str
    name: str
    group: str # backlog, unstarted, started, completed, cancelled
    color: str

class Issue(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    project_id: str
    state_id: Optional[str] = None
    cycle_id: Optional[str] = None
    priority: Optional[str] = None # urgent, high, medium, low, none
    assignee_ids: List[str] = []
    labels: List[str] = []
    due_date: Optional[datetime] = None
    parent_id: Optional[str] = None

class ProjectPort(ABC):
    """
    Abstract Port for Project Management systems (Plane.so, JIRA, Linear).
    """

    @abstractmethod
    async def get_projects(self) -> List[Project]:
        pass

    @abstractmethod
    async def get_project(self, project_id: str) -> Optional[Project]:
        pass
    
    @abstractmethod
    async def create_project(self, project: Project) -> Project:
        pass

    @abstractmethod
    async def get_cycles(self, project_id: str) -> List[Cycle]:
        pass

    @abstractmethod
    async def get_states(self, project_id: str) -> List[IssueState]:
        pass

    @abstractmethod
    async def get_issues(self, project_id: str, cycle_id: Optional[str] = None) -> List[Issue]:
        pass

    @abstractmethod
    async def get_issue(self, issue_id: str) -> Optional[Issue]:
        pass

    @abstractmethod
    async def create_issue(self, issue: Issue) -> Issue:
        pass

    @abstractmethod
    async def update_issue(self, issue_id: str, updates: Dict[str, Any]) -> Issue:
        pass
