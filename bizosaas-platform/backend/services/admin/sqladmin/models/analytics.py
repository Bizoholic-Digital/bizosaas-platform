"""
Analytics Data Models for SQLAdmin Dashboard
Handles metrics, reports, events, and performance tracking
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, JSON, ForeignKey, UUID, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class MetricType(enum.Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"

class ReportStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class EventType(enum.Enum):
    PAGE_VIEW = "page_view"
    USER_ACTION = "user_action"
    CONVERSION = "conversion"
    ERROR = "error"
    SYSTEM = "system"

# Analytics Events
class EventAdmin(Base):
    __tablename__ = "analytics_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Event details
    event_type = Column(Enum(EventType), nullable=False)
    event_name = Column(String(255), nullable=False, index=True)
    event_category = Column(String(100))
    event_action = Column(String(100))
    event_label = Column(String(255))
    event_value = Column(Float)
    
    # Event data
    properties = Column(JSON, default={})
    custom_data = Column(JSON, default={})
    
    # Context
    session_id = Column(String(255), index=True)
    page_url = Column(String(500))
    referrer = Column(String(500))
    user_agent = Column(Text)
    ip_address = Column(String(45))
    
    # Geographic data
    country = Column(String(100))
    region = Column(String(100))
    city = Column(String(100))
    
    # Device and browser
    device_type = Column(String(50))
    browser = Column(String(100))
    os = Column(String(100))
    screen_resolution = Column(String(20))
    
    # UTM parameters
    utm_source = Column(String(100))
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))
    utm_term = Column(String(100))
    utm_content = Column(String(100))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    event_timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)

# Metrics and KPIs
class MetricAdmin(Base):
    __tablename__ = "analytics_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Metric details
    name = Column(String(255), nullable=False, index=True)
    display_name = Column(String(255))
    description = Column(Text)
    metric_type = Column(Enum(MetricType), default=MetricType.GAUGE)
    
    # Current value
    current_value = Column(Float, default=0.0)
    previous_value = Column(Float, default=0.0)
    
    # Configuration
    unit = Column(String(50))  # %, count, seconds, bytes, etc.
    decimal_places = Column(Integer, default=2)
    
    # Aggregation settings
    aggregation_method = Column(String(50), default="sum")  # sum, avg, count, min, max
    time_window = Column(String(50), default="1h")  # 1h, 1d, 1w, 1m
    
    # Thresholds and alerts
    warning_threshold = Column(Float)
    critical_threshold = Column(Float)
    target_value = Column(Float)
    
    # Display settings
    chart_type = Column(String(50), default="line")
    color = Column(String(7))  # Hex color
    sort_order = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    last_calculated_at = Column(DateTime(timezone=True))

# Metric Values History
class MetricValueAdmin(Base):
    __tablename__ = "analytics_metric_values"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    metric_id = Column(UUID(as_uuid=True), ForeignKey("analytics_metrics.id"), nullable=False)
    
    # Value data
    value = Column(Float, nullable=False)
    
    # Time dimensions
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    hour = Column(Integer)
    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)
    
    # Additional dimensions
    dimensions = Column(JSON, default={})  # Custom grouping dimensions
    
    # Aggregation level
    aggregation_level = Column(String(20), default="raw")  # raw, hourly, daily, monthly

# Analytics Reports
class AnalyticsReportAdmin(Base):
    __tablename__ = "analytics_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Report details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    report_type = Column(String(100), nullable=False)  # dashboard, summary, detailed, etc.
    
    # Report configuration
    metrics = Column(JSON, default=[])  # List of metric IDs to include
    filters = Column(JSON, default={})  # Report filters
    date_range = Column(JSON, default={})  # start_date, end_date, period
    
    # Data and results
    data = Column(JSON)  # Report data
    summary = Column(JSON)  # Summary statistics
    insights = Column(JSON, default=[])  # AI-generated insights
    
    # Scheduling
    is_scheduled = Column(Boolean, default=False)
    schedule_cron = Column(String(100))  # Cron expression
    last_run_at = Column(DateTime(timezone=True))
    next_run_at = Column(DateTime(timezone=True))
    
    # Generation details
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING)
    generation_time_ms = Column(Integer)
    error_message = Column(Text)
    
    # Sharing and access
    is_public = Column(Boolean, default=False)
    share_token = Column(String(255), unique=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    generated_at = Column(DateTime(timezone=True))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

# Custom Dashboards
class DashboardAdmin(Base):
    __tablename__ = "analytics_dashboards"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Dashboard details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    slug = Column(String(255), nullable=False, index=True)
    
    # Layout and configuration
    layout = Column(JSON, default={})  # Grid layout configuration
    widgets = Column(JSON, default=[])  # Widget configurations
    filters = Column(JSON, default={})  # Dashboard-level filters
    
    # Customization
    theme = Column(String(50), default="default")
    refresh_interval = Column(Integer, default=300)  # Seconds
    
    # Access control
    is_default = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    allowed_users = Column(JSON, default=[])
    allowed_roles = Column(JSON, default=[])
    
    # Performance
    cache_duration = Column(Integer, default=300)  # Seconds
    last_cached_at = Column(DateTime(timezone=True))
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

# A/B Test Experiments
class ExperimentAdmin(Base):
    __tablename__ = "analytics_experiments"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Experiment details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    hypothesis = Column(Text)
    
    # Experiment configuration
    variants = Column(JSON, nullable=False)  # List of experiment variants
    traffic_allocation = Column(JSON, default={})  # Percentage per variant
    success_metrics = Column(JSON, default=[])  # Metrics to track
    
    # Targeting
    audience_filters = Column(JSON, default={})
    geographic_targeting = Column(JSON, default={})
    device_targeting = Column(JSON, default={})
    
    # Timeline
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    duration_days = Column(Integer)
    
    # Results
    participants = Column(Integer, default=0)
    conversion_rate = Column(Float)
    statistical_significance = Column(Float)
    winner_variant = Column(String(100))
    
    # Status
    status = Column(String(50), default="draft")  # draft, running, paused, completed
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

# User Segments for Analytics
class SegmentAdmin(Base):
    __tablename__ = "analytics_segments"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Segment details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Segmentation criteria
    criteria = Column(JSON, nullable=False)
    is_dynamic = Column(Boolean, default=True)
    
    # Segment size
    user_count = Column(Integer, default=0)
    last_calculated_at = Column(DateTime(timezone=True))
    
    # Performance metrics
    conversion_rate = Column(Float)
    average_session_duration = Column(Float)
    average_page_views = Column(Float)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

# Goal Tracking
class GoalAdmin(Base):
    __tablename__ = "analytics_goals"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Goal details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    goal_type = Column(String(50), nullable=False)  # event, page_view, revenue, etc.
    
    # Goal configuration
    target_metric = Column(String(255), nullable=False)
    target_value = Column(Float, nullable=False)
    completion_criteria = Column(JSON, default={})
    
    # Tracking
    current_value = Column(Float, default=0.0)
    completion_percentage = Column(Float, default=0.0)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True))
    
    # Timeline
    start_date = Column(DateTime(timezone=True))
    target_date = Column(DateTime(timezone=True))
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))