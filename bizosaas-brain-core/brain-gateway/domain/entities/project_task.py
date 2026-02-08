from enum import Enum
from typing import Optional, List
from pydantic import Field
from datetime import datetime
from .base import BaseEntity

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    BLOCKED = "blocked"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Project(BaseEntity):
    """
    Canonical representation of a Project.
    Maps to: Trello Board, Notion Page/Database, Jira Project, Asana Project.
    """
    name: str
    description: Optional[str] = None
    status: str = "active"
    
    # Connector details
    source_system: str = Field(..., description="e.g., 'notion', 'trello', 'jira'")
    external_id: str = Field(..., description="ID in the external system")
    external_url: Optional[str] = None
    
    owner_id: Optional[str] = None
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None

class Task(BaseEntity):
    """
    Canonical representation of a Task.
    Maps to: Trello Card, Notion Item, Jira Ticket, Asana Task.
    """
    project_id: str = Field(..., description="Reference to local generic Project ID")
    parent_task_id: Optional[str] = None
    
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    
    # Connector details
    source_system: str = Field(..., description="e.g., 'notion', 'trello', 'jira'")
    external_id: str = Field(..., description="ID in the external system")
    external_url: Optional[str] = None
    
    assignee_id: Optional[str] = None
    due_date: Optional[datetime] = None
    tags: List[str] = []
    
    model_config = {"use_enum_values": True}
