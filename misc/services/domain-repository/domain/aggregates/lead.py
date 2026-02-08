"""
Lead Aggregate - Central domain model for lead management

This aggregate handles lead lifecycle including:
- Lead creation from various sources
- Lead qualification and scoring
- Status transitions
- Contact information management
- Lead-to-customer conversion
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator
from sqlalchemy import Column, String, DateTime, Numeric, Text, Enum as SQLEnum, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from .base import AggregateRoot, DomainEvent, ValueObject, BaseEntity, BusinessRuleViolation


class LeadSource(str, Enum):
    """Sources from which leads can be generated"""
    WEBSITE_FORM = "website_form"
    SOCIAL_MEDIA = "social_media"
    EMAIL_CAMPAIGN = "email_campaign"
    REFERRAL = "referral"
    COLD_OUTREACH = "cold_outreach"
    ADVERTISING = "advertising"
    WEBINAR = "webinar"
    TRADE_SHOW = "trade_show"
    ORGANIC_SEARCH = "organic_search"
    PAID_SEARCH = "paid_search"
    DIRECT = "direct"
    PARTNER = "partner"
    OTHER = "other"


class LeadStatus(str, Enum):
    """Lead status throughout the lifecycle"""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    UNQUALIFIED = "unqualified"
    NURTURING = "nurturing"
    PROPOSAL_SENT = "proposal_sent"
    NEGOTIATION = "negotiation"
    CONVERTED = "converted"
    LOST = "lost"
    RECYCLED = "recycled"


class LeadPriority(str, Enum):
    """Lead priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class ContactInfo(ValueObject):
    """Value object for lead contact information"""
    
    email: Optional[str] = None
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    
    @validator('email')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Invalid email format')
        return v
    
    @property
    def full_name(self) -> str:
        """Get full name from first and last name"""
        parts = [self.first_name, self.last_name]
        return ' '.join(filter(None, parts))
    
    @property
    def display_name(self) -> str:
        """Get the best display name available"""
        if self.full_name.strip():
            return self.full_name
        if self.email:
            return self.email
        if self.company:
            return self.company
        return "Unknown"


