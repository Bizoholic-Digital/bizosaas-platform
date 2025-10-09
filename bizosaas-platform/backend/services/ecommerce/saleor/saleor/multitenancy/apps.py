"""
Multi-tenancy app configuration for Saleor
"""

from django.apps import AppConfig


class MultitenancyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'saleor.multitenancy'
    verbose_name = 'Multi-tenant Organizations'

    def ready(self):
        """Import signals and setup when app is ready"""
        # Import any signals here if needed
        pass