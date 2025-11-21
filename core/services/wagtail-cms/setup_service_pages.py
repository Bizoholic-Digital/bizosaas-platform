#!/usr/bin/env python
"""
Setup script to create 9 individual service pages for Bizoholic marketing services
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagtail_cms.settings.development')
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas/services/wagtail-cms')

django.setup()

from wagtail.models import Page, Site
from cms.models import BizoholicHomePage, ServicePage

# Define the 9 marketing services with detailed content
SERVICES_DATA = [
    {
        'title': 'SEO Optimization & Local SEO',
        'slug': 'seo-optimization-local-seo',
        'icon': '🔍',
        'badge': 'Most Popular',
        'category': 'Search Marketing',
        'service_description': 'Boost your search rankings with AI-powered SEO optimization. Our advanced algorithms analyze your website, competitors, and search trends to deliver 200% better organic traffic within 90 days.',
        'featured': True,
        'order': 1,
        'price_data': {
            'starting_price': '$299',
            'currency': 'USD',
            'billing_period': 'month'
        }
    },
    {
        'title': 'Paid Advertising (PPC) Management',
        'slug': 'paid-advertising-ppc-management',
        'icon': '💰',
        'badge': 'High ROI',
        'category': 'Paid Media',
        'service_description': 'Maximize your ad spend with AI-driven PPC campaigns. Our intelligent bidding algorithms reduce cost-per-click by 45% while increasing conversions by 180%.',
        'featured': True,
        'order': 2,
        'price_data': {
            'starting_price': '$599',
            'currency': 'USD',
            'billing_period': 'month'
        }
    },
    {
        'title': 'Social Media Marketing & Management',
        'slug': 'social-media-marketing-management',
        'icon': '📱',
        'badge': 'Trending',
        'category': 'Social Media',
        'service_description': 'Grow your social presence with AI-powered content creation and scheduling. Generate viral-worthy posts, optimize posting times, and engage with your audience automatically.',
        'featured': True,
        'order': 3,
        'price_data': {
            'starting_price': '$399',
            'currency': 'USD',
            'billing_period': 'month'
        }
    },
    {
        'title': 'Content Marketing & Blog Writing',
        'slug': 'content-marketing-blog-writing',
        'icon': '✍️',
        'badge': 'SEO Optimized',
        'category': 'Content Marketing',
        'service_description': 'Create engaging, SEO-optimized content that converts. Our AI writers produce high-quality blog posts, articles, and web copy that ranks on page 1 of Google.',
        'featured': False,
        'order': 4,
        'price_data': {
            'starting_price': '$249',
            'currency': 'USD',
            'billing_period': 'month'
        }
    },
    {
        'title': 'Email Marketing Automation',
        'slug': 'email-marketing-automation',
        'icon': '📧',
        'badge': 'High Conversion',
        'category': 'Email Marketing',
        'service_description': 'Build automated email sequences that nurture leads and drive sales. Our AI personalizes every email for maximum engagement and 60% higher conversion rates.',
        'featured': False,
        'order': 5,
        'price_data': {
            'starting_price': '$199',
            'currency': 'USD',
            'billing_period': 'month'
        }
    },
    {
        'title': 'Lead Generation & Conversion',
        'slug': 'lead-generation-conversion',
        'icon': '🎯',
        'badge': 'Results Guaranteed',
        'category': 'Lead Generation',
        'service_description': 'Generate high-quality leads with AI-powered targeting and conversion optimization. Increase your lead volume by 300% while reducing cost-per-lead by 50%.',
        'featured': True,
        'order': 6,
        'price_data': {
            'starting_price': '$449',
            'currency': 'USD',
            'billing_period': 'month'
        }
    },
    {
        'title': 'Website Design & Development',
        'slug': 'website-design-development',
        'icon': '🌐',
        'badge': 'Mobile First',
        'category': 'Web Development',
        'service_description': 'Build high-converting websites with AI-optimized design and development. Our responsive, fast-loading sites increase conversion rates by 150% and improve user experience.',
        'featured': False,
        'order': 7,
        'price_data': {
            'starting_price': '$1299',
            'currency': 'USD',
            'billing_period': 'one-time'
        }
    },
    {
        'title': 'Analytics & Performance Tracking',
        'slug': 'analytics-performance-tracking',
        'icon': '📊',
        'badge': 'Data Driven',
        'category': 'Analytics',
        'service_description': 'Make data-driven decisions with advanced analytics and AI insights. Track every metric that matters and get actionable recommendations to improve your marketing ROI.',
        'featured': False,
        'order': 8,
        'price_data': {
            'starting_price': '$149',
            'currency': 'USD',
            'billing_period': 'month'
        }
    },
    {
        'title': 'Brand Strategy & Reputation Management',
        'slug': 'brand-strategy-reputation-management',
        'icon': '🏆',
        'badge': 'Brand Building',
        'category': 'Brand Management',
        'service_description': 'Build and protect your brand with AI-powered reputation management. Monitor mentions, respond to reviews automatically, and strengthen your brand presence across all channels.',
        'featured': False,
        'order': 9,
        'price_data': {
            'starting_price': '$349',
            'currency': 'USD',
            'billing_period': 'month'
        }
    }
]

def setup_service_pages():
    """Create all 9 service pages"""
    
    try:
        # Get the homepage as parent
        homepage = BizoholicHomePage.objects.first()
        if not homepage:
            print("❌ BizoholicHomePage not found. Please create it first.")
            return False
        
        print(f"🏠 Using homepage: {homepage.title}")
        
        created_count = 0
        updated_count = 0
        
        for service_data in SERVICES_DATA:
            # Check if service page already exists
            existing_page = ServicePage.objects.filter(
                slug=service_data['slug']
            ).first()
            
            if existing_page:
                print(f"📝 Updating existing service: {service_data['title']}")
                # Update existing page
                for key, value in service_data.items():
                    if key != 'slug':
                        setattr(existing_page, key, value)
                existing_page.save_revision().publish()
                updated_count += 1
            else:
                print(f"✨ Creating new service: {service_data['title']}")
                # Create new service page
                service_page = ServicePage(**service_data)
                
                # Add as child of homepage
                homepage.add_child(instance=service_page)
                
                # Publish the page
                service_page.save_revision().publish()
                created_count += 1
        
        print(f"\n✅ Service pages setup completed!")
        print(f"📊 Created: {created_count} pages")
        print(f"🔄 Updated: {updated_count} pages")
        print(f"🌐 All services available at: http://localhost:3000/")
        
        # Print service URLs
        print(f"\n🔗 Service Page URLs:")
        for service_data in SERVICES_DATA:
            print(f"   • {service_data['title']}: http://localhost:3000/{service_data['slug']}/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating service pages: {e}")
        import traceback
        traceback.print_exc()
        return False

def update_homepage_services_links():
    """Update homepage to include links to service pages"""
    try:
        homepage = BizoholicHomePage.objects.first()
        if not homepage:
            return False
        
        print("🔗 Updating homepage service links...")
        
        # Update homepage to include service navigation
        # This would modify the homepage template or content to include service links
        
        return True
    except Exception as e:
        print(f"❌ Error updating homepage: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Setting up Bizoholic service pages...")
    
    success = setup_service_pages()
    
    if success:
        print("✨ Service pages setup completed successfully!")
        print("🎯 Next steps:")
        print("   1. Visit http://localhost:3000/ to see the updated homepage")
        print("   2. Check each service page for content and styling")
        print("   3. Add service links to the homepage navigation")
        print("   4. Test SEO optimization on each page")
    else:
        print("💥 Service pages setup failed!")