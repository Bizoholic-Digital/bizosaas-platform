"""
SEO Database Models
SQLAlchemy models for SEO workflow and data management

This module defines the database schema for SEO workflow management, audit results,
and performance tracking within the BizOSaaS multi-tenant architecture.

Key Features:
- Multi-tenant SEO data isolation
- Comprehensive SEO audit result storage
- Workflow state management and tracking
- Performance metrics and analytics
- HITL approval workflow tracking
- Integration with existing tenant system
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum as PyEnum
import uuid
import json

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Float, 
    ForeignKey, JSON, Enum, Index, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pydantic import BaseModel

# Base class for all models
Base = declarative_base()

# Enums
class SEOWorkflowStatus(PyEnum):
    """Status of SEO workflows"""
    PENDING = "pending"
    INITIALIZING = "initializing"
    EXECUTING = "executing"
    AWAITING_APPROVAL = "awaiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class SEOWorkflowType(PyEnum):
    """Types of SEO workflows"""
    TECHNICAL_AUDIT = "technical_audit"
    ON_PAGE_OPTIMIZATION = "on_page_optimization"
    OFF_PAGE_STRATEGY = "off_page_strategy"
    KEYWORD_RESEARCH = "keyword_research"
    CONTENT_OPTIMIZATION = "content_optimization"
    BACKLINK_ANALYSIS = "backlink_analysis"
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    LOCAL_SEO = "local_seo"
    COMPREHENSIVE_AUDIT = "comprehensive_audit"

class HITLApprovalStatus(PyEnum):
    """HITL approval status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"

