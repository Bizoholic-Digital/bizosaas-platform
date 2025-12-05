"""
Core signals for Django CRM
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    """Handle user creation"""
    if created:
        # TODO: Add user creation logic
        pass