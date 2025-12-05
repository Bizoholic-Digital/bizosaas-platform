#!/usr/bin/env python3

"""
Monitoring Views for SQLAdmin Dashboard
Enhanced admin views for comprehensive infrastructure monitoring
"""

from sqladmin import ModelView, BaseView
from sqlalchemy import text, func, desc, and_, or_
from sqlalchemy.orm import sessionmaker
from fastapi import Request
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
import json

from monitoring_models import (
    # AI Monitoring
    AIAgentMonitoring, WorkflowExecution, AgentErrorLog,
    # System Infrastructure
    DatabaseHealthMetrics, RedisHealthMetrics, ContainerMetrics, APIEndpointMetrics,
    # Business Operations
    TenantActivityMetrics, UserSessionAnalytics, PlatformUsageStats,
    # Security & Compliance
    SecurityEventLog, AuthenticationLog, RateLimitStatus, AdminActionAudit,
    # Integration Monitoring
    ExternalAPIHealth, WebhookDeliveryStatus, DataSyncStatus, IntegrationConnectivity,
    # Alerts
    SystemAlert
)

# ============================================================================
# AI AGENTS MONITORING VIEWS
# ============================================================================

class AIAgentMonitoringView(ModelView, model=AIAgentMonitoring):
    name = "AI Agent Monitoring"
    identity = "ai_agent_monitoring"
    category = "AI Monitoring"
    
    column_list = [
        AIAgentMonitoring.agent_name, AIAgentMonitoring.agent_type, 
        AIAgentMonitoring.status, AIAgentMonitoring.success_rate,
        AIAgentMonitoring.response_time_ms, AIAgentMonitoring.error_count,
        AIAgentMonitoring.last_execution, AIAgentMonitoring.updated_at
    ]
    
    column_details_list = [
        AIAgentMonitoring.id, AIAgentMonitoring.agent_name, AIAgentMonitoring.agent_type,
        AIAgentMonitoring.tenant_id, AIAgentMonitoring.status, AIAgentMonitoring.last_execution,
        AIAgentMonitoring.response_time_ms, AIAgentMonitoring.success_rate,
        AIAgentMonitoring.error_count, AIAgentMonitoring.total_executions,
        AIAgentMonitoring.memory_usage_mb, AIAgentMonitoring.cpu_usage_percent,
        AIAgentMonitoring.created_at, AIAgentMonitoring.updated_at, AIAgentMonitoring.metadata
    ]
    
    column_searchable_list = [AIAgentMonitoring.agent_name, AIAgentMonitoring.agent_type]
    column_sortable_list = [
        AIAgentMonitoring.agent_name, AIAgentMonitoring.success_rate,
        AIAgentMonitoring.response_time_ms, AIAgentMonitoring.error_count,
        AIAgentMonitoring.last_execution
    ]
    
    column_formatters = {
        AIAgentMonitoring.success_rate: lambda m, a: f"{getattr(m, a, 0):.1f}%" if getattr(m, a) is not None else "N/A",
        AIAgentMonitoring.response_time_ms: lambda m, a: f"{getattr(m, a, 0):,}ms" if getattr(m, a) is not None else "N/A",
        AIAgentMonitoring.memory_usage_mb: lambda m, a: f"{getattr(m, a, 0):.1f}MB" if getattr(m, a) is not None else "N/A",
        AIAgentMonitoring.cpu_usage_percent: lambda m, a: f"{getattr(m, a, 0):.1f}%" if getattr(m, a) is not None else "N/A"
    }

class WorkflowExecutionView(ModelView, model=WorkflowExecution):
    name = "Workflow Executions"
    identity = "workflow_executions"
    category = "AI Monitoring"
    
    column_list = [
        WorkflowExecution.workflow_name, WorkflowExecution.execution_status,
        WorkflowExecution.started_at, WorkflowExecution.duration_ms,
        WorkflowExecution.steps_completed, WorkflowExecution.steps_total,
        WorkflowExecution.triggered_by
    ]
    
    column_details_list = [
        WorkflowExecution.id, WorkflowExecution.workflow_id, WorkflowExecution.workflow_name,
        WorkflowExecution.tenant_id, WorkflowExecution.execution_status,
        WorkflowExecution.started_at, WorkflowExecution.completed_at, WorkflowExecution.duration_ms,
        WorkflowExecution.steps_total, WorkflowExecution.steps_completed, WorkflowExecution.steps_failed,
        WorkflowExecution.error_message, WorkflowExecution.triggered_by,
        WorkflowExecution.input_data, WorkflowExecution.output_data, WorkflowExecution.resource_usage
    ]
    
    column_searchable_list = [WorkflowExecution.workflow_name, WorkflowExecution.triggered_by]
    column_sortable_list = [
        WorkflowExecution.started_at, WorkflowExecution.duration_ms,
        WorkflowExecution.execution_status
    ]
    
    column_formatters = {
        WorkflowExecution.duration_ms: lambda m, a: f"{getattr(m, a, 0):,}ms" if getattr(m, a) is not None else "Running...",
        WorkflowExecution.steps_completed: lambda m, a: f"{getattr(m, a, 0)}/{getattr(m, 'steps_total', 0)}"
    }

