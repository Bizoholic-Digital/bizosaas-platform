"""
Serializers for leads app
DRF serializers with validation and nested relationships
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import (
    LeadSource, LeadTag, Lead, LeadActivity, 
    LeadNote, LeadCustomField, LeadCustomFieldValue
)

User = get_user_model()


class LeadSourceSerializer(serializers.ModelSerializer):
    """Serializer for lead sources"""
    leads_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = LeadSource
        fields = [
            'id', 'name', 'description', 'is_active',
            'conversion_rate', 'total_leads', 'converted_leads',
            'leads_count', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'conversion_rate', 'total_leads', 'converted_leads',
            'created_at', 'updated_at'
        ]
    
    def validate_name(self, value):
        """Validate unique name per tenant"""
        tenant = self.context['request'].tenant
        qs = LeadSource.objects.filter(tenant=tenant, name=value)
        
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        
        if qs.exists():
            raise serializers.ValidationError(
                "A lead source with this name already exists."
            )
        return value


class LeadTagSerializer(serializers.ModelSerializer):
    """Serializer for lead tags"""
    leads_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = LeadTag
        fields = [
            'id', 'name', 'color', 'description', 'is_active',
            'leads_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_name(self, value):
        """Validate unique name per tenant"""
        tenant = self.context['request'].tenant
        qs = LeadTag.objects.filter(tenant=tenant, name=value)
        
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        
        if qs.exists():
            raise serializers.ValidationError(
                "A lead tag with this name already exists."
            )
        return value
    
    def validate_color(self, value):
        """Validate hex color format"""
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError(
                "Color must be in hex format (e.g., #007bff)."
            )
        return value


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user serializer for lead assignments"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name']
        read_only_fields = ['email', 'first_name', 'last_name', 'full_name']


class LeadActivitySerializer(serializers.ModelSerializer):
    """Serializer for lead activities"""
    user = UserBasicSerializer(read_only=True)
    user_id = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = LeadActivity
        fields = [
            'id', 'activity_type', 'title', 'description', 'metadata',
            'scheduled_at', 'is_completed', 'user', 'user_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create activity with current user if not specified"""
        if 'user_id' not in validated_data:
            validated_data['user'] = self.context['request'].user
        else:
            user_id = validated_data.pop('user_id')
            try:
                validated_data['user'] = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise serializers.ValidationError({"user_id": "Invalid user ID."})
        
        return super().create(validated_data)


