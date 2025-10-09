"""
Multi-tenant managers for Saleor models
Provides automatic organization filtering for data isolation
"""

from django.db import models
from django.db.models import QuerySet
from django.core.exceptions import ImproperlyConfigured

from .middleware import get_current_organization_id


class OrganizationQuerySet(QuerySet):
    """
    QuerySet that automatically filters by current organization
    """
    
    def for_organization(self, organization):
        """Filter queryset by specific organization"""
        if hasattr(organization, 'id'):
            organization_id = organization.id
        else:
            organization_id = organization
        
        return self.filter(organization_id=organization_id)
    
    def for_current_organization(self):
        """Filter queryset by current organization from thread-local storage"""
        organization_id = get_current_organization_id()
        if not organization_id:
            # In development/testing, allow queries without organization context
            # In production, you might want to raise an exception
            return self.none()
        
        return self.filter(organization_id=organization_id)


class OrganizationManager(models.Manager):
    """
    Manager that automatically filters by current organization
    """
    
    def get_queryset(self):
        """Return queryset filtered by current organization"""
        return OrganizationQuerySet(self.model, using=self._db).for_current_organization()
    
    def all_organizations(self):
        """Get objects from all organizations (bypass filtering)"""
        return OrganizationQuerySet(self.model, using=self._db)
    
    def for_organization(self, organization):
        """Get objects for specific organization"""
        return OrganizationQuerySet(self.model, using=self._db).for_organization(organization)


class PublicManager(models.Manager):
    """
    Manager for models that don't require organization filtering
    (public/shared data)
    """
    
    def get_queryset(self):
        """Return unfiltered queryset"""
        return super().get_queryset()


class OrganizationAwareModelMixin:
    """
    Mixin for models that should be organization-aware
    """
    
    def save(self, *args, **kwargs):
        """Auto-set organization on save if not already set"""
        if hasattr(self, 'organization_id') and not self.organization_id:
            organization_id = get_current_organization_id()
            if organization_id:
                self.organization_id = organization_id
            else:
                # In some cases you might want to require organization context
                # raise ImproperlyConfigured("Organization context required for saving this model")
                pass
        
        super().save(*args, **kwargs)


def make_organization_aware(model_class):
    """
    Decorator/function to make a model organization-aware by adding organization field and manager
    """
    if not hasattr(model_class, 'organization'):
        # Add organization field if not already present
        from .models import Organization
        
        organization_field = models.ForeignKey(
            Organization,
            on_delete=models.CASCADE,
            related_name=f"{model_class._meta.model_name}_set",
            null=True,  # Allow null for existing data migration
            blank=True,
            help_text=f"Organization that owns this {model_class._meta.verbose_name}"
        )
        
        model_class.add_to_class('organization', organization_field)
    
    # Add organization-aware manager
    if not hasattr(model_class, 'organization_objects'):
        model_class.add_to_class('organization_objects', OrganizationManager())
    
    # Add mixin methods if not already present
    if not issubclass(model_class, OrganizationAwareModelMixin):
        # Add mixin methods to the class
        original_save = model_class.save
        
        def organization_aware_save(self, *args, **kwargs):
            # Auto-set organization on save if not already set
            if hasattr(self, 'organization_id') and not self.organization_id:
                organization_id = get_current_organization_id()
                if organization_id:
                    self.organization_id = organization_id
            
            return original_save(self, *args, **kwargs)
        
        model_class.save = organization_aware_save
    
    return model_class