class AgentErrorLogView(ModelView, model=AgentErrorLog):
    name = "Agent Error Logs"
    identity = "agent_error_logs"
    category = "AI Monitoring"
    
    column_list = [
        AgentErrorLog.agent_name, AgentErrorLog.error_type,
        AgentErrorLog.severity, AgentErrorLog.occurred_at,
        AgentErrorLog.resolved_at
    ]
    
    column_details_list = [
        AgentErrorLog.id, AgentErrorLog.agent_name, AgentErrorLog.tenant_id,
        AgentErrorLog.error_type, AgentErrorLog.severity, AgentErrorLog.error_message,
        AgentErrorLog.stack_trace, AgentErrorLog.context_data,
        AgentErrorLog.occurred_at, AgentErrorLog.resolved_at,
        AgentErrorLog.resolution_notes, AgentErrorLog.user_id
    ]
    
    column_searchable_list = [AgentErrorLog.agent_name, AgentErrorLog.error_type, AgentErrorLog.error_message]
    column_sortable_list = [AgentErrorLog.occurred_at, AgentErrorLog.severity]

# ============================================================================
# SYSTEM INFRASTRUCTURE MONITORING VIEWS
# ============================================================================

class DatabaseHealthMetricsView(ModelView, model=DatabaseHealthMetrics):
    name = "Database Health"
    identity = "database_health_metrics"
    category = "Infrastructure"
    
    column_list = [
        DatabaseHealthMetrics.timestamp, DatabaseHealthMetrics.active_connections,
        DatabaseHealthMetrics.cache_hit_ratio, DatabaseHealthMetrics.slow_query_count,
        DatabaseHealthMetrics.cpu_usage_percent, DatabaseHealthMetrics.memory_usage_percent
    ]
    
    column_details_list = [
        DatabaseHealthMetrics.id, DatabaseHealthMetrics.timestamp,
        DatabaseHealthMetrics.active_connections, DatabaseHealthMetrics.total_connections,
        DatabaseHealthMetrics.max_connections, DatabaseHealthMetrics.idle_connections,
        DatabaseHealthMetrics.database_size_mb, DatabaseHealthMetrics.cache_hit_ratio,
        DatabaseHealthMetrics.checkpoint_frequency, DatabaseHealthMetrics.slow_query_count,
        DatabaseHealthMetrics.deadlock_count, DatabaseHealthMetrics.temp_files_count,
        DatabaseHealthMetrics.temp_files_size_mb, DatabaseHealthMetrics.replication_lag_ms,
        DatabaseHealthMetrics.vacuum_last_run, DatabaseHealthMetrics.analyze_last_run,
        DatabaseHealthMetrics.disk_usage_percent, DatabaseHealthMetrics.memory_usage_percent,
        DatabaseHealthMetrics.cpu_usage_percent
    ]
    
    column_sortable_list = [DatabaseHealthMetrics.timestamp]
    
    column_formatters = {
        DatabaseHealthMetrics.cache_hit_ratio: lambda m, a: f"{getattr(m, a, 0):.2f}%" if getattr(m, a) is not None else "N/A",
        DatabaseHealthMetrics.database_size_mb: lambda m, a: f"{getattr(m, a, 0):,}MB" if getattr(m, a) is not None else "N/A",
        DatabaseHealthMetrics.cpu_usage_percent: lambda m, a: f"{getattr(m, a, 0):.1f}%" if getattr(m, a) is not None else "N/A",
        DatabaseHealthMetrics.memory_usage_percent: lambda m, a: f"{getattr(m, a, 0):.1f}%" if getattr(m, a) is not None else "N/A"
    }

class RedisHealthMetricsView(ModelView, model=RedisHealthMetrics):
    name = "Redis Health"
    identity = "redis_health_metrics"
    category = "Infrastructure"
    
    column_list = [
        RedisHealthMetrics.timestamp, RedisHealthMetrics.connected_clients,
        RedisHealthMetrics.used_memory_mb, RedisHealthMetrics.hit_rate_percent,
        RedisHealthMetrics.operations_per_second, RedisHealthMetrics.cpu_usage_percent
    ]
    
    column_details_list = [
        RedisHealthMetrics.id, RedisHealthMetrics.timestamp,
        RedisHealthMetrics.connected_clients, RedisHealthMetrics.blocked_clients,
        RedisHealthMetrics.used_memory_mb, RedisHealthMetrics.used_memory_peak_mb,
        RedisHealthMetrics.memory_usage_percent, RedisHealthMetrics.keyspace_hits,
        RedisHealthMetrics.keyspace_misses, RedisHealthMetrics.hit_rate_percent,
        RedisHealthMetrics.evicted_keys, RedisHealthMetrics.expired_keys,
        RedisHealthMetrics.total_keys, RedisHealthMetrics.operations_per_second,
        RedisHealthMetrics.network_input_mb, RedisHealthMetrics.network_output_mb,
        RedisHealthMetrics.cpu_usage_percent, RedisHealthMetrics.replication_offset
    ]
    
    column_sortable_list = [RedisHealthMetrics.timestamp]
    
    column_formatters = {
        RedisHealthMetrics.used_memory_mb: lambda m, a: f"{getattr(m, a, 0):,}MB" if getattr(m, a) is not None else "N/A",
        RedisHealthMetrics.hit_rate_percent: lambda m, a: f"{getattr(m, a, 0):.2f}%" if getattr(m, a) is not None else "N/A",
        RedisHealthMetrics.operations_per_second: lambda m, a: f"{getattr(m, a, 0):.0f} ops/s" if getattr(m, a) is not None else "N/A"
    }

