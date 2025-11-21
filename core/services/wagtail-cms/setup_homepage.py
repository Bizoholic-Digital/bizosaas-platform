#!/usr/bin/env python
"""
Setup script to create BizoholicHomePage as the site's root page
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagtail_cms.settings.development')
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas/services/wagtail-cms')

django.setup()

from wagtail.models import Page, Site
from cms.models import BizoholicHomePage

def setup_homepage():
    """Create and configure the BizoholicHomePage as site root"""
    
    try:
        # Get the default site
        try:
            site = Site.objects.get(is_default_site=True)
            print(f"Found default site: {site.hostname}:{site.port}")
        except Site.DoesNotExist:
            # Create default site
            root_page = Page.get_first_root_node()
            site = Site.objects.create(
                hostname='localhost',
                port=8006,
                site_name='Bizoholic Marketing',
                root_page=root_page,
                is_default_site=True
            )
            print(f"Created default site: {site.hostname}:{site.port}")
        
        # Check if BizoholicHomePage already exists
        existing_homepage = BizoholicHomePage.objects.filter(
            title="Bizoholic - AI-Powered Marketing"
        ).first()
        
        if existing_homepage:
            print(f"Homepage already exists: {existing_homepage.title}")
            # Update site root to this page
            site.root_page = existing_homepage
            site.save()
            return existing_homepage
        
        # Get or create root page
        root_page = site.root_page
        if not root_page:
            root_page = Page.get_first_root_node()
        
        # Create the BizoholicHomePage
        homepage = BizoholicHomePage(
            title="Bizoholic - AI-Powered Marketing",
            slug="home",
            hero_title="AI-Powered Marketing Automation",
            hero_subtitle="Transform your marketing with AI automation. Get 75% cost savings, ROI within 7 days, and setup in 15 minutes. The smartest marketing platform for small businesses.",
            hero_cta_text="Get Started Free",
            hero_cta_url="/contact",
            features_title="Why Choose Bizoholic?",
            show_service_status=True,
        )
        
        # Add as child of root page
        root_page.add_child(instance=homepage)
        
        # Publish the page
        homepage.save_revision().publish()
        
        # Set as site root
        site.root_page = homepage
        site.save()
        
        print(f"✅ Successfully created homepage: {homepage.title}")
        print(f"✅ Set as site root for {site.hostname}:{site.port}")
        print(f"🌐 Homepage URL: http://{site.hostname}:{site.port}/")
        
        return homepage
        
    except Exception as e:
        print(f"❌ Error creating homepage: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🚀 Setting up Bizoholic homepage...")
    homepage = setup_homepage()
    
    if homepage:
        print("✨ Homepage setup completed successfully!")
        print(f"📝 Page ID: {homepage.id}")
        print(f"🔗 Admin URL: http://localhost:8006/admin/pages/{homepage.id}/")
    else:
        print("💥 Homepage setup failed!")