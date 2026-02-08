import strawberry
from typing import Optional, List
from datetime import datetime
from enum import Enum

@strawberry.enum
class TaskStatusEnum(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    BLOCKED = "blocked"

@strawberry.type
class ProjectType:
    id: str
    name: str
    description: Optional[str]
    status: str
    source_system: str
    external_id: str
    external_url: Optional[str]
    created_at: datetime
    updated_at: datetime

@strawberry.type
class TaskType:
    id: str
    project_id: str
    title: str
    description: Optional[str]
    status: TaskStatusEnum
    priority: str
    source_system: str
    external_id: str
    external_url: Optional[str]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
