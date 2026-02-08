from django.urls import path
from . import enhanced_api_views, api_views

urlpatterns = [
    # Tenant management
    path('tenants/', enhanced_api_views.tenant_list, name='tenant-list'),
    path('tenants/<str:tenant_id>/pages/', enhanced_api_views.tenant_pages, name='tenant-pages'),
    path('tenants/<str:tenant_id>/content-summary/', enhanced_api_views.tenant_content_summary, name='tenant-content-summary'),
    
    # Content types by tenant
    path('tenants/<str:tenant_id>/landing-pages/', enhanced_api_views.landing_pages, name='tenant-landing-pages'),
    path('tenants/<str:tenant_id>/service-pages/', enhanced_api_views.service_pages, name='tenant-service-pages'),
    path('tenants/<str:tenant_id>/content-pages/', enhanced_api_views.content_pages, name='tenant-content-pages'),
    path('tenants/<str:tenant_id>/faq-pages/', enhanced_api_views.faq_pages, name='tenant-faq-pages'),
    
    # Snippets by tenant
    path('tenants/<str:tenant_id>/team-members/', enhanced_api_views.team_members, name='tenant-team-members'),
    path('tenants/<str:tenant_id>/testimonials/', enhanced_api_views.testimonials, name='tenant-testimonials'),
    
    # AI Agent Integration
    path('tenants/<str:tenant_id>/ai/content/', enhanced_api_views.ai_create_content, name='ai-create-content'),
    path('tenants/<str:tenant_id>/ai/content/<int:content_id>/', enhanced_api_views.ai_update_content, name='ai-update-content'),
    path('tenants/<str:tenant_id>/ai/templates/', enhanced_api_views.ai_content_templates, name='ai-content-templates'),
    
    # Navigation and structure
    path('tenants/<str:tenant_id>/navigation/', enhanced_api_views.site_navigation, name='site-navigation'),
    
    # Site settings and branding management
    path('settings/', api_views.site_settings, name='site-settings'),
    path('settings/<int:site_id>/', api_views.site_settings, name='site-settings-by-id'),
    path('tenants/<str:tenant_id>/branding/', api_views.tenant_branding, name='tenant-branding'),
    path('tenants/<str:tenant_id>/branding/update/', api_views.update_tenant_branding, name='update-tenant-branding'),
    
    # Unified CMS endpoints (as requested in requirements)
    path('cms/pages/', enhanced_api_views.cms_pages, name='cms-pages'),
    path('cms/content/<str:content_type>/', enhanced_api_views.cms_content_by_type, name='cms-content-by-type'),
]