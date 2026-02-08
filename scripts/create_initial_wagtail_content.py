"""
Create initial Wagtail content for Bizoholic frontend
This script creates homepage and service pages so the frontend displays dynamic content
"""

from wagtail.models import Page, Site
from cms.models import Tenant, ServicePage, BizoholicHomePage
from django.contrib.auth import get_user_model

User = get_user_model()

# Get or create admin user
admin, created = User.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@bizoholic.com', 'is_staff': True, 'is_superuser': True}
)
if created:
    admin.set_password('admin123')
    admin.save()
    print(f"✓ Created admin user")
else:
    print(f"✓ Admin user already exists")

# Get root page
root_page = Page.objects.get(id=1)

# Create or get Wagtail site
site, created = Site.objects.get_or_create(
    hostname='localhost',
    defaults={
        'port': 8002,
        'site_name': 'Bizoholic',
        'root_page': root_page,
        'is_default_site': True
    }
)
print(f"✓ Site: {site.site_name}")

# Create or get tenant
tenant, created = Tenant.objects.get_or_create(
    domain='localhost',
    defaults={
        'name': 'Bizoholic',
        'wagtail_site': site
    }
)
if created:
    print(f"✓ Created tenant: {tenant.name}")
else:
    print(f"✓ Tenant already exists: {tenant.name}")

# Check if homepage already exists
existing_home = BizoholicHomePage.objects.filter(slug='home').first()
if existing_home:
    print(f"✓ Homepage already exists")
    homepage = existing_home
else:
    # Create homepage
    homepage = BizoholicHomePage(
        title="Bizoholic - AI-Powered Marketing",
        slug="home",
        hero_title="Transform Your Business with AI Marketing",
        hero_subtitle="Bizoholic Digital empowers businesses with autonomous AI agents that handle marketing campaigns, content creation, SEO optimization, and lead generation - all running 24/7 on autopilot.",
        hero_cta_text="Start Free Trial",
        hero_cta_url="/portal/register",
        features_title="Everything You Need to Dominate Digital Marketing",
        show_service_status=True,
        live=True
    )
    root_page.add_child(instance=homepage)
    homepage.save_revision().publish()
    print(f"✓ Created homepage: {homepage.title}")

# Create service pages
services_data = [
    {
        'title': 'SEO Optimization & Local SEO',
        'slug': 'seo-optimization',
        'icon': '🔍',
        'badge': 'Most Popular',
        'category': 'Search Marketing',
        'service_description': 'Boost your search rankings with AI-powered SEO optimization. Our advanced algorithms analyze your website, competitors, and search trends to deliver 200% better organic traffic within 90 days.',
        'featured': True,
        'order': 1,
        'starting_price': '$299',
        'currency': 'USD',
        'billing_period': 'month'
    },
    {
        'title': 'Paid Advertising (PPC) Management',
        'slug': 'paid-advertising-ppc',
        'icon': '💰',
        'badge': 'High ROI',
        'category': 'Paid Media',
        'service_description': 'Maximize your ad spend with AI-driven PPC campaigns. Our intelligent bidding algorithms reduce cost-per-click by 45% while increasing conversions by 180%.',
        'featured': True,
        'order': 2,
        'starting_price': '$599',
        'currency': 'USD',
        'billing_period': 'month'
    },
    {
        'title': 'Social Media Marketing & Management',
        'slug': 'social-media-marketing',
        'icon': '📱',
        'badge': 'Trending',
        'category': 'Social Media',
        'service_description': 'Grow your social presence with AI-powered content creation and scheduling. Generate viral-worthy posts, optimize posting times, and engage with your audience automatically.',
        'featured': True,
        'order': 3,
        'starting_price': '$399',
        'currency': 'USD',
        'billing_period': 'month'
    },
    {
        'title': 'Content Generation & Marketing',
        'slug': 'content-generation',
        'icon': '🎯',
        'badge': 'AI-Powered',
        'category': 'Content Marketing',
        'service_description': 'AI-powered content creation for blogs, social media, email campaigns, and website copy that converts visitors into customers.',
        'featured': True,
        'order': 4,
        'starting_price': '$349',
        'currency': 'USD',
        'billing_period': 'month'
    },
    {
        'title': 'Performance Analytics & Reporting',
        'slug': 'performance-analytics',
        'icon': '📊',
        'badge': 'Data-Driven',
        'category': 'Analytics',
        'service_description': 'Real-time analytics and insights with automated reporting that helps you understand what\'s working and what needs optimization.',
        'featured': True,
        'order': 5,
        'starting_price': '$249',
        'currency': 'USD',
        'billing_period': 'month'
    },
    {
        'title': 'AI Campaign Management',
        'slug': 'ai-campaign-management',
        'icon': '🤖',
        'badge': 'Automated',
        'category': 'Campaign Management',
        'service_description': 'Autonomous agents create, optimize, and manage your advertising campaigns across Google Ads, Meta, LinkedIn, and 40+ other platforms.',
        'featured': True,
        'order': 6,
        'starting_price': '$799',
        'currency': 'USD',
        'billing_period': 'month'
    }
]

created_count = 0
for service_data in services_data:
    existing_service = ServicePage.objects.filter(slug=service_data['slug']).first()
    if existing_service:
        print(f"  - Service already exists: {service_data['title']}")
        continue
    
    service_page = ServicePage(
        title=service_data['title'],
        slug=service_data['slug'],
        icon=service_data['icon'],
        badge=service_data['badge'],
        category=service_data['category'],
        service_description=service_data['service_description'],
        featured=service_data['featured'],
        order=service_data['order'],
        starting_price=service_data['starting_price'],
        currency=service_data['currency'],
        billing_period=service_data['billing_period'],
        live=True
    )
    homepage.add_child(instance=service_page)
    service_page.save_revision().publish()
    created_count += 1
    print(f"  ✓ Created service: {service_data['title']}")

if created_count > 0:
    print(f"\n✓ Created {created_count} service pages")
else:
    print(f"\n✓ All service pages already exist")

# Summary
print(f"\n=== Summary ===")
print(f"Total pages: {Page.objects.count()}")
print(f"Service pages: {ServicePage.objects.count()}")
print(f"Homepage: {BizoholicHomePage.objects.count()}")
print(f"\n✓ Initial content creation complete!")
print(f"\nFrontend should now display service cards at: http://localhost:3001")
