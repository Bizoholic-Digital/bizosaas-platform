#!/usr/bin/env python3

"""
Monitoring Models for SQLAdmin Dashboard
Comprehensive infrastructure monitoring models for BizOSaaS platform
"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, JSON, ForeignKey, UUID, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

Base = declarative_base()

# ============================================================================
# AI AGENTS MONITORING MODELS
# ============================================================================

class AIAgentMonitoring(Base):
    """Monitor AI agent performance and status"""
    __tablename__ = "ai_agent_monitoring"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_name = Column(String(100), nullable=False)
    agent_type = Column(String(50), nullable=False)  # crewai, langchain, custom
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    status = Column(String(20), default='active')  # active, idle, error, offline
    last_execution = Column(DateTime(timezone=True))
    response_time_ms = Column(Integer)
    success_rate = Column(Float)  # Percentage
    error_count = Column(Integer, default=0)
    total_executions = Column(BigInteger, default=0)
    memory_usage_mb = Column(Float)
    cpu_usage_percent = Column(Float)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON)

class WorkflowExecution(Base):
    """Track workflow execution monitoring"""
    __tablename__ = "workflow_executions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(String(100), nullable=False)
    workflow_name = Column(String(200))
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    execution_status = Column(String(20))  # running, completed, failed, cancelled
    started_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at = Column(DateTime(timezone=True))
    duration_ms = Column(BigInteger)
    steps_total = Column(Integer)
    steps_completed = Column(Integer)
    steps_failed = Column(Integer)
    error_message = Column(Text)
    input_data = Column(JSON)
    output_data = Column(JSON)
    resource_usage = Column(JSON)  # CPU, memory, API calls
    triggered_by = Column(String(100))  # user_id, schedule, webhook, etc.

class AgentErrorLog(Base):
    """Track AI agent errors and debugging info"""
    __tablename__ = "agent_error_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_name = Column(String(100), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    error_type = Column(String(50))  # api_error, timeout, memory_error, etc.
    severity = Column(String(20))  # low, medium, high, critical
    error_message = Column(Text)
    stack_trace = Column(Text)
    context_data = Column(JSON)
    occurred_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    resolved_at = Column(DateTime(timezone=True))
    resolution_notes = Column(Text)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

# ============================================================================
# SYSTEM INFRASTRUCTURE MONITORING MODELS
# ============================================================================

class DatabaseHealthMetrics(Base):
    """Monitor PostgreSQL database health and performance"""
    __tablename__ = "database_health_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    active_connections = Column(Integer)
    total_connections = Column(Integer)
    max_connections = Column(Integer)
    idle_connections = Column(Integer)
    database_size_mb = Column(BigInteger)
    cache_hit_ratio = Column(Float)
    checkpoint_frequency = Column(Integer)
    slow_query_count = Column(Integer)
    deadlock_count = Column(Integer)
    temp_files_count = Column(Integer)
    temp_files_size_mb = Column(BigInteger)
    replication_lag_ms = Column(BigInteger)
    vacuum_last_run = Column(DateTime(timezone=True))
    analyze_last_run = Column(DateTime(timezone=True))
    disk_usage_percent = Column(Float)
    memory_usage_percent = Column(Float)
    cpu_usage_percent = Column(Float)

class RedisHealthMetrics(Base):
    """Monitor Redis cache health and performance"""
    __tablename__ = "redis_health_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    connected_clients = Column(Integer)
    blocked_clients = Column(Integer)
    used_memory_mb = Column(BigInteger)
    used_memory_peak_mb = Column(BigInteger)
    memory_usage_percent = Column(Float)
    keyspace_hits = Column(BigInteger)
    keyspace_misses = Column(BigInteger)
    hit_rate_percent = Column(Float)
    evicted_keys = Column(BigInteger)
    expired_keys = Column(BigInteger)
    total_keys = Column(BigInteger)
    operations_per_second = Column(Float)
    network_input_mb = Column(Float)
    network_output_mb = Column(Float)
    cpu_usage_percent = Column(Float)
    replication_offset = Column(BigInteger)

class ContainerMetrics(Base):
    """Monitor Docker container status and resource usage"""
    __tablename__ = "container_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    container_name = Column(String(100), nullable=False)
    container_id = Column(String(64))
    status = Column(String(20))  # running, stopped, paused, dead
    cpu_usage_percent = Column(Float)
    memory_usage_mb = Column(Float)
    memory_limit_mb = Column(Float)
    memory_usage_percent = Column(Float)
    network_rx_mb = Column(Float)
    network_tx_mb = Column(Float)
    disk_read_mb = Column(Float)
    disk_write_mb = Column(Float)
    restart_count = Column(Integer)
    uptime_seconds = Column(BigInteger)
    health_status = Column(String(20))  # healthy, unhealthy, starting

class APIEndpointMetrics(Base):
    """Monitor API endpoint performance and availability"""
    __tablename__ = "api_endpoint_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    endpoint_url = Column(String(500), nullable=False)
    method = Column(String(10))  # GET, POST, PUT, DELETE
    service_name = Column(String(100))
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    response_time_ms = Column(Integer)
    status_code = Column(Integer)
    success_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    total_requests = Column(BigInteger, default=0)
    average_response_time = Column(Float)
    p95_response_time = Column(Float)
    p99_response_time = Column(Float)
    error_rate_percent = Column(Float)
    throughput_rps = Column(Float)  # Requests per second

# ============================================================================
# BUSINESS OPERATIONS MONITORING MODELS
# ============================================================================

class TenantActivityMetrics(Base):
    """Monitor tenant activity and usage patterns"""
    __tablename__ = "tenant_activity_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    date = Column(DateTime(timezone=True), default=datetime.utcnow)
    active_users = Column(Integer, default=0)
    total_logins = Column(Integer, default=0)
    unique_logins = Column(Integer, default=0)
    session_duration_avg = Column(Float)  # Average session duration in minutes
    api_calls_count = Column(BigInteger, default=0)
    workflow_executions = Column(Integer, default=0)
    ai_agent_calls = Column(Integer, default=0)
    storage_used_mb = Column(BigInteger, default=0)
    bandwidth_used_mb = Column(BigInteger, default=0)
    feature_usage = Column(JSON)  # Track which features are being used
    platform_usage = Column(JSON)  # Usage across different platforms
    revenue_generated = Column(Float)
    costs_incurred = Column(Float)

class UserSessionAnalytics(Base):
    """Track user session analytics and behavior"""
    __tablename__ = "user_session_analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    session_start = Column(DateTime(timezone=True), default=datetime.utcnow)
    session_end = Column(DateTime(timezone=True))
    duration_minutes = Column(Float)
    pages_visited = Column(Integer, default=0)
    actions_performed = Column(Integer, default=0)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    device_type = Column(String(50))  # desktop, mobile, tablet
    browser = Column(String(50))
    operating_system = Column(String(50))
    country = Column(String(50))
    city = Column(String(100))
    referrer = Column(String(500))
    exit_page = Column(String(500))
    conversion_events = Column(JSON)  # Track conversion actions

class PlatformUsageStats(Base):
    """Track platform-wide usage statistics"""
    __tablename__ = "platform_usage_stats"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime(timezone=True), default=datetime.utcnow)
    total_users = Column(Integer, default=0)
    active_users_daily = Column(Integer, default=0)
    active_users_weekly = Column(Integer, default=0)
    active_users_monthly = Column(Integer, default=0)
    new_signups = Column(Integer, default=0)
    churn_count = Column(Integer, default=0)
    total_tenants = Column(Integer, default=0)
    active_tenants = Column(Integer, default=0)
    total_revenue = Column(Float, default=0)
    recurring_revenue = Column(Float, default=0)
    average_revenue_per_user = Column(Float, default=0)
    cost_per_acquisition = Column(Float, default=0)
    lifetime_value = Column(Float, default=0)
    feature_adoption_rates = Column(JSON)
    support_tickets = Column(Integer, default=0)
    system_uptime_percent = Column(Float, default=100)

# ============================================================================
# SECURITY & COMPLIANCE MONITORING MODELS
# ============================================================================

class SecurityEventLog(Base):
    """Track security events and potential threats"""
    __tablename__ = "security_event_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String(50), nullable=False)  # login_failure, suspicious_activity, etc.
    severity = Column(String(20))  # low, medium, high, critical
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    event_details = Column(JSON)
    occurred_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    resolved_at = Column(DateTime(timezone=True))
    action_taken = Column(Text)
    risk_score = Column(Integer)  # 1-100 risk assessment
    geo_location = Column(JSON)  # Country, city, coordinates
    is_blocked = Column(Boolean, default=False)
    false_positive = Column(Boolean, default=False)

class AuthenticationLog(Base):
    """Track authentication attempts and patterns"""
    __tablename__ = "authentication_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    email_attempted = Column(String(255))
    login_method = Column(String(50))  # password, oauth, sso, api_key
    success = Column(Boolean, nullable=False)
    failure_reason = Column(String(100))  # invalid_password, account_locked, etc.
    ip_address = Column(String(45))
    user_agent = Column(Text)
    device_fingerprint = Column(String(100))
    geo_location = Column(JSON)
    mfa_used = Column(Boolean, default=False)
    mfa_method = Column(String(50))  # totp, sms, email
    session_id = Column(UUID(as_uuid=True))
    attempted_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    risk_assessment = Column(JSON)  # IP reputation, device trust, etc.

class RateLimitStatus(Base):
    """Monitor rate limiting status and violations"""
    __tablename__ = "rate_limit_status"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identifier = Column(String(255), nullable=False)  # IP, user_id, api_key
    identifier_type = Column(String(50))  # ip, user, api_key, tenant
    endpoint = Column(String(500))
    limit_type = Column(String(50))  # requests_per_minute, requests_per_hour, etc.
    limit_value = Column(Integer)
    current_count = Column(Integer, default=0)
    window_start = Column(DateTime(timezone=True), default=datetime.utcnow)
    window_end = Column(DateTime(timezone=True))
    violations = Column(Integer, default=0)
    last_violation = Column(DateTime(timezone=True))
    is_blocked = Column(Boolean, default=False)
    blocked_until = Column(DateTime(timezone=True))
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))

class AdminActionAudit(Base):
    """Audit trail for admin actions"""
    __tablename__ = "admin_action_audit"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    admin_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action_type = Column(String(100), nullable=False)  # user_modification, system_configuration, etc.
    resource_type = Column(String(50))  # user, tenant, system_setting
    resource_id = Column(String(100))
    action_details = Column(JSON)
    before_state = Column(JSON)
    after_state = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    performed_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    compliance_flags = Column(JSON)  # GDPR, SOX, etc.

# ============================================================================
# INTEGRATION MONITORING MODELS
# ============================================================================

class ExternalAPIHealth(Base):
    """Monitor external API health and connectivity"""
    __tablename__ = "external_api_health"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    api_name = Column(String(100), nullable=False)  # openai, stripe, hubspot, etc.
    api_url = Column(String(500))
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    status = Column(String(20))  # healthy, degraded, down
    response_time_ms = Column(Integer)
    status_code = Column(Integer)
    error_message = Column(Text)
    success_rate_24h = Column(Float)
    average_response_time_24h = Column(Float)
    uptime_percent_24h = Column(Float)
    last_success = Column(DateTime(timezone=True))
    last_failure = Column(DateTime(timezone=True))
    consecutive_failures = Column(Integer, default=0)
    checked_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    api_key_valid = Column(Boolean)
    rate_limit_remaining = Column(Integer)
    quota_usage_percent = Column(Float)

class WebhookDeliveryStatus(Base):
    """Track webhook delivery status and retries"""
    __tablename__ = "webhook_delivery_status"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    webhook_id = Column(String(100))
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    destination_url = Column(String(500), nullable=False)
    event_type = Column(String(100))
    payload_size_bytes = Column(Integer)
    delivery_attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)
    status = Column(String(20))  # pending, delivered, failed, abandoned
    last_attempt_at = Column(DateTime(timezone=True))
    next_retry_at = Column(DateTime(timezone=True))
    response_code = Column(Integer)
    response_time_ms = Column(Integer)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    delivered_at = Column(DateTime(timezone=True))
    payload_hash = Column(String(64))  # For deduplication

class DataSyncStatus(Base):
    """Monitor data synchronization across services"""
    __tablename__ = "data_sync_status"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sync_job_id = Column(String(100), nullable=False)
    source_service = Column(String(100))
    destination_service = Column(String(100))
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    data_type = Column(String(100))  # users, leads, orders, analytics
    sync_type = Column(String(50))  # full, incremental, real_time
    status = Column(String(20))  # running, completed, failed, paused
    started_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at = Column(DateTime(timezone=True))
    records_processed = Column(BigInteger, default=0)
    records_success = Column(BigInteger, default=0)
    records_failed = Column(BigInteger, default=0)
    last_processed_id = Column(String(100))
    error_details = Column(JSON)
    performance_metrics = Column(JSON)  # throughput, memory usage, etc.
    next_sync_scheduled = Column(DateTime(timezone=True))

class IntegrationConnectivity(Base):
    """Monitor third-party service connectivity"""
    __tablename__ = "integration_connectivity"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_name = Column(String(100), nullable=False)
    service_type = Column(String(50))  # payment, crm, marketing, analytics
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    connection_status = Column(String(20))  # connected, disconnected, error
    last_successful_call = Column(DateTime(timezone=True))
    last_failed_call = Column(DateTime(timezone=True))
    total_calls_24h = Column(Integer, default=0)
    successful_calls_24h = Column(Integer, default=0)
    failed_calls_24h = Column(Integer, default=0)
    average_latency_ms = Column(Float)
    error_rate_percent = Column(Float)
    quota_used = Column(BigInteger, default=0)
    quota_limit = Column(BigInteger)
    quota_reset_at = Column(DateTime(timezone=True))
    configuration_valid = Column(Boolean, default=True)
    last_configuration_check = Column(DateTime(timezone=True))
    health_checked_at = Column(DateTime(timezone=True), default=datetime.utcnow)

# ============================================================================
# SYSTEM ALERTS AND NOTIFICATIONS
# ============================================================================

class SystemAlert(Base):
    """System-wide alerts and notifications"""
    __tablename__ = "system_alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_type = Column(String(50), nullable=False)  # performance, security, business
    severity = Column(String(20))  # info, warning, error, critical
    title = Column(String(200), nullable=False)
    description = Column(Text)
    source_service = Column(String(100))
    affected_tenants = Column(JSON)  # List of tenant IDs affected
    metric_name = Column(String(100))
    threshold_value = Column(Float)
    current_value = Column(Float)
    alert_data = Column(JSON)  # Additional context data
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    acknowledged_at = Column(DateTime(timezone=True))
    acknowledged_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    resolved_at = Column(DateTime(timezone=True))
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    resolution_notes = Column(Text)
    is_active = Column(Boolean, default=True)
    notification_sent = Column(Boolean, default=False)
    escalation_level = Column(Integer, default=1)
    parent_alert_id = Column(UUID(as_uuid=True), ForeignKey("system_alerts.id"))