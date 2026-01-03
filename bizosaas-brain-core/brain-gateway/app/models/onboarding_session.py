"""
OnboardingSession Model - Persistent storage for multi-step onboarding state.

This model replaces the in-memory MOCK_STORE to allow:
- Draft saving and resuming
- Multi-session persistence
- Tenant isolation
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON, ForeignKey, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.models import Base


class OnboardingStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class OnboardingSession(Base):
    """
    Stores the complete onboarding state for a tenant/user.
    Supports draft saving and multi-step progression.
    """
    __tablename__ = "onboarding_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Ownership
    tenant_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    
    # Progress Tracking
    current_step = Column(Integer, default=0)
    status = Column(SqlEnum(OnboardingStatus), default=OnboardingStatus.NOT_STARTED)
    is_complete = Column(Boolean, default=False)
    
    # Business Profile (Step 1-2)
    profile_data = Column(JSON, default=dict)
    # Keys: companyName, industry, location, gmbLink, website, phone, description
    
    # Digital Presence (Step 3)
    digital_presence_data = Column(JSON, default=dict)
    # Keys: websiteDetected, cmsType, crmType, hasTracking
    
    # Analytics & Social (Step 4-5)
    analytics_config = Column(JSON, default=dict)
    # Keys: gaId, gscId, setupLater
    
    social_media_config = Column(JSON, default=dict)
    # Keys: platforms[], facebookPageId, instagramHandle, etc.
    
    # Goals & Strategy (Step 6-7)
    campaign_goals = Column(JSON, default=dict)
    # Keys: primaryGoal, secondaryGoals[], monthlyBudget, currency, targetAudience
    
    # Tool Integration (Step 8-9)
    tool_integration = Column(JSON, default=dict)
    # Keys: selectedMcps[], emailMarketing, adPlatforms[], wordpress, fluentCrm, wooCommerce
    
    # AI Agent Config (Step 10)
    agent_config = Column(JSON, default=dict)
    # Keys: persona, name, tone
    
    # Strategy Validation (PRD Step 11 - Feasibility Loop)
    strategy_validated = Column(Boolean, default=False)
    strategy_feedback = Column(JSON, default=list)  # List of AI feedback iterations
    
    # Audit Results (Background processing)
    audit_results = Column(JSON, default=dict)
    audit_completed_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    def to_dict(self):
        """Serialize session to dictionary for API responses."""
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "currentStep": self.current_step,
            "status": self.status.value if self.status else "not_started",
            "isComplete": self.is_complete,
            "profile": self.profile_data or {},
            "digitalPresence": self.digital_presence_data or {},
            "analytics": self.analytics_config or {},
            "socialMedia": self.social_media_config or {},
            "goals": self.campaign_goals or {},
            "tools": self.tool_integration or {},
            "agent": self.agent_config or {},
            "strategyValidated": self.strategy_validated,
            "strategyFeedback": self.strategy_feedback or [],
            "auditResults": self.audit_results or {},
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def update_step(self, step: int, data: dict, step_key: str):
        """Update a specific step's data and advance progress."""
        step_mapping = {
            "profile": "profile_data",
            "digitalPresence": "digital_presence_data",
            "analytics": "analytics_config",
            "socialMedia": "social_media_config",
            "goals": "campaign_goals",
            "tools": "tool_integration",
            "agent": "agent_config",
        }
        
        if step_key in step_mapping:
            setattr(self, step_mapping[step_key], data)
        
        if step > self.current_step:
            self.current_step = step
            
        if self.status == OnboardingStatus.NOT_STARTED:
            self.status = OnboardingStatus.IN_PROGRESS
            
        self.updated_at = datetime.utcnow()
