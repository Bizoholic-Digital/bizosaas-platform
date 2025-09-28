# SQLAdmin Dashboard Data Models
# Comprehensive model definitions for BizOSaaS platform management

from .core import *
from .crm import *
from .ecommerce import *
from .cms import *
from .billing import *
from .analytics import *
from .integrations import *
from .security import *

__all__ = [
    # Core models
    'TenantAdmin', 'UserAdmin', 'UserSessionAdmin', 'OrganizationAdmin',
    # CRM models
    'ContactAdmin', 'LeadAdmin', 'DealAdmin', 'ActivityAdmin', 'CampaignAdmin',
    # E-commerce models
    'ProductAdmin', 'CategoryAdmin', 'OrderAdmin', 'CustomerAdmin', 'InventoryAdmin',
    # CMS models
    'PageAdmin', 'MediaAdmin', 'FormAdmin', 'CollectionAdmin', 'MenuAdmin',
    # Billing models
    'SubscriptionAdmin', 'InvoiceAdmin', 'PaymentAdmin', 'PlanAdmin',
    # Analytics models
    'AnalyticsReportAdmin', 'MetricAdmin', 'DashboardAdmin', 'EventAdmin',
    # Integration models
    'IntegrationAdmin', 'WebhookAdmin', 'APIKeyAdmin', 'ExternalServiceAdmin',
    # Security models
    'SecurityEventAdmin', 'AuditLogAdmin', 'RoleAdmin', 'PermissionAdmin'
]