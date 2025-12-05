"""
Comprehensive SQLAdmin Views for BizOSaaS Platform
Advanced admin interface with full CRUD operations, filtering, and analytics
"""

from datetime import datetime
from typing import Optional, Dict, Any, List, Union
from sqladmin import ModelView, BaseView, action
from sqladmin.forms import get_model_form
from sqlalchemy import func, text, and_, or_
from sqlalchemy.orm import Session
from fastapi import Request, HTTPException
from starlette.responses import Response
import json

# Import all models
from models.core import *
from models.crm import *
from models.ecommerce import *
from models.cms import *
from models.billing import *
from models.analytics import *
from models.integrations import *
from models.security import *

# Import Business Directory Models
from business_directory_models import (
    DirectoryPlatformSettings, DirectoryIntegrationConfig, DirectoryNotificationSettings,
    DirectoryModerationQueue, DirectoryAnalyticsMetrics, DirectoryContentFilter
)

# Custom Admin View Base Class with Enhanced Features
class EnhancedModelView(ModelView):
    """Base class for all admin views with enhanced functionality"""
    
    # Enhanced display options
    column_default_sort = [('created_at', True)]  # Default sort by created_at desc
    column_searchable_list = []
    column_filters = []
    column_editable_list = []
    
    # Pagination
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    
    # Export options
    can_export = True
    export_max_rows = 10000
    export_types = ['csv', 'xlsx', 'json']
    
    # Security
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    
    # Custom templates
    list_template = 'admin/model/list.html'
    create_template = 'admin/model/create.html'
    edit_template = 'admin/model/edit.html'
    details_template = 'admin/model/details.html'
    
    # Bulk operations
    column_select_related_list = []
    
    def is_accessible(self, request: Request) -> bool:
        """Check if user has access to this view"""
        # This would integrate with the authentication system
        user_session = getattr(request.state, 'user_session', None)
        if not user_session or not user_session.is_super_admin:
            return False
        return True
    
    def get_query(self, request: Request):
        """Override to add tenant filtering if needed"""
        query = super().get_query(request)
        
        # Add tenant filtering for multi-tenant models
        if hasattr(self.model, 'tenant_id'):
            user_session = getattr(request.state, 'user_session', None)
            if user_session and not user_session.is_super_admin:
                query = query.filter(self.model.tenant_id == user_session.tenant_id)
        
        return query
    
    def create_model(self, request: Request, data: dict) -> Any:
        """Enhanced model creation with audit logging"""
        # Add tenant_id for multi-tenant models
        if hasattr(self.model, 'tenant_id'):
            user_session = getattr(request.state, 'user_session', None)
            if user_session and 'tenant_id' not in data:
                data['tenant_id'] = user_session.tenant_id
        
        # Add created_by if applicable
        if hasattr(self.model, 'created_by'):
            user_session = getattr(request.state, 'user_session', None)
            if user_session:
                data['created_by'] = user_session.user_id
        
        model = super().create_model(request, data)
        
        # Log the creation
        self._log_audit_event(request, 'create', model)
        
        return model
    
    def update_model(self, request: Request, pk: Any, data: dict) -> Any:
        """Enhanced model update with audit logging"""
        # Get old values for audit
        old_model = self.get_object_for_edit(request, pk)
        old_values = {c.name: getattr(old_model, c.name) for c in old_model.__table__.columns}
        
        # Add updated_by if applicable
        if hasattr(self.model, 'updated_by'):
            user_session = getattr(request.state, 'user_session', None)
            if user_session:
                data['updated_by'] = user_session.user_id
        
        model = super().update_model(request, pk, data)
        
        # Log the update
        self._log_audit_event(request, 'update', model, old_values=old_values, new_values=data)
        
        return model
    
    def delete_model(self, request: Request, pk: Any) -> bool:
        """Enhanced model deletion with audit logging"""
        model = self.get_object_for_details(request, pk)
        model_data = {c.name: getattr(model, c.name) for c in model.__table__.columns}
        
        result = super().delete_model(request, pk)
        
        if result:
            self._log_audit_event(request, 'delete', model_data=model_data)
        
        return result
    
    def _log_audit_event(self, request: Request, action: str, model=None, old_values=None, new_values=None, model_data=None):
        """Log audit events for admin actions"""
        try:
            user_session = getattr(request.state, 'user_session', None)
            if not user_session:
                return
            
            # This would integrate with your audit logging system
            # For now, we'll just log to the console
            audit_data = {
                'user_id': user_session.user_id,
                'action': action,
                'model': self.model.__name__,
                'timestamp': datetime.utcnow().isoformat(),
                'ip_address': request.client.host,
                'user_agent': request.headers.get('user-agent', ''),
                'old_values': old_values,
                'new_values': new_values,
                'model_data': model_data
            }
            print(f"AUDIT LOG: {json.dumps(audit_data, default=str)}")
            
        except Exception as e:
            print(f"Failed to log audit event: {e}")

