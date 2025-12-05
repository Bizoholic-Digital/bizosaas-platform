"""
Core permissions for Django CRM
Multi-tenant permission handling and role-based access control
"""
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from django.db.models import Q


class TenantPermissionMixin:
    """Mixin to handle tenant-based filtering in ViewSets"""
    
    def get_queryset(self):
        """Filter queryset by tenant"""
        queryset = super().get_queryset()
        
        # Filter by tenant if request has tenant context
        if hasattr(self.request, 'tenant') and self.request.tenant:
            return queryset.filter(tenant=self.request.tenant)
        
        return queryset.none()  # Return empty queryset if no tenant
    
    def perform_create(self, serializer):
        """Set tenant when creating objects"""
        if hasattr(self.request, 'tenant') and self.request.tenant:
            serializer.save(tenant=self.request.tenant)
        else:
            raise permissions.PermissionDenied("No tenant context available")


class IsTenantMember(BasePermission):
    """Permission to check if user is a member of the tenant"""
    
    message = "You must be a member of this tenant to perform this action."
    
    def has_permission(self, request, view):
        """Check if user is authenticated and is a tenant member"""
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Superuser can access everything
        if request.user.is_superuser:
            return True
        
        # Check if request has tenant context
        if not hasattr(request, 'tenant') or not request.tenant:
            return False
        
        # Check if user is a member of the tenant
        return request.user.memberships.filter(
            tenant=request.tenant,
            is_active=True
        ).exists()


class IsTenantAdmin(BasePermission):
    """Permission to check if user is an admin of the tenant"""
    
    message = "You must be an admin of this tenant to perform this action."
    
    def has_permission(self, request, view):
        """Check if user is authenticated and is a tenant admin"""
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Superuser can access everything
        if request.user.is_superuser:
            return True
        
        # Check if request has tenant context
        if not hasattr(request, 'tenant') or not request.tenant:
            return False
        
        # Check if user is an admin or owner of the tenant
        return request.user.memberships.filter(
            tenant=request.tenant,
            role__in=['owner', 'admin'],
            is_active=True
        ).exists()


class IsTenantOwner(BasePermission):
    """Permission to check if user is the owner of the tenant"""
    
    message = "You must be the owner of this tenant to perform this action."
    
    def has_permission(self, request, view):
        """Check if user is authenticated and is a tenant owner"""
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Superuser can access everything
        if request.user.is_superuser:
            return True
        
        # Check if request has tenant context
        if not hasattr(request, 'tenant') or not request.tenant:
            return False
        
        # Check if user is the owner of the tenant
        return request.user.memberships.filter(
            tenant=request.tenant,
            role='owner',
            is_active=True
        ).exists()


class CanManageLeads(BasePermission):
    """Permission to manage leads"""
    
    message = "You don't have permission to manage leads."
    
    def has_permission(self, request, view):
        """Check if user can manage leads"""
        # Must be tenant member first
        if not IsTenantMember().has_permission(request, view):
            return False
        
        # Check role-based permissions
        membership = request.user.memberships.filter(
            tenant=request.tenant,
            is_active=True
        ).first()
        
        if not membership:
            return False
        
        # Owners and admins can always manage leads
        if membership.role in ['owner', 'admin']:
            return True
        
        # Managers can manage leads
        if membership.role == 'manager':
            return True
        
        # Users can manage leads but with restrictions
        if membership.role == 'user':
            return True
        
        # Read-only users cannot manage leads
        return False
    
    def has_object_permission(self, request, view, obj):
        """Check object-level permissions"""
        # Must have basic permission first
        if not self.has_permission(request, view):
            return False
        
        # Get user's membership
        membership = request.user.memberships.filter(
            tenant=request.tenant,
            is_active=True
        ).first()
        
        if not membership:
            return False
        
        # Owners and admins can access all leads
        if membership.role in ['owner', 'admin']:
            return True
        
        # Managers can access all leads
        if membership.role == 'manager':
            return True
        
        # Users can only access their own assigned leads for updates/deletes
        if membership.role == 'user':
            if request.method in ['GET', 'HEAD', 'OPTIONS']:
                return True  # Can view all leads
            else:
                # Can only modify assigned leads or unassigned leads
                return obj.assigned_to == request.user or obj.assigned_to is None
        
        return False