class ContainerMetricsView(ModelView, model=ContainerMetrics):
    name = "Container Metrics"
    identity = "container_metrics"
    category = "Infrastructure"
    
    column_list = [
        ContainerMetrics.container_name, ContainerMetrics.status,
        ContainerMetrics.cpu_usage_percent, ContainerMetrics.memory_usage_percent,
        ContainerMetrics.restart_count, ContainerMetrics.health_status,
        ContainerMetrics.timestamp
    ]
    
    column_details_list = [
        ContainerMetrics.id, ContainerMetrics.timestamp, ContainerMetrics.container_name,
        ContainerMetrics.container_id, ContainerMetrics.status,
        ContainerMetrics.cpu_usage_percent, ContainerMetrics.memory_usage_mb,
        ContainerMetrics.memory_limit_mb, ContainerMetrics.memory_usage_percent,
        ContainerMetrics.network_rx_mb, ContainerMetrics.network_tx_mb,
        ContainerMetrics.disk_read_mb, ContainerMetrics.disk_write_mb,
        ContainerMetrics.restart_count, ContainerMetrics.uptime_seconds,
        ContainerMetrics.health_status
    ]
    
    column_searchable_list = [ContainerMetrics.container_name]
    column_sortable_list = [ContainerMetrics.timestamp, ContainerMetrics.container_name]
    
    column_formatters = {
        ContainerMetrics.memory_usage_mb: lambda m, a: f"{getattr(m, a, 0):.1f}MB" if getattr(m, a) is not None else "N/A",
        ContainerMetrics.uptime_seconds: lambda m, a: f"{getattr(m, a, 0) // 3600:.0f}h {(getattr(m, a, 0) % 3600) // 60:.0f}m" if getattr(m, a) is not None else "N/A"
    }

class APIEndpointMetricsView(ModelView, model=APIEndpointMetrics):
    name = "API Endpoint Metrics"
    identity = "api_endpoint_metrics"
    category = "Infrastructure"
    
    column_list = [
        APIEndpointMetrics.service_name, APIEndpointMetrics.endpoint_url,
        APIEndpointMetrics.method, APIEndpointMetrics.average_response_time,
        APIEndpointMetrics.error_rate_percent, APIEndpointMetrics.throughput_rps,
        APIEndpointMetrics.timestamp
    ]
    
    column_details_list = [
        APIEndpointMetrics.id, APIEndpointMetrics.timestamp,
        APIEndpointMetrics.endpoint_url, APIEndpointMetrics.method,
        APIEndpointMetrics.service_name, APIEndpointMetrics.tenant_id,
        APIEndpointMetrics.response_time_ms, APIEndpointMetrics.status_code,
        APIEndpointMetrics.success_count, APIEndpointMetrics.error_count,
        APIEndpointMetrics.total_requests, APIEndpointMetrics.average_response_time,
        APIEndpointMetrics.p95_response_time, APIEndpointMetrics.p99_response_time,
        APIEndpointMetrics.error_rate_percent, APIEndpointMetrics.throughput_rps
    ]
    
    column_searchable_list = [APIEndpointMetrics.service_name, APIEndpointMetrics.endpoint_url]
    column_sortable_list = [
        APIEndpointMetrics.timestamp, APIEndpointMetrics.average_response_time,
        APIEndpointMetrics.error_rate_percent, APIEndpointMetrics.throughput_rps
    ]
    
    column_formatters = {
        APIEndpointMetrics.average_response_time: lambda m, a: f"{getattr(m, a, 0):.0f}ms" if getattr(m, a) is not None else "N/A",
        APIEndpointMetrics.error_rate_percent: lambda m, a: f"{getattr(m, a, 0):.2f}%" if getattr(m, a) is not None else "N/A",
        APIEndpointMetrics.throughput_rps: lambda m, a: f"{getattr(m, a, 0):.1f} req/s" if getattr(m, a) is not None else "N/A"
    }

# ============================================================================
# BUSINESS OPERATIONS MONITORING VIEWS
# ============================================================================

class TenantActivityMetricsView(ModelView, model=TenantActivityMetrics):
    name = "Tenant Activity"
    identity = "tenant_activity_metrics"
    category = "Business Operations"
    
    column_list = [
        TenantActivityMetrics.tenant_id, TenantActivityMetrics.date,
        TenantActivityMetrics.active_users, TenantActivityMetrics.total_logins,
        TenantActivityMetrics.api_calls_count, TenantActivityMetrics.workflow_executions,
        TenantActivityMetrics.revenue_generated
    ]
    
    column_details_list = [
        TenantActivityMetrics.id, TenantActivityMetrics.tenant_id, TenantActivityMetrics.date,
        TenantActivityMetrics.active_users, TenantActivityMetrics.total_logins,
        TenantActivityMetrics.unique_logins, TenantActivityMetrics.session_duration_avg,
        TenantActivityMetrics.api_calls_count, TenantActivityMetrics.workflow_executions,
        TenantActivityMetrics.ai_agent_calls, TenantActivityMetrics.storage_used_mb,
        TenantActivityMetrics.bandwidth_used_mb, TenantActivityMetrics.feature_usage,
        TenantActivityMetrics.platform_usage, TenantActivityMetrics.revenue_generated,
        TenantActivityMetrics.costs_incurred
    ]
    
    column_sortable_list = [
        TenantActivityMetrics.date, TenantActivityMetrics.active_users,
        TenantActivityMetrics.revenue_generated
    ]
    
    column_formatters = {
        TenantActivityMetrics.storage_used_mb: lambda m, a: f"{getattr(m, a, 0):,}MB" if getattr(m, a) is not None else "N/A",
        TenantActivityMetrics.bandwidth_used_mb: lambda m, a: f"{getattr(m, a, 0):,}MB" if getattr(m, a) is not None else "N/A",
        TenantActivityMetrics.revenue_generated: lambda m, a: f"${getattr(m, a, 0):.2f}" if getattr(m, a) is not None else "$0.00",
        TenantActivityMetrics.session_duration_avg: lambda m, a: f"{getattr(m, a, 0):.1f}min" if getattr(m, a) is not None else "N/A"
    }