# =============================================================================
# CORE PLATFORM VIEWS
# =============================================================================

class TenantAdminView(EnhancedModelView, model=TenantAdmin):
    name = "Tenants"
    icon = "fa-solid fa-building"
    category = "Core Platform"
    
    column_list = [
        TenantAdmin.id, TenantAdmin.name, TenantAdmin.slug, TenantAdmin.status,
        TenantAdmin.subscription_plan, TenantAdmin.user_limit, TenantAdmin.created_at
    ]
    
    column_details_list = [
        TenantAdmin.id, TenantAdmin.name, TenantAdmin.slug, TenantAdmin.status,
        TenantAdmin.company_name, TenantAdmin.industry, TenantAdmin.website,
        TenantAdmin.subscription_plan, TenantAdmin.subscription_status,
        TenantAdmin.trial_ends_at, TenantAdmin.allowed_platforms,
        TenantAdmin.user_limit, TenantAdmin.storage_limit_gb, TenantAdmin.api_call_limit,
        TenantAdmin.created_at, TenantAdmin.updated_at
    ]
    
    column_searchable_list = [TenantAdmin.name, TenantAdmin.slug, TenantAdmin.company_name]
    column_sortable_list = [TenantAdmin.name, TenantAdmin.created_at, TenantAdmin.status]
    column_filters = [TenantAdmin.status, TenantAdmin.subscription_plan, TenantAdmin.industry]
    
    form_excluded_columns = [TenantAdmin.id, TenantAdmin.created_at, TenantAdmin.updated_at]

class UserAdminView(EnhancedModelView, model=UserAdmin):
    name = "Users"
    icon = "fa-solid fa-users"
    category = "Core Platform"
    
    column_list = [
        UserAdmin.id, UserAdmin.email, UserAdmin.full_name, UserAdmin.role,
        UserAdmin.is_active, UserAdmin.last_login_at, UserAdmin.created_at
    ]
    
    column_details_list = [
        UserAdmin.id, UserAdmin.email, UserAdmin.first_name, UserAdmin.last_name,
        UserAdmin.role, UserAdmin.tenant_id, UserAdmin.organization_id,
        UserAdmin.is_active, UserAdmin.is_verified, UserAdmin.is_superuser,
        UserAdmin.two_factor_enabled, UserAdmin.login_count, UserAdmin.last_login_at,
        UserAdmin.timezone, UserAdmin.language, UserAdmin.created_at
    ]
    
    column_searchable_list = [UserAdmin.email, UserAdmin.first_name, UserAdmin.last_name]
    column_sortable_list = [UserAdmin.email, UserAdmin.created_at, UserAdmin.last_login_at]
    column_filters = [UserAdmin.role, UserAdmin.is_active, UserAdmin.is_verified, UserAdmin.tenant_id]
    
    form_excluded_columns = [
        UserAdmin.id, UserAdmin.hashed_password, UserAdmin.created_at, 
        UserAdmin.updated_at, UserAdmin.last_login_at, UserAdmin.login_count
    ]

