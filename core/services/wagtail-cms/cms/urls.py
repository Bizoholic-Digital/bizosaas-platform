from django.urls import path, include

urlpatterns = [
    # Custom API endpoints for BizOSaaS integration
    path('tenant/', include('cms.api_urls')),
]