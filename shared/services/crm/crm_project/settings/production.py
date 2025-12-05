"""
Production settings for Django CRM
Uses HashiCorp Vault for secure secret management
"""
from .base import *
from decouple import config

# Import Vault configuration helper
try:
    from crm_project.vault_config_helper import (
        get_database_config,
        get_redis_config,
    )
    VAULT_ENABLED = True
except ImportError:
    VAULT_ENABLED = False
    print("⚠️  Vault helper not available in production, using environment variables")

# Production settings
DEBUG = False

# Production security
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# Production database with connection pooling - Using Vault
if VAULT_ENABLED:
    db_config = get_database_config()
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='django_crm'),
            'USER': db_config['username'],
            'PASSWORD': db_config['password'],
            'HOST': db_config['host'],
            'PORT': db_config['port'],
            'CONN_MAX_AGE': 600,
            'OPTIONS': {
                'options': '-c search_path=public,crm'
            }
        }
    }
else:
    # Fallback to environment variables if Vault unavailable
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='bizosaas'),
            'USER': config('DB_USER', default='admin'),
            'PASSWORD': config('DB_PASSWORD', default='BizoholicSecure2025'),
            'HOST': config('DB_HOST', default='bizosaas-postgres'),
            'PORT': config('DB_PORT', default='5432'),
            'CONN_MAX_AGE': 600,
            'OPTIONS': {
                'options': '-c search_path=public,crm'
            }
        }
    }

# Production caching with Redis - Using Vault
if VAULT_ENABLED:
    redis_config = get_redis_config()
    redis_url = config('REDIS_URL', default=f"redis://{redis_config['host']}:{redis_config['port']}/1")
else:
    redis_url = config('REDIS_URL', default='redis://bizosaas-redis:6379/1')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': redis_url,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            }
        },
        'KEY_PREFIX': 'crm_prod',
        'TIMEOUT': 300,
    }
}

# Production Celery - Using Vault
if VAULT_ENABLED:
    redis_config = get_redis_config()
    CELERY_BROKER_URL = config('CELERY_BROKER_URL', default=f"redis://{redis_config['host']}:{redis_config['port']}/2")
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default=f"redis://{redis_config['host']}:{redis_config['port']}/3")
else:
    CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://bizosaas-redis:6379/2')
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://bizosaas-redis:6379/3')

# Production AI Integration
AI_AGENTS_URL = config('AI_AGENTS_URL', default='http://bizosaas-ai-agents:8000')
TEMPORAL_URL = config('TEMPORAL_URL', default='http://bizosaas-temporal-integration:8202')
VAULT_URL = config('VAULT_URL', default='http://bizosaas-vault-integration:8201')

# Production CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://bizoholic.com",
    "https://www.bizoholic.com",
    "https://coreldove.com",
    "https://www.coreldove.com",
    "https://app.bizoholic.com",
    "https://crm.bizoholic.com",
]

# Production logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'json': {
            'format': '{{"level": "{levelname}", "time": "{asctime}", "module": "{module}", "message": "{message}"}}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/app/logs/django.log',
            'maxBytes': 50 * 1024 * 1024,  # 50MB
            'backupCount': 5,
            'formatter': 'json',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/app/logs/error.log',
            'maxBytes': 50 * 1024 * 1024,  # 50MB
            'backupCount': 5,
            'formatter': 'json',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'crm_project': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Production email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'