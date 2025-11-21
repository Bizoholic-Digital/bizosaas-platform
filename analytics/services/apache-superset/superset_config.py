# Apache Superset Configuration for BizOSaaS Platform
import os
from typing import Optional

# Basic configuration
ROW_LIMIT = 5000
VIZ_ROW_LIMIT = 10000
SUPERSET_WEBSERVER_PORT = 8088

# Secret key for security
SECRET_KEY = os.environ.get('SUPERSET_SECRET_KEY', 'superset-secret-key-development')

# Database configuration - Use BizOSaaS PostgreSQL
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL', 
    'postgresql://admin:securepassword@postgres:5432/bizosaas'
)

# Redis configuration
REDIS_HOST = 'redis'
REDIS_PORT = 6379
REDIS_DB = 4

class CeleryConfig:
    CELERY_IMPORTS = ('superset.sql_lab', )
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}
    BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
    CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

CELERY_CONFIG = CeleryConfig

# Enable CORS for BizOSaaS integration
ENABLE_CORS = True
CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': ['http://localhost:3000', 'http://localhost:8001', 'http://bizosaas.local']
}

# Authentication configuration
AUTH_TYPE = 1  # AUTH_DB

# Feature flags
FEATURE_FLAGS = {
    'ALERT_REPORTS': True,
    'DASHBOARD_FILTERS_EXPERIMENTAL': True,
    'ENABLE_TEMPLATE_PROCESSING': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'HORIZONTAL_FILTER_BAR': True,
}

# Cache configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': REDIS_HOST,
    'CACHE_REDIS_PORT': REDIS_PORT,
    'CACHE_REDIS_DB': REDIS_DB,
}

# Enable asynchronous query execution
RESULTS_BACKEND = {
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'superset_results_',
    'CACHE_REDIS_URL': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
}

# Security settings
WTF_CSRF_ENABLED = True
WTF_CSRF_EXEMPT_LIST = ['superset.views.core.log']
WTF_CSRF_TIME_LIMIT = None

# File upload settings
UPLOAD_FOLDER = '/app/superset_home/uploads/'

# Email configuration (for alerts and reports)
SMTP_HOST = os.environ.get('SMTP_HOST', 'localhost')
SMTP_STARTTLS = True
SMTP_SSL = False
SMTP_USER = os.environ.get('SMTP_USER', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
SMTP_MAIL_FROM = os.environ.get('SMTP_MAIL_FROM', 'noreply@bizosaas.local')

# Logging configuration
ENABLE_TIME_ROTATE = True
TIME_ROTATE_LOG_LEVEL = 'INFO'
FILENAME = os.path.join('/app/superset_home', 'superset.log')

# Dashboard configuration
DASHBOARD_AUTO_REFRESH_MODE = "fetch"
DASHBOARD_AUTO_REFRESH_INTERVALS = [
    [0, "Don't refresh"],
    [10, "10 seconds"],
    [30, "30 seconds"],
    [60, "1 minute"],
    [300, "5 minutes"],
    [1800, "30 minutes"],
    [3600, "1 hour"],
]

# BizOSaaS specific configurations
BIZOSAAS_BRAIN_API_URL = os.environ.get('BIZOSAAS_BRAIN_API_URL', 'http://bizosaas-brain:8001')
BIZOSAAS_PLATFORM = True