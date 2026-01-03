"""
OnboardingSessionService - Business logic for onboarding state management.

Provides CRUD operations and step-by-step progression handling.
"""

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.models.onboarding_session import OnboardingSession, OnboardingStatus


class OnboardingSessionService:
    """Service layer for managing onboarding sessions."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_session(self, tenant_id: str, user_id: str) -> OnboardingSession:
        """
        Get existing session or create a new one.
        Each user has one active onboarding session at a time.
        """
        session = self.db.query(OnboardingSession).filter(
            OnboardingSession.tenant_id == tenant_id,
            OnboardingSession.user_id == user_id,
            OnboardingSession.is_complete == False
        ).first()
        
        if not session:
            session = OnboardingSession(
                tenant_id=tenant_id,
                user_id=user_id,
                status=OnboardingStatus.NOT_STARTED
            )
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)
        
        return session
    
    def get_session(self, tenant_id: str, user_id: str) -> Optional[OnboardingSession]:
        """Get the current active session for a user."""
        return self.db.query(OnboardingSession).filter(
            OnboardingSession.tenant_id == tenant_id,
            OnboardingSession.user_id == user_id,
            OnboardingSession.is_complete == False
        ).first()
    
    def get_session_by_id(self, session_id: uuid.UUID) -> Optional[OnboardingSession]:
        """Get a session by its ID."""
        return self.db.query(OnboardingSession).filter(
            OnboardingSession.id == session_id
        ).first()
    
    def save_step(
        self, 
        tenant_id: str, 
        user_id: str, 
        step: int, 
        step_key: str, 
        data: Dict[str, Any]
    ) -> OnboardingSession:
        """
        Save data for a specific onboarding step.
        Creates session if it doesn't exist.
        """
        session = self.get_or_create_session(tenant_id, user_id)
        session.update_step(step, data, step_key)
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def save_profile(self, tenant_id: str, user_id: str, profile_data: Dict[str, Any]) -> OnboardingSession:
        """Save business profile data (Step 1-2)."""
        return self.save_step(tenant_id, user_id, 2, "profile", profile_data)
    
    def save_digital_presence(self, tenant_id: str, user_id: str, data: Dict[str, Any]) -> OnboardingSession:
        """Save digital presence data (Step 3)."""
        return self.save_step(tenant_id, user_id, 3, "digitalPresence", data)
    
    def save_analytics(self, tenant_id: str, user_id: str, data: Dict[str, Any]) -> OnboardingSession:
        """Save analytics config (Step 4)."""
        return self.save_step(tenant_id, user_id, 4, "analytics", data)
    
    def save_social_media(self, tenant_id: str, user_id: str, data: Dict[str, Any]) -> OnboardingSession:
        """Save social media config (Step 5)."""
        return self.save_step(tenant_id, user_id, 5, "socialMedia", data)
    
    def save_goals(self, tenant_id: str, user_id: str, data: Dict[str, Any]) -> OnboardingSession:
        """Save campaign goals (Step 6-7)."""
        return self.save_step(tenant_id, user_id, 7, "goals", data)
    
    def save_tools(self, tenant_id: str, user_id: str, data: Dict[str, Any]) -> OnboardingSession:
        """Save tool integrations (Step 8-9)."""
        return self.save_step(tenant_id, user_id, 9, "tools", data)
    
    def save_agent_config(self, tenant_id: str, user_id: str, data: Dict[str, Any]) -> OnboardingSession:
        """Save AI agent configuration (Step 10)."""
        return self.save_step(tenant_id, user_id, 10, "agent", data)
    
    def mark_strategy_validated(
        self, 
        tenant_id: str, 
        user_id: str, 
        feedback: Dict[str, Any]
    ) -> OnboardingSession:
        """Mark strategy as validated after feasibility check (Step 11)."""
        session = self.get_or_create_session(tenant_id, user_id)
        
        if session.strategy_feedback is None:
            session.strategy_feedback = []
        session.strategy_feedback.append(feedback)
        session.strategy_validated = True
        session.current_step = max(session.current_step, 11)
        
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def save_audit_results(
        self, 
        tenant_id: str, 
        user_id: str, 
        audit_results: Dict[str, Any]
    ) -> OnboardingSession:
        """Save background audit results."""
        session = self.get_or_create_session(tenant_id, user_id)
        session.audit_results = audit_results
        session.audit_completed_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def complete_onboarding(self, tenant_id: str, user_id: str) -> OnboardingSession:
        """Mark onboarding as complete."""
        session = self.get_or_create_session(tenant_id, user_id)
        session.is_complete = True
        session.status = OnboardingStatus.COMPLETED
        session.completed_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def get_status(self, tenant_id: str, user_id: str) -> Dict[str, Any]:
        """Get onboarding status for API response."""
        session = self.get_session(tenant_id, user_id)
        
        if not session:
            return {
                "isConnectionSuccess": True,
                "isComplete": False,
                "currentStep": 0,
                "status": "not_started"
            }
        
        return {
            "isConnectionSuccess": True,
            "isComplete": session.is_complete,
            "currentStep": session.current_step,
            "status": session.status.value if session.status else "not_started",
            "sessionId": str(session.id)
        }
    
    def get_draft(self, tenant_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get the full draft state for resuming onboarding."""
        session = self.get_session(tenant_id, user_id)
        
        if not session:
            return None
        
        return session.to_dict()
