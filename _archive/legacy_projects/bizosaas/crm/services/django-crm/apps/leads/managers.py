"""
Custom managers for leads app
Query optimization and common filters
"""
from django.db import models
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta


class LeadSourceManager(models.Manager):
    """Manager for LeadSource model"""
    
    def active(self):
        """Get active lead sources"""
        return self.filter(is_active=True)
    
    def with_stats(self):
        """Get sources with lead statistics"""
        return self.annotate(
            total_leads_count=Count('leads'),
            converted_leads_count=Count(
                'leads',
                filter=Q(leads__status='converted')
            ),
            avg_lead_score=Avg('leads__score')
        )
    
    def top_performing(self, limit=10):
        """Get top performing sources by conversion rate"""
        return self.with_stats().filter(
            total_leads_count__gt=0
        ).order_by('-conversion_rate', '-total_leads_count')[:limit]


class LeadTagManager(models.Manager):
    """Manager for LeadTag model"""
    
    def active(self):
        """Get active tags"""
        return self.filter(is_active=True)
    
    def with_counts(self):
        """Get tags with lead counts"""
        return self.annotate(
            leads_count=Count('leads')
        )
    
    def popular(self, limit=20):
        """Get most popular tags"""
        return self.with_counts().filter(
            leads_count__gt=0
        ).order_by('-leads_count', 'name')[:limit]


class LeadQuerySet(models.QuerySet):
    """Custom queryset for Lead model"""
    
    def active(self):
        """Get active leads (not lost or unresponsive)"""
        return self.exclude(status__in=['lost', 'unresponsive'])
    
    def new(self):
        """Get new leads"""
        return self.filter(status='new')
    
    def contacted(self):
        """Get contacted leads"""
        return self.filter(status='contacted')
    
    def qualified(self):
        """Get qualified leads"""
        return self.filter(status='qualified')
    
    def converted(self):
        """Get converted leads"""
        return self.filter(status='converted')
    
    def lost(self):
        """Get lost leads"""
        return self.filter(status='lost')
    
    def high_priority(self):
        """Get high priority leads"""
        return self.filter(priority__in=['high', 'urgent'])
    
    def high_score(self, threshold=70):
        """Get high scoring leads"""
        return self.filter(score__gte=threshold)
    
    def medium_score(self, low=40, high=70):
        """Get medium scoring leads"""
        return self.filter(score__gte=low, score__lt=high)
    
    def low_score(self, threshold=40):
        """Get low scoring leads"""
        return self.filter(score__lt=threshold)
    
    def unassigned(self):
        """Get unassigned leads"""
        return self.filter(assigned_to__isnull=True)
    
    def assigned_to(self, user):
        """Get leads assigned to specific user"""
        return self.filter(assigned_to=user)
    
    def from_source(self, source):
        """Get leads from specific source"""
        return self.filter(source=source)
    
    def with_tags(self, tags):
        """Get leads with specific tags"""
        return self.filter(tags__in=tags).distinct()
    
    def has_budget(self):
        """Get leads with budget information"""
        return self.filter(budget__isnull=False, budget__gt=0)
    
    def decision_makers(self):
        """Get leads who are decision makers"""
        return self.filter(decision_maker=True)
    
    def created_recently(self, days=7):
        """Get leads created in the last N days"""
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(created_at__gte=cutoff)
    
    def created_today(self):
        """Get leads created today"""
        today = timezone.now().date()
        return self.filter(created_at__date=today)
    
    def created_this_week(self):
        """Get leads created this week"""
        return self.created_recently(days=7)
    
    def created_this_month(self):
        """Get leads created this month"""
        return self.created_recently(days=30)
    
    def overdue_followup(self):
        """Get leads with overdue follow-ups"""
        now = timezone.now()
        return self.active().filter(
            next_follow_up__lt=now,
            next_follow_up__isnull=False
        )
    
    def due_for_followup(self, days=1):
        """Get leads due for follow-up in next N days"""
        now = timezone.now()
        future = now + timedelta(days=days)
        return self.active().filter(
            next_follow_up__gte=now,
            next_follow_up__lte=future
        )
    
    def no_contact_recently(self, days=7):
        """Get leads with no contact in N days"""
        cutoff = timezone.now() - timedelta(days=days)
        return self.active().filter(
            Q(last_contact_date__isnull=True) |
            Q(last_contact_date__lt=cutoff)
        )
    
    def contacted_recently(self, days=7):
        """Get leads contacted in the last N days"""
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(last_contact_date__gte=cutoff)
    
    def with_company_size(self, size):
        """Get leads from companies of specific size"""
        return self.filter(company_size=size)
    
    def from_industry(self, industry):
        """Get leads from specific industry"""
        return self.filter(industry__icontains=industry)
    
    def with_revenue_range(self, min_revenue=None, max_revenue=None):
        """Get leads with annual revenue in range"""
        queryset = self
        if min_revenue:
            queryset = queryset.filter(annual_revenue__gte=min_revenue)
        if max_revenue:
            queryset = queryset.filter(annual_revenue__lte=max_revenue)
        return queryset
    
    def with_budget_range(self, min_budget=None, max_budget=None):
        """Get leads with budget in range"""
        queryset = self
        if min_budget:
            queryset = queryset.filter(budget__gte=min_budget)
        if max_budget:
            queryset = queryset.filter(budget__lte=max_budget)
        return queryset
    
    def search(self, query):
        """Full-text search across lead fields"""
        return self.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(company__icontains=query) |
            Q(job_title__icontains=query) |
            Q(notes__icontains=query) |
            Q(pain_points__icontains=query) |
            Q(requirements__icontains=query)
        )
    
    def with_utm_source(self, source):
        """Get leads from specific UTM source"""
        return self.filter(utm_source__icontains=source)
    
    def with_utm_campaign(self, campaign):
        """Get leads from specific UTM campaign"""
        return self.filter(utm_campaign__icontains=campaign)
    
    def optimized_for_list(self):
        """Optimized queryset for list views"""
        return self.select_related(
            'source',
            'assigned_to'
        ).prefetch_related(
            'tags'
        )
    
    def optimized_for_detail(self):
        """Optimized queryset for detail views"""
        from .models import LeadActivity, LeadNote
        return self.select_related(
            'source',
            'assigned_to'
        ).prefetch_related(
            'tags',
            models.Prefetch(
                'activities',
                queryset=LeadActivity.objects.select_related('user').order_by('-created_at')[:10]
            ),
            models.Prefetch(
                'lead_notes',
                queryset=LeadNote.objects.select_related('user').order_by('-created_at')[:5]
            ),
            'custom_field_values__custom_field'
        )
    
    def with_activity_stats(self):
        """Annotate with activity statistics"""
        return self.annotate(
            activity_count=Count('activities'),
            note_count=Count('lead_notes'),
            last_activity_date=models.Max('activities__created_at')
        )
    
    def requiring_attention(self):
        """Get leads requiring immediate attention"""
        now = timezone.now()
        return self.active().filter(
            Q(priority__in=['high', 'urgent']) |
            Q(next_follow_up__lt=now) |
            Q(score__gte=80, assigned_to__isnull=True) |
            Q(
                status='new',
                created_at__lt=now - timedelta(days=3)
            )
        )