class UserSessionAdminView(EnhancedModelView, model=UserSessionAdmin):
    name = "User Sessions"
    icon = "fa-solid fa-user-clock"
    category = "Core Platform"
    
    column_list = [
        UserSessionAdmin.id, UserSessionAdmin.user_id, UserSessionAdmin.platform,
        UserSessionAdmin.ip_address, UserSessionAdmin.is_active, UserSessionAdmin.created_at,
        UserSessionAdmin.expires_at
    ]
    
    column_searchable_list = [UserSessionAdmin.ip_address, UserSessionAdmin.user_agent]
    column_filters = [UserSessionAdmin.platform, UserSessionAdmin.is_active, UserSessionAdmin.device_type]
    
    can_create = False  # Sessions are created programmatically
    can_edit = False

class OrganizationAdminView(EnhancedModelView, model=OrganizationAdmin):
    name = "Organizations"
    icon = "fa-solid fa-sitemap"
    category = "Core Platform"
    
    column_list = [
        OrganizationAdmin.id, OrganizationAdmin.name, OrganizationAdmin.slug,
        OrganizationAdmin.industry, OrganizationAdmin.company_size, OrganizationAdmin.is_active
    ]
    
    column_searchable_list = [OrganizationAdmin.name, OrganizationAdmin.slug]
    column_filters = [OrganizationAdmin.industry, OrganizationAdmin.company_size, OrganizationAdmin.is_active]

# =============================================================================
# CRM VIEWS
# =============================================================================

class ContactAdminView(EnhancedModelView, model=ContactAdmin):
    name = "Contacts"
    icon = "fa-solid fa-address-book"
    category = "CRM"
    
    column_list = [
        ContactAdmin.id, ContactAdmin.full_name, ContactAdmin.email, ContactAdmin.phone,
        ContactAdmin.company, ContactAdmin.contact_type, ContactAdmin.lead_score,
        ContactAdmin.created_at
    ]
    
    column_searchable_list = [
        ContactAdmin.first_name, ContactAdmin.last_name, ContactAdmin.email,
        ContactAdmin.phone, ContactAdmin.company
    ]
    column_filters = [ContactAdmin.contact_type, ContactAdmin.source, ContactAdmin.is_active]

class LeadAdminView(EnhancedModelView, model=LeadAdmin):
    name = "Leads"
    icon = "fa-solid fa-bullseye"
    category = "CRM"
    
    column_list = [
        LeadAdmin.id, LeadAdmin.title, LeadAdmin.contact_id, LeadAdmin.status,
        LeadAdmin.estimated_value, LeadAdmin.probability, LeadAdmin.source,
        LeadAdmin.created_at
    ]
    
    column_searchable_list = [LeadAdmin.title, LeadAdmin.description]
    column_filters = [LeadAdmin.status, LeadAdmin.source, LeadAdmin.priority, LeadAdmin.assigned_to]

class DealAdminView(EnhancedModelView, model=DealAdmin):
    name = "Deals"
    icon = "fa-solid fa-handshake"
    category = "CRM"
    
    column_list = [
        DealAdmin.id, DealAdmin.name, DealAdmin.stage, DealAdmin.amount,
        DealAdmin.probability, DealAdmin.expected_close_date, DealAdmin.owner_id
    ]
    
    column_searchable_list = [DealAdmin.name, DealAdmin.description]
    column_filters = [DealAdmin.stage, DealAdmin.currency, DealAdmin.risk_level]

class ActivityAdminView(EnhancedModelView, model=ActivityAdmin):
    name = "Activities"
    icon = "fa-solid fa-tasks"
    category = "CRM"
    
    column_list = [
        ActivityAdmin.id, ActivityAdmin.type, ActivityAdmin.subject,
        ActivityAdmin.contact_id, ActivityAdmin.scheduled_at, ActivityAdmin.is_completed,
        ActivityAdmin.assigned_to
    ]
    
    column_searchable_list = [ActivityAdmin.subject, ActivityAdmin.description]
    column_filters = [ActivityAdmin.type, ActivityAdmin.is_completed, ActivityAdmin.priority]

class CampaignAdminView(EnhancedModelView, model=CampaignAdmin):
    name = "Campaigns"
    icon = "fa-solid fa-bullhorn"
    category = "CRM"
    
    column_list = [
        CampaignAdmin.id, CampaignAdmin.name, CampaignAdmin.type, CampaignAdmin.status,
        CampaignAdmin.budget, CampaignAdmin.leads_generated, CampaignAdmin.start_date
    ]
    
    column_searchable_list = [CampaignAdmin.name, CampaignAdmin.description]
    column_filters = [CampaignAdmin.type, CampaignAdmin.status]

