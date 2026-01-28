from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
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
            # Update last run even in simulation
            workflow.last_run = datetime.utcnow()
            workflow.runs_today += 1
            self.db.commit()
            return {"status": "simulated", "workflow_id": workflow_id}

        # Actual Temporal trigger logic would go here
        try:
            run_id = await self.workflow_port.start_workflow(
                workflow_name=workflow.name,
                workflow_id=f"{tenant_id}-{workflow_id}",
                task_queue=f"queue-{tenant_id}",
                args=[params] if params else []
            )
            workflow.last_run = datetime.utcnow()
            workflow.last_run_id = run_id
            workflow.runs_today += 1
            self.db.commit()
            return {"status": "started", "run_id": run_id}
        except Exception as e:
            logger.error(f"Failed to start workflow {workflow_id}: {e}")
            return {"status": "error", "message": str(e)}

    async def set_triggers(self, tenant_id: str, workflow_id: str, triggers: List[Dict[str, Any]]) -> bool:
        """Configure autonomous triggers for a workflow"""
        workflow = self.db.query(Workflow).filter(Workflow.id == workflow_id, Workflow.tenant_id == tenant_id).first()
        if not workflow:
            return False
        
        workflow.triggers = triggers
        self.db.commit()
        return True

    async def find_workflows_by_trigger(self, trigger_type: str, match_key: str, match_value: str) -> List[Workflow]:
        """Find all workflows across all tenants that match a specific trigger condition"""
        # Note: This is a bit inefficient with JSON columns in some DBs, 
        # but works for small/medium scale.
        # Format: trigger = {"type": "webhook", "path": "/listen-1"}
        all_workflows = self.db.query(Workflow).filter(Workflow.status == "running").all()
        matched = []
        for wf in all_workflows:
            for trigger in (wf.triggers or []):
                if trigger.get("type") == trigger_type and trigger.get(match_key) == match_value:
                    matched.append(wf)
        return matched
