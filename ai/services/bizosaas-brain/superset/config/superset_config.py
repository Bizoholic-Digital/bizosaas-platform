"""
Apache Superset Configuration for BizOSaaS Multi-Tenant Analytics
Integrates with Brain API for authentication and tenant isolation
"""

import os
import logging
from typing import Dict, Any, Optional
from flask import request, g
from flask_appbuilder.security.manager import BaseSecurityManager
import requests

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# BASIC CONFIGURATION
# =============================================================================

# Database Configuration
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{os.getenv('DATABASE_USER', 'superset')}:"
    f"{os.getenv('DATABASE_PASSWORD', 'superset_secure_password')}@"
    f"{os.getenv('DATABASE_HOST', 'superset-db')}:"
    f"{os.getenv('DATABASE_PORT', '5432')}/"
    f"{os.getenv('DATABASE_DB', 'superset')}"
)

# Redis Configuration for Caching
REDIS_HOST = os.getenv('REDIS_HOST', 'superset-redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'redis_secure_password')

# Cache Configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': REDIS_HOST,
    'CACHE_REDIS_PORT': REDIS_PORT,
    'CACHE_REDIS_PASSWORD': REDIS_PASSWORD,
    'CACHE_REDIS_DB': 1,
}

# Results Backend for Async Queries
RESULTS_BACKEND = {
    'cache_type': 'RedisCache',
    'cache_default_timeout': 86400,  # 1 day
    'cache_key_prefix': 'superset_results_',
    'cache_redis_host': REDIS_HOST,
    'cache_redis_port': REDIS_PORT,
    'cache_redis_password': REDIS_PASSWORD,
    'cache_redis_db': 2,
}

# Secret Key for Security
SECRET_KEY = os.getenv('SECRET_KEY', 'your-super-secret-key-change-in-production')

# =============================================================================
# BRAIN API INTEGRATION
# =============================================================================

BRAIN_API_URL = os.getenv('BRAIN_API_URL', 'http://brain-api:8001')
BRAIN_API_TOKEN = os.getenv('BRAIN_API_TOKEN', 'brain_api_secure_token')

def get_brain_api_headers() -> Dict[str, str]:
    """Get headers for Brain API requests"""
    return {
        'Authorization': f'Bearer {BRAIN_API_TOKEN}',
        'Content-Type': 'application/json'
    }

def validate_tenant_access(tenant_id: str, user_id: str) -> bool:
    """Validate if user has access to tenant data"""
    try:
        response = requests.get(
            f"{BRAIN_API_URL}/api/tenant/access-check",
            headers=get_brain_api_headers(),
            params={'tenant_id': tenant_id, 'user_id': user_id},
            timeout=5
        )
        return response.status_code == 200 and response.json().get('has_access', False)
    except Exception as e:
        logger.error(f"Brain API access check failed: {e}")
        return False