class LeadScore(ValueObject):
    """Value object for lead scoring"""
    
    total_score: int = 0
    demographic_score: int = 0
    behavioral_score: int = 0
    firmographic_score: int = 0
    engagement_score: int = 0
    last_calculated: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('total_score', 'demographic_score', 'behavioral_score', 'firmographic_score', 'engagement_score')
    def validate_score_range(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Score must be between 0 and 100')
        return v


class LeadQualificationCriteria(ValueObject):
    """Value object for lead qualification criteria"""
    
    budget_range: Optional[str] = None
    timeline: Optional[str] = None
    decision_maker: bool = False
    pain_points: List[str] = Field(default_factory=list)
    use_case: Optional[str] = None
    company_size: Optional[str] = None
    industry: Optional[str] = None


class InteractionRecord(ValueObject):
    """Value object for tracking lead interactions"""
    
    interaction_id: UUID = Field(default_factory=uuid4)
    interaction_type: str  # email, call, meeting, form_submission, etc.
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    details: Dict[str, Any] = Field(default_factory=dict)
    user_id: Optional[UUID] = None
    channel: Optional[str] = None
    outcome: Optional[str] = None


# Domain Events
class LeadCreated(DomainEvent):
    """Event raised when a new lead is created"""
    event_type: str = "lead.created"


class LeadStatusChanged(DomainEvent):
    """Event raised when lead status changes"""
    event_type: str = "lead.status_changed"


class LeadQualified(DomainEvent):
    """Event raised when a lead is qualified"""
    event_type: str = "lead.qualified"


class LeadScoreUpdated(DomainEvent):
    """Event raised when lead score is updated"""
    event_type: str = "lead.score_updated"


class LeadConverted(DomainEvent):
    """Event raised when a lead is converted to customer"""
    event_type: str = "lead.converted"


class LeadAssigned(DomainEvent):
    """Event raised when a lead is assigned to a user"""
    event_type: str = "lead.assigned"


class LeadInteractionAdded(DomainEvent):
    """Event raised when an interaction is recorded"""
    event_type: str = "lead.interaction_added"


# Lead Aggregate Root
class Lead(AggregateRoot):
    """
    Lead aggregate root - manages lead lifecycle and business rules
    """
    
    # Basic Information
    source: LeadSource
    status: LeadStatus = LeadStatus.NEW
    priority: LeadPriority = LeadPriority.MEDIUM
    contact_info: ContactInfo
    
    # Qualification and Scoring
    score: LeadScore = Field(default_factory=LeadScore)
    qualification_criteria: Optional[LeadQualificationCriteria] = None
    is_qualified: bool = False
    qualification_date: Optional[datetime] = None
    
    # Assignment and Ownership
    assigned_to: Optional[UUID] = None
    assigned_at: Optional[datetime] = None
    assigned_by: Optional[UUID] = None
    
    # Conversion
    converted_to_customer_id: Optional[UUID] = None
    conversion_date: Optional[datetime] = None
    conversion_value: Optional[Decimal] = None
    
    # Tracking and Analytics
    interactions: List[InteractionRecord] = Field(default_factory=list)
    utm_parameters: Dict[str, str] = Field(default_factory=dict)
    referrer_url: Optional[str] = None
    landing_page: Optional[str] = None
    
    # Campaign and Attribution
    campaign_id: Optional[UUID] = None
    attribution_data: Dict[str, Any] = Field(default_factory=dict)
    
    # Custom Fields and Notes
    custom_fields: Dict[str, Any] = Field(default_factory=dict)
    notes: List[str] = Field(default_factory=list)
    tags: Set[str] = Field(default_factory=set)
    
    def __init__(self, **data):
        super().__init__(**data)
        
        # Raise creation event
        self.add_domain_event(LeadCreated(
            aggregate_id=self.id,
            aggregate_type="Lead",
            tenant_id=self.tenant_id,
            data={
                "lead_id": str(self.id),
                "source": self.source.value,
                "contact_info": self.contact_info.dict(),
                "utm_parameters": self.utm_parameters,
                "campaign_id": str(self.campaign_id) if self.campaign_id else None
            }
        ))
    
    def change_status(self, new_status: LeadStatus, user_id: Optional[UUID] = None, reason: Optional[str] = None) -> None:
        """Change lead status with business rule validation"""
        
        if new_status == self.status:
            return  # No change needed
        
        # Validate status transition
        if not self._is_valid_status_transition(self.status, new_status):
            raise BusinessRuleViolation(
                f"Invalid status transition from {self.status.value} to {new_status.value}",
                details={"current_status": self.status.value, "new_status": new_status.value}
            )
        
        old_status = self.status
        self.status = new_status
        self.increment_version()
        
        # Handle specific status changes
        if new_status == LeadStatus.QUALIFIED:
            self.qualify_lead(user_id)
        elif new_status == LeadStatus.CONVERTED:
            if not self.is_qualified:
                raise BusinessRuleViolation("Cannot convert unqualified lead")
        
        # Record interaction
        self.add_interaction(
            interaction_type="status_change",
            user_id=user_id,
            details={
                "old_status": old_status.value,
                "new_status": new_status.value,
                "reason": reason
            }
        )
        
        # Raise status change event
        self.add_domain_event(LeadStatusChanged(
            aggregate_id=self.id,
            aggregate_type="Lead",
            tenant_id=self.tenant_id,
            data={
                "lead_id": str(self.id),
                "old_status": old_status.value,
                "new_status": new_status.value,
                "changed_by": str(user_id) if user_id else None,
                "reason": reason
            }
        ))
    
    def qualify_lead(self, user_id: Optional[UUID] = None, criteria: Optional[LeadQualificationCriteria] = None) -> None:
        """Qualify the lead"""
        
        if self.is_qualified:
            return  # Already qualified
        
        self.is_qualified = True
        self.qualification_date = datetime.utcnow()
        
        if criteria:
            self.qualification_criteria = criteria
        
        self.increment_version()
        
        # Raise qualification event
        self.add_domain_event(LeadQualified(
            aggregate_id=self.id,
            aggregate_type="Lead",
            tenant_id=self.tenant_id,
            data={
                "lead_id": str(self.id),
                "qualified_by": str(user_id) if user_id else None,
                "qualification_criteria": criteria.dict() if criteria else None,
                "qualification_date": self.qualification_date.isoformat()
            }
        ))
    
    def update_score(self, new_score: LeadScore, user_id: Optional[UUID] = None) -> None:
        """Update lead score"""
        
        old_score = self.score.total_score
        self.score = new_score
        self.increment_version()
        
        # Raise score update event
        self.add_domain_event(LeadScoreUpdated(
            aggregate_id=self.id,
            aggregate_type="Lead",
            tenant_id=self.tenant_id,
            data={
                "lead_id": str(self.id),
                "old_score": old_score,
                "new_score": new_score.total_score,
                "score_breakdown": new_score.dict(),
                "updated_by": str(user_id) if user_id else None
            }
        ))
        
        # Auto-qualify high-scoring leads
        if new_score.total_score >= 80 and not self.is_qualified:
            self.qualify_lead(user_id)
    
    def assign_to_user(self, user_id: UUID, assigned_by: Optional[UUID] = None) -> None:
        """Assign lead to a user"""
        
        if self.assigned_to == user_id:
            return  # Already assigned to this user
        
        old_assignee = self.assigned_to
        self.assigned_to = user_id
        self.assigned_at = datetime.utcnow()
        self.assigned_by = assigned_by
        self.increment_version()
        
        # Record interaction
        self.add_interaction(
            interaction_type="assignment",
            user_id=assigned_by,
            details={
                "old_assignee": str(old_assignee) if old_assignee else None,
                "new_assignee": str(user_id),
                "assigned_by": str(assigned_by) if assigned_by else None
            }
        )
        
        # Raise assignment event
        self.add_domain_event(LeadAssigned(
            aggregate_id=self.id,
            aggregate_type="Lead",
            tenant_id=self.tenant_id,
            data={
                "lead_id": str(self.id),
                "assigned_to": str(user_id),
                "assigned_by": str(assigned_by) if assigned_by else None,
                "old_assignee": str(old_assignee) if old_assignee else None
            }
        ))
    
    def convert_to_customer(self, customer_id: UUID, conversion_value: Optional[Decimal] = None, user_id: Optional[UUID] = None) -> None:
        """Convert lead to customer"""
        
        if not self.is_qualified:
            raise BusinessRuleViolation("Cannot convert unqualified lead")
        
        if self.status == LeadStatus.CONVERTED:
            raise BusinessRuleViolation("Lead is already converted")
        
        self.converted_to_customer_id = customer_id
        self.conversion_date = datetime.utcnow()
        self.conversion_value = conversion_value
        self.status = LeadStatus.CONVERTED
        self.increment_version()
        
        # Record interaction
        self.add_interaction(
            interaction_type="conversion",
            user_id=user_id,
            details={
                "customer_id": str(customer_id),
                "conversion_value": float(conversion_value) if conversion_value else None
            }
        )
        
        # Raise conversion event
        self.add_domain_event(LeadConverted(
            aggregate_id=self.id,
            aggregate_type="Lead",
            tenant_id=self.tenant_id,
            data={
                "lead_id": str(self.id),
                "customer_id": str(customer_id),
                "conversion_value": float(conversion_value) if conversion_value else None,
                "converted_by": str(user_id) if user_id else None,
                "conversion_date": self.conversion_date.isoformat()
            }
        ))
    
    def add_interaction(self, interaction_type: str, user_id: Optional[UUID] = None, details: Optional[Dict[str, Any]] = None, channel: Optional[str] = None, outcome: Optional[str] = None) -> None:
        """Add an interaction record"""
        
        interaction = InteractionRecord(
            interaction_type=interaction_type,
            user_id=user_id,
            details=details or {},
            channel=channel,
            outcome=outcome
        )
        
        self.interactions.append(interaction)
        self.increment_version()
        
        # Raise interaction event
        self.add_domain_event(LeadInteractionAdded(
            aggregate_id=self.id,
            aggregate_type="Lead",
            tenant_id=self.tenant_id,
            data={
                "lead_id": str(self.id),
                "interaction": interaction.dict(),
                "interaction_count": len(self.interactions)
            }
        ))
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the lead"""
        self.tags.add(tag.lower().strip())
        self.increment_version()
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the lead"""
        self.tags.discard(tag.lower().strip())
        self.increment_version()
    
    def update_contact_info(self, contact_info: ContactInfo) -> None:
        """Update contact information"""
        self.contact_info = contact_info
        self.increment_version()
    
    def add_note(self, note: str, user_id: Optional[UUID] = None) -> None:
        """Add a note to the lead"""
        timestamp = datetime.utcnow().isoformat()
        formatted_note = f"[{timestamp}] {note}"
        if user_id:
            formatted_note = f"[{timestamp}] [{user_id}] {note}"
        
        self.notes.append(formatted_note)
        self.increment_version()
    
    def _is_valid_status_transition(self, from_status: LeadStatus, to_status: LeadStatus) -> bool:
        """Validate if status transition is allowed"""
        
        # Define allowed transitions
        allowed_transitions = {
            LeadStatus.NEW: [LeadStatus.CONTACTED, LeadStatus.QUALIFIED, LeadStatus.UNQUALIFIED, LeadStatus.LOST],
            LeadStatus.CONTACTED: [LeadStatus.QUALIFIED, LeadStatus.UNQUALIFIED, LeadStatus.NURTURING, LeadStatus.LOST],
            LeadStatus.QUALIFIED: [LeadStatus.PROPOSAL_SENT, LeadStatus.NEGOTIATION, LeadStatus.CONVERTED, LeadStatus.LOST, LeadStatus.NURTURING],
            LeadStatus.UNQUALIFIED: [LeadStatus.RECYCLED, LeadStatus.LOST],
            LeadStatus.NURTURING: [LeadStatus.QUALIFIED, LeadStatus.CONTACTED, LeadStatus.LOST],
            LeadStatus.PROPOSAL_SENT: [LeadStatus.NEGOTIATION, LeadStatus.CONVERTED, LeadStatus.LOST, LeadStatus.NURTURING],
            LeadStatus.NEGOTIATION: [LeadStatus.CONVERTED, LeadStatus.LOST, LeadStatus.PROPOSAL_SENT],
            LeadStatus.CONVERTED: [],  # Final state
            LeadStatus.LOST: [LeadStatus.RECYCLED],
            LeadStatus.RECYCLED: [LeadStatus.NEW, LeadStatus.CONTACTED, LeadStatus.NURTURING]
        }
        
        return to_status in allowed_transitions.get(from_status, [])
    
    @property
    def age_in_days(self) -> int:
        """Get lead age in days"""
        return (datetime.utcnow() - self.created_at).days
    
    @property
    def last_interaction_date(self) -> Optional[datetime]:
        """Get the date of the last interaction"""
        if not self.interactions:
            return None
        return max(interaction.timestamp for interaction in self.interactions)
    
    @property
    def interaction_count(self) -> int:
        """Get total number of interactions"""
        return len(self.interactions)


# SQLAlchemy Model for Persistence
class LeadEntity(BaseEntity):
    """SQLAlchemy model for Lead persistence"""
    
    __tablename__ = "leads"
    
    # Basic Information
    source = Column(SQLEnum(LeadSource), nullable=False)
    status = Column(SQLEnum(LeadStatus), nullable=False, default=LeadStatus.NEW)
    priority = Column(SQLEnum(LeadPriority), nullable=False, default=LeadPriority.MEDIUM)
    
    # Contact Information (stored as JSON)
    contact_info = Column(JSON, nullable=False)
    
    # Qualification and Scoring
    score_data = Column(JSON)  # LeadScore as JSON
    qualification_criteria = Column(JSON)  # LeadQualificationCriteria as JSON
    is_qualified = Column(Boolean, default=False)
    qualification_date = Column(DateTime)
    
    # Assignment
    assigned_to = Column(PGUUID(as_uuid=True))
    assigned_at = Column(DateTime)
    assigned_by = Column(PGUUID(as_uuid=True))
    
    # Conversion
    converted_to_customer_id = Column(PGUUID(as_uuid=True))
    conversion_date = Column(DateTime)
    conversion_value = Column(Numeric(10, 2))
    
    # Tracking
    interactions = Column(JSON, default=list)  # List of InteractionRecord as JSON
    utm_parameters = Column(JSON, default=dict)
    referrer_url = Column(String(500))
    landing_page = Column(String(500))
    
    # Campaign and Attribution
    campaign_id = Column(PGUUID(as_uuid=True))
    attribution_data = Column(JSON, default=dict)
    
    # Custom Fields
    custom_fields = Column(JSON, default=dict)
    notes = Column(JSON, default=list)
    tags = Column(JSON, default=list)  # Convert set to list for JSON storage
    
    def to_domain(self) -> Lead:
        """Convert SQLAlchemy model to domain aggregate"""
        
        # Convert JSON data back to value objects
        contact_info = ContactInfo(**self.contact_info) if self.contact_info else ContactInfo()
        score = LeadScore(**self.score_data) if self.score_data else LeadScore()
        qualification_criteria = LeadQualificationCriteria(**self.qualification_criteria) if self.qualification_criteria else None
        
        # Convert interactions
        interactions = [InteractionRecord(**interaction) for interaction in (self.interactions or [])]
        
        return Lead(
            id=self.id,
            tenant_id=self.tenant_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            version=self.version,
            source=self.source,
            status=self.status,
            priority=self.priority,
            contact_info=contact_info,
            score=score,
            qualification_criteria=qualification_criteria,
            is_qualified=self.is_qualified,
            qualification_date=self.qualification_date,
            assigned_to=self.assigned_to,
            assigned_at=self.assigned_at,
            assigned_by=self.assigned_by,
            converted_to_customer_id=self.converted_to_customer_id,
            conversion_date=self.conversion_date,
            conversion_value=self.conversion_value,
            interactions=interactions,
            utm_parameters=self.utm_parameters or {},
            referrer_url=self.referrer_url,
            landing_page=self.landing_page,
            campaign_id=self.campaign_id,
            attribution_data=self.attribution_data or {},
            custom_fields=self.custom_fields or {},
            notes=self.notes or [],
            tags=set(self.tags or [])
        )
    
    @classmethod
    def from_domain(cls, domain_lead: Lead) -> 'LeadEntity':
        """Create SQLAlchemy model from domain aggregate"""
        
        return cls(
            id=domain_lead.id,
            tenant_id=domain_lead.tenant_id,
            created_at=domain_lead.created_at,
            updated_at=domain_lead.updated_at,
            version=domain_lead.version,
            source=domain_lead.source,
            status=domain_lead.status,
            priority=domain_lead.priority,
            contact_info=domain_lead.contact_info.dict(),
            score_data=domain_lead.score.dict(),
            qualification_criteria=domain_lead.qualification_criteria.dict() if domain_lead.qualification_criteria else None,
            is_qualified=domain_lead.is_qualified,
            qualification_date=domain_lead.qualification_date,
            assigned_to=domain_lead.assigned_to,
            assigned_at=domain_lead.assigned_at,
            assigned_by=domain_lead.assigned_by,
            converted_to_customer_id=domain_lead.converted_to_customer_id,
            conversion_date=domain_lead.conversion_date,
            conversion_value=domain_lead.conversion_value,
            interactions=[interaction.dict() for interaction in domain_lead.interactions],
            utm_parameters=domain_lead.utm_parameters,
            referrer_url=domain_lead.referrer_url,
            landing_page=domain_lead.landing_page,
            campaign_id=domain_lead.campaign_id,
            attribution_data=domain_lead.attribution_data,
            custom_fields=domain_lead.custom_fields,
            notes=domain_lead.notes,
            tags=list(domain_lead.tags)
        )