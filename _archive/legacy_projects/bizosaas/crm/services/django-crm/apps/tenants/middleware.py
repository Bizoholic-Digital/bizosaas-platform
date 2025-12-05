"""
Tenant middleware for multi-tenant Django CRM
Handles tenant resolution and context setting
"""
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .models import Tenant, Domain


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware to handle tenant resolution from various sources:
    1. Subdomain (e.g., tenant1.bizoholic.com)
    2. Custom domain (e.g., crm.company.com)
    3. Header (X-Tenant-Id)
    4. JWT token tenant_id
    """
    
    def process_request(self, request):
        """Resolve tenant from request"""
        tenant = None
        
        # Try to get tenant from various sources
        tenant = (
            self._get_tenant_from_header(request) or
            self._get_tenant_from_domain(request) or
            self._get_tenant_from_subdomain(request)
        )
        
        # Set tenant context
        if tenant:
            request.tenant = tenant
            request.tenant_id = tenant.id
        else:
            request.tenant = None
            request.tenant_id = None
        
        return None
    
    def _get_tenant_from_header(self, request):
        """Get tenant from X-Tenant-Id header"""
        tenant_id = request.META.get('HTTP_X_TENANT_ID')
        if tenant_id:
            try:
                return Tenant.objects.get(id=tenant_id, is_active=True)
            except (Tenant.DoesNotExist, ValueError):
                pass
        return None
    
    def _get_tenant_from_domain(self, request):
        """Get tenant from custom domain"""
        host = request.get_host().split(':')[0]  # Remove port if present
        
        try:
            domain = Domain.objects.select_related('tenant').get(
                domain=host,
                is_verified=True,
                tenant__is_active=True
            )
            return domain.tenant
        except Domain.DoesNotExist:
            pass
        
        return None
    
    def _get_tenant_from_subdomain(self, request):
        """Get tenant from subdomain (e.g., tenant1.bizoholic.com)"""
        host = request.get_host().split(':')[0]  # Remove port if present
        host_parts = host.split('.')
        
        # Check if it's a subdomain (at least 3 parts)
        if len(host_parts) >= 3:
            subdomain = host_parts[0]
            
            # Skip www and common subdomains
            if subdomain in ['www', 'api', 'app', 'admin']:
                return None
            
            try:
                return Tenant.objects.get(slug=subdomain, is_active=True)
            except Tenant.DoesNotExist:
                pass
        
        return None
    
    def process_response(self, request, response):
        """Add tenant information to response headers"""
        if hasattr(request, 'tenant') and request.tenant:
            response['X-Tenant-Id'] = str(request.tenant.id)
            response['X-Tenant-Name'] = request.tenant.name
        
        return response


class RequireTenantMiddleware(MiddlewareMixin):
    """
    Middleware to require tenant context for certain paths
    """
    
    TENANT_REQUIRED_PATHS = [
        '/api/leads/',
        '/api/customers/',
        '/api/products/',
        '/api/orders/',
        '/api/analytics/',
    ]
    
    def process_request(self, request):
        """Check if tenant is required for this path"""
        path = request.path
        
        # Check if this path requires tenant
        requires_tenant = any(
            path.startswith(tenant_path) 
            for tenant_path in self.TENANT_REQUIRED_PATHS
        )
        
        if requires_tenant and not getattr(request, 'tenant', None):
            return JsonResponse(
                {
                    'error': 'Tenant context required',
                    'message': 'This endpoint requires tenant identification via subdomain, custom domain, or X-Tenant-Id header',
                    'code': 'TENANT_REQUIRED'
                },
                status=400
            )
        
        return None