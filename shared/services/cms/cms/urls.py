from django.urls import path, include
from . import views
from . import api_views

urlpatterns = [
    # Custom API endpoints for BizOSaaS integration
    path('tenant/', include('cms.api_urls')),
    
    # SSO Endpoints
    path('admin/sso/login/', views.sso_login, name='sso_login'),
    path('api/internal/sso/token/', api_views.generate_sso_token, name='generate_sso_token'),
]