class UserSessionAnalyticsView(ModelView, model=UserSessionAnalytics):
    name = "User Session Analytics"
    identity = "user_session_analytics"
    category = "Business Operations"
    
    column_list = [
        UserSessionAnalytics.user_id, UserSessionAnalytics.session_start,
        UserSessionAnalytics.duration_minutes, UserSessionAnalytics.pages_visited,
        UserSessionAnalytics.device_type, UserSessionAnalytics.country
    ]
    
    column_details_list = [
        UserSessionAnalytics.id, UserSessionAnalytics.user_id, UserSessionAnalytics.tenant_id,
        UserSessionAnalytics.session_start, UserSessionAnalytics.session_end,
        UserSessionAnalytics.duration_minutes, UserSessionAnalytics.pages_visited,
        UserSessionAnalytics.actions_performed, UserSessionAnalytics.ip_address,
        UserSessionAnalytics.user_agent, UserSessionAnalytics.device_type,
        UserSessionAnalytics.browser, UserSessionAnalytics.operating_system,
        UserSessionAnalytics.country, UserSessionAnalytics.city,
        UserSessionAnalytics.referrer, UserSessionAnalytics.exit_page,
        UserSessionAnalytics.conversion_events
    ]
    
    column_searchable_list = [UserSessionAnalytics.country, UserSessionAnalytics.city]
    column_sortable_list = [
        UserSessionAnalytics.session_start, UserSessionAnalytics.duration_minutes
    ]
    
    column_formatters = {
        UserSessionAnalytics.duration_minutes: lambda m, a: f"{getattr(m, a, 0):.1f}min" if getattr(m, a) is not None else "Active"
    }

class PlatformUsageStatsView(ModelView, model=PlatformUsageStats):
    name = "Platform Usage Statistics"
    identity = "platform_usage_stats"
    category = "Business Operations"
    
    column_list = [
        PlatformUsageStats.date, PlatformUsageStats.total_users,
        PlatformUsageStats.active_users_daily, PlatformUsageStats.new_signups,
        PlatformUsageStats.total_revenue, PlatformUsageStats.system_uptime_percent
    ]
    
    column_details_list = [
        PlatformUsageStats.id, PlatformUsageStats.date,
        PlatformUsageStats.total_users, PlatformUsageStats.active_users_daily,
        PlatformUsageStats.active_users_weekly, PlatformUsageStats.active_users_monthly,
        PlatformUsageStats.new_signups, PlatformUsageStats.churn_count,
        PlatformUsageStats.total_tenants, PlatformUsageStats.active_tenants,
        PlatformUsageStats.total_revenue, PlatformUsageStats.recurring_revenue,
        PlatformUsageStats.average_revenue_per_user, PlatformUsageStats.cost_per_acquisition,
        PlatformUsageStats.lifetime_value, PlatformUsageStats.feature_adoption_rates,
        PlatformUsageStats.support_tickets, PlatformUsageStats.system_uptime_percent
    ]
    
    column_sortable_list = [PlatformUsageStats.date]
    
    column_formatters = {
        PlatformUsageStats.total_revenue: lambda m, a: f"${getattr(m, a, 0):,.2f}" if getattr(m, a) is not None else "$0.00",
        PlatformUsageStats.average_revenue_per_user: lambda m, a: f"${getattr(m, a, 0):.2f}" if getattr(m, a) is not None else "$0.00",
        PlatformUsageStats.system_uptime_percent: lambda m, a: f"{getattr(m, a, 0):.2f}%" if getattr(m, a) is not None else "N/A"
    }

# ============================================================================
# SECURITY & COMPLIANCE MONITORING VIEWS
# ============================================================================

class SecurityEventLogView(ModelView, model=SecurityEventLog):
    name = "Security Events"
    identity = "security_event_logs"
    category = "Security & Compliance"
    
    column_list = [
        SecurityEventLog.event_type, SecurityEventLog.severity,
        SecurityEventLog.occurred_at, SecurityEventLog.ip_address,
        SecurityEventLog.risk_score, SecurityEventLog.is_blocked
    ]
    
    column_details_list = [
        SecurityEventLog.id, SecurityEventLog.event_type, SecurityEventLog.severity,
        SecurityEventLog.user_id, SecurityEventLog.tenant_id, SecurityEventLog.ip_address,
        SecurityEventLog.user_agent, SecurityEventLog.event_details,
        SecurityEventLog.occurred_at, SecurityEventLog.resolved_at,
        SecurityEventLog.action_taken, SecurityEventLog.risk_score,
        SecurityEventLog.geo_location, SecurityEventLog.is_blocked,
        SecurityEventLog.false_positive
    ]
    
    column_searchable_list = [SecurityEventLog.event_type, SecurityEventLog.ip_address]
    column_sortable_list = [
        SecurityEventLog.occurred_at, SecurityEventLog.severity, SecurityEventLog.risk_score
    ]