# =============================================================================
# E-COMMERCE VIEWS
# =============================================================================

class ProductAdminView(EnhancedModelView, model=ProductAdmin):
    name = "Products"
    icon = "fa-solid fa-box"
    category = "E-commerce"
    
    column_list = [
        ProductAdmin.id, ProductAdmin.name, ProductAdmin.sku, ProductAdmin.price,
        ProductAdmin.status, ProductAdmin.inventory_quantity, ProductAdmin.category_id,
        ProductAdmin.created_at
    ]
    
    column_searchable_list = [ProductAdmin.name, ProductAdmin.sku, ProductAdmin.description]
    column_filters = [ProductAdmin.status, ProductAdmin.category_id, ProductAdmin.is_featured]

class CategoryAdminView(EnhancedModelView, model=CategoryAdmin):
    name = "Categories"
    icon = "fa-solid fa-tags"
    category = "E-commerce"
    
    column_list = [
        CategoryAdmin.id, CategoryAdmin.name, CategoryAdmin.slug, CategoryAdmin.parent_id,
        CategoryAdmin.level, CategoryAdmin.sort_order, CategoryAdmin.is_active
    ]
    
    column_searchable_list = [CategoryAdmin.name, CategoryAdmin.description]
    column_filters = [CategoryAdmin.is_active, CategoryAdmin.is_featured, CategoryAdmin.level]

class OrderAdminView(EnhancedModelView, model=OrderAdmin):
    name = "Orders"
    icon = "fa-solid fa-shopping-cart"
    category = "E-commerce"
    
    column_list = [
        OrderAdmin.id, OrderAdmin.order_number, OrderAdmin.customer_id,
        OrderAdmin.order_status, OrderAdmin.payment_status, OrderAdmin.total_amount,
        OrderAdmin.created_at
    ]
    
    column_searchable_list = [OrderAdmin.order_number, OrderAdmin.customer_email]
    column_filters = [OrderAdmin.order_status, OrderAdmin.payment_status, OrderAdmin.shipping_status]

class CustomerAdminView(EnhancedModelView, model=CustomerAdmin):
    name = "Customers"
    icon = "fa-solid fa-user-tie"
    category = "E-commerce"
    
    column_list = [
        CustomerAdmin.id, CustomerAdmin.first_name, CustomerAdmin.last_name,
        CustomerAdmin.email, CustomerAdmin.customer_type, CustomerAdmin.total_orders,
        CustomerAdmin.total_spent
    ]
    
    column_searchable_list = [
        CustomerAdmin.first_name, CustomerAdmin.last_name, CustomerAdmin.email,
        CustomerAdmin.company_name
    ]
    column_filters = [CustomerAdmin.customer_type, CustomerAdmin.is_active]

class InventoryAdminView(EnhancedModelView, model=InventoryAdmin):
    name = "Inventory"
    icon = "fa-solid fa-warehouse"
    category = "E-commerce"
    
    column_list = [
        InventoryAdmin.id, InventoryAdmin.sku, InventoryAdmin.quantity_on_hand,
        InventoryAdmin.quantity_allocated, InventoryAdmin.quantity_available,
        InventoryAdmin.reorder_level
    ]
    
    column_searchable_list = [InventoryAdmin.sku]
    column_filters = [InventoryAdmin.warehouse_location]

# =============================================================================
# CMS VIEWS
# =============================================================================

class PageAdminView(EnhancedModelView, model=PageAdmin):
    name = "Pages"
    icon = "fa-solid fa-file-alt"
    category = "CMS"
    
    column_list = [
        PageAdmin.id, PageAdmin.title, PageAdmin.slug, PageAdmin.status,
        PageAdmin.is_visible_in_menu, PageAdmin.view_count, PageAdmin.published_at
    ]
    
    column_searchable_list = [PageAdmin.title, PageAdmin.content]
    column_filters = [PageAdmin.status, PageAdmin.is_visible_in_menu, PageAdmin.template]

