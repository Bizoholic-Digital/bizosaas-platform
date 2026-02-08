import re
import httpx
import asyncio
import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Add parent directory to path to allow imports from app
sys.path.append(os.getcwd())

# 1. Immediate Vault Initialization (Must happen before app dependencies import)
def load_vault_secrets_sync():
    """Synchronously load secrets from Vault into environment variables."""
    try:
        from adapters.vault_adapter import VaultAdapter
        mount_point = os.getenv("VAULT_MOUNT_POINT", "bizosaas")
        vault = VaultAdapter(mount_point=mount_point)
        if vault.client and vault.client.is_authenticated():
            print("INFO: Connected to Vault. Loading secrets for seeding...")
            
            # Load Infrastructure Secrets (contains DATABASE_URL)
            infra_secrets = vault.get_secret_sync("platform/infrastructure")
            if infra_secrets:
                for k, v in infra_secrets.items():
                    if k not in os.environ:
                        os.environ[k] = v
            
            # Load Platform Secrets
            platform_secrets = vault.get_secret_sync("platform/brain-gateway")
            if platform_secrets:
                for k, v in platform_secrets.items():
                    if k not in os.environ:
                        os.environ[k] = v
            
            print("INFO: Vault secrets loaded successfully.")
    except Exception as e:
        print(f"WARNING: Vault early loading failed: {e}. Falling back to .env")

load_dotenv()
load_vault_secrets_sync()

from app.models.mcp import McpRegistry, McpCategory
from app.dependencies import SessionLocal
from app.services.mcp_curator import McpCuratorService

AWESOME_MCP_URL = "https://raw.githubusercontent.com/punkpeye/awesome-mcp-servers/main/README.md"

def get_category_map(db: Session, categories: dict):
    """
    Ensures categories exist and returns a map of slug -> id
    """
    cat_map = {}
    for slug, data in categories.items():
        cat = db.query(McpCategory).filter(McpCategory.slug == slug).first()
        if not cat:
            cat = McpCategory(slug=slug, **data)
            db.add(cat)
            db.commit()
            db.refresh(cat)
        cat_map[slug] = cat.id
    return cat_map

def parse_readme(text: str):
    """
    Parses the README markdown to extract MCP servers and their categories.
    Returns a list of dicts.
    """
    servers = []
    current_category = "other-tools-and-integrations" # Default
    
    # Map header text to our category slugs (Aligned with seed_mcp.py)
    header_to_slug = {
        "Cloud Platforms": "utilities",
        "Databases": "utilities",
        "Developer Tools": "utilities",
        "Communication": "communication",
        "Search": "analytics",
        "CMS": "cms",
        "Ecommerce": "ecommerce",
        "Finance & Fintech": "billing-revenue",
        "Browser Automation": "utilities",
        "AI": "analytics",
    }
    
    category_definitions = {
        "ecommerce": {"name": "E-commerce", "description": "Online store platforms", "icon": "ShoppingCart", "sort_order": 1},
        "crm": {"name": "CRM", "description": "Customer Relationship Management", "icon": "Users", "sort_order": 2},
        "cms": {"name": "CMS", "description": "Content Management Systems", "icon": "FileText", "sort_order": 3},
        "email-marketing": {"name": "Email Marketing", "description": "Email campaigns & automation", "icon": "Mail", "sort_order": 4},
        "billing-revenue": {"name": "Billing & Revenue", "description": "Payments, Invoicing & Subscriptions", "icon": "CreditCard", "sort_order": 5},
        "project-management": {"name": "Project Management", "description": "Tasks, boards and team workflows", "icon": "CheckSquare", "sort_order": 6},
        "analytics": {"name": "Analytics", "description": "Web & product analytics", "icon": "BarChart", "sort_order": 7},
        "advertising": {"name": "Advertising", "description": "Ad platforms", "icon": "Megaphone", "sort_order": 8},
        "communication": {"name": "Communication", "description": "Messaging & chat", "icon": "MessageCircle", "sort_order": 9},
        "utilities": {"name": "Utilities", "description": "Storage and automation tools", "icon": "Terminal", "sort_order": 10},
    }

    lines = text.split('\n')
    
    # Regex for headers: ### 🚀 <a name="..."></a>Aerospace & Astrodynamics
    header_regex = re.compile(r'^#{2,4}\s+.*<a name=".*"></a>(.+)')
    # Fallback header regex: ## Databases
    simple_header_regex = re.compile(r'^#{2,4}\s+(.+)')
    
    # Regex for list items: - [Name](URL) - Description
    # Matches: - [owner/repo](url) - (emoji)? Description
    link_regex = re.compile(r'^\s*-\s+\[(.*?)\]\((.*?)\)\s*-?\s*(.*)')

    current_cat_slug = "other"

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for header
        h_match = header_regex.match(line)
        if not h_match:
            # Try simple header if it matches ## Header
            if line.startswith('##') and '<a name=' not in line:
                 h_match = simple_header_regex.match(line)

        if h_match:
            header_text = h_match.group(1).strip()
            # Normalize header text to map to our known categories
            text_lower = header_text.lower()
            if any(x in text_lower for x in ["database", "cloud", "developer", "devtools", "automation", "utilities", "browser"]):
                current_cat_slug = "utilities"
            elif any(x in text_lower for x in ["communication", "chat", "slack", "discord", "messaging"]):
                current_cat_slug = "communication"
            elif any(x in text_lower for x in ["search", "analytics", "google", "data"]):
                current_cat_slug = "analytics"
            elif any(x in text_lower for x in ["cms", "content"]):
                current_cat_slug = "cms"
            elif any(x in text_lower for x in ["commerce", "shop"]):
                current_cat_slug = "ecommerce"
            elif any(x in text_lower for x in ["fintech", "finance", "payment", "billing"]):
                current_cat_slug = "billing-revenue"
            elif any(x in text_lower for x in ["project", "task", "collaboration", "notion"]):
                current_cat_slug = "project-management"
            elif any(x in text_lower for x in ["social", "advertising", "marketing", "ads"]):
                current_cat_slug = "advertising"
            else:
                current_cat_slug = "utilities" # Default bucket
            
            continue
            
        # Check for link item
        l_match = link_regex.match(line)
        if l_match:
            name_text = l_match.group(1).strip()
            url = l_match.group(2).strip()
            description = l_match.group(3).strip()
            
            # Clean description (remove leading emojis often found in this list)
            # e.g. "🐍 ☁️ - Description"
            # Remove leading non-alphanumeric chars generously
            # description = re.sub(r'^[^\w\s]+', '', description).strip()
            
            # Extract simple name from "owner/repo" or just use text
            # Often name_text is "Owner/Repo"
            simple_name = name_text
            if "/" in name_text:
                simple_name = name_text.split("/")[-1]
            
            # Slugify
            slug = name_text.replace('/', '-').lower().replace(' ', '-')
            
            # Source type inference
            source_type = 'community'
            if 'Official' in description or 'official' in name_text.lower():
                source_type = 'official'
            
            servers.append({
                "name": simple_name,
                "slug": slug,
                "description": description,
                "source_url": url,
                "category_slug": current_cat_slug,
                "source_type": source_type,
                "creator_org": name_text.split("/")[0] if "/" in name_text else None,
                "is_official": source_type == 'official',
                # Mock some metrics for now since we aren't hitting GitHub API
                "github_stars": 10 if source_type == 'community' else 100 
            })
            
    return servers, category_definitions

