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
        
        # 1. Categories - Refined per User Request
        categories_data = [
            {"name": "E-commerce", "slug": "ecommerce", "description": "Online store platforms", "icon": "ShoppingCart", "sort_order": 1},
            {"name": "CRM", "slug": "crm", "description": "Customer Relationship Management", "icon": "Users", "sort_order": 2},
            {"name": "CMS", "slug": "cms", "description": "Content Management Systems", "icon": "FileText", "sort_order": 3},
            {"name": "Email Marketing", "slug": "email-marketing", "description": "Email campaigns & automation", "icon": "Mail", "sort_order": 4},
            {"name": "Billing & Revenue", "slug": "billing-revenue", "description": "Payments, Invoicing & Subscriptions", "icon": "CreditCard", "sort_order": 5},
            {"name": "Project Management", "slug": "project-management", "description": "Tasks, boards and team workflows", "icon": "CheckSquare", "sort_order": 6},
            {"name": "Analytics", "slug": "analytics", "description": "Web & product analytics", "icon": "BarChart", "sort_order": 7},
            {"name": "Advertising", "slug": "advertising", "description": "Ad platforms", "icon": "Megaphone", "sort_order": 8},
            {"name": "Communication", "slug": "communication", "description": "Messaging & chat", "icon": "MessageCircle", "sort_order": 9},
            {"name": "Utilities", "slug": "utilities", "description": "Storage and automation tools", "icon": "Terminal", "sort_order": 10},
        ]
        
        categories = {}
        # Clear existing categories to ensure clean slate (Optional, but safer for restructuring)
        # db.query(McpCategory).delete() 
        
        for cat_data in categories_data:
            cat = db.query(McpCategory).filter_by(slug=cat_data["slug"]).first()
            if not cat:
                cat = McpCategory(**cat_data)
                db.add(cat)
                print(f"Created category: {cat.name}")
            else:
                for key, value in cat_data.items():
                    setattr(cat, key, value)
                print(f"Updated category: {cat.name}")
            categories[cat.slug] = cat
        
        db.flush() # Get IDs
        
        # 2. MCPs - Reorganized as per strategic plan
        mcps_data = [
            # --- E-commerce & Marketplaces ---
            {"name": "Amazon US", "slug": "amazon-us", "category_slug": "ecommerce", "description": "Sell your products on Amazon.com (United States).", "vendor_name": "Amazon", "sort_order": 1, "is_featured": True, "capabilities": ["listings", "orders", "fba", "advertising"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-amazon:latest"}, "is_official": True},
            {"name": "Amazon India", "slug": "amazon-in", "category_slug": "ecommerce", "description": "Sell your products on Amazon.in (India).", "vendor_name": "Amazon", "sort_order": 2, "is_featured": True, "capabilities": ["listings", "orders", "easy_ship", "advertising"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-amazon-in:latest"}, "is_official": True},
            {"name": "Shopify Hub", "slug": "shopify", "category_slug": "ecommerce", "description": "Global Hub for catalog, inventory, and multichannel sync.", "vendor_name": "Shopify Inc", "sort_order": 3, "is_featured": True, "capabilities": ["products", "orders", "inventory", "webhooks"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-shopify:latest"}, "is_official": True},
            {"name": "Flipkart Integration", "slug": "flipkart", "category_slug": "ecommerce", "description": "Sell on India's leading marketplace. Full listing & order sync.", "vendor_name": "Flipkart", "sort_order": 4, "is_featured": True, "capabilities": ["listings", "orders", "inventory"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-flipkart:latest"}, "is_official": True},
            {"name": "Meesho Integration", "slug": "meesho", "category_slug": "ecommerce", "description": "List and sell on Meesho social commerce platform.", "vendor_name": "Meesho", "sort_order": 5, "is_featured": True, "capabilities": ["listings", "orders", "logistics"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-meesho:latest"}, "is_official": True},
            {"name": "Snapdeal Connector", "slug": "snapdeal", "category_slug": "ecommerce", "description": "Expand your reach on Snapdeal marketplace.", "vendor_name": "Snapdeal", "sort_order": 6, "capabilities": ["listings", "orders"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-snapdeal:latest"}, "is_official": True},
            {"name": "Shopify Marketplace Connect", "slug": "shopify-marketplace-connect", "category_slug": "ecommerce", "description": "Connect Shopify to Amazon US, Walmart, and eBay.", "vendor_name": "Shopify", "sort_order": 7, "capabilities": ["global_marketplace", "order_sync"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-marketplace-connect:latest"}, "is_official": True},
            {"name": "WooCommerce", "slug": "woocommerce", "category_slug": "ecommerce", "description": "Flexible, open-source e-commerce for WordPress.", "vendor_name": "Automattic", "sort_order": 8, "is_featured": True, "capabilities": ["products", "orders", "customers", "coupons"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-woocommerce:latest"}, "is_official": True},

            # --- CRM ---
            {"name": "Zoho CRM", "slug": "zoho-crm", "category_slug": "crm", "description": "Comprehensive CRM for growing businesses.", "vendor_name": "Zoho Corporation", "sort_order": 1, "is_featured": True, "capabilities": ["leads", "contacts", "deals", "tasks"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-zoho-crm:latest"}, "is_official": True},
            {"name": "HubSpot", "slug": "hubspot", "category_slug": "crm", "description": "Inbound marketing and sales CRM.", "vendor_name": "HubSpot Inc", "sort_order": 2, "is_featured": True, "capabilities": ["contacts", "deals", "companies", "tickets"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-hubspot:latest"}, "is_official": True},
            {"name": "Salesforce", "slug": "salesforce", "category_slug": "crm", "description": "Cloud-based CRM solutions.", "vendor_name": "Salesforce", "sort_order": 3, "capabilities": ["leads", "opportunities", "accounts", "reports"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-salesforce:latest"}, "is_official": True},
            {"name": "Bitrix24 CRM", "slug": "bitrix24", "category_slug": "crm", "description": "Free CRM with contact center and project management.", "vendor_name": "Bitrix24", "sort_order": 4, "capabilities": ["crm", "collaboration", "tasks", "contact_center"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-bitrix24:latest"}, "is_official": True},
            {"name": "FluentCRM", "slug": "fluentcrm", "category_slug": "crm", "description": "Self-hosted email automation & CRM for WordPress.", "vendor_name": "WPManageNinja", "sort_order": 5, "capabilities": ["contacts", "campaigns", "tags", "emails"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-fluentcrm:latest"}, "is_official": True},

            # --- CMS ---
            {"name": "WordPress Comprehensive MCP", "slug": "wordpress-mcp", "category_slug": "cms", "description": "Full-stack WordPress management: Content (Pages/Posts), Media, Plugins, SEO (Yoast), and Platform Settings.", "vendor_name": "BizOSaaS Official", "sort_order": 1, "is_featured": True, "capabilities": ["posts", "pages", "media", "plugins", "categories", "seo", "settings"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-wordpress-comprehensive:latest"}, "is_official": True},
            {"name": "Webflow", "slug": "webflow", "category_slug": "cms", "description": "Visual web development platform.", "vendor_name": "Webflow Inc", "sort_order": 2, "is_featured": True, "capabilities": ["sites", "collections", "forms", "ecommerce"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-webflow:latest"}, "is_official": True},

            # --- Email Marketing (Updated) ---
            {"name": "Amazon SES", "slug": "amazon-ses", "category_slug": "email-marketing", "description": "Cost-effective, managed email sending service. Perfect for high-volume campaigns.", "vendor_name": "Amazon", "sort_order": 1, "is_featured": True, "capabilities": ["sending", "templates", "stats", "reputation"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-amazon-ses:latest"}, "is_official": True},
            {"name": "Brevo", "slug": "brevo", "category_slug": "email-marketing", "description": "All-in-one marketing platform for email & SMS automation.", "vendor_name": "Brevo", "sort_order": 2, "is_featured": True, "capabilities": ["email", "sms", "automation", "crm"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-brevo:latest"}, "is_official": True},
            {"name": "Mailchimp", "slug": "mailchimp", "category_slug": "email-marketing", "description": "Popular all-in-one marketing platform.", "vendor_name": "Intuit", "sort_order": 4, "capabilities": ["campaigns", "audiences", "reports", "automations"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-mailchimp:latest"}, "is_official": True},

            # --- Billing & Revenue ---
            {"name": "PayU", "slug": "payu", "category_slug": "billing-revenue", "description": "Leading payment gateway for India-based businesses.", "vendor_name": "PayU", "sort_order": 1, "is_featured": True, "capabilities": ["payments", "checkout", "payouts"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-payu:latest"}, "is_official": True},
            {"name": "Razorpay", "slug": "razorpay", "category_slug": "billing-revenue", "description": "Payments for modern Indian businesses.", "vendor_name": "Razorpay", "sort_order": 2, "is_featured": True, "capabilities": ["payments", "orders", "subscriptions"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-razorpay:latest"}, "is_official": True},
            {"name": "Stripe", "slug": "stripe", "category_slug": "billing-revenue", "description": "Global financial infrastructure for the internet.", "vendor_name": "Stripe", "sort_order": 3, "is_featured": True, "capabilities": ["payments", "subscriptions", "invoices"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-stripe:latest"}, "is_official": True},
            {"name": "Lago", "slug": "lago", "category_slug": "billing-revenue", "description": "Usage-based billing and revenue management (Internal/Managed).", "vendor_name": "Lago", "sort_order": 4, "capabilities": ["metering", "billing", "usage", "invoices"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-lago:latest"}, "is_official": True},
            {"name": "Zoho Billing", "slug": "zoho-billing", "category_slug": "billing-revenue", "description": "End-to-end billing and subscription management.", "vendor_name": "Zoho", "sort_order": 5, "capabilities": ["subscriptions", "recurring_billing", "invoices"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-zoho-billing:latest"}, "is_official": True},
            {"name": "Zoho Books", "slug": "zoho-books", "category_slug": "billing-revenue", "description": "VAT/GST compliant accounting software.", "vendor_name": "Zoho", "sort_order": 6, "capabilities": ["accounting", "gst", "expenses"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-zoho-books:latest"}, "is_official": True},
            {"name": "QuickBooks", "slug": "quickbooks", "category_slug": "billing-revenue", "description": "Cloud accounting for small businesses.", "vendor_name": "Intuit", "sort_order": 7, "capabilities": ["invoices", "expenses", "accounting"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-quickbooks:latest"}, "is_official": True},

            # --- Project Management ---
            {"name": "Notion", "slug": "notion", "category_slug": "project-management", "description": "All-in-one workspace for notes & tasks.", "vendor_name": "Notion Labs", "sort_order": 1, "is_featured": True, "capabilities": ["pages", "databases", "collaboration"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-notion:latest"}, "is_official": True},
            {"name": "Zoho Projects", "slug": "zoho-projects", "category_slug": "project-management", "description": "Task management & team collaboration.", "vendor_name": "Zoho Corporation", "sort_order": 2, "is_featured": True, "capabilities": ["tasks", "gantt", "timesheets"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-zoho-projects:latest"}, "is_official": True},
            {"name": "Asana", "slug": "asana", "category_slug": "project-management", "description": "Work management for modern teams.", "vendor_name": "Asana Inc", "sort_order": 3, "capabilities": ["projects", "status", "timelines"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-asana:latest"}, "is_official": True},
            {"name": "Monday.com", "slug": "monday", "category_slug": "project-management", "description": "Visual Work OS for managing anything.", "vendor_name": "Monday.com Ltd", "sort_order": 4, "capabilities": ["boards", "automations", "dashboards"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-monday:latest"}, "is_official": True},
            {"name": "ClickUp", "slug": "clickup", "category_slug": "project-management", "description": "One app to replace them all.", "vendor_name": "ClickUp", "sort_order": 5, "capabilities": ["tasks", "docs", "goals"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-clickup:latest"}, "is_official": True},
            {"name": "Trello", "slug": "trello", "category_slug": "project-management", "description": "Simple Kanban boards for teams.", "vendor_name": "Atlassian", "sort_order": 6, "capabilities": ["boards", "cards", "powerups"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-trello:latest"}, "is_official": True},

            # --- Analytics ---
            {"name": "Google Analytics 4", "slug": "google-analytics", "category_slug": "analytics", "description": "Standard web analytics and insights.", "vendor_name": "Google", "sort_order": 1, "is_featured": True, "capabilities": ["traffic", "conversions", "realtime"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-google-analytics:latest"}, "is_official": True},
            {"name": "Facebook Analytics", "slug": "facebook-analytics", "category_slug": "analytics", "description": "Deep insights into Facebook and Instagram user behavior.", "vendor_name": "Meta", "sort_order": 2, "is_featured": True, "capabilities": ["demographics", "retention", "funnels"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-facebook-analytics:latest"}, "is_official": True},
            {"name": "Bing Analytics", "slug": "bing-analytics", "category_slug": "analytics", "description": "Microsoft Advertising UET and performance analytics.", "vendor_name": "Microsoft", "sort_order": 3, "is_featured": True, "capabilities": ["conversions", "audience", "keywords"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-bing-analytics:latest"}, "is_official": True},
            {"name": "Microsoft Clarity", "slug": "clarity", "category_slug": "analytics", "description": "Free heatmaps and session recordings.", "vendor_name": "Microsoft", "sort_order": 4, "is_featured": True, "capabilities": ["heatmaps", "recordings", "insights"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-clarity:latest"}, "is_official": True},
            {"name": "PostHog", "slug": "posthog", "category_slug": "analytics", "description": "Product OS: Analytics, Flags, Session Replays.", "vendor_name": "PostHog", "sort_order": 5, "capabilities": ["events", "recordings", "feature_flags"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-posthog:latest"}, "is_official": True},
            {"name": "Zoho Analytics", "slug": "zoho-analytics", "category_slug": "analytics", "description": "Self-service BI and analytics platform.", "vendor_name": "Zoho", "sort_order": 6, "capabilities": ["reports", "dashboards", "bi"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-zoho-analytics:latest"}, "is_official": True},

            # --- Advertising ---
            {"name": "Google Ads", "slug": "google-ads", "category_slug": "advertising", "description": "Reach users on Google Search, YouTube, and Gmail.", "vendor_name": "Google", "sort_order": 1, "is_featured": True, "capabilities": ["campaigns", "search", "display"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-google-ads:latest"}, "is_official": True},
            {"name": "Meta Ads", "slug": "meta-ads", "category_slug": "advertising", "description": "Targeted ads on Facebook and Instagram.", "vendor_name": "Meta", "sort_order": 2, "is_featured": True, "capabilities": ["campaigns", "audience", "creative"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-meta-ads:latest"}, "is_official": True},
            {"name": "TikTok Ads", "slug": "tiktok-ads", "category_slug": "advertising", "description": "Engagement on short-form video platform.", "vendor_name": "ByteDance", "sort_order": 3, "capabilities": ["video_ads", "brand_vulnerability"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-tiktok-ads:latest"}, "is_official": True},
            {"name": "LinkedIn Ads", "slug": "linkedin-ads", "category_slug": "advertising", "description": "Professional B2B advertising platform.", "vendor_name": "Microsoft", "sort_order": 4, "capabilities": ["professional_targeting", "lead_forms"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-linkedin-ads:latest"}, "is_official": True},

            # --- Communication ---
            {"name": "WhatsApp for Business", "slug": "whatsapp-business", "category_slug": "communication", "description": "Automate customer support on WhatsApp.", "vendor_name": "Meta", "sort_order": 1, "is_featured": True, "capabilities": ["messaging", "automation", "catalogs"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-whatsapp:latest"}, "is_official": True},
            {"name": "Microsoft Teams", "slug": "ms-teams", "category_slug": "communication", "description": "Collaboration and video meetings.", "vendor_name": "Microsoft", "sort_order": 2, "capabilities": ["meetings", "chat", "channels"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-ms-teams:latest"}, "is_official": True},
            {"name": "Slack", "slug": "slack", "category_slug": "communication", "description": "Team messaging and productivity.", "vendor_name": "Salesforce", "sort_order": 3, "capabilities": ["channels", "messaging", "huddles"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-slack:latest"}, "is_official": True},
            {"name": "Twilio", "slug": "twilio", "category_slug": "communication", "description": "Programmable SMS, Voice and Email.", "vendor_name": "Twilio Inc", "sort_order": 4, "capabilities": ["sms", "voice", "verify"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-twilio:latest"}, "is_official": True},

            # --- Utilities ---
            {"name": "Google Workspace", "slug": "google-workspace", "category_slug": "utilities", "description": "Professional Gmail, Drive & Docs.", "vendor_name": "Google", "sort_order": 1, "is_featured": True, "capabilities": ["identity", "docs", "storage"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-google-workspace:latest"}, "is_official": True},
            {"name": "Microsoft 365", "slug": "microsoft-365", "category_slug": "utilities", "description": "Office apps, storage and cloud services.", "vendor_name": "Microsoft", "sort_order": 2, "capabilities": ["office", "onedrive", "mail"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-office365:latest"}, "is_official": True},
            {"name": "Zapier", "slug": "zapier", "category_slug": "utilities", "description": "Connect thousands of apps for automation.", "vendor_name": "Zapier", "sort_order": 3, "is_featured": True, "capabilities": ["automations", "triggers", "actions"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-zapier:latest"}, "is_official": True},
            {"name": "Make.com", "slug": "make", "category_slug": "utilities", "description": "Advanced visual automation platform.", "vendor_name": "Make", "sort_order": 4, "capabilities": ["scenarios", "webhooks", "data_transfer"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-make:latest"}, "is_official": True},
            {"name": "n8n", "slug": "n8n", "category_slug": "utilities", "description": "Fair-code workflow automation tool.", "vendor_name": "n8n.io", "sort_order": 5, "is_featured": True, "capabilities": ["workflows", "nodes", "webhooks"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-n8n:latest"}, "is_official": True},
            {"name": "Pabbly Connect", "slug": "pabbly", "category_slug": "utilities", "description": "Connect apps and automate workflows.", "vendor_name": "Pabbly", "sort_order": 6, "capabilities": ["automation", "integration", "workflows"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-pabbly:latest"}, "is_official": True},
            {"name": "GitHub", "slug": "github", "category_slug": "utilities", "description": "Code hosting and version control.", "vendor_name": "Microsoft", "sort_order": 7, "capabilities": ["repos", "issues", "actions"], "mcp_config": {"type": "docker", "image": "bizosaas/mcp-github:latest"}, "is_official": True},
        ]
        
        # Remove old categories that are no longer needed
        obsolete_categories = ["hosting", "hr-payroll", "search", "payments", "infrastructure"]
        for old_slug in obsolete_categories:
            db.query(McpRegistry).filter(McpRegistry.category_id == db.query(McpCategory.id).filter(McpCategory.slug == old_slug).scalar_subquery()).delete(synchronize_session=False)
            db.query(McpCategory).filter(McpCategory.slug == old_slug).delete()
        
        # Delete existing MCPs to ensure clean mapping
        db.query(McpRegistry).delete()
        db.flush()

        for mcp_data in mcps_data:
            cat_slug = mcp_data.pop("category_slug")
            cat = categories.get(cat_slug)
            if cat:
                mcp = McpRegistry(**mcp_data, category_id=cat.id)
                db.add(mcp)
                print(f"Provisioned MCP: {mcp.name}")
            else:
                print(f"Category CRITICAL ERROR: {cat_slug} not found for {mcp_data['name']}")
        
        db.commit()
        print("BizOSaaS Marketplace Seeding completed successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_mcp_registry()
