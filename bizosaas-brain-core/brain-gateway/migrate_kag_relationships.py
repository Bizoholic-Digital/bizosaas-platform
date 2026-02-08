
import os
import sys
from sqlalchemy import create_engine, text

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

def apply_migration():
    if not DATABASE_URL:
        print("DATABASE_URL not set")
        return
        
    print(f"Connecting to database...")
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            print("Checking if 'kag_relationships' table exists...")
            result = connection.execute(text("SELECT to_regclass('public.kag_relationships')"))
            table_exists = result.scalar()
            
            if table_exists:
                print("Table 'kag_relationships' already exists. Skipping creation.")
            else:
                print("Table 'kag_relationships' does not exist. Creating...")
                create_table_sql = """
                CREATE TABLE kag_relationships (
                    id UUID PRIMARY KEY,
                    source_tool VARCHAR(100) NOT NULL,
                    target_tool VARCHAR(100) NOT NULL,
                    relationship_type VARCHAR(50) NOT NULL,
                    strength INTEGER DEFAULT 10,
                    evidence_count INTEGER DEFAULT 1,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX idx_kag_source ON kag_relationships (source_tool);
                CREATE INDEX idx_kag_target ON kag_relationships (target_tool);
                """
                connection.execute(text(create_table_sql))
                connection.commit()
                print("Table 'kag_relationships' created successfully!")

    except Exception as e:
        print(f"Error applying migration: {e}")

if __name__ == "__main__":
    apply_migration()
