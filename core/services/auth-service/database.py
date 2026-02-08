"""
Database configuration for BizOSaaS Authentication Service
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://admin:admin@infrastructure-shared-postgres:5432/bizosaas_auth"
)

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Create async session factory
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Base class for models
Base = declarative_base()

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database sessions"""
    async with async_session_maker() as session:
        yield session

async def create_db_and_tables():
    """Create database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
