"""
Django signals for leads app
Automatic actions and integrations
"""
from django.db.models.signals import post_save, pre_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from apps.core.models import ActivityLog
from .models import Lead, LeadActivity, LeadSource
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Lead)
def lead_pre_save(sender, instance, **kwargs):
    """Actions before saving a lead"""
    try:
        # Track status changes
        if instance.pk:
            try:
                old_instance = Lead.objects.get(pk=instance.pk)
                
                # Status change tracking
                if old_instance.status != instance.status:
                    instance._status_changed = True
                    instance._old_status = old_instance.status
                    instance._new_status = instance.status
                
                # Assignment change tracking
                if old_instance.assigned_to != instance.assigned_to:
                    instance._assignment_changed = True
                    instance._old_assigned_to = old_instance.assigned_to
                    instance._new_assigned_to = instance.assigned_to
                
                # Score change tracking
                if old_instance.score != instance.score:
                    instance._score_changed = True
                    instance._old_score = old_instance.score
                    instance._new_score = instance.score
                    
            except Lead.DoesNotExist:
                pass
        
        # Auto-set conversion timestamp
        if instance.status == 'converted' and not instance.converted_at:
            instance.converted_at = timezone.now()
        
        # Clear conversion timestamp if status changes from converted
        if instance.status != 'converted' and instance.converted_at:
            instance.converted_at = None
            instance.conversion_value = None
            
    except Exception as e:
        logger.error(f"Error in lead_pre_save signal: {e}")


@receiver(post_save, sender=Lead)
def lead_post_save(sender, instance, created, **kwargs):
    """Actions after saving a lead"""
    try:
        # Create activity log for new leads
        if created:
            ActivityLog.objects.create(
                tenant=instance.tenant,
                user_id=getattr(instance, '_created_by_user_id', None),
                activity_type='create',
                object_type='Lead',
                object_id=str(instance.id),
                description=f"New lead created: {instance.full_name} from {instance.company or 'Unknown Company'}",
                metadata={
                    'lead_email': instance.email,
                    'lead_company': instance.company,
                    'lead_source': instance.source.name if instance.source else None,
                    'initial_score': instance.score
                }
            )
            
            # Auto-assign initial score for new leads
            if instance.score == 0:
                instance.update_score()
        
        # Handle status changes
        if hasattr(instance, '_status_changed') and instance._status_changed:
            # Create activity for status change
            LeadActivity.objects.create(
                tenant=instance.tenant,
                lead=instance,
                user_id=getattr(instance, '_changed_by_user_id', None),
                activity_type='status_change',
                title=f"Status changed from {instance._old_status} to {instance._new_status}",
                description=f"Lead status updated from {instance._old_status} to {instance._new_status}",
                metadata={
                    'old_status': instance._old_status,
                    'new_status': instance._new_status
                }
            )
            
            # Update source statistics if converted or lost
            if instance.status in ['converted', 'lost'] and instance.source:
                instance.source.update_conversion_stats()
        
        # Handle assignment changes
        if hasattr(instance, '_assignment_changed') and instance._assignment_changed:
            old_user = instance._old_assigned_to
            new_user = instance._new_assigned_to
            
            description = f"Lead assignment changed"
            if old_user and new_user:
                description += f" from {old_user.get_full_name() or old_user.email} to {new_user.get_full_name() or new_user.email}"
            elif new_user:
                description += f" to {new_user.get_full_name() or new_user.email}"
            elif old_user:
                description += f" (unassigned from {old_user.get_full_name() or old_user.email})"
            
            LeadActivity.objects.create(
                tenant=instance.tenant,
                lead=instance,
                user_id=getattr(instance, '_changed_by_user_id', None),
                activity_type='assignment',
                title="Assignment Changed",
                description=description,
                metadata={
                    'old_assigned_to': old_user.email if old_user else None,
                    'new_assigned_to': new_user.email if new_user else None
                }
            )
        
        # Handle score changes (but not initial scoring)
        if (hasattr(instance, '_score_changed') and instance._score_changed and 
            not created and instance._old_score > 0):
            
            score_diff = instance._new_score - instance._old_score
            direction = "increased" if score_diff > 0 else "decreased"
            
            LeadActivity.objects.create(
                tenant=instance.tenant,
                lead=instance,
                user_id=getattr(instance, '_changed_by_user_id', None),
                activity_type='note',
                title=f"AI Score {direction.title()}",
                description=f"AI lead score {direction} from {instance._old_score} to {instance._new_score} ({score_diff:+d} points)",
                metadata={
                    'old_score': instance._old_score,
                    'new_score': instance._new_score,
                    'score_change': score_diff,
                    'score_factors': instance.score_factors
                }
            )
            
    except Exception as e:
        logger.error(f"Error in lead_post_save signal: {e}")


