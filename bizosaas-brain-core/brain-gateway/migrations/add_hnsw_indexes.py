"""
Database migration: Add HNSW indexing to knowledge_chunks table.

This migration enhances the vector search performance by:
1. Adding HNSW (Hierarchical Navigable Small World) index for sub-linear ANN search
2. Adding tenant_id index for efficient tenant-scoped queries
3. Adding composite index for common query patterns

Run this migration against your NeonDB PostgreSQL instance.
"""

import os
import logging
import sqlalchemy as sa
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration(db_url: str):
    """Execute the migration"""
    engine = sa.create_engine(db_url)
    
    with engine.connect() as conn:
        try:
            # Ensure pgvector extension is enabled
            logger.info("Ensuring pgvector extension is enabled...")
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
            
            # Check if HNSW index already exists
            result = conn.execute(text("""
                SELECT indexname FROM pg_indexes 
                WHERE tablename = 'knowledge_chunks' 
                AND indexname = 'idx_knowledge_chunks_hnsw'
            """))
            
            if result.fetchone():
                logger.info("HNSW index already exists, skipping...")
            else:
                logger.info("Creating HNSW index on embedding column...")
                conn.execute(text("""
                    CREATE INDEX idx_knowledge_chunks_hnsw 
                    ON knowledge_chunks 
                    USING hnsw (embedding vector_cosine_ops)
                    WITH (m = 16, ef_construction = 64)
                """))
                logger.info("✓ HNSW index created successfully")
            
            # Add tenant_id index if not exists
            result = conn.execute(text("""
                SELECT indexname FROM pg_indexes 
                WHERE tablename = 'knowledge_chunks' 
                AND indexname = 'idx_knowledge_chunks_tenant'
            """))
            
            if result.fetchone():
                logger.info("Tenant index already exists, skipping...")
            else:
                logger.info("Creating index on tenant_id...")
                conn.execute(text("""
                    CREATE INDEX idx_knowledge_chunks_tenant 
                    ON knowledge_chunks(tenant_id)
                """))
                logger.info("✓ Tenant index created successfully")
            
            # Add composite index for common query pattern (tenant + agent)
            result = conn.execute(text("""
                SELECT indexname FROM pg_indexes 
                WHERE tablename = 'knowledge_chunks' 
                AND indexname = 'idx_knowledge_chunks_tenant_agent'
            """))
            
            if result.fetchone():
                logger.info("Composite index already exists, skipping...")
            else:
                logger.info("Creating composite index on (tenant_id, agent_id)...")
                conn.execute(text("""
                    CREATE INDEX idx_knowledge_chunks_tenant_agent 
                    ON knowledge_chunks(tenant_id, agent_id)
                """))
                logger.info("✓ Composite index created successfully")
            
            # Add created_at index for time-based queries
            result = conn.execute(text("""
                SELECT indexname FROM pg_indexes 
                WHERE tablename = 'knowledge_chunks' 
                AND indexname = 'idx_knowledge_chunks_created_at'
            """))
            
            if result.fetchone():
                logger.info("Created_at index already exists, skipping...")
            else:
                logger.info("Creating index on created_at...")
                conn.execute(text("""
                    CREATE INDEX idx_knowledge_chunks_created_at 
                    ON knowledge_chunks(created_at DESC)
                """))
                logger.info("✓ Created_at index created successfully")
            
            conn.commit()
            logger.info("\n✅ Migration completed successfully!")
            
            # Show index information
            logger.info("\nCurrent indexes on knowledge_chunks:")
            result = conn.execute(text("""
                SELECT indexname, indexdef 
                FROM pg_indexes 
                WHERE tablename = 'knowledge_chunks'
                ORDER BY indexname
            """))
            for row in result:
                logger.info(f"  - {row.indexname}")
            
        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            conn.rollback()
            raise

if __name__ == "__main__":
    # Get database URL from environment or use default
    db_url = os.getenv("VECTOR_DB_URL") or os.getenv("DATABASE_URL")
    
    if not db_url:
        logger.error("❌ DATABASE_URL or VECTOR_DB_URL environment variable not set")
        logger.info("Please set one of these variables to your NeonDB connection string")
        logger.info("Example: postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/dbname")
        exit(1)
    
    logger.info(f"Running migration against: {db_url.split('@')[1] if '@' in db_url else 'database'}")
    run_migration(db_url)
