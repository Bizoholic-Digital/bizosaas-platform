from .base import *

DEBUG = True

# Development-specific settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# Disable caching for development to avoid Redis connection issues
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Development database optimizations
DATABASES['default']['OPTIONS'] = {
    'connect_timeout': 10,
}

# Development logging
LOGGING['root']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'DEBUG'
LOGGING['loggers']['wagtail']['level'] = 'DEBUG'

# Django Extensions for development
if 'django_extensions' in INSTALLED_APPS:
    INSTALLED_APPS.append('django_extensions')

# Development-specific Wagtail settings  
WAGTAILADMIN_BASE_URL = 'http://localhost:8006'