class AuthenticationLogView(ModelView, model=AuthenticationLog):
    name = "Authentication Logs"
    identity = "authentication_logs"
    category = "Security & Compliance"
    
    column_list = [
        AuthenticationLog.email_attempted, AuthenticationLog.success,
        AuthenticationLog.login_method, AuthenticationLog.attempted_at,
        AuthenticationLog.ip_address, AuthenticationLog.mfa_used
    ]
    
    column_details_list = [
        AuthenticationLog.id, AuthenticationLog.user_id, AuthenticationLog.tenant_id,
        AuthenticationLog.email_attempted, AuthenticationLog.login_method,
        AuthenticationLog.success, AuthenticationLog.failure_reason,
        AuthenticationLog.ip_address, AuthenticationLog.user_agent,
        AuthenticationLog.device_fingerprint, AuthenticationLog.geo_location,
        AuthenticationLog.mfa_used, AuthenticationLog.mfa_method,
        AuthenticationLog.session_id, AuthenticationLog.attempted_at,
        AuthenticationLog.risk_assessment
    ]
    
    column_searchable_list = [AuthenticationLog.email_attempted, AuthenticationLog.ip_address]
    column_sortable_list = [AuthenticationLog.attempted_at]

class RateLimitStatusView(ModelView, model=RateLimitStatus):
    name = "Rate Limit Status"
    identity = "rate_limit_status"
    category = "Security & Compliance"
    
    column_list = [
        RateLimitStatus.identifier, RateLimitStatus.identifier_type,
        RateLimitStatus.endpoint, RateLimitStatus.current_count,
        RateLimitStatus.limit_value, RateLimitStatus.violations,
        RateLimitStatus.is_blocked
    ]
    
    column_details_list = [
        RateLimitStatus.id, RateLimitStatus.identifier, RateLimitStatus.identifier_type,
        RateLimitStatus.endpoint, RateLimitStatus.limit_type, RateLimitStatus.limit_value,
        RateLimitStatus.current_count, RateLimitStatus.window_start,
        RateLimitStatus.window_end, RateLimitStatus.violations,
        RateLimitStatus.last_violation, RateLimitStatus.is_blocked,
        RateLimitStatus.blocked_until, RateLimitStatus.tenant_id
    ]
    
    column_searchable_list = [RateLimitStatus.identifier, RateLimitStatus.endpoint]
    column_sortable_list = [RateLimitStatus.violations, RateLimitStatus.current_count]

class AdminActionAuditView(ModelView, model=AdminActionAudit):
    name = "Admin Action Audit"
    identity = "admin_action_audit"
    category = "Security & Compliance"
    
    column_list = [
        AdminActionAudit.admin_user_id, AdminActionAudit.action_type,
        AdminActionAudit.resource_type, AdminActionAudit.performed_at,
        AdminActionAudit.success, AdminActionAudit.ip_address
    ]
    
    column_details_list = [
        AdminActionAudit.id, AdminActionAudit.admin_user_id, AdminActionAudit.action_type,
        AdminActionAudit.resource_type, AdminActionAudit.resource_id,
        AdminActionAudit.action_details, AdminActionAudit.before_state,
        AdminActionAudit.after_state, AdminActionAudit.ip_address,
        AdminActionAudit.user_agent, AdminActionAudit.performed_at,
        AdminActionAudit.success, AdminActionAudit.error_message,
        AdminActionAudit.compliance_flags
    ]
    
    column_searchable_list = [AdminActionAudit.action_type, AdminActionAudit.resource_type]
    column_sortable_list = [AdminActionAudit.performed_at]

# ============================================================================
# INTEGRATION MONITORING VIEWS
# ============================================================================

class ExternalAPIHealthView(ModelView, model=ExternalAPIHealth):
    name = "External API Health"
    identity = "external_api_health"
    category = "Integration Monitoring"
    
    column_list = [
        ExternalAPIHealth.api_name, ExternalAPIHealth.status,
        ExternalAPIHealth.response_time_ms, ExternalAPIHealth.success_rate_24h,
        ExternalAPIHealth.uptime_percent_24h, ExternalAPIHealth.checked_at
    ]
    
    column_details_list = [
        ExternalAPIHealth.id, ExternalAPIHealth.api_name, ExternalAPIHealth.api_url,
        ExternalAPIHealth.tenant_id, ExternalAPIHealth.status,
        ExternalAPIHealth.response_time_ms, ExternalAPIHealth.status_code,
        ExternalAPIHealth.error_message, ExternalAPIHealth.success_rate_24h,
        ExternalAPIHealth.average_response_time_24h, ExternalAPIHealth.uptime_percent_24h,
        ExternalAPIHealth.last_success, ExternalAPIHealth.last_failure,
        ExternalAPIHealth.consecutive_failures, ExternalAPIHealth.checked_at,
        ExternalAPIHealth.api_key_valid, ExternalAPIHealth.rate_limit_remaining,
        ExternalAPIHealth.quota_usage_percent
    ]
    
    column_searchable_list = [ExternalAPIHealth.api_name]
    column_sortable_list = [
        ExternalAPIHealth.checked_at, ExternalAPIHealth.success_rate_24h,
        ExternalAPIHealth.response_time_ms
    ]
    
    column_formatters = {
        ExternalAPIHealth.success_rate_24h: lambda m, a: f"{getattr(m, a, 0):.1f}%" if getattr(m, a) is not None else "N/A",
        ExternalAPIHealth.uptime_percent_24h: lambda m, a: f"{getattr(m, a, 0):.2f}%" if getattr(m, a) is not None else "N/A",
        ExternalAPIHealth.response_time_ms: lambda m, a: f"{getattr(m, a, 0):,}ms" if getattr(m, a) is not None else "N/A"
    }

