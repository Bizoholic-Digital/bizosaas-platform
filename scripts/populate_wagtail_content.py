#!/usr/bin/env python
"""
Populate Wagtail CMS with initial content for Bizoholic
All content will be manageable through the Wagtail admin panel
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagtail_cms.settings.production')
django.setup()

from wagtail.models import Page, Site
from cms.models import Tenant, ServicePage, BizoholicHomePage
from django.contrib.auth import get_user_model

User = get_user_model()

def create_content():
    print("=" * 60)
    print("Creating Wagtail Content for Bizoholic")
    print("=" * 60)
    
    # 1. Ensure admin user exists
    print("\n1. Setting up admin user...")
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@bizoholic.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print("   ✓ Created admin user (username: admin, password: admin123)")
    else:
        print("   ✓ Admin user already exists")
    
    # 2. Setup site
    print("\n2. Setting up Wagtail site...")
    root_page = Page.objects.get(id=1)
    
    site, created = Site.objects.get_or_create(
        hostname='localhost',
        defaults={
            'port': 8002,
            'site_name': 'Bizoholic Digital',
            'root_page': root_page,
            'is_default_site': True
        }
    )
    print(f"   ✓ Site: {site.site_name} ({site.hostname}:{site.port})")
    
    # 3. Create tenant
    print("\n3. Setting up tenant...")
    tenant, created = Tenant.objects.get_or_create(
        domain='localhost',
        defaults={
            'name': 'Bizoholic',
            'wagtail_site': site
        }
    )
    if created:
        print(f"   ✓ Created tenant: {tenant.name}")
    else:
        print(f"   ✓ Tenant exists: {tenant.name}")
    
    # 4. Create homepage
    print("\n4. Creating homepage...")
    existing_home = BizoholicHomePage.objects.filter(slug='home').first()
    
    if existing_home:
        print("   ✓ Homepage already exists, updating...")
        homepage = existing_home
        homepage.hero_title = "Transform Your Business with AI Marketing"
        homepage.hero_subtitle = "Bizoholic Digital empowers businesses with autonomous AI agents that handle marketing campaigns, content creation, SEO optimization, and lead generation - all running 24/7 on autopilot."
        homepage.save_revision().publish()
    else:
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
        print(f"   ✓ Created homepage: {homepage.title}")
    
    # 5. Create service pages
    print("\n5. Creating service pages...")
    
    services_data = [
        {
            'title': 'SEO Optimization & Local SEO',
            'slug': 'seo-optimization',
            'icon': '🔍',
            'badge': 'Most Popular',
            'category': 'Search Marketing',
            'service_description': '''Boost your search rankings with AI-powered SEO optimization. Our advanced algorithms analyze your website, competitors, and search trends to deliver exceptional results.

**What You Get:**
- Comprehensive SEO audit and strategy
- On-page and technical SEO optimization
- Local SEO for multi-location businesses
- Keyword research and content optimization
- Monthly performance reports and insights

**Results:** 200% increase in organic traffic within 90 days (average client result)''',
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
            'service_description': '''Maximize your ad spend with AI-driven PPC campaigns across Google Ads, Facebook, Instagram, LinkedIn, and more.

**What You Get:**
- AI-powered bid optimization
- Ad copy creation and A/B testing
- Audience targeting and segmentation
- Landing page optimization
- Real-time performance monitoring

**Results:** 45% reduction in cost-per-click, 180% increase in conversions''',
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
            'service_description': '''Grow your social presence with AI-powered content creation, scheduling, and community management across all major platforms.

**What You Get:**
- AI-generated content calendar
- Viral-worthy post creation
- Optimal posting time analysis
- Community engagement automation
- Influencer collaboration management

**Results:** 300% increase in engagement, 150% follower growth in 6 months''',
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
            'service_description': '''AI-powered content creation for blogs, social media, email campaigns, and website copy that converts visitors into customers.

**What You Get:**
- Blog post and article writing
- Email campaign content
- Social media captions and posts
- Website copy and landing pages
- SEO-optimized content

**Results:** 10x faster content production, 85% reduction in content costs''',
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
            'service_description': '''Real-time analytics and insights with automated reporting that helps you understand what's working and what needs optimization.

**What You Get:**
- Custom analytics dashboards
- Automated weekly/monthly reports
- ROI tracking across all channels
- Competitor analysis
- Predictive performance insights

**Results:** Make data-driven decisions 5x faster with actionable insights''',
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
            'service_description': '''Autonomous AI agents create, optimize, and manage your advertising campaigns across Google Ads, Meta, LinkedIn, and 40+ other platforms.

**What You Get:**
- Multi-platform campaign orchestration
- Automated budget allocation
- Real-time optimization
- Creative testing and iteration
- 24/7 campaign monitoring

**Results:** 60% time savings, 120% improvement in campaign performance''',
            'featured': True,
            'order': 6,
            'starting_price': '$799',
            'currency': 'USD',
            'billing_period': 'month'
        },
        {
            'title': 'Email Marketing Automation',
            'slug': 'email-marketing',
            'icon': '📧',
            'badge': 'High Conversion',
            'category': 'Email Marketing',
            'service_description': '''Strategic email campaigns with personalized content, automation, and advanced segmentation for maximum engagement.

**What You Get:**
- Email sequence automation
- Personalized content generation
- Advanced audience segmentation
- A/B testing and optimization
- Deliverability monitoring

**Results:** 45% open rates, 12% click-through rates (2x industry average)''',
            'featured': True,
            'order': 7,
            'starting_price': '$279',
            'currency': 'USD',
            'billing_period': 'month'
        },
        {
            'title': 'Marketing Strategy Consulting',
            'slug': 'strategy-consulting',
            'icon': '💡',
            'badge': 'Expert Guidance',
            'category': 'Consulting',
            'service_description': '''Expert marketing strategy consultation to align your business goals with data-driven marketing approaches.

**What You Get:**
- Comprehensive marketing audit
- Custom strategy development
- Quarterly strategy reviews
- Team training and workshops
- Ongoing strategic support

**Results:** Clear roadmap to achieve your business goals with measurable KPIs''',
            'featured': True,
            'order': 8,
            'starting_price': '$999',
            'currency': 'USD',
            'billing_period': 'month'
        },
        {
            'title': 'Creative Design Services',
            'slug': 'creative-design',
            'icon': '🎨',
            'badge': 'Professional',
            'category': 'Design',
            'service_description': '''Professional design services for all your marketing materials, from social media graphics to landing pages.

**What You Get:**
- Social media graphics
- Landing page design
- Email template design
- Ad creative development
- Brand asset creation

**Results:** Professional designs that convert 3x better than DIY alternatives''',
            'featured': True,
            'order': 9,
            'starting_price': '$449',
            'currency': 'USD',
            'billing_period': 'month'
        }
    ]
    
    created_count = 0
    updated_count = 0
    
    for service_data in services_data:
        existing_service = ServicePage.objects.filter(slug=service_data['slug']).first()
        
        if existing_service:
            # Update existing service
            existing_service.title = service_data['title']
            existing_service.icon = service_data['icon']
            existing_service.badge = service_data['badge']
            existing_service.category = service_data['category']
            existing_service.service_description = service_data['service_description']
            existing_service.featured = service_data['featured']
            existing_service.order = service_data['order']
            existing_service.starting_price = service_data['starting_price']
            existing_service.currency = service_data['currency']
            existing_service.billing_period = service_data['billing_period']
            existing_service.save_revision().publish()
            updated_count += 1
            print(f"   ✓ Updated: {service_data['title']}")
        else:
            # Create new service
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
            print(f"   ✓ Created: {service_data['title']}")
    
    if created_count > 0:
        print(f"\n   Created {created_count} new service pages")
    if updated_count > 0:
        print(f"   Updated {updated_count} existing service pages")
    
    # 6. Summary
    print("\n" + "=" * 60)
    print("Content Creation Summary")
    print("=" * 60)
    print(f"Total pages in Wagtail: {Page.objects.count()}")
    print(f"Service pages: {ServicePage.objects.count()}")
    print(f"Homepage: {BizoholicHomePage.objects.count()}")
    print(f"Tenants: {Tenant.objects.count()}")
    print("\n✓ Content creation complete!")
    print("\nAccess Points:")
    print("  - Wagtail Admin: http://localhost:8002/admin/")
    print("  - Portal (Embedded): http://localhost:3001/portal/dashboard/content")
    print("  - Frontend: http://localhost:3001")
    print("\nAdmin Credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nAll content is now manageable through the Wagtail admin panel!")
    print("=" * 60)

if __name__ == '__main__':
    create_content()
