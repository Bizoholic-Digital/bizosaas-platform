from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

class WorkflowPort(ABC):
    """
    Port for Workflow Orchestration (Temporal).
    Follows Hexagonal Architecture.
    """
    
    @abstractmethod
    async def start_workflow(
        self,
        workflow_name: str,
        workflow_id: str,
        task_queue: str,
        args: Optional[List[Any]] = None,
        search_attributes: Optional[Dict[str, Any]] = None
    ) -> str:
        """Start a workflow execution"""
        pass

    @abstractmethod
    async def signal_workflow(
        self,
        workflow_id: str,
        signal_name: str,
        args: List[Any],
        run_id: Optional[str] = None
    ) -> None:
        """Send a signal to a running workflow"""
        pass
    
    @abstractmethod
    async def query_workflow(
        self,
        workflow_id: str,
        query_type: str,
        args: Optional[List[Any]] = None,
        run_id: Optional[str] = None
    ) -> Any:
        """Query workflow state"""
        pass
        
    @abstractmethod
    async def get_workflow_status(
        self,
        workflow_id: str,
        run_id: Optional[str] = None
    ) -> str:
        """Get workflow execution status"""
        pass
        
    @abstractmethod
    async def terminate_workflow(
        self,
        workflow_id: str,
        reason: str,
        run_id: Optional[str] = None
    ) -> None:
        """Terminate a workflow execution"""
        pass

    @abstractmethod
    async def create_schedule(
        self,
        schedule_id: str,
        workflow_name: str,
        args: List[Any],
        cron_expression: str,
        task_queue: str
    ) -> None:
        """Create a recurring schedule"""
        pass