async def fetch_github_stars(repo_path: str) -> int:
    """Fetches star count from GitHub API."""
    if not repo_path or "/" not in repo_path:
        return 0
    
    url = f"https://api.github.com/repos/{repo_path}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "BizOSaaS-MCP-Seeder"
    }
    
    # Use token if available in environment
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                return data.get("stargazers_count", 0)
            elif response.status_code == 403:
                # Rate limited
                return -1
    except Exception as e:
        print(f"Failed to fetch stars for {repo_path}: {e}")
    
    return 0

async def seed_live_data():
    print(f"Fetching MCP list from {AWESOME_MCP_URL}...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(AWESOME_MCP_URL, follow_redirects=True)
            response.raise_for_status()
            content = response.text
    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return

    print("Parsing content...")
    servers, category_definitions = parse_readme(content)
    print(f"Found {len(servers)} servers.")
    
    db = SessionLocal()
    try:
        # 1. Setup Categories
        cat_map = get_category_map(db, category_definitions)
        
        # 2. Insert/Update Servers
        print("Fetching GitHub metrics and seeding database...")
        for i, s in enumerate(servers):
            # Fetch real repo name for stars
            repo_path = None
            if "github.com/" in s["source_url"]:
                repo_path = s["source_url"].split("github.com/")[-1].strip("/")
            
            stars = 0
            if repo_path:
                stars = await fetch_github_stars(repo_path)
                if stars == -1: # Rate limited
                    print("GitHub API Rate limited. Using default star counts for remaining items.")
                    stars = 10 if s["source_type"] == 'community' else 100
                    # Don't try anymore
                    # repo_path = None 
                
                # Small delay to be polite
                await asyncio.sleep(0.1)

            existing = db.query(McpRegistry).filter(McpRegistry.slug == s["slug"]).first()
            if not existing:
                # Create new
                mcp = McpRegistry(
                    name=s["name"],
                    slug=s["slug"],
                    description=s["description"],
                    source_url=s["source_url"],
                    source_type=s["source_type"],
                    creator_org=s["creator_org"],
                    is_official=s["is_official"],
                    github_stars=max(0, stars),
                    category_id=cat_map.get(s["category_slug"], cat_map["utilities"]),
                    mcp_config={"type": "unknown", "url": s["source_url"]},
                    capabilities=[]
                )
                McpCuratorService.classify_and_tag(mcp)
                db.add(mcp)
                print(f"[{i+1}/{len(servers)}] Added: {mcp.name} ({stars} stars)")
            else:
                # Update existing
                existing.description = s["description"]
                if stars > 0:
                    existing.github_stars = stars
                McpCuratorService.classify_and_tag(existing)
                print(f"[{i+1}/{len(servers)}] Updated: {existing.name} ({stars} stars)")
            
            # Commit periodically
            if i % 10 == 0:
                db.commit()
        
        db.commit()
        print("Data seeding complete.")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(seed_live_data())
