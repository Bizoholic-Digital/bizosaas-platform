"""
Django management command to delete a tenant and associated resources
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from wagtail.models import Site as WagtailSite
from cms.models import Tenant
import uuid


class Command(BaseCommand):
    help = 'Delete a tenant and all associated resources (USE WITH CAUTION)'

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '--tenant-id',
            type=str,
            help='Tenant UUID to delete'
        )
        group.add_argument(
            '--bizosaas-tenant-id',
            type=str,
            help='BizOSaaS tenant ID to delete'
        )
        group.add_argument(
            '--domain',
            type=str,
            help='Domain of tenant to delete'
        )
        
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompt',
            default=False
        )
        parser.add_argument(
            '--preserve-site',
            action='store_true',
            help='Keep the Wagtail site but remove tenant association',
            default=False
        )
        parser.add_argument(
            '--preserve-pages',
            action='store_true',
            help='Keep pages but remove tenant association',
            default=False
        )

    def handle(self, *args, **options):
        tenant_id = options.get('tenant_id')
        bizosaas_tenant_id = options.get('bizosaas_tenant_id')
        domain = options.get('domain')
        force = options['force']
        preserve_site = options['preserve_site']
        preserve_pages = options['preserve_pages']

        # Find the tenant
        try:
            if tenant_id:
                tenant = Tenant.objects.select_related('wagtail_site').get(id=tenant_id)
            elif bizosaas_tenant_id:
                tenant = Tenant.objects.select_related('wagtail_site').get(bizosaas_tenant_id=bizosaas_tenant_id)
            elif domain:
                tenant = Tenant.objects.select_related('wagtail_site').get(domain=domain)
        except Tenant.DoesNotExist:
            identifier = tenant_id or bizosaas_tenant_id or domain
            raise CommandError(f'Tenant not found: {identifier}')

        # Display tenant information
        self.stdout.write(f'Tenant to delete:')
        self.stdout.write(f'  ID: {tenant.id}')
        self.stdout.write(f'  Name: {tenant.name}')
        self.stdout.write(f'  Domain: {tenant.domain}')
        self.stdout.write(f'  BizOSaaS Tenant ID: {tenant.bizosaas_tenant_id}')
        self.stdout.write(f'  Is Active: {tenant.is_active}')
        
        if tenant.wagtail_site:
            self.stdout.write(f'  Associated Wagtail Site: {tenant.wagtail_site.site_name} ({tenant.wagtail_site.hostname}:{tenant.wagtail_site.port})')
        
        # Count associated resources
        resources_info = []
        
        # Count tenant pages
        from cms.models import TenantHomePage, TenantContentPage
        home_pages = TenantHomePage.objects.filter(tenant=tenant).count()
        content_pages = TenantContentPage.objects.filter(tenant=tenant).count()
        if home_pages or content_pages:
            resources_info.append(f'{home_pages + content_pages} pages ({home_pages} home, {content_pages} content)')

        # Count collections
        from wagtail.models import Collection
        if tenant.wagtail_site:
            collections = Collection.objects.filter(name__startswith=tenant.name).count()
            if collections:
                resources_info.append(f'{collections} media collections')

        if resources_info:
            self.stdout.write(f'  Associated Resources: {", ".join(resources_info)}')

        # Confirm deletion
        if not force:
            self.stdout.write(
                self.style.WARNING(
                    '\nThis action will permanently delete the tenant and associated resources.'
                )
            )
            if preserve_site:
                self.stdout.write('The Wagtail site will be preserved but unlinked.')
            if preserve_pages:
                self.stdout.write('Pages will be preserved but unlinked from tenant.')
            
            confirm = input('\nAre you sure you want to continue? [y/N]: ')
            if confirm.lower() not in ['y', 'yes']:
                self.stdout.write('Operation cancelled.')
                return

        try:
            with transaction.atomic():
                self.stdout.write('Deleting tenant resources...')

                # Handle pages
                if not preserve_pages:
                    # Delete tenant pages
                    home_pages = TenantHomePage.objects.filter(tenant=tenant)
                    content_pages = TenantContentPage.objects.filter(tenant=tenant)
                    
                    deleted_pages = 0
                    for page in home_pages:
                        # Delete children first
                        for child in page.get_children():
                            child.delete()
                            deleted_pages += 1
                        page.delete()
                        deleted_pages += 1
                    
                    for page in content_pages:
                        if page.get_parent():  # Only delete if still has parent (not already deleted)
                            page.delete()
                            deleted_pages += 1
                    
                    if deleted_pages > 0:
                        self.stdout.write(f'  Deleted {deleted_pages} pages')
                else:
                    # Unlink pages from tenant
                    updated_pages = TenantHomePage.objects.filter(tenant=tenant).update(tenant=None)
                    updated_pages += TenantContentPage.objects.filter(tenant=tenant).update(tenant=None)
                    if updated_pages > 0:
                        self.stdout.write(f'  Unlinked {updated_pages} pages from tenant')

                # Handle collections
                collections = Collection.objects.filter(name__startswith=tenant.name)
                deleted_collections = collections.count()
                if deleted_collections > 0:
                    collections.delete()
                    self.stdout.write(f'  Deleted {deleted_collections} media collections')

                # Handle Wagtail site
                if tenant.wagtail_site:
                    if not preserve_site:
                        site_name = tenant.wagtail_site.site_name
                        tenant.wagtail_site.delete()
                        self.stdout.write(f'  Deleted Wagtail site: {site_name}')
                    else:
                        # Just unlink the site
                        site_name = tenant.wagtail_site.site_name
                        tenant.wagtail_site = None
                        tenant.save()
                        self.stdout.write(f'  Unlinked Wagtail site: {site_name}')

                # Delete the tenant
                tenant_name = tenant.name
                tenant.delete()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully deleted tenant "{tenant_name}" and associated resources.'
                    )
                )

        except Exception as e:
            raise CommandError(f'Error deleting tenant: {str(e)}')