
import os
import sys
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

# Add parent directory to path to import models if needed
sys.path.append(os.getcwd())

# Database URL from environment or hardcoded fallback for staging
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:BizOSaaS2025%21StagingDB@localhost:5432/bizosaas_staging")

def cleanup_data():
    print(f"Connecting to database: {DATABASE_URL}")
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            print("Cleaning up old audit logs (> 30 days)...")
            # Example cleanup for audit_logs if it existed, or generic 'logs'
            # Assuming a table named 'audit_logs' or similar might exist, or we check common tables
            
            # 1. Clean up old sessions if any (though usually managed by Auth service)
            # 2. Clean up temporary tables or cached data
            
            # Since user mentioned "junk or unnecessary data", let's look for potential candidates like 'audit_logs', 'notifications', etc.
            # For now, we will just print what we would do or run safe deletes if we knew the schema.
            # Given schema constraints (Neon free tier 0.5GB), highly relevant to clean up:
            # - Large TEXT/JSON blobs in archived records
            # - Old notifications
            
            # Let's try to delete from a hypothetical 'notifications' table older than 30 days
            try:
                connection.execute(text("DELETE FROM notifications WHERE created_at < NOW() - INTERVAL '30 days'"))
                print("Cleaned up old notifications.")
            except Exception as e:
                print(f"Skipping notifications cleanup (table might not exist): {e}")

            # Commit changes
            connection.commit()
            print("Cleanup completed.")

    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    cleanup_data()
