"""
Custom management command to run initial migrations without post_migrate signals
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db.migrations.executor import MigrationExecutor
from django.db import connection
from django.contrib.auth.management import create_permissions
from django.db.models.signals import post_migrate


class Command(BaseCommand):
    help = 'Run initial migrations without permission creation signals'

    def handle(self, *args, **options):
        self.stdout.write('Temporarily disconnecting post_migrate signals...')

        # Disconnect the create_permissions signal
        post_migrate.disconnect(create_permissions, dispatch_uid="django.contrib.auth.management.create_permissions")

        try:
            self.stdout.write('Running migrations...')
            call_command('migrate', '--noinput', verbosity=2)
            self.stdout.write(self.style.SUCCESS('Migrations completed successfully!'))

            # Now reconnect and run create_permissions manually
            self.stdout.write('Creating permissions...')
            post_migrate.connect(create_permissions, dispatch_uid="django.contrib.auth.management.create_permissions")

            # Trigger permission creation for all apps
            from django.apps import apps
            for app_config in apps.get_app_configs():
                if app_config.models_module:
                    create_permissions(app_config, verbosity=2)

            self.stdout.write(self.style.SUCCESS('Permissions created successfully!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Migration failed: {e}'))
            raise