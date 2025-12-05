"""
Content Marketing Database Models
SQLAlchemy models for comprehensive content marketing automation workflows

This module defines the data models for:
- Content strategies and brand guidelines
- Content calendar and scheduling
- Content pieces with versions and performance
- Community engagement tracking
- Performance analytics and optimization
- HITL approval workflows
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Any, List, Optional
import uuid
import json

Base = declarative_base()

class ContentType(Enum):
    """Types of content pieces"""
    BLOG_POST = "blog_post"
    SOCIAL_MEDIA_POST = "social_media_post"
    EMAIL_NEWSLETTER = "email_newsletter"
    VIDEO_SCRIPT = "video_script"
    INFOGRAPHIC = "infographic"
    PODCAST_SCRIPT = "podcast_script"
    WEBINAR_CONTENT = "webinar_content"
    EBOOK = "ebook"
    WHITEPAPER = "whitepaper"
    CASE_STUDY = "case_study"
    USER_GENERATED_CONTENT = "user_generated_content"

class ContentStatus(Enum):
    """Content lifecycle status"""
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    REJECTED = "rejected"

class ContentPlatform(Enum):
    """Content distribution platforms"""
    WEBSITE_BLOG = "website_blog"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    PINTEREST = "pinterest"
    EMAIL = "email"
    NEWSLETTER = "newsletter"

class HITLApprovalType(Enum):
    """Types of HITL approval required"""
    CONTENT_STRATEGY = "content_strategy"
    BRAND_VOICE = "brand_voice"
    HIGH_IMPACT_CONTENT = "high_impact_content"
    CRISIS_MANAGEMENT = "crisis_management"
    LEGAL_COMPLIANCE = "legal_compliance"
    EXECUTIVE_CONTENT = "executive_content"

class AutomationLevel(Enum):
    """Progressive automation levels"""
    LEVEL_1_MANUAL = "level_1_manual"
    LEVEL_2_ASSISTED = "level_2_assisted"
    LEVEL_3_SEMI_AUTO = "level_3_semi_auto"
    LEVEL_4_AUTO_REVIEW = "level_4_auto_review"
    LEVEL_5_AUTONOMOUS = "level_5_autonomous"

class ContentStrategy(Base):
    """Content strategy and brand guidelines"""
    __tablename__ = 'content_strategies'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(255), nullable=False, index=True)
    strategy_name = Column(String(255), nullable=False)
    
    # Brand Voice and Tone
    brand_voice = Column(JSON, nullable=False)  # Voice characteristics, tone guidelines
    target_audience = Column(JSON, nullable=False)  # Personas, demographics, psychographics
    content_pillars = Column(JSON, nullable=False)  # Main themes and topics
    competitive_landscape = Column(JSON, nullable=True)  # Competitor analysis
    
    # Content Goals and KPIs
    content_goals = Column(JSON, nullable=False)  # SMART goals
    kpi_definitions = Column(JSON, nullable=False)  # Metrics and targets
    success_metrics = Column(JSON, nullable=False)  # Performance benchmarks
    
    # Editorial Guidelines
    editorial_calendar_framework = Column(JSON, nullable=False)  # Calendar structure
    content_format_strategy = Column(JSON, nullable=False)  # Preferred formats
    seo_integration_config = Column(JSON, nullable=False)  # SEO integration settings
    
    # Automation and Approval
    automation_level = Column(SQLEnum(AutomationLevel), default=AutomationLevel.LEVEL_2_ASSISTED)
    hitl_approval_rules = Column(JSON, nullable=False)  # Approval workflow rules
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    content_calendars = relationship("ContentCalendar", back_populates="strategy")
    content_pieces = relationship("ContentPiece", back_populates="strategy")

class ContentCalendar(Base):
    """Content calendar and scheduling management"""
    __tablename__ = 'content_calendars'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(255), nullable=False, index=True)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    
    calendar_name = Column(String(255), nullable=False)
    calendar_period = Column(String(50), nullable=False)  # monthly, quarterly, yearly
    
    # Calendar Configuration
    content_themes = Column(JSON, nullable=False)  # Monthly/weekly themes
    publishing_schedule = Column(JSON, nullable=False)  # Platform-specific schedules
    campaign_coordination = Column(JSON, nullable=True)  # Campaign alignments
    seasonal_events = Column(JSON, nullable=True)  # Holiday and seasonal content
    
    # Resource Management
    resource_allocation = Column(JSON, nullable=False)  # Team assignments
    deadline_management = Column(JSON, nullable=False)  # Timeline and deadlines
    collaboration_workflows = Column(JSON, nullable=False)  # Cross-team workflows
    
    # Performance Optimization
    performance_data = Column(JSON, nullable=True)  # Historical performance
    optimization_insights = Column(JSON, nullable=True)  # AI recommendations
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    strategy = relationship("ContentStrategy", back_populates="content_calendars")
    content_pieces = relationship("ContentPiece", back_populates="calendar")

class ContentPiece(Base):
    """Individual content pieces with versions and performance"""
    __tablename__ = 'content_pieces'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(255), nullable=False, index=True)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey('content_strategies.id'), nullable=False)
    calendar_id = Column(UUID(as_uuid=True), ForeignKey('content_calendars.id'), nullable=True)
    
    # Content Identification
    title = Column(String(500), nullable=False)
    content_type = Column(SQLEnum(ContentType), nullable=False)
    platforms = Column(ARRAY(String), nullable=False)  # Target platforms
    status = Column(SQLEnum(ContentStatus), default=ContentStatus.DRAFT)
    
    # Content Data
    content_data = Column(JSON, nullable=False)  # Main content and metadata
    seo_optimization = Column(JSON, nullable=True)  # SEO-specific data
    visual_assets = Column(JSON, nullable=True)  # Images, videos, graphics
    
    # AI Generation
    ai_generated = Column(Boolean, default=False)
    generation_prompt = Column(Text, nullable=True)
    ai_model_used = Column(String(100), nullable=True)
    human_edited = Column(Boolean, default=False)
    
    # Scheduling and Distribution
    scheduled_publish_time = Column(DateTime, nullable=True)
    actual_publish_time = Column(DateTime, nullable=True)
    distribution_config = Column(JSON, nullable=False)  # Platform-specific settings
    
    # Performance Tracking
    performance_metrics = Column(JSON, nullable=True)  # Engagement, reach, conversions
    optimization_history = Column(JSON, nullable=True)  # A/B tests and optimizations
    roi_attribution = Column(JSON, nullable=True)  # Revenue attribution
    
    # Approval and Compliance
    approval_history = Column(JSON, nullable=True)  # HITL approval tracking
    compliance_checks = Column(JSON, nullable=True)  # Legal and brand compliance
    version_history = Column(JSON, nullable=True)  # Content version tracking
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(255), nullable=False)
    
    # Relationships
    strategy = relationship("ContentStrategy", back_populates="content_pieces")
    calendar = relationship("ContentCalendar", back_populates="content_pieces")
    engagement_data = relationship("CommunityEngagement", back_populates="content_piece")

class CommunityEngagement(Base):
    """Community management and engagement tracking"""
    __tablename__ = 'community_engagement'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(255), nullable=False, index=True)
    content_piece_id = Column(UUID(as_uuid=True), ForeignKey('content_pieces.id'), nullable=True)
    
    # Engagement Details
    platform = Column(SQLEnum(ContentPlatform), nullable=False)
    engagement_type = Column(String(100), nullable=False)  # comment, mention, share, etc.
    original_message = Column(Text, nullable=False)
    
    # User Information
    user_handle = Column(String(255), nullable=True)
    user_data = Column(JSON, nullable=True)  # Available user information
    sentiment_score = Column(Float, nullable=True)  # AI sentiment analysis
    
    # Response Management
    requires_response = Column(Boolean, default=False)
    response_priority = Column(Integer, default=3)  # 1=high, 5=low
    ai_suggested_response = Column(Text, nullable=True)
    actual_response = Column(Text, nullable=True)
    response_time = Column(DateTime, nullable=True)
    responded_by = Column(String(255), nullable=True)
    
    # Crisis Management
    is_crisis_related = Column(Boolean, default=False)
    escalation_level = Column(Integer, default=0)
    crisis_tags = Column(ARRAY(String), nullable=True)
    
    # Performance Impact
    engagement_metrics = Column(JSON, nullable=True)  # Likes, shares, etc.
    influence_score = Column(Float, nullable=True)  # User influence rating
    conversion_potential = Column(Float, nullable=True)  # Lead conversion likelihood
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    content_piece = relationship("ContentPiece", back_populates="engagement_data")

class ContentPerformanceAnalytics(Base):
    """Performance analytics and optimization insights"""
    __tablename__ = 'content_performance_analytics'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(255), nullable=False, index=True)
    content_piece_id = Column(UUID(as_uuid=True), ForeignKey('content_pieces.id'), nullable=True)
    
    # Analytics Period
    analysis_date = Column(DateTime, nullable=False)
    analysis_period = Column(String(50), nullable=False)  # daily, weekly, monthly
    platform = Column(SQLEnum(ContentPlatform), nullable=False)
    
    # Performance Metrics
    reach_metrics = Column(JSON, nullable=False)  # Impressions, reach, etc.
    engagement_metrics = Column(JSON, nullable=False)  # Likes, comments, shares
    conversion_metrics = Column(JSON, nullable=True)  # Clicks, leads, sales
    roi_metrics = Column(JSON, nullable=True)  # Revenue attribution
    
    # AI Analysis
    performance_insights = Column(JSON, nullable=True)  # AI-generated insights
    optimization_recommendations = Column(JSON, nullable=True)  # Improvement suggestions
    predictive_modeling = Column(JSON, nullable=True)  # Future performance predictions
    competitive_benchmarking = Column(JSON, nullable=True)  # vs competitor performance
    
    # Conservative Estimation
    estimated_performance = Column(JSON, nullable=True)  # Conservative projections
    actual_vs_estimated = Column(JSON, nullable=True)  # Over-delivery tracking
    confidence_intervals = Column(JSON, nullable=True)  # Statistical confidence
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HITLApprovalWorkflow(Base):
    """Human-in-the-loop approval workflow tracking"""
    __tablename__ = 'hitl_approval_workflows'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(255), nullable=False, index=True)
    content_piece_id = Column(UUID(as_uuid=True), ForeignKey('content_pieces.id'), nullable=True)
    
    # Approval Request
    approval_type = Column(SQLEnum(HITLApprovalType), nullable=False)
    request_data = Column(JSON, nullable=False)  # Content or strategy data
    ai_confidence_score = Column(Float, nullable=True)  # AI confidence in recommendation
    risk_assessment = Column(JSON, nullable=True)  # Risk analysis
    
    # Approval Status
    status = Column(String(50), default="pending")  # pending, approved, rejected, modified
    assigned_to = Column(String(255), nullable=True)  # Reviewer assignment
    priority_level = Column(Integer, default=3)  # 1=critical, 5=low
    
    # Approval Decision
    approved_by = Column(String(255), nullable=True)
    approval_timestamp = Column(DateTime, nullable=True)
    approval_comments = Column(Text, nullable=True)
    modifications_requested = Column(JSON, nullable=True)
    
    # Workflow Processing
    automation_level_used = Column(SQLEnum(AutomationLevel), nullable=False)
    escalation_history = Column(JSON, nullable=True)  # If escalated
    approval_timeline = Column(JSON, nullable=True)  # Workflow timeline
    
    # Learning and Optimization
    approval_outcome = Column(String(50), nullable=True)  # final outcome
    feedback_for_ai = Column(JSON, nullable=True)  # Learning data for AI
    similar_requests = Column(JSON, nullable=True)  # Related approval requests
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deadline = Column(DateTime, nullable=True)

class ContentWorkflowExecution(Base):
    """Content marketing workflow execution tracking"""
    __tablename__ = 'content_workflow_executions'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(255), nullable=False, index=True)
    
    # Workflow Identification
    workflow_type = Column(String(100), nullable=False)  # strategy_dev, content_creation, etc.
    execution_id = Column(String(255), nullable=False, unique=True)
    parent_execution_id = Column(String(255), nullable=True)  # For nested workflows
    
    # Execution Status
    status = Column(String(50), default="initiated")  # initiated, executing, completed, failed
    progress_percentage = Column(Integer, default=0)
    current_stage = Column(String(100), nullable=True)
    
    # Input and Configuration
    input_parameters = Column(JSON, nullable=False)
    workflow_config = Column(JSON, nullable=False)
    automation_level = Column(SQLEnum(AutomationLevel), nullable=False)
    
    # Execution Results
    execution_results = Column(JSON, nullable=True)
    performance_metrics = Column(JSON, nullable=True)
    error_details = Column(JSON, nullable=True)
    
    # Timeline and Performance
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    execution_duration = Column(Float, nullable=True)  # seconds
    estimated_completion = Column(DateTime, nullable=True)
    
    # Conservative Estimation
    estimated_impact = Column(JSON, nullable=True)  # Conservative projections
    actual_impact = Column(JSON, nullable=True)  # Actual results
    over_delivery_tracking = Column(JSON, nullable=True)  # Performance vs estimates
    
    # AI Agent Information
    agents_involved = Column(JSON, nullable=False)  # List of AI agents used
    agent_performance = Column(JSON, nullable=True)  # Agent-specific metrics
    human_interventions = Column(JSON, nullable=True)  # HITL interventions
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Index definitions for performance optimization
from sqlalchemy import Index

# Content Strategy indexes
Index('idx_content_strategies_tenant', ContentStrategy.tenant_id)
Index('idx_content_strategies_active', ContentStrategy.tenant_id, ContentStrategy.is_active)

# Content Calendar indexes
Index('idx_content_calendars_tenant', ContentCalendar.tenant_id)
Index('idx_content_calendars_period', ContentCalendar.tenant_id, ContentCalendar.start_date, ContentCalendar.end_date)

# Content Piece indexes
Index('idx_content_pieces_tenant', ContentPiece.tenant_id)
Index('idx_content_pieces_status', ContentPiece.tenant_id, ContentPiece.status)
Index('idx_content_pieces_type', ContentPiece.tenant_id, ContentPiece.content_type)
Index('idx_content_pieces_schedule', ContentPiece.tenant_id, ContentPiece.scheduled_publish_time)

# Community Engagement indexes
Index('idx_community_engagement_tenant', CommunityEngagement.tenant_id)
Index('idx_community_engagement_platform', CommunityEngagement.tenant_id, CommunityEngagement.platform)
Index('idx_community_engagement_priority', CommunityEngagement.tenant_id, CommunityEngagement.requires_response, CommunityEngagement.response_priority)

# Performance Analytics indexes
Index('idx_performance_analytics_tenant', ContentPerformanceAnalytics.tenant_id)
Index('idx_performance_analytics_date', ContentPerformanceAnalytics.tenant_id, ContentPerformanceAnalytics.analysis_date)
Index('idx_performance_analytics_platform', ContentPerformanceAnalytics.tenant_id, ContentPerformanceAnalytics.platform)

# HITL Approval indexes
Index('idx_hitl_approval_tenant', HITLApprovalWorkflow.tenant_id)
Index('idx_hitl_approval_status', HITLApprovalWorkflow.tenant_id, HITLApprovalWorkflow.status)
Index('idx_hitl_approval_priority', HITLApprovalWorkflow.tenant_id, HITLApprovalWorkflow.priority_level)

# Workflow Execution indexes
Index('idx_workflow_execution_tenant', ContentWorkflowExecution.tenant_id)
Index('idx_workflow_execution_status', ContentWorkflowExecution.tenant_id, ContentWorkflowExecution.status)
Index('idx_workflow_execution_type', ContentWorkflowExecution.tenant_id, ContentWorkflowExecution.workflow_type)