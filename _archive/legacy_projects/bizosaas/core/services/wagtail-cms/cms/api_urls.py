from django.urls import path
from . import api_views

urlpatterns = [
    # Tenant management endpoints
    path('list/', api_views.tenant_list, name='tenant_list'),
    path('<str:tenant_id>/pages/', api_views.tenant_pages, name='tenant_pages'),
    path('<str:tenant_id>/content/', api_views.tenant_content, name='tenant_content'),
    
    # Content management endpoints
    path('<str:tenant_id>/landing-pages/', api_views.landing_pages, name='landing_pages'),
    path('<str:tenant_id>/campaigns/', api_views.campaign_pages, name='campaign_pages'),
    path('<str:tenant_id>/content-pages/', api_views.content_pages, name='content_pages'),
]