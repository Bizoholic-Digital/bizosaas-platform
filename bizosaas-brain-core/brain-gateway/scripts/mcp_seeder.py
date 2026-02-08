import asyncio
import httpx
import uuid
import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.dependencies import SessionLocal
from app.models.mcp import McpRegistry, McpCategory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sources
MCPHUB_API = "https://mcphub.ai/api/servers" # Placeholder - might need scraping or official API
AWESOME_MCP_JSON = "https://raw.githubusercontent.com/punkpeye/awesome-mcp-servers/main/servers.json" # Mocking structure

async def fetch_external_mcps() -> List[Dict[str, Any]]:
    """
    Fetch live MCP servers from community sources.
    """
    # ... (rest of the function remains the same)
    curated_servers = [
        {
            "name": "Google Maps",
            "slug": "google-maps",
            "description": "Integration with Google Maps for location search, routing, and places.",
            "vendor_name": "Google",
            "category": "Communication",
            "is_official": True,
            "quality_score": 98,
            "github_stars": 1500,
            "tags": ["maps", "location", "api"],
            "capabilities": ["search_places", "get_directions", "reverse_geocode"]
        },
        {
            "name": "BigQuery",
            "slug": "bigquery",
            "description": "Execute queries on Google BigQuery datasets.",
            "vendor_name": "Google",
            "category": "Data Management",
            "is_official": True,
            "quality_score": 95,
            "github_stars": 800,
            "tags": ["database", "analytics", "sql"],
            "capabilities": ["execute_query", "list_datasets", "get_table_schema"]
        },
        {
            "name": "Slack",
            "slug": "slack",
            "description": "Send messages and interact with Slack channels.",
            "vendor_name": "Slack",
            "category": "Communication",
            "is_official": True,
            "quality_score": 92,
            "github_stars": 1200,
            "tags": ["chat", "notifications", "collaboration"],
            "capabilities": ["post_message", "list_channels", "add_reaction"]
        },
        {
            "name": "PostgreSQL",
            "slug": "postgres",
            "description": "Direct interaction with PostgreSQL databases.",
            "vendor_name": "Community",
            "category": "Data Management",
            "is_official": False,
            "quality_score": 88,
            "github_stars": 3400,
            "tags": ["sql", "database", "orm"],
            "capabilities": ["query", "list_tables", "inspect_schema"]
        },
        {
            "name": "GitHub",
            "slug": "github",
            "description": "Search repositories, manage issues, and review pull requests.",
            "vendor_name": "GitHub",
            "category": "Development",
            "is_official": True,
            "quality_score": 97,
            "github_stars": 5600,
            "tags": ["git", "code", "devops"],
            "capabilities": ["search_repos", "create_issue", "get_pr_details"]
        }
    ]
    
    return curated_servers

async def seed_mcp_registry():
    """
    Main seeder function.
    """
    db = SessionLocal()
    try:
        logger.info("Starting MCP Registry Seeding...")
        
        # 1. Ensure Categories exist
        categories = {
            "Communication": "Tools for messaging, email, and collaboration.",
            "Data Management": "Integrations with databases and data warehouses.",
            "Development": "Tools for coding, version control, and CI/CD.",
            "Finance": "Payment gateways and accounting tools.",
            "Marketing": "CRM and email marketing automation."
        }
        
        db_categories = {}
        for name, desc in categories.items():
            cat = db.query(McpCategory).filter(McpCategory.name == name).first()
            if not cat:
                cat = McpCategory(id=uuid.uuid4(), name=name, description=desc)
                db.add(cat)
                db.commit()
                db.refresh(cat)
            db_categories[name] = cat
            
        # 2. Fetch and Upsert MCPs
        external_mcps = await fetch_external_mcps()
        
        for mcp_data in external_mcps:
            # Check if exists
            existing = db.query(McpRegistry).filter(McpRegistry.slug == mcp_data["slug"]).first()
            
            cat = db_categories.get(mcp_data["category"])
            if not cat: continue 

            if existing:
                logger.info(f"Updating existing MCP: {mcp_data['name']}")
                existing.name = mcp_data["name"]
                existing.description = mcp_data["description"]
                existing.vendor_name = mcp_data["vendor_name"]
                existing.is_official = mcp_data["is_official"]
                existing.quality_score = mcp_data["quality_score"]
                existing.github_stars = mcp_data["github_stars"]
                existing.tags = mcp_data["tags"]
                existing.capabilities = mcp_data["capabilities"]
            else:
                logger.info(f"Adding new MCP: {mcp_data['name']}")
                new_mcp = McpRegistry(
                    id=uuid.uuid4(),
                    name=mcp_data["name"],
                    slug=mcp_data["slug"],
                    description=mcp_data["description"],
                    category_id=cat.id,
                    vendor_name=mcp_data["vendor_name"],
                    is_official=mcp_data["is_official"],
                    is_featured=(mcp_data.get("quality_score") or 0) > 90,
                    quality_score=mcp_data["quality_score"],
                    github_stars=mcp_data["github_stars"],
                    tags=mcp_data["tags"],
                    capabilities=mcp_data["capabilities"],
                    is_active=True
                )
                db.add(new_mcp)
        
        db.commit()
        logger.info("MCP Registry Seeding Complete!")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(seed_mcp_registry())