class CanViewLeads(BasePermission):
    """Permission to view leads"""
    
    message = "You don't have permission to view leads."
    
    def has_permission(self, request, view):
        """Check if user can view leads"""
        # Must be tenant member first
        if not IsTenantMember().has_permission(request, view):
            return False
        
        # All tenant members can view leads
        return True
    
    def has_object_permission(self, request, view, obj):
        """Check object-level permissions for viewing"""
        # Must have basic permission first
        if not self.has_permission(request, view):
            return False
        
        # All tenant members can view all leads
        return True


class CanManageLeadSources(BasePermission):
    """Permission to manage lead sources"""
    
    message = "You don't have permission to manage lead sources."
    
    def has_permission(self, request, view):
        """Check if user can manage lead sources"""
        # Must be tenant member first
        if not IsTenantMember().has_permission(request, view):
            return False
        
        # Get user's membership
        membership = request.user.memberships.filter(
            tenant=request.tenant,
            is_active=True
        ).first()
        
        if not membership:
            return False
        
        # Only admins and owners can manage lead sources
        return membership.role in ['owner', 'admin']


class CanManageTenantSettings(BasePermission):
    """Permission to manage tenant settings"""
    
    message = "You don't have permission to manage tenant settings."
    
    def has_permission(self, request, view):
        """Check if user can manage tenant settings"""
        # Must be tenant admin
        return IsTenantAdmin().has_permission(request, view)


class IsOwnerOrReadOnly(BasePermission):
    """Permission to edit only own objects"""
    
    def has_object_permission(self, request, view, obj):
        """Check if user owns the object or is read-only"""
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for object owner
        return obj.user == request.user


class IsAssignedOrReadOnly(BasePermission):
    """Permission for assigned user or read-only access"""
    
    def has_object_permission(self, request, view, obj):
        """Check if user is assigned to the lead or read-only"""
        # Read permissions for any tenant member
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions for assigned user or admins
        if hasattr(obj, 'assigned_to') and obj.assigned_to == request.user:
            return True
        
        # Check if user is admin
        if hasattr(request, 'tenant'):
            membership = request.user.memberships.filter(
                tenant=request.tenant,
                role__in=['owner', 'admin'],
                is_active=True
            ).first()
            return membership is not None
        
        return False


# Utility functions for permission checking
def check_tenant_permission(user, tenant, required_role=None):
    """Check if user has permission for tenant with optional role requirement"""
    if not user or not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    membership = user.memberships.filter(
        tenant=tenant,
        is_active=True
    ).first()
    
    if not membership:
        return False
    
    if required_role:
        role_hierarchy = {
            'readonly': 0,
            'user': 1,
            'manager': 2,
            'admin': 3,
            'owner': 4
        }
        
        user_level = role_hierarchy.get(membership.role, 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return user_level >= required_level
    
    return True


def get_user_tenant_role(user, tenant):
    """Get user's role in a specific tenant"""
    if not user or not user.is_authenticated:
        return None
    
    if user.is_superuser:
        return 'superuser'
    
    membership = user.memberships.filter(
        tenant=tenant,
        is_active=True
    ).first()
    
    return membership.role if membership else None


def filter_objects_by_tenant_permission(queryset, user, tenant):
    """Filter objects based on user's tenant permissions"""
    if not user or not user.is_authenticated:
        return queryset.none()
    
    if user.is_superuser:
        return queryset.filter(tenant=tenant)
    
    role = get_user_tenant_role(user, tenant)
    
    if not role:
        return queryset.none()
    
    # Filter based on role
    if role in ['owner', 'admin', 'manager']:
        # Can see all objects in tenant
        return queryset.filter(tenant=tenant)
    elif role == 'user':
        # Can see assigned objects or unassigned
        if hasattr(queryset.model, 'assigned_to'):
            return queryset.filter(
                tenant=tenant
            ).filter(
                Q(assigned_to=user) | Q(assigned_to__isnull=True)
            )
        else:
            # For objects without assignment, show all
            return queryset.filter(tenant=tenant)
    else:
        # Read-only access
        return queryset.filter(tenant=tenant)