class SEOTaskPriority(PyEnum):
    """SEO task priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Database Models
class SEOWorkflow(Base):
    """SEO workflow execution tracking"""
    __tablename__ = "seo_workflows"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(255), nullable=False, index=True)
    workflow_type = Column(Enum(SEOWorkflowType), nullable=False)
    status = Column(Enum(SEOWorkflowStatus), nullable=False, default=SEOWorkflowStatus.PENDING)
    
    # Workflow Configuration
    domain = Column(String(255), nullable=False)
    target_keywords = Column(JSONB, default=[])
    competitor_domains = Column(JSONB, default=[])
    workflow_config = Column(JSONB, default={})
    
    # Execution Tracking
    progress_percentage = Column(Integer, default=0)
    current_stage = Column(String(100))
    estimated_completion = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Execution Results
    execution_time = Column(Float)  # seconds
    error_message = Column(Text)
    raw_result = Column(JSONB)
    
    # Conservative estimation flags
    conservative_estimation = Column(Boolean, default=True)
    hitl_level = Column(String(50), default="medium")
    
    # Relationships
    audit_results = relationship("SEOAuditResult", back_populates="workflow", cascade="all, delete-orphan")
    insights = relationship("SEOInsight", back_populates="workflow", cascade="all, delete-orphan")
    approvals = relationship("HITLApproval", back_populates="workflow", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_seo_workflow_tenant_status', 'tenant_id', 'status'),
        Index('idx_seo_workflow_tenant_type', 'tenant_id', 'workflow_type'),
        Index('idx_seo_workflow_created', 'created_at'),
    )

class SEOAuditResult(Base):
    """SEO audit results and findings"""
    __tablename__ = "seo_audit_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('seo_workflows.id'), nullable=False)
    tenant_id = Column(String(255), nullable=False, index=True)
    
    # Audit Information
    domain = Column(String(255), nullable=False)
    audit_type = Column(Enum(SEOWorkflowType), nullable=False)
    overall_score = Column(Float, nullable=False)  # 0-100
    
    # Technical SEO Metrics
    technical_score = Column(Float)
    page_speed_score = Column(Float)
    mobile_score = Column(Float)
    security_score = Column(Float)
    
    # Content Metrics
    content_score = Column(Float)
    keyword_optimization_score = Column(Float)
    readability_score = Column(Float)
    
    # Authority Metrics
    domain_authority = Column(Float)
    backlink_count = Column(Integer)
    referring_domains = Column(Integer)
    
    # Detailed Results
    technical_issues = Column(JSONB, default=[])
    content_opportunities = Column(JSONB, default=[])
    backlink_analysis = Column(JSONB, default={})
    competitive_analysis = Column(JSONB, default={})
    
    # Performance Projections
    estimated_impact = Column(JSONB, default={})
    implementation_timeline = Column(String(100))
    estimated_roi = Column(JSONB, default={})
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workflow = relationship("SEOWorkflow", back_populates="audit_results")
    
    # Indexes
    __table_args__ = (
        Index('idx_seo_audit_tenant_domain', 'tenant_id', 'domain'),
        Index('idx_seo_audit_workflow', 'workflow_id'),
        Index('idx_seo_audit_score', 'overall_score'),
    )

class SEOInsight(Base):
    """Individual SEO insights and recommendations"""
    __tablename__ = "seo_insights"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('seo_workflows.id'), nullable=False)
    tenant_id = Column(String(255), nullable=False, index=True)
    
    # Insight Details
    category = Column(String(100), nullable=False)  # technical, content, links, etc.
    priority = Column(Enum(SEOTaskPriority), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    
    # Impact Assessment
    impact_score = Column(Float, nullable=False)  # 0-100
    effort_estimate = Column(Integer)  # hours
    confidence_level = Column(Float, nullable=False)  # 0-1
    
    # Implementation Details
    implementation_steps = Column(JSONB, default=[])
    expected_timeline = Column(String(100))
    required_resources = Column(JSONB, default=[])
    
    # Status Tracking
    status = Column(String(50), default="identified")  # identified, approved, in_progress, completed
    requires_approval = Column(Boolean, default=False)
    approved_at = Column(DateTime)
    implemented_at = Column(DateTime)
    
    # Results Tracking
    actual_impact = Column(Float)  # measured after implementation
    implementation_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workflow = relationship("SEOWorkflow", back_populates="insights")
    
    # Indexes
    __table_args__ = (
        Index('idx_seo_insight_tenant_category', 'tenant_id', 'category'),
        Index('idx_seo_insight_priority', 'priority'),
        Index('idx_seo_insight_impact', 'impact_score'),
        Index('idx_seo_insight_status', 'status'),
    )

class HITLApproval(Base):
    """Human-in-the-loop approval requests and responses"""
    __tablename__ = "hitl_approvals"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('seo_workflows.id'), nullable=False)
    tenant_id = Column(String(255), nullable=False, index=True)
    
    # Approval Details
    approval_type = Column(String(100), nullable=False)  # technical_change, content_modification, etc.
    description = Column(Text, nullable=False)
    requested_changes = Column(JSONB, default={})
    
    # Status and Decision
    status = Column(Enum(HITLApprovalStatus), nullable=False, default=HITLApprovalStatus.PENDING)
    approved_by = Column(String(255))  # user_id of approver
    decision_comments = Column(Text)
    modifications = Column(JSONB, default={})
    
    # Priority and Context
    priority_level = Column(Enum(SEOTaskPriority), nullable=False)
    business_impact = Column(String(50))  # low, medium, high
    risk_level = Column(String(50))  # low, medium, high
    
    # Timeline
    requested_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    deadline = Column(DateTime)
    responded_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workflow = relationship("SEOWorkflow", back_populates="approvals")
    
    # Indexes
    __table_args__ = (
        Index('idx_hitl_approval_tenant_status', 'tenant_id', 'status'),
        Index('idx_hitl_approval_workflow', 'workflow_id'),
        Index('idx_hitl_approval_priority', 'priority_level'),
        Index('idx_hitl_approval_deadline', 'deadline'),
    )

class SEOKeywordTracking(Base):
    """SEO keyword ranking and performance tracking"""
    __tablename__ = "seo_keyword_tracking"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(255), nullable=False, index=True)
    domain = Column(String(255), nullable=False)
    
    # Keyword Details
    keyword = Column(String(255), nullable=False)
    keyword_type = Column(String(50))  # primary, secondary, long_tail
    search_volume = Column(Integer)
    competition_score = Column(Float)
    
    # Ranking Data
    current_position = Column(Integer)
    previous_position = Column(Integer)
    best_position = Column(Integer)
    position_change = Column(Integer)  # calculated field
    
    # Traffic Data
    organic_clicks = Column(Integer)
    impressions = Column(Integer)
    ctr = Column(Float)  # click-through rate
    
    # Tracking Metadata
    search_engine = Column(String(50), default="google")
    location = Column(String(100))  # for local SEO
    device_type = Column(String(20), default="desktop")  # desktop, mobile
    
    # Timestamps
    tracking_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_keyword_tracking_tenant_domain', 'tenant_id', 'domain'),
        Index('idx_keyword_tracking_keyword', 'keyword'),
        Index('idx_keyword_tracking_date', 'tracking_date'),
        Index('idx_keyword_tracking_position', 'current_position'),
        UniqueConstraint('tenant_id', 'domain', 'keyword', 'tracking_date', 'search_engine', 'device_type', 
                        name='uq_keyword_tracking_daily'),
    )

class SEOPerformanceMetrics(Base):
    """Aggregated SEO performance metrics"""
    __tablename__ = "seo_performance_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(255), nullable=False, index=True)
    domain = Column(String(255), nullable=False)
    
    # Traffic Metrics
    organic_traffic = Column(Integer, default=0)
    organic_sessions = Column(Integer, default=0)
    bounce_rate = Column(Float)
    avg_session_duration = Column(Float)  # seconds
    pages_per_session = Column(Float)
    
    # Ranking Metrics
    keywords_in_top_3 = Column(Integer, default=0)
    keywords_in_top_10 = Column(Integer, default=0)
    keywords_in_top_50 = Column(Integer, default=0)
    total_tracked_keywords = Column(Integer, default=0)
    avg_keyword_position = Column(Float)
    
    # Technical Metrics
    page_speed_score = Column(Float)
    mobile_usability_score = Column(Float)
    core_web_vitals_score = Column(Float)
    
    # Authority Metrics
    domain_authority = Column(Float)
    page_authority = Column(Float)
    backlink_count = Column(Integer, default=0)
    referring_domains = Column(Integer, default=0)
    
    # Content Metrics
    indexed_pages = Column(Integer, default=0)
    crawl_errors = Column(Integer, default=0)
    
    # Conversion Metrics
    goal_completions = Column(Integer, default=0)
    ecommerce_revenue = Column(Float)  # if applicable
    conversion_rate = Column(Float)
    
    # Time Period
    metric_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    period_type = Column(String(20), default="daily")  # daily, weekly, monthly
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_seo_metrics_tenant_domain', 'tenant_id', 'domain'),
        Index('idx_seo_metrics_date', 'metric_date'),
        Index('idx_seo_metrics_period', 'period_type'),
        UniqueConstraint('tenant_id', 'domain', 'metric_date', 'period_type', 
                        name='uq_seo_metrics_daily'),
    )

class SEOIntegrationConfig(Base):
    """SEO tool integration configurations"""
    __tablename__ = "seo_integration_configs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(255), nullable=False, index=True)
    
    # Integration Details
    integration_name = Column(String(100), nullable=False)  # google_search_console, ahrefs, etc.
    integration_type = Column(String(50), nullable=False)  # api, webhook, manual
    
    # Configuration
    api_credentials = Column(JSONB, default={})  # encrypted
    webhook_url = Column(String(500))
    sync_settings = Column(JSONB, default={})
    
    # Status
    is_active = Column(Boolean, default=True)
    last_sync = Column(DateTime)
    sync_frequency = Column(String(50), default="daily")  # hourly, daily, weekly
    
    # Error Tracking
    last_error = Column(Text)
    error_count = Column(Integer, default=0)
    consecutive_errors = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('idx_seo_integration_tenant', 'tenant_id'),
        Index('idx_seo_integration_name', 'integration_name'),
        Index('idx_seo_integration_active', 'is_active'),
        UniqueConstraint('tenant_id', 'integration_name', name='uq_seo_integration_tenant'),
    )

# Pydantic Models for API
class SEOWorkflowCreate(BaseModel):
    """Pydantic model for creating SEO workflows"""
    workflow_type: str
    domain: str
    target_keywords: List[str] = []
    competitor_domains: List[str] = []
    workflow_config: Dict[str, Any] = {}
    conservative_estimation: bool = True
    hitl_level: str = "medium"

class SEOWorkflowResponse(BaseModel):
    """Pydantic model for SEO workflow responses"""
    id: str
    tenant_id: str
    workflow_type: str
    status: str
    domain: str
    target_keywords: List[str]
    competitor_domains: List[str]
    progress_percentage: int
    current_stage: Optional[str]
    estimated_completion: Optional[datetime]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    execution_time: Optional[float]
    error_message: Optional[str]
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class SEOInsightResponse(BaseModel):
    """Pydantic model for SEO insight responses"""
    id: str
    category: str
    priority: str
    title: str
    description: str
    impact_score: float
    effort_estimate: Optional[int]
    confidence_level: float
    implementation_steps: List[str]
    expected_timeline: Optional[str]
    status: str
    requires_approval: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SEOPerformanceResponse(BaseModel):
    """Pydantic model for SEO performance metrics"""
    domain: str
    organic_traffic: int
    keywords_in_top_10: int
    domain_authority: Optional[float]
    backlink_count: int
    metric_date: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Database utility functions
class SEODatabase:
    """Database utility class for SEO operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    async def create_workflow(self, tenant_id: str, workflow_data: SEOWorkflowCreate) -> SEOWorkflow:
        """Create a new SEO workflow"""
        workflow = SEOWorkflow(
            tenant_id=tenant_id,
            workflow_type=SEOWorkflowType(workflow_data.workflow_type),
            domain=workflow_data.domain,
            target_keywords=workflow_data.target_keywords,
            competitor_domains=workflow_data.competitor_domains,
            workflow_config=workflow_data.workflow_config,
            conservative_estimation=workflow_data.conservative_estimation,
            hitl_level=workflow_data.hitl_level
        )
        
        self.session.add(workflow)
        self.session.commit()
        self.session.refresh(workflow)
        
        return workflow
    
    async def get_workflow(self, workflow_id: str, tenant_id: str) -> Optional[SEOWorkflow]:
        """Get workflow by ID and tenant"""
        return self.session.query(SEOWorkflow).filter(
            SEOWorkflow.id == workflow_id,
            SEOWorkflow.tenant_id == tenant_id
        ).first()
    
    async def update_workflow_status(
        self, 
        workflow_id: str, 
        status: SEOWorkflowStatus,
        progress: Optional[int] = None,
        current_stage: Optional[str] = None
    ) -> bool:
        """Update workflow status and progress"""
        workflow = self.session.query(SEOWorkflow).filter(
            SEOWorkflow.id == workflow_id
        ).first()
        
        if not workflow:
            return False
        
        workflow.status = status
        if progress is not None:
            workflow.progress_percentage = progress
        if current_stage is not None:
            workflow.current_stage = current_stage
        
        if status == SEOWorkflowStatus.EXECUTING and not workflow.started_at:
            workflow.started_at = datetime.utcnow()
        elif status == SEOWorkflowStatus.COMPLETED:
            workflow.completed_at = datetime.utcnow()
            if workflow.started_at:
                workflow.execution_time = (workflow.completed_at - workflow.started_at).total_seconds()
        
        self.session.commit()
        return True
    
    async def save_audit_result(self, workflow_id: str, tenant_id: str, audit_data: Dict[str, Any]) -> SEOAuditResult:
        """Save SEO audit results"""
        audit_result = SEOAuditResult(
            workflow_id=workflow_id,
            tenant_id=tenant_id,
            domain=audit_data.get("domain"),
            audit_type=SEOWorkflowType(audit_data.get("audit_type")),
            overall_score=audit_data.get("overall_score", 0),
            technical_score=audit_data.get("technical_score"),
            page_speed_score=audit_data.get("page_speed_score"),
            mobile_score=audit_data.get("mobile_score"),
            security_score=audit_data.get("security_score"),
            content_score=audit_data.get("content_score"),
            domain_authority=audit_data.get("domain_authority"),
            backlink_count=audit_data.get("backlink_count"),
            referring_domains=audit_data.get("referring_domains"),
            technical_issues=audit_data.get("technical_issues", []),
            content_opportunities=audit_data.get("content_opportunities", []),
            backlink_analysis=audit_data.get("backlink_analysis", {}),
            competitive_analysis=audit_data.get("competitive_analysis", {}),
            estimated_impact=audit_data.get("estimated_impact", {}),
            implementation_timeline=audit_data.get("implementation_timeline"),
            estimated_roi=audit_data.get("estimated_roi", {})
        )
        
        self.session.add(audit_result)
        self.session.commit()
        self.session.refresh(audit_result)
        
        return audit_result
    
    async def save_insights(self, workflow_id: str, tenant_id: str, insights_data: List[Dict[str, Any]]) -> List[SEOInsight]:
        """Save SEO insights"""
        insights = []
        
        for insight_data in insights_data:
            insight = SEOInsight(
                workflow_id=workflow_id,
                tenant_id=tenant_id,
                category=insight_data.get("category"),
                priority=SEOTaskPriority(insight_data.get("priority")),
                title=insight_data.get("title"),
                description=insight_data.get("description"),
                impact_score=insight_data.get("impact_score", 0),
                effort_estimate=insight_data.get("effort_estimate"),
                confidence_level=insight_data.get("confidence_level", 0),
                implementation_steps=insight_data.get("implementation_steps", []),
                expected_timeline=insight_data.get("expected_timeline"),
                requires_approval=insight_data.get("requires_approval", False)
            )
            
            insights.append(insight)
            self.session.add(insight)
        
        self.session.commit()
        
        for insight in insights:
            self.session.refresh(insight)
        
        return insights
    
    async def get_tenant_workflows(
        self, 
        tenant_id: str, 
        status: Optional[SEOWorkflowStatus] = None,
        limit: int = 50
    ) -> List[SEOWorkflow]:
        """Get workflows for a tenant"""
        query = self.session.query(SEOWorkflow).filter(
            SEOWorkflow.tenant_id == tenant_id
        )
        
        if status:
            query = query.filter(SEOWorkflow.status == status)
        
        return query.order_by(SEOWorkflow.created_at.desc()).limit(limit).all()
    
    async def get_performance_metrics(
        self, 
        tenant_id: str, 
        domain: str,
        days: int = 30
    ) -> List[SEOPerformanceMetrics]:
        """Get performance metrics for domain"""
        since_date = datetime.utcnow() - timedelta(days=days)
        
        return self.session.query(SEOPerformanceMetrics).filter(
            SEOPerformanceMetrics.tenant_id == tenant_id,
            SEOPerformanceMetrics.domain == domain,
            SEOPerformanceMetrics.metric_date >= since_date
        ).order_by(SEOPerformanceMetrics.metric_date.desc()).all()