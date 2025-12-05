"""
Tenant models for multi-tenant Django CRM
"""
from django.db import models
from django.contrib.auth.models import User
from apps.core.models import UUIDModel, TimeStampedModel
import uuid


class Tenant(UUIDModel, TimeStampedModel):
    """Multi-tenant organization model"""
    SUBSCRIPTION_TIERS = (
        ('free', 'Free'),
        ('starter', 'Starter'),
        ('professional', 'Professional'),
        ('enterprise', 'Enterprise'),
    )
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField(blank=True)
    
    # Contact information
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Address
    address_line1 = models.CharField(max_length=200, blank=True)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Subscription and billing
    subscription_tier = models.CharField(max_length=20, choices=SUBSCRIPTION_TIERS, default='free')
    subscription_status = models.CharField(max_length=20, default='active')
    billing_email = models.EmailField(blank=True)
    
    # Settings
    timezone = models.CharField(max_length=50, default='UTC')
    currency = models.CharField(max_length=3, default='USD')
    language = models.CharField(max_length=10, default='en')
    
    # Status
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    
    # Limits
    max_users = models.IntegerField(default=5)
    max_leads = models.IntegerField(default=1000)
    max_customers = models.IntegerField(default=500)
    max_storage_mb = models.IntegerField(default=100)  # MB
    
    # Integration settings
    integrations_config = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'tenants_tenant'
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    @property
    def current_users_count(self):
        """Get current active users count"""
        return self.memberships.filter(is_active=True).count()
    
    @property
    def storage_used_mb(self):
        """Calculate storage usage in MB"""
        # TODO: Implement actual storage calculation
        return 0


class Domain(UUIDModel, TimeStampedModel):
    """Custom domains for tenants"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='domains')
    domain = models.CharField(max_length=255, unique=True)
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    ssl_enabled = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'tenants_domain'
        unique_together = [['tenant', 'is_primary']]
        
    def __str__(self):
        return f"{self.domain} ({'Primary' if self.is_primary else 'Secondary'})"


class TenantMembership(UUIDModel, TimeStampedModel):
    """User membership in tenants"""
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
        ('readonly', 'Read Only'),
    )
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    
    # Status
    is_active = models.BooleanField(default=True)
    invited_at = models.DateTimeField(auto_now_add=True)
    joined_at = models.DateTimeField(null=True, blank=True)
    
    # Permissions
    permissions = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'tenants_membership'
        unique_together = [['tenant', 'user']]
        
    def __str__(self):
        return f"{self.user.email} - {self.tenant.name} ({self.role})"
    
    def has_permission(self, permission):
        """Check if membership has specific permission"""
        return permission in self.permissions.get('custom', [])


class TenantInvitation(UUIDModel, TimeStampedModel):
    """Invitations to join tenants"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='invitations')
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=TenantMembership.ROLE_CHOICES, default='user')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Status
    is_accepted = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)
    
    # Invitation token
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    
    class Meta:
        db_table = 'tenants_invitation'
        unique_together = [['tenant', 'email']]
        
    def __str__(self):
        return f"Invite {self.email} to {self.tenant.name}"


class TenantAPIKey(UUIDModel, TimeStampedModel):
    """API keys for tenant integrations"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=100)
    key_hash = models.CharField(max_length=128, unique=True)  # Hashed API key
    
    # Permissions
    permissions = models.JSONField(default=list, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Usage tracking
    usage_count = models.IntegerField(default=0)
    rate_limit = models.IntegerField(default=1000)  # requests per hour
    
    class Meta:
        db_table = 'tenants_api_key'
        
    def __str__(self):
        return f"{self.tenant.name} - {self.name}"


class TenantAuditLog(UUIDModel, TimeStampedModel):
    """Audit log for tenant-level activities"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='audit_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    action = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=50)
    resource_id = models.CharField(max_length=255, blank=True)
    
    # Details
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    
    # Request info
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        db_table = 'tenants_audit_log'
        indexes = [
            models.Index(fields=['tenant', 'action']),
            models.Index(fields=['tenant', 'resource_type']),
            models.Index(fields=['created_at']),
        ]
        
    def __str__(self):
        return f"{self.tenant.name} - {self.action}"