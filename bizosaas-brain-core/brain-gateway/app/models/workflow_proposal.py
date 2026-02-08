"""
Workflow Proposal Model
Represents agent-proposed workflows awaiting admin approval.
"""

from sqlalchemy import Column, String, DateTime, JSON, Float, Text, Enum
from sqlalchemy.sql import func
from .base import Base
import enum


class WorkflowStatus(str, enum.Enum):
    """Workflow lifecycle states"""
    PROPOSED = "proposed"
    REFINEMENT_REQUESTED = "refinement_requested"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class WorkflowProposal(Base):
    """
    Agent-proposed workflows that require admin approval before deployment.
    This is the core of the autonomous agentic feedback loop.
    """
    __tablename__ = "workflow_proposals"

    id = Column(String, primary_key=True, default=lambda: f"wfp_{func.gen_random_uuid()}")
    name = Column(String, nullable=False)
    description = Column(Text)
    type = Column(String, nullable=False)  # Marketing, Operations, Security, etc.
    category = Column(String, nullable=False)  # infrastructure, hitl, all
    status = Column(Enum(WorkflowStatus), default=WorkflowStatus.PROPOSED, nullable=False)
    
    # Workflow definition (JSON/YAML blueprint)
    workflow_definition = Column(JSON, nullable=False)
    
    # Discovery metadata
    discovered_by = Column(String, nullable=False)  # Agent identifier
    discovery_method = Column(String)  # RAG, KAG, Manual, etc.
    estimated_cost = Column(Float)  # Estimated monthly cost
    impact_analysis = Column(Text)  # AI-generated impact assessment
    
    # Admin review
    admin_feedback = Column(Text)
    suggested_changes = Column(JSON)
    approved_by = Column(String)
    rejected_by = Column(String)
    admin_notes = Column(Text)
    rejection_reason = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    approved_at = Column(DateTime(timezone=True))
    rejected_at = Column(DateTime(timezone=True))
    refinement_requested_at = Column(DateTime(timezone=True))
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "category": self.category,
            "status": self.status.value if isinstance(self.status, enum.Enum) else self.status,
            "workflow_definition": self.workflow_definition,
            "discovered_by": self.discovered_by,
            "discovery_method": self.discovery_method,
            "estimated_cost": self.estimated_cost,
            "impact_analysis": self.impact_analysis,
            "admin_feedback": self.admin_feedback,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
        }
