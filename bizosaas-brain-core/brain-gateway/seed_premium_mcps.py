
import uuid
import os
import sys
from datetime import datetime
from app.dependencies import SessionLocal
from app.models.mcp import McpRegistry, McpCategory

def seed():
    db = SessionLocal()
    try:
        # Get SEO category
        category = db.query(McpCategory).filter(McpCategory.slug == 'seo').first()
        if not category:
            print("SEO category not found, creating...")
            category = McpCategory(
                id=uuid.uuid4(),
                name="SEO & Analytics",
                slug="seo",
                description="Search Engine Optimization and Web Analytics tools"
            )
            db.add(category)
            db.commit()
            db.refresh(category)

        # Semrush
        semrush = db.query(McpRegistry).filter(McpRegistry.slug == 'semrush').first()
        if not semrush:
            semrush = McpRegistry(
                id=uuid.uuid4(),
                name="Semrush",
                slug="semrush",
                description="Comprehensive SEO suite for keyword research and domain analysis",
                category_id=category.id,
                source_type="official",
                mcp_config={"type": "http", "url": "http://semrush-mcp:8000"},
                capabilities=["keyword_research", "domain_analysis", "backlink_audit"],
                is_official=True,
                is_verified=True
            )
            db.add(semrush)
            print("Seeded Semrush")
        else:
            print("Semrush already exists")

        # Ahrefs
        ahrefs = db.query(McpRegistry).filter(McpRegistry.slug == 'ahrefs').first()
        if not ahrefs:
            ahrefs = McpRegistry(
                id=uuid.uuid4(),
                name="Ahrefs",
                slug="ahrefs",
                description="Powerful backlink and SEO analysis tool",
                category_id=category.id,
                source_type="official",
                mcp_config={"type": "http", "url": "http://ahrefs-mcp:8000"},
                capabilities=["site_explorer", "keyword_explorer", "content_explorer"],
                is_official=True,
                is_verified=True
            )
            db.add(ahrefs)
            print("Seeded Ahrefs")
        else:
            print("Ahrefs already exists")

        db.commit()
        print("Done.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