class MediaAdminView(EnhancedModelView, model=MediaAdmin):
    name = "Media"
    icon = "fa-solid fa-images"
    category = "CMS"
    
    column_list = [
        MediaAdmin.id, MediaAdmin.filename, MediaAdmin.media_type,
        MediaAdmin.file_size, MediaAdmin.width, MediaAdmin.height,
        MediaAdmin.usage_count, MediaAdmin.created_at
    ]
    
    column_searchable_list = [MediaAdmin.filename, MediaAdmin.original_filename, MediaAdmin.alt_text]
    column_filters = [MediaAdmin.media_type, MediaAdmin.folder, MediaAdmin.is_public]

class FormAdminView(EnhancedModelView, model=FormAdmin):
    name = "Forms"
    icon = "fa-solid fa-wpforms"
    category = "CMS"
    
    column_list = [
        FormAdmin.id, FormAdmin.name, FormAdmin.title, FormAdmin.status,
        FormAdmin.submission_count, FormAdmin.conversion_rate, FormAdmin.created_at
    ]
    
    column_searchable_list = [FormAdmin.name, FormAdmin.title, FormAdmin.description]
    column_filters = [FormAdmin.status, FormAdmin.is_public]

class CollectionAdminView(EnhancedModelView, model=CollectionAdmin):
    name = "Collections"
    icon = "fa-solid fa-layer-group"
    category = "CMS"
    
    column_list = [
        CollectionAdmin.id, CollectionAdmin.name, CollectionAdmin.slug,
        CollectionAdmin.collection_type, CollectionAdmin.is_active, CollectionAdmin.is_featured
    ]
    
    column_searchable_list = [CollectionAdmin.name, CollectionAdmin.description]
    column_filters = [CollectionAdmin.collection_type, CollectionAdmin.is_active]

class MenuAdminView(EnhancedModelView, model=MenuAdmin):
    name = "Menus"
    icon = "fa-solid fa-bars"
    category = "CMS"
    
    column_list = [
        MenuAdmin.id, MenuAdmin.name, MenuAdmin.slug, MenuAdmin.location,
        MenuAdmin.is_active, MenuAdmin.created_at
    ]
    
    column_searchable_list = [MenuAdmin.name, MenuAdmin.description]
    column_filters = [MenuAdmin.location, MenuAdmin.is_active]

# =============================================================================
# BILLING VIEWS
# =============================================================================

class PlanAdminView(EnhancedModelView, model=PlanAdmin):
    name = "Plans"
    icon = "fa-solid fa-credit-card"
    category = "Billing"
    
    column_list = [
        PlanAdmin.id, PlanAdmin.name, PlanAdmin.price, PlanAdmin.currency,
        PlanAdmin.interval, PlanAdmin.is_popular, PlanAdmin.is_active
    ]
    
    column_searchable_list = [PlanAdmin.name, PlanAdmin.description]
    column_filters = [PlanAdmin.interval, PlanAdmin.is_active, PlanAdmin.is_popular]

class SubscriptionAdminView(EnhancedModelView, model=SubscriptionAdmin):
    name = "Subscriptions"
    icon = "fa-solid fa-sync-alt"
    category = "Billing"
    
    column_list = [
        SubscriptionAdmin.id, SubscriptionAdmin.tenant_id, SubscriptionAdmin.plan_id,
        SubscriptionAdmin.status, SubscriptionAdmin.amount, SubscriptionAdmin.current_period_end
    ]
    
    column_filters = [SubscriptionAdmin.status, SubscriptionAdmin.plan_id]

class InvoiceAdminView(EnhancedModelView, model=InvoiceAdmin):
    name = "Invoices"
    icon = "fa-solid fa-file-invoice"
    category = "Billing"
    
    column_list = [
        InvoiceAdmin.id, InvoiceAdmin.invoice_number, InvoiceAdmin.status,
        InvoiceAdmin.total_amount, InvoiceAdmin.amount_due, InvoiceAdmin.due_date
    ]
    
    column_searchable_list = [InvoiceAdmin.invoice_number, InvoiceAdmin.bill_to_email]
    column_filters = [InvoiceAdmin.status, InvoiceAdmin.currency]

