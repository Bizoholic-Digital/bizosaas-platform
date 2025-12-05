"""
Multi-tenant organization models for Saleor
Provides organization-based isolation for BizOSaaS platform integration
"""

import uuid
from django.db import models
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from ..core.models import ModelWithMetadata
from ..account.models import User


class Organization(ModelWithMetadata):
    """
    Organization model for multi-tenant isolation in Saleor
    Each organization represents a separate BizOSaaS tenant with isolated data
    """
    
    # Core identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Organization display name")
    slug = models.SlugField(max_length=100, unique=True, help_text="URL-safe organization identifier")
    
    # BizOSaaS Integration
    bizosaas_tenant_id = models.CharField(
        max_length=100,
        unique=True,
        help_text="Corresponding tenant ID in BizOSaaS platform"
    )
    
    # Domain configuration
    domain = models.CharField(
        max_length=255,
        unique=True,
        help_text="Primary domain for this organization"
    )
    subdomain = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Subdomain for multi-tenant routing (e.g., 'client1' for client1.bizosaas.com)"
    )
    
    # Site relationship for Saleor
    site = models.OneToOneField(
        Site,
        on_delete=models.CASCADE,
        related_name='organization',
        null=True,
        blank=True,
        help_text="Associated Django Site for this organization"
    )
    
    # Organization settings
    is_active = models.BooleanField(default=True, help_text="Whether organization is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Subscription tier (matches BizOSaaS pricing)
    TIER_CHOICES = [
        ('tier_1', 'Marketing Starter ($97/month)'),
        ('tier_2', 'Growth Accelerator ($297/month)'),
        ('tier_3', 'Enterprise Scale ($997/month)'),
    ]
    subscription_tier = models.CharField(
        max_length=20,
        choices=TIER_CHOICES,
        default='tier_1',
        help_text="Subscription tier determining feature access"
    )
    
    # Organization configuration
    settings = models.JSONField(
        default=dict,
        help_text="Organization-specific settings and configuration"
    )
    
    # Branding and appearance
    logo = models.ImageField(upload_to='organization-logos/', null=True, blank=True)
    primary_color = models.CharField(max_length=7, default='#007cba', help_text="Primary brand color (hex)")
    secondary_color = models.CharField(max_length=7, default='#6c757d', help_text="Secondary brand color (hex)")
    
    # Limits and quotas based on subscription tier
    max_products = models.PositiveIntegerField(default=100, help_text="Maximum products allowed")
    max_orders_per_month = models.PositiveIntegerField(default=1000, help_text="Maximum orders per month")
    max_staff_users = models.PositiveIntegerField(default=5, help_text="Maximum staff users")
    storage_limit_gb = models.PositiveIntegerField(default=10, help_text="Storage limit in GB")
    
    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        ordering = ['name']
        indexes = [
            models.Index(fields=['domain'], name='org_domain_idx'),
            models.Index(fields=['bizosaas_tenant_id'], name='org_bizosaas_tenant_idx'),
            models.Index(fields=['is_active'], name='org_is_active_idx'),
            models.Index(fields=['subscription_tier'], name='org_tier_idx'),
        ]

    def __str__(self):
        return self.name

    @property
    def full_domain(self):
        """Get the full domain for this organization"""
        if self.subdomain:
            return f"{self.subdomain}.{self.domain}"
        return self.domain
    
    @property
    def tier_limits(self):
        """Get limits based on subscription tier"""
        tier_configs = {
            'tier_1': {
                'max_products': 100,
                'max_orders_per_month': 1000,
                'max_staff_users': 5,
                'storage_limit_gb': 10,
                'features': ['basic_ecommerce', 'basic_cms', 'basic_crm']
            },
            'tier_2': {
                'max_products': 1000,
                'max_orders_per_month': 10000,
                'max_staff_users': 20,
                'storage_limit_gb': 100,
                'features': ['advanced_ecommerce', 'advanced_cms', 'advanced_crm', 'ai_agents', 'analytics']
            },
            'tier_3': {
                'max_products': -1,  # Unlimited
                'max_orders_per_month': -1,  # Unlimited
                'max_staff_users': -1,  # Unlimited
                'storage_limit_gb': 1000,
                'features': ['full_platform', 'premium_support', 'custom_integrations', 'white_label']
            }
        }
        return tier_configs.get(self.subscription_tier, tier_configs['tier_1'])
    
    def has_feature(self, feature_name: str) -> bool:
        """Check if organization has access to a specific feature"""
        return feature_name in self.tier_limits.get('features', [])
    
    def can_add_product(self) -> bool:
        """Check if organization can add more products"""
        max_products = self.tier_limits['max_products']
        if max_products == -1:  # Unlimited
            return True
        
        from ..product.models import Product
        current_count = Product.objects.filter(
            organization=self
        ).count()
        return current_count < max_products
    
    def can_add_staff_user(self) -> bool:
        """Check if organization can add more staff users"""
        max_staff = self.tier_limits['max_staff_users']
        if max_staff == -1:  # Unlimited
            return True
        
        current_count = OrganizationMember.objects.filter(
            organization=self,
            role__in=['admin', 'staff']
        ).count()
        return current_count < max_staff


class OrganizationMember(models.Model):
    """
    Relationship between Users and Organizations
    Manages user access and roles within organizations
    """
    
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organization_memberships'
    )
    
    # Role within the organization
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Administrator'),
        ('staff', 'Staff Member'),
        ('viewer', 'Viewer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    
    # Membership status
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Invitation system
    invited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_invitations'
    )
    invitation_accepted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['organization', 'user']
        verbose_name = _("Organization Member")
        verbose_name_plural = _("Organization Members")
        indexes = [
            models.Index(fields=['organization', 'role'], name='org_member_org_role_idx'),
            models.Index(fields=['user'], name='org_member_user_idx'),
            models.Index(fields=['is_active'], name='org_member_active_idx'),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.organization.name} ({self.role})"
    
    @property
    def can_manage_organization(self) -> bool:
        """Check if user can manage organization settings"""
        return self.role in ['owner', 'admin']
    
    @property
    def can_manage_users(self) -> bool:
        """Check if user can manage other users"""
        return self.role in ['owner', 'admin']
    
    @property
    def can_manage_products(self) -> bool:
        """Check if user can manage products"""
        return self.role in ['owner', 'admin', 'staff']
    
    @property
    def permissions_for_role(self):
        """Get permissions based on role"""
        role_permissions = {
            'owner': ['manage_organization', 'manage_users', 'manage_products', 'manage_orders', 'view_analytics'],
            'admin': ['manage_users', 'manage_products', 'manage_orders', 'view_analytics'],
            'staff': ['manage_products', 'manage_orders', 'view_basic_analytics'],
            'viewer': ['view_products', 'view_orders'],
        }
        return role_permissions.get(self.role, [])


