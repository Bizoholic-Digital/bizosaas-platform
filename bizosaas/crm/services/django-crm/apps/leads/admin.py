"""
Django admin configuration for leads app
"""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone
from .models import (
    LeadSource, LeadTag, Lead, LeadActivity, 
    LeadNote, LeadCustomField, LeadCustomFieldValue
)


@admin.register(LeadSource)
class LeadSourceAdmin(admin.ModelAdmin):
    """Admin for lead sources"""
    list_display = ['name', 'tenant', 'total_leads', 'converted_leads', 'conversion_rate', 'is_active']
    list_filter = ['is_active', 'tenant', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['total_leads', 'converted_leads', 'conversion_rate', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('tenant', 'name', 'description', 'is_active')
        }),
        ('Statistics', {
            'fields': ('total_leads', 'converted_leads', 'conversion_rate'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Filter by tenant if user is not superuser"""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Filter by user's tenants
            user_tenants = request.user.tenants.all()
            qs = qs.filter(tenant__in=user_tenants)
        return qs


@admin.register(LeadTag)
class LeadTagAdmin(admin.ModelAdmin):
    """Admin for lead tags"""
    list_display = ['name', 'tenant', 'color_preview', 'lead_count', 'is_active']
    list_filter = ['is_active', 'tenant', 'created_at']
    search_fields = ['name', 'description']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('tenant', 'name', 'description', 'color', 'is_active')
        }),
    )
    
    def color_preview(self, obj):
        """Show color preview"""
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def lead_count(self, obj):
        """Count of leads with this tag"""
        return obj.leads.count()
    lead_count.short_description = 'Leads'
    
    def get_queryset(self, request):
        """Filter by tenant if user is not superuser"""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            user_tenants = request.user.tenants.all()
            qs = qs.filter(tenant__in=user_tenants)
        return qs


class LeadActivityInline(admin.TabularInline):
    """Inline admin for lead activities"""
    model = LeadActivity
    extra = 0
    readonly_fields = ['created_at']
    fields = ['activity_type', 'title', 'description', 'user', 'created_at']
    
    def get_queryset(self, request):
        """Limit to recent activities"""
        return super().get_queryset(request).order_by('-created_at')[:10]


class LeadNoteInline(admin.TabularInline):
    """Inline admin for lead notes"""
    model = LeadNote
    extra = 0
    readonly_fields = ['created_at']
    fields = ['content', 'user', 'is_private', 'created_at']


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """Admin for leads"""
    list_display = [
        'full_name', 'email', 'company', 'status', 'priority', 
        'score', 'assigned_to', 'source', 'created_at'
    ]
    list_filter = [
        'status', 'priority', 'source', 'assigned_to', 'tenant',
        'created_at', 'converted_at'
    ]
    search_fields = [
        'first_name', 'last_name', 'email', 'company', 
        'phone', 'job_title'
    ]
    readonly_fields = [
        'score', 'score_factors', 'last_scored_at', 'days_since_created',
        'created_at', 'updated_at'
    ]
    raw_id_fields = ['assigned_to', 'source']
    filter_horizontal = ['tags']
    
    fieldsets = (
        ('Contact Information', {
            'fields': (
                'tenant', 'first_name', 'last_name', 'email', 'phone'
            )
        }),
        ('Company Information', {
            'fields': (
                'company', 'job_title', 'company_website', 'company_size',
                'industry', 'annual_revenue'
            )
        }),
        ('Lead Management', {
            'fields': (
                'status', 'priority', 'source', 'assigned_to', 'tags'
            )
        }),
        ('AI Scoring', {
            'fields': (
                'score', 'score_factors', 'last_scored_at'
            ),
            'classes': ('collapse',)
        }),
        ('Qualification', {
            'fields': (
                'budget', 'timeline', 'decision_maker', 
                'pain_points', 'requirements'
            ),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': (
                'first_contact_date', 'last_contact_date', 'next_follow_up',
                'converted_at', 'conversion_value', 'lost_reason'
            ),
            'classes': ('collapse',)
        }),
        ('Marketing', {
            'fields': (
                'utm_source', 'utm_medium', 'utm_campaign', 
                'utm_term', 'utm_content', 'referrer'
            ),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('days_since_created', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [LeadActivityInline, LeadNoteInline]
    
    actions = ['update_scores', 'mark_as_contacted', 'assign_to_me']
    
    def days_since_created(self, obj):
        """Show days since lead creation"""
        return obj.days_since_created
    days_since_created.short_description = 'Days Old'
    
    def update_scores(self, request, queryset):
        """Action to update AI scores for selected leads"""
        count = 0
        for lead in queryset:
            lead.update_score()
            count += 1
        
        self.message_user(
            request, 
            f"Updated AI scores for {count} leads."
        )
    update_scores.short_description = "Update AI scores"
    
    def mark_as_contacted(self, request, queryset):
        """Action to mark leads as contacted"""
        count = 0
        for lead in queryset.filter(status='new'):
            lead.mark_as_contacted(request.user)
            count += 1
        
        self.message_user(
            request, 
            f"Marked {count} leads as contacted."
        )
    mark_as_contacted.short_description = "Mark as contacted"
    
    def assign_to_me(self, request, queryset):
        """Action to assign leads to current user"""
        count = queryset.update(assigned_to=request.user)
        self.message_user(
            request, 
            f"Assigned {count} leads to you."
        )
    assign_to_me.short_description = "Assign to me"
    
    def get_queryset(self, request):
        """Filter by tenant if user is not superuser"""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            user_tenants = request.user.tenants.all()
            qs = qs.filter(tenant__in=user_tenants)
        return qs
    
    def save_model(self, request, obj, form, change):
        """Auto-update score when saving"""
        super().save_model(request, obj, form, change)
        if not change or 'score' not in form.changed_data:
            obj.update_score()


@admin.register(LeadActivity)
class LeadActivityAdmin(admin.ModelAdmin):
    """Admin for lead activities"""
    list_display = [
        'lead', 'activity_type', 'user', 'title', 
        'is_completed', 'created_at'
    ]
    list_filter = [
        'activity_type', 'is_completed', 'tenant', 
        'created_at', 'scheduled_at'
    ]
    search_fields = ['lead__first_name', 'lead__last_name', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['lead', 'user']
    
    fieldsets = (
        ('Activity Information', {
            'fields': (
                'tenant', 'lead', 'user', 'activity_type', 
                'title', 'description'
            )
        }),
        ('Scheduling', {
            'fields': ('scheduled_at', 'is_completed'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Filter by tenant if user is not superuser"""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            user_tenants = request.user.tenants.all()
            qs = qs.filter(tenant__in=user_tenants)
        return qs


@admin.register(LeadNote)
class LeadNoteAdmin(admin.ModelAdmin):
    """Admin for lead notes"""
    list_display = ['lead', 'user', 'content_preview', 'is_private', 'created_at']
    list_filter = ['is_private', 'tenant', 'created_at']
    search_fields = ['lead__first_name', 'lead__last_name', 'content']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['lead', 'user']
    
    def content_preview(self, obj):
        """Show content preview"""
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'
    
    def get_queryset(self, request):
        """Filter by tenant if user is not superuser"""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            user_tenants = request.user.tenants.all()
            qs = qs.filter(tenant__in=user_tenants)
        return qs


@admin.register(LeadCustomField)
class LeadCustomFieldAdmin(admin.ModelAdmin):
    """Admin for lead custom fields"""
    list_display = ['name', 'tenant', 'field_type', 'is_required', 'order', 'is_active']
    list_filter = ['field_type', 'is_required', 'is_active', 'tenant']
    search_fields = ['name', 'help_text']
    ordering = ['tenant', 'order', 'name']
    
    fieldsets = (
        ('Field Information', {
            'fields': (
                'tenant', 'name', 'field_type', 'help_text',
                'is_required', 'is_active', 'order'
            )
        }),
        ('Field Options', {
            'fields': ('default_value', 'options'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Filter by tenant if user is not superuser"""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            user_tenants = request.user.tenants.all()
            qs = qs.filter(tenant__in=user_tenants)
        return qs


@admin.register(LeadCustomFieldValue)
class LeadCustomFieldValueAdmin(admin.ModelAdmin):
    """Admin for lead custom field values"""
    list_display = ['lead', 'custom_field', 'value_preview']
    list_filter = ['custom_field', 'tenant']
    search_fields = ['lead__first_name', 'lead__last_name', 'value']
    raw_id_fields = ['lead', 'custom_field']
    
    def value_preview(self, obj):
        """Show value preview"""
        value = obj.value
        return value[:50] + '...' if len(value) > 50 else value
    value_preview.short_description = 'Value'
    
    def get_queryset(self, request):
        """Filter by tenant if user is not superuser"""
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            user_tenants = request.user.tenants.all()
            qs = qs.filter(tenant__in=user_tenants)
        return qs