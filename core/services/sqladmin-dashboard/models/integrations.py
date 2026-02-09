"""
Integration Data Models for SQLAdmin Dashboard
Handles external services, webhooks, APIs, and automation
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, JSON, ForeignKey, UUID, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class IntegrationStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    PENDING = "pending"
    SUSPENDED = "suspended"

class WebhookStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAILED = "failed"
    PAUSED = "paused"

class ServiceType(enum.Enum):
    CRM = "crm"
    EMAIL = "email"
    PAYMENT = "payment"
    ANALYTICS = "analytics"
    MARKETING = "marketing"
    STORAGE = "storage"
    COMMUNICATION = "communication"
    AI = "ai"
    OTHER = "other"

# External Service Integrations
class IntegrationAdmin(Base):
    __tablename__ = "integrations"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Integration details
    name = Column(String(255), nullable=False)
    service_name = Column(String(100), nullable=False, index=True)  # stripe, mailchimp, salesforce, etc.
    service_type = Column(Enum(ServiceType), nullable=False)
    description = Column(Text)
    
    # Connection details
    api_endpoint = Column(String(500))
    api_version = Column(String(50))
    
    # Authentication
    auth_type = Column(String(50), nullable=False)  # oauth2, api_key, basic, bearer
    credentials = Column(JSON)  # Encrypted credentials
    access_token = Column(Text)  # Encrypted
    refresh_token = Column(Text)  # Encrypted
    token_expires_at = Column(DateTime(timezone=True))
    
    # Configuration
    settings = Column(JSON, default={})
    sync_settings = Column(JSON, default={})
    mapping_rules = Column(JSON, default={})  # Field mappings
    
    # Status and health
    status = Column(Enum(IntegrationStatus), default=IntegrationStatus.PENDING)
    last_sync_at = Column(DateTime(timezone=True))
    last_error = Column(Text)
    error_count = Column(Integer, default=0)
    
    # Rate limiting
    rate_limit = Column(Integer)  # Requests per minute
    requests_made = Column(Integer, default=0)
    rate_limit_reset_at = Column(DateTime(timezone=True))
    
    # Usage statistics
    total_requests = Column(Integer, default=0)
    successful_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    
    # Sync configuration
    auto_sync_enabled = Column(Boolean, default=True)
    sync_frequency = Column(String(50), default="hourly")  # realtime, hourly, daily, weekly
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    connected_at = Column(DateTime(timezone=True))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    webhooks = relationship("WebhookAdmin", back_populates="integration", cascade="all, delete-orphan")
    api_logs = relationship("APILogAdmin", back_populates="integration")

# Webhook Management
class WebhookAdmin(Base):
    __tablename__ = "webhooks"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    integration_id = Column(UUID(as_uuid=True), ForeignKey("integrations.id"))
    
    # Webhook details
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    method = Column(String(10), default="POST")
    
    # Event configuration
    events = Column(JSON, nullable=False)  # List of events to listen for
    event_filters = Column(JSON, default={})  # Additional filtering criteria
    
    # Security
    secret = Column(String(255))  # Webhook secret for verification
    auth_header = Column(String(255))  # Authorization header
    
    # Retry configuration
    max_retries = Column(Integer, default=3)
    retry_delay = Column(Integer, default=5)  # Seconds
    timeout = Column(Integer, default=30)  # Seconds
    
    # Status and health
    status = Column(Enum(WebhookStatus), default=WebhookStatus.ACTIVE)
    last_triggered_at = Column(DateTime(timezone=True))
    last_success_at = Column(DateTime(timezone=True))
    last_failure_at = Column(DateTime(timezone=True))
    failure_count = Column(Integer, default=0)
    
    # Statistics
    total_deliveries = Column(Integer, default=0)
    successful_deliveries = Column(Integer, default=0)
    failed_deliveries = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    integration = relationship("IntegrationAdmin", back_populates="webhooks")
    deliveries = relationship("WebhookDeliveryAdmin", back_populates="webhook", cascade="all, delete-orphan")

# Webhook Delivery Log
class WebhookDeliveryAdmin(Base):
    __tablename__ = "webhook_deliveries"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    webhook_id = Column(UUID(as_uuid=True), ForeignKey("webhooks.id"), nullable=False)
    
    # Delivery details
    event_type = Column(String(100), nullable=False)
    payload = Column(JSON)  # The payload sent
    
    # HTTP details
    response_status = Column(Integer)
    response_body = Column(Text)
    response_headers = Column(JSON)
    response_time_ms = Column(Integer)
    
    # Delivery status
    is_successful = Column(Boolean, default=False)
    attempt_number = Column(Integer, default=1)
    error_message = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    delivered_at = Column(DateTime(timezone=True))
    
    # Relationships
    webhook = relationship("WebhookAdmin", back_populates="deliveries")

# External Service APIs
class ExternalServiceAdmin(Base):
    __tablename__ = "external_services"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))  # Nullable for global services
    
    # Service details
    name = Column(String(255), nullable=False)
    provider = Column(String(100), nullable=False)  # stripe, mailchimp, etc.
    service_type = Column(Enum(ServiceType), nullable=False)
    description = Column(Text)
    
    # API configuration
    base_url = Column(String(500), nullable=False)
    api_version = Column(String(50))
    documentation_url = Column(String(500))
    
    # Service limits
    rate_limit = Column(Integer)  # Requests per minute
    daily_limit = Column(Integer)
    monthly_limit = Column(Integer)
    
    # Health monitoring
    is_healthy = Column(Boolean, default=True)
    last_health_check = Column(DateTime(timezone=True))
    response_time_avg = Column(Float)  # Average response time in ms
    uptime_percentage = Column(Float, default=100.0)
    
    # Service metadata
    features = Column(JSON, default=[])
    supported_regions = Column(JSON, default=[])
    pricing_model = Column(String(100))
    
    # Status
    is_active = Column(Boolean, default=True)
    is_deprecated = Column(Boolean, default=False)
    deprecation_date = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

# API Key Management
class APIKeyAdmin(Base):
    __tablename__ = "api_keys"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Key details
    name = Column(String(255), nullable=False)
    key_hash = Column(String(255), nullable=False, unique=True, index=True)
    key_prefix = Column(String(20))  # First few characters for identification
    
    # Permissions and scope
    scopes = Column(JSON, default=[])
    permissions = Column(JSON, default={})
    allowed_endpoints = Column(JSON, default=[])
    
    # Rate limiting
    rate_limit = Column(Integer, default=1000)  # Requests per hour
    requests_made = Column(Integer, default=0)
    rate_limit_reset_at = Column(DateTime(timezone=True))
    
    # IP restrictions
    allowed_ips = Column(JSON, default=[])
    blocked_ips = Column(JSON, default=[])
    
    # Usage tracking
    total_requests = Column(Integer, default=0)
    last_used_at = Column(DateTime(timezone=True))
    last_used_ip = Column(String(45))
    last_user_agent = Column(Text)
    
    # Key lifecycle
    expires_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    
    # Security
    rotation_required = Column(Boolean, default=False)
    last_rotation_at = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

# API Request Logging
class APILogAdmin(Base):
    __tablename__ = "api_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    integration_id = Column(UUID(as_uuid=True), ForeignKey("integrations.id"))
    api_key_id = Column(UUID(as_uuid=True), ForeignKey("api_keys.id"))
    
    # Request details
    method = Column(String(10), nullable=False)
    endpoint = Column(String(500), nullable=False)
    url = Column(String(1000))
    
    # Request data
    request_headers = Column(JSON)
    request_body = Column(Text)
    query_parameters = Column(JSON)
    
    # Response data
    response_status = Column(Integer)
    response_headers = Column(JSON)
    response_body = Column(Text)
    response_time_ms = Column(Integer)
    
    # Client information
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # Error handling
    error_message = Column(Text)
    error_code = Column(String(50))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    
    # Relationships
    integration = relationship("IntegrationAdmin", back_populates="api_logs")

# Data Sync Jobs
class DataSyncJobAdmin(Base):
    __tablename__ = "data_sync_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    integration_id = Column(UUID(as_uuid=True), ForeignKey("integrations.id"), nullable=False)
    
    # Job details
    job_type = Column(String(100), nullable=False)  # import, export, sync
    data_type = Column(String(100), nullable=False)  # contacts, products, orders, etc.
    direction = Column(String(20), nullable=False)  # inbound, outbound, bidirectional
    
    # Job configuration
    filters = Column(JSON, default={})
    mapping_config = Column(JSON, default={})
    
    # Progress tracking
    status = Column(String(50), default="pending")  # pending, running, completed, failed, cancelled
    total_records = Column(Integer, default=0)
    processed_records = Column(Integer, default=0)
    successful_records = Column(Integer, default=0)
    failed_records = Column(Integer, default=0)
    progress_percentage = Column(Float, default=0.0)
    
    # Timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer)
    
    # Results
    result_summary = Column(JSON)
    error_log = Column(Text)
    success_message = Column(Text)
    
    # Scheduling
    is_scheduled = Column(Boolean, default=False)
    schedule_cron = Column(String(100))
    next_run_at = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

# Automation Rules
class AutomationRuleAdmin(Base):
    __tablename__ = "automation_rules"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    # Rule details
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Trigger configuration
    trigger_type = Column(String(100), nullable=False)  # event, schedule, webhook, etc.
    trigger_config = Column(JSON, nullable=False)
    trigger_conditions = Column(JSON, default=[])
    
    # Actions to perform
    actions = Column(JSON, nullable=False)  # List of actions to execute
    
    # Execution settings
    is_active = Column(Boolean, default=True)
    execution_order = Column(Integer, default=0)
    max_executions = Column(Integer)  # Limit number of executions
    
    # Statistics
    execution_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)
    last_executed_at = Column(DateTime(timezone=True))
    
    # Error handling
    on_error_action = Column(String(50), default="stop")  # stop, continue, retry
    retry_attempts = Column(Integer, default=3)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

# Automation Execution Log
class AutomationExecutionAdmin(Base):
    __tablename__ = "automation_executions"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    rule_id = Column(UUID(as_uuid=True), ForeignKey("automation_rules.id"), nullable=False)
    
    # Execution details
    trigger_data = Column(JSON)  # Data that triggered the automation
    execution_context = Column(JSON)  # Context at time of execution
    
    # Results
    status = Column(String(50), nullable=False)  # success, failure, partial
    actions_executed = Column(Integer, default=0)
    actions_successful = Column(Integer, default=0)
    actions_failed = Column(Integer, default=0)
    
    # Performance
    execution_time_ms = Column(Integer)
    
    # Error handling
    error_message = Column(Text)
    error_details = Column(JSON)
    
    # Output data
    output_data = Column(JSON)  # Results of the automation
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))