class PaymentAdminView(EnhancedModelView, model=PaymentAdmin):
    name = "Payments"
    icon = "fa-solid fa-money-check-alt"
    category = "Billing"
    
    column_list = [
        PaymentAdmin.id, PaymentAdmin.transaction_id, PaymentAdmin.amount,
        PaymentAdmin.status, PaymentAdmin.payment_method, PaymentAdmin.processed_at
    ]
    
    column_searchable_list = [PaymentAdmin.transaction_id, PaymentAdmin.gateway_transaction_id]
    column_filters = [PaymentAdmin.status, PaymentAdmin.payment_method]

# =============================================================================
# ANALYTICS VIEWS
# =============================================================================

class EventAdminView(EnhancedModelView, model=EventAdmin):
    name = "Events"
    icon = "fa-solid fa-chart-line"
    category = "Analytics"
    
    column_list = [
        EventAdmin.id, EventAdmin.event_type, EventAdmin.event_name,
        EventAdmin.user_id, EventAdmin.ip_address, EventAdmin.created_at
    ]
    
    column_searchable_list = [EventAdmin.event_name, EventAdmin.page_url]
    column_filters = [EventAdmin.event_type, EventAdmin.device_type, EventAdmin.country]

class MetricAdminView(EnhancedModelView, model=MetricAdmin):
    name = "Metrics"
    icon = "fa-solid fa-tachometer-alt"
    category = "Analytics"
    
    column_list = [
        MetricAdmin.id, MetricAdmin.name, MetricAdmin.current_value,
        MetricAdmin.metric_type, MetricAdmin.unit, MetricAdmin.is_active
    ]
    
    column_searchable_list = [MetricAdmin.name, MetricAdmin.description]
    column_filters = [MetricAdmin.metric_type, MetricAdmin.is_active]

class AnalyticsReportAdminView(EnhancedModelView, model=AnalyticsReportAdmin):
    name = "Reports"
    icon = "fa-solid fa-chart-bar"
    category = "Analytics"
    
    column_list = [
        AnalyticsReportAdmin.id, AnalyticsReportAdmin.name, AnalyticsReportAdmin.report_type,
        AnalyticsReportAdmin.status, AnalyticsReportAdmin.last_run_at, AnalyticsReportAdmin.created_at
    ]
    
    column_searchable_list = [AnalyticsReportAdmin.name, AnalyticsReportAdmin.description]
    column_filters = [AnalyticsReportAdmin.report_type, AnalyticsReportAdmin.status]

class DashboardAdminView(EnhancedModelView, model=DashboardAdmin):
    name = "Dashboards"
    icon = "fa-solid fa-desktop"
    category = "Analytics"
    
    column_list = [
        DashboardAdmin.id, DashboardAdmin.name, DashboardAdmin.slug,
        DashboardAdmin.is_default, DashboardAdmin.is_public, DashboardAdmin.is_active
    ]
    
    column_searchable_list = [DashboardAdmin.name, DashboardAdmin.description]
    column_filters = [DashboardAdmin.is_default, DashboardAdmin.is_public, DashboardAdmin.is_active]

# =============================================================================
# INTEGRATION VIEWS
# =============================================================================

class IntegrationAdminView(EnhancedModelView, model=IntegrationAdmin):
    name = "Integrations"
    icon = "fa-solid fa-plug"
    category = "Integrations"
    
    column_list = [
        IntegrationAdmin.id, IntegrationAdmin.name, IntegrationAdmin.service_name,
        IntegrationAdmin.service_type, IntegrationAdmin.status, IntegrationAdmin.last_sync_at
    ]
    
    column_searchable_list = [IntegrationAdmin.name, IntegrationAdmin.service_name]
    column_filters = [IntegrationAdmin.service_type, IntegrationAdmin.status, IntegrationAdmin.auto_sync_enabled]

class WebhookAdminView(EnhancedModelView, model=WebhookAdmin):
    name = "Webhooks"
    icon = "fa-solid fa-webhook"
    category = "Integrations"
    
    column_list = [
        WebhookAdmin.id, WebhookAdmin.name, WebhookAdmin.url, WebhookAdmin.status,
        WebhookAdmin.total_deliveries, WebhookAdmin.successful_deliveries, WebhookAdmin.last_triggered_at
    ]
    
    column_searchable_list = [WebhookAdmin.name, WebhookAdmin.url]
    column_filters = [WebhookAdmin.status, WebhookAdmin.integration_id]

