from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.models.workflow import Workflow
from app.ports.workflow_port import WorkflowPort
import logging

logger = logging.getLogger(__name__)

class WorkflowService:
    def __init__(self, db: Session, workflow_port: Optional[WorkflowPort] = None):
        self.db = db
        self.workflow_port = workflow_port

    async def create_workflow(self, tenant_id: str, data: Dict[str, Any]) -> Workflow:
        workflow = Workflow(
            tenant_id=tenant_id,
            name=data["name"],
            description=data.get("description"),
            type=data.get("type", "Custom"),
            status=data.get("status", "paused"),
            config=data.get("config") or {"retries": 3, "timeout": 30, "notifyOnError": False, "priority": "medium"}
        )
        self.db.add(workflow)
        self.db.commit()
        self.db.refresh(workflow)
        return workflow

    async def list_workflows(self, tenant_id: str) -> List[Workflow]:
        return self.db.query(Workflow).filter(Workflow.tenant_id == tenant_id).all()

    async def update_config(self, tenant_id: str, workflow_id: str, config_update: Dict[str, Any]) -> bool:
        workflow = self.db.query(Workflow).filter(Workflow.id == workflow_id, Workflow.tenant_id == tenant_id).first()
        if not workflow:
            return False
        
        current_config = dict(workflow.config or {})
        for key, value in config_update.items():
            if value is not None:
                current_config[key] = value
        
        workflow.config = current_config
        self.db.commit()
        return True

    async def toggle_status(self, tenant_id: str, workflow_id: str) -> Optional[str]:
        workflow = self.db.query(Workflow).filter(Workflow.id == workflow_id, Workflow.tenant_id == tenant_id).first()
        if not workflow:
            return None
        
        workflow.status = "paused" if workflow.status == "running" else "running"
        self.db.commit()
        return workflow.status

    async def trigger_workflow(self, tenant_id: str, workflow_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        workflow = self.db.query(Workflow).filter(Workflow.id == workflow_id, Workflow.tenant_id == tenant_id).first()
        if not workflow:
            raise ValueError("Workflow not found")
            
        if not self.workflow_port:
            logger.warning("WorkflowPort not configured, simulating trigger")
            return {"status": "simulated", "workflow_id": workflow_id}

        # Actual Temporal trigger logic would go here
        try:
            run_id = await self.workflow_port.start_workflow(
                workflow_name=workflow.name,
                workflow_id=f"{tenant_id}-{workflow_id}",
                task_queue=f"queue-{tenant_id}",
                args=[params] if params else []
            )
            return {"status": "started", "run_id": run_id}
        except Exception as e:
            logger.error(f"Failed to start workflow {workflow_id}: {e}")
            return {"status": "error", "message": str(e)}
