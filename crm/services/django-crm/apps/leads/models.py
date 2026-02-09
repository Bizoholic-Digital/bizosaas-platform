"""
Lead models for Django CRM with AI scoring integration
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.core.models import BaseModel
from .managers import (
    LeadSourceManager, LeadTagManager, LeadManager,
    LeadActivityManager, LeadNoteManager
)
import json

User = get_user_model()


class LeadSource(BaseModel):
    """Lead source tracking"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    # Tracking
    conversion_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        help_text="Conversion rate percentage"
    )
    total_leads = models.IntegerField(default=0)
    converted_leads = models.IntegerField(default=0)
    
    objects = LeadSourceManager()
    
    class Meta:
        db_table = 'leads_source'
        unique_together = [['tenant', 'name']]
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.tenant.name})"
    
    def update_conversion_stats(self):
        """Update conversion statistics"""
        self.total_leads = self.leads.count()
        self.converted_leads = self.leads.filter(status='converted').count()
        if self.total_leads > 0:
            self.conversion_rate = (self.converted_leads / self.total_leads) * 100
        else:
            self.conversion_rate = 0.00
        self.save()


class LeadTag(BaseModel):
    """Tags for lead categorization"""
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    objects = LeadTagManager()
    
    class Meta:
        db_table = 'leads_tag'
        unique_together = [['tenant', 'name']]
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.tenant.name})"


class Lead(BaseModel):
    """Main lead model with AI scoring"""
    
    # Status choices
    STATUS_CHOICES = (
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal Sent'),
        ('negotiation', 'In Negotiation'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
        ('unresponsive', 'Unresponsive'),
    )
    
    # Priority choices
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )
    
    # Contact Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    # Company Information
    company = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    company_website = models.URLField(blank=True)
    company_size = models.CharField(max_length=50, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    annual_revenue = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Estimated annual revenue"
    )
    
    # Lead Management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    source = models.ForeignKey(
        LeadSource, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='leads',
        help_text="How the lead was acquired"
    )
    
    # Assignment
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads',
        help_text="User responsible for this lead"
    )
    
    # AI Scoring
    score = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="AI-generated lead score (0-100)"
    )
    score_factors = models.JSONField(
        default=dict,
        blank=True,
        help_text="Factors contributing to the lead score"
    )
    last_scored_at = models.DateTimeField(null=True, blank=True)
    
    # Communication
    notes = models.TextField(blank=True, help_text="Internal notes about the lead")
    tags = models.ManyToManyField(LeadTag, blank=True, related_name='leads')
    
    # Tracking
    first_contact_date = models.DateTimeField(null=True, blank=True)
    last_contact_date = models.DateTimeField(null=True, blank=True)
    next_follow_up = models.DateTimeField(null=True, blank=True)
    
    # Marketing
    utm_source = models.CharField(max_length=100, blank=True)
    utm_medium = models.CharField(max_length=100, blank=True)
    utm_campaign = models.CharField(max_length=100, blank=True)
    utm_term = models.CharField(max_length=100, blank=True)
    utm_content = models.CharField(max_length=100, blank=True)
    referrer = models.URLField(blank=True)
    
    # Qualification
    budget = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Estimated budget"
    )
    timeline = models.CharField(max_length=100, blank=True, help_text="Expected timeline")
    decision_maker = models.BooleanField(
        default=False, 
        help_text="Is this person a decision maker?"
    )
    pain_points = models.TextField(blank=True, help_text="Identified pain points")
    requirements = models.TextField(blank=True, help_text="Business requirements")
    
    # Conversion tracking
    converted_at = models.DateTimeField(null=True, blank=True)
    conversion_value = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Value of conversion"
    )
    lost_reason = models.TextField(blank=True, help_text="Reason if lead was lost")
    
    objects = LeadManager()
    
    class Meta:
        db_table = 'leads_lead'
        indexes = [
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['tenant', 'assigned_to']),
            models.Index(fields=['tenant', 'score']),
            models.Index(fields=['tenant', 'priority']),
            models.Index(fields=['tenant', 'source']),
            models.Index(fields=['email']),
            models.Index(fields=['company']),
            models.Index(fields=['created_at']),
            models.Index(fields=['next_follow_up']),
        ]
        ordering = ['-score', '-created_at']
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company}"
    
    @property
    def full_name(self):
        """Get full name of the lead"""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def days_since_created(self):
        """Get days since lead was created"""
        return (timezone.now() - self.created_at).days
    
    @property
    def days_until_follow_up(self):
        """Get days until next follow up"""
        if self.next_follow_up:
            return (self.next_follow_up - timezone.now()).days
        return None
    
    @property
    def is_overdue(self):
        """Check if follow up is overdue"""
        if self.next_follow_up:
            return timezone.now() > self.next_follow_up
        return False
    
    def update_score(self, factors=None):
        """Update AI lead score based on various factors"""
        score = 0
        score_factors = factors or {}
        
        # Company size scoring
        company_size_scores = {
            'startup': 10,
            'small': 20,
            'medium': 40,
            'large': 60,
            'enterprise': 80
        }
        if self.company_size:
            score += company_size_scores.get(self.company_size.lower(), 10)
            score_factors['company_size'] = company_size_scores.get(self.company_size.lower(), 10)
        
        # Budget scoring
        if self.budget:
            if self.budget >= 100000:
                score += 30
                score_factors['budget'] = 30
            elif self.budget >= 50000:
                score += 20
                score_factors['budget'] = 20
            elif self.budget >= 10000:
                score += 10
                score_factors['budget'] = 10
        
        # Decision maker bonus
        if self.decision_maker:
            score += 15
            score_factors['decision_maker'] = 15
        
        # Contact information completeness
        contact_score = 0
        if self.phone:
            contact_score += 5
        if self.company:
            contact_score += 5
        if self.job_title:
            contact_score += 5
        score += contact_score
        score_factors['contact_completeness'] = contact_score
        
        # Engagement scoring (based on status)
        status_scores = {
            'new': 5,
            'contacted': 10,
            'qualified': 25,
            'proposal': 40,
            'negotiation': 60,
            'converted': 100,
            'lost': 0,
            'unresponsive': 0
        }
        score += status_scores.get(self.status, 0)
        score_factors['status'] = status_scores.get(self.status, 0)
        
        # Timeline scoring
        if 'immediate' in (self.timeline or '').lower():
            score += 20
            score_factors['timeline'] = 20
        elif 'month' in (self.timeline or '').lower():
            score += 15
            score_factors['timeline'] = 15
        elif 'quarter' in (self.timeline or '').lower():
            score += 10
            score_factors['timeline'] = 10
        
        # Cap at 100
        score = min(score, 100)
        
        self.score = score
        self.score_factors = score_factors
        self.last_scored_at = timezone.now()
        self.save(update_fields=['score', 'score_factors', 'last_scored_at'])
        
        return score
    
    def mark_as_contacted(self, user=None):
        """Mark lead as contacted and update timestamps"""
        if self.status == 'new':
            self.status = 'contacted'
        
        now = timezone.now()
        if not self.first_contact_date:
            self.first_contact_date = now
        self.last_contact_date = now
        
        self.save(update_fields=['status', 'first_contact_date', 'last_contact_date'])
        
        # Create activity record
        if user:
            LeadActivity.objects.create(
                tenant=self.tenant,
                lead=self,
                user=user,
                activity_type='contact',
                description=f"Lead marked as contacted by {user.get_full_name() or user.email}"
            )
    
    def convert(self, value=None, user=None):
        """Convert the lead to customer"""
        self.status = 'converted'
        self.converted_at = timezone.now()
        if value:
            self.conversion_value = value
        
        # Update score to 100 for converted leads
        self.score = 100
        
        self.save(update_fields=['status', 'converted_at', 'conversion_value', 'score'])
        
        # Update source statistics
        if self.source:
            self.source.update_conversion_stats()
        
        # Create activity record
        if user:
            LeadActivity.objects.create(
                tenant=self.tenant,
                lead=self,
                user=user,
                activity_type='convert',
                description=f"Lead converted by {user.get_full_name() or user.email}",
                metadata={'conversion_value': float(value) if value else None}
            )


