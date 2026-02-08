"""
URL routing for leads app
RESTful API endpoints with nested routing
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import (
    LeadSourceViewSet, LeadTagViewSet, LeadViewSet,
    LeadActivityViewSet, LeadNoteViewSet
)

# Create the main router
router = DefaultRouter()

# Register main viewsets
router.register(r'sources', LeadSourceViewSet, basename='leadsource')
router.register(r'tags', LeadTagViewSet, basename='leadtag')
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'activities', LeadActivityViewSet, basename='leadactivity')
router.register(r'notes', LeadNoteViewSet, basename='leadnote')

# Create nested routers for lead-specific resources
leads_router = NestedSimpleRouter(router, r'leads', lookup='lead')
leads_router.register(r'activities', LeadActivityViewSet, basename='lead-activities')
leads_router.register(r'notes', LeadNoteViewSet, basename='lead-notes')

app_name = 'leads'

urlpatterns = [
    # Main API endpoints
    path('api/v1/', include(router.urls)),
    
    # Nested endpoints for lead-specific resources
    path('api/v1/', include(leads_router.urls)),
    
    # Additional custom endpoints
    path('api/v1/leads/dashboard/', 
         LeadViewSet.as_view({'get': 'dashboard_stats'}), 
         name='lead-dashboard'),
    
    path('api/v1/leads/bulk-update/', 
         LeadViewSet.as_view({'post': 'bulk_update'}), 
         name='lead-bulk-update'),
    
    path('api/v1/leads/update-scores/', 
         LeadViewSet.as_view({'post': 'update_scores'}), 
         name='lead-update-scores'),
    
    path('api/v1/leads/overdue-followups/', 
         LeadViewSet.as_view({'get': 'overdue_followups'}), 
         name='lead-overdue-followups'),
    
    path('api/v1/leads/high-priority/', 
         LeadViewSet.as_view({'get': 'high_priority'}), 
         name='lead-high-priority'),
    
    path('api/v1/leads/unassigned/', 
         LeadViewSet.as_view({'get': 'unassigned'}), 
         name='lead-unassigned'),
    
    # Activity endpoints
    path('api/v1/activities/upcoming/', 
         LeadActivityViewSet.as_view({'get': 'upcoming'}), 
         name='activity-upcoming'),
    
    path('api/v1/activities/overdue/', 
         LeadActivityViewSet.as_view({'get': 'overdue'}), 
         name='activity-overdue'),
]