import logging
from uuid import uuid4
from app.models.mcp import McpCategory, McpRegistry
from app.dependencies import SessionLocal

logger = logging.getLogger(__name__)

def seed_mcp_registry():
    """
    Seeds the MCP Registry with Automation tools and Industry standards.
    """
    db = SessionLocal()
    try:
        logger.info("🌱 Seeding MCP Registry...")
        
        # 1. Categories
        categories = [
            {"name": "Automation", "slug": "automation", "icon": "settings", "sort_order": 1},
            {"name": "E-commerce", "slug": "ecommerce", "icon": "shopping-cart", "sort_order": 2},
            {"name": "Marketing", "slug": "marketing", "icon": "megaphone", "sort_order": 3},
            {"name": "CRM", "slug": "crm", "icon": "users", "sort_order": 4},
        ]
        
        cat_map = {}
        for cat_data in categories:
            cat = db.query(McpCategory).filter(McpCategory.slug == cat_data["slug"]).first()
            if not cat:
                cat = McpCategory(**cat_data)
                db.add(cat)
                db.commit()
                db.refresh(cat)
            cat_map[cat_data["slug"]] = cat.id

        # 2. Registry Items
        registry_items = [
            {
                "name": "n8n Automation",
                "slug": "n8n",
                "description": "Self-hosted workflow automation tool with 400+ integrations.",
                "category_id": cat_map["automation"],
                "capabilities": ["workflows", "webhooks", "data-sync"],
                "mcp_config": {"type": "external", "url": "https://n8n.io"},
                "is_official": True,
                "rating": 5
            },
            {
                "name": "Zapier",
                "slug": "zapier",
                "description": "Connect your apps and automate workflows.",
                "category_id": cat_map["automation"],
                "capabilities": ["workflows", "zaps"],
                "mcp_config": {"type": "saas", "url": "https://zapier.com"},
                "is_official": False,
                "rating": 4
            },
            {
                "name": "Make.com",
                "slug": "make",
                "description": "Visual platform to design, build, and automate anything.",
                "category_id": cat_map["automation"],
                "capabilities": ["scenarios", "webhooks"],
                "mcp_config": {"type": "saas", "url": "https://make.com"},
                "is_official": False,
                "rating": 4
            },
            {
                "name": "WordPress Connector",
                "slug": "wordpress",
                "description": "Deep integration with WordPress for content and users.",
                "category_id": cat_map["ecommerce"],
                "capabilities": ["posts", "pages", "users"],
                "mcp_config": {"type": "internal"},
                "is_official": True,
                "rating": 5
            }
        ]
        
        for item_data in registry_items:
            item = db.query(McpRegistry).filter(McpRegistry.slug == item_data["slug"]).first()
            if not item:
                item = McpRegistry(**item_data)
                db.add(item)
        
        db.commit()
        logger.info("✅ MCP Registry seeded successfully!")
        
    except Exception as e:
        logger.error(f"❌ MCP Seeding failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_mcp_registry()
