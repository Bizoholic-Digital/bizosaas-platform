import os
import sys
import uuid
from datetime import datetime

# Add current directory to path so imports work
sys.path.append(os.getcwd())

from app.dependencies import SessionLocal
from app.models.mcp import McpCategory, McpRegistry

def seed_google_mcps():
    db = SessionLocal()
    try:
        print("Seeding Google MCPs into Registry...")
        
        # 1. Ensure Categories Exist
        analytics_cat = db.query(McpCategory).filter_by(slug="analytics").first()
        if not analytics_cat:
            analytics_cat = McpCategory(
                name="Analytics", 
                slug="analytics", 
                description="Web & product analytics", 
                icon="BarChart", 
                sort_order=7
            )
            db.add(analytics_cat)
            db.flush()

        search_cat = db.query(McpCategory).filter_by(slug="search").first()
        if not search_cat:
            search_cat = McpCategory(
                name="Search & Research", 
                slug="search", 
                description="SEO and Web Data Research", 
                icon="Search", 
                sort_order=11
            )
            db.add(search_cat)
            db.flush()

        # 2. Define Google MCPs
        google_mcps = [
            {
                "name": "Google Search Console",
                "slug": "google-search-console",
                "category_id": search_cat.id,
                "description": "Access search analytics, URL inspection, and site management for Google Search.",
                "vendor_name": "Google",
                "is_official": True,
                "is_featured": True,
                "capabilities": ["search_analytics", "url_inspection", "sitemaps", "site_management"],
                "mcp_config": {
                    "type": "docker",
                    "image": "bizosaas/mcp-google-search-console:latest",
                    "env": ["GOOGLE_CLOUD_PROJECT", "GOOGLE_APPLICATION_CREDENTIALS"]
                }
            },
            {
                "name": "Google Analytics 4",
                "slug": "google-analytics",
                "category_id": analytics_cat.id,
                "description": "Standard web analytics, user behavior, and conversion tracking.",
                "vendor_name": "Google",
                "is_official": True,
                "is_featured": True,
                "capabilities": ["traffic_reports", "user_metrics", "conversions", "realtime_data"],
                "mcp_config": {
                    "type": "docker",
                    "image": "bizosaas/mcp-google-analytics:latest",
                    "env": ["GA4_PROPERTY_ID", "GOOGLE_APPLICATION_CREDENTIALS"]
                }
            }
        ]

        for mcp_data in google_mcps:
            existing = db.query(McpRegistry).filter_by(slug=mcp_data["slug"]).first()
            if not existing:
                mcp = McpRegistry(**mcp_data)
                db.add(mcp)
                print(f"Registered MCP: {mcp.name}")
            else:
                for key, value in mcp_data.items():
                    setattr(existing, key, value)
                print(f"Updated MCP: {existing.name}")

        db.commit()
        print("Google MCP Registry seeding completed successfully!")
        
    except Exception as e:
        print(f"Error seeding Google MCPs: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_google_mcps()
