"""
Management command to create initial Bizoholic content in Wagtail
"""
from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from cms.models import BizoholicHomePage, ServicePage
from django.db import transaction


class Command(BaseCommand):
    help = 'Creates initial Bizoholic content pages in Wagtail'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Creating Bizoholic content...')
        
        # Get or create the root page
        try:
            root_page = Page.objects.get(depth=1)
        except Page.DoesNotExist:
            self.stdout.write(self.style.ERROR('Root page not found. Run migrations first.'))
            return
        
        # Check if homepage already exists
        if BizoholicHomePage.objects.exists():
            self.stdout.write(self.style.WARNING('Homepage already exists. Skipping creation.'))
            homepage = BizoholicHomePage.objects.first()
        else:
            # Create homepage
            homepage = BizoholicHomePage(
                title='Bizoholic - AI-Powered Marketing Automation',
                slug='home',
                hero_title='AI-Powered Marketing Automation',
                hero_subtitle='Transform your marketing with AI automation. Get 75% cost savings, ROI within 7 days, and setup in 15 minutes. The smartest marketing platform for small businesses.',
                hero_cta_text='Get Started Free',
                hero_cta_url='/contact',
                features_title='Why Choose Bizoholic?',
                show_service_status=True,
            )
            root_page.add_child(instance=homepage)
            homepage.save_revision().publish()
            self.stdout.write(self.style.SUCCESS(f'✓ Created homepage: {homepage.title}'))
        
        # Create service pages
        services_data = [
            {
                'title': 'AI Campaign Management',
                'slug': 'ai-campaign-management',
                'service_description': 'Autonomous agents create, optimize, and manage your advertising campaigns across Google Ads, Meta, LinkedIn, and 40+ other platforms.',
                'icon': '🤖',
                'category': 'AI Marketing',
                'featured': True,
                'order': 1,
            },
            {
                'title': 'Content Generation',
                'slug': 'content-generation',
                'service_description': 'AI-powered content creation for blogs, social media, email campaigns, and website copy that converts visitors into customers.',
                'icon': '🎯',
                'category': 'Content',
                'featured': True,
                'order': 2,
            },
            {
                'title': 'Performance Analytics',
                'slug': 'performance-analytics',
                'service_description': 'Real-time analytics and insights with automated reporting that helps you understand what\'s working and what needs optimization.',
                'icon': '📊',
                'category': 'Analytics',
                'featured': True,
                'order': 3,
            },
            {
                'title': 'SEO Optimization',
                'slug': 'seo-optimization',
                'service_description': 'AI-driven SEO strategies that improve your search rankings and drive organic traffic to your website.',
                'icon': '🔍',
                'category': 'SEO',
                'featured': False,
                'order': 4,
            },
            {
                'title': 'Social Media Marketing',
                'slug': 'social-media-marketing',
                'service_description': 'Automated social media management across all major platforms with AI-generated content and optimal posting schedules.',
                'icon': '📱',
                'category': 'Social Media',
                'featured': False,
                'order': 5,
            },
            {
                'title': 'Email Marketing',
                'slug': 'email-marketing',
                'service_description': 'Personalized email campaigns with AI-powered segmentation, content generation, and send-time optimization.',
                'icon': '📧',
                'category': 'Email',
                'featured': False,
                'order': 6,
            },
        ]
        
        for service_data in services_data:
            # Check if service already exists
            if ServicePage.objects.filter(slug=service_data['slug']).exists():
                self.stdout.write(self.style.WARNING(f'Service "{service_data["title"]}" already exists. Skipping.'))
                continue
            
            service = ServicePage(
                **service_data
            )
            homepage.add_child(instance=service)
            service.save_revision().publish()
            self.stdout.write(self.style.SUCCESS(f'✓ Created service: {service.title}'))
        
        # Set the site root page to homepage if not already set
        try:
            site = Site.objects.get(is_default_site=True)
            if site.root_page != homepage:
                site.root_page = homepage
                site.save()
                self.stdout.write(self.style.SUCCESS('✓ Set homepage as site root'))
        except Site.DoesNotExist:
            # Create default site
            site = Site.objects.create(
                hostname='localhost',
                port=8002,
                site_name='Bizoholic',
                root_page=homepage,
                is_default_site=True
            )
            self.stdout.write(self.style.SUCCESS('✓ Created default site'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Bizoholic content created successfully!'))
        self.stdout.write(f'Homepage: {homepage.url}')
        self.stdout.write(f'Services created: {len(services_data)}')