class LeadManager(models.Manager):
    """Manager for Lead model"""
    
    def get_queryset(self):
        """Return custom queryset"""
        return LeadQuerySet(self.model, using=self._db)
    
    def active(self):
        """Get active leads"""
        return self.get_queryset().active()
    
    def new(self):
        """Get new leads"""
        return self.get_queryset().new()
    
    def high_priority(self):
        """Get high priority leads"""
        return self.get_queryset().high_priority()
    
    def high_score(self, threshold=70):
        """Get high scoring leads"""
        return self.get_queryset().high_score(threshold)
    
    def unassigned(self):
        """Get unassigned leads"""
        return self.get_queryset().unassigned()
    
    def overdue_followup(self):
        """Get leads with overdue follow-ups"""
        return self.get_queryset().overdue_followup()
    
    def created_recently(self, days=7):
        """Get leads created recently"""
        return self.get_queryset().created_recently(days)
    
    def requiring_attention(self):
        """Get leads requiring attention"""
        return self.get_queryset().requiring_attention()
    
    def search(self, query):
        """Search leads"""
        return self.get_queryset().search(query)
    
    def optimized_for_list(self):
        """Optimized for list views"""
        return self.get_queryset().optimized_for_list()
    
    def optimized_for_detail(self):
        """Optimized for detail views"""
        return self.get_queryset().optimized_for_detail()


class LeadActivityManager(models.Manager):
    """Manager for LeadActivity model"""
    
    def upcoming(self):
        """Get upcoming scheduled activities"""
        now = timezone.now()
        return self.filter(
            scheduled_at__gte=now,
            is_completed=False
        )
    
    def overdue(self):
        """Get overdue activities"""
        now = timezone.now()
        return self.filter(
            scheduled_at__lt=now,
            is_completed=False
        )
    
    def completed(self):
        """Get completed activities"""
        return self.filter(is_completed=True)
    
    def of_type(self, activity_type):
        """Get activities of specific type"""
        return self.filter(activity_type=activity_type)
    
    def for_lead(self, lead):
        """Get activities for specific lead"""
        return self.filter(lead=lead)
    
    def by_user(self, user):
        """Get activities by specific user"""
        return self.filter(user=user)
    
    def recent(self, days=7):
        """Get recent activities"""
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(created_at__gte=cutoff)
    
    def today(self):
        """Get activities from today"""
        today = timezone.now().date()
        return self.filter(created_at__date=today)


class LeadNoteManager(models.Manager):
    """Manager for LeadNote model"""
    
    def public(self):
        """Get public notes"""
        return self.filter(is_private=False)
    
    def private(self):
        """Get private notes"""
        return self.filter(is_private=True)
    
    def for_lead(self, lead):
        """Get notes for specific lead"""
        return self.filter(lead=lead)
    
    def by_user(self, user):
        """Get notes by specific user"""
        return self.filter(user=user)
    
    def recent(self, days=7):
        """Get recent notes"""
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(created_at__gte=cutoff)
    
    def accessible_to_user(self, user, tenant):
        """Get notes accessible to specific user"""
        # Get user's role in tenant
        from apps.core.permissions import get_user_tenant_role
        role = get_user_tenant_role(user, tenant)
        
        if role in ['owner', 'admin']:
            # Admins can see all notes
            return self.filter(tenant=tenant)
        else:
            # Regular users can see public notes and their own private notes
            return self.filter(
                tenant=tenant
            ).filter(
                Q(is_private=False) | Q(user=user)
            )