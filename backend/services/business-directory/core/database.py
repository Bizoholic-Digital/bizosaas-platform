"""
Database Configuration and Connection Management
Provides async database connections, session management, and tenant isolation
"""

from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional
import logging
import asyncio

from .config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Database metadata and base
metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

Base = declarative_base(metadata=metadata)

# Async Engine Configuration
async_engine = create_async_engine(
    settings.DATABASE_URL,
    **settings.database_config,
    poolclass=QueuePool,
    future=True
)

# Sync Engine for Alembic migrations
sync_engine = create_engine(
    settings.DATABASE_URL.replace("+asyncpg", ""),
    **{k: v for k, v in settings.database_config.items() if k != "echo"},
    poolclass=QueuePool,
    future=True
)

# Session factories
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=True,
    autocommit=False
)

SessionLocal = sessionmaker(
    sync_engine,
    autocommit=False,
    autoflush=False
)


class DatabaseManager:
    """
    Database manager for handling connections, sessions, and tenant isolation
    """
    
    def __init__(self):
        self.async_engine = async_engine
        self.sync_engine = sync_engine
        self._async_session_factory = AsyncSessionLocal
        self._session_factory = SessionLocal
    
    async def get_async_session(self) -> AsyncSession:
        """Get async database session"""
        async with self._async_session_factory() as session:
            return session
    
    def get_session(self):
        """Get sync database session"""
        return self._session_factory()
    
    async def health_check(self) -> bool:
        """Check database connectivity"""
        try:
            async with self.async_engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
                return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    async def ensure_extensions(self):
        """Ensure required PostgreSQL extensions are installed"""
        try:
            async with self.async_engine.begin() as conn:
                # Enable pgvector extension for AI embeddings
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                
                # Enable UUID extension
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
                
                # Enable PostGIS for geolocation (if needed)
                try:
                    await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
                except Exception:
                    logger.warning("PostGIS extension not available")
                
                # Enable full-text search extensions
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS unaccent"))
                
                logger.info("Database extensions ensured successfully")
        except Exception as e:
            logger.error(f"Failed to ensure database extensions: {e}")
            raise
    
    async def setup_tenant_isolation(self):
        """Setup Row Level Security for tenant isolation"""
        try:
            async with self.async_engine.begin() as conn:
                # Enable RLS on tenant-scoped tables
                tenant_tables = [
                    "business_listings",
                    "business_reviews", 
                    "business_events",
                    "business_products",
                    "business_coupons",
                    "business_analytics"
                ]
                
                for table in tenant_tables:
                    try:
                        await conn.execute(text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY"))
                        
                        # Create policy for tenant isolation
                        policy_sql = f"""
                        CREATE POLICY IF NOT EXISTS tenant_isolation_{table} ON {table}
                        USING (tenant_id = current_setting('app.current_tenant_id')::uuid)
                        WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::uuid)
                        """
                        await conn.execute(text(policy_sql))
                        
                    except Exception as table_error:
                        logger.warning(f"Could not setup RLS for table {table}: {table_error}")
                
                logger.info("Tenant isolation setup completed")
        except Exception as e:
            logger.error(f"Failed to setup tenant isolation: {e}")
    
    async def set_tenant_context(self, session: AsyncSession, tenant_id: str):
        """Set tenant context for the current session"""
        try:
            await session.execute(
                text("SELECT set_config('app.current_tenant_id', :tenant_id, false)"),
                {"tenant_id": tenant_id}
            )
        except Exception as e:
            logger.error(f"Failed to set tenant context: {e}")
            raise
    
    async def close(self):
        """Close database connections"""
        await self.async_engine.dispose()
        self.sync_engine.dispose()


# Global database manager instance
db_manager = DatabaseManager()


# Dependency for FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for getting database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Tenant-aware database dependency
@asynccontextmanager
async def get_tenant_db(tenant_id: str) -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session with tenant context
    """
    async with AsyncSessionLocal() as session:
        try:
            # Set tenant context
            await db_manager.set_tenant_context(session, tenant_id)
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


class TenantSessionMixin:
    """
    Mixin for tenant-aware database operations
    """
    
    @staticmethod
    async def with_tenant_context(session: AsyncSession, tenant_id: str):
        """Set tenant context for session"""
        await db_manager.set_tenant_context(session, tenant_id)
    
    @staticmethod
    async def get_tenant_session(tenant_id: str) -> AsyncSession:
        """Get session with tenant context"""
        session = AsyncSessionLocal()
        await db_manager.set_tenant_context(session, tenant_id)
        return session


# Database initialization and startup
async def init_db():
    """Initialize database with extensions and RLS"""
    try:
        logger.info("Initializing database...")
        
        # Ensure extensions
        await db_manager.ensure_extensions()
        
        # Setup tenant isolation
        await db_manager.setup_tenant_isolation()
        
        # Create tables (in production, use Alembic migrations)
        if settings.is_development:
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database initialization completed")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


# Health check function
async def check_db_health() -> dict:
    """
    Comprehensive database health check
    """
    health_status = {
        "database": "unhealthy",
        "connection": False,
        "extensions": {},
        "tables": {},
        "performance": {}
    }
    
    try:
        # Basic connectivity
        health_status["connection"] = await db_manager.health_check()
        
        if health_status["connection"]:
            async with async_engine.begin() as conn:
                # Check extensions
                ext_result = await conn.execute(text("""
                    SELECT extname FROM pg_extension 
                    WHERE extname IN ('vector', 'uuid-ossp', 'pg_trgm', 'unaccent')
                """))
                extensions = [row[0] for row in ext_result]
                health_status["extensions"] = {
                    "vector": "vector" in extensions,
                    "uuid": "uuid-ossp" in extensions,
                    "fulltext": "pg_trgm" in extensions and "unaccent" in extensions
                }
                
                # Check table existence
                table_result = await conn.execute(text("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name LIKE 'business_%'
                """))
                tables = [row[0] for row in table_result]
                health_status["tables"] = {
                    "business_listings": "business_listings" in tables,
                    "business_categories": "business_categories" in tables,
                    "business_reviews": "business_reviews" in tables
                }
                
                # Performance check (query timing)
                import time
                start_time = time.time()
                await conn.execute(text("SELECT COUNT(*) FROM pg_stat_database"))
                query_time = time.time() - start_time
                health_status["performance"] = {
                    "query_time_ms": round(query_time * 1000, 2),
                    "status": "good" if query_time < 0.1 else "slow"
                }
            
            health_status["database"] = "healthy"
    
    except Exception as e:
        health_status["error"] = str(e)
        logger.error(f"Database health check error: {e}")
    
    return health_status


# Cleanup function
async def cleanup_db():
    """Cleanup database connections"""
    try:
        await db_manager.close()
        logger.info("Database cleanup completed")
    except Exception as e:
        logger.error(f"Database cleanup error: {e}")