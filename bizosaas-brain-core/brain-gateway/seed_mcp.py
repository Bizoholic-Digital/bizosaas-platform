import os
import sys
import uuid

# Add current directory to path so imports work
sys.path.append(os.getcwd())

from app.dependencies import SessionLocal
from app.models.mcp import McpCategory, McpRegistry

from dotenv import load_dotenv
load_dotenv()

def seed_mcp_registry():
    db = SessionLocal()
    try:
        print("Seeding MCP Registry...")
        
        # 1. Categories
        categories_data = [
            {"name": "E-commerce", "slug": "ecommerce", "description": "Online store platforms", "icon": "ShoppingCart", "sort_order": 1},
            {"name": "CRM", "slug": "crm", "description": "Customer Relationship Management", "icon": "Users", "sort_order": 2},
            {"name": "CMS", "slug": "cms", "description": "Content Management Systems", "icon": "FileText", "sort_order": 3},
            {"name": "Email Marketing", "slug": "email-marketing", "description": "Email campaigns & automation", "icon": "Mail", "sort_order": 4},
            {"name": "Payments", "slug": "payments", "description": "Payment gateways", "icon": "CreditCard", "sort_order": 5},
            {"name": "Analytics", "slug": "analytics", "description": "Web & product analytics", "icon": "BarChart", "sort_order": 6},
            {"name": "Advertising", "slug": "advertising", "description": "Ad platforms", "icon": "Megaphone", "sort_order": 7},
            {"name": "Communication", "slug": "communication", "description": "Messaging & chat", "icon": "MessageCircle", "sort_order": 8},
            {"name": "Search", "slug": "search", "description": "Web and local search capability", "icon": "Search", "sort_order": 9},
            {"name": "Utilities", "slug": "utilities", "description": "Development and system tools", "icon": "Terminal", "sort_order": 10},
            {"name": "Hosting", "slug": "hosting", "description": "Web hosting & infrastructure", "icon": "Server", "sort_order": 11},
            {"name": "HR & Payroll", "slug": "hr-payroll", "description": "Employee management & payroll", "icon": "Briefcase", "sort_order": 12},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat = db.query(McpCategory).filter_by(slug=cat_data["slug"]).first()
            if not cat:
                cat = McpCategory(**cat_data)
                db.add(cat)
                print(f"Created category: {cat.name}")
            else:
                print(f"Category exists: {cat.name}")
            categories[cat.slug] = cat
        
        db.flush() # Get IDs
        
        # 2. MCPs - Expanded for Global SMBs
        mcps_data = [
            # --- E-commerce ---
            {
                "name": "WooCommerce", "slug": "woocommerce", "category_slug": "ecommerce",
                "description": "Flexible, open-source e-commerce for WordPress.",
                "vendor_name": "Automattic",
                "sort_order": 1,
                "is_featured": True,
                "affiliate_link": "https://woocommerce.com/?aff=123",
                "capabilities": ["products", "orders", "customers", "coupons"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-woocommerce:latest"},
                "is_official": True
            },
            {
                "name": "Shopify", "slug": "shopify", "category_slug": "ecommerce",
                "description": "All-in-one commerce platform to start, run, and grow a business.",
                "vendor_name": "Shopify Inc",
                "sort_order": 2,
                "is_featured": True,
                "affiliate_link": "https://shopify.pxf.io/c/123",
                "capabilities": ["products", "orders", "customers", "analytics"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-shopify:latest"},
                "is_official": True
            },
            # --- CRM ---
            {
                "name": "FluentCRM", "slug": "fluentcrm", "category_slug": "crm",
                "description": "Self-hosted email marketing automation for WordPress.",
                "vendor_name": "WPManageNinja",
                "sort_order": 1,
                "is_featured": True,
                "affiliate_link": "https://fluentcrm.com/?ref=123",
                "capabilities": ["contacts", "campaigns", "tags", "emails"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-fluentcrm:latest"},
                "is_official": True
            },
            {
                "name": "HubSpot", "slug": "hubspot", "category_slug": "crm",
                "description": "Powerful CRM platform for scaling businesses.",
                "vendor_name": "HubSpot Inc",
                "sort_order": 2,
                "is_featured": False,
                "affiliate_link": "https://hubspot.sjv.io/c/123",
                "capabilities": ["contacts", "deals", "companies", "tickets"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-hubspot:latest"},
                "is_official": True
            },
            {
                "name": "Salesforce", "slug": "salesforce", "category_slug": "crm",
                "description": "The world's #1 CRM. Connect with customers in a whole new way.",
                "capabilities": ["leads", "opportunities", "accounts", "reports"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-salesforce:latest"},
                "is_official": True
            },
             {
                "name": "Pipedrive", "slug": "pipedrive", "category_slug": "crm",
                "description": "Sales CRM & pipeline management software.",
                "capabilities": ["leads", "deals", "activities", "pipelines"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-pipedrive:latest"},
                "is_official": True
            },
            # --- CMS ---
            {
                "name": "WordPress", "slug": "wordpress", "category_slug": "cms",
                "description": "The world's most popular website builder.",
                "capabilities": ["posts", "pages", "media", "comments", "themes"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-wordpress:latest"},
                "is_official": True
            },
            {
                "name": "Wix", "slug": "wix", "category_slug": "cms",
                "description": "Cloud-based web development platform.",
                "capabilities": ["site_management", "blog", "store"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-wix:latest"},
                "is_official": True
            },
            # --- Email Marketing ---
            {
                "name": "Mailchimp", "slug": "mailchimp", "category_slug": "email-marketing",
                "description": "All-in-one marketing platform for small business.",
                "capabilities": ["campaigns", "audiences", "reports", "automations"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-mailchimp:latest"},
                "is_official": True
            },
            {
                "name": "SendGrid", "slug": "sendgrid", "category_slug": "email-marketing",
                "description": "Cloud-based email delivery platform.",
                "capabilities": ["send_email", "stats", "contacts"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-sendgrid:latest"},
                "is_official": True
            },
            # --- Payments / Finance ---
            {
                "name": "Stripe", "slug": "stripe", "category_slug": "payments",
                "description": "Financial infrastructure for the internet.",
                "capabilities": ["payments", "subscriptions", "customers", "invoices"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-stripe:latest"},
                "is_official": True
            },
            {
                "name": "PayPal", "slug": "paypal", "category_slug": "payments",
                "description": "The safer, easier way to pay and get paid online.",
                "capabilities": ["payments", "invoicing", "payouts"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-paypal:latest"},
                "is_official": True
            },
            {
                "name": "Razorpay", "slug": "razorpay", "category_slug": "payments",
                "description": "Payments for India-based businesses.",
                "capabilities": ["payments", "orders", "subscriptions"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-razorpay:latest"},
                "is_official": True
            },
             {
                "name": "QuickBooks", "slug": "quickbooks", "category_slug": "payments",
                "description": "Smart accounting software for small businesses.",
                "capabilities": ["invoices", "expenses", "reports", "accounting"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-quickbooks:latest"},
                "is_official": True
            },
             {
                "name": "Xero", "slug": "xero", "category_slug": "payments",
                "description": "Beautiful accounting software for small business.",
                "capabilities": ["invoices", "bank_feeds", "reports"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-xero:latest"},
                "is_official": True
            },
            # --- Analytics ---
            {
                "name": "Google Analytics 4", "slug": "google-analytics", "category_slug": "analytics",
                "description": "Get essential customer insights.",
                "capabilities": ["traffic", "events", "conversions", "realtime"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-google-analytics:latest"},
                "is_official": True
            },
            {
                "name": "PostHog", "slug": "posthog", "category_slug": "analytics",
                "description": "Open source product analytics.",
                "capabilities": ["events", "recordings", "feature_flags"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-posthog:latest"},
                "is_official": True
            },
            # --- Advertising / Social ---
            {
                "name": "Meta Ads", "slug": "meta-ads", "category_slug": "advertising",
                "description": "Advertise on Facebook and Instagram.",
                "capabilities": ["campaigns", "adsets", "insights"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-meta-ads:latest"},
                "is_official": True
            },
            {
                "name": "Google Ads", "slug": "google-ads", "category_slug": "advertising",
                "description": "Reach customers with Google Ads.",
                "capabilities": ["campaigns", "keywords", "performance"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-google-ads:latest"},
                "is_official": True
            },
             {
                "name": "LinkedIn", "slug": "linkedin", "category_slug": "advertising", # Also serves as Social
                "description": "Professional network and B2B marketing.",
                "capabilities": ["posts", "ads", "company_page"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-linkedin:latest"},
                "is_official": True
            },
            # --- Communication ---
            {
                "name": "Slack", "slug": "slack", "category_slug": "communication",
                "description": "Team communication and collaboration.",
                "capabilities": ["send_message", "channels", "users"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-slack:latest"},
                "is_official": True
            },
            {
                "name": "WhatsApp Business", "slug": "whatsapp", "category_slug": "communication",
                "description": "Connect with customers on WhatsApp.",
                "capabilities": ["messages", "templates", "contacts"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-whatsapp:latest"},
                "is_official": True
            },
             {
                "name": "Zoom", "slug": "zoom", "category_slug": "communication",
                "description": "Video conferencing and meetings.",
                "capabilities": ["meetings", "users", "recordings"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-zoom:latest"},
                "is_official": True
            },
            {
                "name": "Twilio", "slug": "twilio", "category_slug": "communication",
                "description": "SMS, voice, and video communication platform.",
                "capabilities": ["sms", "voice", "video", "verify"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-twilio:latest"},
                "is_official": True
            },
            {
                "name": "MessageBird", "slug": "messagebird", "category_slug": "communication",
                "description": "Omnichannel communication platform for SMS, Voice, and Chat.",
                "capabilities": ["sms", "voice", "conversations", "verify"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-messagebird:latest"},
                "is_official": True
            },
            {
                "name": "Plivo", "slug": "plivo", "category_slug": "communication",
                "description": "Cloud communication platform for SMS and Voice.",
                "capabilities": ["sms", "voice", "mms"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-plivo:latest"},
                "is_official": True
            },
            # --- Search ---
            {
                "name": "Brave Search", "slug": "brave-search", "category_slug": "search",
                "description": "Privacy-focused search engine.",
                "capabilities": ["web_search", "news", "images"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-brave-search:latest"},
                "is_official": True
            },
            {
                "name": "Google Search Console", "slug": "gsc", "category_slug": "search",
                "description": "Monitor and maintain your site's presence in Google Search results.",
                "capabilities": ["performance", "sitemaps", "inspection"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-gsc:latest"},
                "is_official": True
            },
            # --- HR & Payroll ---
            {
                "name": "Deel", "slug": "deel", "category_slug": "hr-payroll",
                "description": "Global payroll and compliance for international teams.",
                "capabilities": ["contracts", "payroll", "documents"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-deel:latest"},
                "is_official": True
            },
             {
                "name": "Gusto", "slug": "gusto", "category_slug": "hr-payroll",
                "description": "Payroll, benefits, and HR platform.",
                "capabilities": ["payroll", "employees", "benefits"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-gusto:latest"},
                "is_official": True
            },
             {
                "name": "Remote", "slug": "remote", "category_slug": "hr-payroll",
                "description": "Global HR solution for distributed teams.",
                "capabilities": ["employment", "payroll", "benefits"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-remote:latest"},
                "is_official": True
            },
            # --- Hosting ---
            {
                "name": "WP Engine", "slug": "wp-engine", "category_slug": "hosting",
                "description": "Managed WordPress hosting platform.",
                "capabilities": ["sites", "backups", "domains"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-wpengine:latest"},
                "is_official": True
            },
             {
                "name": "Kinsta", "slug": "kinsta", "category_slug": "hosting",
                "description": "Premium managed WordPress hosting.",
                "capabilities": ["sites", "analytics", "staging"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-kinsta:latest"},
                "is_official": True
            },
            {
                "name": "Cloudways", "slug": "cloudways", "category_slug": "hosting",
                "description": "Managed cloud hosting platform.",
                "capabilities": ["servers", "apps", "backups"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-cloudways:latest"},
                "is_official": True
            },
             # --- Project Management (New) ---
            {
                "name": "Notion", "slug": "notion", "category_slug": "utilities",
                "description": "All-in-one workspace for notes, tasks, wikis, and databases.",
                "capabilities": ["pages", "databases", "blocks"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-notion:latest"},
                "is_official": True
            },
            {
                "name": "Trello", "slug": "trello", "category_slug": "utilities",
                "description": "Collaborative project management with boards.",
                "capabilities": ["boards", "lists", "cards"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-trello:latest"},
                "is_official": True
            },
            # --- Utilities / Storage ---
            {
                "name": "Google Drive", "slug": "google-drive", "category_slug": "utilities",
                "description": "Cloud file storage and synchronization.",
                "capabilities": ["files", "folders", "permissions"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-google-drive:latest"},
                "is_official": True
            },
             {
                "name": "GitHub", "slug": "github", "category_slug": "utilities",
                "description": "Software development platform.",
                "capabilities": ["repos", "issues", "prs", "actions"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-github:latest"},
                "is_official": True
            },
             {
                "name": "Zapier", "slug": "zapier", "category_slug": "utilities",
                "description": "Automate workflows by connecting your apps.",
                "capabilities": ["zaps", "triggers", "actions"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-zapier:latest"},
                "is_official": True
            },
        ]
        
        for mcp_data in mcps_data:
            mcp = db.query(McpRegistry).filter_by(slug=mcp_data["slug"]).first()
            if not mcp:
                cat_slug = mcp_data.pop("category_slug")
                cat = categories.get(cat_slug)
                if cat:
                    mcp = McpRegistry(**mcp_data, category_id=cat.id)
                    db.add(mcp)
                    print(f"Created MCP: {mcp.name}")
                else:
                    print(f"Category not found: {cat_slug}")
            else:
                # Update existing MCP data if needed (optional)
                for key, value in mcp_data.items():
                    if key != "category_slug":
                        setattr(mcp, key, value)
                print(f"Updated MCP: {mcp.name}")
        
        db.commit()
        print("Seeding completed successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_mcp_registry()
