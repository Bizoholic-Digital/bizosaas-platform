"""
StrategyValidation Model - Stores AI-powered strategy validation results.

Implements PRD Step 11: Feasibility check loop where AI analyzes client goals
against historical data and provides refinement recommendations.
"""

from sqlalchemy import Column, String, Float, Boolean, DateTime, JSON, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import enum

from app.models import Base


class ValidationStatus(str, enum.Enum):
    PENDING = "pending"
    ANALYZING = "analyzing"
    NEEDS_REFINEMENT = "needs_refinement"
    APPROVED = "approved"
    REJECTED = "rejected"


class StrategyValidation(Base):
    """
    Stores strategy validation results from the AI feasibility engine.
    Links to onboarding sessions for the strategy refinement loop.
    """
    __tablename__ = "strategy_validations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Ownership
    tenant_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False)
    onboarding_session_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Input: Client's Proposed Strategy
    proposed_goal = Column(String, nullable=False)  # e.g., "lead_gen", "ecommerce_sales"
    proposed_budget = Column(Float, nullable=False)
    proposed_currency = Column(String, default="USD")
    proposed_platforms = Column(JSON, default=list)  # e.g., ["google-ads", "facebook-ads"]
    target_audience = Column(JSON, default=dict)  # Location, age, interests
    timeline_months = Column(Float, default=3.0)
    
    # Analysis Results
    status = Column(String, default=ValidationStatus.PENDING.value)
    
    # AI Scoring (0-100)
    feasibility_score = Column(Float, nullable=True)  # Overall score
    budget_adequacy_score = Column(Float, nullable=True)
    platform_fit_score = Column(Float, nullable=True)
    audience_reach_score = Column(Float, nullable=True)
    timeline_realism_score = Column(Float, nullable=True)
    
    # AI Recommendations
    ai_analysis = Column(Text, nullable=True)  # Detailed analysis text
    recommendations = Column(JSON, default=list)  # Structured recommendations
    suggested_adjustments = Column(JSON, default=dict)  # Specific value changes
    
    # Historical Data Used
    benchmark_data = Column(JSON, default=dict)  # Industry/platform benchmarks
    connector_insights = Column(JSON, default=dict)  # Data from connected platforms
    
    # Iteration Tracking (PRD Step 11 loop)
    iteration_number = Column(Integer, default=1)
    previous_validation_id = Column(UUID(as_uuid=True), nullable=True)
    refinement_accepted = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "status": self.status,
            "feasibilityScore": self.feasibility_score,
            "budgetAdequacyScore": self.budget_adequacy_score,
            "platformFitScore": self.platform_fit_score,
            "audienceReachScore": self.audience_reach_score,
            "timelineRealismScore": self.timeline_realism_score,
            "analysis": self.ai_analysis,
            "recommendations": self.recommendations or [],
            "suggestedAdjustments": self.suggested_adjustments or {},
            "benchmarkData": self.benchmark_data or {},
            "iterationNumber": self.iteration_number,
            "refinementAccepted": self.refinement_accepted,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }
    
    def is_feasible(self) -> bool:
        """Check if strategy meets minimum feasibility threshold."""
        return self.feasibility_score is not None and self.feasibility_score >= 60



