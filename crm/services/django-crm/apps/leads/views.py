"""
Views for leads app
DRF ViewSets with filtering, search, pagination, and AI integration
"""
from django.db.models import Q, Count, Avg, Sum, Prefetch
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.core.permissions import TenantPermissionMixin
from apps.core.pagination import StandardResultsSetPagination
from .models import (
    LeadSource, LeadTag, Lead, LeadActivity, 
    LeadNote, LeadCustomField, LeadCustomFieldValue
)
from .serializers import (
    LeadSourceSerializer, LeadTagSerializer, LeadListSerializer,
    LeadDetailSerializer, LeadCreateSerializer, LeadActivitySerializer,
    LeadNoteSerializer, LeadBulkUpdateSerializer, LeadScoreUpdateSerializer
)
from .filters import LeadFilter
import requests
from datetime import timedelta


class LeadSourceViewSet(TenantPermissionMixin, viewsets.ModelViewSet):
    """ViewSet for lead sources"""
    queryset = LeadSource.objects.all()
    serializer_class = LeadSourceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'conversion_rate', 'total_leads', 'created_at']
    ordering = ['-total_leads', 'name']
    
    def get_queryset(self):
        """Filter by tenant and add lead counts"""
        return super().get_queryset().annotate(
            leads_count=Count('lead_set')
        )
    
    @action(detail=True, methods=['post'])
    def refresh_stats(self, request, pk=None):
        """Refresh conversion statistics"""
        source = self.get_object()
        source.update_conversion_stats()
        
        return Response({
            'message': 'Statistics refreshed',
            'total_leads': source.total_leads,
            'converted_leads': source.converted_leads,
            'conversion_rate': source.conversion_rate
        })