class LeadActivity(BaseModel):
    """Activity tracking for leads"""
    
    ACTIVITY_TYPES = (
        ('note', 'Note Added'),
        ('email', 'Email Sent'),
        ('call', 'Phone Call'),
        ('meeting', 'Meeting'),
        ('contact', 'First Contact'),
        ('follow_up', 'Follow Up'),
        ('proposal', 'Proposal Sent'),
        ('convert', 'Converted'),
        ('lost', 'Marked as Lost'),
        ('status_change', 'Status Changed'),
        ('assignment', 'Assignment Changed'),
    )
    
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    
    # Scheduling for future activities
    scheduled_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=True)
    
    objects = LeadActivityManager()
    
    class Meta:
        db_table = 'leads_activity'
        indexes = [
            models.Index(fields=['tenant', 'lead']),
            models.Index(fields=['tenant', 'user']),
            models.Index(fields=['tenant', 'activity_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['scheduled_at']),
        ]
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.lead.full_name} - {self.get_activity_type_display()}"


class LeadNote(BaseModel):
    """Notes attached to leads"""
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='lead_notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    content = models.TextField()
    is_private = models.BooleanField(default=False, help_text="Private note visible only to author")
    
    objects = LeadNoteManager()
    
    class Meta:
        db_table = 'leads_note'
        indexes = [
            models.Index(fields=['tenant', 'lead']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Note for {self.lead.full_name} by {self.user.email}"


class LeadCustomField(BaseModel):
    """Custom fields for leads per tenant"""
    
    FIELD_TYPES = (
        ('text', 'Text'),
        ('textarea', 'Text Area'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('datetime', 'Date Time'),
        ('boolean', 'Yes/No'),
        ('select', 'Dropdown'),
        ('multi_select', 'Multi Select'),
        ('url', 'URL'),
        ('email', 'Email'),
    )
    
    name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    is_required = models.BooleanField(default=False)
    default_value = models.TextField(blank=True)
    options = models.JSONField(
        default=list, 
        blank=True,
        help_text="Options for select/multi_select fields"
    )
    help_text = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'leads_custom_field'
        unique_together = [['tenant', 'name']]
        ordering = ['order', 'name']
        
    def __str__(self):
        return f"{self.name} ({self.tenant.name})"


class LeadCustomFieldValue(BaseModel):
    """Values for custom fields"""
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='custom_field_values')
    custom_field = models.ForeignKey(LeadCustomField, on_delete=models.CASCADE)
    value = models.TextField(blank=True)
    
    class Meta:
        db_table = 'leads_custom_field_value'
        unique_together = [['lead', 'custom_field']]
        
    def __str__(self):
        return f"{self.lead.full_name} - {self.custom_field.name}"
    
    def get_typed_value(self):
        """Return value in the correct type based on field type"""
        if not self.value:
            return None
            
        field_type = self.custom_field.field_type
        
        if field_type == 'number':
            try:
                return float(self.value)
            except ValueError:
                return None
        elif field_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif field_type in ('select', 'multi_select'):
            if field_type == 'multi_select':
                try:
                    return json.loads(self.value)
                except json.JSONDecodeError:
                    return []
            return self.value
        else:
            return self.value