"""
Core models for Django CRM
Base models and abstractions for multi-tenant architecture
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class TimeStampedModel(models.Model):
    """Abstract model with timestamp fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Abstract model with UUID primary key"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Meta:
        abstract = True


class TenantAwareModel(models.Model):
    """Abstract model with tenant awareness"""
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='%(class)s_set'
    )
    
    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['tenant']),
        ]


class BaseModel(UUIDModel, TimeStampedModel, TenantAwareModel):
    """Base model combining UUID, timestamps, and tenant awareness"""
    
    class Meta:
        abstract = True


class UserProfile(UUIDModel, TimeStampedModel):
    """Extended user profile with CRM-specific data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='crm_profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # User preferences
    timezone = models.CharField(max_length=50, default='UTC')
    language = models.CharField(max_length=10, default='en')
    
    class Meta:
        db_table = 'crm_user_profile'
        
    def __str__(self):
        return f"{self.user.email} Profile"


class ActivityLog(BaseModel):
    """Activity logging for audit trail"""
    ACTIVITY_TYPES = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('export', 'Export'),
        ('import', 'Import'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    object_type = models.CharField(max_length=50)
    object_id = models.CharField(max_length=255)
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        db_table = 'core_activity_log'
        indexes = [
            models.Index(fields=['tenant', 'user']),
            models.Index(fields=['tenant', 'activity_type']),
            models.Index(fields=['tenant', 'object_type']),
            models.Index(fields=['created_at']),
        ]
        
    def __str__(self):
        return f"{self.user.email} - {self.activity_type} {self.object_type}"


class SystemSetting(models.Model):
    """System-wide settings"""
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'core_system_setting'
        
    def __str__(self):
        return self.key


class TenantSetting(BaseModel):
    """Tenant-specific settings"""
    key = models.CharField(max_length=100)
    value = models.JSONField()
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'core_tenant_setting'
        unique_together = [['tenant', 'key']]
        
    def __str__(self):
        return f"{self.tenant.name} - {self.key}"