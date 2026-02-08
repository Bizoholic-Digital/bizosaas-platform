import os
import sys
from sqlalchemy import text
sys.path.append(os.getcwd())
from app.dependencies import engine

def migrate():
    with engine.connect() as conn:
        print("Running missing columns migration...")
        
        # Define missing columns for 'workflows' table
        workflow_columns = [
            ("workflow_blueprint", "JSON"),
            ("triggers", "JSON DEFAULT '[]'"),
            ("last_run_id", "VARCHAR"),
            ("hitl_enabled", "BOOLEAN DEFAULT TRUE"),
            ("approved_by", "VARCHAR"),
            ("approved_at", "TIMESTAMP"),
            ("success_rate", "FLOAT DEFAULT 100.0"),
            ("runs_today", "INTEGER DEFAULT 0"),
            ("category", "VARCHAR DEFAULT 'all'")
        ]
        
        # Define missing columns for 'users' table
        user_columns = [
            ("tenant_id", "UUID"),
            ("role", "VARCHAR(20) DEFAULT 'user'"),
            ("hashed_password", "VARCHAR(1024)"),
            ("first_name", "VARCHAR(50)"),
            ("last_name", "VARCHAR(50)"),
            ("is_active", "BOOLEAN DEFAULT TRUE"),
            ("is_superuser", "BOOLEAN DEFAULT FALSE"),
            ("is_verified", "BOOLEAN DEFAULT FALSE"),
            ("login_count", "INTEGER DEFAULT 0"),
            ("two_factor_enabled", "BOOLEAN DEFAULT FALSE"),
            ("marketing_consent", "BOOLEAN DEFAULT FALSE"),
            ("failed_login_attempts", "INTEGER DEFAULT 0"),
            ("phone", "VARCHAR(20)"),
            ("avatar_url", "VARCHAR(255)"),
            ("permissions", "JSON"),
            ("last_login_at", "TIMESTAMP WITH TIME ZONE"),
            ("last_activity_at", "TIMESTAMP WITH TIME ZONE"),
            ("allowed_platforms", "JSON"),
            ("platform_preferences", "JSON"),
            ("locked_until", "TIMESTAMP WITH TIME ZONE"),
            ("password_changed_at", "TIMESTAMP WITH TIME ZONE"),
            ("two_factor_secret", "VARCHAR(32)"),
            ("terms_accepted_at", "TIMESTAMP WITH TIME ZONE"),
            ("privacy_accepted_at", "TIMESTAMP WITH TIME ZONE")
        ]

        # Migrate Workflows
        for col_name, col_type in workflow_columns:
            try:
                conn.execute(text(f"ALTER TABLE workflows ADD COLUMN {col_name} {col_type}"))
                conn.commit()
                print(f"Added column workflows.{col_name}")
            except Exception as e:
                conn.rollback()
                if "DuplicateColumn" in str(e) or "already exists" in str(e):
                    print(f"Column workflows.{col_name} already exists.")
                else:
                    print(f"Error adding workflows.{col_name}: {e}")

        # Migrate Users
        for col_name, col_type in user_columns:
            try:
                # User columns might have NOT NULL constraints in model but we must add them as NULLable first 
                # or with default to avoid errors on existing rows. 
                # For simplicity in this rescue script, we add them without NOT NULL constraint if possible, 
                # or rely on the DEFAULT provided.
                conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}"))
                conn.commit()
                print(f"Added column users.{col_name}")
            except Exception as e:
                conn.rollback()
                if "DuplicateColumn" in str(e) or "already exists" in str(e):
                    print(f"Column users.{col_name} already exists.")
                else:
                    print(f"Error adding users.{col_name}: {e}")

        print("Missing columns migration complete.")

if __name__ == "__main__":
    migrate()
