"""
Management command to set up initial leads data
Creates default sources, tags, and sample data
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.tenants.models import Tenant
from apps.leads.models import LeadSource, LeadTag


class Command(BaseCommand):
    """Command to setup initial leads data"""
    help = 'Set up initial lead sources, tags, and sample data for tenants'
    
    def add_arguments(self, parser):
        """Add command arguments"""
        parser.add_argument(
            '--tenant-slug',
            type=str,
            help='Specific tenant slug to setup data for',
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Skip if data already exists',
        )
    
    def handle(self, *args, **options):
        """Handle the command"""
        tenant_slug = options.get('tenant_slug')
        skip_existing = options.get('skip_existing')
        
        if tenant_slug:
            try:
                tenant = Tenant.objects.get(slug=tenant_slug)
                tenants = [tenant]
            except Tenant.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Tenant with slug "{tenant_slug}" not found')
                )
                return
        else:
            tenants = Tenant.objects.filter(is_active=True)
        
        for tenant in tenants:
            self.setup_tenant_data(tenant, skip_existing)
    
    def setup_tenant_data(self, tenant, skip_existing=False):
        """Setup data for a specific tenant"""
        self.stdout.write(f'Setting up data for tenant: {tenant.name}')
        
        with transaction.atomic():
            # Create default lead sources
            sources_created = self.create_lead_sources(tenant, skip_existing)
            
            # Create default lead tags  
            tags_created = self.create_lead_tags(tenant, skip_existing)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Created {sources_created} sources and {tags_created} tags for {tenant.name}'
                )
            )
    
    def create_lead_sources(self, tenant, skip_existing):
        """Create default lead sources"""
        default_sources = [
            {
                'name': 'Website',
                'description': 'Leads from company website contact forms'
            },
            {
                'name': 'Social Media', 
                'description': 'Leads from social media platforms'
            },
            {
                'name': 'Email Campaign',
                'description': 'Leads from email marketing campaigns'
            },
            {
                'name': 'Google Ads',
                'description': 'Leads from Google advertising campaigns'
            },
            {
                'name': 'LinkedIn',
                'description': 'Leads from LinkedIn outreach and ads'
            },
            {
                'name': 'Referral',
                'description': 'Leads from customer referrals'
            },
            {
                'name': 'Cold Outreach',
                'description': 'Leads from cold calling or emailing'
            },
            {
                'name': 'Trade Show',
                'description': 'Leads from trade shows and events'
            },
            {
                'name': 'Partner',
                'description': 'Leads from business partners'
            },
            {
                'name': 'Content Marketing',
                'description': 'Leads from blog posts, whitepapers, webinars'
            },
        ]
        
        created_count = 0
        for source_data in default_sources:
            source, created = LeadSource.objects.get_or_create(
                tenant=tenant,
                name=source_data['name'],
                defaults={
                    'description': source_data['description'],
                    'is_active': True
                }
            )
            
            if created or not skip_existing:
                created_count += 1
                self.stdout.write(f'  ✓ Created source: {source.name}')
        
        return created_count
    
    def create_lead_tags(self, tenant, skip_existing):
        """Create default lead tags"""
        default_tags = [
            {
                'name': 'Hot Lead',
                'color': '#ff4444',
                'description': 'High-priority leads requiring immediate attention'
            },
            {
                'name': 'Warm Lead',
                'color': '#ff8800',
                'description': 'Engaged leads showing interest'
            },
            {
                'name': 'Cold Lead',
                'color': '#4488ff',
                'description': 'Early-stage leads requiring nurturing'
            },
            {
                'name': 'Enterprise',
                'color': '#9944ff',
                'description': 'Large enterprise prospects'
            },
            {
                'name': 'SMB',
                'color': '#44ff88',
                'description': 'Small to medium business prospects'
            },
            {
                'name': 'Decision Maker',
                'color': '#ff0088',
                'description': 'Contact is a decision maker'
            },
            {
                'name': 'Budget Approved',
                'color': '#00ff44',
                'description': 'Budget has been approved'
            },
            {
                'name': 'Demo Requested',
                'color': '#ffaa00',
                'description': 'Prospect has requested a demo'
            },
            {
                'name': 'Proposal Sent',
                'color': '#aa00ff',
                'description': 'Proposal has been sent to prospect'
            },
            {
                'name': 'Follow Up',
                'color': '#00aaff',
                'description': 'Requires follow up contact'
            },
            {
                'name': 'New Technology',
                'color': '#444444',
                'description': 'Interested in new technology solutions'
            },
            {
                'name': 'Existing Customer',
                'color': '#ff4400',
                'description': 'Existing customer for upsell/cross-sell'
            },
        ]
        
        created_count = 0
        for tag_data in default_tags:
            tag, created = LeadTag.objects.get_or_create(
                tenant=tenant,
                name=tag_data['name'],
                defaults={
                    'color': tag_data['color'],
                    'description': tag_data['description'],
                    'is_active': True
                }
            )
            
            if created or not skip_existing:
                created_count += 1
                self.stdout.write(f'  ✓ Created tag: {tag.name}')
        
        return created_count