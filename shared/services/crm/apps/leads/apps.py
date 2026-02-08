"""
Django app configuration for leads
"""
from django.apps import AppConfig


class LeadsConfig(AppConfig):
    """Leads app configuration"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.leads'
    verbose_name = 'Leads Management'
    
    def ready(self):
        """Import signals when the app is ready"""
        try:
            import apps.leads.signals  # noqa F401
        except ImportError:
            pass