@receiver(post_save, sender=LeadActivity)
def activity_post_save(sender, instance, created, **kwargs):
    """Actions after saving a lead activity"""
    try:
        if created and instance.activity_type in ['email', 'call', 'meeting', 'contact']:
            # Update lead's last contact date
            lead = instance.lead
            lead.last_contact_date = timezone.now()
            
            # Set first contact date if not set
            if not lead.first_contact_date:
                lead.first_contact_date = timezone.now()
            
            # Update status if still new
            if lead.status == 'new' and instance.activity_type in ['email', 'call', 'contact']:
                lead.status = 'contacted'
            
            lead.save(update_fields=['last_contact_date', 'first_contact_date', 'status'])
            
    except Exception as e:
        logger.error(f"Error in activity_post_save signal: {e}")


@receiver(m2m_changed, sender=Lead.tags.through)
def lead_tags_changed(sender, instance, action, pk_set, **kwargs):
    """Actions when lead tags are changed"""
    try:
        if action in ['post_add', 'post_remove'] and pk_set:
            from .models import LeadTag
            
            if action == 'post_add':
                tags = LeadTag.objects.filter(id__in=pk_set)
                tag_names = [tag.name for tag in tags]
                
                LeadActivity.objects.create(
                    tenant=instance.tenant,
                    lead=instance,
                    user_id=getattr(instance, '_changed_by_user_id', None),
                    activity_type='note',
                    title="Tags Added",
                    description=f"Tags added: {', '.join(tag_names)}",
                    metadata={
                        'action': 'add',
                        'tag_names': tag_names,
                        'tag_ids': list(pk_set)
                    }
                )
                
            elif action == 'post_remove':
                # We can't get the tag names after removal, so just log IDs
                LeadActivity.objects.create(
                    tenant=instance.tenant,
                    lead=instance,
                    user_id=getattr(instance, '_changed_by_user_id', None),
                    activity_type='note',
                    title="Tags Removed",
                    description=f"Tags removed (IDs: {', '.join(map(str, pk_set))})",
                    metadata={
                        'action': 'remove',
                        'tag_ids': list(pk_set)
                    }
                )
                
    except Exception as e:
        logger.error(f"Error in lead_tags_changed signal: {e}")


@receiver(post_delete, sender=Lead)
def lead_post_delete(sender, instance, **kwargs):
    """Actions after deleting a lead"""
    try:
        # Log lead deletion
        ActivityLog.objects.create(
            tenant=instance.tenant,
            user_id=getattr(instance, '_deleted_by_user_id', None),
            activity_type='delete',
            object_type='Lead',
            object_id=str(instance.id),
            description=f"Lead deleted: {instance.full_name} ({instance.email})",
            metadata={
                'lead_name': instance.full_name,
                'lead_email': instance.email,
                'lead_company': instance.company,
                'lead_status': instance.status,
                'lead_score': instance.score
            }
        )
        
        # Update source statistics
        if instance.source:
            instance.source.update_conversion_stats()
            
    except Exception as e:
        logger.error(f"Error in lead_post_delete signal: {e}")


@receiver(post_save, sender=LeadSource)
def source_post_save(sender, instance, created, **kwargs):
    """Actions after saving a lead source"""
    try:
        if created:
            ActivityLog.objects.create(
                tenant=instance.tenant,
                user_id=getattr(instance, '_created_by_user_id', None),
                activity_type='create',
                object_type='LeadSource',
                object_id=str(instance.id),
                description=f"New lead source created: {instance.name}",
                metadata={
                    'source_name': instance.name,
                    'source_description': instance.description
                }
            )
            
    except Exception as e:
        logger.error(f"Error in source_post_save signal: {e}")


# Helper function to set user context for signals
def set_lead_user_context(lead, user, action='change'):
    """Set user context on lead instance for signal tracking"""
    if action == 'create':
        setattr(lead, '_created_by_user_id', user.id if user else None)
    elif action == 'change':
        setattr(lead, '_changed_by_user_id', user.id if user else None)
    elif action == 'delete':
        setattr(lead, '_deleted_by_user_id', user.id if user else None)


# Connect to logging system
import sys
if 'test' not in sys.argv:
    # Only set up logging for non-test environments
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(),
        ]
    )