from sqlalchemy import Column, String, JSON, DateTime, ForeignKey, Boolean, Float, Integer, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .user import Base
from .utils import GUID

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    type = Column(String) # 'Marketing', 'E-commerce', 'Content', etc.
    status = Column(String, default="running") # 'running', 'paused', 'error', 'active'
    category = Column(String, default="all")  # 'infrastructure', 'hitl', 'all'
    config = Column(JSON, default={}) # retries, timeout, etc.
    workflow_blueprint = Column(JSON)  # Complete workflow definition from agent proposal
    triggers = Column(JSON, default=[]) # List of triggers: {type: 'webhook', 'schedule', 'event'}
    last_run = Column(DateTime, nullable=True)
    last_run_id = Column(String) # Temporal run_id for latest execution
    success_rate = Column(Float, default=100.0)
    runs_today = Column(Integer, default=0)
    
    # Approval tracking
    approved_by = Column(String)
    approved_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "status": self.status,
            "category": self.category,
            "config": self.config,
            "workflow_blueprint": self.workflow_blueprint,
            "triggers": self.triggers,
            "lastRun": self.last_run.isoformat() if self.last_run else None,
            "lastRunId": self.last_run_id,
            "successRate": self.success_rate,
            "runsToday": self.runs_today,
            "approvedBy": self.approved_by,
            "approvedAt": self.approved_at.isoformat() if self.approved_at else None,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None
        }

class WorkflowProposal(Base):
    __tablename__ = "workflow_proposals"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    type = Column(String)
    category = Column(String, default="all")
    status = Column(String, default="proposed") # 'proposed', 'approved', 'rejected', 'refinement_requested'
    workflow_definition = Column(JSON)
    estimated_cost = Column(Float)
    impact_analysis = Column(Text)
    discovered_by = Column(String)
    admin_notes = Column(Text)
    admin_feedback = Column(Text)
    suggested_changes = Column(JSON)
    
    # Audit trail
    approved_by = Column(String)
    approved_at = Column(DateTime)
    rejected_by = Column(String)
    rejected_at = Column(DateTime)
    refinement_requested_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "category": self.category,
            "status": self.status,
            "workflowDefinition": self.workflow_definition,
            "estimatedCost": self.estimated_cost,
            "impactAnalysis": self.impact_analysis,
            "discoveredBy": self.discovered_by,
            "adminNotes": self.admin_notes,
            "adminFeedback": self.admin_feedback,
            "suggestedChanges": self.suggested_changes,
            "approvedBy": self.approved_by,
            "approvedAt": self.approved_at.isoformat() if self.approved_at else None,
            "rejectedBy": self.rejected_by,
            "rejectedAt": self.rejected_at.isoformat() if self.rejected_at else None,
            "createdAt": self.created_at.isoformat() if self.created_at else None
        }
