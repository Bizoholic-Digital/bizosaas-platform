"""
CRM Data Models for SQLAdmin Dashboard
Handles contacts, leads, deals, activities, campaigns, and sales pipeline
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, JSON, ForeignKey, UUID, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class LeadStatus(enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class ContactType(enum.Enum):
    PROSPECT = "prospect"
    CUSTOMER = "customer"
    PARTNER = "partner"
    VENDOR = "vendor"
    OTHER = "other"

class DealStage(enum.Enum):
    DISCOVERY = "discovery"
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class ActivityType(enum.Enum):
    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    TASK = "task"
    NOTE = "note"
    DEMO = "demo"
    FOLLOW_UP = "follow_up"

class CampaignStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# Contacts - All people in the system
class ContactAdmin(Base):
    __tablename__ = "crm_contacts"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Personal details
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    full_name = Column(String(200))  # Computed field
    email = Column(String(255), index=True)
    phone = Column(String(20))
    mobile = Column(String(20))
    
    # Professional details
    job_title = Column(String(100))
    company = Column(String(200))
    industry = Column(String(100))
    website = Column(String(255))
    linkedin_url = Column(String(255))
    
    # Address
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))
    
    # Classification
    contact_type = Column(Enum(ContactType), default=ContactType.PROSPECT)
    source = Column(String(100))  # How they were acquired
    tags = Column(JSON, default=[])
    
    # Status and scoring
    is_active = Column(Boolean, default=True)
    lead_score = Column(Integer, default=0)
    engagement_score = Column(Float, default=0.0)
    last_contacted_at = Column(DateTime(timezone=True))
    
    # Social media
    social_profiles = Column(JSON, default={})  # {platform: url}
    
    # Custom fields and metadata
    custom_fields = Column(JSON, default={})
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    leads = relationship("LeadAdmin", back_populates="contact", cascade="all, delete-orphan")
    activities = relationship("ActivityAdmin", back_populates="contact")

# Leads - Potential sales opportunities
class LeadAdmin(Base):
    __tablename__ = "crm_leads"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("crm_contacts.id"))
    
    # Lead details
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    
    # Value and priority
    estimated_value = Column(Float)
    probability = Column(Float, default=0.0)  # 0-1 chance of closing
    priority = Column(String(20), default="medium")  # low, medium, high, urgent
    
    # Source and attribution
    source = Column(String(100))  # website, referral, campaign, etc.
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("crm_campaigns.id"))
    utm_source = Column(String(100))
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))
    
    # Timeline
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    first_contacted_at = Column(DateTime(timezone=True))
    last_contacted_at = Column(DateTime(timezone=True))
    expected_close_date = Column(DateTime(timezone=True))
    closed_at = Column(DateTime(timezone=True))
    
    # Assignment and ownership
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Qualification criteria
    budget_confirmed = Column(Boolean, default=False)
    authority_confirmed = Column(Boolean, default=False)
    need_confirmed = Column(Boolean, default=False)
    timeline_confirmed = Column(Boolean, default=False)
    
    # Custom fields and metadata
    custom_fields = Column(JSON, default={})
    tags = Column(JSON, default=[])
    
    # Relationships
    contact = relationship("ContactAdmin", back_populates="leads")
    deal = relationship("DealAdmin", uselist=False, back_populates="lead")
    activities = relationship("ActivityAdmin", back_populates="lead")
    campaign = relationship("CampaignAdmin", back_populates="leads")

# Deals - Active sales opportunities
class DealAdmin(Base):
    __tablename__ = "crm_deals"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("crm_leads.id"), unique=True)
    
    # Deal details
    name = Column(String(200), nullable=False)
    description = Column(Text)
    stage = Column(Enum(DealStage), default=DealStage.DISCOVERY)
    
    # Financial details
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    discount_amount = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    total_amount = Column(Float)  # Computed field
    
    # Probability and forecasting
    probability = Column(Float, default=0.0)  # 0-1 chance of closing
    weighted_amount = Column(Float)  # amount * probability
    expected_revenue = Column(Float)
    
    # Timeline
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    expected_close_date = Column(DateTime(timezone=True))
    actual_close_date = Column(DateTime(timezone=True))
    
    # Assignment and ownership
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Pipeline and process
    pipeline_id = Column(UUID(as_uuid=True))  # Reference to sales pipeline
    stage_entered_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    days_in_stage = Column(Integer, default=0)
    
    # Products and services
    products = Column(JSON, default=[])  # List of product IDs and quantities
    services = Column(JSON, default=[])  # List of service IDs
    
    # Competition and risks
    competitors = Column(JSON, default=[])
    risks = Column(JSON, default=[])
    risk_level = Column(String(20), default="low")
    
    # Custom fields and metadata
    custom_fields = Column(JSON, default={})
    tags = Column(JSON, default=[])
    
    # Relationships
    lead = relationship("LeadAdmin", back_populates="deal")
    activities = relationship("ActivityAdmin", back_populates="deal")

# Activities - All interactions and tasks
class ActivityAdmin(Base):
    __tablename__ = "crm_activities"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Activity details
    type = Column(Enum(ActivityType), nullable=False)
    subject = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Relationships
    contact_id = Column(UUID(as_uuid=True), ForeignKey("crm_contacts.id"))
    lead_id = Column(UUID(as_uuid=True), ForeignKey("crm_leads.id"))
    deal_id = Column(UUID(as_uuid=True), ForeignKey("crm_deals.id"))
    
    # Scheduling
    scheduled_at = Column(DateTime(timezone=True))
    due_date = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer)  # For calls, meetings
    
    # Status and priority
    is_completed = Column(Boolean, default=False)
    priority = Column(String(20), default="medium")
    status = Column(String(50), default="pending")
    
    # Assignment
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Communication details (for calls, emails)
    phone_number = Column(String(20))
    email_address = Column(String(255))
    meeting_link = Column(String(500))
    location = Column(String(255))
    
    # Outcome and results
    outcome = Column(String(100))  # connected, voicemail, no-answer, etc.
    result = Column(Text)  # Notes about the outcome
    next_action = Column(String(200))
    follow_up_date = Column(DateTime(timezone=True))
    
    # Metadata
    custom_fields = Column(JSON, default={})
    attachments = Column(JSON, default=[])  # File references
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    contact = relationship("ContactAdmin", back_populates="activities")
    lead = relationship("LeadAdmin", back_populates="activities")
    deal = relationship("DealAdmin", back_populates="activities")

# Campaigns - Marketing and sales campaigns
class CampaignAdmin(Base):
    __tablename__ = "crm_campaigns"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Campaign details
    name = Column(String(200), nullable=False)
    description = Column(Text)
    type = Column(String(50))  # email, social, ppc, content, webinar, etc.
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)
    
    # Timeline
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Budget and costs
    budget = Column(Float)
    actual_cost = Column(Float, default=0.0)
    cost_per_lead = Column(Float)
    cost_per_acquisition = Column(Float)
    
    # Performance metrics
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    leads_generated = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    revenue_generated = Column(Float, default=0.0)
    
    # Targeting and audience
    target_audience = Column(JSON, default={})
    audience_size = Column(Integer)
    demographic_filters = Column(JSON, default={})
    geographic_filters = Column(JSON, default={})
    
    # Content and assets
    creative_assets = Column(JSON, default=[])  # Images, videos, copy
    landing_page_url = Column(String(500))
    call_to_action = Column(String(200))
    
    # UTM parameters for tracking
    utm_source = Column(String(100))
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))
    utm_term = Column(String(100))
    utm_content = Column(String(100))
    
    # Channel-specific settings
    channel_settings = Column(JSON, default={})  # Platform-specific configuration
    automation_rules = Column(JSON, default=[])  # Automated actions and triggers
    
    # Assignment and ownership
    campaign_manager = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Custom fields and metadata
    custom_fields = Column(JSON, default={})
    tags = Column(JSON, default=[])
    
    # Relationships
    leads = relationship("LeadAdmin", back_populates="campaign")

# Sales Pipeline Stages
class PipelineStageAdmin(Base):
    __tablename__ = "crm_pipeline_stages"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Stage details
    name = Column(String(100), nullable=False)
    description = Column(Text)
    order = Column(Integer, nullable=False)  # Display order
    
    # Stage characteristics
    is_active = Column(Boolean, default=True)
    probability = Column(Float, default=0.0)  # Default probability for this stage
    expected_duration_days = Column(Integer)  # How long deals typically stay here
    
    # Automation
    entry_requirements = Column(JSON, default=[])  # Conditions to enter this stage
    exit_requirements = Column(JSON, default=[])  # Conditions to exit this stage
    auto_actions = Column(JSON, default=[])  # Actions to take when entering/exiting
    
    # Metrics
    conversion_rate = Column(Float)  # Historical conversion rate to next stage
    average_deal_value = Column(Float)  # Average deal value in this stage
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

# Customer Segments for targeted marketing
class CustomerSegmentAdmin(Base):
    __tablename__ = "crm_customer_segments"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Segment details
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Segmentation criteria
    criteria = Column(JSON, nullable=False)  # Rules for segment membership
    is_dynamic = Column(Boolean, default=True)  # Auto-update membership
    
    # Metrics
    member_count = Column(Integer, default=0)
    last_calculated_at = Column(DateTime(timezone=True))
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))