def get_user_tenant_context(user_id: str) -> Optional[str]:
    """Get user's tenant context from Brain API"""
    try:
        response = requests.get(
            f"{BRAIN_API_URL}/api/auth/user-context",
            headers=get_brain_api_headers(),
            params={'user_id': user_id},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('tenant_id')
    except Exception as e:
        logger.error(f"Failed to get user tenant context: {e}")
    return None

# =============================================================================
# MULTI-TENANT CONFIGURATION
# =============================================================================

# Feature Flags for Multi-Tenancy
FEATURE_FLAGS = {
    'ENABLE_TEMPLATE_PROCESSING': True,
    'ROW_LEVEL_SECURITY': True,
    'DASHBOARD_FILTERS_EXPERIMENTAL': True,
    'DASHBOARD_NATIVE_FILTERS': True,
    'GLOBAL_ASYNC_QUERIES': True,
    'VERSIONED_EXPORT': True,
    'THUMBNAILS': True,
    'ALERT_REPORTS': True,
    'DYNAMIC_PLUGINS': True,
}

# Row Level Security Filter
def get_rls_filter() -> Optional[str]:
    """
    Generate Row Level Security filter based on current user's tenant
    This function is called by Superset to add tenant isolation to queries
    """
    try:
        # Get current user from Flask-AppBuilder
        from flask_appbuilder.security.sqla.models import User
        from flask import g
        
        if not hasattr(g, 'user') or not g.user:
            return "1=0"  # Deny access if no user
            
        user_id = str(g.user.id)
        tenant_id = get_user_tenant_context(user_id)
        
        if not tenant_id:
            logger.warning(f"No tenant context for user {user_id}")
            return "1=0"  # Deny access if no tenant
            
        # Store tenant_id in g for use in other parts of the app
        g.tenant_id = tenant_id
        
        # Return SQL filter for tenant isolation
        return f"tenant_id = '{tenant_id}'"
        
    except Exception as e:
        logger.error(f"RLS filter generation failed: {e}")
        return "1=0"  # Deny access on error

# Apply RLS to all datasets
RLS_BASE_FILTER = get_rls_filter

# =============================================================================
# DATABASE CONNECTIONS
# =============================================================================

# Main BizOSaaS Database Connection
BIZOSAAS_DB_URI = (
    f"postgresql://{os.getenv('BIZOSAAS_DB_USER', 'bizosaas')}:"
    f"{os.getenv('BIZOSAAS_DB_PASSWORD', 'bizosaas_password')}@"
    f"{os.getenv('BIZOSAAS_DB_HOST', 'postgres')}:"
    f"{os.getenv('BIZOSAAS_DB_PORT', '5432')}/"
    f"{os.getenv('BIZOSAAS_DB_NAME', 'bizosaas')}"
)

# ClickHouse for Analytics (if enabled)
CLICKHOUSE_URI = (
    f"clickhouse+native://{os.getenv('CLICKHOUSE_USER', 'analytics')}:"
    f"{os.getenv('CLICKHOUSE_PASSWORD', 'clickhouse_secure_password')}@"
    f"{os.getenv('CLICKHOUSE_HOST', 'clickhouse')}:"
    f"{os.getenv('CLICKHOUSE_PORT', '9000')}/"
    f"{os.getenv('CLICKHOUSE_DB', 'analytics')}"
)

# =============================================================================
# SECURITY CONFIGURATION
# =============================================================================

# Custom Security Manager for Brain API Integration
class BrainAPISecurityManager(BaseSecurityManager):
    """Custom security manager that integrates with Brain API for authentication"""
    
    def auth_user_brain_api(self, username: str, password: str) -> Optional[Any]:
        """Authenticate user against Brain API"""
        try:
            response = requests.post(
                f"{BRAIN_API_URL}/api/auth/login",
                json={'username': username, 'password': password},
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                return user_data
                
        except Exception as e:
            logger.error(f"Brain API authentication failed: {e}")
        
        return None
    
    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information from Brain API"""
        try:
            response = requests.get(
                f"{BRAIN_API_URL}/api/auth/user/{user_id}",
                headers=get_brain_api_headers(),
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
                
        except Exception as e:
            logger.error(f"Failed to get user info: {e}")
        
        return None

# Use custom security manager
CUSTOM_SECURITY_MANAGER = BrainAPISecurityManager

# =============================================================================
# DASHBOARD AND VISUALIZATION CONFIGURATION
# =============================================================================

# Default Dashboard Filters
DEFAULT_FEATURE_FLAGS = {
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_NATIVE_FILTERS_SET': True,
    'GLOBAL_ASYNC_QUERIES': True,
}

# Chart configurations
VIZ_TYPE_DENYLIST = []  # Allow all visualization types

# Dashboard configuration
SUPERSET_DASHBOARD_POSITION_DATA_LIMIT = 65535
DASHBOARD_AUTO_REFRESH_INTERVALS = [
    [0, "Don't refresh"],
    [10, "10 seconds"],
    [30, "30 seconds"], 
    [60, "1 minute"],
    [300, "5 minutes"],
    [1800, "30 minutes"],
    [3600, "1 hour"],
]

# =============================================================================
# API CONFIGURATION
# =============================================================================

# Enable public API
FAB_API_SWAGGER_UI = True
CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': {
        '/api/*': {'origins': '*'},
        '/superset/csrf_token/': {'origins': '*'}
    }
}

# API rate limiting
RATELIMIT_ENABLED = True
RATELIMIT_STORAGE_URI = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/3"

# =============================================================================
# PERFORMANCE AND SCALING
# =============================================================================

# Query timeout
SUPERSET_WEBSERVER_TIMEOUT = 300  # 5 minutes

# Async queries
GLOBAL_ASYNC_QUERIES_TRANSPORT = "polling"
GLOBAL_ASYNC_QUERIES_POLLING_DELAY = 500

# SQL Lab Configuration
SQLLAB_ASYNC_TIME_LIMIT_SEC = 300
SQLLAB_TIMEOUT = 300
SQL_MAX_ROW = 100000

# =============================================================================
# LOGGING
# =============================================================================

# Logging configuration
ENABLE_TIME_ROTATE = True
TIME_ROTATE_LOG_LEVEL = 'DEBUG'
FILENAME = '/app/superset_home/superset.log'

# =============================================================================
# CUSTOM JINJA CONTEXT
# =============================================================================

def custom_jinja_context() -> Dict[str, Any]:
    """Add custom variables to Jinja templates"""
    return {
        'tenant_id': getattr(g, 'tenant_id', 'default'),
        'current_user_id': getattr(g, 'user', {}).get('id', 'anonymous'),
        'brain_api_url': BRAIN_API_URL,
    }

JINJA_CONTEXT_ADDONS = custom_jinja_context

# =============================================================================
# EMAIL CONFIGURATION (Optional)
# =============================================================================

# Email configuration for reports and alerts
SMTP_HOST = os.getenv('SMTP_HOST', 'localhost')
SMTP_STARTTLS = True
SMTP_SSL = False
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
SMTP_MAIL_FROM = os.getenv('SMTP_MAIL_FROM', 'superset@bizosaas.com')

EMAIL_NOTIFICATIONS = True
ALERT_REPORTS_NOTIFICATION_DRY_RUN = False

# =============================================================================
# CELERY CONFIGURATION (for async tasks)
# =============================================================================

# Celery configuration for background tasks
class CeleryConfig:
    BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/4"
    CELERY_IMPORTS = ['superset.sql_lab', 'superset.tasks']
    CELERY_RESULT_BACKEND = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/5"
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}
    CELERY_TASK_PROTOCOL = 1

CELERY_CONFIG = CeleryConfig

# =============================================================================
# BRAIN API WEBHOOK ENDPOINTS
# =============================================================================

# Webhook for tenant updates
BRAIN_API_WEBHOOKS = {
    'tenant_updated': f"{BRAIN_API_URL}/webhooks/superset/tenant-updated",
    'user_updated': f"{BRAIN_API_URL}/webhooks/superset/user-updated",
    'permissions_changed': f"{BRAIN_API_URL}/webhooks/superset/permissions-changed",
}