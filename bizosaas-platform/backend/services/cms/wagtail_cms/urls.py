from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from django.conf.urls.static import static

from . import views

# Create API router
api_router = WagtailAPIRouter('wagtailapi')
api_router.register_endpoint('pages', PagesAPIViewSet)

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    
    # Wagtail API v2 (standard API)
    path("api/v2/", api_router.urls),
    
    # Custom CMS API 
    path("api/v2/", include('cms.api')),
    
    # API endpoints for BizOSaaS integration  
    path("api/v1/", include("cms.urls")),
    
    # Enhanced CMS API for AI agents and unified content management
    path("api/", include("cms.enhanced_api_urls")),
    
    # IMPORTANT: Storage-only API (no business logic)
    # All business logic is handled by FastAPI Brain
    path("api/", include("cms.storage_urls")),
    
    # Health check endpoint
    path("health/", views.health_check, name="health_check"),
    
    # Temporary superuser creation endpoint (DEBUG only)
    path("create-superuser/", views.create_superuser_endpoint, name="create_superuser"),
    
    # Authentication bridge endpoints
    path("auth/", include("authentication.urls")),
    
    # Wagtail pages
    path("", include(wagtail_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)