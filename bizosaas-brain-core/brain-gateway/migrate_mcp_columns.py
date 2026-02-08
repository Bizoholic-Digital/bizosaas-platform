import os
import sys
from sqlalchemy import text
sys.path.append(os.getcwd())
from app.dependencies import engine

def migrate():
    with engine.connect() as conn:
        print("Migrating mcp_registry table...")
        
        columns = [
            ("vendor_name", "VARCHAR(100)"),
            ("affiliate_link", "VARCHAR(255)"),
            ("sort_order", "INTEGER DEFAULT 0"),
            ("is_featured", "BOOLEAN DEFAULT FALSE"),
            ("external_id", "VARCHAR(100)"),
            ("sync_metadata", "JSON")
        ]
        
        for col_name, col_type in columns:
            try:
                # Check if column exists
                # This is a bit hacky for cross-db compatibility but works for postgres usually if we catch error
                conn.execute(text(f"ALTER TABLE mcp_registry ADD COLUMN {col_name} {col_type}"))
                conn.commit()
                print(f"Added {col_name}")
            except Exception as e:
                # Need to rollback if transaction is aborted
                conn.rollback()
                if "DuplicateColumn" in str(e) or "already exists" in str(e):
                     print(f"Column {col_name} already exists.")
                else:
                    print(f"Error adding {col_name}: {e}")
            
        conn.commit()
        print("Migration complete.")

if __name__ == "__main__":
    migrate()