class ExternalServiceAdminView(EnhancedModelView, model=ExternalServiceAdmin):
    name = "External Services"
    icon = "fa-solid fa-cloud"
    category = "Integrations"
    
    column_list = [
        ExternalServiceAdmin.id, ExternalServiceAdmin.name, ExternalServiceAdmin.provider,
        ExternalServiceAdmin.service_type, ExternalServiceAdmin.is_healthy, ExternalServiceAdmin.uptime_percentage
    ]
    
    column_searchable_list = [ExternalServiceAdmin.name, ExternalServiceAdmin.provider]
    column_filters = [ExternalServiceAdmin.service_type, ExternalServiceAdmin.is_healthy, ExternalServiceAdmin.is_active]

class APIKeyAdminView(EnhancedModelView, model=APIKeyAdmin):
    name = "API Keys"
    icon = "fa-solid fa-key"
    category = "Integrations"
    
    column_list = [
        APIKeyAdmin.id, APIKeyAdmin.name, APIKeyAdmin.key_prefix,
        APIKeyAdmin.rate_limit, APIKeyAdmin.total_requests, APIKeyAdmin.last_used_at
    ]
    
    column_searchable_list = [APIKeyAdmin.name]
    column_filters = [APIKeyAdmin.is_active]
    
    # Hide sensitive data
    column_exclude_list = [APIKeyAdmin.key_hash]

# =============================================================================
# SECURITY VIEWS
# =============================================================================

class SecurityEventAdminView(EnhancedModelView, model=SecurityEventAdmin):
    name = "Security Events"
    icon = "fa-solid fa-shield-alt"
    category = "Security"
    
    column_list = [
        SecurityEventAdmin.id, SecurityEventAdmin.event_type, SecurityEventAdmin.risk_level,
        SecurityEventAdmin.user_id, SecurityEventAdmin.ip_address, SecurityEventAdmin.created_at
    ]
    
    column_searchable_list = [SecurityEventAdmin.event_description, SecurityEventAdmin.ip_address]
    column_filters = [SecurityEventAdmin.event_type, SecurityEventAdmin.risk_level, SecurityEventAdmin.is_resolved]

class AuditLogAdminView(EnhancedModelView, model=AuditLogAdmin):
    name = "Audit Logs"
    icon = "fa-solid fa-history"
    category = "Security"
    
    column_list = [
        AuditLogAdmin.id, AuditLogAdmin.action_type, AuditLogAdmin.resource_type,
        AuditLogAdmin.user_id, AuditLogAdmin.ip_address, AuditLogAdmin.created_at
    ]
    
    column_searchable_list = [AuditLogAdmin.resource_name, AuditLogAdmin.description]
    column_filters = [AuditLogAdmin.action_type, AuditLogAdmin.resource_type, AuditLogAdmin.is_successful]
    
    can_create = False  # Audit logs are created automatically
    can_edit = False
    can_delete = False

class RoleAdminView(EnhancedModelView, model=RoleAdmin):
    name = "Roles"
    icon = "fa-solid fa-user-tag"
    category = "Security"
    
    column_list = [
        RoleAdmin.id, RoleAdmin.name, RoleAdmin.display_name,
        RoleAdmin.is_system_role, RoleAdmin.is_default, RoleAdmin.is_active
    ]
    
    column_searchable_list = [RoleAdmin.name, RoleAdmin.display_name, RoleAdmin.description]
    column_filters = [RoleAdmin.is_system_role, RoleAdmin.is_default, RoleAdmin.is_active]

class PermissionAdminView(EnhancedModelView, model=PermissionAdmin):
    name = "Permissions"
    icon = "fa-solid fa-lock"
    category = "Security"
    
    column_list = [
        PermissionAdmin.id, PermissionAdmin.name, PermissionAdmin.display_name,
        PermissionAdmin.category, PermissionAdmin.is_system_permission, PermissionAdmin.is_dangerous
    ]
    
    column_searchable_list = [PermissionAdmin.name, PermissionAdmin.display_name, PermissionAdmin.description]
    column_filters = [PermissionAdmin.category, PermissionAdmin.is_system_permission, PermissionAdmin.is_dangerous]

