from django.urls import path
from cms.wagtail_api_endpoints import get_services, get_homepage

urlpatterns = [
    path('', get_services, name='api_services'),  # For /api/v2/services
    path('', get_homepage, name='api_homepage'),   # For /api/v2/homepage
]
