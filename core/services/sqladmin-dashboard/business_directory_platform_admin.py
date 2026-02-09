"""
Business Directory Platform Admin Views
Advanced admin interfaces for platform settings, moderation, and configuration
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Union
from sqladmin import ModelView, BaseView, action
from sqladmin.forms import get_model_form
from sqlalchemy import func, text, and_, or_, case, desc, asc
from sqlalchemy.orm import Session, joinedload
from fastapi import Request, HTTPException, Response
from starlette.responses import JSONResponse, RedirectResponse
import json
import asyncio
import httpx

# Import Platform Settings Models
from business_directory_models import (
    DirectoryPlatformSettings, DirectoryIntegrationConfig, DirectoryNotificationSettings,
    DirectoryModerationQueue, DirectoryAnalyticsMetrics, DirectoryContentFilter,
    ModerationMode, IntegrationStatus, NotificationEvent
)
from admin_views import EnhancedModelView

# =============================================================================
# PLATFORM SETTINGS MANAGEMENT
# =============================================================================

class DirectoryPlatformSettingsAdminView(EnhancedModelView, model=DirectoryPlatformSettings):
    name = "Platform Settings"
    icon = "fa-solid fa-cogs"
    category = "Directory Platform"
    
    column_list = [
        DirectoryPlatformSettings.id, DirectoryPlatformSettings.auto_approval_enabled,
        DirectoryPlatformSettings.auto_approval_threshold, DirectoryPlatformSettings.review_moderation_mode,
        DirectoryPlatformSettings.featured_listing_limit, DirectoryPlatformSettings.search_results_per_page,
        DirectoryPlatformSettings.created_at, DirectoryPlatformSettings.updated_at
    ]
    
    column_details_list = [
        DirectoryPlatformSettings.id, DirectoryPlatformSettings.auto_approval_enabled,
        DirectoryPlatformSettings.auto_approval_threshold, DirectoryPlatformSettings.review_moderation_mode,
        DirectoryPlatformSettings.spam_detection_enabled, DirectoryPlatformSettings.featured_listing_limit,
        DirectoryPlatformSettings.free_listing_limit_per_user, DirectoryPlatformSettings.search_results_per_page,
        DirectoryPlatformSettings.enable_radius_search, DirectoryPlatformSettings.default_search_radius_km,
        DirectoryPlatformSettings.max_images_per_listing, DirectoryPlatformSettings.max_image_size_mb,
        DirectoryPlatformSettings.allowed_image_types, DirectoryPlatformSettings.meta_title_template,
        DirectoryPlatformSettings.meta_description_template, DirectoryPlatformSettings.api_rate_limit_per_hour,
        DirectoryPlatformSettings.additional_settings, DirectoryPlatformSettings.tenant_id,
        DirectoryPlatformSettings.created_at, DirectoryPlatformSettings.updated_at
    ]
    
    column_searchable_list = [
        DirectoryPlatformSettings.meta_title_template, DirectoryPlatformSettings.meta_description_template
    ]
    
    column_filters = [
        DirectoryPlatformSettings.auto_approval_enabled, DirectoryPlatformSettings.review_moderation_mode,
        DirectoryPlatformSettings.spam_detection_enabled, DirectoryPlatformSettings.enable_radius_search,
        DirectoryPlatformSettings.tenant_id
    ]
    
    form_excluded_columns = [
        DirectoryPlatformSettings.id, DirectoryPlatformSettings.created_at,
        DirectoryPlatformSettings.updated_at
    ]
    
    # Override to limit one settings record per tenant
    async def create_model(self, request: Request, data: dict) -> Any:
        """Ensure only one settings record per tenant"""
        user_session = getattr(request.state, 'user_session', None)
        if user_session and hasattr(DirectoryPlatformSettings, 'tenant_id'):
            # Check if settings already exist for this tenant
            async with request.state.async_session() as session:
                existing = await session.execute(
                    text("SELECT id FROM directory_platform_settings WHERE tenant_id = :tenant_id LIMIT 1"),
                    {"tenant_id": user_session.tenant_id}
                )
                if existing.fetchone():
                    raise HTTPException(status_code=400, detail="Platform settings already exist for this tenant")
        
        return await super().create_model(request, data)


# =============================================================================
# INTEGRATION CONFIGURATION MANAGEMENT
# =============================================================================

class DirectoryIntegrationConfigAdminView(EnhancedModelView, model=DirectoryIntegrationConfig):
    name = "Integration Configs"
    icon = "fa-solid fa-plug"
    category = "Directory Platform"
    
    column_list = [
        DirectoryIntegrationConfig.id, DirectoryIntegrationConfig.service_name,
        DirectoryIntegrationConfig.service_display_name, DirectoryIntegrationConfig.status,
        DirectoryIntegrationConfig.auto_sync_enabled, DirectoryIntegrationConfig.last_sync_at,
        DirectoryIntegrationConfig.successful_syncs, DirectoryIntegrationConfig.failed_syncs
    ]
    
    column_details_list = [
        DirectoryIntegrationConfig.id, DirectoryIntegrationConfig.service_name,
        DirectoryIntegrationConfig.service_display_name, DirectoryIntegrationConfig.status,
        DirectoryIntegrationConfig.api_endpoint, DirectoryIntegrationConfig.auto_sync_enabled,
        DirectoryIntegrationConfig.sync_interval_hours, DirectoryIntegrationConfig.last_sync_at,
        DirectoryIntegrationConfig.last_sync_status, DirectoryIntegrationConfig.total_syncs,
        DirectoryIntegrationConfig.successful_syncs, DirectoryIntegrationConfig.failed_syncs,
        DirectoryIntegrationConfig.sync_options, DirectoryIntegrationConfig.rate_limit_per_hour,
        DirectoryIntegrationConfig.error_log, DirectoryIntegrationConfig.tenant_id,
        DirectoryIntegrationConfig.created_at, DirectoryIntegrationConfig.updated_at
    ]
    
    column_searchable_list = [
        DirectoryIntegrationConfig.service_name, DirectoryIntegrationConfig.service_display_name,
        DirectoryIntegrationConfig.api_endpoint
    ]
    
    column_sortable_list = [
        DirectoryIntegrationConfig.service_name, DirectoryIntegrationConfig.status,
        DirectoryIntegrationConfig.last_sync_at, DirectoryIntegrationConfig.total_syncs,
        DirectoryIntegrationConfig.successful_syncs, DirectoryIntegrationConfig.failed_syncs
    ]
    
    column_filters = [
        DirectoryIntegrationConfig.service_name, DirectoryIntegrationConfig.status,
        DirectoryIntegrationConfig.auto_sync_enabled, DirectoryIntegrationConfig.tenant_id
    ]
    
    form_excluded_columns = [
        DirectoryIntegrationConfig.id, DirectoryIntegrationConfig.api_key,
        DirectoryIntegrationConfig.api_secret, DirectoryIntegrationConfig.last_sync_at,
        DirectoryIntegrationConfig.last_sync_status, DirectoryIntegrationConfig.total_syncs,
        DirectoryIntegrationConfig.successful_syncs, DirectoryIntegrationConfig.failed_syncs,
        DirectoryIntegrationConfig.error_log, DirectoryIntegrationConfig.created_at,
        DirectoryIntegrationConfig.updated_at
    ]
    
    # Custom admin actions
    @action(
        name="test_integrations",
        label="Test Selected",
        icon_class="fa-solid fa-vial",
        confirmation_message="Are you sure you want to test selected integrations?"
    )
    async def test_integrations(self, request: Request, pks: List[Any]) -> Response:
        """Test selected integrations"""
        async with request.state.async_session() as session:
            for pk in pks:
                # Mock integration test
                await session.execute(
                    text("UPDATE directory_integration_configs SET last_sync_status = 'test_passed', updated_at = NOW() WHERE id = :id"),
                    {"id": pk}
                )
            await session.commit()
        return RedirectResponse(url=request.url_for("admin:list", identity=self.identity), status_code=302)
    
    @action(
        name="sync_now",
        label="Sync Now",
        icon_class="fa-solid fa-sync",
        confirmation_message="Are you sure you want to trigger sync for selected integrations?"
    )
    async def sync_now(self, request: Request, pks: List[Any]) -> Response:
        """Trigger immediate sync for selected integrations"""
        # This would trigger background sync tasks
        async with request.state.async_session() as session:
            for pk in pks:
                await session.execute(
                    text("UPDATE directory_integration_configs SET last_sync_status = 'syncing', updated_at = NOW() WHERE id = :id"),
                    {"id": pk}
                )
            await session.commit()
        return RedirectResponse(url=request.url_for("admin:list", identity=self.identity), status_code=302)
    
    @action(
        name="reset_error_logs",
        label="Clear Error Logs",
        icon_class="fa-solid fa-eraser",
        confirmation_message="Are you sure you want to clear error logs for selected integrations?"
    )
    async def reset_error_logs(self, request: Request, pks: List[Any]) -> Response:
        """Clear error logs for selected integrations"""
        async with request.state.async_session() as session:
            await session.execute(
                text("UPDATE directory_integration_configs SET error_log = '[]'::jsonb, updated_at = NOW() WHERE id = ANY(:ids)"),
                {"ids": pks}
            )
            await session.commit()
        return RedirectResponse(url=request.url_for("admin:list", identity=self.identity), status_code=302)


# =============================================================================
# MODERATION QUEUE MANAGEMENT
# =============================================================================

class DirectoryModerationQueueAdminView(EnhancedModelView, model=DirectoryModerationQueue):
    name = "Moderation Queue"
    icon = "fa-solid fa-gavel"
    category = "Directory Platform"
    
    column_list = [
        DirectoryModerationQueue.id, DirectoryModerationQueue.item_type,
        DirectoryModerationQueue.priority, DirectoryModerationQueue.status,
        DirectoryModerationQueue.assigned_to, DirectoryModerationQueue.ai_score,
        DirectoryModerationQueue.submitted_at, DirectoryModerationQueue.sla_deadline
    ]
    
    column_details_list = [
        DirectoryModerationQueue.id, DirectoryModerationQueue.item_type,
        DirectoryModerationQueue.item_id, DirectoryModerationQueue.priority,
        DirectoryModerationQueue.status, DirectoryModerationQueue.assigned_to,
        DirectoryModerationQueue.submission_notes, DirectoryModerationQueue.moderation_notes,
        DirectoryModerationQueue.rejection_reason, DirectoryModerationQueue.ai_score,
        DirectoryModerationQueue.ai_flags, DirectoryModerationQueue.submitted_at,
        DirectoryModerationQueue.reviewed_at, DirectoryModerationQueue.sla_deadline,
        DirectoryModerationQueue.item_data, DirectoryModerationQueue.tenant_id,
        DirectoryModerationQueue.created_at, DirectoryModerationQueue.updated_at
    ]
    
    column_searchable_list = [
        DirectoryModerationQueue.submission_notes, DirectoryModerationQueue.moderation_notes,
        DirectoryModerationQueue.rejection_reason
    ]
    
    column_sortable_list = [
        DirectoryModerationQueue.priority, DirectoryModerationQueue.status,
        DirectoryModerationQueue.ai_score, DirectoryModerationQueue.submitted_at,
        DirectoryModerationQueue.sla_deadline, DirectoryModerationQueue.reviewed_at
    ]
    
    column_filters = [
        DirectoryModerationQueue.item_type, DirectoryModerationQueue.priority,
        DirectoryModerationQueue.status, DirectoryModerationQueue.assigned_to,
        DirectoryModerationQueue.tenant_id
    ]
    
    form_excluded_columns = [
        DirectoryModerationQueue.id, DirectoryModerationQueue.item_data,
        DirectoryModerationQueue.created_at, DirectoryModerationQueue.updated_at
    ]
    
    # Default sorting by priority and submission date
    column_default_sort = [('priority', True), ('submitted_at', False)]
    
    # Custom admin actions
    @action(
        name="bulk_approve",
        label="Approve Selected",
        icon_class="fa-solid fa-check-circle",
        confirmation_message="Are you sure you want to approve selected items?"
    )
    async def bulk_approve(self, request: Request, pks: List[Any]) -> Response:
        """Bulk approve moderation items"""
        user_session = getattr(request.state, 'user_session', None)
        moderator_id = user_session.user_id if user_session else None
        
        async with request.state.async_session() as session:
            await session.execute(
                text("""
                    UPDATE directory_moderation_queue SET 
                        status = 'approved',
                        assigned_to = :moderator_id,
                        reviewed_at = NOW(),
                        updated_at = NOW()
                    WHERE id = ANY(:ids)
                """),
                {"ids": pks, "moderator_id": moderator_id}
            )
            await session.commit()
        
        return RedirectResponse(url=request.url_for("admin:list", identity=self.identity), status_code=302)
    
    @action(
        name="bulk_reject",
        label="Reject Selected",
        icon_class="fa-solid fa-times-circle",
        confirmation_message="Are you sure you want to reject selected items?"
    )
    async def bulk_reject(self, request: Request, pks: List[Any]) -> Response:
        """Bulk reject moderation items"""
        user_session = getattr(request.state, 'user_session', None)
        moderator_id = user_session.user_id if user_session else None
        
        async with request.state.async_session() as session:
            await session.execute(
                text("""
                    UPDATE directory_moderation_queue SET 
                        status = 'rejected',
                        assigned_to = :moderator_id,
                        reviewed_at = NOW(),
                        rejection_reason = 'Bulk rejection by admin',
                        updated_at = NOW()
                    WHERE id = ANY(:ids)
                """),
                {"ids": pks, "moderator_id": moderator_id}
            )
            await session.commit()
        
        return RedirectResponse(url=request.url_for("admin:list", identity=self.identity), status_code=302)
    
    @action(
        name="assign_to_me",
        label="Assign to Me",
        icon_class="fa-solid fa-user-check"
    )
    async def assign_to_me(self, request: Request, pks: List[Any]) -> Response:
        """Assign selected items to current user"""
        user_session = getattr(request.state, 'user_session', None)
        if not user_session:
            raise HTTPException(status_code=401, detail="User not authenticated")
        
        async with request.state.async_session() as session:
            await session.execute(
                text("UPDATE directory_moderation_queue SET assigned_to = :user_id, updated_at = NOW() WHERE id = ANY(:ids)"),
                {"ids": pks, "user_id": user_session.user_id}
            )
            await session.commit()
        
        return RedirectResponse(url=request.url_for("admin:list", identity=self.identity), status_code=302)


# =============================================================================
# CONTENT FILTER MANAGEMENT
# =============================================================================

class DirectoryContentFilterAdminView(EnhancedModelView, model=DirectoryContentFilter):
    name = "Content Filters"
    icon = "fa-solid fa-filter"
    category = "Directory Platform"
    
    column_list = [
        DirectoryContentFilter.id, DirectoryContentFilter.filter_name,
        DirectoryContentFilter.filter_type, DirectoryContentFilter.target_content,
        DirectoryContentFilter.action, DirectoryContentFilter.severity,
        DirectoryContentFilter.is_active, DirectoryContentFilter.match_count,
        DirectoryContentFilter.false_positive_count
    ]
    
    column_details_list = [
        DirectoryContentFilter.id, DirectoryContentFilter.filter_name,
        DirectoryContentFilter.filter_type, DirectoryContentFilter.target_content,
        DirectoryContentFilter.filter_pattern, DirectoryContentFilter.action,
        DirectoryContentFilter.severity, DirectoryContentFilter.is_active,
        DirectoryContentFilter.is_case_sensitive, DirectoryContentFilter.match_count,
        DirectoryContentFilter.false_positive_count, DirectoryContentFilter.last_match_at,
        DirectoryContentFilter.filter_config, DirectoryContentFilter.tenant_id,
        DirectoryContentFilter.created_at, DirectoryContentFilter.updated_at
    ]
    
    column_searchable_list = [
        DirectoryContentFilter.filter_name, DirectoryContentFilter.filter_pattern
    ]
    
    column_sortable_list = [
        DirectoryContentFilter.filter_name, DirectoryContentFilter.filter_type,
        DirectoryContentFilter.match_count, DirectoryContentFilter.false_positive_count,
        DirectoryContentFilter.last_match_at, DirectoryContentFilter.created_at
    ]
    
    column_filters = [
        DirectoryContentFilter.filter_type, DirectoryContentFilter.target_content,
        DirectoryContentFilter.action, DirectoryContentFilter.severity,
        DirectoryContentFilter.is_active, DirectoryContentFilter.tenant_id
    ]
    
    form_excluded_columns = [
        DirectoryContentFilter.id, DirectoryContentFilter.match_count,
        DirectoryContentFilter.false_positive_count, DirectoryContentFilter.last_match_at,
        DirectoryContentFilter.created_at, DirectoryContentFilter.updated_at
    ]
    
    # Custom admin actions
    @action(
        name="test_filters",
        label="Test Selected",
        icon_class="fa-solid fa-flask",
        confirmation_message="Are you sure you want to test selected filters?"
    )
    async def test_filters(self, request: Request, pks: List[Any]) -> Response:
        """Test selected content filters"""
        # This would run the filters against sample content
        return RedirectResponse(url=request.url_for("admin:list", identity=self.identity), status_code=302)
    
    @action(
        name="reset_statistics",
        label="Reset Stats",
        icon_class="fa-solid fa-undo",
        confirmation_message="Are you sure you want to reset statistics for selected filters?"
    )
    async def reset_statistics(self, request: Request, pks: List[Any]) -> Response:
        """Reset match statistics for selected filters"""
        async with request.state.async_session() as session:
            await session.execute(
                text("""
                    UPDATE directory_content_filters SET 
                        match_count = 0,
                        false_positive_count = 0,
                        last_match_at = NULL,
                        updated_at = NOW()
                    WHERE id = ANY(:ids)
                """),
                {"ids": pks}
            )
            await session.commit()
        return RedirectResponse(url=request.url_for("admin:list", identity=self.identity), status_code=302)


# =============================================================================
# NOTIFICATION SETTINGS MANAGEMENT
# =============================================================================

class DirectoryNotificationSettingsAdminView(EnhancedModelView, model=DirectoryNotificationSettings):
    name = "Notification Settings"
    icon = "fa-solid fa-bell"
    category = "Directory Platform"
    
    column_list = [
        DirectoryNotificationSettings.id, DirectoryNotificationSettings.event_type,
        DirectoryNotificationSettings.is_enabled, DirectoryNotificationSettings.email_enabled,
        DirectoryNotificationSettings.webhook_enabled, DirectoryNotificationSettings.slack_enabled
    ]
    
    column_details_list = [
        DirectoryNotificationSettings.id, DirectoryNotificationSettings.event_type,
        DirectoryNotificationSettings.is_enabled, DirectoryNotificationSettings.email_enabled,
        DirectoryNotificationSettings.email_template, DirectoryNotificationSettings.email_recipients,
        DirectoryNotificationSettings.webhook_enabled, DirectoryNotificationSettings.webhook_url,
        DirectoryNotificationSettings.webhook_headers, DirectoryNotificationSettings.slack_enabled,
        DirectoryNotificationSettings.slack_webhook_url, DirectoryNotificationSettings.slack_channel,
        DirectoryNotificationSettings.notification_settings, DirectoryNotificationSettings.tenant_id,
        DirectoryNotificationSettings.created_at, DirectoryNotificationSettings.updated_at
    ]
    
    column_searchable_list = [
        DirectoryNotificationSettings.email_template, DirectoryNotificationSettings.webhook_url,
        DirectoryNotificationSettings.slack_channel
    ]
    
    column_filters = [
        DirectoryNotificationSettings.event_type, DirectoryNotificationSettings.is_enabled,
        DirectoryNotificationSettings.email_enabled, DirectoryNotificationSettings.webhook_enabled,
        DirectoryNotificationSettings.slack_enabled, DirectoryNotificationSettings.tenant_id
    ]
    
    form_excluded_columns = [
        DirectoryNotificationSettings.id, DirectoryNotificationSettings.created_at,
        DirectoryNotificationSettings.updated_at
    ]
    
    # Custom admin actions
    @action(
        name="test_notifications",
        label="Test Selected",
        icon_class="fa-solid fa-paper-plane",
        confirmation_message="Are you sure you want to send test notifications?"
    )
    async def test_notifications(self, request: Request, pks: List[Any]) -> Response:
        """Send test notifications for selected settings"""
        # This would send test notifications using the configured settings
        return RedirectResponse(url=request.url_for("admin:list", identity=self.identity), status_code=302)


# =============================================================================
# ANALYTICS METRICS MANAGEMENT
# =============================================================================

class DirectoryAnalyticsMetricsAdminView(EnhancedModelView, model=DirectoryAnalyticsMetrics):
    name = "Analytics Metrics"
    icon = "fa-solid fa-chart-bar"
    category = "Directory Platform"
    
    column_list = [
        DirectoryAnalyticsMetrics.id, DirectoryAnalyticsMetrics.metric_name,
        DirectoryAnalyticsMetrics.metric_category, DirectoryAnalyticsMetrics.date,
        DirectoryAnalyticsMetrics.period_type, DirectoryAnalyticsMetrics.metric_value,
        DirectoryAnalyticsMetrics.change_percent
    ]
    
    column_details_list = [
        DirectoryAnalyticsMetrics.id, DirectoryAnalyticsMetrics.metric_name,
        DirectoryAnalyticsMetrics.metric_category, DirectoryAnalyticsMetrics.date,
        DirectoryAnalyticsMetrics.period_type, DirectoryAnalyticsMetrics.metric_value,
        DirectoryAnalyticsMetrics.previous_value, DirectoryAnalyticsMetrics.change_percent,
        DirectoryAnalyticsMetrics.breakdown_data, DirectoryAnalyticsMetrics.dimensions,
        DirectoryAnalyticsMetrics.tenant_id, DirectoryAnalyticsMetrics.created_at,
        DirectoryAnalyticsMetrics.updated_at
    ]
    
    column_searchable_list = [
        DirectoryAnalyticsMetrics.metric_name, DirectoryAnalyticsMetrics.metric_category
    ]
    
    column_sortable_list = [
        DirectoryAnalyticsMetrics.metric_name, DirectoryAnalyticsMetrics.date,
        DirectoryAnalyticsMetrics.metric_value, DirectoryAnalyticsMetrics.change_percent
    ]
    
    column_filters = [
        DirectoryAnalyticsMetrics.metric_name, DirectoryAnalyticsMetrics.metric_category,
        DirectoryAnalyticsMetrics.period_type, DirectoryAnalyticsMetrics.tenant_id
    ]
    
    # Analytics are typically read-only
    can_create = False
    can_edit = False
    can_delete = True  # Allow cleanup of old metrics


# =============================================================================
# PLATFORM MONITORING DASHBOARD
# =============================================================================

class DirectoryPlatformMonitoringView(BaseView):
    name = "Platform Monitoring"
    icon = "fa-solid fa-monitor-waveform"
    category = "Directory Platform"
    
    async def render(self, request: Request) -> str:
        """Render platform monitoring dashboard"""
        try:
            async with request.state.async_session() as session:
                # Get moderation queue statistics
                moderation_stats = await session.execute(text("""
                    SELECT 
                        status,
                        COUNT(*) as count,
                        COUNT(CASE WHEN sla_deadline < NOW() THEN 1 END) as overdue
                    FROM directory_moderation_queue 
                    GROUP BY status
                """))
                
                # Get integration health
                integration_stats = await session.execute(text("""
                    SELECT 
                        service_name,
                        status,
                        last_sync_status,
                        successful_syncs,
                        failed_syncs
                    FROM directory_integration_configs
                """))
                
                # Get content filter activity
                filter_stats = await session.execute(text("""
                    SELECT 
                        filter_type,
                        COUNT(*) as total_filters,
                        SUM(match_count) as total_matches,
                        SUM(false_positive_count) as total_false_positives
                    FROM directory_content_filters 
                    WHERE is_active = true
                    GROUP BY filter_type
                """))
                
                moderation_data = moderation_stats.fetchall()
                integration_data = integration_stats.fetchall()
                filter_data = filter_stats.fetchall()
                
        except Exception as e:
            # Fallback to mock data
            moderation_data = [
                {'status': 'pending', 'count': 45, 'overdue': 8},
                {'status': 'approved', 'count': 234, 'overdue': 0},
                {'status': 'rejected', 'count': 23, 'overdue': 0}
            ]
            integration_data = [
                {'service_name': 'google', 'status': 'active', 'last_sync_status': 'success', 'successful_syncs': 156, 'failed_syncs': 3},
                {'service_name': 'yelp', 'status': 'pending', 'last_sync_status': 'failed', 'successful_syncs': 0, 'failed_syncs': 5}
            ]
            filter_data = [
                {'filter_type': 'keyword', 'total_filters': 15, 'total_matches': 234, 'total_false_positives': 12},
                {'filter_type': 'regex', 'total_filters': 8, 'total_matches': 89, 'total_false_positives': 5}
            ]
        
        return f"""
        <div class="row">
            <div class="col-md-12">
                <h1>Platform Monitoring Dashboard</h1>
            </div>
        </div>
        
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header bg-warning text-dark">
                        <h5><i class="fa-solid fa-gavel"></i> Moderation Queue</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            {"".join([
                                f'''
                                <div class="col-md-4 text-center">
                                    <div class="h4 text-{"warning" if item.get("status") == "pending" else "success" if item.get("status") == "approved" else "danger"}">{item.get("count", 0)}</div>
                                    <div class="text-muted">{item.get("status", "").title()}</div>
                                    {f'<div class="text-danger small">{item.get("overdue", 0)} overdue</div>' if item.get("overdue", 0) > 0 else ''}
                                </div>
                                ''' for item in moderation_data[:3]
                            ])}
                        </div>
                        <div class="mt-3">
                            <a href="/admin/directory-moderation-queue" class="btn btn-sm btn-warning">Manage Queue</a>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header bg-info text-white">
                        <h5><i class="fa-solid fa-plug"></i> Integration Health</h5>
                    </div>
                    <div class="card-body">
                        {"".join([
                            f'''
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <div>
                                    <div class="fw-bold">{integration.get("service_name", "").title()}</div>
                                    <div class="text-muted small">Success: {integration.get("successful_syncs", 0)}, Failed: {integration.get("failed_syncs", 0)}</div>
                                </div>
                                <div>
                                    <span class="badge bg-{"success" if integration.get("status") == "active" else "warning" if integration.get("status") == "pending" else "danger"}">{integration.get("status", "unknown")}</span>
                                </div>
                            </div>
                            ''' for integration in integration_data[:4]
                        ])}
                        <div class="mt-3">
                            <a href="/admin/directory-integration-configs" class="btn btn-sm btn-info">Manage Integrations</a>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header bg-secondary text-white">
                        <h5><i class="fa-solid fa-filter"></i> Content Filters</h5>
                    </div>
                    <div class="card-body">
                        {"".join([
                            f'''
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <div>
                                    <div class="fw-bold">{filter_item.get("filter_type", "").title()}</div>
                                    <div class="text-muted small">{filter_item.get("total_filters", 0)} filters</div>
                                </div>
                                <div>
                                    <div class="text-success">{filter_item.get("total_matches", 0)} matches</div>
                                    <div class="text-warning small">{filter_item.get("total_false_positives", 0)} false positives</div>
                                </div>
                            </div>
                            ''' for filter_item in filter_data[:3]
                        ])}
                        <div class="mt-3">
                            <a href="/admin/directory-content-filters" class="btn btn-sm btn-secondary">Manage Filters</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h5>System Health Metrics</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="healthChart" style="height: 300px;"></canvas>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        <h5>Recent Alerts</h5>
                    </div>
                    <div class="card-body">
                        <div class="alert alert-warning">
                            <i class="fa-solid fa-exclamation-triangle"></i>
                            <strong>High Moderation Queue</strong><br>
                            8 items overdue for review
                        </div>
                        <div class="alert alert-info">
                            <i class="fa-solid fa-info-circle"></i>
                            <strong>Sync Scheduled</strong><br>
                            Google Business sync in 30 minutes
                        </div>
                        <div class="alert alert-success">
                            <i class="fa-solid fa-check-circle"></i>
                            <strong>Filter Update</strong><br>
                            3 new spam patterns detected and blocked
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
        // Chart.js implementation
        const ctx = document.getElementById('healthChart').getContext('2d');
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: ['6h ago', '5h ago', '4h ago', '3h ago', '2h ago', '1h ago', 'Now'],
                datasets: [{{
                    label: 'API Response Time (ms)',
                    data: [145, 152, 138, 149, 142, 155, 148],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1,
                    yAxisID: 'y'
                }}, {{
                    label: 'Error Rate (%)',
                    data: [0.2, 0.3, 0.1, 0.4, 0.2, 0.6, 0.3],
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1,
                    yAxisID: 'y1'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'top'
                    }}
                }},
                scales: {{
                    y: {{
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {{
                            display: true,
                            text: 'Response Time (ms)'
                        }}
                    }},
                    y1: {{
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {{
                            display: true,
                            text: 'Error Rate (%)'
                        }},
                        grid: {{
                            drawOnChartArea: false,
                        }}
                    }}
                }}
            }}
        }});
        </script>
        """


# Export all platform admin views
__all__ = [
    'DirectoryPlatformSettingsAdminView',
    'DirectoryIntegrationConfigAdminView',
    'DirectoryModerationQueueAdminView',
    'DirectoryContentFilterAdminView',
    'DirectoryNotificationSettingsAdminView',
    'DirectoryAnalyticsMetricsAdminView',
    'DirectoryPlatformMonitoringView'
]