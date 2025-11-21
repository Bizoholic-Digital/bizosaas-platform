# Saleor Configuration Overrides
# Additional settings for CoreLDove e-commerce platform

import os
from decimal import Decimal

# CoreLDove specific configurations
SHOP_SETTINGS = {
    'shop_name': 'CoreLDove Marketplace',
    'shop_description': 'Premium Digital Products and Services',
    'default_currency': 'USD',
    'default_country': 'US',
    'header_text': 'CoreLDove - Your Digital Marketplace',
    'default_weight_unit': 'kg',
    'automatic_fulfillment_digital_products': True,
    'charge_taxes_on_shipping': True,
    'include_taxes_in_prices': False,
    'display_gross_prices': True,
    'track_inventory_by_default': True,
    'default_digital_max_downloads': 5,
    'default_digital_url_valid_days': 30,
    'customer_set_password_url': '/account/set-password/',
    'reserve_stock_duration_anonymous_user': 10,
    'reserve_stock_duration_authenticated_user': 30,
}

# Channel configuration for multi-channel support
DEFAULT_CHANNEL_SETTINGS = {
    'name': 'CoreLDove Main',
    'slug': 'coreldove-main',
    'currency_code': 'USD',
    'is_active': True,
    'default_country': 'US',
}

# Warehouse configuration
DEFAULT_WAREHOUSE_SETTINGS = {
    'name': 'CoreLDove Digital Warehouse',
    'slug': 'coreldove-digital',
    'email': 'warehouse@coreldove.com',
    'address': {
        'country': 'US',
        'country_area': 'California',
        'city': 'San Francisco',
        'postal_code': '94102',
        'street_address_1': '123 Digital Ave',
    }
}

# Shipping zones and methods
SHIPPING_ZONES = [
    {
        'name': 'Digital Products Worldwide',
        'countries': ['WORLDWIDE'],
        'shipping_methods': [
            {
                'name': 'Digital Download',
                'type': 'PRICE',
                'price': Decimal('0.00'),
                'minimum_order_price': Decimal('0.00'),
                'maximum_order_price': None,
                'minimum_order_weight': 0,
                'maximum_order_weight': None,
            }
        ]
    },
    {
        'name': 'US Standard Shipping',
        'countries': ['US'],
        'shipping_methods': [
            {
                'name': 'Standard Shipping',
                'type': 'PRICE',
                'price': Decimal('9.99'),
                'minimum_order_price': Decimal('0.00'),
                'maximum_order_price': None,
            },
            {
                'name': 'Express Shipping',
                'type': 'PRICE', 
                'price': Decimal('19.99'),
                'minimum_order_price': Decimal('0.00'),
                'maximum_order_price': None,
            }
        ]
    }
]

# Tax configuration
TAX_RATES = [
    {
        'country': 'US',
        'rate': Decimal('8.25'),  # California tax rate
        'name': 'US Sales Tax'
    }
]

# Payment gateway configuration
PAYMENT_GATEWAYS = {
    'stripe': {
        'supported_currencies': ['USD', 'EUR', 'GBP'],
        'config': [
            {
                'field': 'public_key',
                'value': os.getenv('STRIPE_PUBLIC_KEY', ''),
            },
            {
                'field': 'secret_key',
                'value': os.getenv('STRIPE_SECRET_KEY', ''),
            },
            {
                'field': 'webhook_secret',
                'value': os.getenv('STRIPE_WEBHOOK_SECRET', ''),
            }
        ]
    },
    'dummy': {
        'supported_currencies': ['USD', 'EUR', 'GBP'],
        'config': []
    }
}

# Plugin configurations
PLUGINS = [
    'saleor.payment.gateways.dummy',
    'saleor.payment.gateways.stripe',
    'saleor.plugins.avatax',
    'saleor.plugins.vatlayer',
    'saleor.plugins.webhook',
]

# Email configuration
EMAIL_TEMPLATES_SETTINGS = {
    'default_email_sender_name': 'CoreLDove',
    'default_email_sender_address': 'noreply@coreldove.com',
}

# Search configuration
SEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'saleor.search.backends.postgresql',
    }
}

# Thumbnail settings
THUMBNAIL_SETTINGS = {
    'thumbnail_size': 256,
    'background_color': '#ffffff',
}

# JWT Token settings
JWT_TTL_ACCESS = 60 * 5  # 5 minutes
JWT_TTL_REFRESH = 60 * 60 * 24 * 30  # 30 days

# GraphQL settings
GRAPHQL_QUERY_MAX_COMPLEXITY = 2000
GRAPHQL_QUERY_MAX_DEPTH = 20
GRAPHQL_DISABLE_INTROSPECTION = False

# CORS settings
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3001',
    'http://127.0.0.1:3001',
    'https://coreldove.com',
    'https://storefront.coreldove.com',
]

CORS_ALLOW_ALL_ORIGINS = True  # Only for development
CORS_ALLOW_CREDENTIALS = True

# Media and static files
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# Celery settings
CELERY_TASK_SOFT_TIME_LIMIT = 60 * 10  # 10 minutes
CELERY_TASK_TIME_LIMIT = 60 * 15  # 15 minutes
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True

# Logging configuration
LOGGING_LEVEL = 'DEBUG'
LOG_QUERIES = True

# Security settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_TZ = True
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en'

# Cache settings
CACHE_TTL = 60 * 60  # 1 hour

# Feature flags for development
ENABLE_EXPERIMENTAL_FEATURES = True
ENABLE_DEBUG_TOOLBAR = True if os.getenv('DEBUG') == 'True' else False