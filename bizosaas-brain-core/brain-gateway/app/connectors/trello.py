import httpx
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from ..ports.task_port import TaskPort, Task, Board, TaskList
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class TrelloConnector(BaseConnector, TaskPort):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="trello",
            name="Trello",
            type=ConnectorType.OTHER, # Or TASK if added to enum
            description="Manage projects and tasks with boards.",
            icon="trello",
            version="1.0.0",
            auth_schema={
                "api_key": {"type": "string", "label": "API Key"},
                "api_token": {"type": "string", "label": "API Token"}
            }
        )

    def _get_params(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        p = params.copy() if params else {}
        p["key"] = self.credentials.get("api_key")
        p["token"] = self.credentials.get("api_token")
        return p

    async def validate_credentials(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.trello.com/1/members/me",
                    params=self._get_params(),
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Trello validation failed: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {"data": []}
    
    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {}

    # --- TaskPort Implementation ---

    async def get_boards(self) -> List[Board]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.trello.com/1/members/me/boards",
                params=self._get_params(),
                timeout=15.0
            )
            response.raise_for_status()
            data = response.json()
            return [
                Board(id=b["id"], name=b["name"], description=b.get("desc"), url=b["url"])
                for b in data
            ]

    async def get_lists(self, board_id: str) -> List[TaskList]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.trello.com/1/boards/{board_id}/lists",
                params=self._get_params()
            )
            response.raise_for_status()
            data = response.json()
            return [TaskList(id=l["id"], name=l["name"], board_id=board_id) for l in data]

    async def get_tasks(self, board_id: str, list_id: Optional[str] = None) -> List[Task]:
        # Trello gets cards from board or list
        endpoint = f"https://api.trello.com/1/boards/{board_id}/cards"
        if list_id:
            endpoint = f"https://api.trello.com/1/lists/{list_id}/cards"
            
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint, params=self._get_params())
            response.raise_for_status()
            data = response.json()
            
            tasks = []
            for card in data:
                tasks.append(Task(
                    id=card["id"],
                    title=card["name"],
                    description=card.get("desc"),
                    status="open" if not card.get("closed") else "closed",
                    board_id=board_id,
                    list_id=card["idList"],
                    due_date=card.get("due"), # string, Pydantic handles parsing if valid ISO
                    url=card["url"],
                    assignee_ids=card.get("idMembers", [])
                ))
            return tasks

    async def get_task(self, task_id: str) -> Optional[Task]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.trello.com/1/cards/{task_id}",
                params=self._get_params()
            )
            if response.status_code == 404: return None
            card = response.json()
            return Task(
                id=card["id"],
                title=card["name"],
                description=card.get("desc"),
                board_id=card["idBoard"],
                url=card["url"]
            )

    async def create_task(self, task: Task) -> Task:
        # Trello needs idList
        if not task.list_id:
            raise ValueError("list_id is required to create a card in Trello")
            
        payload = self._get_params({
            "name": task.title,
            "desc": task.description,
            "idList": task.list_id,
            "due": task.due_date.isoformat() if task.due_date else None
        })
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.trello.com/1/cards",
                params=payload # Trello mostly accepts query params or form data
            )
            response.raise_for_status()
            card = response.json()
            task.id = card["id"]
            return task

    async def update_task(self, task_id: str, updates: Dict[str, Any]) -> Task:
        return await self.get_task(task_id) # Mock update

    async def move_task(self, task_id: str, to_list_id: str) -> bool:
        async with httpx.AsyncClient() as client:
             response = await client.put(
                f"https://api.trello.com/1/cards/{task_id}",
                params=self._get_params({"idList": to_list_id})
             )
             return response.status_code == 200

    async def delete_task(self, task_id: str) -> bool:
         async with httpx.AsyncClient() as client:
             response = await client.delete(
                f"https://api.trello.com/1/cards/{task_id}",
                params=self._get_params()
             )
             return response.status_code == 200
