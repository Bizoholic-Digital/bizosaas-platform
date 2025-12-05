"""
Multi-tenant middleware for Wagtail CMS
Handles tenant resolution based on domain/subdomain and sets up proper site context
"""

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sites.models import Site
from wagtail.models import Site as WagtailSite
from django.core.cache import cache

from .models import Tenant


class MultiTenantMiddleware(MiddlewareMixin):
    """
    Middleware to resolve tenant based on request domain and set up proper site context
    """
    
    def process_request(self, request):
        """Process incoming request to determine tenant context"""
        
        # Get hostname from request
        hostname = request.get_host()
        
        # Remove port if present
        if ':' in hostname:
            hostname = hostname.split(':')[0]
        
        # Check cache first for performance
        cache_key = f"tenant_lookup:{hostname}"
        tenant = cache.get(cache_key)
        
        if tenant is None:
            # Try to find tenant by exact domain match
            try:
                tenant = Tenant.objects.select_related('wagtail_site').get(
                    domain=hostname,
                    is_active=True
                )
            except Tenant.DoesNotExist:
                # Try subdomain matching
                tenant = self._resolve_subdomain_tenant(hostname)
            
            if tenant:
                # Cache for 5 minutes
                cache.set(cache_key, tenant, 300)
        
        if tenant:
            # Set tenant context on request
            request.tenant = tenant
            request.tenant_id = tenant.bizosaas_tenant_id
            
            # Set Wagtail site context if available
            if tenant.wagtail_site:
                # Override the current site for this request
                Site.objects.clear_cache()
                request._wagtail_site = tenant.wagtail_site
                
                # Add site to request for easy access
                request.site = tenant.wagtail_site
            
            # Add tenant-specific settings to request
            request.tenant_settings = {
                'theme': tenant.theme_settings,
                'seo': tenant.seo_settings,
                'api': tenant.api_settings
            }
        else:
            # No tenant found - use default or raise error
            request.tenant = None
            request.tenant_id = None
            request.tenant_settings = {}
            
            # In development, allow access without tenant
            # In production, you might want to redirect or show error
            if hostname in ['localhost', '127.0.0.1', '0.0.0.0']:
                return None
            
            # For production domains without tenant, raise 404
            raise Http404(f"No tenant found for domain: {hostname}")
    
    def _resolve_subdomain_tenant(self, hostname):
        """Try to resolve tenant by subdomain matching"""
        try:
            # Split hostname to check for subdomain pattern
            parts = hostname.split('.')
            
            if len(parts) >= 3:
                # Pattern: subdomain.domain.tld
                subdomain = parts[0]
                parent_domain = '.'.join(parts[1:])
                
                tenant = Tenant.objects.select_related('wagtail_site').get(
                    subdomain=subdomain,
                    domain=parent_domain,
                    is_active=True
                )
                return tenant
                
            elif len(parts) == 2:
                # Pattern: subdomain.domain (like tenant.bizosaas.com)
                subdomain = parts[0]
                
                # Try to find tenant with this subdomain pattern
                tenant = Tenant.objects.select_related('wagtail_site').filter(
                    subdomain=subdomain,
                    is_active=True
                ).first()
                
                return tenant
                
        except Tenant.DoesNotExist:
            pass
        
        return None


class TenantContextMiddleware(MiddlewareMixin):
    """
    Additional middleware to add tenant context to templates and views
    """
    
    def process_request(self, request):
        """Add tenant context to request"""
        if not hasattr(request, 'tenant') or not request.tenant:
            return None
        
        # Add commonly used tenant data to context
        request.tenant_context = {
            'tenant_name': request.tenant.name,
            'tenant_id': request.tenant.bizosaas_tenant_id,
            'domain': request.tenant.full_domain,
            'is_active': request.tenant.is_active,
            'theme_settings': request.tenant.theme_settings,
            'seo_settings': request.tenant.seo_settings,
        }
    
    def process_template_response(self, request, response):
        """Add tenant context to template context"""
        if hasattr(response, 'context_data') and hasattr(request, 'tenant_context'):
            if response.context_data is None:
                response.context_data = {}
            
            response.context_data['tenant'] = request.tenant_context
        
        return response


class WagtailSiteMiddleware(MiddlewareMixin):
    """
    Custom Wagtail site middleware to work with multi-tenant setup
    """
    
    def process_request(self, request):
        """Set the appropriate Wagtail site for the current tenant"""
        
        # Skip if no tenant or no wagtail site
        if not hasattr(request, 'tenant') or not request.tenant or not request.tenant.wagtail_site:
            return None
        
        # Set the wagtail site for this request
        wagtail_site = request.tenant.wagtail_site
        
        # Override Wagtail's site finding mechanism
        request._wagtail_site = wagtail_site
        
        # Also set for Django's sites framework compatibility
        from django.contrib.sites.shortcuts import get_current_site
        from django.contrib.sites.models import Site as DjangoSite
        
        try:
            # Try to find corresponding Django site
            django_site = DjangoSite.objects.get(domain=wagtail_site.hostname)
            request._current_site_cache = django_site
        except DjangoSite.DoesNotExist:
            # Create Django site if it doesn't exist
            django_site = DjangoSite.objects.create(
                domain=wagtail_site.hostname,
                name=wagtail_site.site_name
            )
            request._current_site_cache = django_site


class TenantDatabaseMiddleware(MiddlewareMixin):
    """
    Middleware to add tenant context to database queries
    This ensures tenant isolation at the database level
    """
    
    def process_request(self, request):
        """Set up database context for tenant isolation"""
        if not hasattr(request, 'tenant') or not request.tenant:
            return None
        
        # Store tenant ID in thread-local storage for use in model queries
        from threading import local
        
        if not hasattr(self, '_local'):
            self._local = local()
        
        self._local.tenant_id = request.tenant.bizosaas_tenant_id
        
        # Add tenant context to request for easy access in views
        request.db_tenant_id = request.tenant.bizosaas_tenant_id
    
    @classmethod
    def get_current_tenant_id(cls):
        """Get current tenant ID from thread-local storage"""
        if hasattr(cls, '_local') and hasattr(cls._local, 'tenant_id'):
            return cls._local.tenant_id
        return None