class OrganizationInvitation(models.Model):
    """
    Invitation system for adding users to organizations
    """
    
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    email = models.EmailField(help_text="Email address of the invited user")
    role = models.CharField(
        max_length=20,
        choices=OrganizationMember.ROLE_CHOICES,
        default='staff'
    )
    
    invited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_org_invitations'
    )
    
    # Invitation token and status
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    is_accepted = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)
    accepted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_org_invitations'
    )
    
    class Meta:
        unique_together = ['organization', 'email']
        verbose_name = _("Organization Invitation")
        verbose_name_plural = _("Organization Invitations")
        indexes = [
            models.Index(fields=['token'], name='org_invite_token_idx'),
            models.Index(fields=['email'], name='org_invite_email_idx'),
            models.Index(fields=['is_accepted'], name='org_invite_accepted_idx'),
            models.Index(fields=['expires_at'], name='org_invite_expires_idx'),
        ]

    def __str__(self):
        return f"Invitation for {self.email} to {self.organization.name}"
    
    @property
    def is_valid(self) -> bool:
        """Check if invitation is still valid"""
        from django.utils import timezone
        return not self.is_accepted and not self.is_expired and self.expires_at > timezone.now()


class OrganizationSettings(models.Model):
    """
    Extended settings for organizations
    Allows for flexible configuration per organization
    """
    
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        related_name='extended_settings'
    )
    
    # E-commerce settings
    currency = models.CharField(max_length=3, default='USD', help_text="Default currency code")
    tax_calculation = models.BooleanField(default=True, help_text="Enable automatic tax calculation")
    inventory_tracking = models.BooleanField(default=True, help_text="Track inventory levels")
    
    # Shipping settings
    default_shipping_zone = models.CharField(max_length=100, blank=True)
    free_shipping_threshold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Checkout settings
    guest_checkout_enabled = models.BooleanField(default=True)
    account_required = models.BooleanField(default=False)
    
    # Email settings
    order_confirmation_email = models.BooleanField(default=True)
    shipping_confirmation_email = models.BooleanField(default=True)
    
    # Analytics and tracking
    google_analytics_id = models.CharField(max_length=50, blank=True)
    facebook_pixel_id = models.CharField(max_length=50, blank=True)
    
    # API and integration settings
    api_settings = models.JSONField(default=dict, help_text="API configuration and keys")
    webhook_settings = models.JSONField(default=dict, help_text="Webhook configuration")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Organization Settings")
        verbose_name_plural = _("Organization Settings")

    def __str__(self):
        return f"Settings for {self.organization.name}"