import os
import sys
from sqlalchemy import text
sys.path.append(os.getcwd())
from app.dependencies import engine

def migrate():
    with engine.connect() as conn:
        print("Migrating mcp_registry table to V2...")
        
        columns = [
            ("source_type", "VARCHAR(50) DEFAULT 'community'"),
            ("package_name", "VARCHAR(255)"),
            ("hosted_url", "VARCHAR(500)"),
            ("documentation_url", "VARCHAR(500)"),
            ("creator_name", "VARCHAR(255)"),
            ("creator_org", "VARCHAR(255)"),
            ("github_stars", "INTEGER DEFAULT 0"),
            ("github_forks", "INTEGER DEFAULT 0"),
            ("last_commit_date", "TIMESTAMP WITH TIME ZONE"),
            ("is_maintained", "BOOLEAN DEFAULT TRUE"),
            ("security_audit_status", "VARCHAR(50) DEFAULT 'not_required'"),
            ("quality_score", "INTEGER DEFAULT 50"),
            ("tags", "JSON DEFAULT '[]'"),
            ("is_recommended", "BOOLEAN DEFAULT FALSE"),
            ("vendor_name", "VARCHAR(100)"),
            ("affiliate_link", "VARCHAR(255)"),
            ("sort_order", "INTEGER DEFAULT 0"),
            ("is_featured", "BOOLEAN DEFAULT FALSE"),
            ("external_id", "VARCHAR(100)"),
            ("sync_metadata", "JSON")
        ]
        
        for col_name, col_type in columns:
            try:
                # Add column if not exists
                conn.execute(text(f"ALTER TABLE mcp_registry ADD COLUMN {col_name} {col_type}"))
                conn.commit()
                print(f"Added {col_name}")
            except Exception as e:
                conn.rollback()
                if "DuplicateColumn" in str(e) or "already exists" in str(e):
                    print(f"Column {col_name} already exists.")
                else:
                    print(f"Error adding {col_name}: {e}")
            
        conn.commit()
        print("Migration complete.")

if __name__ == "__main__":
    migrate()
