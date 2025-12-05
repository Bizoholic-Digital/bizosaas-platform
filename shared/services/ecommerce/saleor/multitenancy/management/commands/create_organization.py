"""
Django management command to create and configure multi-tenant organizations
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.sites.models import Site
from django.utils.text import slugify
from saleor.multitenancy.models import Organization, OrganizationSettings
import uuid


class Command(BaseCommand):
    help = 'Create a new organization with associated site and configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            'name',
            type=str,
            help='Organization name'
        )
        parser.add_argument(
            'domain',
            type=str,
            help='Primary domain for the organization'
        )
        parser.add_argument(
            '--slug',
            type=str,
            help='URL-safe organization slug (auto-generated if not provided)',
            default=None
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
            '--subscription-tier',
            type=str,
            choices=['tier_1', 'tier_2', 'tier_3'],
            help='Subscription tier',
            default='tier_1'
        )
        parser.add_argument(
            '--primary-color',
            type=str,
            help='Primary brand color (hex format)',
            default='#007cba'
        )
        parser.add_argument(
            '--secondary-color',
            type=str,
            help='Secondary brand color (hex format)',
            default='#6c757d'
        )
        parser.add_argument(
            '--currency',
            type=str,
            help='Default currency code',
            default='USD'
        )
        parser.add_argument(
            '--is-active',
            action='store_true',
            help='Set organization as active (default: True)',
            default=True
        )

    def handle(self, *args, **options):
        name = options['name']
        domain = options['domain']
        slug = options.get('slug') or slugify(name)
        subdomain = options.get('subdomain')
        bizosaas_tenant_id = options.get('bizosaas_tenant_id') or str(uuid.uuid4())
        subscription_tier = options['subscription_tier']
        primary_color = options['primary_color']
        secondary_color = options['secondary_color']
        currency = options['currency']
        is_active = options['is_active']

        try:
            with transaction.atomic():
                # Check if organization already exists
                if Organization.objects.filter(bizosaas_tenant_id=bizosaas_tenant_id).exists():
                    raise CommandError(f'Organization with BizOSaaS ID {bizosaas_tenant_id} already exists')

                if Organization.objects.filter(domain=domain).exists():
                    raise CommandError(f'Organization with domain {domain} already exists')

                if Organization.objects.filter(slug=slug).exists():
                    raise CommandError(f'Organization with slug {slug} already exists')

                # Check if Site already exists for this domain
                if Site.objects.filter(domain=domain).exists():
                    raise CommandError(f'Site for {domain} already exists')

                self.stdout.write(f'Creating organization: {name}')
                self.stdout.write(f'Domain: {domain}')
                self.stdout.write(f'Slug: {slug}')
                self.stdout.write(f'Subdomain: {subdomain or "None"}')
                self.stdout.write(f'BizOSaaS Tenant ID: {bizosaas_tenant_id}')
                self.stdout.write(f'Subscription Tier: {subscription_tier}')

                # Create Django Site first
                self.stdout.write('Creating Django site...')
                site = Site.objects.create(
                    domain=domain,
                    name=name
                )

                # Create the organization
                tier_limits = self._get_tier_limits(subscription_tier)
                
                organization = Organization.objects.create(
                    name=name,
                    slug=slug,
                    domain=domain,
                    subdomain=subdomain,
                    bizosaas_tenant_id=bizosaas_tenant_id,
                    site=site,
                    is_active=is_active,
                    subscription_tier=subscription_tier,
                    primary_color=primary_color,
                    secondary_color=secondary_color,
                    max_products=tier_limits['max_products'],
                    max_orders_per_month=tier_limits['max_orders_per_month'],
                    max_staff_users=tier_limits['max_staff_users'],
                    storage_limit_gb=tier_limits['storage_limit_gb'],
                    settings={
                        'features': tier_limits['features'],
                        'created_via': 'management_command'
                    }
                )

                # Create organization settings
                self.stdout.write('Creating organization settings...')
                OrganizationSettings.objects.create(
                    organization=organization,
                    currency=currency,
                    tax_calculation=True,
                    inventory_tracking=True,
                    guest_checkout_enabled=True,
                    account_required=False,
                    order_confirmation_email=True,
                    shipping_confirmation_email=True,
                    api_settings={
                        'rate_limit': tier_limits.get('api_rate_limit', 1000),
                        'allowed_origins': []
                    },
                    webhook_settings={
                        'enabled': False,
                        'endpoints': []
                    }
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created organization "{name}" with:\n'
                        f'  - Organization ID: {organization.id}\n'
                        f'  - Slug: {slug}\n'
                        f'  - BizOSaaS Tenant ID: {bizosaas_tenant_id}\n'
                        f'  - Domain: {domain}\n'
                        f'  - Subdomain: {subdomain or "None"}\n'
                        f'  - Site ID: {site.id}\n'
                        f'  - Subscription Tier: {subscription_tier}\n'
                        f'  - Max Products: {tier_limits["max_products"]}\n'
                        f'  - Max Orders/Month: {tier_limits["max_orders_per_month"]}\n'
                        f'  - Max Staff: {tier_limits["max_staff_users"]}\n'
                        f'  - Storage Limit: {tier_limits["storage_limit_gb"]}GB\n'
                        f'  - Features: {", ".join(tier_limits["features"])}\n'
                        f'  - Status: {"Active" if is_active else "Inactive"}'
                    )
                )

        except Exception as e:
            raise CommandError(f'Error creating organization: {str(e)}')

    def _get_tier_limits(self, tier):
        """Get limits and features based on subscription tier"""
        tier_configs = {
            'tier_1': {
                'max_products': 100,
                'max_orders_per_month': 1000,
                'max_staff_users': 5,
                'storage_limit_gb': 10,
                'api_rate_limit': 1000,
                'features': ['basic_ecommerce', 'basic_cms', 'basic_crm']
            },
            'tier_2': {
                'max_products': 1000,
                'max_orders_per_month': 10000,
                'max_staff_users': 20,
                'storage_limit_gb': 100,
                'api_rate_limit': 5000,
                'features': ['advanced_ecommerce', 'advanced_cms', 'advanced_crm', 'ai_agents', 'analytics']
            },
            'tier_3': {
                'max_products': 99999,  # Effectively unlimited
                'max_orders_per_month': 99999,  # Effectively unlimited
                'max_staff_users': 999,  # Effectively unlimited
                'storage_limit_gb': 1000,
                'api_rate_limit': 10000,
                'features': ['full_platform', 'premium_support', 'custom_integrations', 'white_label']
            }
        }
        return tier_configs.get(tier, tier_configs['tier_1'])