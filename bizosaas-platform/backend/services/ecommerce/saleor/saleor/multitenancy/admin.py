"""
Django admin interface for multi-tenancy models
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Organization, OrganizationMember, OrganizationInvitation, OrganizationSettings


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin interface for Organization model"""
    
    list_display = [
        'name', 'slug', 'domain', 'subscription_tier', 
        'is_active', 'member_count', 'created_at'
    ]
    list_filter = ['subscription_tier', 'is_active', 'created_at']
    search_fields = ['name', 'slug', 'domain', 'bizosaas_tenant_id']
    readonly_fields = ['id', 'created_at', 'updated_at', 'member_count', 'settings_link']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'domain', 'subdomain', 'is_active')
        }),
        ('Integration', {
            'fields': ('bizosaas_tenant_id', 'site')
        }),
        ('Subscription', {
            'fields': ('subscription_tier', 'max_products', 'max_orders_per_month', 
                      'max_staff_users', 'storage_limit_gb')
        }),
        ('Branding', {
            'fields': ('logo', 'primary_color', 'secondary_color'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('settings', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Links', {
            'fields': ('member_count', 'settings_link'),
            'classes': ('collapse',)
        })
    )
    
    def member_count(self, obj):
        """Get member count for organization"""
        count = obj.members.filter(is_active=True).count()
        url = reverse('admin:multitenancy_organizationmember_changelist') + f'?organization__id__exact={obj.id}'
        return format_html('<a href="{}">{} members</a>', url, count)
    member_count.short_description = 'Active Members'
    
    def settings_link(self, obj):
        """Link to organization settings"""
        try:
            settings = obj.extended_settings
            url = reverse('admin:multitenancy_organizationsettings_change', args=[settings.id])
            return format_html('<a href="{}">View Settings</a>', url)
        except OrganizationSettings.DoesNotExist:
            url = reverse('admin:multitenancy_organizationsettings_add') + f'?organization={obj.id}'
            return format_html('<a href="{}">Create Settings</a>', url)
    settings_link.short_description = 'Settings'


class OrganizationMemberInline(admin.TabularInline):
    """Inline admin for organization members"""
    model = OrganizationMember
    extra = 0
    fields = ['user', 'role', 'is_active', 'joined_at']
    readonly_fields = ['joined_at']


@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    """Admin interface for OrganizationMember model"""
    
    list_display = ['user', 'organization', 'role', 'is_active', 'joined_at']
    list_filter = ['role', 'is_active', 'joined_at', 'organization__subscription_tier']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'organization__name']
    readonly_fields = ['joined_at', 'updated_at']
    
    fieldsets = (
        ('Membership', {
            'fields': ('organization', 'user', 'role', 'is_active')
        }),
        ('Invitation', {
            'fields': ('invited_by', 'invitation_accepted_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('joined_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(OrganizationInvitation)
class OrganizationInvitationAdmin(admin.ModelAdmin):
    """Admin interface for OrganizationInvitation model"""
    
    list_display = ['email', 'organization', 'role', 'is_accepted', 'is_expired', 'created_at']
    list_filter = ['role', 'is_accepted', 'is_expired', 'created_at']
    search_fields = ['email', 'organization__name', 'invited_by__email']
    readonly_fields = ['token', 'created_at', 'accepted_at', 'accepted_by', 'is_valid_status']
    
    fieldsets = (
        ('Invitation Details', {
            'fields': ('organization', 'email', 'role', 'invited_by')
        }),
        ('Status', {
            'fields': ('is_accepted', 'is_expired', 'is_valid_status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'expires_at', 'accepted_at', 'accepted_by'),
            'classes': ('collapse',)
        }),
        ('Token', {
            'fields': ('token',),
            'classes': ('collapse',)
        })
    )
    
    def is_valid_status(self, obj):
        """Show if invitation is valid"""
        if obj.is_valid:
            return format_html('<span style="color: green;">✓ Valid</span>')
        else:
            return format_html('<span style="color: red;">✗ Invalid</span>')
    is_valid_status.short_description = 'Valid'


@admin.register(OrganizationSettings)
class OrganizationSettingsAdmin(admin.ModelAdmin):
    """Admin interface for OrganizationSettings model"""
    
    list_display = ['organization', 'currency', 'tax_calculation', 'inventory_tracking', 'updated_at']
    list_filter = ['currency', 'tax_calculation', 'inventory_tracking', 'guest_checkout_enabled']
    search_fields = ['organization__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Organization', {
            'fields': ('organization',)
        }),
        ('E-commerce Settings', {
            'fields': ('currency', 'tax_calculation', 'inventory_tracking',
                      'free_shipping_threshold', 'default_shipping_zone')
        }),
        ('Checkout Settings', {
            'fields': ('guest_checkout_enabled', 'account_required'),
            'classes': ('collapse',)
        }),
        ('Email Settings', {
            'fields': ('order_confirmation_email', 'shipping_confirmation_email'),
            'classes': ('collapse',)
        }),
        ('Analytics', {
            'fields': ('google_analytics_id', 'facebook_pixel_id'),
            'classes': ('collapse',)
        }),
        ('API & Integration Settings', {
            'fields': ('api_settings', 'webhook_settings'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_form(self, request, obj=None, **kwargs):
        """Customize form display"""
        form = super().get_form(request, obj, **kwargs)
        
        # Add help text for JSON fields
        form.base_fields['api_settings'].help_text = (
            'API configuration in JSON format. Example: '
            '{"rate_limit": 1000, "allowed_origins": ["https://example.com"]}'
        )
        form.base_fields['webhook_settings'].help_text = (
            'Webhook configuration in JSON format. Example: '
            '{"enabled": true, "endpoints": ["https://webhook.example.com"]}'
        )
        
        return form