class WebhookDeliveryStatusView(ModelView, model=WebhookDeliveryStatus):
    name = "Webhook Delivery"
    identity = "webhook_delivery_status"
    category = "Integration Monitoring"
    
    column_list = [
        WebhookDeliveryStatus.webhook_id, WebhookDeliveryStatus.destination_url,
        WebhookDeliveryStatus.event_type, WebhookDeliveryStatus.status,
        WebhookDeliveryStatus.delivery_attempts, WebhookDeliveryStatus.created_at
    ]
    
    column_details_list = [
        WebhookDeliveryStatus.id, WebhookDeliveryStatus.webhook_id,
        WebhookDeliveryStatus.tenant_id, WebhookDeliveryStatus.destination_url,
        WebhookDeliveryStatus.event_type, WebhookDeliveryStatus.payload_size_bytes,
        WebhookDeliveryStatus.delivery_attempts, WebhookDeliveryStatus.max_attempts,
        WebhookDeliveryStatus.status, WebhookDeliveryStatus.last_attempt_at,
        WebhookDeliveryStatus.next_retry_at, WebhookDeliveryStatus.response_code,
        WebhookDeliveryStatus.response_time_ms, WebhookDeliveryStatus.error_message,
        WebhookDeliveryStatus.created_at, WebhookDeliveryStatus.delivered_at,
        WebhookDeliveryStatus.payload_hash
    ]
    
    column_searchable_list = [WebhookDeliveryStatus.destination_url, WebhookDeliveryStatus.event_type]
    column_sortable_list = [WebhookDeliveryStatus.created_at, WebhookDeliveryStatus.delivery_attempts]

class DataSyncStatusView(ModelView, model=DataSyncStatus):
    name = "Data Sync Status"
    identity = "data_sync_status"
    category = "Integration Monitoring"
    
    column_list = [
        DataSyncStatus.sync_job_id, DataSyncStatus.source_service,
        DataSyncStatus.destination_service, DataSyncStatus.data_type,
        DataSyncStatus.status, DataSyncStatus.records_processed,
        DataSyncStatus.started_at
    ]
    
    column_details_list = [
        DataSyncStatus.id, DataSyncStatus.sync_job_id, DataSyncStatus.source_service,
        DataSyncStatus.destination_service, DataSyncStatus.tenant_id,
        DataSyncStatus.data_type, DataSyncStatus.sync_type, DataSyncStatus.status,
        DataSyncStatus.started_at, DataSyncStatus.completed_at,
        DataSyncStatus.records_processed, DataSyncStatus.records_success,
        DataSyncStatus.records_failed, DataSyncStatus.last_processed_id,
        DataSyncStatus.error_details, DataSyncStatus.performance_metrics,
        DataSyncStatus.next_sync_scheduled
    ]
    
    column_searchable_list = [DataSyncStatus.sync_job_id, DataSyncStatus.source_service, DataSyncStatus.destination_service]
    column_sortable_list = [DataSyncStatus.started_at, DataSyncStatus.records_processed]
    
    column_formatters = {
        DataSyncStatus.records_processed: lambda m, a: f"{getattr(m, a, 0):,}" if getattr(m, a) is not None else "0"
    }

class IntegrationConnectivityView(ModelView, model=IntegrationConnectivity):
    name = "Integration Connectivity"
    identity = "integration_connectivity"
    category = "Integration Monitoring"
    
    column_list = [
        IntegrationConnectivity.service_name, IntegrationConnectivity.service_type,
        IntegrationConnectivity.connection_status, IntegrationConnectivity.error_rate_percent,
        IntegrationConnectivity.average_latency_ms, IntegrationConnectivity.health_checked_at
    ]
    
    column_details_list = [
        IntegrationConnectivity.id, IntegrationConnectivity.service_name,
        IntegrationConnectivity.service_type, IntegrationConnectivity.tenant_id,
        IntegrationConnectivity.connection_status, IntegrationConnectivity.last_successful_call,
        IntegrationConnectivity.last_failed_call, IntegrationConnectivity.total_calls_24h,
        IntegrationConnectivity.successful_calls_24h, IntegrationConnectivity.failed_calls_24h,
        IntegrationConnectivity.average_latency_ms, IntegrationConnectivity.error_rate_percent,
        IntegrationConnectivity.quota_used, IntegrationConnectivity.quota_limit,
        IntegrationConnectivity.quota_reset_at, IntegrationConnectivity.configuration_valid,
        IntegrationConnectivity.last_configuration_check, IntegrationConnectivity.health_checked_at
    ]
    
    column_searchable_list = [IntegrationConnectivity.service_name, IntegrationConnectivity.service_type]
    column_sortable_list = [
        IntegrationConnectivity.health_checked_at, IntegrationConnectivity.error_rate_percent,
        IntegrationConnectivity.average_latency_ms
    ]
    
    column_formatters = {
        IntegrationConnectivity.error_rate_percent: lambda m, a: f"{getattr(m, a, 0):.2f}%" if getattr(m, a) is not None else "N/A",
        IntegrationConnectivity.average_latency_ms: lambda m, a: f"{getattr(m, a, 0):.0f}ms" if getattr(m, a) is not None else "N/A"
    }

