"""
Wagtail CMS Storage Layer URLs
IMPORTANT: These are storage-only endpoints with NO business logic
All business logic is handled by FastAPI Brain
"""

from django.urls import path
from . import storage_api

urlpatterns = [
    # Storage layer health check
    path('storage/health/', storage_api.health_storage, name='storage-health'),
    
    # Tenant data storage (no business logic)
    path('storage/tenants/', storage_api.list_tenants, name='storage-list-tenants'),
    path('storage/tenants/<str:tenant_id>/', storage_api.get_tenant_data, name='storage-get-tenant'),
    path('storage/tenants/create/', storage_api.store_tenant_data, name='storage-create-tenant'),
    
    # Site settings storage (no business logic)
    path('storage/sites/<int:site_id>/settings/', storage_api.get_site_settings, name='storage-get-site-settings'),
    path('storage/sites/<int:site_id>/settings/update/', storage_api.store_site_settings, name='storage-update-site-settings'),
    
    # Page storage (no business logic)
    path('storage/tenants/<str:tenant_id>/pages/', storage_api.get_tenant_pages, name='storage-get-tenant-pages'),
]

# NOTE: All business logic endpoints have been removed
# Business logic is now handled by FastAPI Brain (port 8001)