class LeadTagViewSet(TenantPermissionMixin, viewsets.ModelViewSet):
    """ViewSet for lead tags"""
    queryset = LeadTag.objects.all()
    serializer_class = LeadTagSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Filter by tenant and add lead counts"""
        return super().get_queryset().annotate(
            leads_count=Count('leads')
        )


class LeadViewSet(TenantPermissionMixin, viewsets.ModelViewSet):
    """ViewSet for leads with advanced filtering and AI features"""
    queryset = Lead.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = LeadFilter
    search_fields = [
        'first_name', 'last_name', 'email', 'phone', 'company', 
        'job_title', 'notes', 'pain_points', 'requirements'
    ]
    ordering_fields = [
        'first_name', 'last_name', 'company', 'status', 'priority',
        'score', 'created_at', 'updated_at', 'last_contact_date'
    ]
    ordering = ['-score', '-created_at']
    
    def get_queryset(self):
        """Optimized queryset with related data"""
        return super().get_queryset().select_related(
            'source', 'assigned_to'
        ).prefetch_related(
            'tags',
            Prefetch(
                'activities',
                queryset=LeadActivity.objects.select_related('user').order_by('-created_at')[:5]
            ),
            Prefetch(
                'lead_notes',
                queryset=LeadNote.objects.select_related('user').order_by('-created_at')[:5]
            )
        )
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return LeadCreateSerializer
        elif self.action == 'list':
            return LeadListSerializer
        elif self.action in ['update_scores', 'update_score']:
            return LeadScoreUpdateSerializer
        elif self.action == 'bulk_update':
            return LeadBulkUpdateSerializer
        return LeadDetailSerializer
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get dashboard statistics"""
        queryset = self.get_queryset()
        
        # Basic counts
        total_leads = queryset.count()
        new_leads = queryset.filter(status='new').count()
        converted_leads = queryset.filter(status='converted').count()
        
        # Score distribution
        high_score_leads = queryset.filter(score__gte=70).count()
        medium_score_leads = queryset.filter(score__gte=40, score__lt=70).count()
        low_score_leads = queryset.filter(score__lt=40).count()
        
        # Recent activity
        recent_leads = queryset.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        # Conversion rate
        conversion_rate = 0
        if total_leads > 0:
            conversion_rate = (converted_leads / total_leads) * 100
        
        # Average score
        avg_score = queryset.aggregate(Avg('score'))['score__avg'] or 0
        
        # Top sources
        top_sources = LeadSource.objects.filter(
            tenant=request.tenant,
            lead_set__in=queryset
        ).annotate(
            leads_count=Count('lead_set')
        ).order_by('-leads_count')[:5]
        
        return Response({
            'total_leads': total_leads,
            'new_leads': new_leads,
            'converted_leads': converted_leads,
            'recent_leads': recent_leads,
            'conversion_rate': round(conversion_rate, 2),
            'average_score': round(avg_score, 1),
            'score_distribution': {
                'high': high_score_leads,
                'medium': medium_score_leads,
                'low': low_score_leads
            },
            'top_sources': [
                {
                    'id': source.id,
                    'name': source.name,
                    'leads_count': source.leads_count
                }
                for source in top_sources
            ]
        })
    
    @action(detail=True, methods=['post'])
    def update_score(self, request, pk=None):
        """Update AI score for a single lead"""
        lead = self.get_object()
        serializer = self.get_serializer(lead, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Score updated successfully',
                'score': lead.score,
                'score_factors': lead.score_factors,
                'last_scored_at': lead.last_scored_at
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def update_scores(self, request):
        """Update AI scores for multiple leads"""
        lead_ids = request.data.get('lead_ids', [])
        if not lead_ids:
            return Response(
                {'error': 'lead_ids is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leads = self.get_queryset().filter(id__in=lead_ids)
        updated_count = 0
        
        for lead in leads:
            lead.update_score()
            updated_count += 1
        
        return Response({
            'message': f'Updated scores for {updated_count} leads',
            'updated_count': updated_count
        })
    
    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """Bulk update leads"""
        serializer = LeadBulkUpdateSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            lead_ids = validated_data.pop('lead_ids')
            
            leads = self.get_queryset().filter(id__in=lead_ids)
            
            # Update fields
            update_fields = {}
            for field in ['status', 'priority', 'assigned_to_id', 'source_id']:
                if field in validated_data:
                    update_fields[field] = validated_data[field]
            
            updated_count = leads.update(**update_fields) if update_fields else 0
            
            # Handle tags separately
            if 'tag_ids' in validated_data:
                from .models import LeadTag
                tags = LeadTag.objects.filter(
                    tenant=request.tenant,
                    id__in=validated_data['tag_ids']
                )
                for lead in leads:
                    lead.tags.set(tags)
            
            return Response({
                'message': f'Updated {updated_count} leads',
                'updated_count': updated_count
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def mark_contacted(self, request, pk=None):
        """Mark lead as contacted"""
        lead = self.get_object()
        lead.mark_as_contacted(request.user)
        
        return Response({
            'message': 'Lead marked as contacted',
            'status': lead.status,
            'first_contact_date': lead.first_contact_date,
            'last_contact_date': lead.last_contact_date
        })
    
    @action(detail=True, methods=['post'])
    def convert(self, request, pk=None):
        """Convert lead to customer"""
        lead = self.get_object()
        value = request.data.get('conversion_value')
        
        if value:
            try:
                value = float(value)
            except (ValueError, TypeError):
                return Response(
                    {'error': 'Invalid conversion_value'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        lead.convert(value=value, user=request.user)
        
        return Response({
            'message': 'Lead converted successfully',
            'status': lead.status,
            'converted_at': lead.converted_at,
            'conversion_value': lead.conversion_value
        })
    
    @action(detail=True, methods=['post'])
    def mark_lost(self, request, pk=None):
        """Mark lead as lost"""
        lead = self.get_object()
        reason = request.data.get('reason', '')
        
        lead.status = 'lost'
        lead.lost_reason = reason
        lead.save(update_fields=['status', 'lost_reason'])
        
        # Create activity record
        LeadActivity.objects.create(
            tenant=lead.tenant,
            lead=lead,
            user=request.user,
            activity_type='lost',
            description=f"Lead marked as lost by {request.user.get_full_name() or request.user.email}",
            metadata={'reason': reason}
        )
        
        return Response({
            'message': 'Lead marked as lost',
            'status': lead.status,
            'lost_reason': lead.lost_reason
        })
    
    @action(detail=True, methods=['post'])
    def ai_insights(self, request, pk=None):
        """Get AI-powered insights for a lead"""
        lead = self.get_object()
        
        # This would integrate with your AI service (CrewAI)
        # For now, return mock insights based on lead data
        insights = {
            'score_breakdown': lead.score_factors,
            'recommendations': [],
            'risk_factors': [],
            'opportunities': []
        }
        
        # Generate recommendations based on lead data
        if lead.score < 30:
            insights['recommendations'].append({
                'type': 'qualification',
                'message': 'Focus on qualifying this lead further',
                'priority': 'high'
            })
        
        if not lead.budget:
            insights['recommendations'].append({
                'type': 'discovery',
                'message': 'Discover budget information',
                'priority': 'medium'
            })
        
        if lead.next_follow_up and lead.is_overdue:
            insights['risk_factors'].append({
                'type': 'follow_up',
                'message': 'Follow-up is overdue',
                'priority': 'high'
            })
        
        if lead.decision_maker and lead.budget and lead.budget > 10000:
            insights['opportunities'].append({
                'type': 'high_value',
                'message': 'High-value decision maker opportunity',
                'priority': 'high'
            })
        
        # TODO: Integrate with actual AI service
        # ai_response = requests.post(
        #     'http://crewai-service:8000/analyze-lead',
        #     json={'lead_data': LeadDetailSerializer(lead).data}
        # )
        
        return Response(insights)
    
    @action(detail=False, methods=['get'])
    def overdue_followups(self, request):
        """Get leads with overdue follow-ups"""
        now = timezone.now()
        overdue_leads = self.get_queryset().filter(
            next_follow_up__lt=now,
            status__in=['new', 'contacted', 'qualified', 'proposal', 'negotiation']
        ).order_by('next_follow_up')
        
        page = self.paginate_queryset(overdue_leads)
        if page is not None:
            serializer = LeadListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = LeadListSerializer(overdue_leads, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def high_priority(self, request):
        """Get high priority leads"""
        high_priority_leads = self.get_queryset().filter(
            priority__in=['high', 'urgent'],
            status__in=['new', 'contacted', 'qualified', 'proposal', 'negotiation']
        ).order_by('-priority', '-score')
        
        page = self.paginate_queryset(high_priority_leads)
        if page is not None:
            serializer = LeadListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = LeadListSerializer(high_priority_leads, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unassigned(self, request):
        """Get unassigned leads"""
        unassigned_leads = self.get_queryset().filter(
            assigned_to__isnull=True
        ).order_by('-score', '-created_at')
        
        page = self.paginate_queryset(unassigned_leads)
        if page is not None:
            serializer = LeadListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = LeadListSerializer(unassigned_leads, many=True)
        return Response(serializer.data)


class LeadActivityViewSet(TenantPermissionMixin, viewsets.ModelViewSet):
    """ViewSet for lead activities"""
    queryset = LeadActivity.objects.all()
    serializer_class = LeadActivitySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['activity_type', 'is_completed', 'lead']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'scheduled_at', 'activity_type']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter by tenant and include user info"""
        return super().get_queryset().select_related('user', 'lead')
    
    def perform_create(self, serializer):
        """Set lead from URL if provided"""
        lead_id = self.request.data.get('lead_id') or self.kwargs.get('lead_pk')
        if lead_id:
            lead = get_object_or_404(Lead, id=lead_id, tenant=self.request.tenant)
            serializer.save(lead=lead, tenant=self.request.tenant)
        else:
            super().perform_create(serializer)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming scheduled activities"""
        now = timezone.now()
        upcoming = self.get_queryset().filter(
            scheduled_at__gte=now,
            is_completed=False
        ).order_by('scheduled_at')
        
        page = self.paginate_queryset(upcoming)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue activities"""
        now = timezone.now()
        overdue = self.get_queryset().filter(
            scheduled_at__lt=now,
            is_completed=False
        ).order_by('scheduled_at')
        
        page = self.paginate_queryset(overdue)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(overdue, many=True)
        return Response(serializer.data)


class LeadNoteViewSet(TenantPermissionMixin, viewsets.ModelViewSet):
    """ViewSet for lead notes"""
    queryset = LeadNote.objects.all()
    serializer_class = LeadNoteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_private', 'lead']
    search_fields = ['content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter private notes and include user info"""
        queryset = super().get_queryset().select_related('user', 'lead')
        
        # Filter private notes - only show to author or tenant admins
        if not self.request.user.is_superuser:
            user_memberships = self.request.user.memberships.filter(
                tenant=self.request.tenant,
                role__in=['owner', 'admin']
            )
            
            if not user_memberships.exists():
                # Regular users can only see their own private notes
                queryset = queryset.filter(
                    Q(is_private=False) | Q(user=self.request.user)
                )
        
        return queryset
    
    def perform_create(self, serializer):
        """Set lead from URL if provided"""
        lead_id = self.request.data.get('lead_id') or self.kwargs.get('lead_pk')
        if lead_id:
            lead = get_object_or_404(Lead, id=lead_id, tenant=self.request.tenant)
            serializer.save(lead=lead, tenant=self.request.tenant)
        else:
            super().perform_create(serializer)