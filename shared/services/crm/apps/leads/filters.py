"""
Filters for leads app
Django Filter integration for advanced filtering
"""
import django_filters
from django.db.models import Q
from django.utils import timezone
from .models import Lead, LeadSource, LeadTag
from datetime import timedelta


class LeadFilter(django_filters.FilterSet):
    """Advanced filtering for leads"""
    
    # Basic filters
    status = django_filters.MultipleChoiceFilter(choices=Lead.STATUS_CHOICES)
    priority = django_filters.MultipleChoiceFilter(choices=Lead.PRIORITY_CHOICES)
    
    # Relationship filters
    source = django_filters.ModelMultipleChoiceFilter(
        field_name='source',
        queryset=LeadSource.objects.none(),  # Will be set in __init__
        to_field_name='id'
    )
    assigned_to = django_filters.UUIDFilter(field_name='assigned_to__id')
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags',
        queryset=LeadTag.objects.none(),  # Will be set in __init__
        to_field_name='id'
    )
    
    # Score filters
    score_min = django_filters.NumberFilter(field_name='score', lookup_expr='gte')
    score_max = django_filters.NumberFilter(field_name='score', lookup_expr='lte')
    score_range = django_filters.RangeFilter(field_name='score')
    
    # Budget filters
    budget_min = django_filters.NumberFilter(field_name='budget', lookup_expr='gte')
    budget_max = django_filters.NumberFilter(field_name='budget', lookup_expr='lte')
    budget_range = django_filters.RangeFilter(field_name='budget')
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    created_date_range = django_filters.DateFromToRangeFilter(field_name='created_at')
    
    # Contact filters
    contacted_after = django_filters.DateTimeFilter(field_name='last_contact_date', lookup_expr='gte')
    contacted_before = django_filters.DateTimeFilter(field_name='last_contact_date', lookup_expr='lte')
    
    # Company filters
    company_size = django_filters.MultipleChoiceFilter(
        choices=[
            ('startup', 'Startup'),
            ('small', 'Small'),
            ('medium', 'Medium'),
            ('large', 'Large'),
            ('enterprise', 'Enterprise'),
        ]
    )
    industry = django_filters.CharFilter(lookup_expr='icontains')
    
    # Boolean filters
    decision_maker = django_filters.BooleanFilter()
    has_budget = django_filters.BooleanFilter(
        method='filter_has_budget',
        label='Has Budget Information'
    )
    has_phone = django_filters.BooleanFilter(
        method='filter_has_phone',
        label='Has Phone Number'
    )
    is_assigned = django_filters.BooleanFilter(
        method='filter_is_assigned',
        label='Is Assigned'
    )
    is_overdue = django_filters.BooleanFilter(
        method='filter_is_overdue',
        label='Follow-up Overdue'
    )
    
    # Timeline filters
    timeline_urgent = django_filters.BooleanFilter(
        method='filter_timeline_urgent',
        label='Urgent Timeline'
    )
    
    # Custom date filters
    created_today = django_filters.BooleanFilter(
        method='filter_created_today',
        label='Created Today'
    )
    created_this_week = django_filters.BooleanFilter(
        method='filter_created_this_week',
        label='Created This Week'
    )
    created_this_month = django_filters.BooleanFilter(
        method='filter_created_this_month',
        label='Created This Month'
    )
    
    # Activity filters
    no_activity_days = django_filters.NumberFilter(
        method='filter_no_activity_days',
        label='No Activity for X Days'
    )
    
    # Marketing filters
    utm_source = django_filters.CharFilter(lookup_expr='icontains')
    utm_medium = django_filters.CharFilter(lookup_expr='icontains')
    utm_campaign = django_filters.CharFilter(lookup_expr='icontains')
    
    # Text search across multiple fields
    search = django_filters.CharFilter(
        method='filter_search',
        label='Search'
    )
    
    class Meta:
        model = Lead
        fields = {
            'email': ['exact', 'icontains'],
            'phone': ['exact', 'icontains'],
            'company': ['exact', 'icontains'],
            'job_title': ['exact', 'icontains'],
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize filter with tenant-specific querysets"""
        super().__init__(*args, **kwargs)
        
        # Get tenant from request
        request = kwargs.get('request')
        if request and hasattr(request, 'tenant'):
            tenant = request.tenant
            
            # Set tenant-specific querysets
            self.filters['source'].queryset = LeadSource.objects.filter(
                tenant=tenant, is_active=True
            )
            self.filters['tags'].queryset = LeadTag.objects.filter(
                tenant=tenant, is_active=True
            )
    
    def filter_has_budget(self, queryset, name, value):
        """Filter leads with/without budget information"""
        if value:
            return queryset.filter(budget__isnull=False, budget__gt=0)
        return queryset.filter(Q(budget__isnull=True) | Q(budget=0))
    
    def filter_has_phone(self, queryset, name, value):
        """Filter leads with/without phone number"""
        if value:
            return queryset.exclude(phone='')
        return queryset.filter(phone='')
    
    def filter_is_assigned(self, queryset, name, value):
        """Filter assigned/unassigned leads"""
        if value:
            return queryset.filter(assigned_to__isnull=False)
        return queryset.filter(assigned_to__isnull=True)
    
    def filter_is_overdue(self, queryset, name, value):
        """Filter overdue follow-ups"""
        now = timezone.now()
        if value:
            return queryset.filter(
                next_follow_up__lt=now,
                status__in=['new', 'contacted', 'qualified', 'proposal', 'negotiation']
            )
        return queryset.filter(
            Q(next_follow_up__isnull=True) |
            Q(next_follow_up__gte=now) |
            Q(status__in=['converted', 'lost', 'unresponsive'])
        )
    
    def filter_timeline_urgent(self, queryset, name, value):
        """Filter leads with urgent timeline"""
        if value:
            return queryset.filter(
                Q(timeline__icontains='immediate') |
                Q(timeline__icontains='urgent') |
                Q(timeline__icontains='asap')
            )
        return queryset.exclude(
            Q(timeline__icontains='immediate') |
            Q(timeline__icontains='urgent') |
            Q(timeline__icontains='asap')
        )
    
    def filter_created_today(self, queryset, name, value):
        """Filter leads created today"""
        if value:
            today = timezone.now().date()
            return queryset.filter(created_at__date=today)
        return queryset.exclude(created_at__date=timezone.now().date())
    
    def filter_created_this_week(self, queryset, name, value):
        """Filter leads created this week"""
        if value:
            week_start = timezone.now() - timedelta(days=7)
            return queryset.filter(created_at__gte=week_start)
        return queryset.exclude(created_at__gte=timezone.now() - timedelta(days=7))
    
    def filter_created_this_month(self, queryset, name, value):
        """Filter leads created this month"""
        if value:
            month_start = timezone.now() - timedelta(days=30)
            return queryset.filter(created_at__gte=month_start)
        return queryset.exclude(created_at__gte=timezone.now() - timedelta(days=30))
    
    def filter_no_activity_days(self, queryset, name, value):
        """Filter leads with no activity for X days"""
        if value:
            cutoff_date = timezone.now() - timedelta(days=value)
            return queryset.filter(
                Q(last_contact_date__isnull=True) |
                Q(last_contact_date__lt=cutoff_date)
            )
        return queryset
    
    def filter_search(self, queryset, name, value):
        """Full-text search across multiple fields"""
        if value:
            search_query = (
                Q(first_name__icontains=value) |
                Q(last_name__icontains=value) |
                Q(email__icontains=value) |
                Q(phone__icontains=value) |
                Q(company__icontains=value) |
                Q(job_title__icontains=value) |
                Q(notes__icontains=value) |
                Q(pain_points__icontains=value) |
                Q(requirements__icontains=value)
            )
            return queryset.filter(search_query)
        return queryset


class LeadSourceFilter(django_filters.FilterSet):
    """Filter for lead sources"""
    
    name = django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()
    
    # Performance filters
    conversion_rate_min = django_filters.NumberFilter(
        field_name='conversion_rate', 
        lookup_expr='gte'
    )
    conversion_rate_max = django_filters.NumberFilter(
        field_name='conversion_rate', 
        lookup_expr='lte'
    )
    
    total_leads_min = django_filters.NumberFilter(
        field_name='total_leads', 
        lookup_expr='gte'
    )
    total_leads_max = django_filters.NumberFilter(
        field_name='total_leads', 
        lookup_expr='lte'
    )
    
    class Meta:
        model = LeadSource
        fields = ['name', 'is_active']


class LeadTagFilter(django_filters.FilterSet):
    """Filter for lead tags"""
    
    name = django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()
    color = django_filters.CharFilter()
    
    class Meta:
        model = LeadTag
        fields = ['name', 'is_active', 'color']