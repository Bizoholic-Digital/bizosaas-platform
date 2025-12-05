"""
Django management command to list all tenants and their configuration
"""

from django.core.management.base import BaseCommand
from cms.models import Tenant
from wagtail.models import Site as WagtailSite
from django.utils import timezone
import json


class Command(BaseCommand):
    help = 'List all tenants and their configuration details'

    def add_arguments(self, parser):
        parser.add_argument(
            '--active-only',
            action='store_true',
            help='Show only active tenants',
            default=False
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['table', 'json'],
            help='Output format (default: table)',
            default='table'
        )
        parser.add_argument(
            '--domain',
            type=str,
            help='Filter by domain (partial match)',
            default=None
        )

    def handle(self, *args, **options):
        active_only = options['active_only']
        output_format = options['format']
        domain_filter = options.get('domain')

        # Build queryset
        queryset = Tenant.objects.select_related('wagtail_site').all()
        
        if active_only:
            queryset = queryset.filter(is_active=True)
        
        if domain_filter:
            queryset = queryset.filter(domain__icontains=domain_filter)

        tenants = list(queryset.order_by('created_at'))

        if not tenants:
            filter_desc = []
            if active_only:
                filter_desc.append("active")
            if domain_filter:
                filter_desc.append(f"domain containing '{domain_filter}'")
            
            filter_text = " and ".join(filter_desc)
            if filter_text:
                self.stdout.write(f'No {filter_text} tenants found.')
            else:
                self.stdout.write('No tenants found.')
            return

        if output_format == 'json':
            self._output_json(tenants)
        else:
            self._output_table(tenants)

    def _output_table(self, tenants):
        """Output tenants in table format"""
        
        # Header
        self.stdout.write(
            self.style.SUCCESS(
                f"{'ID':<8} {'Name':<20} {'Domain':<25} {'Subdomain':<15} {'Site ID':<8} {'Status':<8} {'Created':<12}"
            )
        )
        self.stdout.write("-" * 98)

        # Rows
        for tenant in tenants:
            site_id = tenant.wagtail_site.id if tenant.wagtail_site else 'None'
            status = 'Active' if tenant.is_active else 'Inactive'
            created = tenant.created_at.strftime('%Y-%m-%d') if hasattr(tenant, 'created_at') else 'Unknown'
            subdomain = tenant.subdomain or 'None'
            
            # Truncate long names/domains
            name = tenant.name[:19] + '…' if len(tenant.name) > 20 else tenant.name
            domain = tenant.domain[:24] + '…' if len(tenant.domain) > 25 else tenant.domain
            subdomain = subdomain[:14] + '…' if len(subdomain) > 15 else subdomain

            self.stdout.write(
                f"{str(tenant.id)[:8]:<8} {name:<20} {domain:<25} {subdomain:<15} {str(site_id):<8} {status:<8} {created:<12}"
            )

        self.stdout.write(f"\nTotal: {len(tenants)} tenant(s)")

        # Summary statistics
        active_count = sum(1 for t in tenants if t.is_active)
        with_sites = sum(1 for t in tenants if t.wagtail_site)
        
        self.stdout.write(f"Active: {active_count}")
        self.stdout.write(f"With Wagtail Sites: {with_sites}")

    def _output_json(self, tenants):
        """Output tenants in JSON format"""
        
        tenant_data = []
        
        for tenant in tenants:
            data = {
                'id': str(tenant.id),
                'name': tenant.name,
                'domain': tenant.domain,
                'subdomain': tenant.subdomain,
                'bizosaas_tenant_id': tenant.bizosaas_tenant_id,
                'is_active': tenant.is_active,
                'wagtail_site': {
                    'id': tenant.wagtail_site.id if tenant.wagtail_site else None,
                    'hostname': tenant.wagtail_site.hostname if tenant.wagtail_site else None,
                    'port': tenant.wagtail_site.port if tenant.wagtail_site else None,
                    'site_name': tenant.wagtail_site.site_name if tenant.wagtail_site else None,
                    'is_default': tenant.wagtail_site.is_default_site if tenant.wagtail_site else None
                },
                'settings': {
                    'theme': json.loads(tenant.theme_settings) if tenant.theme_settings else {},
                    'seo': json.loads(tenant.seo_settings) if tenant.seo_settings else {},
                    'api': json.loads(tenant.api_settings) if tenant.api_settings else {}
                }
            }
            
            # Add created_at if available
            if hasattr(tenant, 'created_at'):
                data['created_at'] = tenant.created_at.isoformat()
            
            # Add updated_at if available
            if hasattr(tenant, 'updated_at'):
                data['updated_at'] = tenant.updated_at.isoformat()
            
            tenant_data.append(data)

        # Output JSON
        self.stdout.write(json.dumps({
            'tenants': tenant_data,
            'total_count': len(tenants),
            'active_count': sum(1 for t in tenants if t.is_active),
            'with_sites_count': sum(1 for t in tenants if t.wagtail_site),
            'generated_at': timezone.now().isoformat()
        }, indent=2))