"""
Django management command to synchronize tenant-site relationships and fix inconsistencies
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from wagtail.models import Site as WagtailSite, Page
from cms.models import Tenant
from django.contrib.sites.models import Site as DjangoSite


class Command(BaseCommand):
    help = 'Synchronize tenant-site relationships and fix inconsistencies'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without making changes',
            default=False
        )
        parser.add_argument(
            '--create-missing-sites',
            action='store_true',
            help='Create Wagtail sites for tenants that don\'t have them',
            default=False
        )
        parser.add_argument(
            '--create-missing-django-sites',
            action='store_true',
            help='Create Django sites for Wagtail sites that don\'t have them',
            default=False
        )
        parser.add_argument(
            '--fix-orphaned-sites',
            action='store_true',
            help='Link orphaned Wagtail sites to tenants where possible',
            default=False
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Run all sync operations',
            default=False
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        create_missing_sites = options['create_missing_sites'] or options['all']
        create_missing_django_sites = options['create_missing_django_sites'] or options['all']
        fix_orphaned_sites = options['fix_orphaned_sites'] or options['all']

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))

        self.stdout.write('Analyzing tenant-site relationships...\n')

        # Get all tenants and sites
        tenants = Tenant.objects.select_related('wagtail_site').all()
        wagtail_sites = WagtailSite.objects.all()
        django_sites = DjangoSite.objects.all()

        # Analysis
        tenants_without_sites = [t for t in tenants if not t.wagtail_site]
        tenants_with_sites = [t for t in tenants if t.wagtail_site]
        
        # Find orphaned Wagtail sites (not linked to any tenant)
        linked_site_ids = {t.wagtail_site.id for t in tenants_with_sites}
        orphaned_sites = [s for s in wagtail_sites if s.id not in linked_site_ids]

        # Find Wagtail sites without Django sites
        django_hostnames = {s.domain for s in django_sites}
        wagtail_sites_without_django = [
            s for s in wagtail_sites 
            if s.hostname not in django_hostnames
        ]

        # Report current state
        self.stdout.write(f'Current State:')
        self.stdout.write(f'  Total tenants: {len(tenants)}')
        self.stdout.write(f'  Tenants with sites: {len(tenants_with_sites)}')
        self.stdout.write(f'  Tenants without sites: {len(tenants_without_sites)}')
        self.stdout.write(f'  Total Wagtail sites: {len(wagtail_sites)}')
        self.stdout.write(f'  Orphaned Wagtail sites: {len(orphaned_sites)}')
        self.stdout.write(f'  Wagtail sites without Django sites: {len(wagtail_sites_without_django)}')

        changes_made = 0

        # 1. Create missing Wagtail sites for tenants
        if create_missing_sites and tenants_without_sites:
            self.stdout.write(f'\n1. Creating Wagtail sites for {len(tenants_without_sites)} tenants...')
            
            # Get root page
            try:
                root_page = Page.objects.get(slug='home', depth=2)
            except Page.DoesNotExist:
                root_page = Page.objects.filter(depth=2).first()
                if not root_page:
                    self.stdout.write(self.style.ERROR('No root page found. Cannot create sites.'))
                    return

            for tenant in tenants_without_sites:
                if not dry_run:
                    with transaction.atomic():
                        # Check if site already exists for this domain
                        existing_site = WagtailSite.objects.filter(
                            hostname=tenant.domain
                        ).first()
                        
                        if existing_site:
                            # Link existing site to tenant
                            tenant.wagtail_site = existing_site
                            tenant.save()
                            self.stdout.write(f'  Linked existing site to {tenant.name}')
                        else:
                            # Create new site
                            site = WagtailSite.objects.create(
                                hostname=tenant.domain,
                                port=80,
                                site_name=tenant.name,
                                root_page=root_page,
                                is_default_site=False
                            )
                            tenant.wagtail_site = site
                            tenant.save()
                            self.stdout.write(f'  Created site for {tenant.name} ({tenant.domain})')
                else:
                    self.stdout.write(f'  Would create site for {tenant.name} ({tenant.domain})')
                
                changes_made += 1

        # 2. Fix orphaned sites
        if fix_orphaned_sites and orphaned_sites:
            self.stdout.write(f'\n2. Fixing {len(orphaned_sites)} orphaned sites...')
            
            for site in orphaned_sites:
                # Try to find a tenant that matches this site's hostname
                matching_tenant = Tenant.objects.filter(
                    domain=site.hostname,
                    wagtail_site__isnull=True
                ).first()
                
                if matching_tenant:
                    if not dry_run:
                        matching_tenant.wagtail_site = site
                        matching_tenant.save()
                        self.stdout.write(f'  Linked site {site.site_name} to tenant {matching_tenant.name}')
                    else:
                        self.stdout.write(f'  Would link site {site.site_name} to tenant {matching_tenant.name}')
                    changes_made += 1
                else:
                    self.stdout.write(f'  No matching tenant found for site {site.site_name} ({site.hostname})')

        # 3. Create missing Django sites
        if create_missing_django_sites and wagtail_sites_without_django:
            self.stdout.write(f'\n3. Creating Django sites for {len(wagtail_sites_without_django)} Wagtail sites...')
            
            for wagtail_site in wagtail_sites_without_django:
                if not dry_run:
                    django_site = DjangoSite.objects.create(
                        domain=wagtail_site.hostname,
                        name=wagtail_site.site_name
                    )
                    self.stdout.write(f'  Created Django site for {wagtail_site.site_name}')
                else:
                    self.stdout.write(f'  Would create Django site for {wagtail_site.site_name}')
                changes_made += 1

        # Final report
        if dry_run:
            self.stdout.write(f'\nDry run complete. {changes_made} changes would be made.')
        else:
            if changes_made > 0:
                self.stdout.write(self.style.SUCCESS(f'\nSync complete. {changes_made} changes made.'))
            else:
                self.stdout.write(self.style.SUCCESS('\nSync complete. No changes needed.'))

        # Post-sync verification
        self.stdout.write('\nPost-sync verification:')
        tenants_refreshed = Tenant.objects.select_related('wagtail_site').all()
        tenants_still_without_sites = [t for t in tenants_refreshed if not t.wagtail_site]
        
        if tenants_still_without_sites:
            self.stdout.write(f'  ⚠️  {len(tenants_still_without_sites)} tenants still without sites:')
            for tenant in tenants_still_without_sites:
                self.stdout.write(f'    - {tenant.name} ({tenant.domain})')
        else:
            self.stdout.write(f'  ✅ All tenants now have associated Wagtail sites')