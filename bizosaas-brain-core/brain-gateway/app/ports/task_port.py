from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class TaskUser(BaseModel):
    id: str
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None

class Board(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    url: Optional[str] = None

class TaskList(BaseModel):
    id: str
    name: str
    board_id: str

class Task(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    status: Optional[str] = None # e.g. "To Do", "Done"
    list_id: Optional[str] = None # Column/List ID
    board_id: str
    assignee_ids: List[str] = []
    due_date: Optional[datetime] = None
    url: Optional[str] = None
    labels: List[str] = []

class TaskPort(ABC):
    """
    Abstract Port for Task Management systems (Trello, ClickUp, Asana).
    """

    @abstractmethod
    async def get_boards(self) -> List[Board]:
        pass

    @abstractmethod
    async def get_lists(self, board_id: str) -> List[TaskList]:
        pass

    @abstractmethod
    async def get_tasks(self, board_id: str, list_id: Optional[str] = None) -> List[Task]:
        pass

    @abstractmethod
    async def get_task(self, task_id: str) -> Optional[Task]:
        pass

    @abstractmethod
    async def create_task(self, task: Task) -> Task:
        pass

    @abstractmethod
    async def update_task(self, task_id: str, updates: Dict[str, Any]) -> Task:
        pass
        
    @abstractmethod
    async def move_task(self, task_id: str, to_list_id: str) -> bool:
        pass
    
    @abstractmethod
    async def delete_task(self, task_id: str) -> bool:
        pass