class LeadNoteSerializer(serializers.ModelSerializer):
    """Serializer for lead notes"""
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = LeadNote
        fields = [
            'id', 'content', 'is_private', 'user',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create note with current user"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class LeadCustomFieldValueSerializer(serializers.ModelSerializer):
    """Serializer for custom field values"""
    field_name = serializers.CharField(source='custom_field.name', read_only=True)
    field_type = serializers.CharField(source='custom_field.field_type', read_only=True)
    
    class Meta:
        model = LeadCustomFieldValue
        fields = [
            'id', 'custom_field', 'field_name', 'field_type', 
            'value', 'created_at', 'updated_at'
        ]
        read_only_fields = ['field_name', 'field_type', 'created_at', 'updated_at']


class LeadListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for lead lists"""
    full_name = serializers.CharField(read_only=True)
    source_name = serializers.CharField(source='source.name', read_only=True)
    assigned_to_name = serializers.CharField(
        source='assigned_to.get_full_name', 
        read_only=True
    )
    tags = LeadTagSerializer(many=True, read_only=True)
    days_since_created = serializers.IntegerField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Lead
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 
            'phone', 'company', 'job_title', 'status', 'priority', 
            'score', 'source_name', 'assigned_to_name', 'tags',
            'days_since_created', 'is_overdue', 'next_follow_up',
            'created_at', 'updated_at'
        ]


class LeadDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for lead CRUD operations"""
    full_name = serializers.CharField(read_only=True)
    source = LeadSourceSerializer(read_only=True)
    source_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    assigned_to = UserBasicSerializer(read_only=True)
    assigned_to_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    tags = LeadTagSerializer(many=True, read_only=True)
    tag_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    
    # Activity tracking
    recent_activities = LeadActivitySerializer(many=True, read_only=True, source='activities')
    notes = LeadNoteSerializer(many=True, read_only=True, source='lead_notes')
    custom_field_values = LeadCustomFieldValueSerializer(many=True, read_only=True)
    
    # Computed fields
    days_since_created = serializers.IntegerField(read_only=True)
    days_until_follow_up = serializers.IntegerField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Lead
        fields = [
            # Basic info
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
            
            # Company info
            'company', 'job_title', 'company_website', 'company_size',
            'industry', 'annual_revenue',
            
            # Lead management
            'status', 'priority', 'source', 'source_id', 
            'assigned_to', 'assigned_to_id', 'tags', 'tag_ids',
            
            # AI scoring
            'score', 'score_factors', 'last_scored_at',
            
            # Qualification
            'budget', 'timeline', 'decision_maker', 
            'pain_points', 'requirements',
            
            # Tracking
            'first_contact_date', 'last_contact_date', 'next_follow_up',
            'converted_at', 'conversion_value', 'lost_reason',
            
            # Marketing
            'utm_source', 'utm_medium', 'utm_campaign',
            'utm_term', 'utm_content', 'referrer',
            
            # Notes and activities
            'notes', 'recent_activities', 'custom_field_values',
            
            # Computed fields
            'days_since_created', 'days_until_follow_up', 'is_overdue',
            
            # Timestamps
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'score', 'score_factors', 'last_scored_at',
            'first_contact_date', 'last_contact_date',
            'converted_at', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def get_recent_activities(self, obj):
        """Get recent activities for the lead"""
        activities = obj.activities.select_related('user').order_by('-created_at')[:10]
        return LeadActivitySerializer(activities, many=True).data
    
    def validate_email(self, value):
        """Validate unique email per tenant"""
        tenant = self.context['request'].tenant
        qs = Lead.objects.filter(tenant=tenant, email=value)
        
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        
        if qs.exists():
            raise serializers.ValidationError(
                "A lead with this email already exists."
            )
        return value
    
    def validate_source_id(self, value):
        """Validate source belongs to tenant"""
        if value:
            tenant = self.context['request'].tenant
            if not LeadSource.objects.filter(tenant=tenant, id=value).exists():
                raise serializers.ValidationError("Invalid source ID.")
        return value
    
    def validate_assigned_to_id(self, value):
        """Validate user belongs to tenant"""
        if value:
            tenant = self.context['request'].tenant
            if not User.objects.filter(tenants=tenant, id=value).exists():
                raise serializers.ValidationError("Invalid user ID.")
        return value
    
    def validate_tag_ids(self, value):
        """Validate tags belong to tenant"""
        if value:
            tenant = self.context['request'].tenant
            valid_tags = LeadTag.objects.filter(
                tenant=tenant, 
                id__in=value
            ).values_list('id', flat=True)
            
            if len(valid_tags) != len(value):
                raise serializers.ValidationError("Some tag IDs are invalid.")
        return value
    
    def validate_budget(self, value):
        """Validate budget is positive"""
        if value is not None and value < 0:
            raise serializers.ValidationError("Budget cannot be negative.")
        return value
    
    def validate_annual_revenue(self, value):
        """Validate annual revenue is positive"""
        if value is not None and value < 0:
            raise serializers.ValidationError("Annual revenue cannot be negative.")
        return value
    
    def validate_conversion_value(self, value):
        """Validate conversion value is positive"""
        if value is not None and value < 0:
            raise serializers.ValidationError("Conversion value cannot be negative.")
        return value
    
    def create(self, validated_data):
        """Create lead with proper relationships"""
        source_id = validated_data.pop('source_id', None)
        assigned_to_id = validated_data.pop('assigned_to_id', None)
        tag_ids = validated_data.pop('tag_ids', [])
        
        # Set relationships
        if source_id:
            validated_data['source_id'] = source_id
        if assigned_to_id:
            validated_data['assigned_to_id'] = assigned_to_id
        
        lead = Lead.objects.create(**validated_data)
        
        # Set tags
        if tag_ids:
            tags = LeadTag.objects.filter(
                tenant=lead.tenant, 
                id__in=tag_ids
            )
            lead.tags.set(tags)
        
        # Calculate initial score
        lead.update_score()
        
        return lead
    
    def update(self, instance, validated_data):
        """Update lead with proper relationships"""
        source_id = validated_data.pop('source_id', None)
        assigned_to_id = validated_data.pop('assigned_to_id', None)
        tag_ids = validated_data.pop('tag_ids', None)
        
        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update relationships
        if source_id is not None:
            instance.source_id = source_id
        if assigned_to_id is not None:
            instance.assigned_to_id = assigned_to_id
        
        instance.save()
        
        # Update tags
        if tag_ids is not None:
            tags = LeadTag.objects.filter(
                tenant=instance.tenant, 
                id__in=tag_ids
            )
            instance.tags.set(tags)
        
        # Recalculate score if relevant fields changed
        score_affecting_fields = [
            'company_size', 'budget', 'decision_maker', 
            'status', 'timeline'
        ]
        if any(field in validated_data for field in score_affecting_fields):
            instance.update_score()
        
        return instance


class LeadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating leads with minimal fields"""
    source_id = serializers.UUIDField(required=False, allow_null=True)
    assigned_to_id = serializers.UUIDField(required=False, allow_null=True)
    tag_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False
    )
    
    class Meta:
        model = Lead
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'company', 'job_title', 'status', 'priority',
            'source_id', 'assigned_to_id', 'tag_ids',
            'notes', 'budget', 'timeline'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate_email(self, value):
        """Validate unique email per tenant"""
        tenant = self.context['request'].tenant
        if Lead.objects.filter(tenant=tenant, email=value).exists():
            raise serializers.ValidationError(
                "A lead with this email already exists."
            )
        return value
    
    def create(self, validated_data):
        """Create lead with relationships"""
        source_id = validated_data.pop('source_id', None)
        assigned_to_id = validated_data.pop('assigned_to_id', None)
        tag_ids = validated_data.pop('tag_ids', [])
        
        # Set relationships
        if source_id:
            validated_data['source_id'] = source_id
        if assigned_to_id:
            validated_data['assigned_to_id'] = assigned_to_id
        
        lead = Lead.objects.create(**validated_data)
        
        # Set tags
        if tag_ids:
            tags = LeadTag.objects.filter(
                tenant=lead.tenant, 
                id__in=tag_ids
            )
            lead.tags.set(tags)
        
        # Calculate initial score
        lead.update_score()
        
        return lead


class LeadBulkUpdateSerializer(serializers.Serializer):
    """Serializer for bulk updating leads"""
    lead_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=True
    )
    status = serializers.ChoiceField(
        choices=Lead.STATUS_CHOICES,
        required=False
    )
    priority = serializers.ChoiceField(
        choices=Lead.PRIORITY_CHOICES,
        required=False
    )
    assigned_to_id = serializers.UUIDField(required=False, allow_null=True)
    source_id = serializers.UUIDField(required=False, allow_null=True)
    tag_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False
    )
    
    def validate_lead_ids(self, value):
        """Validate leads belong to tenant"""
        tenant = self.context['request'].tenant
        valid_leads = Lead.objects.filter(
            tenant=tenant, 
            id__in=value
        ).values_list('id', flat=True)
        
        if len(valid_leads) != len(value):
            raise serializers.ValidationError("Some lead IDs are invalid.")
        return value
    
    def validate_assigned_to_id(self, value):
        """Validate user belongs to tenant"""
        if value:
            tenant = self.context['request'].tenant
            if not User.objects.filter(tenants=tenant, id=value).exists():
                raise serializers.ValidationError("Invalid user ID.")
        return value


class LeadScoreUpdateSerializer(serializers.Serializer):
    """Serializer for updating lead scores"""
    score_factors = serializers.JSONField(required=False)
    
    def update(self, instance, validated_data):
        """Update lead score"""
        factors = validated_data.get('score_factors')
        instance.update_score(factors)
        return instance