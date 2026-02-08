import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.mcp import McpRegistry, McpCategory
from app.dependencies import SessionLocal
from app.services.mcp_curator import McpCuratorService

def seed_mcp_registry():
    db = SessionLocal()
    try:
        # 1. Ensure Categories Exist
        categories = {
            "cms": {"name": "CMS", "description": "Content Management Systems", "icon": "file-text", "sort_order": 1},
            "ecommerce": {"name": "Ecommerce", "description": "Online Stores and Shopping", "icon": "shopping-cart", "sort_order": 2},
            "crm": {"name": "CRM", "description": "Customer Relationship Management", "icon": "users", "sort_order": 3},
            "dev_tools": {"name": "Developer Tools", "description": "Code and Infrastructure", "icon": "terminal", "sort_order": 4},
            "search": {"name": "Search & Research", "description": "AI Search and Web Data", "icon": "search", "sort_order": 5},
            "communication": {"name": "Communication", "description": "Chat and Notifications", "icon": "message-square", "sort_order": 6},
        }
        
        category_map = {}
        for slug, data in categories.items():
            cat = db.query(McpCategory).filter(McpCategory.slug == slug).first()
            if not cat:
                cat = McpCategory(slug=slug, **data)
                db.add(cat)
                db.commit()
                db.refresh(cat)
            category_map[slug] = cat.id

        # 2. Priority MCPs
        priority_mcps = [
            {
                "name": "GitHub MCP",
                "slug": "github-mcp",
                "category_id": category_map["dev_tools"],
                "description": "Full GitHub API access for managing repositories, issues, PRs, and searching code.",
                "source_type": "official",
                "source_url": "https://github.com/modelcontextprotocol/server-github",
                "package_name": "@modelcontextprotocol/server-github",
                "is_official": True,
                "github_stars": 15000,
                "creator_org": "Anthropic",
                "capabilities": ["read_file", "list_directory", "create_issue", "search_code"],
                "mcp_config": {"type": "docker", "image": "mcp/github"}
            },
            {
                "name": "Saleor MCP",
                "slug": "saleor-mcp",
                "category_id": category_map["ecommerce"],
                "description": "Read-only access to Saleor Commerce GraphQL API for products, orders, and customers.",
                "source_type": "official",
                "source_url": "https://github.com/saleor/saleor-mcp",
                "hosted_url": "https://mcp.saleor.app/mcp",
                "is_official": True,
                "github_stars": 2400,
                "creator_org": "Saleor",
                "capabilities": ["get_products", "get_orders", "get_customers"],
                "mcp_config": {"type": "http", "url": "https://mcp.saleor.app/mcp"}
            },
            {
                "name": "WordPress MCP",
                "slug": "wordpress-mcp",
                "category_id": category_map["cms"],
                "description": "Official WordPress MCP server for managing sites, posts, and media.",
                "source_type": "official",
                "source_url": "https://github.com/mcp-wp/mcp-server",
                "is_official": True,
                "github_stars": 1200,
                "creator_org": "Automattic",
                "capabilities": ["get_posts", "create_post", "update_post"],
                "mcp_config": {"type": "wp-plugin", "slug": "mcp-server"}
            },
            {
                "name": "Brave Search MCP",
                "slug": "brave-search-mcp",
                "category_id": category_map["search"],
                "description": "Search the web using Brave Search API for real-time research.",
                "source_type": "official",
                "source_url": "https://github.com/modelcontextprotocol/server-brave-search",
                "is_official": True,
                "github_stars": 800,
                "creator_org": "Anthropic",
                "capabilities": ["search", "get_page_content"],
                "mcp_config": {"type": "docker", "image": "mcp/brave-search"}
            },
            {
                "name": "PostgreSQL MCP",
                "slug": "postgres-mcp",
                "category_id": category_map["dev_tools"],
                "description": "Direct access to PostgreSQL databases for querying and schema exploration.",
                "source_type": "official",
                "source_url": "https://github.com/modelcontextprotocol/server-postgres",
                "is_official": True,
                "github_stars": 500,
                "creator_org": "Anthropic",
                "capabilities": ["query", "list_tables", "describe_table"],
                "mcp_config": {"type": "docker", "image": "mcp/postgres"}
            }
        ]

        for mcp_data in priority_mcps:
            existing = db.query(McpRegistry).filter(McpRegistry.slug == mcp_data["slug"]).first()
            if not existing:
                mcp = McpRegistry(**mcp_data)
                # Apply quality scoring and tagging
                McpCuratorService.classify_and_tag(mcp)
                db.add(mcp)
                print(f"Added {mcp.name} with quality score {mcp.quality_score}")
        
        db.commit()
        print("Successfully seeded MCP registry.")
        
    finally:
        db.close()

if __name__ == "__main__":
    seed_mcp_registry()