# ============================================================================
# SYSTEM ALERTS AND NOTIFICATIONS
# ============================================================================

class SystemAlertView(ModelView, model=SystemAlert):
    name = "System Alerts"
    identity = "system_alerts"
    category = "Monitoring & Alerts"
    
    column_list = [
        SystemAlert.alert_type, SystemAlert.severity, SystemAlert.title,
        SystemAlert.created_at, SystemAlert.is_active,
        SystemAlert.acknowledged_at, SystemAlert.resolved_at
    ]
    
    column_details_list = [
        SystemAlert.id, SystemAlert.alert_type, SystemAlert.severity,
        SystemAlert.title, SystemAlert.description, SystemAlert.source_service,
        SystemAlert.affected_tenants, SystemAlert.metric_name,
        SystemAlert.threshold_value, SystemAlert.current_value,
        SystemAlert.alert_data, SystemAlert.created_at,
        SystemAlert.acknowledged_at, SystemAlert.acknowledged_by,
        SystemAlert.resolved_at, SystemAlert.resolved_by,
        SystemAlert.resolution_notes, SystemAlert.is_active,
        SystemAlert.notification_sent, SystemAlert.escalation_level,
        SystemAlert.parent_alert_id
    ]
    
    column_searchable_list = [SystemAlert.alert_type, SystemAlert.title, SystemAlert.source_service]
    column_sortable_list = [
        SystemAlert.created_at, SystemAlert.severity, SystemAlert.escalation_level
    ]

# ============================================================================
# CUSTOM DASHBOARD VIEWS
# ============================================================================

