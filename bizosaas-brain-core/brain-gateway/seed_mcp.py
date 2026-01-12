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
        
        # 2. MCPs
        mcps_data = [
            # E-commerce
            {
                "name": "WooCommerce", "slug": "woocommerce", "category_slug": "ecommerce",
                "description": "Connect your WooCommerce store for products, orders, and customers.",
                "capabilities": ["products", "orders", "customers", "coupons"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-woocommerce:latest"},
                "is_official": True
            },
            {
                "name": "Shopify", "slug": "shopify", "category_slug": "ecommerce",
                "description": "Integrate with Shopify for complete store management.",
                "capabilities": ["products", "orders", "customers", "analytics"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-shopify:latest"},
                "is_official": True
            },
            # CRM
            {
                "name": "FluentCRM", "slug": "fluentcrm", "category_slug": "crm",
                "description": "WordPress-based CRM automation.",
                "capabilities": ["contacts", "campaigns", "tags", "emails"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-fluentcrm:latest"},
                "is_official": True
            },
            {
                "name": "HubSpot", "slug": "hubspot", "category_slug": "crm",
                "description": "Enterprise CRM platform.",
                "capabilities": ["contacts", "deals", "companies", "tickets"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-hubspot:latest"},
                "is_official": True
            },
            # Search
            {
                "name": "Brave Search", "slug": "brave-search", "category_slug": "search",
                "description": "Real-time web and local search capability.",
                "capabilities": ["web_search", "local_search"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-brave-search:latest"},
                "is_official": True
            },
            # Utilities
            {
                "name": "Filesystem", "slug": "filesystem", "category_slug": "utilities",
                "description": "Direct interactions with the provisioned storage volume.",
                "capabilities": ["read_file", "write_file", "list_dir"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-filesystem:latest"},
                "is_official": True
            },
            {
                "name": "GitHub", "slug": "github", "category_slug": "utilities",
                "description": "Manage repositories, issues, and pull requests.",
                "capabilities": ["code_search", "repo_management", "issue_tracking"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-github:latest"},
                "is_official": True
            },
            # Productivity
            {
                "name": "Google Drive", "slug": "google-drive", "category_slug": "communication",
                "description": "Read and write files to Google Drive.",
                "capabilities": ["file_upload", "file_list", "file_read"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-google-drive:latest"},
                "is_official": True
            },
            {
                "name": "Slack", "slug": "slack", "category_slug": "communication",
                "description": "Send notifications and interact with channels.",
                "capabilities": ["send_message", "channel_management"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-slack:latest"},
                "is_official": True
            },
            # CMS
            {
                "name": "WordPress", "slug": "wordpress", "category_slug": "cms",
                "description": "Manage posts, pages, and media.",
                "capabilities": ["posts", "pages", "media", "comments"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-wordpress:latest"},
                "is_official": True
            },
            # Email
            {
                "name": "Mailchimp", "slug": "mailchimp", "category_slug": "email-marketing",
                "description": "Email marketing and automation.",
                "capabilities": ["campaigns", "audiences", "reports"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-mailchimp:latest"},
                "is_official": True
            },
            # Payments
            {
                "name": "Stripe", "slug": "stripe", "category_slug": "payments",
                "description": "Payment processing and subscriptions.",
                "capabilities": ["payments", "subscriptions", "customers", "invoices"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-stripe:latest"},
                "is_official": True
            },
            # Analytics
            {
                "name": "Google Analytics 4", "slug": "google-analytics", "category_slug": "analytics",
                "description": "Web traffic and user behavior analytics.",
                "capabilities": ["traffic", "events", "conversions"],
                "mcp_config": {"type": "docker", "image": "bizosaas/mcp-google-analytics:latest"},
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