# =============================================================================
# CUSTOM DASHBOARD VIEWS
# =============================================================================

class PlatformOverviewView(BaseView):
    name = "Platform Overview"
    icon = "fa-solid fa-tachometer-alt"
    
    async def render(self, request: Request) -> str:
        """Render the platform overview dashboard"""
        # This would collect various platform metrics
        # For now, return a placeholder
        return """
        <div class="row">
            <div class="col-md-12">
                <h1>Platform Overview</h1>
                <p>Comprehensive platform statistics and health monitoring.</p>
                <!-- Dashboard widgets would go here -->
            </div>
        </div>
        """

class SystemHealthView(BaseView):
    name = "System Health"
    icon = "fa-solid fa-heartbeat"
    
    async def render(self, request: Request) -> str:
        """Render the system health dashboard"""
        return """
        <div class="row">
            <div class="col-md-12">
                <h1>System Health</h1>
                <p>Real-time system health monitoring and alerts.</p>
                <!-- Health metrics would go here -->
            </div>
        </div>
        """

# Import Business Directory Admin Views
from business_directory_admin import (
    BusinessCategoryAdminView, BusinessListingAdminView, BusinessReviewAdminView,
    BusinessEventAdminView, BusinessProductAdminView, BusinessCouponAdminView,
    BusinessAnalyticsAdminView, DirectorySettingsView, DirectoryAnalyticsDashboard,
    DirectoryIntegrationsView
)

from business_directory_platform_admin import (
    DirectoryPlatformSettingsAdminView, DirectoryIntegrationConfigAdminView,
    DirectoryModerationQueueAdminView, DirectoryContentFilterAdminView,
    DirectoryNotificationSettingsAdminView, DirectoryAnalyticsMetricsAdminView,
    DirectoryPlatformMonitoringView
)

# Export all views for registration
__all__ = [
    # Core Platform
    'TenantAdminView', 'UserAdminView', 'UserSessionAdminView', 'OrganizationAdminView',
    
    # CRM
    'ContactAdminView', 'LeadAdminView', 'DealAdminView', 'ActivityAdminView', 'CampaignAdminView',
    
    # E-commerce
    'ProductAdminView', 'CategoryAdminView', 'OrderAdminView', 'CustomerAdminView', 'InventoryAdminView',
    
    # CMS
    'PageAdminView', 'MediaAdminView', 'FormAdminView', 'CollectionAdminView', 'MenuAdminView',
    
    # Billing
    'PlanAdminView', 'SubscriptionAdminView', 'InvoiceAdminView', 'PaymentAdminView',
    
    # Analytics
    'EventAdminView', 'MetricAdminView', 'AnalyticsReportAdminView', 'DashboardAdminView',
    
    # Integrations
    'IntegrationAdminView', 'WebhookAdminView', 'ExternalServiceAdminView', 'APIKeyAdminView',
    
    # Security
    'SecurityEventAdminView', 'AuditLogAdminView', 'RoleAdminView', 'PermissionAdminView',
    
    # Custom Dashboards
    'PlatformOverviewView', 'SystemHealthView',
    
    # Business Directory - Core Management
    'BusinessCategoryAdminView', 'BusinessListingAdminView', 'BusinessReviewAdminView',
    'BusinessEventAdminView', 'BusinessProductAdminView', 'BusinessCouponAdminView',
    'BusinessAnalyticsAdminView', 'DirectorySettingsView', 'DirectoryAnalyticsDashboard',
    'DirectoryIntegrationsView',
    
    # Business Directory - Platform Administration
    'DirectoryPlatformSettingsAdminView', 'DirectoryIntegrationConfigAdminView',
    'DirectoryModerationQueueAdminView', 'DirectoryContentFilterAdminView',
    'DirectoryNotificationSettingsAdminView', 'DirectoryAnalyticsMetricsAdminView',
    'DirectoryPlatformMonitoringView'
]