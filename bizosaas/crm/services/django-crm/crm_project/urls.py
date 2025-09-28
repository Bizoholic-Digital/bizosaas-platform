"""
Django CRM URL Configuration
Multi-tenant CRM with AI integration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime

@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint for container orchestration"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'django-crm',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected',  # TODO: Add actual DB check
        'cache': 'connected',     # TODO: Add actual cache check
    })

@require_http_methods(["GET"])
def service_info(request):
    """Service information endpoint"""
    return JsonResponse({
        'service': 'Django CRM Service',
        'description': 'Multi-tenant Customer Relationship Management with AI integration',
        'version': '1.0.0',
        'features': [
            'Multi-tenant architecture',
            'Lead management with AI scoring',
            'Customer relationship tracking',
            'Product catalog management',
            'Order processing',
            'AI agent integration',
            'Temporal workflow integration',
            'HashiCorp Vault integration'
        ],
        'endpoints': {
            'health': '/health/',
            'admin': '/admin/',
            'api': '/api/',
            'docs': '/api/docs/',
        },
        'integrations': {
            'ai_agents': settings.AI_AGENTS_URL,
            'temporal': settings.TEMPORAL_URL,
            'vault': settings.VAULT_URL,
        }
    })

urlpatterns = [
    # Health and service info
    path('health/', health_check, name='health'),
    path('', service_info, name='service_info'),
    
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('apps.core.urls')),
    path('api/tenants/', include('apps.tenants.urls')),
    path('api/leads/', include('apps.leads.urls')),
    path('api/customers/', include('apps.customers.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/integrations/', include('apps.integrations.urls')),
    
    # Health check for Django health check app
    path('health-check/', include('health_check.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Add Django Debug Toolbar URLs in development
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

# Custom error handlers
handler400 = 'apps.core.views.bad_request'
handler403 = 'apps.core.views.permission_denied'
handler404 = 'apps.core.views.not_found'
handler500 = 'apps.core.views.server_error'