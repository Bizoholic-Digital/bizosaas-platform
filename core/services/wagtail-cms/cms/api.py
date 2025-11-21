"""
Wagtail API Configuration for BizOSaaS CMS
"""

from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

from .models import LandingPage, CampaignPage, ContentPage

# Create the router
api_router = WagtailAPIRouter('wagtailapi')

# Add the three endpoints using the "register" method
# Tip: register viewsets to only expose a subset of fields
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)

class CMSPagesAPIViewSet(PagesAPIViewSet):
    """Custom API viewset for CMS pages with extended fields"""
    
    # Override filter methods to include our custom fields
    filter_backends = PagesAPIViewSet.filter_backends + []
    
    def get_queryset(self):
        # Get the base queryset and add our custom fields
        queryset = super().get_queryset()
        return queryset.select_related('content_type')

# Register our custom endpoints
api_router.register_endpoint('cms-pages', CMSPagesAPIViewSet)

# URL patterns for Django URLconf
urlpatterns = api_router.get_urlpatterns()