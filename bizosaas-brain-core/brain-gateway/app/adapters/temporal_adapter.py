import logging
from typing import Dict, Any, Optional, List
from temporalio.client import Client
from app.ports.workflow_port import WorkflowPort

logger = logging.getLogger(__name__)

class TemporalAdapter(WorkflowPort):
    """
    Adapter for Temporal Workflow Engine.
    """
    
    def __init__(self, client: Client):
        self.client = client
        
    @classmethod
    async def connect(cls, host: str, namespace: str = "default") -> "TemporalAdapter":
        """Factory method to create connected adapter"""
        try:
            # Connect to Temporal server
            # Note: In production, TLS certs might be needed
            client = await Client.connect(host, namespace=namespace)
            logger.info(f"Connected to Temporal at {host}")
            return cls(client)
        except Exception as e:
            logger.error(f"Failed to connect to Temporal at {host}: {e}")
            raise

    async def start_workflow(
        self,
        workflow_name: str,
        workflow_id: str,
        task_queue: str,
        args: Optional[List[Any]] = None,
        search_attributes: Optional[Dict[str, Any]] = None
    ) -> str:
        try:
            # Convert args to list if None
            workflow_args = args or []
            
            handle = await self.client.start_workflow(
                workflow=workflow_name,
                id=workflow_id,
                task_queue=task_queue,
                args=workflow_args,
                search_attributes=search_attributes,
            )
            logger.info(f"Started workflow {workflow_name} with ID {workflow_id}")
            return handle.id
        except Exception as e:
            logger.error(f"Failed to start workflow {workflow_name}: {e}")
            raise

    async def signal_workflow(
        self,
        workflow_id: str,
        signal_name: str,
        args: List[Any],
        run_id: Optional[str] = None
    ) -> None:
        try:
            handle = self.client.get_workflow_handle(workflow_id, run_id=run_id)
            await handle.signal(signal_name, *args)
            logger.info(f"Signaled workflow {workflow_id} with {signal_name}")
        except Exception as e:
            logger.error(f"Failed to signal workflow {workflow_id}: {e}")
            raise

    async def query_workflow(
        self,
        workflow_id: str,
        query_type: str,
        args: Optional[List[Any]] = None,
        run_id: Optional[str] = None
    ) -> Any:
        try:
            handle = self.client.get_workflow_handle(workflow_id, run_id=run_id)
            result = await handle.query(query_type, *(args or []))
            return result
        except Exception as e:
            logger.error(f"Failed to query workflow {workflow_id}: {e}")
            raise

    async def get_workflow_status(
        self,
        workflow_id: str,
        run_id: Optional[str] = None
    ) -> str:
        try:
            handle = self.client.get_workflow_handle(workflow_id, run_id=run_id)
            desc = await handle.describe()
            return str(desc.status)
        except Exception as e:
            logger.error(f"Failed to get status for workflow {workflow_id}: {e}")
            raise

    async def terminate_workflow(
        self,
        workflow_id: str,
        reason: str,
        run_id: Optional[str] = None
    ) -> None:
        try:
            handle = self.client.get_workflow_handle(workflow_id, run_id=run_id)
            await handle.terminate(reason=reason)
            logger.info(f"Terminated workflow {workflow_id}: {reason}")
        except Exception as e:
            logger.error(f"Failed to terminate workflow {workflow_id}: {e}")
            raise
