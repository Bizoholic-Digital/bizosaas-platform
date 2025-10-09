"""
Django management command to create and configure multi-tenant Wagtail sites
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from wagtail.models import Site as WagtailSite, Page
from wagtail.core.models import Collection
from cms.models import Tenant
import uuid


class Command(BaseCommand):
    help = 'Create a new tenant with associated Wagtail site and pages'

    def add_arguments(self, parser):
        parser.add_argument(
            'name',
            type=str,
            help='Tenant name'
        )
        parser.add_argument(
            'domain',
            type=str,
            help='Primary domain for the tenant'
        )
        parser.add_argument(
            '--subdomain',
            type=str,
            help='Subdomain prefix (e.g., "client1" for client1.bizosaas.com)',
            default=None
        )
        parser.add_argument(
            '--bizosaas-tenant-id',
            type=str,
            help='BizOSaaS tenant ID (UUID format)',
            default=None
        )
        parser.add_argument(
            '--port',
            type=int,
            help='Port for Wagtail site (default: 80)',
            default=80
        )
        parser.add_argument(
            '--theme',
            type=str,
            help='Theme settings JSON string',
            default='{"primary_color": "#007cba", "font_family": "Inter"}'
        )
        parser.add_argument(
            '--is-active',
            action='store_true',
            help='Set tenant as active (default: True)',
            default=True
        )

    def handle(self, *args, **options):
        name = options['name']
        domain = options['domain']
        subdomain = options.get('subdomain')
        bizosaas_tenant_id = options.get('bizosaas_tenant_id') or str(uuid.uuid4())
        port = options['port']
        theme = options['theme']
        is_active = options['is_active']

        try:
            with transaction.atomic():
                # Check if tenant already exists
                if Tenant.objects.filter(bizosaas_tenant_id=bizosaas_tenant_id).exists():
                    raise CommandError(f'Tenant with BizOSaaS ID {bizosaas_tenant_id} already exists')

                if Tenant.objects.filter(domain=domain).exists():
                    raise CommandError(f'Tenant with domain {domain} already exists')

                # Check if Wagtail site already exists for this domain
                if WagtailSite.objects.filter(hostname=domain, port=port).exists():
                    raise CommandError(f'Wagtail site for {domain}:{port} already exists')

                self.stdout.write(f'Creating tenant: {name}')
                self.stdout.write(f'Domain: {domain}')
                self.stdout.write(f'Subdomain: {subdomain or "None"}')
                self.stdout.write(f'BizOSaaS Tenant ID: {bizosaas_tenant_id}')

                # Create the tenant first
                tenant = Tenant(
                    name=name,
                    domain=domain,
                    subdomain=subdomain,
                    bizosaas_tenant_id=bizosaas_tenant_id,
                    is_active=is_active,
                    theme_settings=theme,
                    seo_settings='{"meta_title": "' + name + '", "meta_description": "Welcome to ' + name + '"}',
                    api_settings='{"rate_limit": 1000, "cors_origins": []}'
                )
                
                # Don't save yet - we need to create the Wagtail site first
                self.stdout.write('Creating Wagtail site...')
                
                # Get the root page (usually Home page)
                try:
                    root_page = Page.objects.get(slug='home', depth=2)
                except Page.DoesNotExist:
                    # If no home page, get the first available page at depth 2
                    root_page = Page.objects.filter(depth=2).first()
                    if not root_page:
                        raise CommandError('No root page found. Please ensure Wagtail is properly set up.')

                # Create Wagtail site
                wagtail_site = WagtailSite.objects.create(
                    hostname=domain,
                    port=port,
                    site_name=name,
                    root_page=root_page,
                    is_default_site=False
                )

                # Now assign the site to the tenant and save
                tenant.wagtail_site = wagtail_site
                tenant.save()

                self.stdout.write('Creating tenant-specific pages...')
                
                # Create a tenant-specific home page under the root
                from cms.models import TenantHomePage
                tenant_home = TenantHomePage(
                    title=f'{name} - Home',
                    slug=f'{name.lower().replace(" ", "-")}-home',
                    tenant=tenant,
                    seo_title=f'{name} - Home',
                    search_description=f'Welcome to {name}. Discover our services and solutions.',
                    show_in_menus=True
                )
                
                # Add as child of root page
                root_page.add_child(instance=tenant_home)
                
                # Update the site to use the tenant home page as root
                wagtail_site.root_page = tenant_home
                wagtail_site.save()

                # Create tenant-specific collection
                collection = Collection.objects.create(
                    name=f'{name} Media',
                    parent=Collection.get_first_root_node()
                )

                self.stdout.write('Setting up default pages...')
                
                # Create additional default pages for the tenant
                from cms.models import TenantContentPage
                
                # About page
                about_page = TenantContentPage(
                    title='About Us',
                    slug='about',
                    tenant=tenant,
                    seo_title=f'About {name}',
                    search_description=f'Learn more about {name} and our mission.',
                    show_in_menus=True,
                    body='<h2>About Us</h2><p>Welcome to our about page. Add your content here.</p>'
                )
                tenant_home.add_child(instance=about_page)

                # Services page
                services_page = TenantContentPage(
                    title='Services',
                    slug='services',
                    tenant=tenant,
                    seo_title=f'{name} Services',
                    search_description=f'Discover the services offered by {name}.',
                    show_in_menus=True,
                    body='<h2>Our Services</h2><p>Explore our range of services. Add your content here.</p>'
                )
                tenant_home.add_child(instance=services_page)

                # Contact page
                contact_page = TenantContentPage(
                    title='Contact',
                    slug='contact',
                    tenant=tenant,
                    seo_title=f'Contact {name}',
                    search_description=f'Get in touch with {name}. Find our contact information here.',
                    show_in_menus=True,
                    body='<h2>Contact Us</h2><p>Get in touch with us. Add your contact information here.</p>'
                )
                tenant_home.add_child(instance=contact_page)

                # Publish all pages
                tenant_home.save_revision().publish()
                about_page.save_revision().publish()
                services_page.save_revision().publish()
                contact_page.save_revision().publish()

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created tenant "{name}" with:\n'
                        f'  - BizOSaaS Tenant ID: {bizosaas_tenant_id}\n'
                        f'  - Domain: {domain}:{port}\n'
                        f'  - Subdomain: {subdomain or "None"}\n'
                        f'  - Wagtail Site ID: {wagtail_site.id}\n'
                        f'  - Home Page ID: {tenant_home.id}\n'
                        f'  - Collection ID: {collection.id}\n'
                        f'  - Default pages: About, Services, Contact\n'
                        f'  - Status: {"Active" if is_active else "Inactive"}'
                    )
                )

        except Exception as e:
            raise CommandError(f'Error creating tenant: {str(e)}')