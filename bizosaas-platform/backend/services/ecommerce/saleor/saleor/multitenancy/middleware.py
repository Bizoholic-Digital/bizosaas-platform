"""
Multi-tenant middleware for Saleor
Handles organization resolution and context setting based on domain/subdomain
"""

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.conf import settings
import logging
import threading

from .models import Organization, OrganizationMember

logger = logging.getLogger(__name__)

# Thread-local storage for organization context
_organization_context = threading.local()


class OrganizationMiddleware(MiddlewareMixin):
    """
    Middleware to resolve organization based on request domain and set up proper context
    """
    
    def process_request(self, request):
        """Process incoming request to determine organization context"""
        
        # Get hostname from request
        hostname = request.get_host()
        
        # Remove port if present
        if ':' in hostname:
            hostname = hostname.split(':')[0]
        
        # Check cache first for performance
        cache_key = f"organization_lookup:{hostname}"
        organization = cache.get(cache_key)
        
        if organization is None:
            # Try to find organization by exact domain match
            try:
                organization = Organization.objects.select_related('site').get(
                    domain=hostname,
                    is_active=True
                )
            except Organization.DoesNotExist:
                # Try subdomain matching
                organization = self._resolve_subdomain_organization(hostname)
            
            if organization:
                # Cache for 5 minutes
                cache.set(cache_key, organization, 300)
        
        if organization:
            # Set organization context on request
            request.organization = organization
            request.organization_id = organization.id
            request.bizosaas_tenant_id = organization.bizosaas_tenant_id
            
            # Set site context if available
            if organization.site:
                # Override the current site for this request
                Site.objects.clear_cache()
                request._current_site_cache = organization.site
                request.site = organization.site
            
            # Add organization-specific settings to request
            request.organization_settings = {
                'subscription_tier': organization.subscription_tier,
                'tier_limits': organization.tier_limits,
                'branding': {
                    'primary_color': organization.primary_color,
                    'secondary_color': organization.secondary_color,
                    'logo_url': organization.logo.url if organization.logo else None,
                }
            }
            
            # Store in thread-local storage for easy access in models/queries
            _organization_context.organization = organization
            _organization_context.organization_id = organization.id
            
        else:
            # No organization found - use default or raise error
            request.organization = None
            request.organization_id = None
            request.bizosaas_tenant_id = None
            request.organization_settings = {}
            
            # Clear thread-local storage
            _organization_context.organization = None
            _organization_context.organization_id = None
            
            # In development, allow access without organization
            # In production, you might want to redirect or show error
            if hostname in ['localhost', '127.0.0.1', '0.0.0.0']:
                return None
            
            # For production domains without organization, raise 404
            logger.warning(f"No organization found for domain: {hostname}")
            raise Http404(f"No organization found for domain: {hostname}")
    
    def _resolve_subdomain_organization(self, hostname):
        """Try to resolve organization by subdomain matching"""
        try:
            # Split hostname to check for subdomain pattern
            parts = hostname.split('.')
            
            if len(parts) >= 3:
                # Pattern: subdomain.domain.tld
                subdomain = parts[0]
                parent_domain = '.'.join(parts[1:])
                
                organization = Organization.objects.select_related('site').get(
                    subdomain=subdomain,
                    domain=parent_domain,
                    is_active=True
                )
                return organization
                
            elif len(parts) == 2:
                # Pattern: subdomain.domain (like tenant.bizosaas.com)
                subdomain = parts[0]
                
                # Try to find organization with this subdomain pattern
                organization = Organization.objects.select_related('site').filter(
                    subdomain=subdomain,
                    is_active=True
                ).first()
                
                return organization
                
        except Organization.DoesNotExist:
            pass
        
        return None


class OrganizationUserMiddleware(MiddlewareMixin):
    """
    Middleware to add organization membership context to authenticated users
    """
    
    def process_request(self, request):
        """Add organization membership context to request"""
        
        # Skip if no organization or no authenticated user
        if not hasattr(request, 'organization') or not request.organization:
            return None
        
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return None
        
        # Check if user is a member of the current organization
        try:
            membership = OrganizationMember.objects.get(
                organization=request.organization,
                user=request.user,
                is_active=True
            )
            
            # Add membership context to request
            request.organization_membership = membership
            request.organization_role = membership.role
            request.organization_permissions = membership.permissions_for_role
            
            # Store in thread-local storage
            _organization_context.user_membership = membership
            _organization_context.user_role = membership.role
            
        except OrganizationMember.DoesNotExist:
            # User is not a member of this organization
            request.organization_membership = None
            request.organization_role = None
            request.organization_permissions = []
            
            _organization_context.user_membership = None
            _organization_context.user_role = None
            
            # For non-public organizations, you might want to restrict access
            # This depends on your business logic
            logger.warning(
                f"User {request.user.email} attempted to access organization "
                f"{request.organization.name} without membership"
            )


class OrganizationDataIsolationMiddleware(MiddlewareMixin):
    """
    Middleware to ensure data isolation at the database level
    This adds organization context to database queries
    """
    
    def process_request(self, request):
        """Set up database context for organization isolation"""
        
        if not hasattr(request, 'organization') or not request.organization:
            return None
        
        # Store organization ID in thread-local storage for use in model queries
        _organization_context.db_organization_id = request.organization.id
        
        # Add organization context to request for easy access in views
        request.db_organization_id = request.organization.id
    
    def process_response(self, request, response):
        """Clean up thread-local storage after request"""
        
        # Clean up thread-local storage
        for attr in ['organization', 'organization_id', 'user_membership', 
                     'user_role', 'db_organization_id']:
            if hasattr(_organization_context, attr):
                delattr(_organization_context, attr)
        
        return response


# Utility functions for accessing organization context
def get_current_organization():
    """Get current organization from thread-local storage"""
    return getattr(_organization_context, 'organization', None)


def get_current_organization_id():
    """Get current organization ID from thread-local storage"""
    return getattr(_organization_context, 'organization_id', None)


def get_current_user_membership():
    """Get current user's organization membership from thread-local storage"""
    return getattr(_organization_context, 'user_membership', None)


def get_current_user_role():
    """Get current user's role in organization from thread-local storage"""
    return getattr(_organization_context, 'user_role', None)


def require_organization_access(permission=None):
    """
    Decorator to require organization access for views
    """
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            # Check if user has organization access
            if not hasattr(request, 'organization_membership') or not request.organization_membership:
                raise Http404("Access denied: Organization membership required")
            
            # Check specific permission if provided
            if permission and permission not in request.organization_permissions:
                raise Http404(f"Access denied: {permission} permission required")
            
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    return decorator


def organization_feature_required(feature_name):
    """
    Decorator to require specific organization feature access
    """
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if not hasattr(request, 'organization') or not request.organization:
                raise Http404("Organization context required")
            
            if not request.organization.has_feature(feature_name):
                raise Http404(f"Feature '{feature_name}' not available in current subscription tier")
            
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    return decorator