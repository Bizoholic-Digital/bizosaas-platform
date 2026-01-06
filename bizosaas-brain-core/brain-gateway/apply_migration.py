
import os
import sys
from sqlalchemy import create_engine, text

# Add parent directory to path to import models if needed
sys.path.append(os.getcwd())

# Database URL from environment or hardcoded fallback for staging
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:BizOSaaS2025%21StagingDB@localhost:5432/bizosaas_staging")

def apply_migration():
    print(f"Connecting to database: {DATABASE_URL}")
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            print("Checking if 'partner_managed_tenants' table exists...")
            result = connection.execute(text("SELECT to_regclass('public.partner_managed_tenants')"))
            table_exists = result.scalar()
            
            if table_exists:
                print("Table 'partner_managed_tenants' already exists. Skipping creation.")
            else:
                print("Table 'partner_managed_tenants' does not exist. Creating...")
                create_table_sql = """
                CREATE TABLE partner_managed_tenants (
                    user_id UUID NOT NULL,
                    tenant_id UUID NOT NULL,
                    PRIMARY KEY (user_id, tenant_id),
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (tenant_id) REFERENCES tenants (id)
                );
                """
                connection.execute(text(create_table_sql))
                # connection.commit() # SQLAlchemy 1.4+ with future=True or 2.0 requires commit, but engine.connect auto-commits DDL in some configs or needs explicit commit
                connection.commit()
                print("Table 'partner_managed_tenants' created successfully!")

    except Exception as e:
        print(f"Error applying migration: {e}")

if __name__ == "__main__":
    apply_migration()