class InfrastructureDashboardView(BaseView):
    name = "Infrastructure Dashboard"
    identity = "infrastructure_dashboard"
    category = "Dashboards"
    
    async def index(self, request: Request) -> HTMLResponse:
        """Custom infrastructure dashboard with real-time metrics"""
        return HTMLResponse("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Infrastructure Dashboard - BizOSaaS</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
        </head>
        <body class="bg-gray-50 dark:bg-gray-900" x-data="dashboard()">
            <div class="min-h-screen">
                <!-- Header -->
                <div class="bg-white dark:bg-gray-800 shadow">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div class="flex justify-between h-16">
                            <div class="flex items-center">
                                <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
                                    Infrastructure Dashboard
                                </h1>
                            </div>
                            <div class="flex items-center space-x-4">
                                <div class="text-sm text-gray-600 dark:text-gray-300">
                                    Last Updated: <span x-text="lastUpdated"></span>
                                </div>
                                <button @click="refreshData()" 
                                        class="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700">
                                    Refresh
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Main Dashboard -->
                <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                    <!-- System Health Overview -->
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                        <!-- Database Health -->
                        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-4">
                            <div class="flex items-center justify-between">
                                <div class="text-sm font-medium text-gray-500 dark:text-gray-400">Database</div>
                                <div class="text-xs px-2 py-1 rounded" 
                                     :class="health.database === 'healthy' ? 'text-green-600 bg-green-100' : 'text-red-600 bg-red-100'"
                                     x-text="health.database"></div>
                            </div>
                            <div class="mt-1 text-lg font-semibold text-gray-900 dark:text-white">
                                PostgreSQL
                            </div>
                            <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                <span x-text="metrics.database.active_connections"></span> active connections
                            </div>
                        </div>

                        <!-- Redis Health -->
                        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-4">
                            <div class="flex items-center justify-between">
                                <div class="text-sm font-medium text-gray-500 dark:text-gray-400">Cache</div>
                                <div class="text-xs px-2 py-1 rounded"
                                     :class="health.redis === 'healthy' ? 'text-green-600 bg-green-100' : 'text-red-600 bg-red-100'"
                                     x-text="health.redis"></div>
                            </div>
                            <div class="mt-1 text-lg font-semibold text-gray-900 dark:text-white">
                                Redis
                            </div>
                            <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                <span x-text="metrics.redis.hit_rate"></span>% hit rate
                            </div>
                        </div>

                        <!-- AI Agents -->
                        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-4">
                            <div class="flex items-center justify-between">
                                <div class="text-sm font-medium text-gray-500 dark:text-gray-400">AI Agents</div>
                                <div class="text-xs px-2 py-1 rounded"
                                     :class="health.ai_agents === 'active' ? 'text-green-600 bg-green-100' : 'text-yellow-600 bg-yellow-100'"
                                     x-text="health.ai_agents"></div>
                            </div>
                            <div class="mt-1 text-lg font-semibold text-gray-900 dark:text-white">
                                <span x-text="metrics.ai_agents.count"></span> Agents
                            </div>
                            <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                <span x-text="metrics.ai_agents.avg_response_time"></span>ms avg response
                            </div>
                        </div>

                        <!-- System Load -->
                        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-4">
                            <div class="flex items-center justify-between">
                                <div class="text-sm font-medium text-gray-500 dark:text-gray-400">System Load</div>
                                <div class="text-xs px-2 py-1 rounded"
                                     :class="metrics.system.cpu_usage < 80 ? 'text-green-600 bg-green-100' : 'text-red-600 bg-red-100'">
                                    <span x-text="metrics.system.cpu_usage"></span>%
                                </div>
                            </div>
                            <div class="mt-1 text-lg font-semibold text-gray-900 dark:text-white">
                                CPU Usage
                            </div>
                            <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                <span x-text="metrics.system.memory_usage"></span>% memory
                            </div>
                        </div>
                    </div>

                    <!-- Charts Section -->
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                        <!-- Performance Chart -->
                        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
                            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
                                Performance Metrics
                            </h3>
                            <canvas id="performanceChart" width="400" height="200"></canvas>
                        </div>

                        <!-- Error Rate Chart -->
                        <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
                            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
                                Error Rates
                            </h3>
                            <canvas id="errorChart" width="400" height="200"></canvas>
                        </div>
                    </div>

                    <!-- Recent Alerts -->
                    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
                        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
                            Recent Alerts
                        </h3>
                        <div class="overflow-x-auto">
                            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                                <thead class="bg-gray-50 dark:bg-gray-700">
                                    <tr>
                                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                            Severity
                                        </th>
                                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                            Alert
                                        </th>
                                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                            Time
                                        </th>
                                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                                            Status
                                        </th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                                    <template x-for="alert in alerts" :key="alert.id">
                                        <tr>
                                            <td class="px-6 py-4 whitespace-nowrap">
                                                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                                                      :class="getSeverityClass(alert.severity)"
                                                      x-text="alert.severity"></span>
                                            </td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
                                                x-text="alert.title"></td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400"
                                                x-text="formatTime(alert.created_at)"></td>
                                            <td class="px-6 py-4 whitespace-nowrap">
                                                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                                                      :class="alert.is_active ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'"
                                                      x-text="alert.is_active ? 'Active' : 'Resolved'"></span>
                                            </td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                function dashboard() {
                    return {
                        lastUpdated: new Date().toLocaleTimeString(),
                        health: {
                            database: 'healthy',
                            redis: 'healthy',
                            ai_agents: 'active',
                            system: 'normal'
                        },
                        metrics: {
                            database: {
                                active_connections: 12
                            },
                            redis: {
                                hit_rate: 96.5
                            },
                            ai_agents: {
                                count: 28,
                                avg_response_time: 245
                            },
                            system: {
                                cpu_usage: 45,
                                memory_usage: 62
                            }
                        },
                        alerts: [
                            {
                                id: 1,
                                severity: 'warning',
                                title: 'High response time detected',
                                created_at: new Date(Date.now() - 300000),
                                is_active: true
                            },
                            {
                                id: 2,
                                severity: 'info',
                                title: 'Scheduled maintenance completed',
                                created_at: new Date(Date.now() - 3600000),
                                is_active: false
                            }
                        ],
                        
                        async refreshData() {
                            this.lastUpdated = new Date().toLocaleTimeString();
                            // In real implementation, fetch from API
                        },
                        
                        getSeverityClass(severity) {
                            const classes = {
                                critical: 'bg-red-100 text-red-800',
                                error: 'bg-red-100 text-red-800',
                                warning: 'bg-yellow-100 text-yellow-800',
                                info: 'bg-blue-100 text-blue-800'
                            };
                            return classes[severity] || 'bg-gray-100 text-gray-800';
                        },
                        
                        formatTime(date) {
                            return new Date(date).toLocaleTimeString();
                        }
                    }
                }
                
                // Initialize charts
                document.addEventListener('DOMContentLoaded', function() {
                    // Performance Chart
                    const perfCtx = document.getElementById('performanceChart').getContext('2d');
                    new Chart(perfCtx, {
                        type: 'line',
                        data: {
                            labels: ['12:00', '12:15', '12:30', '12:45', '13:00', '13:15'],
                            datasets: [{
                                label: 'Response Time (ms)',
                                data: [245, 198, 267, 189, 234, 267],
                                borderColor: 'rgb(59, 130, 246)',
                                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                                tension: 0.1
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                    
                    // Error Chart
                    const errorCtx = document.getElementById('errorChart').getContext('2d');
                    new Chart(errorCtx, {
                        type: 'bar',
                        data: {
                            labels: ['Database', 'API', 'AI Agents', 'Cache'],
                            datasets: [{
                                label: 'Error Rate %',
                                data: [0.1, 0.5, 0.2, 0.0],
                                backgroundColor: [
                                    'rgba(239, 68, 68, 0.8)',
                                    'rgba(245, 158, 11, 0.8)',
                                    'rgba(34, 197, 94, 0.8)',
                                    'rgba(59, 130, 246, 0.8)'
                                ]
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    max: 1
                                }
                            }
                        }
                    });
                });
            </script>
        </body>
        </html>
        """)